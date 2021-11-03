import base64
import inspect
import signal
import os

from google.protobuf.json_format import MessageToDict
import grpc

from isula.isulad import container
from isula.isulad import cri
from isula.isulad import image
from isula.isulad import volume
from isula.isulad_grpc import api_pb2_grpc
from isula.isulad_grpc import container_pb2_grpc
from isula.isulad_grpc import images_pb2_grpc
from isula.isulad_grpc import volumes_pb2_grpc
from isula import utils


class Client(object):
    def __init__(self, channel_target):
        if not channel_target:
            channel_target = 'unix:///run/isulad.sock'
        channel = grpc.insecure_channel(channel_target)

        container_client = container_pb2_grpc.ContainerServiceStub(channel)
        images_client = images_pb2_grpc.ImagesServiceStub(channel)
        volumes_client = volumes_pb2_grpc.VolumeServiceStub(channel)
        cri_runtime_client = api_pb2_grpc.RuntimeServiceStub(channel)
        cri_images_client = api_pb2_grpc.ImageServiceStub(channel)

        self._container = container.Container(container_client)
        self._images = image.Image(images_client)
        self._volumes = volume.Volume(volumes_client)
        self._cri_runtime = cri.CRIRuntime(cri_runtime_client)
        self._cri_images = cri.CRIImage(cri_images_client)

    @utils.response2dict
    def create_container(self, container_id, container_image, rootfs=None,
                         runtime='lcr', **kwargs):
        """ Create a container

        :param container_id: identifier of container
        :param container_image: image used for creating container
        :param rootfs: rootfs used for running container, default as '/dev/ram0'
        :param runtime: runtime to use for containers(default: lcr)
        :param kwargs:
            VolumesFrom:
        :return:
        """
        hc_argspec = inspect.getfullargspec(container.HostConfig.__init__).args
        hc_args = {}
        cc_argspec = inspect.getfullargspec(
            container.ContainerConfig.__init__).args
        cc_args = {}
        for k, v in kwargs.items():
            if k in hc_argspec:
                hc_args[k] = v
            if k in cc_argspec:
                cc_args[k] = v

        hostconfig = container.HostConfig(**hc_args).to_json()
        customconfig = container.ContainerConfig(**cc_args).to_json()
        return self._container.create(container_id, container_image, rootfs,
                                      runtime, hostconfig, customconfig)

    @utils.response2dict
    def start_container(self, container_id, stdin=None, attach_stdin=False,
                        stdout=None, attach_stdout=False, stderr=None,
                        attach_stderr=False):
        """ Start a stopped container

        :param container_id: identifier of container
        :param stdin: FIFO for stdin stream
        :param attach_stdin: Attach stdin or not
        :param stdout: FIFO for stdout stream
        :param attach_stdout: Attach stdout or not
        :param stderr: FIFO for stderr stream
        :param attach_stderr: Attach stderr or not
        :return: return the error code and message if start failed, otherwise return an empty dict.
        """
        return self._container.start(container_id, stdin, attach_stdin, stdout,
                                     attach_stdout, stderr, attach_stderr)

    def remote_start_container(self, container_id, stdin=None, finish=False):
        """ Start a container remotely

        :param container_id: identifier of container
        :param stdin: FIFO for stdin stream
        :param finish:
        :return:
        """
        #return self._container.remote_start(container_id, stdin, finish)
        raise NotImplementedError

    def container_top(self, container_id, args=None):
        """ Display the running processes of a container

        :param container_id: identifier of container
        :param args(List(string)): the parameter for linux command `ps`
        :return: the linux command `ps` information in container.
        """
        if not isinstance(args, list):
            raise Exception("The args should be a list contains ps parameter, such as ['-s', '-q']")
        response = MessageToDict(self._container.top(container_id, args))
        response['titles'] = base64.b64decode(response['titles']).decode()
        for i in range(len(response['processes'])):
            response['processes'][i] = base64.b64decode(response['processes'][i]).decode()
        return response

    @utils.response2dict
    def stop_container(self, container_id, force=False, timeout=None):
        """ Stop a container

        :param container_id: Identifier of a container
        :param force: Enforce stop or not
        :param timeout: Timeout in seconds to wait for the container to
                stop before sending a ``SIGKILL``.
        :return: return the error code and message if stop failed, otherwise return an empty dict.
        """
        return self._container.stop(container_id, force, timeout)

    @utils.response2dict
    def kill_container(self, container_id, k_signal=signal.SIGKILL):
        """ Kill a running container

        :param container_id: Identifier of a container
        :param k_signal: The signal to send. Defaults to ``SIGKILL``
        :return: return the error code and message if kill failed, otherwise return an empty dict.
        """
        return self._container.kill(container_id, k_signal)

    @utils.response2dict
    def delete_container(self, container_id, force=False, volumes=False):
        """ Delete a container

        :param container_id: Identifier of a container
        :param force: Delete a container forcibly
        :param volumes: Delete volumes attached to a container
        :return: return the error code and message if delete failed, otherwise return the deleted container id.
        """
        return self._container.delete(container_id, force, volumes)

    @utils.response2dict
    def pause_container(self, container_id):
        """ Pause a running container

        :param container_id: identifier of container
        :return: return the error code and message if pause failed, otherwise return an empty dict.
        """
        return self._container.pause(container_id)

    @utils.response2dict
    def resume_container(self, container_id):
        """ Resume a paused container

        :param container_id: identifier of container
        :return: return the error code and message if resume failed, otherwise return an empty dict.
        """
        return self._container.resume(container_id)

    @utils.response2dict
    def inspect_container(self, container_id, bformat=False, timeout=None):
        """ Get low-level information on a container

        :param container_id: identifier of container
        :param bformat: Format the output
        :param timeout: Timeout in seconds to wait
        :return: Details info of container
        """
        return self._container.inspect(container_id, bformat, timeout)

    @utils.response2dict
    def list_containers(self, filters=None, is_all=False):
        """ List containers

        :param filters(list or dict): Filter output based on conditions provided
        :param all(boolean): Display all containers (default shows just running)
        :returns: dict -- list of containers' info

        The filters can be a dict like:
            filters = {'id': 'xxx'}
        or a list like:
            filters = [('id', xxx)]
        """
        return self._container.list(filters, is_all)

    @utils.response2dict
    def stats_containers(self, containers=None, all_containers=False):
        """ Display a live stream of container(s) resource usage statistics

        :param containers(List(string)): A list of containers' ID (default shows all running containers)
        :param all_containers: show all containers or not
        :return: resource usage statistics of containers
        """
        return self._container.stats(containers, all_containers)

    @utils.response2dict
    def wait_container(self, container_id, condition=None):
        """ Block until one or more containers stop

        :param container_id: identifier of container
        :param condition: wait until container REMOVED or STOPED
        :return: return the error code and message if wait failed, otherwise return an empty dict.
        """
        return self._container.wait(container_id, condition)

    def container_events(self, container_id=None, since=None, until=None,
                         store_only=False):
        """ Get real time events from the server

        :param container_id: identifier of container
        :param since: time when the events of a container since from
        :param until: time when the evens of a container until
        :param store_only:
        :return: Iterable -- An Iterable object contains container events.

        example:
            import isula
            client = isula.init_isulad_client()
            for event in client.container_events('xxx')
                print(event)
        Note: The for loop will be blocked forever unless the request is canceld by hand.
        """
        return self._container.events(container_id, since, until, store_only)

    @utils.response2dict
    def container_exec(self, container_id, argv, tty=None, open_stdin=False,
                       attach_stdin=False, attach_stdout=False,
                       attach_stderr=False, stdin=None, stdout=None,
                       stderr=None, env=None, user=None, suffix=None,
                       workdir=None):
        """ Run a command in a running container

        :param container_id: identifier of container
        :param argv: specify arguments, should be list format
        :param env: Set environment variables
        :param tty: Allocate a pseudo-TTY
        :param open_stdin:
        :param attach_stdin: Attach stdin stream or not
        :param attach_stdout: Attach stdout stream or not
        :param attach_stderr: Attach stderr stream or not
        :param stdin: FIFO for stdin stream
        :param stdout: FIFO for stdout stream
        :param stderr: FIFO for stderr stream
        :param user: Username or UID
        :param suffix:
        :param workdir: Working directory inside the container, supported only
        when runtime is lcr
        :return: return the error code and message if exec failed, otherwise return an empty dict.
        """
        return self._container.container_exec(
            container_id, tty, open_stdin, attach_stdin, attach_stdout,
            attach_stderr, stdin, stdout, stderr, argv, env, user, suffix,
            workdir)

    def container_remote_exec(self, cmd, finish=None):
        """

        :param cmd: commands to be executed in container
        :param finish: wait until finish or not
        :return:
        """
        #return self._container.remote_exec(cmd, finish)
        raise NotImplementedError

    @utils.response2dict
    def isulad_version(self):
        """ Get isulad package version info

        :return: isulad version info
        """
        return self._container.version()

    @utils.response2dict
    def isulad_info(self):
        """ Display system-wide information

        :return: isula system info, summary and usages
        """
        return self._container.info()

    @utils.response2dict
    def update_container(self, container_id, **kwargs):
        """ Update a container

        :param container_id: identifier of container
        :param kwargs:
        :return: return the error code and message if update failed, otherwise return the container id.
        """
        hc_argspec = inspect.getfullargspec(container.HostConfig.__init__).args
        hc_args = {}
        for k, v in kwargs.items():
            if k in hc_argspec:
                hc_args[k] = v
        hostconfig = container.HostConfig(**hc_args).to_json()

        return self._container.update(container_id, hostconfig)

    def attach_container(self, stdin, finish=None):
        """ Attach to a running container

        :param stdin: TTY attach to a container
        :param finish:
        :return: exit status and message
        """
        return self._container.attach(stdin.encode(), finish)

    @utils.response2dict
    def restart_container(self, container_id, timeout=None):
        """ Restart a container

        :param container_id: identifier of container
        :param timeout: timeout in seconds
        :return: return the error code and message if restart failed, otherwise return an empty dict.
        """
        return self._container.restart(container_id, timeout)

    @utils.response2dict
    def export_container(self, container_id, file_location):
        """ Export a container to an image file

        :param container_id: identifier of container
        :param file_location: file name to save container image
        :return: exit status and message
        """
        file_location = os.path.abspath(file_location)
        return self._container.export(container_id, file_location)

    def copy_from_container(self, container_id, srcpath, runtime=None):
        """ Copy data from a container

        :param container_id: identifier of container
        :param runtime: runtime to use for containers(default: lcr)
        :param srcpath: path of data to be copied out
        :return: exit status and message
        """
        return self._container.copy_from_container(container_id, runtime,
                                                   srcpath)

    def copy_to_container(self, data):
        """ Copy data into a container

        :param data: data to be copied
        :return: exit status and message
        """
        return self._container.copy_to_container(data)

    @utils.response2dict
    def rename_container(self, oldname, newname):
        """ Rename a container

        :param oldname: old name of container
        :param newname: new name of container
        :return: return the error code and message if rename failed, otherwise return the container id.
        """
        return self._container.rename(oldname, newname)

    def container_logs(self, container_id, runtime=None, since=None, until=None,
                       timestamps=False, follow=False, tail=None,
                       details=False):
        """ Fetch the logs of a container

        :param container_id: identifier of container
        :param runtime:
        :param since: Show logs since a given datetime or
                integer epoch (in seconds)
        :param until: Show logs that occurred before the given
                datetime or integer epoch (in seconds)
        :param timestamps: Show timestamps. Default ``False``
        :param follow: Follow log output. Default ``False``
        :param tail: Number of lines to show from the end of the logs
        :param details: return detailed logs or not
        :return: log messages
        """
        return self._container.logs(container_id, runtime, since, until,
                                    timestamps, follow, tail, details)

    @utils.response2dict
    def resize_container(self, container_id, suffix=None, height=None,
                         width=None):
        """ Resize the tty session.

        :param container_id: identifier of container
        :param suffix:
        :param height: Height of tty session
        :param width: Width of tty session
        :return: return the error code and message if resize failed, otherwise return the container id.
        """
        return self._container.resize(container_id, suffix, height, width)

    @utils.response2dict
    def cri_runtime_version(self, version=None):
        """ [CRI] Get runtime version info

        :param version(string): input version parameter
        :return: dict -- version information of isulad Runtime
        """
        return self._cri_runtime.version(version)

    @utils.response2dict
    def cri_list_containers(self, query_filter=None):
        """ [CRI] List containers

        :param query_filter(string): Filter output based on conditions provided
        :return: dict -- list of containers' info
        """
        return self._cri_runtime.list_containers(query_filter)

    @utils.response2dict
    def cri_list_images(self, query_filter=None):
        """ [CRI] List images

        :param query_filter(string): Filter output based on conditions provided
        :return:
        """
        return self._cri_images.list_images(query_filter)

    @utils.response2dict
    def list_images(self, filters=None):
        """ [IMAGE] List images

        :param filters(list): Filter output based on conditions provided
        :return: dict -- list of images' info
        """
        if not filters:
            filters = {}
        for k in filters.keys():
            if k not in ["dangling", "label", "before", "since", "reference"]:
                raise Exception("Only supports the following fields - dangling, label, before, since, reference")

        return self._images.list(filters)

    @utils.response2dict
    def delete_image(self, name, force=False):
        """ [IMAGE] Delete the image in isulad

        :param name(string): The image name that will been deleted
        :param force(bool): Whether to force deletion
        :returns: dict - the result of the operation.
        """
        return self._images.delete(name, force)

    @utils.response2dict
    def load_image(self, image_file, image_type, tag=''):
        """ [IMAGE] Import the image exported using the save command.

        :param image_file(string): The image file that will been loaded
        :param image_type(string): The type of image - oci embedded external
        :param tag(string): The tag of image that will been named
        :returns: dict - the result of the operation.
        """
        # TODO(ffrog): check whether the type and tag meet the corresponding relationship
        if image_type not in ["oci", "embedded", "external"]:
            raise Exception("Only supports the following type - oci, embedded, external")
        image_file = os.path.abspath(image_file)
        return self._images.load(image_file, image_type, tag)

    @utils.response2dict
    def inspect_image(self, image_id, bformat=False, timeout=120):
        """ [IMAGE] Get the metadata of image

        :param image_id(string): The image id
        :param bformat(bool): ?
        :param timeout(int): Maximum waiting time
        :returns: dict - the result of the operation.
        """
        return self._images.inspect(image_id, bformat, timeout)

    @utils.response2dict
    def tag_image(self, src_name, dest_name):
        """ [IMAGE] Tag the image with dest_name for image named src_name

        :param src_name(string): The image name that will been tag
        :param dest_name(string): The new name for origin image
        :returns: dict - the result of the operation.
        """
        return self._images.tag(src_name, dest_name)

    @utils.response2dict
    def import_image(self, image_file, tag):
        """ [IMAGE] Import a new image

        :param image_file(string): The file name which been created by command export
        :param tag(string): The tag name for image
        :returns: dict - the result of the operation.
        """
        image_file = os.path.abspath(image_file)
        return self._images.import_(image_file, tag)

    @utils.response2dict
    def login(self, username, password, server, image_type='oci'):
        """ [IMAGE] Login image registry with username and password

        :param username(string): The username of registry
        :param password(string): The password of username for registry
        :param server(string): The address of registry
        :param type(string): The type of image - oci embedded external
        :returns: dict - return the error code and message if login failed, otherwise return an empty dict.
        """
        if image_type != 'oci':
            raise Exception("Invalid image_type, only oci is supported currently")
        return self._images.login(username, password, server, image_type)

    @utils.response2dict
    def logout(self, server, image_type='oci'):
        """ [IMAGE] Logout image registry

        :param server(string): The address of registry
        :param type(string): The type of image - oci embedded external
        :returns: dict - return the error code and message if logout failed, otherwise return an empty dict.
        """
        if image_type != 'oci':
            raise Exception("Invalid image_type, only oci is supported currently")
        return self._images.logout(server, image_type)

    @utils.response2dict
    def list_volumes(self):
        """ [VOLUME] List volumes

        :return:  dict -- list of volumes' info
        """
        return self._volumes.list()

    @utils.response2dict
    def remove_volume(self, name):
        """ [VOLUME] Remove the volume

        :param name(string): The volume name that will been removed
        :returns: dict - the result of the operation.
        """
        return self._volumes.remove(name)

    @utils.response2dict
    def prune_volume(self):
        """ [VOLUME] Remove the unused volume

        :returns: dict - the result of the operation.
        """
        return self._volumes.prune()
