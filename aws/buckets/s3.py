from os import path
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
    Stack,
    CfnOutput,
    aws_iam as iam,
)
from constructs import Construct

class AwsS3(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3
        self.bucket = s3.Bucket(self, "eci-aws-cdk-paramo-surveillance-colombia",
            removal_policy=RemovalPolicy.DESTROY,  
            auto_delete_objects=True,
            
        )

        # IAM
        self.role = iam.Role(self, "Role", assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"))
        # Agregar políticas de acceso completo a SageMaker
        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"))
        self.role.add_to_policy(iam.PolicyStatement(
            actions=["iam:GetRole"],
            resources=["*"],
        ))
        # Add S3 access policy
        self.role.add_to_policy(iam.PolicyStatement(
            actions=["s3:*"],
            resources=[self.bucket.bucket_arn, f"{self.bucket.bucket_arn}/*"],
        ))

        # Grant read/write access to the S3 bucket
        self.bucket.grant_read_write(self.role)

        CfnOutput(self, "BucketName", value=self.bucket.bucket_name, export_name="BucketName")
        CfnOutput(self, "RoleArn", value=self.role.role_arn , export_name="RoleArn")
