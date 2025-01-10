from sqlalchemy import select, and_

from db.models import async_session
from db.models import UserEmails
from db.requests.Users.get_user_id_db import get_user_id
from db.requests.Users_Emails.update_status_email_db import update_status_email


async def add_email(email: str, password: str, chat_id: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        user_email = await session.scalar(select(UserEmails).where(UserEmails.password == password))
        if not user_email:
            session.add(UserEmails(user_id=user_id,
                                   email=email,
                                   password=password))
            await session.commit()
            user_email = await session.scalar(select(UserEmails).filter(and_(
                UserEmails.user_id == user_id,
                UserEmails.email == email,
                UserEmails.password == password
            )))
            await update_status_email(user_email.user_id, user_email.email)
            return True
        return False
