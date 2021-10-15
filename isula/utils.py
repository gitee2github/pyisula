import functools

from google.protobuf.json_format import MessageToDict


def response2dict(fn):
    @functools.wraps(fn)
    def wrap(*args, **kwargs):
        response = fn(*args, **kwargs)
        response = MessageToDict(response)
        return response

    return wrap
