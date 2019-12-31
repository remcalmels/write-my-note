#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Write-my-note: A notes manager with markdown

    Prerequisites:
        Env var
            - WMN_PATH (required, notes repository path)
            - WMN_EDITOR (optional, specify your favorite text/markdown editor, default="vi")
            - WMN_TOKEN (optional, GitHub access)
            - WMN_LOG (optional, specify the logs path)

    Usage:
        positional arguments:
          {new,list,find,open,remove}
                                action
          subject               subject of the note (new note)
          title                 title of the note (new note)
          content               content of the note (new note)

        optional arguments:
          -h, --help            show this help message and exit
          -file FILE            markdown file to copy content (new note)
          -text TEXT            text to search (open note)
          --debug               debug mode
          --console             to log to the console, logs to ./output.log otherwise
"""

import argparse
import os
import subprocess
import logger as Logger
from git import Repo
from github import Github
import datetime


NOTE_FILE_EXT = ".md"
EDITOR = 'vi'
ENV_NOTES_PATH = 'WMN_PATH'
ENV_EDITOR = 'WMN_EDITOR'
ENV_GIT_TOKEN = 'WMN_TOKEN'
ENV_LOG_PATH = 'WMN_LOG'
GIT_PRIVATE_CHAR = '_'


class WriteMyNote(object):

    def __init__(self,
                 notes_path,
                 action,
                 subject,
                 title,
                 content,
                 file,
                 search,
                 debug_mode=False,
                 console_output=False,
                 github=False):
        self.notes_path = notes_path
        self.action = action
        self.subject = subject
        self.title = title
        self.content = content
        self.file = file
        self.search = search
        self.debug = debug_mode
        self.github = github

        # Logger
        global log
        log = Logger.getLogger('WriteMyNote', debug_mode, console_output, os.environ.get(ENV_LOG_PATH))

    def execute(self):
        print()
        self._init()
        if self.action == 'new':
            self._new_note()
        if self.action == 'list':
            self._list_notes()
        if self.action == 'find':
            self._find_notes()
        if self.action == 'open':
            self._open_note()
        if self.action == 'remove':
            self._remove_note()

    def _init(self):
        if not self.github:
            # No Github
            # Notes directory creation if does not exist
            if not os.path.exists(self.notes_path):
                os.makedirs(self.notes_path)
        else:
            # Github
            if not os.path.exists(self.notes_path):
                # Creates remote repository and clones it
                g = Github(os.environ.get(ENV_GIT_TOKEN))
                repo_name = os.path.basename(os.path.normpath(self.notes_path))
                remote_repo = g.get_user().create_repo(repo_name)
                git_https_url = "https://github.com/" + remote_repo.full_name + ".git"
                self.repo = Repo.clone_from(git_https_url, self.notes_path)
            else:
                # Pull remote changes
                self.repo = Repo(self.notes_path)
                self.repo.git.pull()

    def _list_notes(self):
        nb_notes = 0
        for file in os.listdir(self.notes_path):
            if file.endswith(NOTE_FILE_EXT):
                print(file)
                nb_notes += 1
        print("---\n" + str(nb_notes) + " NOTE(S) FOUND")
        return nb_notes

    def _new_note(self):
        file_path = os.path.join(self.notes_path, self.subject + NOTE_FILE_EXT)
        if not os.path.exists(file_path):
            if self.debug:
                process_debug_logging("Existing file -> update", file_path=file_path)
            f = open(file_path, 'w')
            subject = self.subject
            if subject.startswith(GIT_PRIVATE_CHAR):
                subject = subject[1:]
            f.write("# " + subject.capitalize() + "\n\n")
        else:
            if self.debug:
                process_debug_logging("New file", file_path=file_path)
            f = open(file_path, 'a')
        self._write(f)
        f.close()
        if self.github:
            self._git_push("New note '%s'" % (self.subject + NOTE_FILE_EXT))

    def _write(self, dest_file):
        if self.file is None:
            content = "### " + self.title.capitalize() + "\n" + self.content
        else:
            f = open(self.file, 'r')
            content = f.read()
            f.close()
        text = content + "\n"
        dest_file.write(text)

    def _git_push(self, msg):
        g = self.repo.git
        g.add(A=True)
        g.commit('-m', msg + " - %s" % datetime.datetime.now())
        g.push()

    def _find_notes(self):
        nb_found = 0
        for file in os.listdir(self.notes_path):
            if file.endswith(NOTE_FILE_EXT):
                with open(os.path.join(self.notes_path, file)) as f:
                    lines = f.readlines()
                    for idx, line in enumerate(lines):
                        for part in line.split():
                            if self.search.upper() in part.upper():
                                print(file + " (L" + str(idx + 1) + ")" + " >  " + line)
                                nb_found += 1
                    f.close()
                    if self.debug:
                        process_debug_logging("Content of '%s': " % file, lines)
        return nb_found

    def _open_note(self):
        file_path = os.path.join(self.notes_path, self.subject + NOTE_FILE_EXT)
        if not os.path.exists(file_path):
            msg = "Note not found :|"
            print(msg)
            log.error(msg)
        else:
            cf_editor = os.environ.get(ENV_EDITOR)
            editor = EDITOR if cf_editor is None else cf_editor
            cmd = os.environ.get('EDITOR', editor) + ' ' + file_path
            subprocess.call(cmd, shell=True)
            if self.debug:
                process_debug_logging("Note opened with the editor",
                                      cf_editor=cf_editor,
                                      editor=editor,
                                      file_path=file_path)

    def _remove_note(self):
        file_path = os.path.join(self.notes_path, self.subject + NOTE_FILE_EXT)
        if not os.path.exists(file_path):
            msg = "Note not found :|"
            print(msg)
            log.error(msg)
        else:
            os.remove(file_path)
            if self.github:
                self._git_push("Remove '%s'" % (self.subject + NOTE_FILE_EXT))
            if self.debug:
                log.debug("Note removed")


def process_debug_logging(*args, **kwargs):
    for arg in args:
        log.debug(arg)
    for key, value in kwargs.items():
        log.debug("[%s]= %s" % (key, value))


def main():
    notes_path = os.environ.get(ENV_NOTES_PATH)
    if notes_path == "" or notes_path is None:
        exit("%s must be defined" % ENV_NOTES_PATH)
    parser = argparse.ArgumentParser(description="A notes manager with markdown")
    parser.add_argument('action', choices=['new', 'list', 'find', 'open', 'remove'], help="action")
    parser.add_argument('subject', nargs='?', help="subject of the note (new note)")
    parser.add_argument('title', nargs='?', help="title of the note (new note)")
    parser.add_argument('content', nargs='?', help="content of the note (new note)")
    parser.add_argument('-file', help="markdown file to copy content (new note)")
    parser.add_argument('-text', help="text to search (open note)")
    parser.add_argument('--debug', dest="debug", action="store_true", help="debug mode")
    parser.add_argument('--console', dest="console", action="store_true",
                        help="to log to the console, logs to ./output.log otherwise")
    args = parser.parse_args()
    WriteMyNote(notes_path,
                action=args.action,
                subject=args.subject,
                title=args.title,
                content=args.content,
                file=args.file,
                search=args.text,
                debug_mode=args.debug,
                console_output=args.console,
                github=False if os.environ.get(ENV_GIT_TOKEN) is None else True)\
        .execute()


if __name__ == '__main__':
    main()
