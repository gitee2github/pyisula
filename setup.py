from setuptools import setup


setup(
    name='isula',
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
        'isula/isulad_grpc'],
    install_requires=['grpcio'],
)
