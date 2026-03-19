import texts as T
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_lot, save_rating
from keyboards.inline import kb_back_to_start
from utils.formatting import fmt_price

router = Router()


# ── Rating ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("rate:"))
async def cb_rate(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id, stars = int(parts[1]), int(parts[2])

    await save_rating(lot_id, callback.from_user.id, stars)

    emoji = "🙌" if stars >= 4 else "🙏" if stars >= 3 else "😔"
    star_str = "⭐" * stars

    lots = await __import__("db.queries", fromlist=["get_active_lots"]).get_active_lots()

    await callback.message.edit_text(
        f"Спасибо за оценку! {star_str} {emoji}\n\n"
        f"До следующего аукциона! Следите за новыми лотами в группе.",
        reply_markup=kb_back_to_start(),
        parse_mode="HTML",
    )
    await callback.answer(f"Оценка {stars}/5 принята!")

