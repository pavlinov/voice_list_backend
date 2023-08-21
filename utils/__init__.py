import os
import bcrypt

from passlib.context import CryptContext
from utils.helpers import get_aws_region

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_stage():
    return os.environ.get("VLEnvironment") or "dev"


STAGE = get_stage()

def get_aws_region():
    """func to get aws_region value dynamically.
    This way of getting ENV allows mocking needed value in unit-tests for some multi-region features"""
    return os.environ["AWS_REGION"]


def create_password_hash(password: str) -> str:
    bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(bytes, b'$2b$12$adwPE2D7Nt18aWWUY2loD.')
    return hashed_password.decode()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
