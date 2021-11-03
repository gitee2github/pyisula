import json

from google.protobuf.json_format import MessageToDict

from isula.isulad_grpc import container_pb2


class Container(object):
    def __init__(self, client):
        self.client = client

    def create(self, container_id, image, rootfs, runtime, hostconfig,
               customconfig):
        request = container_pb2.CreateRequest(id=container_id, rootfs=rootfs,
                                              image=image, runtime=runtime,
                                              hostconfig=hostconfig,
                                              customconfig=customconfig)
        response = self.client.Create(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def start(self, container_id, stdin, attach_stdin, stdout, attach_stdout,
              stderr, attach_stderr):
        request = container_pb2.StartRequest(id=container_id, stdin=stdin,
                                             attach_stdin=attach_stdin,
                                             stdout=stdout,
                                             attach_stdout=attach_stdout,
                                             stderr=stderr,
                                             attach_stderr=attach_stderr)
        response = self.client.Start(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def remote_start(self, container_id, stdin, finish):
        request = container_pb2.RemoteStartRequest(stdin=stdin, finish=finish)
        response = self.client.RemoteStart(
            request, metadata=[('username', '0'), ('tls_mode', '0'), ('container-id', container_id)])
        for message in response:
            yield message

    def top(self, container_id, args):
        request = container_pb2.TopRequest(id=container_id, args=args)
        response = self.client.Top(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def stop(self, container_id, force, timeout):
        request = container_pb2.StopRequest(id=container_id, force=force,
                                            timeout=timeout)
        response = self.client.Stop(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def kill(self, container_id, signal):
        request = container_pb2.KillRequest(id=container_id, signal=signal)
        response = self.client.Kill(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def delete(self, container_id, force, volumes):
        request = container_pb2.DeleteRequest(id=container_id, force=force,
                                              volumes=volumes)
        response = self.client.Delete(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def pause(self, container_id):
        request = container_pb2.PauseRequest(id=container_id)
        response = self.client.Pause(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def resume(self, container_id):
        request = container_pb2.ResumeRequest(id=container_id)
        response = self.client.Resume(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def inspect(self, container_id, bformat, timeout):
        request = container_pb2.InspectContainerRequest(
            id=container_id, bformat=bformat, timeout=timeout)
        response = self.client.Inspect(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def list(self, filters, is_all):
        """Get list of containers"""
        request = container_pb2.ListRequest(filters=filters, all=is_all)
        response = self.client.List(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def stats(self, containers, all_containers):
        request = container_pb2.StatsRequest(containers=containers,
                                             all=all_containers)
        response = self.client.Stats(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def wait(self, container_id, condition):
        request = container_pb2.WaitRequest(id=container_id,
                                            condition=condition)
        response = self.client.Wait(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def events(self, container_id, since, until, store_only):
        request = container_pb2.EventsRequest(id=container_id, since=since,
                                              until=until, storeOnly=store_only)
        response = self.client.Events(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        for message in response:
            yield MessageToDict(message)

    def container_exec(self, container_id, tty, open_stdin, attach_stdin,
                       attach_stdout, attach_stderr, stdin, stdout, stderr,
                       argv, env, user, suffix, workdir):
        request = container_pb2.ExecRequest(
            container_id=container_id, tty=tty, open_stdin=open_stdin,
            attach_stdin=attach_stdin, attach_stdout=attach_stdout,
            attach_stderr=attach_stderr, stdin=stdin, stdout=stdout,
            stderr=stderr, argv=argv, env=env, user=user, suffix=suffix,
            workdir=workdir)
        response = self.client.Exec(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def remote_exec(self, cmd, finish):
        request = container_pb2.RemoteExecRequest(cmd=cmd, finish=finish)
        response = self.client.RemoteExec(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        for message in response:
            yield message

    def version(self):
        request = container_pb2.VersionRequest()
        response = self.client.Version(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def info(self):
        request = container_pb2.InfoRequest()
        response = self.client.Info(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def update(self, container_id, hostconfig):
        request = container_pb2.UpdateRequest(id=container_id,
                                              hostconfig=hostconfig)
        response = self.client.Update(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def attach(self, stdin, finish):
        request = container_pb2.AttachRequest(stdin=stdin, finish=finish)
        response = self.client.Attach(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        for message in response:
            yield message

    def restart(self, container_id, timeout):
        request = container_pb2.RestartRequest(id=container_id,
                                               timeout=timeout)
        response = self.client.Restart(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def export(self, container_id, export_file):
        request = container_pb2.ExportRequest(id=container_id, file=export_file)
        response = self.client.Export(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def copy_from_container(self, container_id, runtime, srcpath):
        request = container_pb2.CopyFromContainerRequest(
            id=container_id, runtime=runtime, srcpath=srcpath)
        response = self.client.CopyFromContainer(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        for message in response:
            yield message

    def copy_to_container(self, data):
        request = container_pb2.CopyToContainerRequest(data=data)
        response = self.client.CopyToContainer(
            request, metadata=[('username', '0'), ('tls_mode', '0'),
                               ('isulad-copy-to-container', )])
        for message in response:
            yield message

    def rename(self, oldname, newname):
        request = container_pb2.RenameRequest(oldname=oldname, newname=newname)
        response = self.client.Rename(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response

    def logs(self, container_id, runtime, since, until, timestamps, follow,
             tail, details):
        request = container_pb2.LogsRequest(
            id=container_id, runtime=runtime, since=since, until=until,
            timestamps=timestamps, follow=follow, tail=tail, details=details)
        response = self.client.Logs(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        for message in response:
            yield message

    def resize(self, container_id, suffix, height, width):
        """ Resize a container"""
        request = container_pb2.ResizeRequest(id=container_id, suffix=suffix,
                                              height=height, width=width)
        response = self.client.Resize(
            request, metadata=[('username', '0'), ('tls_mode', '0')])
        return response


class HostConfig(dict):
    def __init__(self, VolumesFrom=None, Binds=None, Mounts=None,
                 NetworkMode='',
                 GroupAdd=None, IpcMode='', PidMode='',
                 Privileged=False, SystemContainer=False, NsChangeFiles=None,
                 UserRemap='', ShmSize=0, AutoRemove=False,
                 AutoRemoveBak=False, ReadonlyRootfs=False, Tmpfs=None,
                 UTSMode='', UsernsMode='', Sysctls=None, Runtime='lcr',
                 RestartPolicy=None, CapAdd=None, CapDrop=None, Dns=None,
                 DnsOptions=None, DnsSearch=None, ExtraHosts=None,
                 HookSpec='', CPUShares=0, Memory=0, OomScoreAdj=0,
                 BlkioWeight=0, BlkioWeightDevice=None,
                 BlkioDeviceReadBps=None, BlkioDeviceWriteBps=None,
                 BlkioDeviceReadIops=None, BlkioDeviceWriteIops=None,
                 NanoCpus=0, CPUPeriod=0,
                 CPUQuota=0, CPURealtimePeriod=0, CPURealtimeRuntime=0,
                 CpusetCpus='', CpusetMems='', Devices=None,
                 DeviceCgroupRules=None, SecurityOpt=None, StorageOpt=None,
                 KernelMemory=0, MemoryReservation=0, MemorySwap=0,
                 MemorySwappiness=None, OomKillDisable=False, PidsLimit=None,
                 FilesLimit=None, Ulimits=None, Hugetlbs=None, HostChannel=None,
                 EnvTargetFile='', ExternalRootfs='', CgroupParent=''):

        if VolumesFrom:
            if not isinstance(VolumesFrom, list):
                raise host_config_type_error('VolumesFrom', VolumesFrom, 'list')
            self['VolumesFrom'] = VolumesFrom

        if Binds:
            if not isinstance(Binds, list):
                raise host_config_type_error('Binds', Binds, 'list')
            self['Binds'] = Binds

        if Mounts:
            if not isinstance(Mounts, list):
                raise host_config_type_error('Mounts', Mounts, 'list')
            self['Mounts'] = Mounts

        if NetworkMode:
            self['NetworkMode'] = NetworkMode

        if GroupAdd:
            if not isinstance(GroupAdd, list):
                raise host_config_type_error('GroupAdd', GroupAdd, 'list')
            self['GroupAdd'] = GroupAdd

        if IpcMode:
            self['IpcMode'] = IpcMode
        if PidMode:
            self['PidMode'] = PidMode
        if Privileged:
            self['Privileged'] = Privileged
        if SystemContainer:
            self['SystemContainer'] = SystemContainer

        if NsChangeFiles:
            if not isinstance(NsChangeFiles, list):
                raise host_config_type_error('NsChangeFiles', NsChangeFiles,
                                             'list')
            self['NsChangeFiles'] = NsChangeFiles

        if NsChangeFiles:
            self['NsChangeFiles'] = NsChangeFiles
        if UserRemap:
            self['UserRemap'] = UserRemap
        if ShmSize:
            self['ShmSize'] = ShmSize
        if AutoRemove:
            self['AutoRemove'] = AutoRemove
        if AutoRemoveBak:
            self['AutoRemoveBak'] = AutoRemoveBak
        if ReadonlyRootfs:
            self['ReadonlyRootfs'] = ReadonlyRootfs

        if Tmpfs:
            if not isinstance(Tmpfs, dict):
                raise host_config_type_error('Tmpfs', Tmpfs, 'dict')
            self['Tmpfs'] = Tmpfs

        if UTSMode:
            self['UTSMode'] = UTSMode
        if UsernsMode:
            self['UsernsMode'] = UsernsMode

        if Sysctls:
            if not isinstance(Sysctls, dict):
                raise host_config_type_error('Sysctls', Sysctls, 'dict')
            self['Sysctls'] = Sysctls

        if Runtime:
            self['Runtime'] = Runtime

        if RestartPolicy:
            if not isinstance(RestartPolicy, dict):
                raise host_config_type_error('RestartPolicy', RestartPolicy,
                                             'dict')
            self['RestartPolicy'] = RestartPolicy

        if CapAdd:
            if not isinstance(CapAdd, list):
                raise host_config_type_error('CapAdd', CapAdd, 'list')
            self['CapAdd'] = CapAdd

        if CapDrop:
            if not isinstance(CapDrop, list):
                raise host_config_type_error('CapDrop', CapDrop, 'list')
            self['CapDrop'] = CapDrop

        if Dns:
            if not isinstance(Dns, list):
                raise host_config_type_error('Dns', Dns, 'list')
            self['Dns'] = Dns

        if DnsOptions:
            if not isinstance(DnsOptions, list):
                raise host_config_type_error('DnsOptions', DnsOptions, 'list')
            self['DnsOptions'] = DnsOptions

        if DnsSearch:
            if not isinstance(DnsSearch, list):
                raise host_config_type_error('DnsSearch', DnsSearch, 'list')
            self['DnsSearch'] = DnsSearch

        if ExtraHosts:
            if not isinstance(ExtraHosts, list):
                raise host_config_type_error('ExtraHosts', ExtraHosts, 'list')
            self['ExtraHosts'] = ExtraHosts

        if HookSpec:
            self['HookSpec'] = HookSpec
        if CPUShares:
            self['CPUShares'] = CPUShares
        if Memory:
            self['Memory'] = Memory
        if OomScoreAdj:
            self['OomScoreAdj'] = OomScoreAdj
        if BlkioWeight:
            self['BlkioWeight'] = BlkioWeight

        if BlkioWeightDevice:
            if not isinstance(BlkioWeightDevice, list):
                raise host_config_type_error('BlkioWeightDevice',
                                             BlkioWeightDevice, 'list')
            self['BlkioWeightDevice'] = BlkioWeightDevice

        if BlkioDeviceReadBps:
            if not isinstance(BlkioDeviceReadBps, list):
                raise host_config_type_error('BlkioDeviceReadBps',
                                             BlkioDeviceReadBps, 'list')
            self['BlkioDeviceReadBps'] = BlkioDeviceReadBps

        if BlkioDeviceWriteBps:
            if not isinstance(BlkioDeviceWriteBps, list):
                raise host_config_type_error('BlkioDeviceWriteBps',
                                             BlkioDeviceWriteBps, 'list')
            self['BlkioDeviceWriteBps'] = BlkioDeviceWriteBps

        if BlkioDeviceReadIops:
            if not isinstance(BlkioDeviceReadIops, list):
                raise host_config_type_error('BlkioDeviceReadIops',
                                             BlkioDeviceReadIops, 'list')
            self['BlkioDeviceReadIops'] = BlkioDeviceReadIops

        if BlkioDeviceWriteIops:
            if not isinstance(BlkioDeviceWriteIops, list):
                raise host_config_type_error('BlkioDeviceWriteIops',
                                             BlkioDeviceWriteIops, 'list')
            self['BlkioDeviceWriteIops'] = BlkioDeviceWriteIops

        if NanoCpus:
            self['NanoCpus'] = NanoCpus
        if CPUPeriod:
            self['CPUPeriod'] = CPUPeriod
        if CPUQuota:
            self['CPUQuota'] = CPUQuota
        if CPURealtimePeriod:
            self['CPURealtimePeriod'] = CPURealtimePeriod
        if CPURealtimeRuntime:
            self['CPURealtimeRuntime'] = CPURealtimeRuntime
        if CpusetCpus:
            self['CpusetCpus'] = CpusetCpus
        if CpusetMems:
            self['CpusetMems'] = CpusetMems

        if Devices:
            if not isinstance(Devices, list):
                raise host_config_type_error('Devices',
                                             Devices, 'list')
            self['Devices'] = Devices

        if DeviceCgroupRules:
            if not isinstance(DeviceCgroupRules, list):
                raise host_config_type_error('DeviceCgroupRules',
                                             DeviceCgroupRules, 'list')
            self['DeviceCgroupRules'] = DeviceCgroupRules

        if SecurityOpt:
            if not isinstance(SecurityOpt, list):
                raise host_config_type_error('SecurityOpt',
                                             SecurityOpt, 'list')
            self['SecurityOpt'] = SecurityOpt

        if StorageOpt:
            if not isinstance(StorageOpt, dict):
                raise host_config_type_error('StorageOpt', StorageOpt, 'dict')
            self['StorageOpt'] = StorageOpt

        if KernelMemory:
            self['KernelMemory'] = KernelMemory
        if MemoryReservation:
            self['MemoryReservation'] = MemoryReservation
        if MemorySwap:
            self['MemorySwap'] = MemorySwap
        if MemorySwappiness:
            self['MemorySwappiness'] = MemorySwappiness
        if OomKillDisable:
            self['OomKillDisable'] = OomKillDisable
        if PidsLimit:
            if not isinstance('PidsLimit', PidsLimit, int):
                raise host_config_type_error('PidsLimit', PidsLimit, 'int')
            self['PidsLimit'] = PidsLimit
        if FilesLimit:
            if not isinstance('FilesLimit', FilesLimit, int):
                raise host_config_type_error('FilesLimit', FilesLimit, 'int')
            self['FilesLimit'] = FilesLimit

        if Ulimits:
            if not isinstance(Ulimits, list):
                raise host_config_type_error('Ulimits', Ulimits, 'list')
            self['Ulimits'] = Ulimits

        if Hugetlbs:
            if not isinstance(Hugetlbs, list):
                raise host_config_type_error('Hugetlbs', Hugetlbs, 'list')
            self['Hugetlbs'] = Hugetlbs

        if HostChannel:
            if not isinstance(HostChannel, dict):
                raise host_config_type_error('HostChannel', HostChannel, 'dict')
            self['HostChannel'] = HostChannel

        if EnvTargetFile:
            self['EnvTargetFile'] = EnvTargetFile
        if ExternalRootfs:
            self['ExternalRootfs'] = ExternalRootfs
        if CgroupParent:
            self['CgroupParent'] = CgroupParent

    def to_json(self):
        return json.dumps(self)


def host_config_type_error(param, param_value, expected):
    error_msg = 'Invalid type for {0} param: expected {1} but found {2}'
    return TypeError(error_msg.format(param, expected, type(param_value)))


class ContainerConfig(dict):
    def __init__(self, container_id=None, name=None, pid=None, status=None,
                 image=None, imageRef=None, command=None, ram=None, swap=None,
                 exit_code=None, restartcount=None, Created=None, startat=None,
                 finishat=None, runtime=None, HealthState=None, Labels=None,
                 Annotations=None):
        if container_id:
            self['id'] = container_id
        if name:
            self['name'] = name
        if pid:
            self['pid'] = pid
        if status:
            self['status'] = status
        if image:
            self['image'] = image
        if imageRef:
            self['imageRef'] = imageRef
        if command:
            self['command'] =command
        if ram:
            self['ram'] = ram
        if swap:
            self['swap'] = swap
        if exit_code:
            self['exit_code'] = exit_code
        if restartcount:
            self['restartcount'] = restartcount
        if Created:
            self['Created'] = Created
        if startat:
            self['startat'] = startat
        if finishat:
            self['finishat'] = finishat
        if runtime:
            self['runtime'] = runtime
        if HealthState:
            self['HealthState'] = HealthState
        if Labels:
            self['Labels'] = Labels
        if Annotations:
            self['Annotations'] = Annotations

    def to_json(self):
        return json.dumps(self)
