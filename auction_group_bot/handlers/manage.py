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
from utils.formatting import fmt_price, fmt_time_left
from utils.guards import admin_only_callback
from utils.scheduler import cancel_auction_job, schedule_auction_finish

router = Router()


# ── Open manage panel ─────────────────────────────────────────

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
    leader = f"@{top_bid.username}" if (top_bid and top_bid.username) else (
        f"id{top_bid.user_id}" if top_bid else "нет ставок"
    )
    text = (
        f"⚙️ <b>Управление · {lot.emoji} {lot.title}</b>\n\n"
        f"Статус: {'⏸ на паузе' if lot.status == LotStatus.PAUSED else '🟢 активен'}\n"
        f"Цена: <b>{fmt_price(lot.current_price)}</b>  ·  {bid_count} ставок\n"
        f"Лидер: {leader}\n"
        f"Осталось: {fmt_time_left(lot.ends_at)}"
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

    # Calculate remaining seconds
    now = datetime.now(timezone.utc)
    seconds_left = max(0, int((lot.ends_at - now).total_seconds())) if lot.ends_at else 0
    await pause_lot(lot_id, seconds_left)
    cancel_auction_job(lot_id)

    # Notify group
    await _notify_group(callback, lot, "⏸ Аукцион временно приостановлен.")

    await callback.message.edit_text(
        f"⏸ <b>Аукцион приостановлен.</b>\n\n"
        f"Таймер остановлен. Ставки заморожены.\n"
        f"Осталось: {seconds_left // 3600}ч {(seconds_left % 3600) // 60}м",
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

    secs = lot.seconds_left or 3600
    new_ends_at = datetime.now(timezone.utc) + timedelta(seconds=secs)
    await resume_lot(lot_id, new_ends_at)

    bot = callback.bot
    from config import GROUP_BOT_TOKEN
    from aiogram import Bot as AiogramBot
    winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
    schedule_auction_finish(lot_id, new_ends_at, bot, winner_bot)

    await _notify_group(callback, lot, "▶️ Аукцион возобновлён.")

    await callback.message.edit_text(
        f"▶️ <b>Аукцион возобновлён!</b>\n\n"
        f"Таймер продолжается. Новое время окончания: {fmt_time_left(new_ends_at)}",
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
    lot_id, hours = int(parts[2]), int(parts[3])
    await _do_extend(callback, lot_id, hours)


async def _do_extend(callback: CallbackQuery, lot_id: int, hours: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    base = lot.ends_at or datetime.now(timezone.utc)
    new_ends_at = base + timedelta(hours=hours)
    await extend_lot(lot_id, new_ends_at)

    bot = callback.bot
    if lot.status == LotStatus.ACTIVE:
        from config import GROUP_BOT_TOKEN
        from aiogram import Bot as AiogramBot
        winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
        schedule_auction_finish(lot_id, new_ends_at, bot, winner_bot)

    await _notify_group(callback, lot, f"⏱ Время аукциона продлено на {hours}ч.")

    await callback.message.edit_text(
        f"✅ <b>Время продлено на {hours}ч.</b>\n\n"
        f"Новое время окончания: {fmt_time_left(new_ends_at)}\n"
        f"Участники уведомлены.",
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

    await _notify_group(callback, lot, f"🚫 Аукцион отменён администратором.")

    await callback.message.edit_text(
        f"🚫 Лот <code>{lot.lot_code}</code> <b>отменён</b>.\n\n"
        f"Топик #{lot.topic_id} закрыт. {bid_count} участников уведомлены.",
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
    price_line = f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>" if lot else ""
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

    lot = await get_lot(lot_id)
    if lot and lot.status == LotStatus.PAUSED:
        from db.queries import resume_lot
        await resume_lot(lot_id, datetime.now(timezone.utc))

    # Завершаем через админский бот (обновляет карточку группы),
    # победителю пишем через клиентский бот
    from config import GROUP_BOT_TOKEN
    from aiogram import Bot as AiogramBot
    group_bot = AiogramBot(token=GROUP_BOT_TOKEN)
    try:
        await _finish_auction_job(lot_id, callback.bot, winner_bot=group_bot)
    finally:
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
    lot_id, user_id = int(parts[2]), int(parts[3])
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
async def cb_ban_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts = callback.data.split(":")
    lot_id, user_id = int(parts[2]), int(parts[3])

    # Cancel their bids
    await cancel_user_bids(lot_id, user_id)

    # Recalculate current price
    top_bid = await get_top_bid(lot_id)
    lot = await get_lot(lot_id)
    if lot and top_bid:
        from sqlalchemy import update
        from db.database import AsyncSessionLocal, Lot
        async with AsyncSessionLocal() as s:
            await s.execute(
                update(Lot).where(Lot.id == lot_id).values(current_price=top_bid.amount)
            )
            await s.commit()

    # Add to banned list
    bidders = await get_bidders_for_lot(lot_id)
    username = None
    for b in bidders:
        if b["user_id"] == user_id:
            username = b["username"]
            break
    await ban_user(user_id, username, callback.from_user.id)

    # Try to kick from group
    try:
        from config import GROUP_ID
        await callback.bot.ban_chat_member(chat_id=GROUP_ID, user_id=user_id)
    except Exception:
        pass

    name = f"@{username}" if username else f"id{user_id}"
    await callback.message.edit_text(
        f"🚫 <b>{name} заблокирован.</b>\n\n"
        f"• Ставки аннулированы\n"
        f"• Участник исключён из группы\n"
        f"• Лидерство пересчитано",
        reply_markup=kb_manage(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("Заблокирован")


# ── Repost card with bid buttons ──────────────────────────────

@router.callback_query(F.data.startswith("mgmt:repost:"))
async def cb_repost_card(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    from config import GROUP_ID
    from utils.formatting import lot_card_text
    from db.queries import set_card_message_id
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton

    # Построить клавиатуру ставок
    step = lot.bid_step
    cur = lot.current_price
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=f"+{step:,} ₽",   callback_data=f"bid:{lot.id}:{cur + step}"),
        InlineKeyboardButton(text=f"+{step*2:,} ₽", callback_data=f"bid:{lot.id}:{cur + step * 2}"),
        InlineKeyboardButton(text=f"+{step*5:,} ₽", callback_data=f"bid:{lot.id}:{cur + step * 5}"),
    )
    if lot.blitz_price and cur < lot.blitz_price:
        builder.row(InlineKeyboardButton(
            text=f"🔥 БЛИЦ — {lot.blitz_price:,} ₽",
            callback_data=f"bid:{lot.id}:{lot.blitz_price}:blitz",
        ))
    builder.row(InlineKeyboardButton(
        text="🔔 Уведомить меня",
        callback_data=f"watch:on:{lot.id}",
    ))

    bid_count = await get_bid_count(lot_id)
    top_bid = await get_top_bid(lot_id)
    text = lot_card_text(lot, bid_count, top_bid)

    try:
        # Удалить старую карточку если есть
        if lot.card_message_id and GROUP_ID:
            try:
                await callback.bot.delete_message(
                    chat_id=GROUP_ID,
                    message_id=lot.card_message_id,
                )
            except Exception:
                pass

        # Опубликовать новую
        msg = await callback.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=lot.topic_id,
            text=text,
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )
        await set_card_message_id(lot_id, msg.message_id)
        await callback.answer("✅ Карточка переопубликована с кнопками!")
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {e}", show_alert=True)

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

