from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Main menu
# ----------------------------------------------------------------------------------------------------------------------
def main_menu() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="💻 Dasturlar"), KeyboardButton(text="🎮 O'yinlar")],
        [KeyboardButton(text="🧲 Torrent"), KeyboardButton(text="ℹ️ Biz haqimizda")],
        [KeyboardButton(text="👨‍💻 Admin bilan bog'lanish")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Programs menu
# ----------------------------------------------------------------------------------------------------------------------
async def programs_menu(products: list) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text=p.name)] for p in products]
    buttons.append([KeyboardButton(text="🔙 Orqaga")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Games menu
# ----------------------------------------------------------------------------------------------------------------------
async def games_menu(products: list) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text=p.name)] for p in products]
    buttons.append([KeyboardButton(text="🔙 Orqaga")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Torrent menu
# ----------------------------------------------------------------------------------------------------------------------
async def torrent_menu(products: list) -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text=p.name)] for p in products]
    buttons.append([KeyboardButton(text="🔙 Orqaga")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Admin menu
# ----------------------------------------------------------------------------------------------------------------------
def admin_menu() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="➕ Qo'shish"), KeyboardButton(text="🗑 O'chirish")],
        [KeyboardButton(text="✏️ Tahrirlash"), KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="📢 E'lon yuborish")],
        [KeyboardButton(text="⬅️ Chiqish")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Add menu
# ----------------------------------------------------------------------------------------------------------------------
def add_menu() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="💻 Dastur"), KeyboardButton(text="🎮 O'yin")],
        [KeyboardButton(text="🧲 Torrent"), KeyboardButton(text="📢 Kanal")],
        [KeyboardButton(text="⬅️ Orqaga")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Edit menu
# ----------------------------------------------------------------------------------------------------------------------
def edit_menu() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="💻 Dastur"), KeyboardButton(text="🎮 O'yin")],
        [KeyboardButton(text="🧲 Torrent")],
        [KeyboardButton(text="⬅️ Orqaga")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Delete menu
# ----------------------------------------------------------------------------------------------------------------------
def delete_menu() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="💻 Dastur"), KeyboardButton(text="🎮 O'yin")],
        [KeyboardButton(text="🧲 Torrent"), KeyboardButton(text="📢 Kanal")],
        [KeyboardButton(text="⬅️ Orqaga")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)