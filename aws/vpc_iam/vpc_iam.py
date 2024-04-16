from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    
    CfnOutput
)
from constructs import Construct

class VpcIAMStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=1,
        )

        

        # Security Group
        security_group = ec2.SecurityGroup(self, "NotebookSecurityGroup", vpc=self.vpc)

        CfnOutput(self, "VpcId", value=self.vpc.vpc_id, export_name="VpcId")
        CfnOutput(self, "SecurityGroupId", value=security_group.security_group_id , export_name="SecurityGroupId")
        CfnOutput(self, "SubNetId", value=self.vpc.public_subnets[0].subnet_id , export_name="SubNetId")
        


