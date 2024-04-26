from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct

class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC with public and private subnets
        self.vpc = ec2.Vpc(
            self, "VPC",
            max_azs=2,
            subnet_configuration=[
            ec2.SubnetConfiguration(
                name="PublicSubnet",
                subnet_type=ec2.SubnetType.PUBLIC,
            ),
            ec2.SubnetConfiguration(
                name="PrivateSubnet",
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
            ),
            ],
            nat_gateways=1
        )

        # Security Group
        security_group = ec2.SecurityGroup(self, "NotebookSecurityGroup", vpc=self.vpc)
        
        # Or, create a Gateway VPC Endpoint for Amazon S3
        s3_gateway_endpoint = ec2.GatewayVpcEndpoint(self, "VPC S3 Gateway Endpoint",
            service=ec2.GatewayVpcEndpointAwsService.S3,
            vpc=self.vpc)

        CfnOutput(self, "VpcId", value=self.vpc.vpc_id, export_name="VpcId")
        CfnOutput(self, "SecurityGroupId", value=security_group.security_group_id , export_name="SecurityGroupId")
        CfnOutput(self, "S3GatewayEndpointId", value=s3_gateway_endpoint.vpc_endpoint_id, export_name="S3GatewayEndpointId")
        CfnOutput(self, "SubNetId", value=self.vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT).subnet_ids[0], export_name="SubNetId")
    
    @property
    def get_vpc(self):
        return self.vpc

    @property
    def get_vpc_public_subnet_ids(self):
        return self.vpc.select_subnets(
            subnet_type=ec2.SubnetType.PUBLIC
        ).subnet_ids

    @property
    def get_vpc_private_subnet_ids(self):
        return self.vpc.select_subnets(
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
        ).subnet_ids