from isula.builder_grpc import control_pb2


class Manifest(object):
    def __init__(self, client):
        self.client = client

    def manifestCreate(self):
        """ManifestCreate requests to create manifest list"""
        pass

    def manifestAnnotate(self):
        """ManifestAnnotate requests to annotate manifest list"""
        pass

    def manifestInspect(self):
        """ManifestInspect requests to inspect manifest list"""
        pass

    def manifestPush(self):
        """ManifestPush requests to push manifest list"""
        pass
