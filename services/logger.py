import logging
import asyncio
from datetime import datetime, timezone, timedelta
from aiogram import Bot
from apps.getenv import ENV

LOG_CHANNEL = ENV.bot.FORWARDER_CHANNEL
UZB = timedelta(hours=5)


def now() -> str:
    return datetime.now(timezone.utc).astimezone(timezone(UZB)).strftime("%d.%m %H:%M")


class ErrorLoggerHandler(logging.Handler):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.setLevel(logging.ERROR)

    def emit(self, record):
        log_entry = self.format(record)
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._send(log_entry))
        except RuntimeError:
            pass

    async def _send(self, message: str):
        try:
            if len(message) > 4000:
                message = message[:4000] + "..."
            await self.bot.send_message(
                LOG_CHANNEL,
                f"❌ <b>Xato!</b>\n\n<code>{message}</code>",
                parse_mode="HTML"
            )
        except Exception:
            pass


def setup_logger(bot: Bot):
    logger = logging.getLogger()
    handler = ErrorLoggerHandler(bot)
    formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(message)s', datefmt='%d.%m %H:%M')
    handler.setFormatter(formatter)
    logger.addHandler(handler)