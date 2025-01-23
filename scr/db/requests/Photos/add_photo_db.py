from sqlalchemy import select, and_

from db.models import async_session
from db.models import Photo, Sample

async def add_new_photo(name_sample: str, name_photo):
    async with async_session() as session:
        sample = await session.scalar(select(Sample).filter(name_sample == Sample.theme))
        if sample:
            photo = await session.scalar(select(Photo).filter(and_(
                Photo.sample_id == sample.id,
                Photo.name_photo == name_photo
            )))
            if not photo:
                session.add(Photo(sample_id=sample.id,
                                  name_photo=name_photo))
                await session.commit()
                return True
        return False
