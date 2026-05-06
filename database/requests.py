from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product, Channel, User


# User requests
# ----------------------------------------------------------------------------------------------------------------------
async def add_user(session: AsyncSession, telegram_id: int, username: str, full_name: str):
    user = await session.get(User, telegram_id)
    if not user:
        session.add(User(id=telegram_id, username=username, full_name=full_name))
        await session.commit()


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()


# Product requests
# ----------------------------------------------------------------------------------------------------------------------
async def add_product(session: AsyncSession, name: str, type: str, message_ids: list):
    session.add(Product(name=name, type=type, message_ids=message_ids))
    await session.commit()


async def get_products_by_type(session: AsyncSession, type: str):
    result = await session.execute(select(Product).where(Product.type == type))
    return result.scalars().all()


async def get_product_by_name(session: AsyncSession, name: str):
    result = await session.execute(select(Product).where(Product.name == name))
    return result.scalar_one_or_none()


async def get_product_by_id(session: AsyncSession, product_id: int):
    return await session.get(Product, product_id)


async def update_product(session: AsyncSession, product_id: int, **kwargs):
    product = await session.get(Product, product_id)
    if product:
        for key, value in kwargs.items():
            setattr(product, key, value)
        await session.commit()


async def delete_product(session: AsyncSession, product_id: int):
    await session.execute(delete(Product).where(Product.id == product_id))
    await session.commit()


# Channel requests
# ----------------------------------------------------------------------------------------------------------------------
async def add_channel(session: AsyncSession, name: str, username: str):
    session.add(Channel(name=name, username=username))
    await session.commit()


async def get_all_channels(session: AsyncSession):
    result = await session.execute(select(Channel))
    return result.scalars().all()


async def delete_channel(session: AsyncSession, channel_id: int):
    await session.execute(delete(Channel).where(Channel.id == channel_id))
    await session.commit()