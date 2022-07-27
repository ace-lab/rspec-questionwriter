# rspec-questionwriter

## Important

- This script currently only supports systems that have UNIX `cp`, `rm`, `mkdir`, and `patch` commands added to their `$PATH`.

## Usage
```
usage: python3 -m rsepcFppGen <destination> <application path> <yaml path> [<yaml path 2>] [<yaml path 3>] [...] [<yaml path n>]
```

## Todo
- put this processing in the autograder to avoid a mess with python versions


## Quickstart

To generate a question, you must first write a general ruby application in a directory and then write the metadata required for the question in a yaml file.

If we have some app in `<dir>/` and would like to generate a question using it, we should write our question a file named `<question_name>.yaml`.
This file should include:
- the prompt of the question (`prompt:`)
- the file that a student submission would be written to (`submit_to:`)
- the solution (`solution:`)
- and all mutations, heirarchially sorted by suite (`mutations:`)

Examples can be seen in the `examples/` directory.  
To generate example question files on a system with `python` (version >=3.8) installed, run `make install` in `rspecFppGen/` and run the command above. For example, after cloning this repository, to make the `leap_year` example question on a system with python3 installed:
```
.../rspec-questionwriter $ cd rspecFppGen/
.../rspec-questionwriter/rspecFppGen $ make install
<output omitted>
Successfully built rspecFppGen
Installing collected packages: rspecFppGen
Successfully installed rspecFppGen-0.1
.../rspec-questionwriter/rspecFppGen $ cd ../examples
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
