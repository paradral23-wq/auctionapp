from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_lot, save_rating
from keyboards.inline import kb_rating, kb_back_to_start
from utils.formatting import fmt_price

router = Router()


# ── Winner confirms purchase ───────────────────────────────────

@router.callback_query(F.data.startswith("win:confirm:"))
async def cb_win_confirm(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    username = callback.from_user.username
    name = f"@{username}" if username else f"id{callback.from_user.id}"

    # Notify group that winner confirmed
    from config import GROUP_ID
    if GROUP_ID and lot.topic_id:
        try:
            await callback.bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=lot.topic_id,
                text=f"✅ Победитель {name} подтвердил покупку.",
                parse_mode="HTML",
            )
        except Exception:
            pass

    await callback.message.edit_text(
        f"✅ <b>Покупка подтверждена!</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"Итоговая цена: <b>{fmt_price(lot.final_price or 0)}</b>\n\n"
        f"👤 <b>Менеджер уже уведомлён</b> и свяжется с вами в ближайшее время.\n\n"
        f"Пожалуйста, оцените ваш опыт участия в аукционе:",
        reply_markup=kb_rating(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("✅ Подтверждено!")


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

