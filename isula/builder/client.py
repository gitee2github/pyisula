import base64
import codecs

from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from google.protobuf.json_format import MessageToDict
import grpc

from isula.builder import image
from isula.builder import manifest
from isula.builder import system
from isula.builder_grpc import control_pb2_grpc


def toDict(fn):
    def wrap(*args, **kwargs):
        response = fn(*args, **kwargs)
        response = MessageToDict(response)
        return response
    return wrap


class Client(object):
    def __init__(self, channel_target, public_key_path):
        if not channel_target:
            channel_target = 'unix:///run/isula_build.sock'
        if not public_key_path:
            public_key_path = '/etc/isula-build/isula-build.pub'
            with open(public_key_path, "r") as key_file:
                # isula-build public key file is PKCS#1 format by default. we should decode it to get der info first.
                derdata = base64.b64decode('\n'.join(key_file.read().splitlines()[1:-1]))
                self.public_key = serialization.load_der_public_key(
                    derdata, backend=backends.default_backend())
        else:
            with open(public_key_path, "rb") as key_file:
                self.public_key = serialization.load_pem_public_key(
                    key_file.read(), backend=backends.default_backend())

        channel = grpc.insecure_channel(channel_target)
        client = control_pb2_grpc.ControlStub(channel)

        self.__image = image.Image(client)
        self.__manifest = manifest.Manifest(client)
        self.__system = system.System(client)

    @toDict
    def server_version(self):
        '''Get the version of isuld-builder server.

        :returns: dict -- the version of isuld-builder server
        '''
        return self.__system.version()

    @toDict
    def server_healthcheck(self):
        '''Get the status of isuld-builder server.

        :returns: dict -- the status of isuld-builder server
        '''
        return self.__system.healthCheck()

    @toDict
    def server_info(self, verbose=False):
        '''Get the detail infomation of isuld-builder server.

        :param verbose(boolean): whether get the mem or heap usage info. False by default.
        :returns: dict -- the detail infomation of isuld-builder server
        '''
        return self.__system.info(verbose)

    @toDict
    def login(self, server, username, password):
        '''Login image registry

        :param server(string): image registry address
        :param username(string): user name for login
        :param password(string): user password for login
        :returns: dict -- Login result
        '''
        # isula-build accept password as hexadecimal encoding string which encrypted by RSA-SHA512
        encrypted_password_byte = self.public_key.encrypt(
            password.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None,
            )
        )
        encrypted_password = codecs.encode(encrypted_password_byte, 'hex_codec')

        return self.__system.login(server, username, encrypted_password)

    @toDict
    def logout(self, server, is_all=False):
        '''Logout image registry

        :param server(string): image registry address
        :param is_all(boolean): Whether login from all registry. False by default.
        :returns: dict -- Logout result
        '''
        return self.__system.logout(server, is_all)

    @toDict
    def list_image(self):
        return self.__image.list()
