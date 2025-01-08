from sqlalchemy import select, and_

from db.models import async_session
from db.models import UserEmails
from db.requests.Users.get_user_id_db import get_user_id


async def get_selected_email(chat_id):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        user_email = await session.scalar(select(UserEmails).filter(and_(
            UserEmails.user_id == user_id,
            UserEmails.status.is_(True)
        )))
        if not user_email:
            return None
        return user_email.email
    