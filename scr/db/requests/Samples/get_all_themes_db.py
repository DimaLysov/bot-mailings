from sqlalchemy import select

from db.models import async_session
from db.models import Sample
from db.requests.Users.get_user_id_db import get_user_id


async def get_all_themes(chat_id):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        user_themes = await session.scalars(select(Sample).where(Sample.user_id == user_id))
        if not user_themes:
            return None
        themes = [user_them.them for user_them in user_themes]
        return themes
