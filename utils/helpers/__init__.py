import os


def get_aws_region():
    """func to get aws_region value dynamically.
    This way of getting ENV allows mocking needed value in unit-tests for some multi-region features"""
    return os.environ["AWS_REGION"]
