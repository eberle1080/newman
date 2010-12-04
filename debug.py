# NEWMAN: Natural English With Mutating Abridged Nouns
#
# Copyright 2010 Chris Eberle <eberle1080@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

__all__ = ['debug', 'set_debug', 'get_debug']

# Debugging
debugging = False

def debug(*args):
    """
    Print a message to stderr
    """

    global debugging
    if not debugging:
        return
    for stmt in args:
        print >> sys.stderr, stmt,
    print >> sys.stderr
    sys.stderr.flush()

def set_debug(enable):
    """
    Enable or disable debugging
    """

    global debugging
    debugging = enable

def get_debug():
    """
    Return whether or not debugging was enabled
    """

    global debugging
    return debugging
