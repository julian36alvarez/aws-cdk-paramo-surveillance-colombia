import subprocess
from termcolor import colored
from aws.buckets.load_files import upload_folder
from aws.sagemaker.sagemaker import deploy_sagemaker
from aws.cloudformation.cloudformation import get_stack_outputs

print(colored('🌱♻️ Protecting the moors is protecting your home. 🌿', 'yellow'))

subprocess.run(["cdk", "deploy" , "AwsS3"])

bucket_name, arnRole = get_stack_outputs("AwsS3")

upload_folder('unet-paramo-insights', bucket_name)
subprocess.run(["cdk", "deploy" , "VpcIAMStack"])

# SageMaker
deploy_sagemaker(arnRole, bucket_name)

