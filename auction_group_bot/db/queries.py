"""
auction_group_bot/db/queries.py
────────────────────────────────
Изменения:
  1. place_bid — добавлен SELECT ... FOR UPDATE внутри begin()-транзакции.
     Это предотвращает race condition при одновременных ставках из бота
     и мини-аппа, которые оба пишут в одну таблицу.
  Всё остальное без изменений.
"""
from __future__ import annotations

import random
import string
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.database import AsyncSessionLocal, Bid, BannedUser, Lot, LotStatus, Watchlist


# ── Helpers ───────────────────────────────────────────────────

def _gen_code() -> str:
    digits = "".join(random.choices(string.digits, k=3))
    return f"LOT-{digits}"


# ── Lot ───────────────────────────────────────────────────────

async def get_lot(lot_id: int) -> Optional[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot).options(selectinload(Lot.bids)).where(Lot.id == lot_id)
        )
        return result.scalar_one_or_none()


async def get_active_lots() -> list[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot)
            .where(Lot.status.in_([LotStatus.ACTIVE, LotStatus.SCHEDULED]))
            .order_by(Lot.ends_at.nullslast())
        )
        return list(result.scalars().all())


async def create_lot(
    *,
    created_by: int,
    category: str,
    emoji: str,
    title: str,
    description: str,
    start_price: int,
    bid_step: int,
    duration_hours: int,
    blitz_price: Optional[int] = None,
    photo_file_id: Optional[str] = None,
) -> Lot:
    async with AsyncSessionLocal() as s:
        lot = Lot(
            lot_code=_gen_code(),
            created_by=created_by,
            category=category,
            emoji=emoji,
            title=title,
            description=description,
            start_price=start_price,
            bid_step=bid_step,
            duration_hours=duration_hours,
            blitz_price=blitz_price,
            current_price=start_price,
            status=LotStatus.PENDING,
            photo_file_id=photo_file_id,
        )
        s.add(lot)
        await s.commit()
        await s.refresh(lot)
        return lot


async def launch_lot(lot_id: int, topic_id: int, ends_at: datetime) -> Lot:
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.ACTIVE,
                topic_id=topic_id,
                starts_at=None,
                ends_at=ends_at,
                card_message_id=None,
            )
        )
        await s.commit()
    return await get_lot(lot_id)


async def schedule_lot(lot_id: int, topic_id: int, starts_at: datetime) -> Lot:
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.SCHEDULED,
                topic_id=topic_id,
                starts_at=starts_at,
                card_message_id=None,
            )
        )
        await s.commit()
    return await get_lot(lot_id)


async def activate_scheduled_lot(lot_id: int, ends_at: datetime) -> Lot:
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(status=LotStatus.ACTIVE, ends_at=ends_at, starts_at=None)
        )
        await s.commit()
    return await get_lot(lot_id)


async def set_card_message_id(lot_id: int, message_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(card_message_id=message_id)
        )
        await s.commit()


async def finish_lot(lot_id: int, winner_user_id: int, winner_username: str, final_price: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.FINISHED,
                winner_user_id=winner_user_id,
                winner_username=winner_username,
                final_price=final_price,
            )
        )
        await s.commit()


async def cancel_lot(lot_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(status=LotStatus.CANCELLED)
        )
        await s.commit()


async def cancel_lot_no_bids(lot_id: int):
    await cancel_lot(lot_id)


async def extend_lot(lot_id: int, new_ends_at: datetime):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(ends_at=new_ends_at)
        )
        await s.commit()


# Alias used by antisnipe
extend_lot_timer = extend_lot


async def get_pending_lot_by_admin(admin_id: int) -> Optional[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot)
            .where(
                Lot.created_by == admin_id,
                Lot.status == LotStatus.PENDING,
                Lot.topic_id == None,
            )
            .order_by(Lot.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


# ── Bids ──────────────────────────────────────────────────────

async def get_top_bid(lot_id: int) -> Optional[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.amount.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


async def get_bid_count(lot_id: int) -> int:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(func.count()).where(
                Bid.lot_id == lot_id, Bid.is_cancelled == False
            )
        )
        return result.scalar_one()


async def get_unique_bidder_count(lot_id: int) -> int:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(func.count(Bid.user_id.distinct()))
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
        )
        return result.scalar_one()


