from datetime import datetime, timedelta, timezone

from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.database import LotStatus
from db.queries import (
    ban_user, cancel_lot, cancel_user_bids, extend_lot,
    get_bid_count, get_bidders_for_lot, get_lot, get_top_bid,
    get_unique_bidder_count, pause_lot, resume_lot,
)
from keyboards.inline import (
    kb_ban_confirm, kb_ban_pick, kb_back_to_main, kb_confirm_action,
    kb_extend_pick, kb_manage, kb_manage_paused, kb_monitor,
)
from utils.formatting import fmt_aed, fmt_time_left
from utils.guards import admin_only_callback
from utils.scheduler import cancel_auction_job, schedule_auction_finish

router = Router()


@router.callback_query(F.data.startswith("mon:manage:"))
async def cb_open_manage(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _show_manage(callback, lot_id)
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:menu:"))
async def cb_manage_menu(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _show_manage(callback, lot_id)
    await callback.answer()


async def _show_manage(callback: CallbackQuery, lot_id: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    bid_count = await get_bid_count(lot_id)
    top_bid = await get_top_bid(lot_id)
    leader = (
        f"@{top_bid.username}" if (top_bid and top_bid.username)
        else f"id{top_bid.user_id}" if top_bid
        else "нет ставок"
    )
    prop = f"{lot.property_type}  ·  " if lot.property_type else ""
    is_dutch = bool(lot.price_drop_interval_minutes and not lot.ends_at)
    status_str = "⏸ на паузе" if lot.status == LotStatus.PAUSED else "🟢 активен"
    time_line = (
        f"Интервал: {lot.price_drop_interval_minutes} мин" if is_dutch
        else f"Осталось: {fmt_time_left(lot.ends_at)}"
    )
    text = (
        f"⚙️ <b>Управление · {lot.emoji} {lot.title}</b>\n\n"
        f"Статус: {status_str}\n"
        f"Цена: <b>{fmt_aed(lot.current_price)}</b>  ·  {prop}{bid_count} ставок\n"
        f"Лидер: {leader}\n"
        f"{time_line}"
    )
    kb = kb_manage_paused(lot_id) if lot.status == LotStatus.PAUSED else kb_manage(lot_id)
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass


# ── Pause ─────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:pause:"))
async def cb_pause(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        await callback.answer("Нельзя поставить на паузу.", show_alert=True)
        return

    now = datetime.now(timezone.utc)
    # Dutch-аукцион: ends_at = None, seconds_left не нужен
    is_dutch = bool(lot.price_drop_interval_minutes and not lot.ends_at)
    seconds_left = 0 if is_dutch else (
        max(0, int((lot.ends_at - now).total_seconds())) if lot.ends_at else 0
    )
    await pause_lot(lot_id, seconds_left)
    cancel_auction_job(lot_id)  # отменяет dutch_drop и finish

    await _notify_group(callback, lot, "⏸ Аукцион временно приостановлен.")

    if is_dutch:
        status_line = f"Цена зафиксирована: <b>{fmt_aed(lot.current_price)}</b>"
    else:
        status_line = f"Осталось: {seconds_left // 3600}ч {(seconds_left % 3600) // 60}м"

    await callback.message.edit_text(
        f"⏸ <b>Аукцион приостановлен.</b>\n\n"
        f"Снижение цены остановлено. Покупка заморожена.\n"
        f"{status_line}",
        reply_markup=kb_manage_paused(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("⏸ Приостановлен")


# ── Resume ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:resume:"))
async def cb_resume(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.PAUSED:
        await callback.answer("Лот не на паузе.", show_alert=True)
        return

    from config import GROUP_BOT_TOKEN
    from aiogram import Bot as AiogramBot

    if lot.price_drop_interval_minutes:
        # Dutch-аукцион — возобновить снижение
        await resume_lot(lot_id, lot.ends_at)  # ends_at остаётся None
        from utils.scheduler import schedule_dutch_drop
        winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
        schedule_dutch_drop(lot_id, lot.price_drop_interval_minutes, callback.bot, winner_bot)
        time_info = f"Снижение продолжается каждые {lot.price_drop_interval_minutes} мин."
    else:
        secs = lot.seconds_left or 3600
        new_ends_at = datetime.now(timezone.utc) + timedelta(seconds=secs)
        await resume_lot(lot_id, new_ends_at)
        winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
        schedule_auction_finish(lot_id, new_ends_at, callback.bot, winner_bot)
        time_info = f"Новое время окончания: {fmt_time_left(new_ends_at)}"

    await _notify_group(callback, lot, "▶️ Аукцион возобновлён.")
    await callback.message.edit_text(
        f"▶️ <b>Аукцион возобновлён!</b>\n\n{time_info}",
        reply_markup=kb_monitor(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("▶️ Возобновлён")


# ── Extend ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:extend_pick:"))
async def cb_extend_pick(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "⏱ <b>Выберите, на сколько продлить:</b>",
        reply_markup=kb_extend_pick(lot_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:extend:"))
async def cb_extend_hours(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts = callback.data.split(":")
    lot_id = int(parts[2])
    hours = int(parts[3])
    await _do_extend(callback, lot_id, hours)


async def _do_extend(callback: CallbackQuery, lot_id: int, hours: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    base = lot.ends_at or datetime.now(timezone.utc)
    new_ends_at = base + timedelta(hours=hours)
    await extend_lot(lot_id, new_ends_at)

    if lot.status == LotStatus.ACTIVE:
        from config import GROUP_BOT_TOKEN
        from aiogram import Bot as AiogramBot
        winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
        schedule_auction_finish(lot_id, new_ends_at, callback.bot, winner_bot)

    await _notify_group(callback, lot, f"⏱ Время аукциона продлено на {hours}ч.")
    await callback.message.edit_text(
        f"✅ <b>Время продлено на {hours}ч.</b>\n\n"
        f"Новое время окончания: {fmt_time_left(new_ends_at)}",
        reply_markup=kb_manage(lot_id),
        parse_mode="HTML",
    )
    await callback.answer(f"+{hours}ч добавлено")


# ── Cancel lot ────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:cancel:"))
async def cb_cancel_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "⚠️ <b>Подтвердите отмену лота</b>\n\n"
        "Все ставки будут аннулированы. Участники получат уведомление.",
        reply_markup=kb_confirm_action(
            yes_cb=f"mgmt:cancel_confirm:{lot_id}",
            no_cb=f"mgmt:menu:{lot_id}",
        ),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:cancel_confirm:"))
async def cb_cancel_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    await cancel_lot(lot_id)
    cancel_auction_job(lot_id)
    bid_count = await get_bid_count(lot_id)
    await _notify_group(callback, lot, "🚫 Аукцион отменён администратором.")

    await callback.message.edit_text(
        f"🚫 Лот <code>{lot.lot_code}</code> <b>отменён</b>.\n\n"
        f"{bid_count} участников уведомлены.",
        reply_markup=kb_back_to_main(),
        parse_mode="HTML",
    )
    await callback.answer("Лот отменён")


# ── Early finish ──────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:early_finish:"))
async def cb_early_finish_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    top_bid = await get_top_bid(lot_id)
    price_line = f"Текущая цена: <b>{fmt_aed(lot.current_price)}</b>" if lot else ""
    leader = ""
    if top_bid:
        name = f"@{top_bid.username}" if top_bid.username else f"id{top_bid.user_id}"
        leader = f"\nЛидер: <b>{name}</b>"

    await callback.message.edit_text(
        f"⚠️ <b>Завершить аукцион досрочно?</b>\n\n"
        f"Победителем становится текущий лидер.\n"
        f"{price_line}{leader}",
        reply_markup=kb_confirm_action(
            yes_cb=f"mgmt:early_confirm:{lot_id}",
            no_cb=f"mgmt:menu:{lot_id}",
        ),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:early_confirm:"))
async def cb_early_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])

    from utils.scheduler import _finish_auction_job
    cancel_auction_job(lot_id)

    # Не трогаем статус вручную — _finish_auction_job сам обработает PAUSED при force=True
    from config import GROUP_BOT_TOKEN
    from aiogram import Bot as AiogramBot
    group_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
    try:
        await _finish_auction_job(lot_id, callback.bot, winner_bot=group_bot, force=True)
    finally:
        if group_bot:
            await group_bot.session.close()

    lot = await get_lot(lot_id)
    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    from utils.formatting import winner_text
    from keyboards.inline import kb_winner
    await callback.message.edit_text(
        winner_text(lot, bid_count, user_count),
        reply_markup=kb_winner(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("Завершено")


# ── Ban user ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:ban_pick:"))
async def cb_ban_pick(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    bidders = await get_bidders_for_lot(lot_id)
    if not bidders:
        await callback.answer("Нет участников для блокировки.", show_alert=True)
        return
    await callback.message.edit_text(
        "👤 <b>Выберите участника для блокировки:</b>",
        reply_markup=kb_ban_pick(lot_id, bidders),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ban:user:"))
async def cb_ban_user_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts = callback.data.split(":")
    lot_id = int(parts[2])
    user_id = int(parts[3])
    bidders = await get_bidders_for_lot(lot_id)
    target = next((b for b in bidders if b["user_id"] == user_id), None)
    name = f"@{target['username']}" if (target and target["username"]) else f"id{user_id}"
    await callback.message.edit_text(
        f"⚠️ <b>Подтвердите блокировку</b>\n\n"
        f"Пользователь: {name}\n"
        f"Все ставки по этому лоту будут аннулированы.",
        reply_markup=kb_ban_confirm(lot_id, user_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ban:confirm:"))
async def cb_ban_confirm_handler(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts = callback.data.split(":")
    lot_id = int(parts[2])
    user_id = int(parts[3])

    await cancel_user_bids(lot_id, user_id)

    top_bid = await get_top_bid(lot_id)
    lot = await get_lot(lot_id)
    if lot and top_bid:
        from sqlalchemy import update as sa_update
        from db.database import AsyncSessionLocal, Lot as LotModel
        async with AsyncSessionLocal() as s:
            await s.execute(
                sa_update(LotModel).where(LotModel.id == lot_id).values(current_price=top_bid.amount)
            )
            await s.commit()
    elif lot and not top_bid:
        from sqlalchemy import update as sa_update
        from db.database import AsyncSessionLocal, Lot as LotModel
        async with AsyncSessionLocal() as s:
            await s.execute(
                sa_update(LotModel).where(LotModel.id == lot_id).values(current_price=lot.start_price)
            )
            await s.commit()

    bidders = await get_bidders_for_lot(lot_id)
    username = next((b["username"] for b in bidders if b["user_id"] == user_id), None)
    await ban_user(user_id, username, callback.from_user.id)

    try:
        from config import GROUP_ID
        await callback.bot.ban_chat_member(chat_id=GROUP_ID, user_id=user_id)
    except Exception:
        pass

    lot = await get_lot(lot_id)
    if top_bid and lot:
        try:
            from config import GROUP_BOT_TOKEN
            from aiogram import Bot as AiogramBot
            notify_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else callback.bot
            await notify_bot.send_message(
                chat_id=top_bid.user_id,
                text=(
                    f"🏆 <b>Вы снова лидируете!</b>\n\n"
                    f"{lot.emoji} {lot.title}\n"
                    f"<code>{lot.lot_code}</code>\n\n"
                    f"Участник был заблокирован, его ставки аннулированы.\n"
                    f"Текущая цена: <b>{fmt_aed(top_bid.amount)}</b>"
                ),
                parse_mode="HTML",
            )
            if GROUP_BOT_TOKEN:
                await notify_bot.session.close()
        except Exception:
            pass

    name = f"@{username}" if username else f"id{user_id}"
    await callback.message.edit_text(
        f"🚫 <b>{name} заблокирован.</b>\n\n"
        f"• Ставки аннулированы\n"
        f"• Участник исключён из группы\n"
        f"• Лидерство пересчитано\n"
        f"• Новый лидер уведомлён",
        reply_markup=kb_manage(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("Заблокирован")


async def _notify_group(callback: CallbackQuery, lot, text: str):
    from config import GROUP_ID
    if not GROUP_ID or not lot.topic_id:
        return
    try:
        await callback.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=lot.topic_id,
            text=text,
        )
    except Exception:
        pass
