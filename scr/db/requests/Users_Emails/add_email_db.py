from sqlalchemy import select

from db.models import async_session
from db.models import UserEmails
from db.requests.Users.get_user_id_db import get_user_id


async def add_email(email: str, password: str, chat_id: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        user_email = await session.scalar(select(UserEmails).where(UserEmails.password == password))
        if not user_email:
            session.add(UserEmails(user_id=user_id,
                                   email=email,
                                   password=password))
            await session.commit()
            return True
        return False