async def get_recent_bids(lot_id: int, limit: int = 5) -> list[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())


async def get_lot_bids(lot_id: int) -> list[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.amount.desc())
        )
        return list(result.scalars().all())


async def cancel_user_bids(lot_id: int, user_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Bid)
            .where(Bid.lot_id == lot_id, Bid.user_id == user_id)
            .values(is_cancelled=True)
        )
        await s.commit()


async def get_bidders_for_lot(lot_id: int) -> list[dict]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(
                Bid.user_id,
                Bid.username,
                func.max(Bid.amount).label("max_amount"),
            )
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .group_by(Bid.user_id, Bid.username)
            .order_by(func.max(Bid.amount).desc())
        )
        return [
            {"user_id": r.user_id, "username": r.username, "amount": r.max_amount}
            for r in result.all()
        ]


async def place_bid(
    lot_id: int,
    user_id: int,
    username: Optional[str],
    amount: int,
) -> tuple[bool, Optional[str], Optional[Bid]]:
    """
    Разместить ставку.

    ИЗМЕНЕНИЕ: теперь использует SELECT ... FOR UPDATE в рамках одной
    транзакции — это полностью исключает race condition при ставках
    из мини-аппа и бота одновременно.

    Возвращает (success, error_message, bid).
    """
    async with AsyncSessionLocal() as s:
        async with s.begin():
            # Проверка бана
            banned = await s.get(BannedUser, user_id)
            if banned:
                return False, "Вы заблокированы", None

            # Блокировка строки лота — никакая другая транзакция
            # не сможет изменить её до коммита/роллбэка.
            result = await s.execute(
                select(Lot)
                .where(Lot.id == lot_id)
                .with_for_update()
            )
            lot = result.scalar_one_or_none()

            if not lot:
                return False, "Лот не найден", None

            if lot.status != LotStatus.ACTIVE:
                return False, "Аукцион не активен", None

            # Проверить время
            if lot.ends_at:
                ends = (
                    lot.ends_at if lot.ends_at.tzinfo
                    else lot.ends_at.replace(tzinfo=timezone.utc)
                )
                if ends <= datetime.now(timezone.utc):
                    return False, "Время аукциона истекло", None

            # Проверить минимальную сумму по актуальной (заблокированной) цене
            min_bid = lot.current_price + lot.bid_step
            if amount < min_bid:
                return False, f"Минимальная ставка: {min_bid:,} ₽", None

            # Создать ставку и обновить цену
            bid = Bid(
                lot_id=lot_id,
                user_id=user_id,
                username=username,
                amount=amount,
            )
            s.add(bid)
            lot.current_price = amount
            # begin() коммитит автоматически при выходе из блока

    # Перечитать bid из БД (нужен id и created_at)
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(
                Bid.lot_id == lot_id,
                Bid.user_id == user_id,
                Bid.amount == amount,
                Bid.is_cancelled == False,
            )
            .order_by(Bid.id.desc())
            .limit(1)
        )
        bid = result.scalar_one_or_none()

    return True, None, bid


# ── Bans ──────────────────────────────────────────────────────

async def ban_user(user_id: int, username: Optional[str], banned_by: int):
    async with AsyncSessionLocal() as s:
        existing = await s.get(BannedUser, user_id)
        if not existing:
            s.add(BannedUser(user_id=user_id, username=username, banned_by=banned_by))
            await s.commit()


async def is_banned(user_id: int) -> bool:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(BannedUser).where(BannedUser.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None


# ── Watchlist ─────────────────────────────────────────────────

async def add_to_watchlist(lot_id: int, user_id: int, username: Optional[str]):
    async with AsyncSessionLocal() as s:
        existing = await s.execute(
            select(Watchlist).where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        if existing.scalar_one_or_none() is None:
            s.add(Watchlist(lot_id=lot_id, user_id=user_id, username=username))
            await s.commit()


async def remove_from_watchlist(lot_id: int, user_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            Watchlist.__table__.delete().where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        await s.commit()


async def is_watching(lot_id: int, user_id: int) -> bool:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Watchlist).where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        return result.scalar_one_or_none() is not None


async def get_watchers(lot_id: int) -> list[Watchlist]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Watchlist).where(Watchlist.lot_id == lot_id)
        )
        return list(result.scalars().all())


