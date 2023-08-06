# This file is placed in the Public Domain.

"threads"

import queue
import threading
import types

class Thr(threading.Thread):
    "basic thread class"
    def __init__(self, func, *args, thrname="", daemon=True):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self.name = thrname or getname(func)
        self.result = None
        self.queue = queue.Queue()
        self.queue.put_nowait((func, args))
        self.sleep = 0

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        "join the thread for result."
        super().join(timeout)
        return self.result

    def run(self):
        "run the payload."
        func, args = self.queue.get_nowait()
        if args:
            target = vars(args[0])
            if target and "txt" in dir(target):
                self.name = target.txt.split()[0]
        self.setName(self.name)
        self.result = func(*args)

def getname(o):
    "return fqn (full qualified name) of the object."
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    if "__self__" in dir(o):
        return "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    if "__class__" in dir(o) and "__name__" in dir(o):
        return "%s.%s" % (o.__class__.__name__, o.__name__)
    if "__class__" in dir(o):
        return o.__class__.__name__
    if "__name__" in dir(o):
        return o.__name__


def launch(func, *args, **kwargs):
    "launch a thread."
    name = kwargs.get("name", getname(func))
    t = Thr(func, *args, thrname=name, daemon=True)
    t.start()
    return t

