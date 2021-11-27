from typing import Any, Dict, List
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



def write_solution(q_root: str, solution: str) -> None:
    """Generate suites/solution/_submission_file using the provided solution"""
    with open(f"{q_root}/suites/solution/_submission_file", 'w') as submission_file:
        for line in solution.split('\n'):
            submission_file.writeline(line.replace('?', '') + '\n')

def write_metadata(q_root: str, submit_to: str) -> None:
    with open(f"{q_root}/suites/meta.json", 'w') as meta:
        meta.write(json_dumps({ "submission_file" : submit_to, "submission_root" : "" }))

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
    
    generate_parsons_component()


    safe_mkdir(f"{q_root}/suites")

    # instructor solution    
    safe_mkdir(f"{q_root}/suites/solution")
    write_solution(q_root, solution)

    # load common files
    common = content['common']
    safe_mkdir(f"{q_root}/suites/common")
    # TODO: f"cp -r {commmon}/* suites/common"

    # load mutations (if any)
    mutations = content.get('mutations', [])
    generate_mutation_suites(q_root, mutations)

    # load metadata (like what file the submission maps to)
    write_metadata(q_root, content['submit_to'])
