from arq import ArqRedis, create_pool
from arq.connections import RedisSettings
from typing import Dict, Any
from src.prediction.predict import predict_on_csv

arqsettings = RedisSettings(host="127.0.0.1", port=6379, database=1)


class Asyncrq:
    pool: ArqRedis

    async def create_pool(self) -> None:
        self.pool = await create_pool(arqsettings)


async def startup(ctx: Dict[str, Any]):
    pass


async def shutdown(ctx: Dict[str, Any]):
    pass


class WorkerSettings:
    functions = [predict_on_csv]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = arqsettings


asyncrq = Asyncrq()
