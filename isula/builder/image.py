import threading

from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

from isula.builder_grpc import control_pb2


class ImageBuild(threading.Thread):
    """Build the image"""
    def __init__(self, client, buildID, buildType, contextDir, fileContent,
                 output, buildArgs, proxy, iidfile, build_time, additionalTag,
                 capAddList, entityID, encrypted, image_format):
        super(ImageBuild, self).__init__()
        self.client = client
        self.buildID = buildID
        self.buildType = buildType
        self.contextDir = contextDir
        self.fileContent = fileContent
        self.output = output
        self.buildArgs = buildArgs
        self.proxy = proxy
        self.iidfile = iidfile
        self.build_time = build_time
        self.additionalTag = additionalTag
        self.capAddList = capAddList
        self.entityID = entityID
        self.encrypted = encrypted
        self.image_format = image_format

    def run(self):
        if self.build_time:
            buildTime = Timestamp()
            buildTime.FromDatetime(self.build_time)
            buildStatic = control_pb2.BuildStatic(buildTime=buildTime)
        else:
            buildStatic = None
        request = control_pb2.BuildRequest(
            buildID=self.buildID, buildType=self.buildType,
            contextDir=self.contextDir, fileContent=self.fileContent,
            output=self.output, buildArgs=self.buildArgs, proxy=self.proxy,
            iidfile=self.iidfile, buildStatic=buildStatic,
            additionalTag=self.additionalTag, capAddList=self.capAddList,
            entityID=self.entityID, encrypted=self.encrypted,
            format=self.image_format)
        self.client.Build(request)


class Image(object):
    def __init__(self, client):
        self.client = client

    def list(self, imageName):
        """List all images in isula-builder"""
        request = control_pb2.ListRequest(imageName=imageName)
        response = self.client.List(request)
        return response

    def build(self, buildID, buildType, contextDir, fileContent, output,
              buildArgs, proxy, iidfile, build_time, additionalTag, capAddList,
              entityID, encrypted, image_format):
        """Build a new image"""
        build_process = ImageBuild(self.client, buildID, buildType, contextDir,
            fileContent, output, buildArgs, proxy, iidfile, build_time,
            additionalTag, capAddList, entityID, encrypted, image_format)
        build_process.start()
        # get image building process log back to caller
        request = control_pb2.StatusRequest(buildID=buildID)
        response = self.client.Status(request)
        for message in response:
            yield MessageToDict(message)['content']

    def push(self, pushID, imageName, image_format):
        """Push pushes image to remote repository"""
        request = control_pb2.PushRequest(pushID=pushID, imageName=imageName,
            format=image_format)
        response = self.client.Push(request)
        return response

    def pull(self, pullID, imageName):
        """Pull pulls image from remote repository"""
        request = control_pb2.PullRequest(pullID=pullID, imageName=imageName)
        response = self.client.Pull(request)
        return response

    def remove(self, imageIDs, is_all, prune):
        """Remove sends an image remove request to isula-builder"""
        if imageIDs:
            request = control_pb2.RemoveRequest(imageID=imageIDs)
        elif is_all:
            request = control_pb2.RemoveRequest(all=True)
        elif prune:
            request = control_pb2.RemoveRequest(prune=True)
        response = self.client.Remove(request)
        return response

    def load(self, path):
        """Load requests an image tar load"""
        request = control_pb2.LoadRequest(path=path)
        response = self.client.Load(request)
        return response

    def import_(self, importID, source, reference):
        # 'import' can not be used as function name in python, use 'import_' instead.
        """Import requests import a new image"""
        request = control_pb2.ImportRequest(importID=importID, source=source,
            reference=reference)
        response = self.client.Import(request)
        return response

    def tag(self, imageID, tag):
        """Tag requests to tag an image"""
        request = control_pb2.TagRequest(image=imageID, tag=tag)
        response = self.client.Tag(request)
        return response

    def save(self, saveID, images, path, image_format):
        """Save saves the image to tarball"""
        request = control_pb2.SaveRequest(saveID=saveID, images=images,
            path=path, format=image_format)
        response = self.client.Save(request)
        return response
