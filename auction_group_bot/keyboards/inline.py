import texts as T
from datetime import timezone, timedelta
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.database import Lot, LotStatus
from config import HELP_URL


# ── Карточка лота в топике ────────────────────────────────────

def kb_lot_card(lot: Lot) -> InlineKeyboardMarkup:
    # Для запланированного лота — только кнопка с временем начала
    if lot.status == LotStatus.SCHEDULED and lot.starts_at:
        builder = InlineKeyboardBuilder()
        starts = lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc)
        msk = starts.astimezone(timezone(timedelta(hours=3)))
        builder.row(InlineKeyboardButton(
            text=f"🕐 Аукцион начнётся в {msk.strftime('%d.%m в %H:%M')} МСК",
            callback_data="noop",
        ))
        return builder.as_markup()

    builder = InlineKeyboardBuilder()
    step = lot.bid_step
    cur  = lot.current_price

    builder.row(
        InlineKeyboardButton(text=f"+{step:,} ₽",   callback_data=f"bid:{lot.id}:{cur + step}"),
        InlineKeyboardButton(text=f"+{step*2:,} ₽", callback_data=f"bid:{lot.id}:{cur + step * 2}"),
        InlineKeyboardButton(text=f"+{step*5:,} ₽", callback_data=f"bid:{lot.id}:{cur + step * 5}"),
    )
    if lot.blitz_price and cur < lot.blitz_price:
        builder.row(InlineKeyboardButton(
            text=f"🔥 БЛИЦ — {lot.blitz_price:,} ₽",
            callback_data=f"bid:{lot.id}:{lot.blitz_price}:blitz",
        ))
    builder.row(
        InlineKeyboardButton(text=T.KB_CUSTOM_BID, callback_data=f"bid:custom:{lot.id}"),
        InlineKeyboardButton(text=T.KB_HELP,      url=HELP_URL),
    )
    return builder.as_markup()


# ── Подтверждение ставки (в личке) ───────────────────────────

def kb_confirm_bid(lot_id: int, amount: int, is_blitz: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    confirm_text = f"{'🔥 ' if is_blitz else '✅ '}Да, ставлю {amount:,} ₽"
    builder.row(
        InlineKeyboardButton(text=confirm_text, callback_data=f"bid:confirm:{lot_id}:{amount}"),
        InlineKeyboardButton(text=T.KB_CANCEL_ACTION,   callback_data=f"bid:cancel_confirm:{lot_id}"),
    )
    return builder.as_markup()


# ── После принятой ставки (в личке) ──────────────────────────

def kb_after_bid(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="✏️ Повысить ставку",
        callback_data=f"bid:custom:{lot_id}",
    ))
    return builder.as_markup()


# ── Уведомление о перебитии (в личке) ────────────────────────

def kb_overbid(lot_id: int, new_price: int, step: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"⚡ +{step:,} ₽ → {new_price + step:,} ₽",
            callback_data=f"bid:{lot_id}:{new_price + step}",
        ),
        InlineKeyboardButton(
            text=f"💪 +{step*3:,} ₽ → {new_price + step*3:,} ₽",
            callback_data=f"bid:{lot_id}:{new_price + step * 3}",
        ),
    )
    builder.row(InlineKeyboardButton(
        text=T.KB_CUSTOM_BID,
        callback_data=f"bid:custom:{lot_id}",
    ))
    return builder.as_markup()


# ── Отмена ввода произвольной ставки ─────────────────────────

def kb_cancel_custom_bid(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=T.KB_CANCEL_ACTION, callback_data=f"bid:custom:cancel:{lot_id}"))
    return builder.as_markup()


# ── Победитель ────────────────────────────────────────────────

def kb_winner(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    return builder.as_markup()


# ── Рейтинг ───────────────────────────────────────────────────

def kb_rating(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.add(InlineKeyboardButton(text="⭐" * i, callback_data=f"rate:{lot_id}:{i}"))
    builder.adjust(5)
    return builder.as_markup()


# ── Заглушка (в уведомлениях после завершения) ───────────────

def kb_back_to_start() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="👋 Следите за новыми лотами в группе", callback_data="noop"))
    return builder.as_markup()



# ══ Добавлено для совместимости с handlers ════════════════════

def kb_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🏷 Активные лоты",  callback_data="lots:list"))
    builder.row(InlineKeyboardButton(text="📋 Мои участия",    callback_data="lots:mine"))
    return builder.as_markup()


