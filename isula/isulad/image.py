from isula.isulad_grpc import images_pb2


class Image(object):
    def __init__(self, client):
        self.client = client

    def list(self, filters):
        """Get list of images"""
        request = images_pb2.ListImagesRequest(filters=filters)
        response = self.client.List(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response
