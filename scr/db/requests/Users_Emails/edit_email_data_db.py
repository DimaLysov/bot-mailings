from sqlalchemy import select, and_

from db.models import async_session
from db.models import UserEmails
from db.requests.Users.get_user_id_db import get_user_id


async def edit_date(chat_id: int, main_email: str, new_value: str, select_user: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        user_email = await session.scalar(select(UserEmails).filter(and_(
            UserEmails.user_id == user_id,
            UserEmails.email == main_email
        )))
        if not user_email:
            return False
        if select_user == 'Почта':
            user_email.email = new_value
        elif select_user == 'Пароль':
            user_email.password = new_value
        await session.commit()
        return True