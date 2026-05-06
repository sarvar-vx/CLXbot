from aiogram import Dispatcher
from apps.getenv import ENV
from apps.handlers.sections import section_router
from admin.router import admin_router

TOKEN = ENV.bot.BOT_TOKEN
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(section_router)