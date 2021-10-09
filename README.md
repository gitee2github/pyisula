# pyisula

#### 介绍
python sdk library for iSulad and isula-build

## 如何使用

安装
```
pip install pyisula
```
代码调用
```
from isula import client

builder_client = client.init_builder_client()
image_list = builder_client.list_image()
print(image_list)

isulad_client = client.init_isulad_client()
....
```

## 如何刷新gRPC接口文件

本python库通过gRPC与iSulad和isula-builder通信，采用protobuf协议。API接口文件通过grpc_tools工具、使用iSulad和isula-builder提供的proto文件自动生成。因此，当iSulad或isula-buidler API发生变动时，需要手动重新生成API接口文件，并分别同步到isula/isulad_grpc和isula/builder_grpc目录。

方法如下：
```
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

| pyisula | iSulad | isula-build | CLI | 状态 |
|  ----  |  ----  |  ----  | ---- | ----  |
| list_image | - | List | isula-build ctr-img image | 开发中 |
| xxx | xxx | xxx | xxx | xxx|

