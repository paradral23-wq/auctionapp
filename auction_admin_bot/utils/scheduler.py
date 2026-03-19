"""
auction_admin_bot/utils/scheduler.py

Поддерживает два режима:
  1. Классический аукцион — ends_at таймер, цена растёт
  2. Dutch-аукцион — цена снижается по интервалу, ends_at = None
"""
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from aiogram import Bot

logger = logging.getLogger(__name__)

_scheduler: Optional[AsyncIOScheduler] = None

# Кеш: lot_id → (last_price, last_leader_id)
_price_cache: dict[int, tuple[int, Optional[int]]] = {}


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    global _scheduler
    _scheduler = AsyncIOScheduler(timezone="UTC")
    return _scheduler


def get_scheduler() -> AsyncIOScheduler:
    return _scheduler


# ══════════════════════════════════════════════════════════════
#  Классический аукцион — финиш по таймеру
# ══════════════════════════════════════════════════════════════

async def _finish_auction_job(
    lot_id: int,
    bot: Bot,
    winner_bot: Bot = None,
    force: bool = False,
):
    from db.queries import (
        get_lot, finish_lot, cancel_lot, get_top_bid,
        get_bid_count, get_unique_bidder_count, get_bidders_for_lot,
    )
    from db.database import LotStatus
    from utils.formatting import winner_text, fmt_aed, auction_finished_text
    from keyboards.inline import kb_winner
    from config import GROUP_ID, ADMIN_IDS

    _winner_bot = winner_bot or bot

    lot = await get_lot(lot_id)
    if not lot:
        return
    # При force=True (досрочное завершение) разрешаем ACTIVE и PAUSED
    # При обычном завершении — только ACTIVE
    allowed = {LotStatus.ACTIVE, LotStatus.PAUSED} if force else {LotStatus.ACTIVE}
    if lot.status not in allowed:
        logger.info(f"_finish_auction_job: lot {lot_id} status={lot.status}, skipping")
        return

    # Если лот на паузе — нужно перевести в ACTIVE чтобы finish_lot отработал корректно
    if lot.status == LotStatus.PAUSED:
        from db.queries import resume_lot as _resume
        await _resume(lot_id, datetime.now(timezone.utc))
        lot = await get_lot(lot_id)

    if not force and lot.ends_at:
        now = datetime.now(timezone.utc)
        actual_ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=timezone.utc)
        if actual_ends > now + timedelta(seconds=2):
            logger.info(f"lot {lot_id} ends_at moved, rescheduling")
            schedule_auction_finish(lot_id, actual_ends, bot, winner_bot)
            return

    top_bid = await get_top_bid(lot_id)
    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)
    _price_cache.pop(lot_id, None)

    if top_bid:
        await finish_lot(lot_id, top_bid.user_id, top_bid.username or "", top_bid.amount)
        lot = await get_lot(lot_id)

        # Удалить карточку из топика
        if lot.topic_id and GROUP_ID and lot.card_message_id:
            try:
                await _winner_bot.delete_message(chat_id=GROUP_ID, message_id=lot.card_message_id)
            except Exception as e:
                logger.warning(f"Card delete failed: {e}")

        # Объявление в топике
        if lot.topic_id and GROUP_ID:
            try:
                finished_text = auction_finished_text(lot, top_bid.amount)
                if lot.client_photo_file_id:
                    await _winner_bot.send_photo(
                        chat_id=GROUP_ID, message_thread_id=lot.topic_id,
                        photo=lot.client_photo_file_id, caption=finished_text, parse_mode="HTML",
                    )
                else:
                    await _winner_bot.send_message(
                        chat_id=GROUP_ID, message_thread_id=lot.topic_id,
                        text=finished_text, parse_mode="HTML",
                    )
            except Exception as e:
                logger.warning(f"Winner post in topic failed: {e}")

        # Уведомление победителю
        winner_msg = (
            f"🏆 <b>ВЫ ПОБЕДИЛИ!</b>\n\n"
            f"{lot.emoji} <b>{lot.title}</b>\n"
            f"<code>{lot.lot_code}</code>\n\n"
            f"📋 {lot.description or '—'}\n\n"
            f"💰 Финальная цена: <b>{fmt_aed(top_bid.amount)}</b>\n\n"
            f"📦 Менеджер свяжется с вами в ближайшее время."
        )
        try:
            if lot.client_photo_file_id:
                await _winner_bot.send_photo(
                    chat_id=top_bid.user_id, photo=lot.client_photo_file_id,
                    caption=winner_msg, parse_mode="HTML",
                )
            else:
                await _winner_bot.send_message(
                    chat_id=top_bid.user_id, text=winner_msg, parse_mode="HTML",
                )
        except Exception as e:
            logger.warning(f"Winner notify failed: {e}")

        # Уведомление проигравшим
        bidders = await get_bidders_for_lot(lot_id)
        for b in bidders:
            if b["user_id"] == top_bid.user_id:
                continue
            try:
                await _winner_bot.send_message(
                    chat_id=b["user_id"],
                    text=(
                        f"🏁 <b>Аукцион завершён</b>\n\n"
                        f"{lot.emoji} {lot.title}\n"
                        f"<code>{lot.lot_code}</code>\n\n"
                        f"К сожалению, вы не победили.\n"
                        f"Финальная цена: <b>{fmt_aed(top_bid.amount)}</b>\n\n"
                        f"<i>Следите за новыми лотами!</i>"
                    ),
                    parse_mode="HTML",
                )
            except Exception:
                pass

        # Уведомление администраторам
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=winner_text(lot, bid_count, user_count),
                    parse_mode="HTML",
                    reply_markup=kb_winner(lot_id),
                )
            except Exception as e:
                logger.warning(f"Admin notify failed for {admin_id}: {e}")
    else:
        # Нет ставок — всё равно переводим в FINISHED (без победителя)
        # чтобы лот появился в разделе "Завершённые"
        await finish_lot(lot_id, winner_user_id=0, winner_username="", final_price=0)
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=(
                        f"📭 Аукцион <code>{lot.lot_code}</code> "
                        f"завершился без ставок.\n{lot.emoji} {lot.title}"
                    ),
                    parse_mode="HTML",
                )
            except Exception:
                pass


