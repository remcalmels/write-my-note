#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A file wrapper to get line number
"""


class FileLineWrapper(object):

    def __init__(self, f):
        self.f = f
        self.line = 0

    def close(self):
        return self.f.close()

    def readline(self):
        self.line += 1
        return self.f.readline()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
