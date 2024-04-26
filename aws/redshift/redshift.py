#!/usr/bin/env python3

import aws_cdk as cdk
from aws_cdk import RemovalPolicy, aws_s3 as s3
from aws_cdk import aws_redshift as redshift
from aws_cdk import aws_iam as iam
from aws_cdk import Fn
from aws_cdk import aws_ec2 as ec2

class RedshiftStack(cdk.Stack):
    def __init__(self, app: cdk.App, id: str, vpc, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        role_arn = Fn.import_value('RoleArn')
        security_group_redshift = ec2.SecurityGroup(self, "RedshiftSecurityGroup", vpc=vpc.get_vpc)

        # Allow inbound SSH traffic from any IP address
        security_group_redshift.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow SSH access from any IP address"
        )

        # Allow inbound HTTP traffic from any IP address
        security_group_redshift.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP access from any IP address"
        )

        security_group_redshift.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(5439),
            description="Allow Redshift access from any IP address"
        )

        # Subnet Group for Cluster
        demo_cluster_subnet_group = redshift.CfnClusterSubnetGroup(
            self,
            "redshiftDemoClusterSubnetGroup",
            subnet_ids=vpc.get_vpc_public_subnet_ids,
            description="Redshift Demo Cluster Subnet Group"
        )


        # Crear una instancia de Redshift
        redshift.CfnCluster(self, "my-paramo-cluster",
            cluster_type="single-node",
            db_name="paramo_cluster",
            master_username="master_admin",
            master_user_password="*",
            iam_roles=[role_arn],
            node_type="dc2.large",
            cluster_subnet_group_name=demo_cluster_subnet_group.ref,
            publicly_accessible=True,
            vpc_security_group_ids=[security_group_redshift.security_group_id],  # Pass the security group ID
        )

