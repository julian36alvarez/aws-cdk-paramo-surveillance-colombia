#!/usr/bin/env python3

import aws_cdk as cdk
from aws.buckets.s3 import AwsS3
from aws.vpc_iam.vpc_iam import VpcIAMStack
from aws.sagemaker.sagemaker import SageMakerStack
import subprocess
import json
app = cdk.App()

AwsS3(app, "AwsS3")
VpcIAMStack(app, "VpcIAMStack")
SageMakerStack(app, "SageMakerStack")
app.synth()


