#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import logger as Logger


class TestLogger(unittest.TestCase):

    def test_getLogger_shouldCreateOutputLogFileInTheCurrentFolder_ifLogPathDoesNotExist(self):
        # Given
        filename = "./output.log"
        # When
        Logger.getLogger('WriteMyNote', True, False, None)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

    def test_getLogger_shouldCreateOutputLogFileInNotesPathFolder_ifLogPathExists(self):
        # Given
        filename = "./notes/output.log"
        # When
        Logger.getLogger('WriteMyNote', True, False, "./notes")
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)
