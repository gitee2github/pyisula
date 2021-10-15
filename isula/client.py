from isula.builder import client as builder_client
from isula.isulad import client as isulad_client


def init_builder_client(channel_target=None, public_key_path=None):
    """Initialize isula-build client object.

    :param channel_target(string): The location of isula-builder daemon socket file.
    :param public_key_path(string): THe location of isula-builder public key file for encryption.
        The content should be pem format.
    :returns: isula.builder.client.Client -- The python object for isula-build client.
    """
    return builder_client.Client(channel_target, public_key_path)


def init_isulad_client(channel_target=None):
    """Initialize iSulad client object.

    :param channel_target(string): The location of iSulad daemon socket file.
    :returns: isula.isulad.client.Client -- The python object for iSulad client.
    """
    return isulad_client.Client(channel_target)
