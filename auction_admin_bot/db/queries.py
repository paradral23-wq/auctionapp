from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.database import AsyncSessionLocal, Admin, Bid, BannedUser, Lot, LotStatus


# ── Helpers ───────────────────────────────────────────────────

async def _gen_code(session: AsyncSession) -> str:
    result = await session.execute(select(func.count()).select_from(Lot))
    count = result.scalar_one()
    return f"LOT-{count + 1:04d}"


# ── Lot CRUD ──────────────────────────────────────────────────

async def create_lot(
    *,
    created_by: int,
    category: str,
    emoji: str,
    title: str,
    description: str,
    start_price: int,
    bid_step: int,
    duration_hours: float,
    blitz_price: Optional[int] = None,
    photo_file_id: Optional[str] = None,
    # ── Поля недвижимости ──────────────────────────────────────
    property_type: Optional[str] = None,
    area_sqft: Optional[int] = None,
    floor_level: Optional[str] = None,
    view_type: Optional[str] = None,
    parking_spots: Optional[int] = None,
    property_status: Optional[str] = None,
    purchase_price: Optional[int] = None,
    market_price: Optional[int] = None,
    discount_pct: Optional[int] = None,
    price_drop_interval_minutes: Optional[int] = None,
    min_price: Optional[int] = None,
) -> Lot:
    async with AsyncSessionLocal() as s:
        lot = Lot(
            lot_code=await _gen_code(s),
            created_by=created_by,
            category=category,
            emoji=emoji,
            title=title,
            description=description,
            start_price=start_price,
            bid_step=bid_step,
            duration_hours=duration_hours,
            blitz_price=blitz_price,
            photo_file_id=photo_file_id,
            current_price=start_price,
            status=LotStatus.PENDING,
            # недвижимость
            property_type=property_type,
            area_sqft=area_sqft,
            floor_level=floor_level,
            view_type=view_type,
            parking_spots=parking_spots,
            property_status=property_status,
            purchase_price=purchase_price,
            market_price=market_price,
            discount_pct=discount_pct,
            price_drop_interval_minutes=price_drop_interval_minutes,
            min_price=min_price,
        )
        s.add(lot)
        await s.commit()
        await s.refresh(lot)
        return lot


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
            .where(Lot.status.in_([LotStatus.SCHEDULED, LotStatus.ACTIVE, LotStatus.PAUSED]))
            .order_by(Lot.created_at)
        )
        return list(result.scalars().all())


async def get_all_lots(limit: int = 20) -> list[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot).order_by(Lot.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())


async def get_draft_lots() -> list[Lot]:
    """Лоты в статусе PENDING (черновики)."""
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot)
            .where(Lot.status == LotStatus.PENDING)
            .order_by(Lot.created_at.desc())
        )
        return list(result.scalars().all())


async def get_finished_lots(limit: int = 10, offset: int = 0) -> tuple[list[Lot], int]:
    """Завершённые и отменённые лоты (включая без победителя)."""
    statuses = [LotStatus.FINISHED, LotStatus.CANCELLED]
    async with AsyncSessionLocal() as s:
        count_result = await s.execute(
            select(func.count()).select_from(Lot).where(Lot.status.in_(statuses))
        )
        total = count_result.scalar_one()
        result = await s.execute(
            select(Lot)
            .where(Lot.status.in_(statuses))
            .order_by(Lot.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all()), total


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


async def activate_scheduled_lot(lot_id: int, ends_at: Optional[datetime] = None) -> Lot:
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(status=LotStatus.ACTIVE, ends_at=ends_at)
        )
        await s.commit()
    return await get_lot(lot_id)


async def launch_lot(lot_id: int, topic_id: int, ends_at: Optional[datetime] = None) -> Lot:
    """Немедленный запуск. ends_at=None для Dutch-аукциона (без фиксированного времени)."""
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


async def set_card_message_id(lot_id: int, message_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(card_message_id=message_id)
        )
        await s.commit()


async def extend_lot(lot_id: int, new_ends_at: datetime):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(ends_at=new_ends_at)
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


# ── Pause / Resume ────────────────────────────────────────────

async def pause_lot(lot_id: int, seconds_left: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(status=LotStatus.PAUSED, seconds_left=seconds_left)
        )
        await s.commit()


async def resume_lot(lot_id: int, new_ends_at: datetime):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(status=LotStatus.ACTIVE, ends_at=new_ends_at, seconds_left=None)
        )
        await s.commit()


