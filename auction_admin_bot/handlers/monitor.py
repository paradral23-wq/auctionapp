import texts as T
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_bid_count, get_lot, get_recent_bids, get_top_bid, get_unique_bidder_count
from keyboards.inline import kb_monitor
from utils.formatting import monitor_text
from utils.guards import admin_only_callback

router = Router()


async def _render_monitor(callback: CallbackQuery, lot_id: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    top_bid = await get_top_bid(lot_id)
    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)
    recent = await get_recent_bids(lot_id, 5)

    text = monitor_text(lot, bid_count, user_count, top_bid, recent)

    try:
        await callback.message.edit_text(
            text,
            reply_markup=kb_monitor(lot_id),
            parse_mode="HTML",
        )
    except Exception:
        pass  # message not modified


@router.callback_query(F.data.startswith("lot:open:"))
async def cb_open_lot(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _render_monitor(callback, lot_id)
    await callback.answer()


@router.callback_query(F.data.startswith("mon:refresh:"))
async def cb_refresh(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _render_monitor(callback, lot_id)
    await callback.answer("🔄 Обновлено")


@router.callback_query(F.data.startswith("mon:bids:"))
async def cb_bid_history(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from db.queries import get_lot_bids
    from utils.formatting import fmt_aed
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    from datetime import timezone, timedelta

    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bids = await get_lot_bids(lot_id)
    if not bids:
        await callback.answer("Ставок пока нет.", show_alert=True)
        return

    msk = timezone(timedelta(hours=3))
    lines = []
    for i, bid in enumerate(bids, 1):
        user = f"@{bid.username}" if bid.username else f"id{bid.user_id}"
        time_str = bid.created_at.astimezone(msk).strftime("%d.%m %H:%M")
        lines.append(f"{i}. <b>{fmt_aed(bid.amount)}</b> — {user} <i>{time_str}</i>")

    text = (
        f"📜 <b>История ставок</b>\n"
        f"{lot.emoji} {lot.title}\n\n"
        + "\n".join(lines)
    )

    builder = InlineKeyboardBuilder()
    if lot.status == "finished":
        builder.row(InlineKeyboardButton(text="← Назад", callback_data=f"finished:open:{lot_id}"))
    else:
        builder.row(InlineKeyboardButton(text="← Мониторинг", callback_data=f"lot:open:{lot_id}"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()
