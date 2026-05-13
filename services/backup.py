import asyncio
import os
import subprocess
from datetime import datetime, timezone, timedelta
from aiogram import Bot
from aiogram.types import BufferedInputFile
from apps.getenv import ENV

BACKUP_CHANNEL = -1003911807536

UZB = timedelta(hours=5)


def now() -> str:
    return datetime.now(timezone.utc).astimezone(timezone(UZB)).strftime("%d.%m.%Y %H:%M")


async def make_backup(bot: Bot) -> None:
    filename = f"backup_{datetime.now().strftime('%d_%m_%Y')}.sql"
    filepath = f"/tmp/{filename}"

    try:
        db_url = ENV.db.DB_URL.replace("postgresql+asyncpg://", "postgresql://")
        subprocess.run(
            [
                "pg_dump",
                f"--dbname={db_url}",
                f"--file={filepath}"
            ],
            check=True
        )

        with open(filepath, "rb") as f:
            await bot.send_document(
                BACKUP_CHANNEL,
                document=BufferedInputFile(f.read(), filename=filename),
                caption=f"🗄 <b>Backup</b>\n📅 {now()}"
            )

        os.remove(filepath)

    except Exception as e:
        await bot.send_message(
            BACKUP_CHANNEL,
            f"❌ <b>Backup xatosi!</b>\n⚠️ {str(e)}\n📅 {now()}"
        )


async def backup_scheduler(bot: Bot) -> None:
    while True:
        await make_backup(bot)
        await asyncio.sleep(86400)