# ── Stats ─────────────────────────────────────────────────────

async def get_stats() -> dict:
    async with AsyncSessionLocal() as s:
        total_lots = (
            await s.execute(select(func.count()).select_from(Lot))
        ).scalar_one()
        finished_lots = (
            await s.execute(
                select(func.count()).where(Lot.status == LotStatus.FINISHED)
            )
        ).scalar_one()
        total_turnover = (
            await s.execute(
                select(func.sum(Lot.final_price)).where(
                    Lot.status == LotStatus.FINISHED
                )
            )
        ).scalar_one() or 0
        total_bids = (
            await s.execute(
                select(func.count()).select_from(Bid).where(Bid.is_cancelled == False)
            )
        ).scalar_one()
        unique_bidders = (
            await s.execute(
                select(func.count(Bid.user_id.distinct())).where(
                    Bid.is_cancelled == False
                )
            )
        ).scalar_one()

    return {
        "total_lots":    total_lots,
        "finished_lots": finished_lots,
        "total_turnover": total_turnover,
        "total_bids":    total_bids,
        "unique_bidders": unique_bidders,
    }


# ── Lots by user bids (Mini App «Мои аукционы») ───────────────

async def get_lots_by_user(user_id: int, limit: int = 50) -> list[dict]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(
                Bid.lot_id,
                Lot.title,
                Lot.emoji,
                Lot.status,
                Lot.winner_user_id,
                Lot.final_price,
                func.max(Bid.amount).label("my_max"),
            )
            .join(Lot, Lot.id == Bid.lot_id)
            .where(Bid.user_id == user_id, Bid.is_cancelled == False)
            .group_by(
                Bid.lot_id, Lot.title, Lot.emoji,
                Lot.status, Lot.winner_user_id, Lot.final_price,
            )
            .order_by(Bid.lot_id.desc())
            .limit(limit)
        )
        rows = result.all()
        return [
            {
                "lot_id":      r.lot_id,
                "title":       r.title,
                "emoji":       r.emoji,
                "status":      r.status,
                "won":         r.winner_user_id == user_id,
                "my_max":      r.my_max,
                "final_price": r.final_price,
            }
            for r in rows
        ]


# ── Rating ────────────────────────────────────────────────────

async def save_rating(lot_id: int, user_id: int, stars: int):
    from db.database import Rating
    async with AsyncSessionLocal() as s:
        existing = await s.execute(
            select(Rating).where(
                Rating.lot_id == lot_id, Rating.user_id == user_id
            )
        )
        rating = existing.scalar_one_or_none()
        if rating:
            rating.stars = stars
        else:
            s.add(Rating(lot_id=lot_id, user_id=user_id, stars=stars))
        await s.commit()


# ── Aliases (для совместимости с bot.py) ──────────────────────

async def update_card_message_id(lot_id: int, message_id: int):
    await set_card_message_id(lot_id, message_id)


async def save_client_photo_file_id(lot_id: int, file_id: str):
    from sqlalchemy import update as sa_update
    async with AsyncSessionLocal() as s:
        await s.execute(
            sa_update(Lot).where(Lot.id == lot_id).values(client_photo_file_id=file_id)
        )
        await s.commit()


# ── pause / resume (добавлено для handlers/manage.py) ─────────

async def pause_lot(lot_id: int, seconds_left: int):
    async with AsyncSessionLocal() as s:
        from sqlalchemy import update as sa_update
        from db.database import LotStatus as _LS
        await s.execute(
            sa_update(Lot).where(Lot.id == lot_id)
            .values(status=_LS.PAUSED, seconds_left=seconds_left)
        )
        await s.commit()


async def resume_lot(lot_id: int, new_ends_at):
    async with AsyncSessionLocal() as s:
        from sqlalchemy import update as sa_update
        from db.database import LotStatus as _LS
        await s.execute(
            sa_update(Lot).where(Lot.id == lot_id)
            .values(status=_LS.ACTIVE, ends_at=new_ends_at, seconds_left=None)
        )
        await s.commit()
