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
        pass  # "message not modified" — ignore


# Open monitor from lot list
@router.callback_query(F.data.startswith("lot:open:"))
async def cb_open_lot(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _render_monitor(callback, lot_id)
    await callback.answer()


# Refresh button
@router.callback_query(F.data.startswith("mon:refresh:"))
async def cb_refresh(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _render_monitor(callback, lot_id)
    await callback.answer("Обновлено ✓")

