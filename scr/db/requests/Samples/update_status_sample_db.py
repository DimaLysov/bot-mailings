from sqlalchemy import select, and_

from db.models import async_session
from db.models import Sample
from db.requests.Users.get_user_id_db import get_user_id


async def update_status_sample(chat_id: int, theme: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        now_active_sample = await session.scalar(select(Sample).filter(and_(
            Sample.user_id == user_id,
            Sample.status.is_(True)
        )))
        if now_active_sample:
            now_active_sample.status = False
            await session.commit()
        new_active_sample = await session.scalar(select(Sample).filter(and_(
            Sample.user_id == user_id,
            Sample.theme == theme
        )))
        if new_active_sample:
            new_active_sample.status = True
            await session.commit()
