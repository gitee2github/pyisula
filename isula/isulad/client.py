import grpc
import os

from isula.isulad import container
from isula.isulad import cri
from isula.isulad import image
from isula.isulad import volume
from isula.isulad_grpc import api_pb2_grpc
from isula.isulad_grpc import container_pb2_grpc
from isula.isulad_grpc import images_pb2_grpc
from isula.isulad_grpc import volumes_pb2_grpc
from isula import utils


class Client(object):
    def __init__(self, channel_target):
        if not channel_target:
            channel_target = 'unix:///run/isulad.sock'
        channel = grpc.insecure_channel(channel_target)

        container_client = container_pb2_grpc.ContainerServiceStub(channel)
        images_client = images_pb2_grpc.ImagesServiceStub(channel)
        volumes_client = volumes_pb2_grpc.VolumeServiceStub(channel)
        cri_runtime_client = api_pb2_grpc.RuntimeServiceStub(channel)
        cri_images_client = api_pb2_grpc.ImageServiceStub(channel)

        self._container = container.Container(container_client)
        self._images = image.Image(images_client)
        self._volumes = volume.Volume(volumes_client)
        self._cri_runtime = cri.CRIRuntime(cri_runtime_client)
        self._cri_images = cri.CRIImage(cri_images_client)

    @utils.response2dict
    def list_containers(self, filters=None, is_all=False):
        """ List containers

        :param filters(list): Filter output based on conditions provided
        :param all(boolean): Display all containers (default shows just running)
        :returns: dict -- list of containers' info
        """
        return self._container.list(filters, is_all)

    @utils.response2dict
    def cri_runtime_version(self, version=None):
        """ [CRI] Get runtime version info

        :param version(string): input version parameter
        :return: dict -- version information of isulad Runtime
        """
        return self._cri_runtime.version(version)

    @utils.response2dict
    def cri_list_containers(self, query_filter=None):
        """ [CRI] List containers

        :param query_filter(string): Filter output based on conditions provided
        :return: dict -- list of containers' info
        """
        return self._cri_runtime.list_containers(query_filter)

    @utils.response2dict
    def cri_list_images(self, query_filter=None):
        """ [CRI] List images

        :param query_filter(string): Filter output based on conditions provided
        :return:
        """
        return self._cri_images.list_images(query_filter)

    @utils.response2dict
    def list_images(self, filters={}):
        """ [IMAGE] List images

        :param filters(list): Filter output based on conditions provided
        :return: dict -- list of images' info
        """
        for k in filters.keys():
            if k not in ["dangling", "label", "before", "since", "reference"]:
                raise Exception("Only supports the following fields - dangling, label, before, since, reference")

        return self._images.list(filters)

    @utils.response2dict
    def delete_image(self, name, force=False):
        """ [IMAGE] Delete the image in isulad

        :param name(string): The image name that will been deleted
        :param force(bool): Whether to force deletion
        :returns: dict - the result of the operation.
        """
        return self._images.delete(name, force)

    @utils.response2dict
    def load_image(self, file, type, tag=''):
        """ [IMAGE] Import the image exported using the save command.

        :param name(string): The image file that will been loaded
        :param type(string): The type of image - oci embedded external
        :param tag(string): The tag of image that will been named
        :returns: dict - the result of the operation.
        """
        # TODO(ffrog): check whether the type and tag meet the corresponding relationship
        if type not in ["oci", "embedded", "external"]:
            raise Exception("Only supports the following type - oci, embedded, external")
        file = os.path.abspath(file)
        return self._images.load(file, type, tag)

    @utils.response2dict
    def inspect_image(self, id, bformat=False, timeout=120):
        """ [IMAGE] Get the metadata of image

        :param id(string): The image id
        :param bformat(bool): ?
        :param timeout(int): Maximum waiting time
        :returns: dict - the result of the operation.
        """
        return self._images.inspect(id, bformat, timeout)

    @utils.response2dict
    def tag_image(self, src_name, dest_name):
        """ [IMAGE] Tag the image with dest_name for image named src_name

        :param src_name(string): The image name that will been tag
        :param dest_name(string): The new name for origin image
        :returns: dict - the result of the operation.
        """
        return self._images.tag(src_name, dest_name)

    @utils.response2dict
    def import_image(self, file, tag):
        """ [IMAGE] Import a new image

        :param file(string): The file name which been created by command export
        :param tag(string): The tag name for image
        :returns: dict - the result of the operation.
        """
        file = os.path.abspath(file)
        return self._images.import_(file, tag)

    @utils.response2dict
    def login(self, username, password, server, type):
        """ [IMAGE] Login image registry with username and password

        :param username(string): The username of registry
        :param password(string): The password of username for registry
        :param server(string): The address of registry
        :param type(string): The type of image - oci embedded external
        :returns: dict - the result of the operation.
        """
        return self._images.login(username, password, server, type)

    @utils.response2dict
    def logout(self, server, type):
        """ [IMAGE] Logout image registry

        :param server(string): The address of registry
        :param type(string): The type of image - oci embedded external
        :returns: dict - the result of the operation.
        """
        return self._images.logout(server, type)

    @utils.response2dict
    def list_volumes(self):
        """ [VOLUME] List volumes

        :return:  dict -- list of volumes' info
        """
        return self._volumes.list()

    @utils.response2dict
    def remove_volume(self, name):
        """ [VOLUME] Remove the volume

        :param name(string): The volume name that will been removed
        :returns: dict - the result of the operation.
        """
        return self._volumes.remove(name)

    @utils.response2dict
    def prune_volume(self):
        """ [VOLUME] Remove the unused volume

        :returns: dict - the result of the operation.
        """
        return self._volumes.prune()
