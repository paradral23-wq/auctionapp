from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_bid_count, get_lot, get_unique_bidder_count
from keyboards.inline import kb_back_to_main, kb_winner
from utils.formatting import report_text
from utils.guards import admin_only_callback

router = Router()


@router.callback_query(F.data.startswith("win:report:"))
async def cb_report(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    await callback.message.edit_text(
        report_text(lot, bid_count, user_count),
        reply_markup=kb_back_to_main(),
        parse_mode="HTML",
    )
    await callback.answer()

