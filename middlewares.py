import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message
from datetime import datetime, timedelta

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=1.0):
        super().__init__()
        self.limit = limit
        self.last_time = {}

    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id
        now = datetime.now()

        if user_id in self.last_time:
            diff = (now - self.last_time[user_id]).total_seconds()
            if diff < self.limit:
                await event.answer("❗ Juda tez yuboryapsiz, biroz kuting.")
                return  # Handler’ga o‘tkazmaymiz

        self.last_time[user_id] = now
        return await handler(event, data)
