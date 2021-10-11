import grpc

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
    def list_images(self, filters=None):
        """ List images

        :param filters(list): Filter output based on conditions provided
        :return: dict -- list of images' info
        """
        return self._images.list(filters)

    @utils.response2dict
    def list_volumes(self):
        """ List volumes

        :return:  dict -- list of volumes' info
        """
        return self._volumes.list()

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
