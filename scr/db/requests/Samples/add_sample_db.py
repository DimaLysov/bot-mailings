from sqlalchemy import select, and_

from db.models import async_session
from db.models import Sample
from db.requests.Samples.update_status_sample_db import update_status_sample
from db.requests.Users.get_user_id_db import get_user_id


async def add_sample(chat_id: int, theme: str, text_name: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        sample = await session.scalar(select(Sample).filter(and_(
            Sample.theme == theme
        )))
        if not sample:
            session.add(Sample(user_id=user_id,
                               theme=theme,
                               text_name=text_name))
            await session.commit()
            await update_status_sample(chat_id, theme)
            return True
        return False
