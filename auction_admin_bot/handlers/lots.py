from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import (
    get_active_lots, get_bid_count, get_lot,
    get_top_bid, get_unique_bidder_count, is_watching,
)
from keyboards.inline import kb_lot_card_dm, kb_lots_list
from utils.formatting import lot_card_text, lot_detail_text, lot_list_text

router = Router()


# ── Lots list ─────────────────────────────────────────────────

@router.callback_query(F.data == "lots:list")
async def cb_lots_list(callback: CallbackQuery):
    lots = await get_active_lots()
    text = lot_list_text(lots)
    try:
        await callback.message.edit_text(
            text,
            reply_markup=kb_lots_list(lots),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer()


# ── Open lot card ─────────────────────────────────────────────

@router.callback_query(F.data.startswith("lot:view:"))
async def cb_view_lot(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    top_bid = await get_top_bid(lot_id)
    watching = await is_watching(lot_id, callback.from_user.id)

    user_is_leader = top_bid and top_bid.user_id == callback.from_user.id

    text = lot_card_text(lot, bid_count, top_bid, watching)
    kb = kb_lot_card_dm(lot, watching=watching)

    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer()


# ── Lot details ───────────────────────────────────────────────

@router.callback_query(F.data.startswith("lot:detail:"))
async def cb_lot_detail(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="← Назад к карточке", callback_data=f"lot:view:{lot_id}"))

    try:
        await callback.message.edit_text(
            lot_detail_text(lot, bid_count, user_count),
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer()

