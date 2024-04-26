from aws_cdk import (
    Stack,
    aws_sagemaker as sagemaker,
    Fn,
)
from constructs import Construct

class NoteBookStack(Stack):

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


        