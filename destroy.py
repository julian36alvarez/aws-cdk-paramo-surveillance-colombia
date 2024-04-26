import subprocess
from termcolor import colored
from aws.sagemaker.sagemaker import delete_sagemaker_endpoint , delete_sagemaker_endpoint_config, delete_sagemaker_model


print(colored('🌱♻️ Protecting the moors is protecting your home. 🌿', 'green'))


delete_sagemaker_endpoint()
delete_sagemaker_endpoint_config()
delete_sagemaker_model()

subprocess.run(["cdk", "destroy" , "--all"])

print(colored('🌱🌿🌱🌿🌱🌿🌱 The Stack has been deleted 🌿🌱🌿🌱🌿🌱🌿🌱', 'yellow'))
