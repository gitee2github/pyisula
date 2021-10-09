from isula.builder_grpc import control_pb2


class Image(object):
    def __init__(self, client):
        self.client = client

    def list(self):
        """List lists all images in isula-builder"""
        request = control_pb2.ListRequest()
        response = self.client.List(request)
        return response

    def build(self):
        """Build requests a new image building"""
        pass

    def status(self):
        """Status pipes the image building process log back to client"""
        pass

    def push(self):
        """Push pushes image to remote repository"""
        pass

    def pull(self):
        """Pull pulls image from remote repository"""
        pass

    def remove(self):
        """Remove sends an image remove request to isula-builder"""
        pass

    def load(self):
        """Load requests an image tar load"""
        pass

    def Import(self):
        # 'import' can not be used as function name in python, use 'Import' instead.
        """Import requests import a new image"""
        pass

    def tag(self):
        """Tag requests to tag an image"""
        pass

    def save(self):
        """Save saves the image to tarball"""
        pass
