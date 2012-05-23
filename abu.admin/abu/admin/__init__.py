# -*- coding:utf-8 -*-

class Interface(object):
    def version(self):
        raise NotImplementedError

    def init(self, path):
        raise NotImplementedError

    def backup(self, path, backup_file):
        raise NotImplementedError

    def restore(self, path, backup_file):
        raise NotImplementedError

    def upgrade(self, path, old_version):
        raise NotImplementedError

