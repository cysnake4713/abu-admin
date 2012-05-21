#!/usr/bin/env python

import os
import sys
import itertools
import ConfigParser
import pkg_resources
import argparse

rc_name = '__ABU_ADMIN_RC___'

eps = pkg_resources.iter_entry_points('abu.admin')

def check_app(name):
    for ep in eps:
        if ep.name == name:
            return True
    return False

def check_path(path):
    return os.path.isdir(path)

def check_rc(path):
    return os.path.exists(path)

def do_list():
    if not eps:
       return
    for no, ep in zip(itertools.count(1), eps):
       print "%s : %s\n" % (no, ep.name)

def do_init():
    name, path = sys.argv[2], sys.argv[3]
    if not check_app(name):
        print '%s is not abu.admin application.' % name
        return
    if not check_path(path):
        print '%s is not a derectory.' % path
        return
    rc_path = os.path.join(path, rc_name)
    if check_rc(rc_path):
        print '%s file already exists, can\'t init env in %s.' % (rc_name, path)
        return
    impl_cls = pkg_resources.load_entry_point(name, 'abu.admin', name)
    impl = impl_cls()
    with open(rc_path, 'w') as rc:
        sec = 'abu.admin'
        cfg = ConfigParser.ConfigParser()
        cfg.add_section(sec)
        cfg.set(sec, 'app', name)
        cfg.set(sec, 'version', impl.version())
        cfg.write(rc)
    try:
        impl.init(path)
    except Exception:
        os.remove(rc_path)
        raise

def do_backup():
    print 'this command is unsupported yet.'

def do_upgrade():
    print 'this command is unsupported yet.'

def print_basic_usage():
    print 'run "abu.admin help" for usage.'

def print_help():
    if len(sys.argv) > 2:
        print_subcommand_help()
        return
    print 'abu.admin <subcommand> [options] [args]'
    print 'run "abu.admin help <subcommand>" for usage of subcommand.'
    print '\n    '.join(['available subcommands:',
        'init',
        'backup',
        'list',
        'upgrade',

        'help',
        ])

def print_subcommand_help():
    subcmd = sys.argv[2]
    if subcmd == 'init':
        print 'abu.admin init <application> </path/to/instance>'
    elif subcmd == 'backup':
        print 'this command is unsupported yet.'
    elif subcmd == 'list':
        print 'list all applications supported abu.abmin.'
        print 'abu.admin list'
    elif subcmd == 'upgrade':
        print 'this command is unsupported yet.'
    else:
        print 'invalid subcommand.'
        print_basic_usage()
        return

def main():
    if len(sys.argv) < 2:
        print_basic_usage()
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'help':
        print_help()
    elif cmd == 'list':
        do_list()
    elif cmd == 'init':
        if len(sys.argv) != 4:
            print_help()
            sys.exit(1)
        do_init()
    elif cmd == 'backup':
        do_backup()
    elif cmd == 'upgrade':
        do_upgrade()
    else:
        print 'subcommand(%s) is not found.' % cmd
        print_basic_usage()
        sys.exit(1)

