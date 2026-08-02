import asyncio
from collections.abc import Awaitable, Callable


class EngineScheduler:
    """
    Scheduler interno del Engine.

    Actualmente ejecuta tareas asíncronas en segundo plano.

    En el futuro podrá integrarse con:
        - APScheduler
        - Celery
        - Redis Queue
        - RabbitMQ
        - Kafka
    """

    @staticmethod
    def schedule(task: Callable[..., Awaitable], *args, **kwargs):

        return asyncio.create_task(
            task(*args, **kwargs)
        )

    @staticmethod
    async def run(task: Callable[..., Awaitable], *args, **kwargs):

        return await task(*args, **kwargs)