from setuptools import setup


setup(
    name='isula',
    # Bump the version once it's ready to release a new version.
    version='0.0.2',
    author='openEuler community',
    author_email='isulad@openeuler.org',
    description='python sdk for isulad and isula-build',
    url='https://gitee.com/openeuler/pyisula',
    packages=[
        'isula',
        'isula/builder',
        'isula/builder_grpc',
        'isula/isulad',
        'isula/isulad_grpc',
    ],
    install_requires=[
        'cryptography===3.3.1',
        'grpcio===1.31.0',
        'protobuf===3.14.0'
    ],
)
