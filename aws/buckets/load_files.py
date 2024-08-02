
from termcolor import colored

import subprocess

def upload_folder(folder_path, bucket):
    try:
        subprocess.check_call(['aws', 's3', 'sync', folder_path, f's3://{bucket}'])
        print(colored(f'Successfully uploaded {folder_path} to {bucket}', 'green'))
    except subprocess.CalledProcessError:
        print(colored(f'Error uploading {folder_path} to {bucket}', 'red'))