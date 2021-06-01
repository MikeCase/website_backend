from fastapi.routing import APIRouter
from models.Users import *

import aiohttp
import asyncio


userRoutes = APIRouter()
session = None

@userRoutes.get('/')
async def get_users():
    users = await User_Pydantic.from_queryset(User.all())
