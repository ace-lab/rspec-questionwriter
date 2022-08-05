# rspec-questionwriter

This is an semi-automated tool to generate Faded Parsons Problems about Ruby RSpec tests to be administered in the Prairielearn Learning Content Management System.

## Important

- This script currently only supports systems that have UNIX `cp`, `rm`, `mkdir`, and `patch` commands added to their `$PATH`.

## Usage
```
usage: python3 -m rsepcFppGen <destination> <application path> <yaml path> [<yaml path 2>] [<yaml path 3>] [...] [<yaml path n>]
```

## Installation
To install this tool for local use:
1) Make sure you have a version of python 3 added to you path with `pip` installed
2) Clone this repository
3) Navigate to rspec-questionwriter/rspecFppGen
4) Run `make install` 

```
.../rspec-questionwriter $ cd rspecFppGen/
.../rspec-questionwriter/rspecFppGen $ make install
<output omitted>
Successfully built rspecFppGen
Installing collected packages: rspecFppGen
Successfully installed rspecFppGen-0.1
.../rspec-questionwriter/rspecFppGen $
```

## Generate questions
To generate questions, first make sure you have this tool installed. Each question requires:
1) A prompt to describe the system under test to the student
2) A system to place under test
3) A correct test suite over that system
4) What segments of the solution to blank out for the student 
5) A number of mutations to be applied to the system under test 

If we have some app in `<dir>/` and would like to generate a question using it, we should write our question a file named `<question_name>.yaml`.
This file should include:
- The prompt of the question (`prompt:`)
- The file that a student test suite would be written to (`submit_to:`)
- The reference test suite (`solution:`)
- And all mutations, heirarchially sorted by variant (`mutations:`)
    - these mutations must be formatted in `diff(1)` standard format

Examples can be seen in the `examples/` directory. For example, after cloning this repository, to make the `leap_year` example question in a new `examples/questions/` directory on a system with python3 installed:
```
.../rspec-questionwriter/ $ cd examples
.../rspec-questionwriter/examples $ mkdir questions
.../rspec-questionwriter/examples $ python -m rspecFppGen questions/ leap_year/app/ leap_year/leap_year.yaml
Running FPP generator
Generating from source examples/questions//leap_year.py
- Extracting from source...
- Creating destination directories...
- Copying leap_year.py to examples/questions/leap_year/source.py ...
- Populating examples/questions/leap_year ...
SyntaxError: Could not extract exports from answer
- Populating examples/questions/leap_year/tests ...
Done.
- Overwriting info.json
- Preparing solution
- Loading common files
- Producing mutations
patching file examples/questions//leap_year//tests/suite0/funcs.rb (read from examples/questions//leap_year//tests/common/funcs.rb)
patching file examples/questions//leap_year//tests/suite1/funcs.rb (read from examples/questions//leap_year//tests/common/funcs.rb)
- Writing grader metadata
.../rspec-questionwriter/examples $ 
```
