from sqlalchemy import select

from db.models import async_session
from db.models import User


async def get_user_id(chat_id: int) -> int | None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == chat_id))
        if not user:
            return None
        return user.id
