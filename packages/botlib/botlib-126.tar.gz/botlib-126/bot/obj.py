# This file is placed in the Public Domain.

"objects"

import datetime
import json as js
import os
import pathlib
import sys
import time
import uuid

def cdir(path):
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def gettype(o):
    return str(type(o)).split()[-1][1:-2]

def getwd():
    try:
        return getattr(sys.modules["__main__"], "wd", "")
    except:
        raise ENOWD

def spl(txt):
    return [x for x in txt.split(",") if x]

class NoJSON(Exception):

    pass


class Nowd(Exception):

    pass

class O:

    __slots__ = ("__dict__", "__stp__", "__otype__")

    def __init__(self):
        self.__otype__ = gettype(self)
        self.__stp__ = os.path.join(
            gettype(self),
            str(uuid.uuid4()),
            os.sep.join(str(datetime.datetime.now()).split()),
        )

    @staticmethod
    def __default__(oo):
        try:
            return vars(oo)
        except TypeError:
            pass
        if isinstance(oo, dict):
            return oo.items()
        if isinstance(oo, list):
            return iter(oo)
        if isinstance(oo, (type(str), type(True), type(False), type(int), type(float))):
            return oo
        return O.__dorepr__(oo)

    @staticmethod
    def __dorepr__(o):
        return "<%s.%s object at %s>" % (
            o.__class__.__module__,
            o.__class__.__name__,
            hex(id(o)),
        )

    def __delitem__(self, k):
        if k in self:
            del self.__dict__[k]

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __repr__(self):
        return js.dumps(self, default=self.__default__, sort_keys=True)

    def __str__(self):
        return str(self.__dict__)


class Obj(O):
    def __init__(self, *args, **kwargs):
        O.__init__(self)
        if args:
            self.update(args[0])

    def delkeys(self, keys=[]):
        for k in keys:
            del self[k]

    def edit(self, setter, skip=True, skiplist=[]):
        count = 0
        for key, v in setter.items():
            if skip and v == "":
                del self[key]
            if key in skiplist:
                continue
            count += 1
            if v in ["True", "true"]:
                self[key] = True
            elif v in ["False", "false"]:
                self[key] = False
            else:
                self[key] = v
        return count

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def last(self):
        db = Db()
        t = str(gettype(self))
        path, l = db.lastfn(t)
        if l:
            self.update(l)
        if path:
            spl = path.split(os.sep)
            stp = os.sep.join(spl[-4:])
            return stp

    def merge(self, d):
        for k, v in d.items():
            if not v:
                continue
            if k in self:
                if isinstance(self[k], dict):
                    continue
                self[k] = self[k] + v
            else:
                self[k] = v

    def overlay(self, d, keys=None, skip=None):
        for k, v in d.items():
            if keys and k not in keys:
                continue
            if skip and k in skip:
                continue
            if v:
                self[k] = v

    def register(self, key, value):
        self[str(key)] = value

    def search(self, s):
        ok = False
        for k, v in s.items():
            vv = getattr(self, k, None)
            if v not in str(vv):
                ok = False
                break
            ok = True
        return ok

    def set(self, key, value):
        self.__dict__[key] = value

    def update(self, data):
        return self.__dict__.update(data)

    def values(self):
        return self.__dict__.values()


class Object(Obj):
    def json(self):
        return repr(self)

    def load(self, opath):
        wd = getwd()
        assert wd
        if opath.count(os.sep) != 3:
            raise NoFile(opath)
        spl = opath.split(os.sep)  
        stp = os.sep.join(spl[-4:])
        lpath = os.path.join(wd, "store", stp)
        if os.path.exists(lpath):
            with open(lpath, "r") as ofile:
                d = js.load(ofile, object_hook=Obj)
                self.update(d)
        self.__stp__ = stp
        return self

    def save(self, tab=False):
        wd = getwd()
        assert wd
        prv = os.sep.join(self.__stp__.split(os.sep)[:2])
        self.__stp__ = os.path.join(
            prv, os.sep.join(str(datetime.datetime.now()).split())
        )
        opath = os.path.join(wd, "store", self.__stp__)
        cdir(opath)
        with open(opath, "w") as ofile:
            js.dump(self.__dict__, ofile, default=self.__default__, indent=4, sort_keys=True)
        os.chmod(opath, 0o444)
        return self.__stp__


