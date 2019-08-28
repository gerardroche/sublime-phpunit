# CONTRIBUTING

Your issue reports and pull requests are welcome.

### Testing

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press `Enter`, and input **"PHPUnitKit"** as the package to test.

### Debugging

Show the Sublime Text console log: **Menu > View > Show Console**.

Command and input logging are enabled by running the following commands in input box at the bottom of the console:

```
sublime.log_commands(True); sublime.log_input(True)
```

To enable plugin debugging on Unix:

```
$ SUBLIME_PHPUNIT_DEBUG=y subl
```

and on Windows:

```
> set SUBLIME_PHPUNIT_DEBUG=y& "C:\Program Files\Sublime Text 3\subl.exe"
```

### Reverting to a freshly installed state

* [Reverting to a freshly installed state](https://www.sublimetext.com/docs/3/revert.html) (Sublime Text Documentation)
* [Reverting Sublime Text to its default configuration](http://docs.sublimetext.info/en/latest/extensibility/packages.html?highlight=fresh#reverting-sublime-text-to-its-default-configuration) (Unofficial Sublime Text Documentation)

#### Reverting vs Cleaning

On Linux and OSX, [this script](https://github.com/gerardroche/dotfiles/blob/master/src/bin/sublime-clean) can be used to clean caches, indexes, workspaces, sessions, etc. Note that cleaning and reverting are not the same: **reverting** removes installed packages and configurations, **cleaning** only removes files that are generated at runtime e.g. caches, indexes, sessions.
