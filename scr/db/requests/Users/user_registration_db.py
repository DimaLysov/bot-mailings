from sqlalchemy import select

from db.models import async_session
from db.models import User


async def registration(chat_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == chat_id))
        if not user:
            session.add(User(chat_id=chat_id))
            await session.commit()
            return True
        return False
