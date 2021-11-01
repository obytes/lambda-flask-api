import boto3

from app.api.conf import settings


def get_ses_client():
    return boto3.client(
        'ses',
        region_name=settings.AWS_REGION
    )


def get_sns_client():
    return boto3.client(
        'sns',
        region_name=settings.AWS_REGION
    )


def get_ddb_resource():
    return boto3.resource(
        'dynamodb',
        region_name=settings.AWS_REGION
    )
