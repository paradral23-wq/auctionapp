"""
handlers/admins.py — управление администраторами бота.
"""
import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.queries import get_all_admins, get_admin, add_admin, remove_admin
from utils.guards import admin_only_callback, admin_only_message, super_admin_only_callback

logger = logging.getLogger(__name__)
router = Router()


class AddAdminFSM(StatesGroup):
    waiting_for_id       = State()
    waiting_for_username = State()
    waiting_for_name     = State()
    confirming           = State()


# ── Helpers ───────────────────────────────────────────────────

def _fmt(admin) -> str:
    name = admin.first_name or ""
    un   = f" {admin.username}" if admin.username else ""
    return f"{name}{un}".strip() or str(admin.user_id)


def kb_admins_list(admins, viewer_is_super: bool) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for a in admins:
        label = ("👑 " if a.is_super else "👤 ") + _fmt(a)
        b.row(InlineKeyboardButton(text=label, callback_data=f"adm:info:{a.user_id}"))
    if viewer_is_super:
        b.row(InlineKeyboardButton(text="➕ Добавить админа", callback_data="adm:add"))
    b.row(InlineKeyboardButton(text="← Главное меню", callback_data="menu:main"))
    return b.as_markup()


def kb_admin_info(admin, viewer_is_super: bool) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if viewer_is_super and not admin.is_super:
        b.row(InlineKeyboardButton(text="🗑 Удалить", callback_data=f"adm:remove_confirm:{admin.user_id}"))
    b.row(InlineKeyboardButton(text="← Список", callback_data="adm:list"))
    return b.as_markup()


def kb_confirm_add(user_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="✅ Добавить", callback_data=f"adm:add_confirm:{user_id}"),
        InlineKeyboardButton(text="❌ Отмена",   callback_data="adm:list"),
    )
    return b.as_markup()


def kb_confirm_remove(user_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="✅ Удалить", callback_data=f"adm:remove:{user_id}"),
        InlineKeyboardButton(text="❌ Отмена",  callback_data=f"adm:info:{user_id}"),
    )
    return b.as_markup()


def kb_cancel() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="❌ Отмена", callback_data="adm:list"))
    return b.as_markup()


def kb_skip_cancel() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="➡️ Пропустить", callback_data="adm:skip"))
    b.row(InlineKeyboardButton(text="❌ Отмена",      callback_data="adm:list"))
    return b.as_markup()


