import texts as T
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_IDS, ANTISNIPE_MINUTES, MIN_BID_STEP
from db.queries import (
    get_active_lots, get_stats, get_finished_lots, get_draft_lots,
)
from keyboards.inline import (
    kb_back_to_main, kb_main_menu, kb_finished_lots, kb_my_lots,
    kb_active_lots,
)
from utils.formatting import fmt_aed, fmt_time_left
from utils.guards import admin_only_callback, admin_only_message

router = Router()

BACK_TO_LOTS = InlineKeyboardBuilder().row(
    InlineKeyboardButton(text="← Назад", callback_data="menu:lots")
).as_markup()


def _back_lots() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))
    return b.as_markup()


# ── /start и главное меню ─────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    await state.clear()
    await message.answer(
        "👑 <b>Панель администратора</b>\n\nДобро пожаловать!",
        reply_markup=kb_main_menu(), parse_mode="HTML",
    )


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.clear()
    await callback.message.edit_text(
        "👑 <b>Панель администратора</b>\n\nДобро пожаловать!",
        reply_markup=kb_main_menu(), parse_mode="HTML",
    )
    await callback.answer()


# ── Мои лоты — подменю ────────────────────────────────────────

@router.callback_query(F.data == "menu:lots")
async def cb_my_lots(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    # Считаем количество в каждой категории
    active   = await get_active_lots()
    drafts   = await get_draft_lots()
    finished, fin_total = await get_finished_lots(limit=1)

    active_count    = len([l for l in active if l.status in ("active", "paused")])
    scheduled_count = len([l for l in active if l.status == "scheduled"])
    draft_count     = len(drafts)

    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text=f"🟢 Активные ({active_count})",          callback_data="lots:active"))
    b.row(InlineKeyboardButton(text=f"🕐 Запланированные ({scheduled_count})", callback_data="lots:scheduled"))
    b.row(InlineKeyboardButton(text=f"📝 Черновики ({draft_count})",           callback_data="lots:drafts"))
    b.row(InlineKeyboardButton(text=f"🏁 Завершённые ({fin_total})",           callback_data="lots:finished"))
    b.row(InlineKeyboardButton(text="← Главное меню",                         callback_data="menu:main"))

    await callback.message.edit_text(
        "🏷 <b>Мои лоты</b>\n\nВыберите категорию:",
        reply_markup=b.as_markup(), parse_mode="HTML",
    )
    await callback.answer()


# ── Активные ─────────────────────────────────────────────────

@router.callback_query(F.data.in_({"lots:active", "menu:active_lots"}))
async def cb_lots_active(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    all_lots = await get_active_lots()
    lots = [l for l in all_lots if l.status in ("active", "paused")]

    if not lots:
        b = InlineKeyboardBuilder()
        b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))
        await callback.message.edit_text(
            "📭 <b>Активных лотов нет.</b>",
            reply_markup=b.as_markup(), parse_mode="HTML",
        )
        await callback.answer()
        return

    b = InlineKeyboardBuilder()
    for lot in lots:
        status = "🟢" if lot.status == "active" else "⏸"
        prop = f"{lot.property_type} · " if lot.property_type else ""
        b.row(InlineKeyboardButton(
            text=f"{status} {lot.emoji} {lot.title[:26]} — {prop}{fmt_aed(lot.current_price)}",
            callback_data=f"lot:open:{lot.id}"
        ))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))

    lines = []
    for lot in lots:
        status = "🟢 LIVE" if lot.status == "active" else "⏸ Пауза"
        prop = f"{lot.property_type}  ·  " if lot.property_type else ""
        lines.append(f"{lot.emoji} <b>{lot.title}</b>\n   {status}  ·  {prop}{fmt_aed(lot.current_price)}")

    await callback.message.edit_text(
        "🟢 <b>Активные лоты</b>\n\n" + "\n\n".join(lines),
        reply_markup=b.as_markup(), parse_mode="HTML",
    )
    await callback.answer()


# ── Запланированные ───────────────────────────────────────────

