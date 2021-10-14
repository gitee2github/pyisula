import base64
import codecs
import json

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
        # manifest API is experimental and disabled by default in isula-build, so if you want to use these APIs,
        # add `experimental = true` into the config file at server side first.
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
    def create_manifest(self, manifestList, manifests):
        '''Create manifest list.

        :param manifestList(string): the manifest list name.
        :param manifests(List[string]): a list of images which contains manifest.
        :returns: dict -- contains the new created manifest list id.
        '''
        return self.__manifest.manifestCreate(manifestList, manifests)

    def annotate_manifest(self, manifestList, target_manifest, arch='', os='', osFeatures=None, variant=''):
        '''Update manifest list.

        :param manifestList(string): the manifest list name.
        :param target_manifest(string): the image which manifest will be updated.
        :param arch(string): the architecture of the image
        :param os(string): the operating system of the image
        :param osFeatures(List[string]): a list of operating system features of the image
        :param variant(string): other info of the image
        returns: None
        '''
        osFeatures = [] if not osFeatures else osFeatures
        self.__manifest.manifestAnnotate(manifestList, target_manifest, arch, os ,osFeatures, variant)

    def inspect_manifest(self, manifestList):
        '''Get create manifest list infomation.

        :param manifestList(string): the manifest list name.
        returns: dict -- the detail infomation of the specifed manifest list.
        '''
        encoded_response = self.__manifest.manifestInspect(manifestList)
        return json.loads(base64.b64decode(MessageToDict(encoded_response)['data']))

    def push_manifest(self, manifestList, dest, timeout=60):
        '''Upload manifest list tot the specified registry.

        :param manifestList(string): the manifest list name.
        :param dest(string): the image registry location.
        :param timeout(int/second): timeout. Default is 60 seconds.
        returns: MultiThreadedRendezvous object -- a grpc async response object.
        '''
        # This API return a grpc multithread async reponse object, users should call the functions the object
        # to get more info. There are some useful functions, such as:
        # MultiThreadedRendezvous.is_active() -- returns whether the push action is active or not.
        # MultiThreadedRendezvous.cancle() -- cancle the push action by hand.
        # MultiThreadedRendezvous.result() -- returns the result of the push action. The thread will be block if there is no result.
        # MultiThreadedRendezvous.running() -- returns whether the push action is running or not.
        # MultiThreadedRendezvous.time_remaining() -- returns when the push action will be stopped by timeout mechanism.
        # MultiThreadedRendezvous.details() -- show the detail info of the push action
        return self.__manifest.manifestPush(manifestList, dest, timeout)

    @toDict
    def list_image(self):
        return self.__image.list()
