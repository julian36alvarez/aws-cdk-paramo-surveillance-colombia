from os import path
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
    Stack,
    CfnOutput,
    aws_iam as iam,
    Fn
)
from constructs import Construct


class IamStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import the bucket names
        bucket_name = Fn.import_value('BucketName')
        bucket_input_output_name = Fn.import_value('BucketInputOutputName')

        self.role = iam.Role(self, "Role", 
                     assumed_by=iam.CompositePrincipal(
                         iam.ServicePrincipal("sagemaker.amazonaws.com"),
                         iam.ServicePrincipal("redshift.amazonaws.com"),
                         iam.ServicePrincipal("ecs-tasks.amazonaws.com")
                     ))
        
        # Agregar políticas de acceso completo a SageMaker, S3 y ECR
        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"))
        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"))
        self.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonECS_FullAccess"))

        # Bucket instances
        bucket = s3.Bucket.from_bucket_name(self, "ImportedBucket", bucket_name)
        bucket_input_output = s3.Bucket.from_bucket_name(self, "ImportedBucketIO", bucket_input_output_name)
        # Grant read/write access to the S3 bucket
        bucket.grant_read_write(self.role)
        bucket_input_output.grant_read_write(self.role)

        CfnOutput(self, "RoleArn", value=self.role.role_arn , export_name="RoleArn")
        CfnOutput(self, "RoleName", value=self.role.role_name, export_name="RoleName")
        CfnOutput(self, "RoleId", value=self.role.role_id, export_name="RoleId")


    @property
    def get_role(self):
        return self.role
    
    @property
    def get_role_arn(self):
        return self.role.role_arn
    
    @property
    def get_role_name(self):
        return self.role.role_name