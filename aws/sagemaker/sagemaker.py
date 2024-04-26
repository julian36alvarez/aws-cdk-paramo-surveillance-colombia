import json
import subprocess
from termcolor import colored
from sagemaker import get_execution_role
from sagemaker.tensorflow import TensorFlowModel
from sagemaker import Session
from botocore.exceptions import ClientError
import boto3

ssm = boto3.client("ssm")

def store_parameter(name, value):
    ssm.put_parameter(
        Name=name,
        Value=value,
        Type="String",
        Overwrite=True,
    )

def get_parameter(name):
    response = ssm.get_parameter(Name=name)
    return response['Parameter']['Value']

def deploy_sagemaker(arnRole, bucket_name):
    # Get the SageMaker execution role
    # Extract the role name from the role ARN

    role_name = arnRole.split("/")[-1]
    sagemaker_session = Session()
    s3_model_location = "s3://{}/models/model.tar.gz".format(bucket_name)

    print(colored(f"Region: {sagemaker_session.boto_region_name}", "blue"))
    print(colored(f"Model location: {s3_model_location}", "blue"))
    print(colored(f"Role name: {role_name}", "blue"))

    print(colored("🤞 Deploying model to SageMaker...", "green"))

    model = TensorFlowModel(
        model_data=s3_model_location,
        role=role_name,
        framework_version="2.14",
        sagemaker_session=sagemaker_session,
    )
    instance_type = "ml.g4dn.xlarge"  # ml.t3.medium
    model.deploy(initial_instance_count=1, instance_type=instance_type)
    store_parameter("sagemaker-endpoint-name", model.endpoint_name)
    print("\n\n")
    print(colored(f"EndpointName {model.endpoint_name}", "blue"))
    print(colored("🎉 Model deployed successfully!", "green"))


def delete_sagemaker_endpoint():
    endpoint_name = get_parameter("sagemaker-endpoint-name")
    print(colored("🗑️ Deleting SageMaker endpoint...", "green"))
    sagemaker_session = Session()
    try:
        sagemaker_session.delete_endpoint(endpoint_name)
        print(colored("🎉 Endpoint deleted successfully!", "green"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "ValidationException":
            print(
                colored(
                    "⚠️ The endpoint does not exist or has already been deleted. Please review your AWS console.",
                    "red",
                )
            )
        else:
            raise


def delete_sagemaker_endpoint_config():
    config_name = get_parameter("sagemaker-endpoint-name")
    print(colored("🗑️ Deleting SageMaker config...", "green"))
    sagemaker_session = Session()
    try:
        sagemaker_session.delete_endpoint_config(config_name)
        print(colored("🎉 Config deleted successfully!", "green"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "ValidationException":
            print(
                colored(
                    "⚠️ The config does not exist or has already been deleted. Please review your AWS console.",
                    "red",
                )
            )
        else:
            raise


def delete_sagemaker_model():
    model_name = get_parameter("sagemaker-endpoint-name")
    print(colored("🗑️ Deleting SageMaker Model...", "green"))
    sagemaker_session = Session()
    try:
        sagemaker_session.delete_model(model_name)
        print(colored("🎉 Model deleted successfully!", "green"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "ValidationException":
            print(
                colored(
                    "⚠️ The model does not exist or has already been deleted. Please review your AWS console.",
                    "red",
                )
            )
        else:
            raise
