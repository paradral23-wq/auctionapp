import texts as T
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.database import Lot, LotStatus
from datetime import timezone, timedelta


# ── Главное меню ──────────────────────────────────────────────

def kb_main_menu() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="➕ Создать лот",   callback_data="menu:create"))
    b.row(InlineKeyboardButton(text="🏷 Мои лоты",      callback_data="menu:lots"))
    b.row(InlineKeyboardButton(text="👥 Администраторы", callback_data="menu:admins"))
    return b.as_markup()


def kb_my_lots() -> InlineKeyboardMarkup:
    """Подменю Мои лоты."""
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🟢 Активные",        callback_data="lots:active"))
    b.row(InlineKeyboardButton(text="🕐 Запланированные", callback_data="lots:scheduled"))
    b.row(InlineKeyboardButton(text="📝 Черновики",       callback_data="lots:drafts"))
    b.row(InlineKeyboardButton(text="🏁 Завершённые",     callback_data="lots:finished"))
    b.row(InlineKeyboardButton(text="← Главное меню",    callback_data="menu:main"))
    return b.as_markup()


def kb_back_to_main() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="← Главное меню", callback_data="menu:main"))
    return b.as_markup()


# ── Список активных лотов ─────────────────────────────────────

def kb_active_lots(lots) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for lot in lots:
        status = "🟢" if lot.status == LotStatus.ACTIVE else "⏸" if lot.status == LotStatus.PAUSED else "🕐"
        prop = f"{lot.property_type} · " if lot.property_type else ""
        b.row(InlineKeyboardButton(
            text=f"{status} {lot.emoji} {lot.title[:25]} — {prop}AED {lot.current_price:,}",
            callback_data=f"lot:open:{lot.id}"
        ))
    b.row(InlineKeyboardButton(text="← Главное меню", callback_data="menu:main"))
    return b.as_markup()


# ── Список завершённых лотов (с пагинацией) ───────────────────

def kb_finished_lots(lots, page: int = 0, total_pages: int = 1) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for lot in lots:
        price = lot.final_price or lot.current_price
        b.row(InlineKeyboardButton(
            text=f"{lot.emoji} {lot.title[:26]} — AED {price:,}",
            callback_data=f"finished:open:{lot.id}"
        ))
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"finished:page:{page-1}"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"finished:page:{page+1}"))
    if nav:
        b.row(*nav)
    b.row(InlineKeyboardButton(text="← Главное меню", callback_data="menu:main"))
    return b.as_markup()


# ── Мониторинг ────────────────────────────────────────────────

def kb_monitor(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🔄 Обновить",       callback_data=f"mon:refresh:{lot_id}"))
    b.row(InlineKeyboardButton(text="⚙️ Управление",     callback_data=f"mon:manage:{lot_id}"))
    b.row(InlineKeyboardButton(text="✏️ Редактировать",  callback_data=f"lot:edit:{lot_id}"))
    b.row(InlineKeyboardButton(text="📜 История ставок", callback_data=f"mon:bids:{lot_id}"))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lots:active"))
    return b.as_markup()


# ── Управление лотом ──────────────────────────────────────────

def kb_manage(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="⏸ Поставить паузу",   callback_data=f"mgmt:pause:{lot_id}"))
    b.row(InlineKeyboardButton(text="⏹ Завершить досрочно", callback_data=f"mgmt:early_finish:{lot_id}"))
    b.row(InlineKeyboardButton(text="🗑 Отменить лот",       callback_data=f"mgmt:cancel:{lot_id}"))
    b.row(InlineKeyboardButton(text="← Мониторинг",         callback_data=f"lot:open:{lot_id}"))
    return b.as_markup()


def kb_manage_paused(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="▶️ Возобновить",        callback_data=f"mgmt:resume:{lot_id}"))
    b.row(InlineKeyboardButton(text="⏹ Завершить досрочно", callback_data=f"mgmt:early_finish:{lot_id}"))
    b.row(InlineKeyboardButton(text="🗑 Отменить лот",       callback_data=f"mgmt:cancel:{lot_id}"))
    b.row(InlineKeyboardButton(text="← Мониторинг",          callback_data=f"lot:open:{lot_id}"))
    return b.as_markup()