# ══════════════════════════════════════════════════════════════
#  Dutch-аукцион — снижение цены по таймеру
# ══════════════════════════════════════════════════════════════

def schedule_dutch_drop(lot_id: int, interval_minutes: int, bot: Bot, winner_bot: Bot = None) -> None:
    """Запланировать следующий тик снижения цены."""
    if _scheduler is None:
        return
    run_at = datetime.now(timezone.utc) + timedelta(minutes=interval_minutes)
    job_id = f"dutch_drop_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)
    _scheduler.add_job(
        _dutch_drop_tick,
        trigger=DateTrigger(run_date=run_at),
        id=job_id,
        args=[lot_id, interval_minutes, bot, winner_bot],
        misfire_grace_time=60,
    )
    logger.info(f"Dutch drop scheduled: lot={lot_id}, interval={interval_minutes}m, at={run_at}")


async def _dutch_drop_tick(lot_id: int, interval_minutes: int, bot: Bot, winner_bot: Bot = None) -> None:
    """
    Один тик Dutch-аукциона:
    1. Снизить цену на bid_step
    2. Если new_price < min_price → завершить без победителя
    3. Иначе → запланировать следующий тик и уведомить подписчиков
    """
    from db.queries import get_lot, cancel_lot, drop_lot_price, get_watchers
    from db.database import LotStatus
    from config import ADMIN_IDS

    lot = await get_lot(lot_id)
    if not lot:
        logger.warning(f"Dutch tick: lot {lot_id} not found")
        return
    if lot.status != LotStatus.ACTIVE:
        logger.info(f"Dutch tick: lot {lot_id} is {lot.status}, skip")
        return

    new_price = lot.current_price - lot.bid_step
    min_price = lot.min_price or 0

    if new_price < min_price:
        logger.info(f"Dutch: lot {lot_id} reached min_price ({min_price}), cancelling")
        await cancel_lot(lot_id)
        _price_cache.pop(lot_id, None)

        # Уведомить подписчиков
        notify = winner_bot or bot
        watchers = await get_watchers(lot_id)
        text = (
            f"🔕 <b>Аукцион не состоялся</b>\n\n"
            f"{lot.emoji} {lot.title}\n"
            f"Цена достигла минимума — покупатель не найден.\n\n"
            f"<i>Следите за новыми лотами в Mini App</i>"
        )
        for w in watchers:
            try:
                await notify.send_message(w.user_id, text, parse_mode="HTML")
            except Exception:
                pass

        # Уведомить администраторов
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=(
                        f"📭 Dutch-аукцион <code>{lot.lot_code}</code> не состоялся.\n"
                        f"{lot.emoji} {lot.title}\n"
                        f"Цена опустилась до минимума {fmt_aed_inline(min_price)}"
                    ),
                    parse_mode="HTML",
                )
            except Exception:
                pass
        return

    # Снизить цену в БД
    await drop_lot_price(lot_id, new_price)
    _price_cache[lot_id] = (new_price, _price_cache.get(lot_id, (0, None))[1])
    logger.info(f"Dutch: lot {lot_id} price dropped {lot.current_price} → {new_price}")

    # Уведомить Mini App бэкенд о снижении цены
    try:
        await _notify_miniapp(lot_id, new_price, interval_secs)
    except Exception as e:
        logger.warning(f"MiniApp notify error: {e}")

    # Уведомить подписчиков о снижении
    notify = winner_bot or bot
    watchers = await get_watchers(lot_id)
    drop_text = (
        f"📉 <b>Цена снизилась!</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"Новая цена: <b>{fmt_aed_inline(new_price)}</b>\n"
        f"Снижение: -{fmt_aed_inline(lot.bid_step)}\n\n"
        f"<i>Откройте Mini App чтобы купить →</i>"
    )
    for w in watchers:
        try:
            await notify.send_message(w.user_id, drop_text, parse_mode="HTML")
        except Exception:
            pass

    # Запланировать следующий тик
    schedule_dutch_drop(lot_id, interval_minutes, bot, winner_bot)


