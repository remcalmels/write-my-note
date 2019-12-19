#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Write-my-note: A notes manager with markdown

    Prerequisites:
        Env var
            - WRITE_MY_NOTE_PATH (required)
            - WRITE_MY_NOTE_EDITOR (optional, default="vi")

    Usage:
        positional arguments:
          {new,list,find,open}  action
          subject               subject of the note
          title                 title of the note
          content               content of the note

        optional arguments:
          -h, --help            show this help message and exit
          -file FILE            markdown file to copy content
          -text TEXT            text to search
          --debug               debug mode
"""

import argparse
import os
import subprocess
from file_wrapper import FileLineWrapper
import logger as Logger

EDITOR = "vi"


class WriteMyNote(object):

    def __init__(self, notes_path, action, subject, title, content, file, search, debug_mode=False):
        self.notes_path = notes_path
        self.action = action
        self.subject = subject
        self.title = title
        self.content = content
        self.file = file
        self.search = search
        self.debug = debug_mode

        # Logger
        global log
        log = Logger.getLogger('WriteMyNote', debug_mode)

    def execute(self):
        print()
        if self.action == 'new':
            self._new_note()
        if self.action == 'list':
            self._list_notes()
        if self.action == 'find':
            self._find_notes()
        if self.action == 'open':
            self._open_note()

    def _list_notes(self):
        folder = os.listdir(self.notes_path)
        print(str(len(folder)) + " NOTE(S) FOUND:\n---")
        for file in folder:
            if file.endswith(".md"):
                print(file)
        return len(folder)

    def _new_note(self):
        file_path = os.path.join(self.notes_path, self.subject + ".md")
        if not os.path.exists(file_path):
            if self.debug:
                process_debug_logging("Existing file -> update", file_path=file_path)
            f = open(file_path, 'w')
            f.write("# " + self.subject.title() + "\n\n")
        else:
            if self.debug:
                process_debug_logging("New file", file_path=file_path)
            f = open(file_path, 'a')
        self._write(f)
        f.close()

    def _write(self, dest_file):
        if self.file is None:
            content = "### " + self.title.title() + "\n" + self.content
        else:
            f = open(self.file, 'r')
            content = f.read()
            f.close()
        text = content + "\n"
        dest_file.write(text)

    def _find_notes(self):
        nb = 0
        for file in os.listdir(self.notes_path):
            if file.endswith(".md"):
                with FileLineWrapper(open(os.path.join(self.notes_path, file))) as openfile:
                    lines = ""
                    while True:
                        line = openfile.readline().strip()
                        if line == '':
                            # either end of file or just a blank line.....
                            # we'll assume EOF, because we don't have a choice with the while loop!
                            break
                        for part in line.split():
                            if self.search.upper() in part.upper():
                                print(file + " (L" + str(openfile.line) + ")" + " >  " + line)
                                nb += 1
                        if self.debug:
                            lines += line + "\n"
                    openfile.close()
                    if self.debug:
                        process_debug_logging("Content of '%s':" % file, lines)
        return nb

    def _open_note(self):
        file_path = os.path.join(self.notes_path, self.subject + ".md")
        if not os.path.exists(file_path):
            msg = "Note not found for this subject"
            print(msg)
            log.error(msg)
        else:
            cf_editor = os.environ.get('WRITE_MY_NOTE_EDITOR')
            editor = EDITOR if cf_editor is None else cf_editor
            cmd = os.environ.get('EDITOR', editor) + ' ' + file_path
            subprocess.call(cmd, shell=True)
            if self.debug:
                process_debug_logging("Note opened with the editor",
                                      cf_editor=cf_editor,
                                      editor=editor,
                                      file_path=file_path)


def process_debug_logging(*args, **kwargs):
    for arg in args:
        log.debug(arg)
    for key, value in kwargs.items():
        log.debug("[%s]= %s" % (key, value))


def main():
    notes_path = os.environ.get('WRITE_MY_NOTE_PATH')
    if notes_path == "" or notes_path is None:
        exit("WRITE_MY_NOTE_PATH must be defined")
    parser = argparse.ArgumentParser(description="A notes manager with markdown")
    parser.add_argument("action", choices=['new', 'list', 'find', 'open'], help="action")
    parser.add_argument("subject", nargs='?', help="subject of the note (new note)")
    parser.add_argument("title", nargs='?', help="title of the note (new note)")
    parser.add_argument("content", nargs='?', help="content of the note (new note)")
    parser.add_argument("-file", help="markdown file to copy content (new note)")
    parser.add_argument("-text", help="text to search (open note)")
    parser.add_argument("--debug", dest="debug", action="store_true", help="debug mode")
    args = parser.parse_args()
    WriteMyNote(notes_path,
                action=args.action,
                subject=args.subject,
                title=args.title,
                content=args.content,
                file=args.file,
                search=args.text,
                debug_mode=args.debug).execute()


if __name__ == "__main__":
    main()
