from sqlalchemy import select, and_

from db.models import async_session
from db.models import Photo, Sample

async def delete_photo(name_sample: str):
    async with async_session() as session:
        sample = await session.scalar(select(Sample).filter(name_sample == Sample.theme))
        if sample:
            photos = await session.scalars(select(Photo).filter(Photo.sample_id == sample.id))
            if photos:
                for photo in photos:
                    await session.delete(photo)
                    await session.commit()
                return True
        return False