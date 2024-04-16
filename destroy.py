import subprocess
from termcolor import colored
from aws.sagemaker.sagemaker import delete_sagemaker_endpoint


print(colored('🌱♻️ Protecting the moors is protecting your home. 🌿', 'green'))

#solicitar a el usuario el nombre del modelo a eliminar
model_name = input(colored("☢️ Enter the model name: ", 'yellow'))
delete_sagemaker_endpoint(model_name)

subprocess.run(["cdk", "destroy" , "--all"])

print(colored('🌱🌿🌱🌿🌱🌿🌱 The Stack has been deleted 🌿🌱🌿🌱🌿🌱🌿🌱', 'yellow'))