# ── Список ────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:admins")
async def cb_admins_list(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.clear()
    await _show_list(callback)
    await callback.answer()


@router.callback_query(F.data == "adm:list")
async def cb_adm_list(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.clear()
    await _show_list(callback)
    await callback.answer()


async def _show_list(callback: CallbackQuery):
    from utils.guards import is_super_admin
    admins = await get_all_admins()
    viewer_is_super = await is_super_admin(callback.from_user.id)

    lines = []
    for a in admins:
        badge = "👑" if a.is_super else "👤"
        name  = a.first_name or "—"
        un    = a.username or "без username"
        lines.append(f"{badge} {name} · {un} · <code>{a.user_id}</code>")

    text = (
        f"👥 <b>Администраторы</b> ({len(admins)})\n\n"
        + "\n".join(lines)
        + ("\n\n<i>👑 — суперадмин (неудаляем)</i>" if any(a.is_super for a in admins) else "")
    )
    try:
        await callback.message.edit_text(text, reply_markup=kb_admins_list(admins, viewer_is_super), parse_mode="HTML")
    except Exception:
        await callback.message.answer(text, reply_markup=kb_admins_list(admins, viewer_is_super), parse_mode="HTML")


# ── Карточка ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("adm:info:"))
async def cb_admin_info(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from utils.guards import is_super_admin

    user_id = int(callback.data.split(":")[2])
    admin = await get_admin(user_id)
    if not admin:
        await callback.answer("Не найден.", show_alert=True)
        return

    viewer_is_super = await is_super_admin(callback.from_user.id)
    badge = "👑 Суперадмин" if admin.is_super else "👤 Обычный админ"

    text = (
        f"<b>{badge}</b>\n\n"
        f"Имя: {admin.first_name or '—'}\n"
        f"Username: {admin.username or '—'}\n"
        f"Telegram ID: <code>{admin.user_id}</code>\n"
        f"Добавлен: {admin.added_at.strftime('%d.%m.%Y') if admin.added_at else '—'}"
    )
    await callback.message.edit_text(text, reply_markup=kb_admin_info(admin, viewer_is_super), parse_mode="HTML")
    await callback.answer()


# ── Добавление: шаг 1 — ID ───────────────────────────────────

@router.callback_query(F.data == "adm:add")
async def cb_add_start(callback: CallbackQuery, state: FSMContext):
    if not await super_admin_only_callback(callback):
        return
    await state.set_state(AddAdminFSM.waiting_for_id)
    await callback.message.edit_text(
        "➕ <b>Добавить администратора</b>\n\n"
        "Шаг 1/3 — Введите <b>Telegram ID</b>:\n\n"
        "<i>Узнать ID можно через @userinfobot</i>",
        reply_markup=kb_cancel(), parse_mode="HTML",
    )
    await callback.answer()


@router.message(AddAdminFSM.waiting_for_id)
async def msg_admin_id(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return

    text = (message.text or "").strip()
    if not text.lstrip("-").isdigit():
        await message.answer("❌ Введите числовой Telegram ID:", reply_markup=kb_cancel(), parse_mode="HTML")
        return

    user_id = int(text)
    existing = await get_admin(user_id)
    if existing:
        await message.answer(
            f"⚠️ Пользователь <code>{user_id}</code> уже администратор.",
            reply_markup=kb_cancel(), parse_mode="HTML",
        )
        return

    await state.update_data(new_user_id=user_id)
    await state.set_state(AddAdminFSM.waiting_for_username)
    await message.answer(
        f"✅ ID: <code>{user_id}</code>\n\n"
        f"─────────────────\n\n"
        f"Шаг 2/3 — Введите <b>username</b> (с @):\n\n"
        f"<i>Например: @username</i>",
        reply_markup=kb_skip_cancel(), parse_mode="HTML",
    )


# ── Добавление: шаг 2 — username ─────────────────────────────

@router.message(AddAdminFSM.waiting_for_username)
async def msg_admin_username(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return

    text = (message.text or "").strip()
    # Нормализуем — убираем @ если есть, потом добавим обратно при отображении
    if text.startswith("@"):
        username = text  # храним с @
    else:
        username = f"@{text}" if text else None

    await state.update_data(new_username=username)
    await state.set_state(AddAdminFSM.waiting_for_name)

    un_str = username or "—"
    await message.answer(
        f"✅ Username: {un_str}\n\n"
        f"─────────────────\n\n"
        f"Шаг 3/3 — Введите <b>имя</b> для отображения:\n\n"
        f"<i>Например: Иван Иванов</i>",
        reply_markup=kb_skip_cancel(), parse_mode="HTML",
    )


@router.callback_query(F.data == "adm:skip", AddAdminFSM.waiting_for_username)
async def cb_skip_username(callback: CallbackQuery, state: FSMContext):
    if not await super_admin_only_callback(callback):
        return
    await state.update_data(new_username=None)
    await state.set_state(AddAdminFSM.waiting_for_name)
    await callback.message.answer(
        "Шаг 3/3 — Введите <b>имя</b> для отображения:\n\n"
        "<i>Например: Иван Иванов</i>",
        reply_markup=kb_skip_cancel(), parse_mode="HTML",
    )
    await callback.answer()


# ── Добавление: шаг 3 — имя ──────────────────────────────────

@router.message(AddAdminFSM.waiting_for_name)
async def msg_admin_name(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return

    name = (message.text or "").strip() or None
    await state.update_data(new_first_name=name)
    await _show_confirm(message, state)


@router.callback_query(F.data == "adm:skip", AddAdminFSM.waiting_for_name)
async def cb_skip_name(callback: CallbackQuery, state: FSMContext):
    if not await super_admin_only_callback(callback):
        return
    await state.update_data(new_first_name=None)
    await _show_confirm(callback.message, state, via_callback=True)
    await callback.answer()


async def _show_confirm(target, state: FSMContext, via_callback: bool = False):
    data = await state.get_data()
    await state.set_state(AddAdminFSM.confirming)

    user_id  = data.get("new_user_id")
    username = data.get("new_username") or "—"
    name     = data.get("new_first_name") or "—"

    text = (
        f"➕ <b>Подтвердите добавление</b>\n\n"
        f"Telegram ID: <code>{user_id}</code>\n"
        f"Username: {username}\n"
        f"Имя: {name}"
    )
    kb = kb_confirm_add(user_id)
    if via_callback:
        await target.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=kb, parse_mode="HTML")


# ── Добавление: подтверждение ─────────────────────────────────

@router.callback_query(F.data.startswith("adm:add_confirm:"))
async def cb_add_confirm(callback: CallbackQuery, state: FSMContext):
    if not await super_admin_only_callback(callback):
        return

    user_id = int(callback.data.split(":")[2])
    data = await state.get_data()
    await state.clear()

    if not data.get("new_user_id"):
        await callback.answer("Сессия истекла, начните заново.", show_alert=True)
        return

    username   = data.get("new_username")
    first_name = data.get("new_first_name")

    await add_admin(
        user_id=user_id,
        username=username,
        first_name=first_name,
        added_by=callback.from_user.id,
        is_super=False,
    )

    display = first_name or username or str(user_id)

    try:
        await callback.bot.send_message(
            chat_id=user_id,
            text="👑 <b>Вы добавлены как администратор аукциона!</b>\n\nНапишите /start чтобы открыть панель управления.",
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"Could not notify new admin {user_id}: {e}")

    await callback.message.edit_text(
        f"✅ <b>{display}</b> добавлен как администратор.\n\n"
        f"Telegram ID: <code>{user_id}</code>",
        reply_markup=kb_admins_list(await get_all_admins(), True),
        parse_mode="HTML",
    )
    await callback.answer("✅ Добавлен")


# ── Удаление ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("adm:remove_confirm:"))
async def cb_remove_confirm(callback: CallbackQuery):
    if not await super_admin_only_callback(callback):
        return

    user_id = int(callback.data.split(":")[2])
    admin = await get_admin(user_id)
    if not admin:
        await callback.answer("Не найден.", show_alert=True)
        return
    if admin.is_super:
        await callback.answer("Суперадмина нельзя удалить.", show_alert=True)
        return

    await callback.message.edit_text(
        f"⚠️ <b>Удалить администратора?</b>\n\n"
        f"{_fmt(admin)}\n"
        f"<code>{user_id}</code>\n\n"
        f"Доступ к боту будет закрыт.",
        reply_markup=kb_confirm_remove(user_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:remove:"))
async def cb_remove(callback: CallbackQuery):
    if not await super_admin_only_callback(callback):
        return

    user_id = int(callback.data.split(":")[2])
    admin = await get_admin(user_id)
    display = _fmt(admin) if admin else str(user_id)

    ok = await remove_admin(user_id)
    if not ok:
        await callback.answer("Не удалось удалить.", show_alert=True)
        return

    try:
        await callback.bot.send_message(chat_id=user_id, text="ℹ️ Ваши права администратора аукциона были отозваны.")
    except Exception:
        pass

    await callback.message.edit_text(
        f"🗑 <b>{display}</b> удалён из администраторов.",
        reply_markup=kb_admins_list(await get_all_admins(), True),
        parse_mode="HTML",
    )
    await callback.answer("Удалён")
