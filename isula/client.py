from isula.builder import client as builder_client
from isula.isulad import client as isulad_client


def init_builder_client(channel_target=None):
    return builder_client.Client(channel_target)


def init_isulad_client(channel_target=None):
    return isulad_client.Client(channel_target)
