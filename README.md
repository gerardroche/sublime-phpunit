# phpunit

phpunit plugin for Sublime Text. Provides decent PHPUnit support.

**Sublime Text 3 only**

[1.0.0 Roadmap](https://github.com/gerardroche/sublime-phpunit/issues/1)

## Overview

* [Features](#features)
* [Key Bindings](#key-bindings)
* [Installation](#installation)
* [Configuration](#configuration)
* [Similar Plugins](#similar-plugins)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Complementary Plugins](#complementary-plugins)
* [Credits](#credits)
* [License](#license)

## Features

* Run all tests
* Run single test-case or single test *(put cursor on test method)*
* Run last test 
* Run test-case for the current implementation class
* Switch between test-case and implementation class
* Goto to test failure file/line-number
* Composer installed PHPUnit support

The PHPUnit configuration file is found by looking for `phpunit.xml` or `phpunit.xml.dist` in the active view file directory or the nearest common ancestor directory in the current open folders.

If the project has a Composer installed PHPUnit then the Composer installed PHPUnit is used to run the tests.

Example:

    |--- /path/to/code/form/src/Form.php
    |--- /path/to/code/form/test/FormTest.php
    |--- /path/to/code/console/src/Command/ListCommand.php
    `--- /path/to/code/console/test/Command/ListCommandTest.php

With `ListCommandTest.php` open in the current active view, the following locations are checked for the configuration file:

* `/path/to/code/console/test/Command/phpunit.xml`
* `/path/to/code/console/test/Command/phpunit.xml.dist`
* `/path/to/code/console/test/phpunit.xml`
* `/path/to/code/console/test/phpunit.xml.dist`
* `/path/to/code/console/phpunit.xml`
* `/path/to/code/console/phpunit.xml.dist`
* `/path/to/code/phpunit.xml`
* `/path/to/code/phpunit.xml.dist`

The `ListCommandTest.php` test-case can be run from the `ListCommand.php` file using the *Run single test-case* command: <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd>.

The PHPUnit command used to run the tests first looks for a Composer installed PHPUnit i.e. `vendor/bin/phpunit` relative to the directory where the configuration file is found. If no Composer installed PHPUnit is found the command `phpunit` is used.

## Key Bindings

| OS X | Windows / Linux | Description |
|------|-----------------|--------------|
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>t</kbd> | Run all tests |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>r</kbd> | Run single test-case or single test |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>e</kbd> | Run last test command |
| <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>.</kbd> | Switch class-under-test/test-case |
| <kbd>F4</kbd> | <kbd>F4</kbd> | Goto to test failure file/line-number |

Example Vintage/Vintageous keymaps can be found in the default key bindings: `Preferences > Package Settings > PHPUnit > Key Bindings - Default`

## Installation

### Manual installation

1. Download or clone this repository to a directory "phpunit" in the Sublime Text Packages directory for your platform:
    * Sublime Text 3
        - Linux: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/.config/sublime-text-3/Packages/phpunit`
        - OS X: `git clone https://github.com/gerardroche/sublime-phpunit.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/phpunit`
        - Windows: `git clone https://github.com/gerardroche/sublime-phpunit.git %APPDATA%\Sublime/ Text/ 3/Packages/phpunit`
2. Restart Sublime Text to complete installation. The features listed above should now be available.

## Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| save_all_on_run | bool | true | Saves all files before running tests |

Put user settings in a `phpunit.sublime-settings` file. Access this file from the `Preferences > Package Settings > PHPUnit > Settings - User` menu item.

### Per-project settings

To set per-project settings use a "phpunit" key in the project definition settings: `Project > Edit Project`

```json
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "phpunit": {
            "save_all_on_run": false
        }
    }
}
```

### Debug messages

Debug messages are disabled by default. To enable debug messages set an environment variable to a non-blank value e.g. `SUBLIME_PHPUNIT_DEBUG=yes`. To disable, set it to a blank value: `SUBLIME_PHPUNI_DEBUG=` 

On Linux, for example, Sublime Text can be opened at the Terminal with an exported environment variable set:

```sh
export SUBLIME_PHPUNIT_DEBUG=yes; ~/sublime_text_3/sublime_text
```

## Similar Plugins

TODO: Similar Plugins

## Known Bugs

* [F4 navigates to symlinked file out of sync with project](https://github.com/SublimeTextIssues/Core/issues/611)

## Contributing

Issue reports and pull requests are always welcome.

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

TODO: Credits

## License

phpunit is released under the [BSD 3-Clause License][license].

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
