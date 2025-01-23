from sqlalchemy import select, and_

from db.models import async_session
from db.models import Sample
from db.requests.Users.get_user_id_db import get_user_id


async def edit_theme_sample(chat_id: int, now_theme: str, new_theme: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        sample = await session.scalar(select(Sample).filter(and_(
            Sample.theme == now_theme,
            Sample.user_id == user_id
        )))
        if not sample:
            return False
        sample.theme = new_theme
        await session.commit()
        return True