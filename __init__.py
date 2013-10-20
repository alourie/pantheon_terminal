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
from autopilot.testcase import AutopilotTestCase
from autopilot.matchers import Eventually
from testtools.matchers import Equals, Contains, FileExists, DirExists
import tempfile
import os


HOME_DIR = os.getenv('HOME')


class TerminalAutopilotTestCase(AutopilotTestCase):

    def setUp(self):
        super(TerminalAutopilotTestCase, self).setUp()
        self.app = self.launch_test_application('pantheon-terminal')

    def create_temp_directory_with_temp_files(self):
        """ Creates a temp directory with temp files 'a' 'b' and 'c' """
        self.keyboard.type('mkdir /tmp/temp-dir\n', delay=0)
        self.keyboard.type('touch /tmp/temp-dir/a\n', delay=0)
        self.keyboard.type('touch /tmp/temp-dir/b\n', delay=0)
        self.keyboard.type('touch /tmp/temp-dir/c\n', delay=0)
