#!/usr/bin/env python3

import aws_cdk as cdk
from aws.buckets.s3 import AwsS3
from aws.vpc_iam.vpc_iam import VpcIAMStack
app = cdk.App()
AwsS3(app, "AwsS3")
VpcIAMStack(app, "VpcIAMStack")

app.synth()


