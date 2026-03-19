import texts as T
import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

logger = logging.getLogger(__name__)

_scheduler: AsyncIOScheduler = None


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    global _scheduler
    _scheduler = AsyncIOScheduler(timezone="UTC")
    return _scheduler


def get_scheduler() -> AsyncIOScheduler:
    return _scheduler


# ── Finish auction ─────────────────────────────────────────────

async def _finish_auction_job(lot_id: int, bot: Bot, winner_bot: Bot = None):
    """
    bot        — бот для обновления карточки группы (может быть админский или клиентский)
    winner_bot — бот для отправки уведомления победителю (всегда клиентский)
                 если не передан — используется bot
    """
    from db.queries import (
        get_lot, get_top_bid, get_bid_count, get_unique_bidder_count,
        finish_lot, cancel_lot_no_bids, get_watchers,
    )
    from db.database import LotStatus
    from utils.formatting import winner_text, auction_finished_text, fmt_price
    from keyboards.inline import kb_back_to_start
    from config import GROUP_ID

    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        return

    top_bid = await get_top_bid(lot_id)
    bid_count = await get_bid_count(lot_id)

    if top_bid:
        await finish_lot(lot_id, top_bid.user_id, top_bid.username or "", top_bid.amount)
        lot = await get_lot(lot_id)

        # Delete card from topic — announcement below will replace it
        if GROUP_ID and lot.topic_id and lot.card_message_id:
            logger.info(f"Deleting card message_id={lot.card_message_id} in chat={GROUP_ID}")
            try:
                await bot.delete_message(
                    chat_id=GROUP_ID,
                    message_id=lot.card_message_id,
                )
                logger.info(f"Card deleted for lot {lot_id}")
            except Exception as e:
                logger.warning(f"Card delete failed: {e}")
        else:
            logger.warning(f"Skip card delete: GROUP_ID={GROUP_ID}, topic_id={lot.topic_id}, card_message_id={lot.card_message_id}")

        # Announce in topic
        if GROUP_ID and lot.topic_id:
            try:
                await bot.send_message(
                    chat_id=GROUP_ID,
                    message_thread_id=lot.topic_id,
                    text=auction_finished_text(lot, top_bid.amount),
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.warning(f"Topic announce failed: {e}")

        # Notify winner in DM
        _winner_bot = winner_bot or bot
        try:
            if lot.client_photo_file_id:
                await _winner_bot.send_photo(
                    chat_id=top_bid.user_id,
                    photo=lot.client_photo_file_id,
                    caption=winner_text(lot, top_bid.amount),
                    parse_mode="HTML",
                )
            else:
                await _winner_bot.send_message(
                    chat_id=top_bid.user_id,
                    text=winner_text(lot, top_bid.amount),
                    parse_mode="HTML",
                )
        except Exception as e:
            logger.warning(f"Winner DM failed for user {top_bid.user_id}: {e}")
            if GROUP_ID and lot.topic_id:
                try:
                    await bot.send_message(
                        chat_id=GROUP_ID,
                        message_thread_id=lot.topic_id,
                        text=(
                            T.WINNER_FALLBACK_TOPIC
                        ),
                        parse_mode="HTML",
                    )
                except Exception:
                    pass

        # Notify watchers (non-winners)
        watchers = await get_watchers(lot_id)
        for w in watchers:
            if w.user_id == top_bid.user_id:
                continue
            try:
                await bot.send_message(
                    chat_id=w.user_id,
                    text=(
                        f"🏁 <b>Аукцион завершён</b>\n\n"
                        f"{lot.emoji} {lot.title}\n"
                        f"Финальная цена: {fmt_price(top_bid.amount)}"
                    ),
                    reply_markup=kb_back_to_start(),
                    parse_mode="HTML",
                )
            except Exception:
                pass

    else:
        # No bids
        await cancel_lot_no_bids(lot_id)
        if GROUP_ID and lot.topic_id:
            try:
                await bot.send_message(
                    chat_id=GROUP_ID,
                    message_thread_id=lot.topic_id,
                    text=T.AUCTION_NO_BIDS.format(emoji=lot.emoji, title=lot.title),
                    parse_mode="HTML",
                )
            except Exception:
                pass


def schedule_auction_finish(lot_id: int, ends_at: datetime, bot: Bot):
    if _scheduler is None:
        return
    job_id = f"finish_lot_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)
    _scheduler.add_job(
        _finish_auction_job,
        trigger="date",
        run_date=ends_at,
        args=[lot_id, bot],
        id=job_id,
        replace_existing=True,
    )


def cancel_auction_job(lot_id: int):
    if _scheduler is None:
        return
    job_id = f"finish_lot_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)


async def apply_antisnipe(lot_id: int, ends_at: datetime, bot: Bot) -> datetime:
    """Если ставка сделана менее чем за ANTISNIPE_SECONDS до конца — продлить."""
    from config import ANTISNIPE_SECONDS
    from db.queries import extend_lot_timer

    now = datetime.now(timezone.utc)
    if ends_at.tzinfo is None:
        ends_at = ends_at.replace(tzinfo=timezone.utc)

    time_left = (ends_at - now).total_seconds()
    if time_left < ANTISNIPE_SECONDS:
        # Всегда устанавливаем ровно ANTISNIPE_SECONDS от текущего момента,
        # а не прибавляем к ends_at — чтобы не накапливалось при нескольких ставках подряд
        new_ends_at = now + timedelta(seconds=ANTISNIPE_SECONDS)
        await extend_lot_timer(lot_id, new_ends_at)
        # Финиш перепланирует admin bot через sync_finish_jobs
        logger.info(f"Antisnipe triggered for lot {lot_id}, extended to {new_ends_at}")
        return new_ends_at
    return ends_at


async def restore_scheduled_jobs(bot: Bot):
    from db.queries import get_active_lots
    from db.database import LotStatus

    now = datetime.now(timezone.utc)
    lots = await get_active_lots()
    for lot in lots:
        if lot.status == LotStatus.ACTIVE and lot.ends_at:
            ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=timezone.utc)
            if ends > now:
                schedule_auction_finish(lot.id, ends, bot)
                logger.info(f"Restored timer for lot {lot.id}")
            else:
                await _finish_auction_job(lot.id, bot)

