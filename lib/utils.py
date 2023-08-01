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

import os


if bool(os.getenv('SUBLIME_PHPUNIT_DEBUG')):
    def debug_message(msg, *args) -> None:
        if args:
            msg = msg % args
        print('PHPUnit: ' + msg)

    def is_debug(view) -> bool:
        return True
else:
    def debug_message(msg, *args) -> None:
        pass

    def is_debug(view) -> bool:
        if view:
            return view.settings().get('phpunit.debug')

        return False


def get_setting(view, name: str):
    return view.settings().get('phpunit.%s' % name)