@router.callback_query(F.data == "lots:scheduled")
async def cb_lots_scheduled(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    all_lots = await get_active_lots()
    lots = [l for l in all_lots if l.status == "scheduled"]

    if not lots:
        b = InlineKeyboardBuilder()
        b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))
        await callback.message.edit_text(
            "📭 <b>Запланированных лотов нет.</b>",
            reply_markup=b.as_markup(), parse_mode="HTML",
        )
        await callback.answer()
        return

    from datetime import timezone, timedelta
    b = InlineKeyboardBuilder()
    for lot in lots:
        b.row(InlineKeyboardButton(
            text=f"🕐 {lot.emoji} {lot.title[:28]}",
            callback_data=f"lot:open:{lot.id}"
        ))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))

    lines = []
    for lot in lots:
        msk = timezone(timedelta(hours=3))
        starts = lot.starts_at.astimezone(msk).strftime("%d.%m в %H:%M МСК") if lot.starts_at else "—"
        lines.append(f"{lot.emoji} <b>{lot.title}</b>\n   🕐 Старт: {starts}  ·  {fmt_aed(lot.start_price)}")

    await callback.message.edit_text(
        "🕐 <b>Запланированные лоты</b>\n\n" + "\n\n".join(lines),
        reply_markup=b.as_markup(), parse_mode="HTML",
    )
    await callback.answer()


# ── Черновики ─────────────────────────────────────────────────

@router.callback_query(F.data.in_({"lots:drafts", "menu:drafts"}))
async def cb_lots_drafts(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    drafts = await get_draft_lots()

    if not drafts:
        b = InlineKeyboardBuilder()
        b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))
        await callback.message.edit_text(
            "📭 <b>Черновиков нет.</b>\n\nСоздайте лот и сохраните как черновик.",
            reply_markup=b.as_markup(), parse_mode="HTML",
        )
        await callback.answer()
        return

    b = InlineKeyboardBuilder()
    for lot in drafts:
        b.row(InlineKeyboardButton(
            text=f"📝 {lot.emoji} {lot.title[:30]}",
            callback_data=f"draft:open:{lot.id}"
        ))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))

    lines = []
    for lot in drafts:
        prop = f"{lot.property_type}  ·  " if lot.property_type else ""
        lines.append(f"{lot.emoji} <b>{lot.title}</b>\n   {prop}{fmt_aed(lot.start_price)}")

    await callback.message.edit_text(
        "📝 <b>Черновики</b>\n\n" + "\n\n".join(lines),
        reply_markup=b.as_markup(), parse_mode="HTML",
    )
    await callback.answer()


# ── Черновик — карточка ───────────────────────────────────────

