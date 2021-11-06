from aws_cdk import core as cdk
from aws_cdk import core
from aws_cdk import aws_lambda as lambda_bw

class BrandwatchCdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lb_bw_api = lambda_bw.Function(
            scope=self,
            id="BrandwatchAPIExtract",
            runtime=lambda_bw.Runtime.PYTHON_3_9,
            code=aws_cdk.aws_lambda.Code.fromBucket()
        )