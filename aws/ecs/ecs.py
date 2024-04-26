from aws_cdk import (
    Stack,
    Fn,
    aws_ecs as ecs,
    aws_iam as iam_aws,
    aws_ecs_patterns as ecs_patterns,
    aws_sagemaker as sagemaker,
    CfnOutput,
    aws_ec2 as ec2,
    Duration,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ssm as ssm,
)
from constructs import Construct


class InstanceECS(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, iam, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role_arn = Fn.import_value("RoleArn")
        role = iam_aws.Role.from_role_arn(self, "Role", role_arn)
        security_group_ecs = ec2.SecurityGroup(
            self, "TaskSecurityGroup", vpc=vpc.get_vpc
        )

        security_group_ecs.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP access from any IP address",
        )

        security_group_ecs.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(8000),
            description="Allow FastApi access from any IP address",
        )

        security_group_ecs.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS access from any IP address",
        )

        security_group_ecs.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow SSH access from any IP address",
        )

        bucket_name = Fn.import_value("BucketName")
        bucket_input_output_name = Fn.import_value("BucketInputOutputName")
        sagemaker_endpoint = ssm.StringParameter.from_string_parameter_attributes(
            self, "SageMakerEndpoint", parameter_name="sagemaker-endpoint-name"
        )

        # Create a cluster in the VPC
        cluster = ecs.Cluster(
            self, "Cluster", vpc=vpc.get_vpc, cluster_name="ParamoCluster"  # rev
        )

        # Create fast-api service as Fargate Task
        fast_api_def = ecs.FargateTaskDefinition(
            self, "FastApiTask", task_role=role, execution_role=role
        )

        fast_api_container = fast_api_def.add_container(
            "FastApiContainer",
            image=ecs.ContainerImage.from_registry("julian36alvarez/fast-api:alpha"),
            environment={
                "BUCKET_LOAD": bucket_name,
                "BUCKET_OUTPUT": bucket_input_output_name,
                "ENDPOINT_NAME": sagemaker_endpoint.string_value,
            },
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "curl -f http://localhost:8000/health || exit 0"],
                start_period=Duration.seconds(10)
            ),
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="FastApiContainer",
            ),
        )

        # Add port mapping to the container, FastApi runs on port 8000
        fast_api_container.add_port_mappings(
            ecs.PortMapping(container_port=8000, protocol=ecs.Protocol.TCP)
        )

        # Get the list of subnet IDs
        subnet_ids = vpc.get_vpc_public_subnet_ids

        # Specify the subnet IDs manually
        #subnet_ids = ["subnet-0f8c23b26505230a2"]  # Replace with your actual subnet IDs

        # Convert the subnet IDs to ISubnet objects
        subnets = [
            ec2.Subnet.from_subnet_id(self, f"Subnet{i}", subnet_id)
            for i, subnet_id in enumerate(subnet_ids)
        ]


        # deploy FastApi service to the cluster with a load balancer
        fast_api_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FastApiService",
            cluster=cluster,
            task_definition=fast_api_def,
            assign_public_ip=True,
            listener_port=80,
            desired_count=1,
            service_name="FastApiService",
            task_subnets=ec2.SubnetSelection(subnets=subnets),
            security_groups=[security_group_ecs],
            cpu=512,  # 0.5 vCPU
            memory_limit_mib=2048
        )

        CfnOutput(
            self,
            "LoadBalancerDNS",
            value=fast_api_service.load_balancer.load_balancer_dns_name,
            export_name="LoadBalancerDNS",
        )
