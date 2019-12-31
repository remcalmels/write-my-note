#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

loggers = {}


def getLogger(name, debug_mode=False, console_handler=False, log_path=None):

    """
    Pour éviter le problème de doublons sur les logs :
    https://stackoverflow.com/questions/7173033/duplicate-log-output-when-using-python-logging-module
    """
    if loggers.get(name):
        return loggers.get(name)
    else:
        """
        https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
        """
        logger = logging.getLogger(name)
        level = logging.DEBUG if debug_mode else logging.INFO
        logger.setLevel(level)

        if console_handler:
            handler = logging.StreamHandler()
        else:
            if log_path is None:
                log_path = "./"
            filename = os.path.join(log_path, '') + "output.log"
            handler = logging.FileHandler(filename=filename)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%d-%m-%Y %H:%M:%S")
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        loggers[name] = logger
        return logger
