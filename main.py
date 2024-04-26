import subprocess
from termcolor import colored
from aws.buckets.load_files import upload_folder
from aws.sagemaker.sagemaker import deploy_sagemaker
from aws.cloudformation.cloudformation import get_stack_outputs

def deploy_stack(stack_name):
    result = subprocess.run(["cdk", "deploy", stack_name], text=True)
    if result.returncode != 0:
        print(f"Error deploying {stack_name}: {result.stderr}")
        exit(1)

def main():
    print(colored('🌱♻️ By taking care of water we take care of the future 🌿🌿', 'yellow'))

    deploy_stack("AwsS3")
    outputs = get_stack_outputs("AwsS3", ["BucketName", "BucketInputOutputName"])
    bucket_name = outputs["BucketName"]
    bucket_name_input_output = outputs["BucketInputOutputName"]
    upload_folder('unet-paramo-insights/geojson', bucket_name_input_output)
    upload_folder('unet-paramo-insights', bucket_name)

    deploy_stack("IamStack")
    deploy_stack("VpcStack")
    deploy_stack("NoteBookStack")

    arnRole_outputs = get_stack_outputs("IamStack", ["RoleArn"])
    arnRole = arnRole_outputs["RoleArn"]
    deploy_sagemaker(arnRole, bucket_name)

    deploy_stack("InstanceECS")

if __name__ == "__main__":
    main()