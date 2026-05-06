from aiogram import Bot
from datetime import datetime
from apps.getenv import ENV

LOG_CHANNEL = ENV.bot.FORWARDER_CHANNEL


def now() -> str:
    return datetime.now().strftime("%d.%m %H:%M")


async def log_new_user(bot: Bot, user_id: int, full_name: str, username: str) -> None:
    await bot.send_message(
        LOG_CHANNEL,
        f"[{now()}] 👤 Yangi foydalanuvchi — {full_name} (@{username or 'yoq'}) [{user_id}]"
    )


async def log_request(bot: Bot, user_id: int, username: str, category: str, product_name: str) -> None:
    await bot.send_message(
        LOG_CHANNEL,
        f"[{now()}] 📦 So'rov — @{username or user_id} → {product_name} ({category})"
    )


async def log_admin_action(bot: Bot, action: str, name: str, type: str = None) -> None:
    type_str = f" ({type})" if type else ""
    await bot.send_message(
        LOG_CHANNEL,
        f"[{now()}] {action} — {name}{type_str}"
    )


async def log_error(bot: Bot, user_id: int, username: str, product_name: str, reason: str) -> None:
    await bot.send_message(
        LOG_CHANNEL,
        f"[{now()}] ❌ Xato — @{username or user_id} → {product_name} ({reason})"
    )