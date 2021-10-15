from isula.isulad_grpc import container_pb2


class Container(object):
    def __init__(self, client):
        self.client = client

    def list(self, filters, is_all):
        """Get list of containers"""
        request = container_pb2.ListRequest(filters=filters, all=is_all)
        response = self.client.List(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response
