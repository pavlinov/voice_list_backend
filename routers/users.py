from fastapi import APIRouter, HTTPException
from services.dynamodb import UsersDBService
from datetime import datetime
from utils import STAGE, create_password_hash, verify_password
from models.User import User

router = APIRouter()
users_db = UsersDBService(f'voice-list-users-{STAGE}')

@router.get('/users/{user_id}', tags=['users'])
async def get_user(user_id: str):
    user = users_db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.get('/users/byname/{username}', tags=['users'])
async def get_user(username: str):
    user = users_db.get_user_by_name(username)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.post('/users', tags=['users'])
async def create_user(user_data: dict):
    user = User(**user_data)
    user.password_hash = create_password_hash(user.password)
    response = users_db.create_user(user.to_vlb())
    return response

@router.put('/users/{user_id}', tags=['users'])
async def update_user(user_id: str, user_data: dict):
    user_data['updated_at'] = str(datetime.now())
    response = users_db.update_user_named(user_id, user_data)
    return response

@router.delete('/users/{user_id}', tags=['users'])
async def delete_user(user_id: str):
    response = users_db.delete_user(user_id)
    return response

@router.post('/users/permission', tags=['users'])
async def add_user_permission(user_data: dict):
    user = User(**user_data)
    response = users_db.add_user_permission(user.to_vlb())
    return response
