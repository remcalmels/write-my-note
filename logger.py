#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

loggers = {}


def getLogger(name, debug_mode=False):

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
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%d-%m-%Y %H:%M:%S")
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        loggers[name] = logger
        return logger
