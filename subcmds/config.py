#
# Copyright (C) 2010 JiangXin@ossxp.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from command import Command
from git_command import GitCommand
from error import GitError

class Config(Command):
  common = True
  helpSummary = "Get and set repo config"
  helpUsage = """
%prog name [value]
"""
  helpDescription = """
'%prog' get or set config of the manifest repository.
"""

  def _Options(self, p):
    p.add_option('--bool',
                 dest='bool', action='store_true',
                 help='git config will ensure that the output is "true" or "false"')

  def Execute(self, opt, args):
    if not args:
      self.Usage()

    if len(args) > 1 and not args[0].startswith ('repo.'):
      print >>sys.stderr, "error: can only set config name starts with 'repo.', but you provide '%s'." % args[0]
      sys.exit(1)

    if len(args) > 1 and args[0] == 'repo.mirror':
      print >>sys.stderr, "fatal: reset repo.mirror is not supported on existing client."
      sys.exit(1)

    mp = self.manifest.manifestProject

    command = ["config"]

    if opt.bool:
      command.append('--bool')

    command.extend(args)

    if GitCommand(mp, command).Wait() != 0:
        return -1
