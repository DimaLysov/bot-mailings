from sqlalchemy import select, and_

from db.models import async_session
from db.models import User


async def registration(chat_id: int, user_name: str):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(and_(
            User.chat_id == chat_id
        )))
        if not user:
            session.add(User(chat_id=chat_id, user_name=user_name))
            await session.commit()
            return True
        return False
