# rspec-questionwriter

## Usage
```
usage: suites_gen.py [yaml path] [destination] [application path]
```

## Quickstart
`suites_gen.py` calls `generate_fpp.py` and various scripts in `lib/`, do not separate these.

To generate a question, you must first write a general ruby application in a directory and then write the metadata required for the question in a yaml file.

For example, if we have some app in `<dir>/` and would like to generate a question utilizing it, we should write in a file named `<question_name>.yaml`.
This file should include:
- the prompt of the question (`prompt:`)
- the file that a student submission would be written to (`submit_to:`)
- the solution (`solution:`)
- and all mutations, heirarchially sorted by suite (`mutations:`)

An example can be seen in the `examples/` directory
