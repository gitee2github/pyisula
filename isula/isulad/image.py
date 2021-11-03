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

    def delete(self, name, force=False):
        """Delete images"""
        request = images_pb2.DeleteImageRequest(name=name, force=force)
        response = self.client.Delete(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def load(self, image_file, image_type, tag):
        """Load the image from tar"""
        request = images_pb2.LoadImageRequest(file=image_file, type=image_type, tag=tag)
        response = self.client.Load(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def inspect(self, image_id, bformat, timeout):
        """Get the metadata of image"""
        request = images_pb2.InspectImageRequest(id=image_id, bformat=bformat, timeout=timeout)
        response = self.client.Inspect(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def tag(self, src_name, dest_name):
        """Tag the image with dest_name for image named src_name"""
        request = images_pb2.TagImageRequest(src_name=src_name, dest_name=dest_name)
        response = self.client.Tag(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def import_(self, import_file, tag):
        # 'import' can not be used as function name in python, use 'import_' instead.
        """Import a new image"""
        request = images_pb2.ImportRequest(file=import_file, tag=tag)
        response = self.client.Import(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def login(self, username, password, server, image_type):
        """Login image registry with username and password"""
        request = images_pb2.LoginRequest(username=username, password=password, server=server, type=image_type)
        response = self.client.Login(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def logout(self, server, image_type):
        """Logout image registry"""
        request = images_pb2.LogoutRequest(server=server, type=image_type)
        response = self.client.Logout(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response
