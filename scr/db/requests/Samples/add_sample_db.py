from sqlalchemy import select

from db.models import async_session
from db.models import Sample
from db.requests.Samples.update_status_sample_db import update_status_sample
from db.requests.Users.get_user_id_db import get_user_id


async def add_sample(chat_id: int, them: str, text: str, photo_name: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        sample = await session.scalar(select(Sample).where(Sample.them == them))
        if not sample:
            session.add(Sample(user_id=user_id,
                               them=them,
                               text=text,
                               photo=photo_name))
            await session.commit()
            await update_status_sample(chat_id, them)
            return True
        return False
