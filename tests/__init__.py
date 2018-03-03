import sublime_plugin

# Sublime Text loads all modules in the root package and initialises all
# commands found in all of those modules. The tests commands are not located in
# the root project because they are only required by the tests. So they need to
# loaded, or "reloaded", when the tests are run.
sublime_plugin.reload_plugin('PHPUnitKit.tests.commands')
