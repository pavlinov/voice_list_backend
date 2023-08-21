from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone

from models.User import User
from services.dynamodb import UsersDBService

from utils import STAGE, create_password_hash, verify_password


router = APIRouter()
security = HTTPBasic()

users_db = UsersDBService(f'voice-list-users-{STAGE}')

# Dummy user database (replace with your own DynamoDB integration)
users = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": create_password_hash("testpassword"),
            #"$2b$12$ATYZ1S2D2qJqWCTOBvVOPeeTV4S12adlnWgMu8dmWX3qEl.wHYprC",  # password: testpassword
    },
}

def get_user(username: str):
    if username in users:
        user_dict = users[username]
        return user_dict

@router.post("/login", tags=["login"])
def login(credentials: HTTPBasicCredentials = Depends(security), post_params: dict = None):
    user_obj_id = users_db.get_user_by_name(credentials.username)
    user_response = users_db.get_user_by_id(user_obj_id.get('id'))
    user = User(**user_response)

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Set cookie with expiration time based on whether user wants to stay logged in
    expiration_hours = 24
    if post_params.get('keep_logged_in'):
        expiration_hours = 24 * 30

    expiration = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(hours=expiration_hours)
    response = JSONResponse({
        "token": "fake-super-secret-token",
        "username": credentials.username,
        "user_id": user.id,
        "email": user.email,
        "password": user.password,
        "message": "Logged in successfully"
    })
    response.set_cookie(
        key="session",
        value=f"{credentials.username}",
        expires=expiration,
        httponly=True,
    )
    return response