def kb_active_lots(lots: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lot in lots:
        builder.row(InlineKeyboardButton(
            text=f"{lot.emoji} {lot.title[:30]} — ₽{lot.current_price:,}",
            callback_data=f"lot:view:{lot.id}",
        ))
    if not lots:
        builder.row(InlineKeyboardButton(text="Нет активных лотов", callback_data="noop"))
    return builder.as_markup()


def kb_lots_list(lots: list) -> InlineKeyboardMarkup:
    return kb_active_lots(lots)


def kb_lot_card_dm(lot: Lot, watching: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    step = lot.bid_step
    cur  = lot.current_price
    from db.database import LotStatus as _LS
    if lot.status == _LS.ACTIVE:
        builder.row(
            InlineKeyboardButton(text=f"+{step:,} ₽",   callback_data=f"bid:{lot.id}:{cur + step}"),
            InlineKeyboardButton(text=f"+{step*2:,} ₽", callback_data=f"bid:{lot.id}:{cur + step * 2}"),
        )
        if lot.blitz_price and cur < lot.blitz_price:
            builder.row(InlineKeyboardButton(
                text=f"🔥 БЛИЦ — {lot.blitz_price:,} ₽",
                callback_data=f"bid:{lot.id}:{lot.blitz_price}:blitz",
            ))
        builder.row(InlineKeyboardButton(text="✏️ Своя сумма", callback_data=f"bid:custom:{lot.id}"))
    watch_text = "🔕 Отписаться" if watching else "🔔 Следить"
    builder.row(
        InlineKeyboardButton(text=watch_text,    callback_data=f"watch:toggle:{lot.id}"),
        InlineKeyboardButton(text="📋 Детали",   callback_data=f"lot:detail:{lot.id}"),
    )
    builder.row(InlineKeyboardButton(text="← Все лоты", callback_data="lots:list"))
    return builder.as_markup()


def kb_monitor(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔄 Обновить",        callback_data=f"monitor:refresh:{lot_id}"))
    builder.row(InlineKeyboardButton(text="⚙️ Управление",      callback_data=f"lot:manage:{lot_id}"))
    builder.row(InlineKeyboardButton(text="← Главное меню",     callback_data="menu:main"))
    return builder.as_markup()


def kb_back_to_main() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="← Главное меню", callback_data="menu:main"))
    return builder.as_markup()


def kb_manage(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⏸ Пауза",            callback_data=f"mgmt:pause:{lot_id}"))
    builder.row(InlineKeyboardButton(text="⏱ Продлить",         callback_data=f"mgmt:extend:{lot_id}"))
    builder.row(InlineKeyboardButton(text="⏹ Завершить",        callback_data=f"mgmt:early_finish:{lot_id}"))
    builder.row(InlineKeyboardButton(text="🚫 Заблокировать",    callback_data=f"mgmt:ban_pick:{lot_id}"))
    builder.row(InlineKeyboardButton(text="← Мониторинг",       callback_data=f"lot:open:{lot_id}"))
    return builder.as_markup()


def kb_manage_paused(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="▶️ Возобновить",      callback_data=f"mgmt:resume:{lot_id}"))
    builder.row(InlineKeyboardButton(text="⏹ Завершить",        callback_data=f"mgmt:early_finish:{lot_id}"))
    builder.row(InlineKeyboardButton(text="← Мониторинг",       callback_data=f"lot:open:{lot_id}"))
    return builder.as_markup()


def kb_extend_pick(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for h, label in [(1, "+1 час"), (3, "+3 часа"), (6, "+6 часов"), (24, "+24 часа")]:
        builder.add(InlineKeyboardButton(text=label, callback_data=f"mgmt:extend:{lot_id}:{h}"))
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="← Назад", callback_data=f"lot:manage:{lot_id}"))
    return builder.as_markup()


def kb_confirm_action(lot_id: int, action: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да",    callback_data=f"mgmt:confirm:{action}:{lot_id}"),
        InlineKeyboardButton(text="❌ Нет",   callback_data=f"lot:manage:{lot_id}"),
    )
    return builder.as_markup()


def kb_ban_pick(lot_id: int, bidders: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for b in bidders:
        name = b.get("username") or f"id{b['user_id']}"
        builder.row(InlineKeyboardButton(
            text=f"🚫 {name} — ₽{b['amount']:,}",
            callback_data=f"mgmt:ban:{lot_id}:{b['user_id']}",
        ))
    builder.row(InlineKeyboardButton(text="← Назад", callback_data=f"lot:manage:{lot_id}"))
    return builder.as_markup()


def kb_ban_confirm(lot_id: int, user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Заблокировать", callback_data=f"mgmt:ban_confirm:{lot_id}:{user_id}"),
        InlineKeyboardButton(text="❌ Отмена",        callback_data=f"mgmt:ban_pick:{lot_id}"),
    )
    return builder.as_markup()


def kb_bid_step() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for step in [500, 1000, 2000, 5000, 10000]:
        builder.add(InlineKeyboardButton(text=f"{step:,} ₽", callback_data=f"create:step:{step}"))
    builder.adjust(3)
    return builder.as_markup()


def kb_duration() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for h, label in [(1, "1 час"), (3, "3 часа"), (6, "6 часов"),
                     (12, "12 часов"), (24, "24 часа"), (48, "48 часов")]:
        builder.add(InlineKeyboardButton(text=label, callback_data=f"create:duration:{h}"))
    builder.adjust(3)
    return builder.as_markup()


def kb_start_time() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="▶️ Начать сразу",      callback_data="create:start:now"))
    builder.row(InlineKeyboardButton(text="🕐 Запланировать",     callback_data="create:start:schedule"))
    return builder.as_markup()


def kb_confirm_lot() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Опубликовать", callback_data="create:confirm"),
        InlineKeyboardButton(text="❌ Отмена",       callback_data="create:cancel"),
    )
    return builder.as_markup()


def kb_finished_lots(lots: list, offset: int = 0, total: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lot in lots:
        builder.row(InlineKeyboardButton(
            text=f"{lot.emoji} {lot.title[:28]} — ₽{lot.final_price or 0:,}",
            callback_data=f"lot:view:{lot.id}",
        ))
    nav = []
    if offset > 0:
        nav.append(InlineKeyboardButton(text="← Назад", callback_data=f"lots:finished:{max(0, offset-10)}"))
    if offset + 10 < total:
        nav.append(InlineKeyboardButton(text="Вперёд →", callback_data=f"lots:finished:{offset+10}"))
    if nav:
        builder.row(*nav)
    builder.row(InlineKeyboardButton(text="← Главное меню", callback_data="menu:main"))
    return builder.as_markup()