def fmt_aed_inline(amount: int) -> str:
    return f"AED {amount:,}".replace(",", " ")


# ══════════════════════════════════════════════════════════════
#  Планирование / отмена классического аукциона
# ══════════════════════════════════════════════════════════════

def schedule_auction_finish(lot_id: int, ends_at: datetime, bot: Bot, winner_bot: Bot = None):
    if _scheduler is None:
        return
    job_id = f"finish_lot_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)
    _scheduler.add_job(
        _finish_auction_job,
        trigger="date",
        run_date=ends_at,
        args=[lot_id, bot, winner_bot],
        id=job_id,
        replace_existing=True,
    )
    logger.info(f"Scheduled finish for lot {lot_id} at {ends_at}")


def schedule_lot_start(lot_id: int, starts_at: datetime, bot: Bot, winner_bot: Bot = None):
    if _scheduler is None:
        return
    now = datetime.now(timezone.utc)
    starts = starts_at if starts_at.tzinfo else starts_at.replace(tzinfo=timezone.utc)
    if starts <= now:
        logger.warning(f"schedule_lot_start: starts_at {starts} is in the past, skipping")
        return
    job_id = f"start_lot_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)
    _scheduler.add_job(
        _start_auction_job,
        trigger="date",
        run_date=starts_at,
        args=[lot_id, bot, winner_bot],
        id=job_id,
        replace_existing=True,
    )
    logger.info(f"Scheduled start for lot {lot_id} at {starts_at}")


async def _notify_miniapp(lot_id: int, current_price: int, interval_secs: int):
    """Отправляет вебхук в Mini App бэкенд для мгновенного обновления цены."""
    import aiohttp, os
    miniapp_url = os.getenv("MINIAPP_INTERNAL_URL", "http://api:8000")
    secret      = os.getenv("INTERNAL_SECRET", "auction_internal_secret")
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                f"{miniapp_url}/internal/price_drop",
                json={
                    "lot_id": lot_id,
                    "current_price": current_price,
                    "seconds_until_drop": interval_secs,
                },
                headers={"x-internal-secret": secret},
                timeout=aiohttp.ClientTimeout(total=3),
            )
        logger.info(f"MiniApp notified: lot={lot_id} price={current_price}")
    except Exception as e:
        logger.warning(f"MiniApp notify failed: {e}")


