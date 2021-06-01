from fastapi.routing import APIRouter
from models.Cities import City, City_Pydantic, CityIn_Pydantic
from dependencies import SingletonAiohttp
import asyncio
# import aiohttp

cityRoutes = APIRouter()

@cityRoutes.get('/cities')
async def get_cities():
    
    cities = await City_Pydantic.from_queryset(City.all())

    tasks = []
    for city in cities:
        task = asyncio.create_task( City.get_current_time(city, SingletonAiohttp.get_aiohttp_client()) )
        tasks.append(task)

    await asyncio.gather(*tasks)
    return cities
# 89234989181
# 516679

@cityRoutes.get('/cities/{city_id}')
async def get_city(city_id: int):
    return await City_Pydantic.from_queryset_single(City.get(id=city_id))

@cityRoutes.post('/cities')
async def create_city(city: CityIn_Pydantic):
    city_obj = await City.create(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_tortoise_orm(city_obj)

@cityRoutes.delete('/cities/{city_id}')
async def delete_city(city_id: int):
    await City.filter(id=city_id).delete()
    return {}