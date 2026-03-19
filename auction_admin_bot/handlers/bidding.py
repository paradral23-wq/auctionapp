import asyncio
import logging
from datetime import timezone
from typing import Dict, Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db.queries import (
    add_to_watchlist, get_bid_count, get_lot, get_top_bid,
    place_bid, remove_from_watchlist, get_watchers,
)
from db.database import LotStatus
from keyboards.inline import (
    kb_after_bid, kb_overbid, kb_lot_card,
    kb_rating, kb_back_to_start, kb_cancel_custom_bid,
    kb_confirm_bid, kb_winner,
)
from utils.formatting import (
    bid_accepted_text, fmt_price, lot_card_text, overbid_notify_text,
)
from utils.scheduler import apply_antisnipe
from utils.states import CustomBidFSM

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer("⏳ Аукцион ещё не начался", show_alert=False)

# Хранилище pending-подтверждений: {user_id: {lot_id, amount, is_blitz, task}}
_pending: Dict[int, Dict[str, Any]] = {}

CONFIRM_TIMEOUT = 30  # секунд до автоотмены


# ─────────────────────────────────────────────────────────────
# ПОРЯДОК ВАЖЕН: специфичные фильтры — ВЫШЕ общих
# ─────────────────────────────────────────────────────────────


# ── Custom bid — шаг 1: кнопка «✏️ Своя сумма» ───────────────

@router.callback_query(F.data.regexp(r"^bid:custom:\d+$"))
async def cb_custom_bid_start(callback: CallbackQuery, state: FSMContext):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    if lot.status != LotStatus.ACTIVE:
        await callback.answer("Аукцион не активен.", show_alert=True)
        return

    await state.set_state(CustomBidFSM.waiting_for_amount)
    await state.update_data(lot_id=lot_id)

    min_bid = lot.current_price + lot.bid_step
    blitz_line = f"\n🔥 Блиц-цена: <b>{fmt_price(lot.blitz_price)}</b>" if lot.blitz_price else ""

    try:
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=(
                f"✏️ <b>Введите сумму ставки</b>\n\n"
                f"{lot.emoji} {lot.title}\n"
                f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
                f"Минимальная ставка: <b>{fmt_price(min_bid)}</b>"
                f"{blitz_line}\n\n"
                f"Напишите сумму числом (например: <code>{min_bid}</code>)"
            ),
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        await callback.answer("✏️ Напишите сумму в личку боту")
    except Exception as e:
        logger.debug(f"Custom bid DM failed: {e}")
        await state.clear()
        await callback.answer(
            "❌ Сначала напишите боту /start в личку — иначе он не сможет написать вам.",
            show_alert=True,
        )


# ── Custom bid — отмена ───────────────────────────────────────

@router.callback_query(F.data.regexp(r"^bid:custom:cancel:\d+$"))
async def cb_custom_bid_cancel(callback: CallbackQuery, state: FSMContext):
    lot_id = int(callback.data.split(":")[3])
    await state.clear()
    await callback.message.edit_text(
        "❌ Ввод ставки отменён.",
        reply_markup=kb_after_bid(lot_id),
    )
    await callback.answer()


# ── Custom bid — шаг 2: получить сумму ───────────────────────