def cancel_auction_job(lot_id: int):
    if _scheduler is None:
        return
    for prefix in ("finish_lot_", "start_lot_", "dutch_drop_"):
        job_id = f"{prefix}{lot_id}"
        if _scheduler.get_job(job_id):
            _scheduler.remove_job(job_id)


async def _start_auction_job(lot_id: int, bot: Bot, winner_bot: Bot = None):
    from db.queries import get_lot, activate_scheduled_lot
    from db.database import LotStatus

    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.SCHEDULED:
        return

    if lot.price_drop_interval_minutes:
        # Dutch-аукцион: активировать без ends_at и запустить снижение цены
        await activate_scheduled_lot(lot_id, ends_at=None)
        lot = await get_lot(lot_id)
        schedule_dutch_drop(lot_id, lot.price_drop_interval_minutes, bot, winner_bot)
        logger.info(f"Lot {lot_id} activated as Dutch auction")
    else:
        # Классический аукцион
        ends_at = datetime.now(timezone.utc) + timedelta(hours=lot.duration_hours)
        await activate_scheduled_lot(lot_id, ends_at)
        lot = await get_lot(lot_id)
        schedule_auction_finish(lot_id, ends_at, bot, winner_bot)
        logger.info(f"Lot {lot_id} activated, ends at {ends_at}")

    # Обновить карточку в топике
    _client_bot = winner_bot or bot
    from config import GROUP_ID
    from db.queries import get_bid_count, get_top_bid
    from utils.formatting import lot_card_text
    from keyboards.inline import kb_lot_card
    if GROUP_ID and lot.topic_id and lot.card_message_id:
        try:
            bid_count = await get_bid_count(lot_id)
            top_bid = await get_top_bid(lot_id)
            text = lot_card_text(lot, bid_count, top_bid)
            kb = kb_lot_card(lot)
            if lot.client_photo_file_id:
                await _client_bot.edit_message_caption(
                    chat_id=GROUP_ID, message_id=lot.card_message_id,
                    caption=text, reply_markup=kb, parse_mode="HTML",
                )
            else:
                await _client_bot.edit_message_text(
                    chat_id=GROUP_ID, message_id=lot.card_message_id,
                    text=text, reply_markup=kb, parse_mode="HTML",
                )
        except Exception as e:
            logger.warning(f"Card update failed for lot {lot_id}: {e}")


# ══════════════════════════════════════════════════════════════
#  Restore on restart
# ══════════════════════════════════════════════════════════════

async def restore_scheduled_jobs(bot: Bot, winner_bot: Bot = None):
    """При рестарте восстанавливает все активные таймеры из БД."""
    from db.queries import get_active_lots, get_top_bid
    from db.database import LotStatus

    now = datetime.now(timezone.utc)
    lots = await get_active_lots()

    for lot in lots:
        if lot.status == LotStatus.SCHEDULED and lot.starts_at:
            starts = lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc)
            if starts > now:
                schedule_lot_start(lot.id, starts, bot, winner_bot)
            else:
                await _start_auction_job(lot.id, bot, winner_bot)

        elif lot.status == LotStatus.ACTIVE:
            if lot.ends_at:
                # Классический аукцион
                ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=timezone.utc)
                if ends > now:
                    schedule_auction_finish(lot.id, ends, bot, winner_bot)
                else:
                    await _finish_auction_job(lot.id, bot, winner_bot)
            elif lot.price_drop_interval_minutes:
                # Dutch-аукцион — возобновить снижение
                schedule_dutch_drop(lot.id, lot.price_drop_interval_minutes, bot, winner_bot)
                logger.info(f"Restored Dutch drop for lot {lot.id}")

        # Инициализация кеша
        try:
            top = await get_top_bid(lot.id)
            _price_cache[lot.id] = (lot.current_price, top.user_id if top else None)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════
