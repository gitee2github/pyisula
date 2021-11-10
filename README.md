# pyisula

## 介绍

python sdk library for iSulad and isula-build

## 如何使用

### 安装

#### 通过pypi安装（开发中）

```shell
pip install pyisula
```

#### 通过RPM安装（开发中）

```shell
yum install python-pyisula
```

#### 通过源码安装

```shell
git clone https://gitee.com/openeuler/pyisula
cd pyisula

python setup.py install
或
pip install -e .
```

### 代码调用

```python
from isula import client

# isula-builder interfaces:
builder_client = client.init_builder_client()
image_list = builder_client.list_images()
print(image_list)

# isula interfaces:
isula_client = client.init_isulad_client()
isula_client.list_container()
isula_client.list_images()
isula_client.list_volumes()
isula_client.cri_list_images()
...
```

## 如何刷新gRPC接口文件

本python库通过gRPC与iSulad和isula-builder通信，采用protobuf协议。API接口文件通过grpc_tools工具、使用iSulad和isula-builder提供的proto文件自动生成。因此，当iSulad或isula-buidler API发生变动时，需要手动重新生成API接口文件，并分别同步到isula/isulad_grpc和isula/builder_grpc目录。

方法如下：

```shell
# iSulad的proto文件在https://gitee.com/openeuler/iSulad/tree/master/src/api/services
# isula—build的proto文件在https://gitee.com/openeuler/isula-build/tree/master/api/services

# 以isula-build为例
pip install grpcio-tools

cd isula-build/api/services
python -m grpc_tools.protoc -I../services --python_out=. --grpc_python_out=. control.proto

完成后，会在isula-build/api/services目录下生成两个文件`control_pb2_grpc.py`和`control_pb2.py`。把这两个文件移动到本仓库的isula/builder_grpc中即可。

最后，把`control_pb2_grpc.py`中的
import control_pb2 as control__pb2
修改成
import isula.builder_grpc.control_pb2 as control__pb2
即可。
```

## 版本配套关系

| pyisula | iSulad | isula-build | 状态 |
|  ----  |  ----  |  ----  |  ----  |
| 0.0.2 | 2.0.9 | 0.9.5 | 开发中 |
| xxx | xx | xxx | xxx|

## 接口配套关系

### isula-build

| pyisula | isula-build | CLI |
| ---- | ---- | ---- |
| server_version | isula.build.v1.Control.Version | isula-build version |
| server_info | isula.build.v1.Control.Info | isula-build info |
| server_healthcheck | isula.build.v1.Control.HealthCheck | - |
| login | isula.build.v1.Control.Login | isula-build login |
| logout | isula.build.v1.Control.Logout | isula-build logout |
| create_manifest | isula.build.v1.Control.ManifestCreate| - |
| annotate_manifest | isula.build.v1.Control.ManifestAnnotate| - |
| inspect_manifest | isula.build.v1.Control.ManifestInspect| - |
| push_manifest | isula.build.v1.Control.ManifestPush| - |
| list_images | isula.build.v1.Control.List | isula-build ctr-img images |
| build_image | isula.build.v1.Control.Build | isula-build ctr-img build |
| push_image | isula.build.v1.Control.Push | isula-build ctr-img push |
| pull_image | isula.build.v1.Control.Pull | isula-build ctr-img pull |
| remove_images | isula.build.v1.Control.Remove | isula-build ctr-img rm |
| load_image | isula.build.v1.Control.Load | isula-build ctr-img load |
| import_image | isula.build.v1.Control.Import | isula-build ctr-img import |
| tag_image | isula.build.v1.Control.Tag | isula-build ctr-img tag |
| save_image | isula.build.v1.Control.Save | isula-build ctr-img save |

### iSulad

| pyisula | iSulad | CLI |
| ---- | ---- | ---- |
| isulad_version | containers.ContainerService/Version | isula version |
| isulad_info | containers.ContainerService/Info | isula info |
| list_containers | containers.ContainerService/List | isula ps |
| create_container | containers.ContainerService/Create | isula create |
| start_container | containers.ContainerService/Start | isula start |
| stop_container | containers.ContainerService/Stop | isula stop |
| update_container | containers.ContainerService/Update | isula update |
| attach_container | containers.ContainerService/Attach | isula attach |
| restart_container | containers.ContainerService/Restart | isula restart |
| export_container | containers.ContainerService/Export | isula export |
| copy_from_container | containers.ContainerService/CopyFromContainer | isula cp |
| rename_container | containers.ContainerService/Rename | isula rename |
| resize_container | containers.ContainerService/Resize | - |
| kill_container | containers.ContainerService/Kill | isula kill |
| delete_container | containers.ContainerService/Delete | isula rm |
| pause_container | containers.ContainerService/Pause | isula pause |
| resume_container | containers.ContainerService/Resume | isula unpause |
| inspect_container | containers.ContainerService/Inspect | isula inspect |
| stats_containers | containers.ContainerService/Stats | isula stats |
| wait_container | containers.ContainerService/Wait | isula wait |
| container_top | containers.ContainerService/Top | isula top |
| container_events | containers.ContainerService/Events | isula events |
| container_exec | containers.ContainerService/Exec | isula exec |
| container_logs | containers.ContainerService/Logs | isula logs |
| cri_runtime_version | runtime.v1alpha2.RuntimeService/Version | - |
| cri_list_containers | runtime.v1alpha2.RuntimeService/ListContainers | - |
| cri_list_images | runtime.v1alpha2.ImageService/ListImages | - |
| list_images | images.ImagesService/List | isula images |
| delete_image | images.ImagesService/Delete | isula rmi |
| load_image | images.ImagesService/Load | isula load |
| inspect_image | images.ImagesService/Inspect | isula inspect |
| tag_image | images.ImagesService/Tag | isula tag |
| import_image | images.ImagesService/Import | isula import |
| login | images.ImagesService/Login | isula login |
| logout | images.ImagesService/Logout | isula logout |
| list_volumes | volume.VolumeService/List | isula volume ls |
| remove_volume | volume.VolumeService/Remove | isula volume rm |
| prune_volume | volume.VolumeService/Prune | isula volume prune |

### 开发中的接口

| pyisula | iSulad | CLI |
| ---- | ---- | ---- |
| remote_start_container | - | - |
| container_remote_exec | - | - |
| copy_to_container | containers.ContainerService/CopyToContainer | isula cp |