@router.message(CustomBidFSM.waiting_for_amount)
async def msg_custom_bid_amount(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return

    data = await state.get_data()
    lot_id = data.get("lot_id")
    if not lot_id:
        await state.clear()
        return

    raw = (message.text or "").strip()
    raw = raw.replace(" ", "").replace(",", "").replace(".", "").replace("\u202f", "").replace("\xa0", "")

    if not raw.isdigit():
        lot = await get_lot(lot_id)
        min_bid = (lot.current_price + lot.bid_step) if lot else 0
        await message.answer(
            f"❌ Введите число без букв.\nНапример: <code>{min_bid}</code>",
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        return

    amount = int(raw)
    lot = await get_lot(lot_id)

    if not lot:
        await state.clear()
        await message.answer("Лот не найден.")
        return

    min_bid = lot.current_price + lot.bid_step
    if amount < min_bid:
        await message.answer(
            f"❌ Ставка слишком низкая.\n"
            f"Минимум: <b>{fmt_price(min_bid)}</b>\n\n"
            f"Введите другую сумму:",
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        return

    await state.clear()

    # Отправить подтверждение в личку
    is_blitz = bool(lot.blitz_price and amount >= lot.blitz_price)
    await _send_confirm_dm(message.bot, message.from_user.id, lot, amount, is_blitz)


# ── Ставка по кнопке из топика — отправить подтверждение в личку

@router.callback_query(F.data.regexp(r"^bid:\d+:\d+(:\w+)?$"))
async def cb_bid_request(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id = int(parts[1])
    amount = int(parts[2])
    is_blitz = len(parts) > 3 and parts[3] == "blitz"
    from_topic = callback.message.chat.type in ("group", "supergroup")

    # Из личного чата (кнопки перебития) — тоже через подтверждение
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    if lot.status != LotStatus.ACTIVE:
        await callback.answer("Аукцион завершён.", show_alert=True)
        return

    user_id = callback.from_user.id

    # Отменить предыдущий pending если был
    old = _pending.pop(user_id, None)
    if old and old.get("task"):
        old["task"].cancel()

    try:
        await _send_confirm_dm(callback.bot, user_id, lot, amount, is_blitz)
        await callback.answer("📩 Подтвердите ставку в личке бота", show_alert=False)
    except Exception as e:
        logger.debug(f"Confirm DM failed: {e}")
        await callback.answer(
            "❌ Сначала напишите боту /start в личку — иначе он не сможет написать вам.",
            show_alert=True,
        )


# ── Подтверждение ставки (из лички) ──────────────────────────

@router.callback_query(F.data.regexp(r"^bid:confirm:\d+:\d+$"))
async def cb_bid_confirmed(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id = int(parts[2])
    amount = int(parts[3])
    user_id = callback.from_user.id

    pending = _pending.pop(user_id, None)
    if pending and pending.get("task"):
        pending["task"].cancel()

    is_blitz = pending.get("is_blitz", False) if pending else False

    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        await callback.message.edit_text(
            "❌ Аукцион уже завершён, ставка не принята.",
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await _execute_bid(
        bot=callback.bot,
        lot_id=lot_id,
        user_id=user_id,
        username=callback.from_user.username,
        amount=amount,
        reply_fn=callback.message.edit_text,
        from_topic=False,
        callback=callback,
        is_blitz=is_blitz,
    )


# ── Отмена подтверждения (из лички) ──────────────────────────

@router.callback_query(F.data.regexp(r"^bid:cancel_confirm:\d+$"))
async def cb_bid_cancel_confirm(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    user_id = callback.from_user.id

    pending = _pending.pop(user_id, None)
    if pending and pending.get("task"):
        pending["task"].cancel()

    lot = await get_lot(lot_id)
    lot_name = f"{lot.emoji} {lot.title}" if lot else "лот"
    await callback.message.edit_text(
        f"❌ Ставка отменена.\n\n{lot_name}",
        parse_mode="HTML",
    )
    await callback.answer("Ставка отменена.")


# ── Watch ─────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("watch:on:"))
async def cb_watch_on(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    await add_to_watchlist(lot_id, callback.from_user.id, callback.from_user.username)
    await callback.answer("🔔 Пришлём результат в личку!", show_alert=True)


# ── Helpers ───────────────────────────────────────────────────

async def _send_confirm_dm(bot, user_id: int, lot, amount: int, is_blitz: bool):
    """Отправить сообщение с подтверждением в личку и запустить таймер."""
    blitz_note = "\n\n🔥 <b>Это блиц-цена — аукцион завершится мгновенно!</b>" if is_blitz else ""
    confirm_text = (
        f"⚡ <b>Подтвердите ставку</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"Ваша ставка: <b>{fmt_price(amount)}</b>"
        f"{blitz_note}\n\n"
        f"⏱ У вас {CONFIRM_TIMEOUT} секунд"
    )
    msg = await bot.send_message(
        chat_id=user_id,
        text=confirm_text,
        reply_markup=kb_confirm_bid(lot.id, amount, is_blitz),
        parse_mode="HTML",
    )

    # Сохранить pending
    old = _pending.pop(user_id, None)
    if old and old.get("task"):
        old["task"].cancel()

    task = asyncio.create_task(
        _auto_expire_confirm(bot, user_id, lot.id, msg.chat.id, msg.message_id)
    )
    _pending[user_id] = {
        "lot_id": lot.id,
        "amount": amount,
        "is_blitz": is_blitz,
        "task": task,
    }


async def _auto_expire_confirm(bot, user_id: int, lot_id: int, chat_id: int, message_id: int):
    """Через CONFIRM_TIMEOUT сек убрать кнопки и сообщить об истечении."""
    await asyncio.sleep(CONFIRM_TIMEOUT)
    if user_id in _pending and _pending[user_id].get("lot_id") == lot_id:
        _pending.pop(user_id, None)
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="⌛ Время на подтверждение истекло. Сделайте ставку заново.",
                parse_mode="HTML",
            )
        except Exception:
            pass


async def _execute_bid(
    bot, lot_id: int, user_id: int, username,
    amount: int, reply_fn, from_topic: bool,
    callback=None, is_blitz: bool = False,
):
    prev_top = await get_top_bid(lot_id)
    prev_leader_id = prev_top.user_id if (prev_top and prev_top.user_id != user_id) else None

    success, reason, bid = await place_bid(lot_id, user_id, username, amount)
    if not success:
        if callback:
            await callback.answer(f"❌ {reason}", show_alert=True)
        await reply_fn(f"❌ {reason}", parse_mode="HTML")
        return

    lot = await get_lot(lot_id)
    bid_count = await get_bid_count(lot_id)

    # Антиснайпинг
    antisnipe_triggered = False
    if lot.ends_at and not is_blitz:
        ends_at = lot.ends_at
        if ends_at.tzinfo is None:
            ends_at = ends_at.replace(tzinfo=timezone.utc)
        new_ends_at = await apply_antisnipe(lot_id, ends_at, bot)
        if new_ends_at != ends_at:
            antisnipe_triggered = True
            lot = await get_lot(lot_id)

    if not is_blitz and lot.blitz_price and amount >= lot.blitz_price:
        is_blitz = True

    # ── БЛИЦ ──────────────────────────────────────────────────
    if is_blitz and lot.blitz_price and amount >= lot.blitz_price:
        from db.queries import finish_lot
        from utils.scheduler import cancel_auction_job
        from utils.formatting import winner_text

        await finish_lot(lot_id, user_id, username or "", amount)
        lot = await get_lot(lot_id)
        cancel_auction_job(lot_id)
        winner_name = f"@{username}" if username else f"id{user_id}"

        await _update_group_card(bot, lot, bid_count, finished=True)

        await reply_fn(
            bid_accepted_text(lot, amount, is_blitz=True),
            reply_markup=kb_rating(lot_id),
            parse_mode="HTML",
        )
        if callback:
            await callback.answer("🔥 Блиц! Вы победили!")

        try:
            await bot.send_message(
                chat_id=user_id,
                text=winner_text(lot, amount),
                reply_markup=kb_winner(lot_id),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.debug(f"Winner DM failed: {e}")

        await _notify_watchers_finish(bot, lot, amount, user_id)
        return

    # ── ОБЫЧНАЯ СТАВКА ────────────────────────────────────────
    antisnipe_note = "\n\n⏱ <i>Антиснайпинг: таймер продлён на 2 мин</i>" if antisnipe_triggered else ""

    await _update_group_card(bot, lot, bid_count)

    await reply_fn(
        bid_accepted_text(lot, amount) + antisnipe_note,
        reply_markup=kb_after_bid(lot_id),
        parse_mode="HTML",
    )
    if callback:
        await callback.answer("✅ Ставка принята!")

    await add_to_watchlist(lot_id, user_id, username)

    if prev_leader_id and prev_leader_id != user_id:
        try:
            await bot.send_message(
                chat_id=prev_leader_id,
                text=overbid_notify_text(lot, amount),
                reply_markup=kb_overbid(lot_id, amount, lot.bid_step),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.debug(f"Overbid notify failed: {e}")


async def _update_group_card(bot, lot, bid_count: int, finished: bool = False):
    from config import GROUP_ID
    from db.queries import get_top_bid
    from utils.formatting import lot_card_text, auction_finished_text

    if not GROUP_ID or not lot.topic_id or not lot.card_message_id:
        return

    top_bid = await get_top_bid(lot.id)

    if finished and top_bid:
        text = auction_finished_text(lot, top_bid.amount)
        reply_markup = None
    else:
        text = lot_card_text(lot, bid_count, top_bid)
        reply_markup = kb_lot_card(lot)

    try:
        if lot.client_photo_file_id:
            await bot.edit_message_caption(
                chat_id=GROUP_ID,
                message_id=lot.card_message_id,
                caption=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
        else:
            await bot.edit_message_text(
                chat_id=GROUP_ID,
                message_id=lot.card_message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
    except Exception as e:
        logger.debug(f"Card update failed: {e}")


async def _notify_watchers_finish(bot, lot, final_price: int, winner_id: int):
    watchers = await get_watchers(lot.id)
    for w in watchers:
        if w.user_id == winner_id:
            continue
        try:
            await bot.send_message(
                chat_id=w.user_id,
                text=(
                    f"🏁 <b>Аукцион завершён</b>\n\n"
                    f"{lot.emoji} {lot.title}\n"
                    f"Финальная цена: {fmt_price(final_price)}"
                ),
                reply_markup=kb_back_to_start(),
                parse_mode="HTML",
            )
        except Exception:
            pass