#  Background tasks
# ══════════════════════════════════════════════════════════════

async def sync_finish_jobs(bot: Bot, winner_bot: Bot = None):
    """Каждые 15 сек синхронизирует ends_at с APScheduler."""
    from db.queries import get_active_lots
    from db.database import LotStatus

    while True:
        await asyncio.sleep(15)
        try:
            lots = await get_active_lots()
            for lot in lots:
                if lot.status != LotStatus.ACTIVE or not lot.ends_at:
                    continue
                ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=timezone.utc)
                job_id = f"finish_lot_{lot.id}"
                job = _scheduler.get_job(job_id) if _scheduler else None
                if job is None:
                    schedule_auction_finish(lot.id, ends, bot, winner_bot)
                elif abs((job.next_run_time - ends).total_seconds()) > 5:
                    schedule_auction_finish(lot.id, ends, bot, winner_bot)
        except Exception as e:
            logger.warning(f"sync_finish_jobs error: {e}")


async def sync_overbid_notifications(bot: Bot, winner_bot: Bot = None):
    """
    Каждые 5 сек обнаруживает ставки из Mini App и:
    - Для классического аукциона: уведомляет вытесненного лидера, обновляет карточку
    - Для Dutch-аукциона: обнаруживает покупку (лот → FINISHED), отменяет dutch_drop,
      уведомляет победителя и администраторов
    """
    from db.queries import get_active_lots, get_top_bid, get_bid_count, get_lot
    from db.database import LotStatus
    from utils.formatting import lot_card_text, fmt_aed, winner_text, auction_finished_text
    from keyboards.inline import kb_lot_card, kb_overbid, kb_winner
    from config import GROUP_ID, ADMIN_IDS

    notify_bot = winner_bot or bot
    logger.info("sync_overbid_notifications started")

    # Множество Dutch-лотов за которыми следим
    dutch_watched: set[int] = set()

    while True:
        await asyncio.sleep(5)
        try:
            lots = await get_active_lots()
            active_ids = {lot.id for lot in lots}

            # ── Классические: чистим кеш ──────────────────────
            for stale_id in list(_price_cache.keys()):
                if stale_id not in active_ids:
                    _price_cache.pop(stale_id, None)

            # ── Dutch: проверяем купленные ─────────────────────
            # get_active_lots() не вернёт FINISHED лоты — проверяем dutch_watched
            for lot_id in list(dutch_watched):
                if lot_id not in active_ids:
                    # Лот исчез из активных — проверим его статус
                    finished_lot = await get_lot(lot_id)
                    if finished_lot and finished_lot.status == LotStatus.FINISHED:
                        logger.info(f"Dutch purchase detected: lot {lot_id}")
                        # Отменить dutch_drop джоб
                        cancel_auction_job(lot_id)
                        _price_cache.pop(lot_id, None)
                        dutch_watched.discard(lot_id)

                        # Уведомить победителя
                        winner_msg = (
                            f"🏆 <b>ВЫ КУПИЛИ!</b>\n\n"
                            f"{finished_lot.emoji} <b>{finished_lot.title}</b>\n"
                            f"<code>{finished_lot.lot_code}</code>\n\n"
                            f"💰 Цена покупки: <b>{fmt_aed(finished_lot.final_price)}</b>\n\n"
                            f"📦 Менеджер свяжется с вами в ближайшее время."
                        )
                        try:
                            await notify_bot.send_message(
                                chat_id=finished_lot.winner_user_id,
                                text=winner_msg,
                                parse_mode="HTML",
                            )
                        except Exception as e:
                            logger.warning(f"Dutch winner notify failed: {e}")

                        # Уведомить администраторов
                        bid_count = await get_bid_count(lot_id)
                        from db.queries import get_unique_bidder_count
                        user_count = await get_unique_bidder_count(lot_id)
                        for admin_id in ADMIN_IDS:
                            try:
                                await bot.send_message(
                                    chat_id=admin_id,
                                    text=winner_text(finished_lot, bid_count, user_count),
                                    reply_markup=kb_winner(lot_id),
                                    parse_mode="HTML",
                                )
                            except Exception as e:
                                logger.warning(f"Admin notify failed: {e}")

                        # Объявление в топике
                        if GROUP_ID and finished_lot.topic_id:
                            try:
                                text = auction_finished_text(finished_lot, finished_lot.final_price)
                                await notify_bot.send_message(
                                    chat_id=GROUP_ID,
                                    message_thread_id=finished_lot.topic_id,
                                    text=text,
                                    parse_mode="HTML",
                                )
                            except Exception as e:
                                logger.debug(f"Dutch finish topic notify failed: {e}")
                    else:
                        dutch_watched.discard(lot_id)

            # ── Классические + Dutch активные ─────────────────
            for lot in lots:
                if lot.status != LotStatus.ACTIVE:
                    continue

                # Регистрируем Dutch-лоты для слежки
                if lot.price_drop_interval_minutes and not lot.ends_at:
                    dutch_watched.add(lot.id)
                    continue  # Dutch-лот не нуждается в overbid-уведомлениях

                # Классический аукцион — overbid notifications
                top_bid = await get_top_bid(lot.id)
                bid_count = await get_bid_count(lot.id)
                new_price = lot.current_price
                new_leader_id = top_bid.user_id if top_bid else None
                cached = _price_cache.get(lot.id)

                if cached is None:
                    _price_cache[lot.id] = (new_price, new_leader_id)
                    continue

                prev_price, prev_leader_id = cached
                if new_price <= prev_price:
                    continue

                logger.info(
                    f"Mini App bid: lot {lot.lot_code} "
                    f"{prev_price} → {new_price} "
                    f"(leader: {prev_leader_id} → {new_leader_id})"
                )

                # Обновить карточку в топике
                if GROUP_ID and lot.topic_id and lot.card_message_id:
                    try:
                        text = lot_card_text(lot, bid_count, top_bid)
                        kb = kb_lot_card(lot)
                        if lot.client_photo_file_id:
                            await notify_bot.edit_message_caption(
                                chat_id=GROUP_ID, message_id=lot.card_message_id,
                                caption=text, reply_markup=kb, parse_mode="HTML",
                            )
                        else:
                            await notify_bot.edit_message_text(
                                chat_id=GROUP_ID, message_id=lot.card_message_id,
                                text=text, reply_markup=kb, parse_mode="HTML",
                            )
                    except Exception as e:
                        logger.debug(f"Card update failed for lot {lot.id}: {e}")

                # Уведомить вытесненного лидера
                if prev_leader_id and prev_leader_id != new_leader_id:
                    try:
                        await notify_bot.send_message(
                            chat_id=prev_leader_id,
                            text=(
                                f"⚡ <b>Вас перебили!</b>\n\n"
                                f"{lot.emoji} {lot.title}\n"
                                f"<code>{lot.lot_code}</code>\n\n"
                                f"Новая цена: <b>{fmt_aed(new_price)}</b>\n\n"
                                f"<i>Откройте Mini App чтобы сделать ставку.</i>"
                            ),
                            reply_markup=kb_overbid(lot.id, new_price, lot.bid_step),
                            parse_mode="HTML",
                        )
                    except Exception as e:
                        logger.debug(f"Overbid notify failed for {prev_leader_id}: {e}")

                _price_cache[lot.id] = (new_price, new_leader_id)

        except Exception as e:
            logger.warning(f"sync_overbid_notifications error: {e}")


async def apply_antisnipe(lot_id: int, ends_at: datetime, bot: Bot) -> datetime:
    from config import ANTISNIPE_MINUTES
    from db.queries import extend_lot

    antisnipe_seconds = ANTISNIPE_MINUTES * 60
    now = datetime.now(timezone.utc)
    if ends_at.tzinfo is None:
        ends_at = ends_at.replace(tzinfo=timezone.utc)

    time_left = (ends_at - now).total_seconds()
    if time_left < antisnipe_seconds:
        new_ends_at = now + timedelta(seconds=antisnipe_seconds)
        await extend_lot(lot_id, new_ends_at)
        logger.info(f"Antisnipe triggered for lot {lot_id}, extended to {new_ends_at}")
        return new_ends_at
    return ends_at
