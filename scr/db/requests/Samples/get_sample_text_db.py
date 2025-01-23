from sqlalchemy import select, and_

from db.models import async_session
from db.models import Sample
from db.requests.Users.get_user_id_db import get_user_id


async def get_name_text(chat_id: int, theme: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        sample = await session.scalar(select(Sample).filter(and_(
            Sample.theme == theme,
            Sample.user_id == user_id
        )))
        return sample.text_name