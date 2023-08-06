#!/usr/bin/env python3

# encoding: utf-8

from libvmake.utils import get_default_encrypter
import sys
import os
import shutil
from pathlib import Path
from .utils import save_proxy


def showhelp():
    print(f'''usage: {sys.executable} -m libvmake <action>
action is one of:
    help            show help document
    init            init vmake template files
    encrypt         encrypt a password
    decrypt         decrypt a password
    proxy           change proxy settings
''')

if __name__ == "__main__":
    try:
        action = 'help' if sys.argv[1] == '-h' or sys.argv[1] == "--help" else sys.argv[1]
        if action not in ['help', 'init', 'encrypt', 'decrypt', 'proxy']:
            raise Exception("invalid parameter")
    except:
        print("invalid parameter, use -h to view help", file=sys.stderr)
        sys.exit(1)

    if action == "help":
        showhelp()
    elif action == "init":
        resdir = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), 'res')
        if not os.path.exists('.gitattributes'):
            shutil.copy(os.path.join(resdir, 'gitattributes'), '.gitattributes')
        resdir_path = Path(resdir)
        for i in resdir_path.glob('*'):
            file = os.path.basename(i)
            if os.path.exists(file) or file == "gitattributes":
                continue
            if file in ['__pycache__', 'elevate.exe']:
                continue
            print(f"copy libvmake initial file: {file}")
            shutil.copy(i, os.curdir) if os.path.isfile(
                i) else shutil.copytree(i, os.path.join(os.curdir, os.path.basename(i)))
        print("ok: init vmake template files success")
    elif action == "encrypt":
        encryper = get_default_encrypter()
        key = input("input the key to encrypt: ").strip()
        print(f"ok: the encrypted key is {encryper.encrypt(key)}")
    elif action == "decrypt":
        encryper = get_default_encrypter()
        key = input("input the key to decrypt: ").strip()
        print(f"ok: the encrypted key is {encryper.decrypt(key.encode('utf-8'))}")
    elif action == "proxy":
        proxy = input("Input the http proxy(empty for none proxy): ").strip()
        noproxy = input("Input the no proxy url (seperated by ','): ").strip()
        save_proxy(proxy, noproxy)
        print("ok: change proxy settings success")
    else:
        print("invalid parameter, use -h to view help", file=sys.stderr)
        sys.exit(1)
