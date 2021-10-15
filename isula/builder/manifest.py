from isula.builder_grpc import control_pb2


class Manifest(object):
    def __init__(self, client):
        self.client = client

    def manifestCreate(self, manifestList, manifests):
        """ManifestCreate requests to create manifest list"""
        request = control_pb2.ManifestCreateRequest(manifestList=manifestList, manifests=manifests)
        response = self.client.ManifestCreate(request)
        return response

    def manifestAnnotate(self, manifestList, manifest, arch, os, osFeatures, variant):
        """ManifestAnnotate requests to annotate manifest list"""
        request = control_pb2.ManifestAnnotateRequest(
            manifestList=manifestList,
            manifest=manifest,
            arch=arch,
            os=os,
            osFeatures=osFeatures,
            variant=variant)
        response = self.client.ManifestAnnotate(request)
        return response

    def manifestInspect(self, manifestList):
        """ManifestInspect requests to inspect manifest list"""
        request = control_pb2.ManifestInspectRequest(manifestList=manifestList)
        response = self.client.ManifestInspect(request)
        return response

    def manifestPush(self, manifestList, dest, timeout):
        """ManifestPush requests to push manifest list"""
        request = control_pb2.ManifestPushRequest(manifestList=manifestList, dest=dest)
        response = self.client.ManifestPush(request, timeout=timeout)
        return response
