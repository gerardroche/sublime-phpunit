# Copyright (C) 2023 Gerard Roche
#
# This file is part of PHPUnitKit.
#
# PHPUnitKit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PHPUnitKit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PHPUnitKit.  If not, see <https://www.gnu.org/licenses/>.

import sublime_plugin

# Sublime Text loads all modules in the root package and initialises all
# commands found in all of those modules. The tests commands are not located in
# the root project because they are only required by the tests. So they need to
# loaded, or "reloaded", when the tests are run.
sublime_plugin.reload_plugin('PHPUnitKit.tests.commands')
