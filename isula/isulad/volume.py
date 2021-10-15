from isula.isulad_grpc import volumes_pb2


class Volume(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        """Get list of volumes"""
        request = volumes_pb2.ListVolumeRequest()
        response = self.client.List(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response
