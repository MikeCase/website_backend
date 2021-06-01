from fastapi.routing import APIRouter
from models.Users import *

import aiohttp
import asyncio


userRoutes = APIRouter()
session = None

@userRoutes.get('/users')
async def get_users():
    users = await User_Pydantic.from_queryset(User.all())
    
    return users

@userRoutes.post('/newUser', response_model=User_Pydantic)
async def add_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)