#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from mock import patch
from write_my_note import WriteMyNote


NOTES_PATH = "notes"
NOTE_SUBJECT = "a_subject"
NOTE_TITLE = "a_title"
NOTE_CONTENT = "a_content"


class TestWriteMyNote(unittest.TestCase):

    def setUp(self):
        self.write_my_note = WriteMyNote(
            NOTES_PATH,
            "list",
            NOTE_SUBJECT,
            NOTE_TITLE,
            NOTE_CONTENT,
            None,
            None,
            debug_mode=True,
            console_output=True
        )

    @patch.object(WriteMyNote, '_new_note')
    def test_execute_shouldCallNewNote_ifActionIsNew(self, wmn_mock):
        # Given
        self.write_my_note.action = 'new'
        # When
        self.write_my_note.execute()
        # Then
        wmn_mock.assert_called_once()

    @patch.object(WriteMyNote, '_list_notes')
    def test_execute_shouldCallListNotes_ifActionIsList(self, wmn_mock):
        # Given
        self.write_my_note.action = 'list'
        # When
        self.write_my_note.execute()
        # Then
        wmn_mock.assert_called_once()

    @patch.object(WriteMyNote, '_find_notes')
    def test_execute_shouldCallFindNotes_ifActionIsFind(self, wmn_mock):
        # Given
        self.write_my_note.action = 'find'
        # When
        self.write_my_note.execute()
        # Then
        wmn_mock.assert_called_once()

    @patch.object(WriteMyNote, '_open_note')
    def test_execute_shouldCallOpenNote_ifActionIsOpen(self, wmn_mock):
        # Given
        self.write_my_note.action = 'open'
        # When
        self.write_my_note.execute()
        # Then
        wmn_mock.assert_called_once()

    def test_listNotes_shouldList2Notes(self):
        # When
        result = self.write_my_note._list_notes()
        # Then
        self.assertEqual(2, result)

    @patch.object(WriteMyNote, '_write')
    def test_newNote_shouldWriteANewFile_whenNoFileWithThisSubjectExists(self, wmn_mock):
        expected_file_path = os.path.join(NOTES_PATH, NOTE_SUBJECT + ".md")
        # When
        self.write_my_note._new_note()
        # Then
        wmn_mock.assert_called_once()
        self.assertTrue(os.path.exists(expected_file_path))
        os.remove(expected_file_path)

    def test_newNote_shouldWriteInExistingFile_whenAFileWithThisSubjectExists(self):
        file_path = os.path.join(NOTES_PATH, NOTE_SUBJECT + ".md")
        # Given
        f = open(file_path, 'w')
        f.write("a line\n")
        f.close()
        # When
        self.write_my_note._new_note()
        # Then
        existing_file = open(file_path, 'r')
        lines_number = len(existing_file.readlines())
        self.assertEqual(3, lines_number)
        existing_file.close()
        os.remove(file_path)

    def test_write_shouldCreateNote(self):
        file_path = os.path.join(NOTES_PATH, NOTE_SUBJECT + ".md")
        f = open(file_path, 'w')
        # When
        self.write_my_note._write(f)
        # Then
        f.close()
        file = open(file_path, 'r')
        content = file.readlines()
        file.close()
        os.remove(file_path)
        self.assertTrue("### " + NOTE_TITLE.upper() in content[0].upper())
        self.assertTrue(NOTE_CONTENT.upper() in content[1].upper())

    def test_write_shouldAddFileContent_whenAMarkdownFileIsSpecified(self):
        file_path = os.path.join(NOTES_PATH, NOTE_SUBJECT + ".md")
        f = open(file_path, 'w')
        # Given
        self.write_my_note.file = "content.md"
        # When
        self.write_my_note._write(f)
        # Then
        f.close()
        file = open(file_path, 'r')
        content = file.readlines()
        file.close()
        os.remove(file_path)
        self.assertTrue("### New subject!" in content[0])
        self.assertTrue("This is the content of the great new subject" in content[1])

    def test_findNotes_shouldFind5Lines(self):
        # Given
        self.write_my_note.search = "Great"
        # When
        result = self.write_my_note._find_notes()
        # Then
        self.assertEqual(5, result)

    @patch('write_my_note.log')
    def test_openNote_shouldLogError_whenNoteIsNotFound(self, log_mock):
        # When
        self.write_my_note._open_note()
        # Then
        log_mock.error.assert_called_with("Note not found for this subject")

    @patch('write_my_note.log')
    @patch('subprocess.call')
    def test_openNote_shouldLogDebug_whenNoteIsOpened(self, sp_mock, log_mock):
        # Given
        sp_mock.return_value = None
        self.write_my_note.subject = "a_note"
        # When
        self.write_my_note._open_note()
        # Then
        log_mock.debug.assert_called_with("[file_path]= notes/a_note.md")
