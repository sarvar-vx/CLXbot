from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from apps.buttons.inline import force_channels
from apps.handlers.forcefollow import check_subscription


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        bot = data.get("bot")
        session = data.get("session")

        unsubscribed = await check_subscription(bot, event.from_user.id, session)
        if unsubscribed:
            await event.answer(
                "❌ Botdan foydalanish uchun quyidagi kanallarga a'zo bo'ling!",
                reply_markup=force_channels(unsubscribed)
            )
            return

        return await handler(event, data)