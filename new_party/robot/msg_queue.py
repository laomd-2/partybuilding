from queue import Queue

__all__ = ['put', 'get']

q = Queue()


def put(user, time, revoke, msg_type, content):
    q.put((user, time, revoke, msg_type, content))


def get():
    return q.get()
