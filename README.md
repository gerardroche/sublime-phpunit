# sublime-phpunit

sublime-phpunit plugin for Sublime Text 3. Provides decent PHPUnit support.

![Screenshot](screenshot.png)

## Overview

* [Features](#features)
* [Key Bindings](#key-bindings)
* [Installation](#installation)
* [Configuration](#configuration)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Roadmap](https://github.com/gerardroche/sublime-phpunit/issues/1)
* [Complementary Plugins](#complementary-plugins)
* [Credits](#credits)
* [License](#license)

## Features

* Run all tests
* Run single test-case
* Run single test method
* Run multiple test methods
* Run the test for the current class
* Rerun last test
* Switch *(and split)* test / implementation
* Goto to next/previous test failure file line number
* Test results formatted in colour including failure diffs
* Toggle TestDox and TAP test results format
* Composer installed PHPUnit support

The PHPUnit configuration file is found by looking for `phpunit.xml` or `phpunit.xml.dist` in the active view file directory or the nearest common ancestor directory in the current open folders. If the project has a Composer installed PHPUnit then the Composer installed PHPUnit is used to run the tests.

## Key Bindings

| OS X | Windows / Linux | Description |
|------|-----------------|--------------|
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | Run all tests |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Run single test-case / test method(s) |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Rerun last test |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch test / implementation |
| <kbd>F4</kbd> | <kbd>F4</kbd> | Goto to next test failure file line number |
| <kbd>Shift</kbd>+<kbd>F4</kbd> | <kbd>Shift</kbd>+<kbd>F4</kbd> | Goto to previous test failure file line number |

To disable the keymaps set `"phpunit.enable_keymaps": false` the User Settings. Access this file from `Preferences > Settings - User` menu item.

Vintage/Vintageous keymaps are disabled by default. To enable them set `"phpunit.enable_vi_keymaps": true` in the User Settings. Access this file from `Preferences > Settings - User` menu item.

| OS X / Windows / Linux | Description |
|------------------------|--------------|
| <kbd>,</kbd><kbd>t</kbd> | Run all tests |
| <kbd>,</kbd><kbd>r</kbd> | Run single test-case / test method(s) |
| <kbd>,</kbd><kbd>e</kbd> | Run last test |
| <kbd>,</kbd><kbd>.</kbd> | Switch test / implementation |

## Installation

### Manual installation

1. Download or clone this repository to a directory `phpunit` in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunit`
    * OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunit`
    * Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunit`
2. Restart Sublime Text to complete installation. The features listed above should now be available.

## Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `save_all_on_run` | `bool` | `true` | Saves all files before running tests |

### User settings

Put user settings in a `phpunit.sublime-settings` file. Access this file from the menu:

`Preferences > Package Settings > PHPUnit > Settings - User`

```json
{
    "save_all_on_run": false
}
```

### Per-project settings

Set per-project settings by prefixing settings with `phpunit.` in the project definition. Access this file from the menu:

`Project > Edit Project`

```json
{
    "settings": {
        "phpunit.save_all_on_run": false
    }
}
```

## Known Bugs

* Sublime Text
    - [F4 navigates to symlinked file out of sync with project](https://github.com/SublimeTextIssues/Core/issues/611)

## Contributing

Issue reports and pull requests are always welcome.

### Debug messages

Debug messages are disabled by default. To enable debug messages set an environment variable to a non-blank value e.g. `SUBLIME_PHPUNIT_DEBUG=yes`. To disable set it to a blank value e.g. `SUBLIME_PHPUNIT_DEBUG=`.

On Linux, for example, Sublime Text can be opened at a Terminal with an exported environment variable:

```sh
export SUBLIME_PHPUNIT_DEBUG=yes; ~/sublime_text_3/sublime_text
```

### Running the tests

On Linux, for example, from the root of the project:

```sh
export SUBLIME_PHPUNIT_DEBUG=; python3 -m unittest discover -t ../ -s tests/ --verbose
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Complementary Plugins

* [php-completions]
* [php-grammar]
* [php-snippets]
* [phpunit-completions]
* [phpunit-snippets]
* [phpunit]

## Credits

sublime-phpunit is based initially on [Sublime Text Ruby Tests](https://github.com/maltize/sublime-text-2-ruby-tests).

## License

sublime-phpunit is released under the [BSD 3-Clause License][license].

[license]: LICENSE
[Package Control]: https://packagecontrol.io
[php-completions]: https://github.com/gerardroche/sublime-phpck
[php-fig]: http://www.php-fig.org
[php-grammar]: https://github.com/gerardroche/sublime-php-grammar
[php-snippets]: https://github.com/gerardroche/sublime-php-snippets
[phpunit-completions]: https://github.com/gerardroche/sublime-phpunitck
[phpunit-snippets]: https://github.com/gerardroche/sublime-phpunit-snippets
[phpunit]: https://github.com/gerardroche/sublime-phpunit
[semver]: http://semver.org
