from sqlalchemy import select, and_

from db.models import async_session
from db.models import Sample
from db.requests.Users.get_user_id_db import get_user_id


async def get_selected_sample(chat_id: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        sample = await session.scalar(select(Sample).filter(and_(
            Sample.user_id == user_id,
            Sample.status.is_(True)
        )))
        if not sample:
            return None
        return sample
