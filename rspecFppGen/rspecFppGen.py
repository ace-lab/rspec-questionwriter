from socket import SOL_ALG
from subprocess import run, PIPE
from typing import Any, Dict
import yaml
from json import dumps as json_dumps
from sys import argv
import os
from uuid import uuid4

base_info_json = lambda: f"""{{
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

def make_parson_source(generation_dir: str, prompt: str, solution: Dict[str, str], q_name: str) -> None:
    """Make source.py for the Faded-Parson's problem system"""
    source = f"""\"\"\"{prompt}\"\"\"
\n
{json_dumps(solution)}
\n
"""
    write_to(f"{generation_dir}/{q_name}.py", source)
    
def apply_mutation(q_root: str, mutations: str, filename: str, variant_name: str) -> int:
    """runs `patch` on the filename with patchfile input `mutations` and returns stderr as bytes"""
    in_file = f"{q_root}/tests/common/{filename}"
    out_file = f"{q_root}/tests/var_{variant_name}/{filename}"

    command = [
        "patch",
        "-o", out_file,
        in_file,
    ]

    return_code = run(command, input=mutations.encode(), stderr=PIPE).returncode
    return return_code

def generate_variants(q_root: str, variants: Dict):

    # each suite has a set of mutations
    for variant, files in variants.items():
        safe_mkdir(f"{q_root}/tests/var_{variant}")

        for file, mutations in files.items():
            os.makedirs(os.path.dirname(f"{q_root}/tests/var_{variant}/{file}"), exist_ok=True)
            err: int = apply_mutation(q_root, mutations, file, variant)
            if err: # make sure to swap file and mutations args
                raise RuntimeError(f"Unexpected error when applying mutation to {file} in variant {variant}: Exited with code {err}")

def write_solution(q_root: str, solution: str) -> None:
    """Generate tests/solution/_submission_file using the provided solution"""
    write_to(f"{q_root}/tests/solution/_submission_file", solution.replace('?', ''))
    safe_mkdir(f"{q_root}/serverFilesQuestion/")
    write_to(f"{q_root}/serverFilesQuestion/solution.py", solution.replace('?', ''))

def write_metadata(q_root: str, submit_to: str, pre_text: str, post_text: str) -> None:
    write_to(
        f"{q_root}/tests/meta.json", 
        json_dumps({ 
            "submission_file" : submit_to, 
            "submission_root" : "",
            "pre-text" : pre_text,
            "post-text" : post_text
        })
    )

def clean_up(question_root: str) -> None:
    # TODO: remove all files and make it look like we were never here
    print(f"Removing output directory: {question_root}")
    os.system(f"rm -rf {question_root}")
    print("Exiting.")
    exit(1)

def main():
    if len(argv) <= 3:
        print(f"USAGE: {argv[0]} <destination> <application root> <question1_data.yaml> [<question2_data.yaml> <question3_data.yaml> ...]")
        exit(1)

    destination = argv[1]
    common = argv[2]
    yaml_paths = argv[3:]
    for yaml_path in yaml_paths:
        yaml_file = os.path.basename(yaml_path)
        q_name = yaml_file[:yaml_file.index('.')]
        q_root = f"{destination}/{q_name}/"

        content: Dict[str, Any] = yaml.safe_load(open(f"{yaml_path}"))

        assert "solution" in content.keys(), f"`solution:` is a required field in question.yaml"
        assert "submit_to" in content.keys(), f"`submit_to:` is a required field in question.yaml"
        # the other two fields are normally "mutations" and ""

        prompt: str = content.get("prompt", "")
        make_parson_source(destination, prompt, content["solution"], q_name)
        
        print(f"Running FPP generator")
        import generate_fpp
        args = generate_fpp.parse_args(["--no-parse", f"{destination}/{q_name}.py"])
        if args.profile:
            generate_fpp.profile_generate_many(args)
        else:
            generate_fpp.generate_many(args)
        os.system(f"rm {destination}/{q_name}.py")

        print(f"- Overwriting info.json")
        write_to(f"{q_root}/info.json", base_info_json())

        safe_mkdir(f"{q_root}/tests")

        # instructor solution    
        print(f"- Preparing solution")
        safe_mkdir(f"{q_root}/tests/solution")
        write_solution(
            q_root, 
            "\n".join([
                content["solution"]["pre"], 
                content["solution"]["lines"], 
                content["solution"]["post"]
            ])
        )

        # load common files
        print(f"- Loading common files")
        safe_mkdir(f"{q_root}/tests/common")
        os.system(f"cp -r {common}/* {q_root}/tests/common/")

        # load mutations (if any)
        print(f"- Producing mutations")
        mutations = content.get('mutations', [])
        if mutations is not None:
            try:
                generate_variants(q_root, mutations)
            except RuntimeError as e:
                print(e.args[0])
                clean_up(q_root)
        else:
            print(f"No mutations found for {yaml_file}: generating no mutations")

        # load metadata (like what file the submission maps to)
        print(f"- Writing grader metadata")
        write_metadata(q_root, content["submit_to"], content["solution"]["pre"], content["solution"]["post"])

        from io_helpers import Bcolors
        Bcolors.printf(Bcolors.OKGREEN, 'Done.')

if __name__ == "__main__":
    main()
