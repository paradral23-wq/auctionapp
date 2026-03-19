"""
miniapp/backend/database.py
Зеркало auction_admin_bot/db/database.py — держать в синхронизации.
"""
from __future__ import annotations
import enum, os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, Float, Integer, String, Text, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./auction.db")
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=True,  # сбрасывать кеш после commit
    autoflush=True,
)


class Base(DeclarativeBase):
    pass


class LotStatus(str, enum.Enum):
    PENDING   = "pending"
    SCHEDULED = "scheduled"
    ACTIVE    = "active"
    PAUSED    = "paused"
    FINISHED  = "finished"
    CANCELLED = "cancelled"


class Lot(Base):
    __tablename__ = "lots"
    id:           Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_code:     Mapped[str]           = mapped_column(String(20), unique=True)
    category:     Mapped[str]           = mapped_column(String(64))
    emoji:        Mapped[str]           = mapped_column(String(8))
    title:        Mapped[str]           = mapped_column(String(256))
    description:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo_file_id:        Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    client_photo_file_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    # Недвижимость
    property_type:    Mapped[Optional[str]] = mapped_column(String(16),  nullable=True)
    area_sqft:        Mapped[Optional[int]] = mapped_column(Integer,      nullable=True)
    floor_level:      Mapped[Optional[str]] = mapped_column(String(16),  nullable=True)
    view_type:        Mapped[Optional[str]] = mapped_column(String(32),  nullable=True)
    parking_spots:    Mapped[Optional[int]] = mapped_column(Integer,      nullable=True)
    property_status:  Mapped[Optional[str]] = mapped_column(String(16),  nullable=True)
    purchase_price:   Mapped[Optional[int]] = mapped_column(Integer,      nullable=True)
    market_price:     Mapped[Optional[int]] = mapped_column(Integer,      nullable=True)
    discount_pct:     Mapped[Optional[int]] = mapped_column(Integer,      nullable=True)
    price_drop_interval_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    min_price:        Mapped[Optional[int]] = mapped_column(Integer,      nullable=True)

    # Ценообразование
    start_price:   Mapped[int]           = mapped_column(Integer)
    bid_step:      Mapped[int]           = mapped_column(Integer)
    blitz_price:   Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    current_price: Mapped[int]           = mapped_column(Integer)

    # Тайминг
    duration_hours: Mapped[float]              = mapped_column(Float)
    starts_at:      Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at:        Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    seconds_left:   Mapped[Optional[int]]      = mapped_column(Integer, nullable=True)

    topic_id:        Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    card_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    status:     Mapped[LotStatus] = mapped_column(Enum(LotStatus), default=LotStatus.PENDING)
    created_by: Mapped[int]       = mapped_column(BigInteger)
    created_at: Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now())

    winner_user_id:  Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    winner_username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    final_price:     Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    bids:  Mapped[list[Bid]]      = relationship("Bid",      back_populates="lot", order_by="Bid.id.desc()")
    media: Mapped[list["LotMedia"]] = relationship("LotMedia", back_populates="lot", order_by="LotMedia.order")


class LotMedia(Base):
    """Медиафайлы лота — фото и видео.
    Фото: file_id = Telegram file_id, file_path = None
    Видео: file_id = Telegram file_id, file_path = путь на диске сервера
    """
    __tablename__ = "lot_media"

    id:         Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id:     Mapped[int]           = mapped_column(ForeignKey("lots.id"))
    file_id:    Mapped[str]           = mapped_column(String(256))
    file_path:  Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    media_type: Mapped[str]           = mapped_column(String(8))
    order:      Mapped[int]           = mapped_column(Integer, default=0)

    lot: Mapped["Lot"] = relationship("Lot", back_populates="media")


class Bid(Base):
    __tablename__ = "bids"
    id:           Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id:       Mapped[int]           = mapped_column(ForeignKey("lots.id"))
    user_id:      Mapped[int]           = mapped_column(BigInteger)
    username:     Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    amount:       Mapped[int]           = mapped_column(Integer)
    is_cancelled: Mapped[bool]          = mapped_column(Boolean, default=False)
    created_at:   Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())
    lot: Mapped[Lot] = relationship("Lot", back_populates="bids")


class BannedUser(Base):
    __tablename__ = "banned_users"
    id:        Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:   Mapped[int]           = mapped_column(BigInteger, unique=True)
    username:  Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    banned_at: Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())
    banned_by: Mapped[int]           = mapped_column(BigInteger)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        import sqlalchemy as sa
        # Создать lot_media если не существует
        try:
            await conn.execute(sa.text("""
                CREATE TABLE IF NOT EXISTS lot_media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lot_id INTEGER NOT NULL REFERENCES lots(id),
                    file_id VARCHAR(256) NOT NULL,
                    file_path VARCHAR(512),
                    media_type VARCHAR(8) NOT NULL DEFAULT 'photo',
                    "order" INTEGER DEFAULT 0
                )
            """))
        except Exception:
            pass
        # Добавить file_path если таблица уже есть
        try:
            await conn.execute(sa.text("ALTER TABLE lot_media ADD COLUMN file_path VARCHAR(512)"))
        except Exception:
            pass