class Default(Object):

    default = ""

    def __getattr__(self, k):
        if k in self:
            return super().__getattribute__(k)
        if k in super().__dict__:
            return super().__getitem__(k)
        return self.default


class Cfg(Default):

    pass


class List(Object):
    def append(self, key, value):
        if key not in self:
            self[key] = []
        if value in self[key]:
            return
        if isinstance(value, list):
            self[key].extend(value)
        else:
            self[key].append(value)

    def update(self, d):
        for k, v in d.items():
            self.append(k, v)



class Db(Object):
    def all(self, otype, selector=None, index=None, timed=None):
        nr = -1
        if selector is None:
            selector = {}
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not o.search(selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            yield fn, o

    def deleted(self, otype):
        for fn in fns(otype):
            o = hook(fn)
            if "_deleted" not in o or not o._deleted:
                continue
            yield fn, o

    def every(self, selector=None, index=None, timed=None):
        wd = getwd()
        assert wd
        if selector is None:
            selector = {}
        nr = -1
        for otype in os.listdir(os.path.join(wd, "store")):
            for fn in fns(otype, timed):
                o = hook(fn)
                if selector and not o.search(selector):
                    continue
                if "_deleted" in o and o._deleted:
                    continue
                nr += 1
                if index is not None and nr != index:
                    continue
                yield fn, o

    def find(self, otype, selector=None, index=None, timed=None):
        if selector is None:
            selector = {}
        got = False
        nr = -1
        for fn in fns(otype, timed):
            o = hook(fn)
            if selector and not o.search(selector):
                continue
            if "_deleted" in o and o._deleted:
                continue
            nr += 1
            if index is not None and nr != index:
                continue
            got = True
            yield (fn, o)
        if not got:
            return (None, None)

    def lastmatch(self, otype, selector=None, index=None, timed=None):
        res = sorted(
            self.find(otype, selector, index, timed), key=lambda x: fntime(x[0])
        )
        if res:
            return res[-1]
        return (None, None)

    def lastobject(self, o):
        return self.lasttype(o.__otype__)

    def lasttype(self, otype):
        fnn = fns(otype)
        if fnn:
            return hook(fnn[-1])

    def lastfn(self, otype):
        fn = fns(otype)
        if fn:
            fnn = fn[-1]
            return (fnn, hook(fnn))
        return (None, None)


def fns(name, timed=None):
    if not name:
        return []
    wd = getwd()
    assert wd
    p = os.path.join(wd, "store", name) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if (
                        timed
                        and "from" in timed
                        and timed["from"]
                        and fntime(p) < timed["from"]
                    ):
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)


def fmt(o, keys=None, empty=True, skip=None):
    if keys is None:
        keys = o.keys()
    if not keys:
        keys = ["txt"]
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in sorted(keys):
        if key in skip:
            continue
        if key in o:
            val = o[key]
            if empty and not val:
                continue
            val = str(val).strip()
            res.append((key, val))
    result = []
    for k, v in res:
        result.append("%s=%s%s" % (k, v, " "))
    txt += " ".join([x.strip() for x in result])
    return txt.strip()


def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        t += float("." + rest)
    else:
        t = 0
    return t


        
def listfiles(wd):
    path = os.path.join(wd, "store")
    if not os.path.exists(path):
        return []
    return sorted(os.listdir(path))


def hook(hfn):
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    mn, cn = cname.rsplit(".", 1)
    mod = sys.modules.get(mn, None)
    if not mod:
        raise NoModule(mn)
    t = getattr(mod, cn, None)
    if t:
        o = t()
        o.load(fn)
        return o
    raise NoType(cname)
