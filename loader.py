from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from data.config import bot_token

dp = Dispatcher()

bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
