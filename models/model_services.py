from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.model import User
from models.schemas import CoordinatesSchema, NotificationSchema


async def create_or_update_user(
        user_tg_id: int,
        coordinates_data: CoordinatesSchema,
        notification: NotificationSchema,
        db: AsyncSession
) -> bool:
    user = await db.scalar(select(User).where(and_(User.user_tg_id == user_tg_id)))
    if user:
        user.lat = coordinates_data.lat
        user.lon = coordinates_data.lon
        user.notifications_json = notification.json()
        db.add(user)
        await db.commit()
        return False
    user = User(
        user_tg_id=user_tg_id,
        lat=coordinates_data.lat,
        lon=coordinates_data.lon,
        notifications_json=notification.json()
    )
    db.add(user)
    await db.commit()
    return True
