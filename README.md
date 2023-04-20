# rspec-questionwriter

This is an semi-automated tool to generate Faded Parsons Problems about Ruby RSpec tests to be administered in the Prairielearn Learning Content Management System.

## Important
This script currently only supports systems that:
- have UNIX `cp`, `rm`, `mkdir`, and `patch` commands added to their `$PATH`.
- have Python 3.8+ installed and added to `$PATH`

## Usage
```
usage: python3 -m rsepcFppGen <destination> <application path> <yaml path> [<yaml path 2>] [<yaml path 3>] [...] [<yaml path n>]
```

Please see [the wiki](https://github.com/ace-lab/rspec-questionwriter/wiki/) for more information
