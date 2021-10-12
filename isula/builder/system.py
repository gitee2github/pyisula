from isula.builder_grpc import control_pb2


class System(object):
    def __init__(self, client):
        self.client = client

    def version(self):
        """Version requests version information of isula-builder"""
        request = control_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self.client.Version(request)
        return response

    def healthCheck(self):
        """HealthCheck requests a health checking in isula-builder"""        
        request = control_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self.client.HealthCheck(request)
        return response

    def login(self, server, username, password):
        """Login requests to access image registry with username and password"""
        request = control_pb2.LoginRequest(server=server, username=username, password=password)
        response = self.client.Login(request)
        return response

    def logout(self, server, is_all):
        """Logout requests to logout registry and delete any credentials"""
        request = control_pb2.LogoutRequest(server=server, all=is_all)
        response = self.client.Logout(request)
        return response

    def info(self, verbose):
        """Info requests isula-build system information"""
        request = control_pb2.InfoRequest(verbose=verbose)
        response = self.client.Info(request)
        return response
