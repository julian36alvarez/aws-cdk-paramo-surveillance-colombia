import os
import boto3
from termcolor import colored

s3 = boto3.resource('s3')

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        s3.meta.client.upload_file(file_name, bucket, object_name)
        print(colored(f'Successfully uploaded {object_name} to {bucket}', 'green'))
    except Exception as e:
        print(colored(f'Error uploading {object_name} to {bucket}', 'red'))
        return False
    return True

def upload_folder(folder_path, bucket):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            object_name = os.path.relpath(file_path, folder_path).replace(os.sep, '/')
            upload_file(file_path, bucket, object_name)