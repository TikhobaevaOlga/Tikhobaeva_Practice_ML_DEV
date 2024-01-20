from arq import create_pool
from arq.connections import RedisSettings

arqsettings = RedisSettings(host='localhost', port=6379, database=1)


class Asyncrq:
    
    async def create_pool(self) -> None:
        self.pool = await create_pool(arqsettings)
        
asyncrq = Asyncrq()