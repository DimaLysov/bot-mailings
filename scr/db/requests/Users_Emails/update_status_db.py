from sqlalchemy import select, and_

from db.models import async_session
from db.models import UserEmails


async def update_status(user_id: int, email: str):
    async with async_session() as session:
        now_user_email = await session.scalar(select(UserEmails).filter(and_(
            UserEmails.user_id == user_id,
            UserEmails.status.is_(True)
        )))
        if now_user_email:
            now_user_email.status = False
            await session.commit()
        new_user_email = await session.scalar(select(UserEmails).filter(and_(
            UserEmails.user_id == user_id,
            UserEmails.email == email
        )))
        new_user_email.status = True
        await session.commit()
