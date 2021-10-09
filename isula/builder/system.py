from isula.builder_grpc import control_pb2


class System(object):
    def __init__(self, client):
        self.client = client

    def version(self):
        """Version requests version information of isula-builder"""
        pass

    def healthCheck(self):
        """HealthCheck requests a health checking in isula-builder"""        
        pass

    def login(self):
        """Login requests to access image registry with username and password"""
        pass

    def logout(self):
        """Logout requests to logout registry and delete any credentials"""
        pass

    def info(self):
        """Info requests isula-build system information"""
        pass
