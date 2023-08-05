import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.cloudformation-include",
    "version": "1.118.0",
    "description": "A package that facilitates working with existing CloudFormation templates in the CDK",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.cloudformation_include",
        "aws_cdk.cloudformation_include._jsii"
    ],
    "package_data": {
        "aws_cdk.cloudformation_include._jsii": [
            "cloudformation-include@1.118.0.jsii.tgz"
        ],
        "aws_cdk.cloudformation_include": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.alexa-ask==1.118.0",
        "aws-cdk.aws-accessanalyzer==1.118.0",
        "aws-cdk.aws-acmpca==1.118.0",
        "aws-cdk.aws-amazonmq==1.118.0",
        "aws-cdk.aws-amplify==1.118.0",
        "aws-cdk.aws-apigateway==1.118.0",
        "aws-cdk.aws-apigatewayv2==1.118.0",
        "aws-cdk.aws-appconfig==1.118.0",
        "aws-cdk.aws-appflow==1.118.0",
        "aws-cdk.aws-appintegrations==1.118.0",
        "aws-cdk.aws-applicationautoscaling==1.118.0",
        "aws-cdk.aws-applicationinsights==1.118.0",
        "aws-cdk.aws-appmesh==1.118.0",
        "aws-cdk.aws-apprunner==1.118.0",
        "aws-cdk.aws-appstream==1.118.0",
        "aws-cdk.aws-appsync==1.118.0",
        "aws-cdk.aws-athena==1.118.0",
        "aws-cdk.aws-auditmanager==1.118.0",
        "aws-cdk.aws-autoscaling==1.118.0",
        "aws-cdk.aws-autoscalingplans==1.118.0",
        "aws-cdk.aws-backup==1.118.0",
        "aws-cdk.aws-batch==1.118.0",
        "aws-cdk.aws-budgets==1.118.0",
        "aws-cdk.aws-cassandra==1.118.0",
        "aws-cdk.aws-ce==1.118.0",
        "aws-cdk.aws-certificatemanager==1.118.0",
        "aws-cdk.aws-chatbot==1.118.0",
        "aws-cdk.aws-cloud9==1.118.0",
        "aws-cdk.aws-cloudfront==1.118.0",
        "aws-cdk.aws-cloudtrail==1.118.0",
        "aws-cdk.aws-cloudwatch==1.118.0",
        "aws-cdk.aws-codeartifact==1.118.0",
        "aws-cdk.aws-codebuild==1.118.0",
        "aws-cdk.aws-codecommit==1.118.0",
        "aws-cdk.aws-codedeploy==1.118.0",
        "aws-cdk.aws-codeguruprofiler==1.118.0",
        "aws-cdk.aws-codegurureviewer==1.118.0",
        "aws-cdk.aws-codepipeline==1.118.0",
        "aws-cdk.aws-codestar==1.118.0",
        "aws-cdk.aws-codestarconnections==1.118.0",
        "aws-cdk.aws-codestarnotifications==1.118.0",
        "aws-cdk.aws-cognito==1.118.0",
        "aws-cdk.aws-config==1.118.0",
        "aws-cdk.aws-connect==1.118.0",
        "aws-cdk.aws-cur==1.118.0",
        "aws-cdk.aws-customerprofiles==1.118.0",
        "aws-cdk.aws-databrew==1.118.0",
        "aws-cdk.aws-datapipeline==1.118.0",
        "aws-cdk.aws-datasync==1.118.0",
        "aws-cdk.aws-dax==1.118.0",
        "aws-cdk.aws-detective==1.118.0",
        "aws-cdk.aws-devopsguru==1.118.0",
        "aws-cdk.aws-directoryservice==1.118.0",
        "aws-cdk.aws-dlm==1.118.0",
        "aws-cdk.aws-dms==1.118.0",
        "aws-cdk.aws-docdb==1.118.0",
        "aws-cdk.aws-dynamodb==1.118.0",
        "aws-cdk.aws-ec2==1.118.0",
        "aws-cdk.aws-ecr==1.118.0",
        "aws-cdk.aws-ecs==1.118.0",
        "aws-cdk.aws-efs==1.118.0",
        "aws-cdk.aws-eks==1.118.0",
        "aws-cdk.aws-elasticache==1.118.0",
        "aws-cdk.aws-elasticbeanstalk==1.118.0",
        "aws-cdk.aws-elasticloadbalancing==1.118.0",
        "aws-cdk.aws-elasticloadbalancingv2==1.118.0",
        "aws-cdk.aws-elasticsearch==1.118.0",
        "aws-cdk.aws-emr==1.118.0",
        "aws-cdk.aws-emrcontainers==1.118.0",
        "aws-cdk.aws-events==1.118.0",
        "aws-cdk.aws-eventschemas==1.118.0",
        "aws-cdk.aws-finspace==1.118.0",
        "aws-cdk.aws-fis==1.118.0",
        "aws-cdk.aws-fms==1.118.0",
        "aws-cdk.aws-frauddetector==1.118.0",
        "aws-cdk.aws-fsx==1.118.0",
        "aws-cdk.aws-gamelift==1.118.0",
        "aws-cdk.aws-globalaccelerator==1.118.0",
        "aws-cdk.aws-glue==1.118.0",
        "aws-cdk.aws-greengrass==1.118.0",
        "aws-cdk.aws-greengrassv2==1.118.0",
        "aws-cdk.aws-groundstation==1.118.0",
        "aws-cdk.aws-guardduty==1.118.0",
        "aws-cdk.aws-iam==1.118.0",
        "aws-cdk.aws-imagebuilder==1.118.0",
        "aws-cdk.aws-inspector==1.118.0",
        "aws-cdk.aws-iot1click==1.118.0",
        "aws-cdk.aws-iot==1.118.0",
        "aws-cdk.aws-iotanalytics==1.118.0",
        "aws-cdk.aws-iotcoredeviceadvisor==1.118.0",
        "aws-cdk.aws-iotevents==1.118.0",
        "aws-cdk.aws-iotfleethub==1.118.0",
        "aws-cdk.aws-iotsitewise==1.118.0",
        "aws-cdk.aws-iotthingsgraph==1.118.0",
        "aws-cdk.aws-iotwireless==1.118.0",
        "aws-cdk.aws-ivs==1.118.0",
        "aws-cdk.aws-kendra==1.118.0",
        "aws-cdk.aws-kinesis==1.118.0",
        "aws-cdk.aws-kinesisanalytics==1.118.0",
        "aws-cdk.aws-kinesisfirehose==1.118.0",
        "aws-cdk.aws-kms==1.118.0",
        "aws-cdk.aws-lakeformation==1.118.0",
        "aws-cdk.aws-lambda==1.118.0",
        "aws-cdk.aws-licensemanager==1.118.0",
        "aws-cdk.aws-location==1.118.0",
        "aws-cdk.aws-logs==1.118.0",
        "aws-cdk.aws-lookoutequipment==1.118.0",
        "aws-cdk.aws-lookoutmetrics==1.118.0",
        "aws-cdk.aws-lookoutvision==1.118.0",
        "aws-cdk.aws-macie==1.118.0",
        "aws-cdk.aws-managedblockchain==1.118.0",
        "aws-cdk.aws-mediaconnect==1.118.0",
        "aws-cdk.aws-mediaconvert==1.118.0",
        "aws-cdk.aws-medialive==1.118.0",
        "aws-cdk.aws-mediapackage==1.118.0",
        "aws-cdk.aws-mediastore==1.118.0",
        "aws-cdk.aws-msk==1.118.0",
        "aws-cdk.aws-mwaa==1.118.0",
        "aws-cdk.aws-neptune==1.118.0",
        "aws-cdk.aws-networkfirewall==1.118.0",
        "aws-cdk.aws-networkmanager==1.118.0",
        "aws-cdk.aws-nimblestudio==1.118.0",
        "aws-cdk.aws-opsworks==1.118.0",
        "aws-cdk.aws-opsworkscm==1.118.0",
        "aws-cdk.aws-pinpoint==1.118.0",
        "aws-cdk.aws-pinpointemail==1.118.0",
        "aws-cdk.aws-qldb==1.118.0",
        "aws-cdk.aws-quicksight==1.118.0",
        "aws-cdk.aws-ram==1.118.0",
        "aws-cdk.aws-rds==1.118.0",
        "aws-cdk.aws-redshift==1.118.0",
        "aws-cdk.aws-resourcegroups==1.118.0",
        "aws-cdk.aws-robomaker==1.118.0",
        "aws-cdk.aws-route53==1.118.0",
        "aws-cdk.aws-route53recoverycontrol==1.118.0",
        "aws-cdk.aws-route53recoveryreadiness==1.118.0",
        "aws-cdk.aws-route53resolver==1.118.0",
        "aws-cdk.aws-s3==1.118.0",
        "aws-cdk.aws-s3objectlambda==1.118.0",
        "aws-cdk.aws-s3outposts==1.118.0",
        "aws-cdk.aws-sagemaker==1.118.0",
        "aws-cdk.aws-sam==1.118.0",
        "aws-cdk.aws-sdb==1.118.0",
        "aws-cdk.aws-secretsmanager==1.118.0",
        "aws-cdk.aws-securityhub==1.118.0",
        "aws-cdk.aws-servicecatalog==1.118.0",
        "aws-cdk.aws-servicecatalogappregistry==1.118.0",
        "aws-cdk.aws-servicediscovery==1.118.0",
        "aws-cdk.aws-ses==1.118.0",
        "aws-cdk.aws-signer==1.118.0",
        "aws-cdk.aws-sns==1.118.0",
        "aws-cdk.aws-sqs==1.118.0",
        "aws-cdk.aws-ssm==1.118.0",
        "aws-cdk.aws-ssmcontacts==1.118.0",
        "aws-cdk.aws-ssmincidents==1.118.0",
        "aws-cdk.aws-sso==1.118.0",
        "aws-cdk.aws-stepfunctions==1.118.0",
        "aws-cdk.aws-synthetics==1.118.0",
        "aws-cdk.aws-timestream==1.118.0",
        "aws-cdk.aws-transfer==1.118.0",
        "aws-cdk.aws-waf==1.118.0",
        "aws-cdk.aws-wafregional==1.118.0",
        "aws-cdk.aws-wafv2==1.118.0",
        "aws-cdk.aws-workspaces==1.118.0",
        "aws-cdk.aws-xray==1.118.0",
        "aws-cdk.core==1.118.0",
        "constructs>=3.3.69, <4.0.0",
        "jsii>=1.31.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved",
        "Framework :: AWS CDK",
        "Framework :: AWS CDK :: 1"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
