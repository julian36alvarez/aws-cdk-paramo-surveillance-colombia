from os import path
from aws_cdk import (
    Duration,
    aws_s3 as s3,
    RemovalPolicy,
    Stack,
    CfnOutput,
    aws_iam as iam,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins
)
from constructs import Construct

class AwsS3(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3
        self.bucketSageMaker = s3.Bucket(self, "sagemaker-aws-cdk-paramo-surveillance-colombia",
            removal_policy=RemovalPolicy.DESTROY,  
            auto_delete_objects=True,
        )

        # S3
        tiles_bucket = self.bucketInputOutput= s3.Bucket(self, "input-output-paramo-surveillance-colombia",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            cors=[s3.CorsRule(
                allowed_methods=[s3.HttpMethods.HEAD, s3.HttpMethods.GET],
                allowed_origins=["*"],
                allowed_headers=["*"]
            )]
        )

        # CloudFront OAI
        oai = cloudfront.OriginAccessIdentity(self, "CloudFrontOAI",
            comment="CloudFront OAI for tiles bucket"
        )

        # S3 bucket policy
        tiles_bucket.add_to_resource_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            principals=[iam.ArnPrincipal(f'arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {oai.origin_access_identity_id}')],
            actions=["s3:GetObject"],
            resources=[f'{tiles_bucket.bucket_arn}/*']
        ))

        # CloudFront cache policy
        cache_policy = cloudfront.CachePolicy(self, "CloudFrontCachePolicy",
            cache_policy_name="cloudfront-cache-policy",
            default_ttl=Duration.seconds(86400),
            max_ttl=Duration.seconds(31536000),
            min_ttl=Duration.seconds(1),
            cookie_behavior=cloudfront.CacheCookieBehavior.none(),
            header_behavior=cloudfront.CacheHeaderBehavior.none(),
            enable_accept_encoding_brotli=True,
            enable_accept_encoding_gzip=True,
            query_string_behavior=cloudfront.CacheQueryStringBehavior.none()
        )

        # CloudFront distribution
        cloudfront.Distribution(self, "TilesCDN",
            default_behavior=cloudfront.BehaviorOptions(
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                cache_policy=cache_policy,
                origin=origins.S3Origin(tiles_bucket, origin_access_identity=oai)
            ),
            enabled=True
        )

        CfnOutput(self, "BucketName", value=self.bucketSageMaker.bucket_name, export_name="BucketName")
        CfnOutput(self, "BucketInputOutputName", value=self.bucketInputOutput.bucket_name, export_name="BucketInputOutputName")

    # properties to share with other stacks
    @property
    def get_tiles_bucket(self):
        return self.bucketInputOutput
    
    @property
    def get_sagemaker_bucket(self):
        return self.bucketSageMaker
    
    @property
    def get_sagemaker_bucket_name(self):
        return self.bucketSageMaker.bucket_name
    
    @property
    def get_input_output_bucket_name(self):
        return self.bucketInputOutput.bucket_name

    
        
        
        
