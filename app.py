#!/usr/bin/env python3

import aws_cdk as cdk
from aws.buckets.s3 import AwsS3
from aws.iam.iam import IamStack
from aws.vpc.vpc import VpcStack
from aws.sagemaker.notebooks import NoteBookStack
from aws.ecs.ecs import InstanceECS

app = cdk.App()
AwsS3(app, "AwsS3")
iam = IamStack(app, "IamStack")
vpc_stack = VpcStack(app, "VpcStack")
notebooks = NoteBookStack(app, "NoteBookStack")
InstanceECS(app, "InstanceECS", vpc=vpc_stack, iam=iam)

app.synth()


