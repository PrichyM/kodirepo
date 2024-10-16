"""resources.lib.passlib.tests.tox_support - helper script for tox tests"""
#=============================================================================
# init script env
#=============================================================================
import os, sys
root_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
sys.path.insert(0, root_dir)

#=============================================================================
# imports
#=============================================================================
# core
import re
import logging; log = logging.getLogger(__name__)
# site
# pkg
from resources.lib.passlib.utils.compat import print_
# local
__all__ = [
]

#=============================================================================
# main
#=============================================================================
TH_PATH = "resources.lib.passlib.tests.test_handlers"

def do_hash_tests(*args):
    """return list of hash algorithm tests that match regexes"""
    if not args:
        print(TH_PATH)
        return
    suffix = ''
    args = list(args)
    while True:
        if args[0] == "--method":
            suffix = '.' + args[1]
            del args[:2]
        else:
            break
    from resources.lib.passlib.tests import test_handlers
    names = [TH_PATH + ":" + name + suffix for name in dir(test_handlers)
             if not name.startswith("_") and any(re.match(arg,name) for arg in args)]
    print_("\n".join(names))
    return not names

def do_preset_tests(name):
    """return list of preset test names"""
    if name == "django" or name == "django-hashes":
        do_hash_tests("django_.*_test", "hex_md5_test")
        if name == "django":
            print_("resources.lib.passlib.tests.test_ext_django")
    else:
        raise ValueError("unknown name: %r" % name)

def do_setup_gae(path, runtime):
    """write fake GAE ``app.yaml`` to current directory so nosegae will work"""
    from resources.lib.passlib.tests.utils import set_file
    set_file(os.path.join(path, "app.yaml"), """\
application: fake-app
version: 2
runtime: %s
api_version: 1
threadsafe: no

handlers:
- url: /.*
  script: dummy.py

libraries:
- name: django
  version: "latest"
""" % runtime)

def main(cmd, *args):
    return globals()["do_" + cmd](*args)

if __name__ == "__main__":
    import sys
    sys.exit(main(*sys.argv[1:]) or 0)

#=============================================================================
# eof
#=============================================================================