@router.callback_query(F.data.startswith("draft:open:"))
async def cb_draft_open(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from db.queries import get_lot
    from keyboards.inline import kb_draft_actions
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    prop = f"{lot.property_type}  ·  {lot.area_sqft} sqft\n" if lot.property_type else ""
    min_p = fmt_aed(lot.min_price) if lot.min_price else "—"
    text = (
        f"📝 <b>Черновик</b>\n\n"
        f"{lot.emoji} <b>{lot.title}</b>\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"{prop}"
        f"Старт: <b>{fmt_aed(lot.start_price)}</b>\n"
        f"Шаг: {fmt_aed(lot.bid_step)}  ·  {lot.price_drop_interval_minutes} мин\n"
        f"Мин. цена: {min_p}"
    )
    await callback.message.edit_text(text, reply_markup=kb_draft_actions(lot_id), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("draft:launch:"))
async def cb_draft_launch(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from db.queries import get_lot, launch_lot
    from keyboards.inline import kb_monitor
    from utils.scheduler import schedule_dutch_drop
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    lot = await launch_lot(lot_id, topic_id=0, ends_at=None)
    if lot.price_drop_interval_minutes:
        schedule_dutch_drop(lot_id, lot.price_drop_interval_minutes, callback.bot)
    area = f"{lot.area_sqft:,} sqft" if lot.area_sqft else "—"
    prop_line = f"Тип: {lot.property_type}  ·  {area}\n" if lot.property_type else ""
    await callback.message.edit_text(
        f"🚀 <b>Dutch-аукцион запущен!</b>\n\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"{lot.emoji} <b>{lot.title}</b>\n"
        f"{prop_line}"
        f"Старт: <b>{fmt_aed(lot.start_price)}</b>\n"
        f"Шаг: {fmt_aed(lot.bid_step)} / {lot.price_drop_interval_minutes} мин\n\n"
        f"<i>Лот опубликован в Mini App 📱</i>",
        reply_markup=kb_monitor(lot_id), parse_mode="HTML",
    )
    await callback.answer("🚀 Запущен")


@router.callback_query(F.data.startswith("draft:delete:"))
async def cb_draft_delete(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from keyboards.inline import kb_confirm_action
    lot_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "⚠️ <b>Удалить черновик?</b>\n\nЭто действие необратимо.",
        reply_markup=kb_confirm_action(
            yes_cb=f"draft:delete_confirm:{lot_id}",
            no_cb=f"draft:open:{lot_id}",
        ),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("draft:delete_confirm:"))
async def cb_draft_delete_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from db.queries import cancel_lot
    lot_id = int(callback.data.split(":")[2])
    await cancel_lot(lot_id)
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lots:drafts"))
    await callback.message.edit_text(
        "🗑 Черновик удалён.",
        reply_markup=b.as_markup(), parse_mode="HTML",
    )
    await callback.answer("Удалён")


# ── Завершённые ───────────────────────────────────────────────

PAGE_SIZE = 8


@router.callback_query(F.data.in_({"lots:finished", "menu:finished_lots"}))
async def cb_lots_finished(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    await _render_finished(callback, page=0)
    await callback.answer()


@router.callback_query(F.data.startswith("finished:page:"))
async def cb_finished_page(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    page = int(callback.data.split(":")[2])
    await _render_finished(callback, page=page)
    await callback.answer()


async def _render_finished(callback: CallbackQuery, page: int = 0):
    lots, total = await get_finished_lots(limit=PAGE_SIZE, offset=page * PAGE_SIZE)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    b = InlineKeyboardBuilder()

    if not lots:
        b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))
        await callback.message.edit_text(
            "📭 <b>Завершённых лотов нет.</b>",
            reply_markup=b.as_markup(), parse_mode="HTML",
        )
        return

    for lot in lots:
        price = fmt_aed(lot.final_price or lot.current_price)
        winner = f"🏆 @{lot.winner_username}" if lot.winner_username else (
            f"🏆 id{lot.winner_user_id}" if lot.winner_user_id and lot.winner_user_id != 0
            else "📭 нет ставок"
        )
        b.row(InlineKeyboardButton(
            text=f"{lot.emoji} {lot.title[:24]} — {price}",
            callback_data=f"finished:open:{lot.id}"
        ))

    # Пагинация
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"finished:page:{page-1}"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"finished:page:{page+1}"))
    if nav:
        b.row(*nav)
    b.row(InlineKeyboardButton(text="← Назад", callback_data="menu:lots"))

    lines = []
    for lot in lots:
        price = fmt_aed(lot.final_price or lot.current_price)
        winner = f"🏆 @{lot.winner_username}" if lot.winner_username else (
            f"🏆 id{lot.winner_user_id}" if lot.winner_user_id and lot.winner_user_id != 0
            else "📭 нет ставок"
        )
        lines.append(f"{lot.emoji} <b>{lot.title}</b>\n   {price}  ·  {winner}")

    text = (
        f"🏁 <b>Завершённые лоты</b>"
        f"  <i>({page * PAGE_SIZE + 1}–{min((page+1)*PAGE_SIZE, total)} из {total})</i>\n\n"
        + "\n\n".join(lines)
    )
    try:
        await callback.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="HTML")
    except Exception:
        pass


@router.callback_query(F.data.startswith("finished:open:"))
async def cb_finished_open(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from db.queries import get_lot, get_bid_count, get_unique_bidder_count
    from utils.formatting import report_text
    from keyboards.inline import kb_report_actions

    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    await callback.message.edit_text(
        report_text(lot, bid_count, user_count),
        reply_markup=kb_report_actions(lot_id, back_cb="lots:finished"),
        parse_mode="HTML",
    )
    await callback.answer()


# ── Статистика / настройки ────────────────────────────────────

@router.callback_query(F.data == "menu:stats")
async def cb_stats(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    stats = await get_stats()
    text = (
        f"📊 <b>Статистика аукционов</b>\n\n"
        f"🏷 Всего лотов: <b>{stats['total_lots']}</b>\n"
        f"✅ Завершено: <b>{stats['finished_lots']}</b>\n"
        f"💰 Оборот: <b>{fmt_aed(stats['total_turnover'])}</b>\n"
        f"👥 Участников: <b>{stats['unique_bidders']}</b>\n"
        f"📈 Ставок: <b>{stats['total_bids']}</b>"
    )
    await callback.message.edit_text(text, reply_markup=kb_back_to_main(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "menu:settings")
async def cb_settings(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    text = (
        f"⚙️ <b>Настройки</b>\n\n"
        f"• Антиснайпинг: <b>вкл</b> ({ANTISNIPE_MINUTES} мин)\n"
        f"• Мин. шаг ставки: <b>AED {MIN_BID_STEP:,}</b>\n\n"
        f"<i>Для изменения — отредактируйте .env и перезапустите бота.</i>"
    )
    await callback.message.edit_text(text, reply_markup=kb_back_to_main(), parse_mode="HTML")
    await callback.answer()
