# CONTRIBUTING

Your issue reports and pull requests are welcome.

## Debugging

To enable debug mode:

1. Open the Command Palette: `Command Palette → Preferences: PHPUnit Settings`.
2. Set the following setting:
   ```json
   {
       "phpunit.debug": true
   }
   ```

3. To view the console log: `Menu → View → Show Console`

## Testing

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests.

1. Open the Command Palette.
2. Type "UnitTesting" and press `Enter`.
3. Type "PHPUnitKit" and press `Enter`.

## Reverting to a freshly installed state

* [Reverting to a freshly installed state](https://www.sublimetext.com/docs/3/revert.html) (Sublime Text Documentation)
* [Reverting Sublime Text to its default configuration](http://docs.sublimetext.info/en/latest/extensibility/packages.html?highlight=fresh#reverting-sublime-text-to-its-default-configuration) (Unofficial Sublime Text Documentation)

### Reverting vs Cleaning

On Linux and OSX, [this script](https://github.com/gerardroche/dotfiles/blob/master/src/bin/sublime-clean) can be used to clean caches, indexes, workspaces, sessions, etc. Note that cleaning and reverting are not the same: **reverting** removes installed packages and configurations, **cleaning** only removes files that are generated at runtime e.g. caches, indexes, sessions.
