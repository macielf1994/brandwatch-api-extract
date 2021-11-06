from aws_cdk import core as cdk
from aws_cdk import aws_lambda as lambda_bw
from aws_cdk import aws_s3 as s3_data_lake
from aws_cdk import aws_iam as bw_iam

class BrandwatchCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_bw_api = lambda_bw.Function(
            scope =  self,
            id = "BrandwatchAPIExtract",
            runtime = lambda_bw.Runtime.PYTHON_3_9,
            code = lambda_bw.Code.from_asset('brandwatch_cdk/code'),
            timeout = cdk.Duration.minutes(amount=15),
            handler = "lambda_handler.handler",
            initial_policy = [bw_iam.PolicyStatement(
                actions = "s3:PutObject",
                resources = ['arn:aws:s3:::data-lake-brandtest/*']
            )]
        )

        bucket_data_lake = s3_data_lake.Bucket(
            scope = self,
            id = "S3DataLakeBucket",
            bucket_name = 'data-lake-brandtest',
            block_public_access = s3_data_lake.BlockPublicAccess(restrict_public_buckets = True)
        )