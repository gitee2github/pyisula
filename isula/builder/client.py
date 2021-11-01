import base64
import codecs
import hashlib
import json
import os
from datetime import datetime
import uuid

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
from isula import utils


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

    @utils.response2dict
    def server_version(self):
        """Get the version of isula-builder.

        :returns: dict -- the version of isula-builder
        """
        return self.__system.version()

    @utils.response2dict
    def server_healthcheck(self):
        """Get the status of isula-builder.

        :returns: dict -- the status of isula-builder
        """
        return self.__system.healthCheck()

    @utils.response2dict
    def server_info(self, verbose=False):
        """Get the detail information of isula-builder

        :param verbose(boolean): whether get the mem or heap usage info. False by default.
        :returns: dict -- the detail infomation of isula-builder server
        """
        return self.__system.info(verbose)

    @utils.response2dict
    def login(self, server, username, password):
        """Login image registry

        :param server(string): image registry address
        :param username(string): user name for login
        :param password(string): user password for login
        :returns: dict -- Login result
        """
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

    @utils.response2dict
    def logout(self, server, is_all=False):
        """Logout image registry

        :param server(string): image registry address
        :param is_all(boolean): Whether login from all registry. False by default.
        :returns: dict -- Logout result
        """
        return self.__system.logout(server, is_all)

    @utils.response2dict
    def create_manifest(self, manifestList, manifests):
        """Create manifest list.

        :param manifestList(string): the manifest list name.
        :param manifests(List[string]): a list of images which contains manifest.
        :returns: dict -- contains the new created manifest list id.
        """
        return self.__manifest.manifestCreate(manifestList, manifests)

    def annotate_manifest(self, manifestList, target_manifest, arch='',
                          operation_system='', osFeatures=None, variant=''):
        """Update manifest list.

        :param manifestList(string): the manifest list name.
        :param target_manifest(string): the image which manifest will be updated.
        :param arch(string): the architecture of the image
        :param operation_system(string): the operating system of the image
        :param osFeatures(List[string]): a list of operating system features of the image
        :param variant(string): the other info of the image
        :returns: None
        """
        osFeatures = [] if not osFeatures else osFeatures
        self.__manifest.manifestAnnotate(manifestList, target_manifest, arch,
            operation_system ,osFeatures, variant)

    def inspect_manifest(self, manifestList):
        """Get manifest list information.

        :param manifestList(string): the manifest list name.
        :returns: dict -- the detail infomation of the specifed manifest list.
        """
        encoded_response = self.__manifest.manifestInspect(manifestList)
        return json.loads(base64.b64decode(MessageToDict(encoded_response)['data']))

    def push_manifest(self, manifestList, dest, timeout=60):
        """Upload manifest list to the specified registry.

        :param manifestList(string): the manifest list name.
        :param dest(string): the image registry location.
        :param timeout(int/second): timeout. Default is 60 seconds.
        :returns: MultiThreadedRendezvous object -- a grpc async response object.
        """
        # This API return a grpc multithread async reponse object, users should call the corresponding functions the object
        # to get more info. There are some useful functions, such as:
        # MultiThreadedRendezvous.is_active() -- returns whether the push action is active or not.
        # MultiThreadedRendezvous.cancel() -- cancel the push action by hand.
        # MultiThreadedRendezvous.result() -- returns the result of the push action. The thread will be blocked if there is no response.
        # MultiThreadedRendezvous.running() -- returns whether the push action is running or not.
        # MultiThreadedRendezvous.time_remaining() -- returns when the push action will be stopped by timeout mechanism.
        # MultiThreadedRendezvous.details() -- show the detail info of the push action
        return self.__manifest.manifestPush(manifestList, dest, timeout)

    @utils.response2dict
    def list_images(self, image_name=''):
        """List all images in isula-builder

        :param image_name(string): the specifed image name ot list
        :returns: dict - the information of the images.
        """
        return self.__image.list(image_name)

    def build_image(self, dockerfile, output, image_format, context_dir,
                    iidfile='', additional_tag='', build_time=None, build_args=None,
                    cap_list=None, proxy=False, encrypted=False):
        """Build a new image.

        :param dockerfile(string): the location of the DockerFile for image building.
        :param output(string): the location that the image to save.
        :parma image_format(string): the format of the image.
        :parma context_dir(string): the working directory of building context
        :param iidfile(string): the file that the image ID will be wrote to.
        :parama additional_tag(string): the tag will be added to the image.
        :parma build_time(string): the build time for the image. In '%Y-%m-%d %H:%M:%S' format.
        :parma build_args(List[(key, value)]): a list of extra args for image building.
        :parma cap_list(List[(key, value)]): a list of Linux capabilities args for image building.
        :parama proxy(boolean): Whether inherit proxy environment variables from host.
        :parma encrypted(boolean): whether to encrypt buildArgs via gRPC transport.
        :returns: Iterable -- An Iterable object contains the build process log.

        Example:

        from isula import client
        builder_client = client.init_builder_client()
        for log in builder_client.build_image(*arg, **args):
            print log
        """

        transport, location = output.split(':', 1)
        if transport not in ['docker', 'docker-archive', 'docker-daemon',
            'oci', 'oci-archive', 'isulad', 'manifest']:
            raise Exception("the output format is not correct.")
        if transport in ['docker-archive', 'oci-archive']:
            location = os.path.abspath(location)
            output = ':'.join([transport, location])
        if image_format not in ['docker', 'oci']:
            raise Exception("image format should be either docker or oci.")

        with open(dockerfile, 'rb') as content:
            fileContent = content.read()
            hasher = hashlib.sha256()
            hasher.update(fileContent)
            digest = hasher.hexdigest()

        if build_time:
            try:
                entityID = '%s:%s' % (digest, build_time)
                build_time = datetime.strptime(build_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise Exception("build time should be in %Y-%m-%d %H:%M:%S format")
        else:
            current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entityID = '%s:%s' % (digest, current)

        buildID = uuid.uuid4().hex[:12]
        # TODO(wxy): buildType is hard-code by iSulad. Move it to a more common place.
        buildType = 'ctr-img'
        build_args = [] if not build_args else build_args
        cap_list = [] if not cap_list else cap_list
        context_dir = os.path.abspath(context_dir)

        return self.__image.build(
            buildID, buildType, context_dir, fileContent, output, build_args,
            proxy, iidfile, build_time, additional_tag, cap_list, entityID,
            encrypted, image_format)

    def push_image(self, image_name, image_format):
        """Push image to remote repository

        :param image_name(string): the image name, contains repository and tag.
        :param image_format(string): the format of image that pushed to registry.
        :returns: list -- the push process log.
        """
        if image_format not in ['docker', 'oci']:
            raise Exception("image format should be either docker or oci.")
        pushID = uuid.uuid4().hex[:12]

        response = self.__image.push(pushID, image_name, image_format)
        return list(response)

    def pull_image(self, image_name):
        """Pull image from remote repository

        :param: image_name(string): the image name, contains repository and tag.
        :returns: list -- the pull process log.
        """
        pullID = uuid.uuid4().hex[:12]
        response = self.__image.pull(pullID, image_name)
        return list(response)

    def remove_images(self, image_ids=None, is_all=False, prune=False):
        """Remove the specified images

        :param image_ids(List[string]): a list of image ids for removal.
        :param is_all(boolean): delete all images.
        :param prune(boolean): delete all untagge images
        :returns: list -- the removal process log.
        """
        if (image_ids and is_all) or (image_ids and prune) or (is_all and prune):
            raise Exception("You should only pass only one parameter "
                            "from [imageIDs, is_all, prune]")
        if not image_ids and not is_all and not prune:
            raise Exception("You must pass one parameter from "
                            "[imageIDs, is_all, prune]")

        response = self.__image.remove(image_ids, is_all, prune)
        return list(response)

    def load_image(self, path):
        """Load an image tar

        :param path(string): the path of loading file.
        :returns: list -- the load process log.
        """
        path = os.path.abspath(path)
        response = self.__image.load(path)
        return list(response)

    def import_image(self, source, reference):
        """Import a new image

        :param source(string): the path of tarball used for import
        :param reference(string): the reference of the import image
        :returns: list -- the import process log.
        """
        importID = uuid.uuid4().hex[:12]
        source = os.path.abspath(source)
        response = self.__image.import_(importID, source, reference)
        return list(response)

    def tag_image(self, image_id, tag):
        """Tag an image

        :param image_id(string): the id of the image.
        :param tag(string): the new tag
        :return: None
        """
        self.__image.tag(image_id, tag)

    def save_image(self, images, path, image_format):
        """Save the image to tarball

        :param images(List[string]): the images in local storage to save
        :param path(string): the location for output tarball
        :param image_format(string): the format of image saved to archive file.
        :returns: list -- the save process log.
        """
        if image_format not in ['docker', 'oci']:
            raise Exception("image format should be either docker or oci.")
        saveID = uuid.uuid4().hex[:12]
        path = os.path.abspath(path)
        response = self.__image.save(saveID, images, path, image_format)
        return list(response)
