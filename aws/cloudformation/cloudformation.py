import json
import subprocess

def get_stack_outputs(stack_name):
    stack = subprocess.check_output(["aws", "cloudformation", "describe-stacks", "--stack-name", stack_name])
    stack = json.loads(stack)
    bucket_name = next(output["OutputValue"] for output in stack["Stacks"][0]["Outputs"] if output["OutputKey"] == "BucketName")
    arnRole = next(output["OutputValue"] for output in stack["Stacks"][0]["Outputs"] if output["OutputKey"] == "RoleArn")
    return bucket_name, arnRole