import json
import subprocess
from termcolor import colored
from sagemaker import get_execution_role
from sagemaker.tensorflow import TensorFlowModel
from sagemaker import Session
from botocore.exceptions import ClientError

def deploy_sagemaker(arnRole, bucket_name):
        # Get the SageMaker execution role
        # Extract the role name from the role ARN

        role_name = arnRole.split('/')[-1]
        sagemaker_session = Session()
        s3_model_location = "s3://{}/models/model.tar.gz".format(bucket_name)

        print(colored(f'Region: {sagemaker_session.boto_region_name}', 'blue'))
        print(colored(f'Model location: {s3_model_location}', 'blue'))
        print(colored(f'Role name: {role_name}', 'blue'))

        print(colored('🤞 Deploying model to SageMaker...', 'green'))

        model = TensorFlowModel(model_data=s3_model_location, role=role_name, framework_version='2.14', sagemaker_session=sagemaker_session)
        instance_type = 'ml.g4dn.xlarge'
        model.deploy(initial_instance_count=1, instance_type=instance_type)
        print("\n\n")
        print(colored(f'ModelName {model.name}', 'green'))
        print(colored('🎉 Model deployed successfully!', 'green'))



def delete_sagemaker_endpoint(model_name):
    print(colored('🗑️ Deleting SageMaker endpoint...', 'green'))
    sagemaker_session = Session()
    try:
        sagemaker_session.delete_endpoint(model_name)
        print(colored('🎉 Endpoint deleted successfully!', 'green'))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationException':
            print(colored('⚠️ The endpoint does not exist or has already been deleted.', 'yellow'))
        else:
            raise