# ── Dutch: снижение цены ──────────────────────────────────────

async def drop_lot_price(lot_id: int, new_price: int):
    """Снизить текущую цену лота (Dutch-аукцион)."""
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(current_price=new_price)
        )
        await s.commit()


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
            select(func.count()).where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
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


async def get_lot_bids(lot_id: int, limit: int = 50) -> list[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id)
            .order_by(Bid.created_at.desc())
            .limit(limit)
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
            select(Bid.user_id, Bid.username, func.max(Bid.amount).label("max_amount"))
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .group_by(Bid.user_id, Bid.username)
            .order_by(func.max(Bid.amount).desc())
        )
        return [{"user_id": r.user_id, "username": r.username, "amount": r.max_amount}
                for r in result.all()]


async def place_bid(
    lot_id: int,
    user_id: int,
    username: Optional[str],
    amount: int,
) -> tuple[bool, Optional[str], None]:
    """
    Размещает ставку.
    Для Dutch-аукциона (price_drop_interval_minutes задан, ends_at=None):
      — принимает любую сумму >= current_price (покупка по текущей цене)
      — сразу переводит лот в FINISHED с победителем
    Для классического аукциона:
      — стандартная логика повышения цены
    Возвращает (success, error_message, bid_or_None).
    is_dutch передаётся вторым элементом tuple только внутренне через bid.
    """
    is_dutch = False

    async with AsyncSessionLocal() as s:
        async with s.begin():
            banned = await s.get(BannedUser, user_id)
            if banned:
                return False, "Вы заблокированы", None

            result = await s.execute(
                select(Lot).where(Lot.id == lot_id).with_for_update()
            )
            lot = result.scalar_one_or_none()

            if not lot:
                return False, "Лот не найден", None
            if lot.status != LotStatus.ACTIVE:
                return False, "Аукцион не активен", None

            from datetime import timezone as _tz
            if lot.ends_at:
                ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=_tz.utc)
                if ends <= datetime.now(_tz.utc):
                    return False, "Время аукциона истекло", None

            # Dutch-аукцион: ends_at=None, price_drop_interval_minutes задан
            if lot.price_drop_interval_minutes and not lot.ends_at:
                is_dutch = True
                # Покупка по текущей цене — принимаем amount >= current_price
                if amount < lot.current_price:
                    return False, f"Текущая цена: {lot.current_price:,} AED", None
                # Фиксируем ставку
                bid = Bid(lot_id=lot_id, user_id=user_id, username=username, amount=lot.current_price)
                s.add(bid)
                # Сразу завершаем лот
                lot.status = LotStatus.FINISHED
                lot.winner_user_id = user_id
                lot.winner_username = username or ""
                lot.final_price = lot.current_price
            else:
                # Классический аукцион
                min_bid = lot.current_price + lot.bid_step
                if amount < min_bid:
                    return False, f"Минимальная ставка: {min_bid:,} AED", None
                bid = Bid(lot_id=lot_id, user_id=user_id, username=username, amount=amount)
                s.add(bid)
                lot.current_price = amount

    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.user_id == user_id,
                   Bid.is_cancelled == False)
            .order_by(Bid.id.desc()).limit(1)
        )
        bid = result.scalar_one_or_none()

    return True, None, bid


# ── Stats ─────────────────────────────────────────────────────

async def get_stats() -> dict:
    async with AsyncSessionLocal() as s:
        total_lots = (await s.execute(select(func.count()).select_from(Lot))).scalar_one()
        finished_lots = (await s.execute(
            select(func.count()).where(Lot.status == LotStatus.FINISHED)
        )).scalar_one()
        total_turnover = (await s.execute(
            select(func.sum(Lot.final_price)).where(Lot.status == LotStatus.FINISHED)
        )).scalar_one() or 0
        total_bids = (await s.execute(
            select(func.count()).select_from(Bid).where(Bid.is_cancelled == False)
        )).scalar_one()
        unique_bidders = (await s.execute(
            select(func.count(Bid.user_id.distinct())).where(Bid.is_cancelled == False)
        )).scalar_one()

    return {
        "total_lots": total_lots,
        "finished_lots": finished_lots,
        "total_turnover": total_turnover,
        "total_bids": total_bids,
        "unique_bidders": unique_bidders,
    }


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