def kb_extend_pick(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for h in [1, 2, 6, 12, 24]:
        b.add(InlineKeyboardButton(text=f"+{h}ч", callback_data=f"mgmt:extend:{lot_id}:{h}"))
    b.adjust(5)
    b.row(InlineKeyboardButton(text="← Назад", callback_data=f"mgmt:menu:{lot_id}"))
    return b.as_markup()


def kb_confirm_action(yes_cb: str, no_cb: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="✅ Подтвердить", callback_data=yes_cb))
    b.row(InlineKeyboardButton(text="← Нет, назад",  callback_data=no_cb))
    return b.as_markup()


# ── Бан ──────────────────────────────────────────────────────

def kb_ban_pick(lot_id: int, bidders: list[dict]) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for bd in bidders[:8]:
        name = bd["username"] or str(bd["user_id"])
        b.row(InlineKeyboardButton(
            text=f"🚫 @{name} — AED {bd['amount']:,}",
            callback_data=f"ban:user:{lot_id}:{bd['user_id']}"
        ))
    b.row(InlineKeyboardButton(text="← Отмена", callback_data=f"mgmt:menu:{lot_id}"))
    return b.as_markup()


def kb_ban_confirm(lot_id: int, user_id: int) -> InlineKeyboardMarkup:
    return kb_confirm_action(
        yes_cb=f"ban:confirm:{lot_id}:{user_id}",
        no_cb=f"mgmt:ban_pick:{lot_id}",
    )


# ── Победитель / отчёт ────────────────────────────────────────

def kb_winner(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="📊 Отчёт по лоту",  callback_data=f"win:report:{lot_id}"))
    b.row(InlineKeyboardButton(text="📜 Все ставки",     callback_data=f"mon:bids:{lot_id}"))
    b.row(InlineKeyboardButton(text="➕ Новый лот",      callback_data="menu:create"))
    b.row(InlineKeyboardButton(text="← Главное меню",    callback_data="menu:main"))
    return b.as_markup()


def kb_draft_actions(lot_id: int) -> InlineKeyboardMarkup:
    """Кнопки для черновика."""
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🚀 Запустить аукцион", callback_data=f"draft:launch:{lot_id}"))
    b.row(InlineKeyboardButton(text="✏️ Редактировать",     callback_data=f"lot:edit:{lot_id}"))
    b.row(InlineKeyboardButton(text="🗑 Удалить черновик",  callback_data=f"draft:delete:{lot_id}"))
    b.row(InlineKeyboardButton(text="← Назад",          callback_data="menu:drafts"))
    return b.as_markup()


def kb_report_actions(lot_id: int, back_cb: str = "menu:finished_lots") -> InlineKeyboardMarkup:
    """Кнопки под отчётом по завершённому лоту — экспорт + навигация."""
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="📥 Excel", callback_data=f"export:xlsx:{lot_id}"),
        InlineKeyboardButton(text="📥 CSV",   callback_data=f"export:csv:{lot_id}"),
    )
    b.row(InlineKeyboardButton(text="📜 Все ставки", callback_data=f"mon:bids:{lot_id}"))
    b.row(InlineKeyboardButton(text="← Назад",       callback_data=back_cb))
    return b.as_markup()


# ── Карточка лота (в топике / личке) ─────────────────────────

