from typing import Any, Dict, List, Tuple
import yaml
from json import dumps as json_dumps
from sys import argv
import os
from uuid import uuid4

base_info_json = f"""
{{
    "uuid": "{uuid4()}",
    "title": "",
    "topic": "",
    "tags": [],
    "type": "v3",
    "gradingMethod" : "External",
    "externalGradingOptions": {{
        "enabled": true,
        "image" : "nalsoon/rspec-autograder",
        "entrypoint": "/grader/run.py",
        "timeout" : 60
    }}
}}
"""

def safe_mkdir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)

def write_to(filename: str, content: str) -> None:
    with open(filename, 'w') as file:
        file.write(content)

def make_parson_source(q_root: str, prompt: str, solution: str) -> None:
    """Make source.py for the Faded-Parson's problem system"""
    with open("source.py" ,'w') as source:
        source.write(f"\"\"\"{prompt}\"\"\"")
        source.write('\n\n')
        source.write(f"## import {q_root}/info.json as info.json ##\n")
        source.write('\n')
        source.write(solution)
        source.write('\n')

def generate_parsons_component() -> None:
    """Generate the necessary components for displaying the parson's problem to the student"""
    # TODO: run logan's tool
    pass

def generate_mutations(q_root: str, mutations: Dict):

    def overlaps(intervals: Tuple[int, int]) -> bool:
        last = intervals[0]
        for intv in intervals[1:]:
            if intv[1] < last[1]:
                return False
        return True

    for suite, files in mutations.items():
        safe_mkdir(f"{q_root}/tests/{suite}")

        for file, mutations in files.items():
            line = 1
            locations = list(map( # basically 'num1-num2' -> { (num1,num2): 'num1-num2', ...}
                lambda s, e: (int(s), int(e)),
                map(
                    lambda i: i.split('-'), 
                    file.keys()
                )
            ))
            locations = sorted(locations, key=(lambda e: e[0]))

            if overlaps(locations):
                clean_up()

            with open(file, 'r') as inp:
                with open(file, 'w') as out:

                    for location in locations:
                        code = file[f"{location[0]}-{location[1]}"]

                        # copy over content before the interval
                        if line < location[0]:
                            out.write(inp.readline(location[0] - line))

                        # skip over content in the interval
                        inp.readline(location[1] - location[0])
                        # insert new content in the interval
                        out.write(inp.readline(code))
                    
                    # add back in everything following the mutations
                    out.writelines(inp.readlines())

def write_solution(q_root: str, solution: str) -> None:
    """Generate suites/solution/_submission_file using the provided solution"""
    with open(f"{q_root}/suites/solution/_submission_file", 'w') as submission_file:
        for line in solution.split('\n'):
            submission_file.writeline(line.replace('?', '') + '\n')

def write_metadata(q_root: str, submit_to: str) -> None:
    with open(f"{q_root}/suites/meta.json", 'w') as meta:
        meta.write(json_dumps({ "submission_file" : submit_to, "submission_root" : "" }))

def clean_up() -> None:
    # TODO: remove all files and make it look like we were never here
    exit(1)

if __name__ == "__main__":
    q_root = argv[1]

    content: Dict[str, Any] = yaml.safe_load(open(f"{q_root}/question.yaml"))

    assert "solution" in content.keys(), f"`solution:` is a required field in question.yaml"
    assert "common" in content.keys(), f"`common:` is a required field in question.yaml"
    assert "submit_to" in content.keys(), f"`submit_to:` is a required field in question.yaml"
    # the other two fields are normally "mutations" and ""

    prompt: str = content.get("prompt", "")
    solution: str = content["solution"]
    # TODO: make info.json
    # write_to("info.json", base_info_json)
    make_parson_source(q_root, prompt, solution)
    
    # should include ans.py, question.html
    generate_parsons_component() 


    safe_mkdir(f"{q_root}/tests")

    # instructor solution    
    safe_mkdir(f"{q_root}/tests/solution")
    write_solution(q_root, solution)

    # load common files
    common = content['common']
    safe_mkdir(f"{q_root}/tests/common")
    os.system(f"cp -r {common}/* {q_root}/tests/common/")

    # load mutations (if any)
    mutations = content.get('mutations', [])
    generate_mutations(q_root, mutations)

    # load metadata (like what file the submission maps to)
    write_metadata(q_root, content['submit_to'])
