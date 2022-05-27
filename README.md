# rspec-questionwriter

## Important

- `suites_gen.py` calls `generate_fpp.py` and various scripts in `lib/`, do not separate these.
- This script currently only supports systems that have UNIX `cp`, `rm`, `mkdir`, and `patch` commands added to their `$PATH`.

## Usage
```
usage: suites_gen.py [yaml path] [destination] [application path]
```

## Todo
- package this into a python module to avoid the working directory constraint
- put this processing in the autograder to avoid a mess with python versions
  

## Quickstart
`suites_gen.py` calls `generate_fpp.py` and various scripts in `lib/`, do not separate these.

To generate a question, you must first write a general ruby application in a directory and then write the metadata required for the question in a yaml file.

If we have some app in `<dir>/` and would like to generate a question utilizing it, we should write in a file named `<question_name>.yaml`.
This file should include:
- the prompt of the question (`prompt:`)
- the file that a student submission would be written to (`submit_to:`)
- the solution (`solution:`)
- and all mutations, heirarchially sorted by suite (`mutations:`)

Examples can be seen in the `examples/` directory.  
To generate example question files on a system with `python3` installed, navigate to this project's root directory and run the command above. For example, after cloning this repository, to make the `leap_year` example question on a system with `/usr/bin/python3.9`:
```
.../rspec-questionwriter $ mkdir examples/questions
.../rspec-questionwriter $ ./suites_gen.py examples/leap_year/leap_year.yaml examples/questions examples/leap_year/app/
Running FPP generator
Generating from source examples/questions/leap_year.py
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
- Writing grader metadata
.../rspec-questionwriter $ 
```
