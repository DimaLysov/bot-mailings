from sqlalchemy import select, and_

from db.models import async_session
from db.models import Photo, Sample

async def get_all_photos(name_sample: str):
    async with async_session() as session:
        sample = await session.scalar(select(Sample).filter(name_sample == Sample.theme))
        if sample:
            photos = await session.scalars(select(Photo).filter(Photo.sample_id == sample.id))
            if not photos:
                return None
            names_photos = [photo.name_photo for photo in photos]
            return names_photos
