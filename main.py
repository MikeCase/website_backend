from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.logger import logger
#Only pull what we need in. register_tortoise()
from tortoise.contrib.fastapi import register_tortoise

# import aiohttp

# Import our routes
from routes import Users, Cities
from dependencies import SingletonAiohttp

fastAPI_logger = logger

async def on_start_up() -> None:
    fastAPI_logger.info("on_start_up")
    SingletonAiohttp.get_aiohttp_client()


async def on_shutdown() -> None:
    fastAPI_logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()

app = FastAPI(dependencies=[Depends(on_start_up)])



@app.get('/')
def index():
    return {'key' : 'value'}

app.include_router(Users.userRoutes)
app.include_router(Cities.cityRoutes, dependencies=[Depends(on_start_up)])

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models.Cities', 'models.Users']},
    generate_schemas=True,
    add_exception_handlers=True
)