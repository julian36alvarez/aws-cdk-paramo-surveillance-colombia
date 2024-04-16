import json
import subprocess
from aws.buckets.load_files import upload_folder

# S3
subprocess.run(["cdk", "deploy" , "AwsS3"])
stack = subprocess.check_output(["aws", "cloudformation", "describe-stacks", "--stack-name", "AwsS3"])
stack = json.loads(stack)
bucket_name = next(output["OutputValue"] for output in stack["Stacks"][0]["Outputs"] if output["OutputKey"] == "BucketName")

# Upload files to S3
upload_folder('unet-paramo-insights', bucket_name)

# VPC
subprocess.run(["cdk", "deploy" , "VpcIAMStack"])


# SageMaker
subprocess.run(["cdk", "deploy", "SageMakerStack"])

