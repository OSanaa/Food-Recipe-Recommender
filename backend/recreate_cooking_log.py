import asyncio
from app.database import engine, Base
from app.models.recipe import CookingLog

async def recreate_cooking_log():
    async with engine.begin() as conn:
        await conn.run_sync(CookingLog.__table__.drop)
        await conn.run_sync(CookingLog.__table__.create)
        print("CookingLog table recreated!")

asyncio.run(recreate_cooking_log())