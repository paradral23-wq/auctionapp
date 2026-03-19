from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS
from db.queries import get_active_lots, get_stats
from keyboards.inline import kb_active_lots, kb_back_to_main, kb_main_menu
from utils.formatting import fmt_price
from utils.guards import admin_only_callback, admin_only_message

router = Router()


# ── /start ────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    await state.clear()
    await message.answer(
        "👑 <b>Панель администратора</b>\n\n"
        "Добро пожаловать! Управляйте аукционами группы через кнопки ниже.",
        reply_markup=kb_main_menu(),
        parse_mode="HTML",
    )


# ── menu:main callback (from any back-button) ────────────────

@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.clear()
    await callback.message.edit_text(
        "👑 <b>Панель администратора</b>\n\n"
        "Добро пожаловать! Управляйте аукционами группы через кнопки ниже.",
        reply_markup=kb_main_menu(),
        parse_mode="HTML",
    )
    await callback.answer()


# ── Stats ─────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:stats")
async def cb_stats(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    stats = await get_stats()
    turnover_fmt = fmt_price(stats["total_turnover"])
    text = (
        f"📊 <b>Статистика аукционов</b>\n\n"
        f"🏷 Всего лотов: <b>{stats['total_lots']}</b>\n"
        f"✅ Завершено: <b>{stats['finished_lots']}</b>\n"
        f"💰 Оборот: <b>{turnover_fmt}</b>\n"
        f"👥 Участников: <b>{stats['unique_bidders']}</b>\n"
        f"📈 Ставок: <b>{stats['total_bids']}</b>"
    )
    await callback.message.edit_text(text, reply_markup=kb_back_to_main(), parse_mode="HTML")
    await callback.answer()


# ── Settings ──────────────────────────────────────────────────

@router.callback_query(F.data == "menu:settings")
async def cb_settings(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from config import ANTISNIPE_MINUTES, MIN_BID_STEP
    text = (
        f"⚙️ <b>Настройки группы</b>\n\n"
        f"• Антиснайпинг: <b>вкл</b> ({ANTISNIPE_MINUTES} мин)\n"
        f"• Мин. шаг ставки: <b>₽ {MIN_BID_STEP:,}</b>\n"
        f"• Уведомления участникам: <b>вкл</b>\n"
        f"• Блокировка чата во время торгов: <b>вкл</b>\n"
        f"• Авто-закрытие топика: <b>вкл</b>\n\n"
        f"<i>Для изменения настроек — отредактируйте .env и перезапустите бота.</i>"
    )
    await callback.message.edit_text(text, reply_markup=kb_back_to_main(), parse_mode="HTML")
    await callback.answer()


# ── Active lots ───────────────────────────────────────────────

@router.callback_query(F.data == "menu:active_lots")
async def cb_active_lots(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lots = await get_active_lots()
    if not lots:
        await callback.message.edit_text(
            "📭 <b>Нет активных лотов.</b>\n\nСоздайте новый аукцион.",
            reply_markup=kb_main_menu(),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    lines = []
    for lot in lots:
        from utils.formatting import fmt_time_left
        status = "🟢 LIVE" if lot.status == "active" else "⏸ Пауза"
        lines.append(
            f"{lot.emoji} <b>{lot.title}</b>\n"
            f"   {status}  ·  {fmt_price(lot.current_price)}  ·  ⏱ {fmt_time_left(lot.ends_at)}"
        )
    text = "📋 <b>Активные лоты</b>\n\n" + "\n\n".join(lines)
    await callback.message.edit_text(
        text,
        reply_markup=kb_active_lots(lots),
        parse_mode="HTML",
    )
    await callback.answer()

