import grpc

from isula.builder import image
from isula.builder import manifest
from isula.builder import system
from isula.builder_grpc import control_pb2_grpc


class Client(object):
    def __init__(self, channel_target):
        if not channel_target:
            channel_target = 'unix:///run/isula_build.sock'
        channel = grpc.insecure_channel(channel_target)
        client = control_pb2_grpc.ControlStub(channel)

        self.__image = image.Image(client)
        self.__manifest = manifest.Manifest(client)
        self.__system = system.System(client)

    def list_image(self):
        return self.__image.list()
