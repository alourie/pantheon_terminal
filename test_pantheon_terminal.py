# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (C) 2013
#
# Author: Daniel Chapman daniel@chapman-mail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
import shutil
import tempfile
from autopilot.matchers import Eventually
from testtools.matchers import Equals, Contains, FileExists, DirExists, DirContains
from pantheon_terminal import TerminalAutopilotTestCase


class TerminalFileSystemTests(TerminalAutopilotTestCase):

    def test_save_a_file(self):
        self.keyboard.type("touch /tmp/test-file\n", delay=0)
        #Verify that test-file has been created
        self.assertTrue('/tmp/testfile', FileExists())
        #Delete the file we created
        self.addCleanup(os.remove, "/tmp/test-file")

    def test_create_directory(self):
        self.keyboard.type('mkdir /tmp/temp-dir\n', delay=0)
        self.assertTrue('/tmp/temp-dir/', DirExists())
        self.addCleanup(os.removedirs, '/tmp/temp-dir')

    def test_directory_contains_files(self):
        self.create_temp_directory_with_temp_files()
        self.assertTrue('/tmp/temp-dir/', DirContains(['a', 'b', 'c']))
        self.addCleanup(shutil.rmtree, '/tmp/temp-dir')

    def test_move_directory_with_files(self):
        self.create_temp_directory_with_temp_files()
        #create directory to move to
        self.keyboard.type('mkdir /tmp/temp-dir2\n', delay=0)
        #move temp-dir to temp-dir2
        self.keyboard.type('mv /tmp/temp-dir/ /tmp/temp-dir2/\n', delay=0)
        #assert dir moved
        self.assertTrue('/tmp/temp-dir2/temp-dir/', DirExists())
        ##assert files moved
        self.assertTrue('/tmp/temp-dir2/temp-dir/', DirContains(['a', 'b', 'c']))

        self.addCleanup(shutil.rmtree, '/tmp/temp-dir2')

    def test_copying_file(self):
        self.create_temp_directory_with_temp_files()
        #create directory to move to
        self.keyboard.type('mkdir /tmp/temp-dir2\n', delay=0)
        #move file 'a' to temp-dir2
        self.keyboard.type('cp /tmp/temp-dir/a /tmp/temp-dir2/\n', delay=0)
        ##assert file moved
        self.assertTrue('/tmp/temp-dir2/temp-dir/', DirContains(['a']))
        self.addCleanup(shutil.rmtree, '/tmp/temp-dir')
        self.addCleanup(shutil.rmtree, '/tmp/temp-dir2')


class TerminalWindowTests(TerminalAutopilotTestCase):

    def test_window_visible(self):
        terminal_window = self.app.select_single('PantheonTerminalPantheonTerminalWindow')
        self.assertThat(terminal_window.visible, Eventually(Equals(1)))

    def test_window_title_simple(self):
        terminal_window = self.app.select_single('PantheonTerminalPantheonTerminalWindow')
        self.assertThat(terminal_window.title, Eventually(Contains('~')))

    def test_window_title_changes_when_changing_directory(self):
        terminal_window = self.app.select_single('PantheonTerminalPantheonTerminalWindow')
        self.keyboard.type('cd\n', delay=0)
        self.keyboard.type('cd Documents\n', delay=0)
        self.assertThat(terminal_window.title, Eventually(Contains('~/Documents')))

    def test_open_new_tab(self):
        #open a new tab
        self.keyboard.press_and_release('Ctrl+Shift+t')
        # test number of tabs(containers) equals 2
        tabs = self.app.select_many('OsThumb')
        self.assertThat(len(tabs), Equals(2))
