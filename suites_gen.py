from typing import Any, Dict, List, Tuple
import yaml
from json import dumps as json_dumps
from sys import argv
import os
from uuid import uuid4

base_info_json = f"""{{
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

def make_parson_source(q_root: str, prompt: str, solution: str, q_name: str) -> None:
    """Make source.py for the Faded-Parson's problem system"""
    source = f"""\"\"\"{prompt}\"\"\"
\n
{solution}
\n
"""
    write_to(f"{argv[2]}/{q_name}.py", source)
        
def generate_mutations(q_root: str, mutations: Dict):

    def overlaps(intervals: Tuple[int, int]) -> bool:
        last = intervals[0]
        for intv in intervals[1:]:
            if intv[1] < last[1]:
                return True
        return False

    for suite, files in mutations.items():
        safe_mkdir(f"{q_root}/tests/{suite}")

        for file, mutations in files.items():
            line = 1

            locations = map(
                lambda i: i.split('-'), 
                mutations.keys()
            )
            locations = map( # basically 'num1-num2' -> { (num1,num2): 'num1-num2', ...}
                lambda intv: (int(intv[0]), int(intv[1])),
                locations
            )
            locations = sorted(list(locations), key=(lambda e: e[0]))

            if overlaps(locations):
                print(f"Invalid ranges for {file} in {suite}")
                clean_up()

            in_file = f"{q_root}/tests/common/{file}"
            out_file = f"{q_root}/tests/{suite}/{file}"
            with open(in_file, 'r') as inp:
                with open(out_file, 'w') as out:

                    for location in locations:
                        code = mutations[f"{location[0]}-{location[1]}"]
                        if code[-1] != '\n':
                            code += '\n'

                        # copy over content before the interval
                        if line < location[0]:
                            for i in range(location[0] - line):
                                out.writelines(inp.readline())

                        # skip over content in the interval
                        for i in range(location[1] - location[0]):
                            inp.readline()
                        # insert new content in the interval
                        out.write(code)

                        line = location[1]
                    
                    # add back in everything following the mutations
                    out.writelines(inp.readlines())

def write_solution(q_root: str, solution: str) -> None:
    """Generate tests/solution/_submission_file using the provided solution"""
    write_to(f"{q_root}/tests/solution/_submission_file", solution.replace('?', ''))

def write_metadata(q_root: str, submit_to: str) -> None:
    write_to(
        f"{q_root}/tests/meta.json", 
        json_dumps({ "submission_file" : submit_to, "submission_root" : "" })
    )

def clean_up() -> None:
    # TODO: remove all files and make it look like we were never here
    exit(1)

if __name__ == "__main__":
    # q_root = argv[1]
    yaml_path = argv[1]
    yam_file = os.path.basename(yaml_path)
    q_name = yaml_file[:yaml_file.index('.')]
    q_root = f"{argv[2]}/{q_name}/"

    content: Dict[str, Any] = yaml.safe_load(open(f"{yaml_path}"))

    assert "solution" in content.keys(), f"`solution:` is a required field in question.yaml"
    assert "common" in content.keys(), f"`common:` is a required field in question.yaml"
    assert "submit_to" in content.keys(), f"`submit_to:` is a required field in question.yaml"
    # the other two fields are normally "mutations" and ""

    prompt: str = content.get("prompt", "")
    solution: str = content["solution"]
    make_parson_source(q_root, prompt, solution, q_name)
    
    print(f"Running FPP generator")
    os.system(f"/usr/bin/python3 generate_fpp.py {argv[2]}/{q_name}.py")
    os.system(f"rm {argv[2]}/{q_name}.py")

    print(f"- Overwriting info.json")
    write_to(f"{q_root}/info.json", base_info_json)

    safe_mkdir(f"{q_root}/tests")

    # instructor solution    
    print(f"- Preparing solution")
    safe_mkdir(f"{q_root}/tests/solution")
    write_solution(q_root, solution)

    # load common files
    print(f"- Loading common files")
    common = content['common']
    safe_mkdir(f"{q_root}/tests/common")
    os.system(f"cp -r {common}/* {q_root}/tests/common/")

    # load mutations (if any)
    print(f"- Producing mutations")
    mutations = content.get('mutations', [])
    generate_mutations(q_root, mutations)

    # load metadata (like what file the submission maps to)
    print(f"- Writing grader metadata")
    write_metadata(q_root, content['submit_to'])