async def is_watching(lot_id: int, user_id: int) -> bool:
    from db.database import WatchList
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(WatchList).where(WatchList.lot_id == lot_id, WatchList.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None


async def add_to_watchlist(lot_id: int, user_id: int, username: Optional[str] = None):
    from db.database import WatchList
    async with AsyncSessionLocal() as s:
        existing = await s.execute(
            select(WatchList).where(WatchList.lot_id == lot_id, WatchList.user_id == user_id)
        )
        if existing.scalar_one_or_none() is None:
            s.add(WatchList(lot_id=lot_id, user_id=user_id, username=username))
            await s.commit()


async def remove_from_watchlist(lot_id: int, user_id: int):
    from db.database import WatchList
    from sqlalchemy import delete as sa_delete
    async with AsyncSessionLocal() as s:
        await s.execute(
            sa_delete(WatchList).where(WatchList.lot_id == lot_id, WatchList.user_id == user_id)
        )
        await s.commit()


async def get_watchers(lot_id: int) -> list:
    from db.database import WatchList
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(WatchList).where(WatchList.lot_id == lot_id)
        )
        return list(result.scalars().all())


# ── Rating ────────────────────────────────────────────────────

async def save_rating(lot_id: int, user_id: int, stars: int):
    from db.database import Rating
    async with AsyncSessionLocal() as s:
        existing = await s.execute(
            select(Rating).where(Rating.lot_id == lot_id, Rating.user_id == user_id)
        )
        rating = existing.scalar_one_or_none()
        if rating:
            rating.stars = stars
        else:
            s.add(Rating(lot_id=lot_id, user_id=user_id, stars=stars))
        await s.commit()


# ── Helpers ───────────────────────────────────────────────────

async def set_card_message_id(lot_id: int, message_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(card_message_id=message_id)
        )
        await s.commit()


async def update_card_message_id(lot_id: int, message_id: int):
    await set_card_message_id(lot_id, message_id)


async def save_client_photo_file_id(lot_id: int, file_id: str):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(client_photo_file_id=file_id)
        )
        await s.commit()


# ── Admins ────────────────────────────────────────────────────

async def get_all_admins() -> list[Admin]:
    """Все админы, суперадмины первыми."""
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Admin).order_by(Admin.is_super.desc(), Admin.added_at)
        )
        return list(result.scalars().all())


async def get_admin(user_id: int) -> Optional[Admin]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Admin).where(Admin.user_id == user_id)
        )
        return result.scalar_one_or_none()


async def is_admin_in_db(user_id: int) -> bool:
    return await get_admin(user_id) is not None


async def add_admin(
    user_id: int,
    username: Optional[str],
    first_name: Optional[str],
    added_by: int,
    is_super: bool = False,
) -> Admin:
    async with AsyncSessionLocal() as s:
        existing = await s.execute(select(Admin).where(Admin.user_id == user_id))
        if existing.scalar_one_or_none():
            # Обновить username/first_name если уже есть
            await s.execute(
                update(Admin)
                .where(Admin.user_id == user_id)
                .values(username=username, first_name=first_name)
            )
            await s.commit()
            return await get_admin(user_id)
        admin = Admin(
            user_id=user_id,
            username=username,
            first_name=first_name,
            is_super=is_super,
            added_by=added_by,
        )
        s.add(admin)
        await s.commit()
        await s.refresh(admin)
        return admin


async def remove_admin(user_id: int) -> bool:
    """Удалить обычного админа. Суперадмина удалить нельзя. Возвращает True если удалён."""
    from sqlalchemy import delete as sa_delete
    async with AsyncSessionLocal() as s:
        admin = await s.get(Admin, user_id)
        # get() ищет по PK, нам нужно по user_id
        result = await s.execute(select(Admin).where(Admin.user_id == user_id))
        admin = result.scalar_one_or_none()
        if not admin or admin.is_super:
            return False
        await s.execute(sa_delete(Admin).where(Admin.user_id == user_id))
        await s.commit()
        return True


async def seed_super_admins(admin_ids: list[int]) -> None:
    """При старте бота — добавить суперадминов из .env в БД если их там нет."""
    for uid in admin_ids:
        existing = await get_admin(uid)
        if not existing:
            await add_admin(
                user_id=uid,
                username=None,
                first_name=None,
                added_by=uid,
                is_super=True,
            )
        elif not existing.is_super:
            # Если был обычным — повысить до супер
            async with AsyncSessionLocal() as s:
                await s.execute(
                    update(Admin).where(Admin.user_id == uid).values(is_super=True)
                )
                await s.commit()