def kb_lot_card(lot: Lot) -> InlineKeyboardMarkup:
    """Кнопки карточки лота для участников (в топике группы)."""
    if lot.status == LotStatus.SCHEDULED and lot.starts_at:
        b = InlineKeyboardBuilder()
        starts = lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc)
        msk = starts.astimezone(timezone(timedelta(hours=3)))
        b.row(InlineKeyboardButton(
            text=f"🕐 Начнётся {msk.strftime('%d.%m в %H:%M')} МСК",
            callback_data="noop",
        ))
        return b.as_markup()

    b = InlineKeyboardBuilder()
    step = lot.bid_step
    cur = lot.current_price
    b.row(
        InlineKeyboardButton(text=f"+{step:,}", callback_data=f"bid:{lot.id}:{cur + step}"),
        InlineKeyboardButton(text=f"+{step*2:,}", callback_data=f"bid:{lot.id}:{cur + step * 2}"),
        InlineKeyboardButton(text=f"+{step*5:,}", callback_data=f"bid:{lot.id}:{cur + step * 5}"),
    )
    b.row(InlineKeyboardButton(text="✏️ Своя сумма", callback_data=f"bid:custom:{lot.id}"))
    return b.as_markup()


def kb_lot_card_dm(lot: Lot, watching: bool = False) -> InlineKeyboardMarkup:
    """Кнопки карточки лота для лички."""
    b = InlineKeyboardBuilder()
    step = lot.bid_step
    cur = lot.current_price
    if lot.status == LotStatus.ACTIVE:
        b.row(
            InlineKeyboardButton(text=f"+{step:,} AED", callback_data=f"bid:{lot.id}:{cur + step}"),
            InlineKeyboardButton(text=f"+{step*2:,} AED", callback_data=f"bid:{lot.id}:{cur + step * 2}"),
        )
        b.row(InlineKeyboardButton(text="✏️ Своя сумма", callback_data=f"bid:custom:{lot.id}"))
    watch_text = "🔕 Отписаться" if watching else "🔔 Следить"
    b.row(
        InlineKeyboardButton(text=watch_text, callback_data=f"watch:toggle:{lot.id}"),
        InlineKeyboardButton(text="📋 Подробнее", callback_data=f"lot:detail:{lot.id}"),
    )
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lots:active"))
    return b.as_markup()


def kb_lots_list(lots: list) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for lot in lots:
        status = "🟢" if lot.status == LotStatus.ACTIVE else "🕐"
        prop = f"{lot.property_type} · " if lot.property_type else ""
        b.row(InlineKeyboardButton(
            text=f"{status} {lot.emoji} {lot.title[:26]} — {prop}AED {lot.current_price:,}",
            callback_data=f"lot:view:{lot.id}",
        ))
    if not lots:
        b.row(InlineKeyboardButton(text="Нет активных лотов", callback_data="noop"))
    return b.as_markup()


def kb_overbid(lot_id: int, new_price: int, step: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(
            text=f"⚡ +{step:,} → {new_price + step:,} AED",
            callback_data=f"bid:{lot_id}:{new_price + step}",
        ),
        InlineKeyboardButton(
            text=f"💪 +{step*3:,} → {new_price + step*3:,} AED",
            callback_data=f"bid:{lot_id}:{new_price + step * 3}",
        ),
    )
    b.row(InlineKeyboardButton(text="✏️ Своя сумма", callback_data=f"bid:custom:{lot_id}"))
    return b.as_markup()


def kb_after_bid(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="✏️ Повысить ставку", callback_data=f"bid:custom:{lot_id}"))
    return b.as_markup()


def kb_cancel_custom_bid(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"bid:custom:cancel:{lot_id}"))
    return b.as_markup()


def kb_confirm_bid(lot_id: int, amount: int, is_blitz: bool = False) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    confirm_text = f"✅ Да, ставлю {amount:,} AED"
    b.row(
        InlineKeyboardButton(text=confirm_text, callback_data=f"bid:confirm:{lot_id}:{amount}"),
        InlineKeyboardButton(text="❌ Отмена",   callback_data=f"bid:cancel_confirm:{lot_id}"),
    )
    return b.as_markup()


def kb_rating(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for i in range(1, 6):
        b.add(InlineKeyboardButton(text="⭐" * i, callback_data=f"rate:{lot_id}:{i}"))
    b.adjust(5)
    return b.as_markup()


def kb_back_to_start() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="👋 Следите за новыми лотами", callback_data="noop"))
    return b.as_markup()
