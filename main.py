import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from apps.dispatcher import dp
from apps.getenv import ENV
from apps.handlers.sections import section_router
from database.engine import session_maker, create_tables
from middlewares.db import DbSessionMiddleware
from middlewares.subscription import SubscriptionMiddleware
from services.logger import setup_logger
from services.backup import backup_scheduler

TOKEN = ENV.bot.BOT_TOKEN


async def main() -> None:
    await create_tables()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    setup_logger(bot)

    dp.update.middleware(DbSessionMiddleware(session_maker))
    section_router.message.middleware(SubscriptionMiddleware())

    asyncio.create_task(backup_scheduler(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")