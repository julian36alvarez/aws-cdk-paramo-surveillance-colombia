import json
import subprocess
from aws_cdk import (
    Stack,
    aws_sagemaker as sagemaker,
    Fn,
)
from constructs import Construct

class SageMakerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = Fn.import_value('BucketName')
        role_arn = Fn.import_value('RoleArn')
        security_group_id = Fn.import_value('SecurityGroupId')
        subnet_id = Fn.import_value('SubNetId')

        sagemaker.CfnNotebookInstanceLifecycleConfig(
            self, "LifecycleConfig",
            notebook_instance_lifecycle_config_name="MyLifecycleConfig"
        )

        # SageMaker Notebook Instance
        self.notebook = sagemaker.CfnNotebookInstance(
            self, "Notebook",
            instance_type="ml.t3.medium", # ml.g4dn.2xlarge ml.t3.medium
            role_arn=role_arn,
            direct_internet_access="Enabled",
            subnet_id=subnet_id,
            security_group_ids=[security_group_id], 
            notebook_instance_name="ParamoNotebook",
            lifecycle_config_name="MyLifecycleConfig",
            default_code_repository="https://github.com/julian36alvarez/unet-paramo-surveillance-colombia"
        )

        primary_container = sagemaker.CfnModel.ContainerDefinitionProperty(
            container_hostname="MyContainer",
            image="763104351884.dkr.ecr.us-east-2.amazonaws.com/tensorflow-inference:2.14.1-gpu",
            image_config=sagemaker.CfnModel.ImageConfigProperty(
                repository_access_mode="Platform",
            ),
            inference_specification_name="inferenceSpecificationName",
            mode="SingleModel",
            model_data_source=sagemaker.CfnModel.ModelDataSourceProperty(
                s3_data_source=sagemaker.CfnModel.S3DataSourceProperty(
                    compression_type="Gzip",
                    s3_data_type="S3Prefix",
                    s3_uri=f"s3://{bucket_name}/models/model.tar.gz"
                )
            ),
        )

        # SageMaker Model
        self.model = sagemaker.CfnModel(
            self, 
            "UnetModel",
            execution_role_arn=role_arn, 
            primary_container=primary_container,
            
        )
'''vpc_config=sagemaker.CfnModel.VpcConfigProperty(
                security_group_ids=[security_group_id],
                subnets=[subnet_id]
            )'''
        
        

       
        

