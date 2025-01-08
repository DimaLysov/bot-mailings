from sqlalchemy import select, and_

from db.models import async_session
from db.models import UserEmails
from db.requests.Users.get_user_id_db import get_user_id


async def get_emails(chat_id: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        user_emails = await session.scalars(select(UserEmails).where(UserEmails.user_id == user_id))
        if not user_emails:
            return None
        emails = [user_email.email for user_email in user_emails]
        return emails
