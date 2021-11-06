#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from aws_cdk import core
from brandwatch_cdk.brandwatch_cdk_stack import BrandwatchCdkStack

app = core.App()
BrandwatchCdkStack(app, "BrandwatchCdkStack")
app.synth()
