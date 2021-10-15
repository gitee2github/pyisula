from isula.isulad_grpc import api_pb2


class CRIRuntime(object):
    def __init__(self, client):
        self.client = client

    def version(self, version):
        """Version requests version information of isulad Runtime"""
        request = api_pb2.VersionRequest(version=version)
        response = self.client.Version(request)
        return response

    def list_containers(self, query_filter):
        """Get list of containers"""
        request = api_pb2.ListContainersRequest(filter=query_filter)
        response = self.client.ListContainers(request)
        return response


class CRIImage(object):
    def __init__(self, client):
        self.client = client

    def list_images(self, query_filter):
        """Get list of images"""
        request = api_pb2.ListImagesRequest(filter=query_filter)
        response = self.client.ListImages(request)
        return response
