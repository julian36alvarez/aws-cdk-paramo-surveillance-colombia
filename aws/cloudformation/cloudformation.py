import json
import subprocess

def get_stack_outputs(stack_name, output_keys):
    stack = subprocess.check_output(["aws", "cloudformation", "describe-stacks", "--stack-name", stack_name])
    stack = json.loads(stack)
    outputs = {}
    for output in stack["Stacks"][0]["Outputs"]:
        if output["OutputKey"] in output_keys:
            outputs[output["OutputKey"]] = output["OutputValue"]
    return outputs