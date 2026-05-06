from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def force_channels(channels: list):
    ikb = InlineKeyboardBuilder()
    for channel in set(channels):
        ikb.add(InlineKeyboardButton(text="Kanalga Obuna", url=f"https://t.me/{channel.replace('@', '')}"))
    ikb.add(InlineKeyboardButton(text="Tekshirish ✅", callback_data="check_sub"))
    ikb.adjust(1)
    return ikb.as_markup()