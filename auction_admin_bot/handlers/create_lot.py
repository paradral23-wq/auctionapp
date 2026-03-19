"""
handlers/create_lot.py — FSM создания лота недвижимости (17 шагов).
Медиа (шаг 3): несколько фото + 1 видео. Хранятся в таблице lot_media.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.queries import create_lot
from utils.formatting import fmt_duration
from utils.guards import admin_only_callback, admin_only_message
from utils.states import CreateLotFSM
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
router = Router()

# Глобальный lock для синхронизации обработки медиагрупп
import asyncio as _asyncio
_media_locks: dict = {}

DEFAULT_EMOJI    = "🏠"
VIDEOS_DIR       = Path(os.getenv("VIDEOS_DIR", "./videos"))
DEFAULT_CATEGORY = "Real Estate"

MIN_AREA = 100
MAX_AREA = 99_999

MIN_AED_DIGITS = 6
MAX_AED_DIGITS = 9
MIN_AED = 10 ** (MIN_AED_DIGITS - 1)
MAX_AED = 10 ** MAX_AED_DIGITS - 1

MIN_PRICE_STEP      = 500
MIN_INTERVAL_MINUTES = 1
MAX_INTERVAL_MINUTES = 60

MAX_PHOTOS = 10   # максимум фото на лот
CANCEL_CB  = "menu:main"


# ── Клавиатуры ────────────────────────────────────────────────

def _cancel_row():
    return [InlineKeyboardButton(text="❌ Отмена", callback_data=CANCEL_CB)]

def _back_cancel_row(back_cb: str):
    return [
        InlineKeyboardButton(text="← Назад", callback_data=back_cb),
        InlineKeyboardButton(text="❌ Отмена", callback_data=CANCEL_CB),
    ]

def kb_back_cancel(back_cb: str) -> InlineKeyboardMarkup:
    """Клавиатура для текстовых шагов — только Назад и Отмена."""
    b = InlineKeyboardBuilder()
    b.row(*_back_cancel_row(back_cb))
    return b.as_markup()


def kb_property_type() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for t in ["1BR","2BR","3BR","4BR","5BR"]:
        b.add(InlineKeyboardButton(text=t, callback_data=f"lot_type:{t}"))
    b.adjust(5)
    for t in ["6BR","7BR","8BR","9BR"]:
        b.add(InlineKeyboardButton(text=t, callback_data=f"lot_type:{t}"))
    b.adjust(5, 4)
    b.row(InlineKeyboardButton(text="🏢 Studio", callback_data="lot_type:Studio"))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:media"))
    b.row(*_cancel_row())
    return b.as_markup()


def kb_floor() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="⬆️ High floor", callback_data="lot_floor:High floor"),
        InlineKeyboardButton(text="➡️ Mid floor",  callback_data="lot_floor:Mid floor"),
        InlineKeyboardButton(text="⬇️ Low floor",  callback_data="lot_floor:Low floor"),
    )
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:type"))
    b.row(*_cancel_row())
    return b.as_markup()


def kb_view() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="🌊 Sea",   callback_data="lot_view:Sea view"),
        InlineKeyboardButton(text="🏙 City",  callback_data="lot_view:City view"),
        InlineKeyboardButton(text="🏗 Facilities", callback_data="lot_view:Facilities view"),
    )
    b.row(
        InlineKeyboardButton(text="🚫 No view",      callback_data="lot_view:No view"),
        InlineKeyboardButton(text="🌆 Burj Khalifa", callback_data="lot_view:Burj Khalifa view"),
    )
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:floor"))
    b.row(*_cancel_row())
    return b.as_markup()


def kb_parking() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for n in range(0, 10):
        b.add(InlineKeyboardButton(text=str(n), callback_data=f"lot_parking:{n}"))
    b.adjust(5, 5)
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:view"))
    b.row(*_cancel_row())
    return b.as_markup()


def kb_property_status() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="🟢 Vacant",   callback_data="lot_status:Vacant"),
        InlineKeyboardButton(text="🔴 Tenanted", callback_data="lot_status:Tenanted"),
    )
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:parking"))
    b.row(*_cancel_row())
    return b.as_markup()


def kb_price_step() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="10 000 AED", callback_data="lot_step:10000"),
        InlineKeyboardButton(text="25 000 AED", callback_data="lot_step:25000"),
        InlineKeyboardButton(text="50 000 AED", callback_data="lot_step:50000"),
    )
    b.row(InlineKeyboardButton(text="✏️ Свой шаг", callback_data="lot_step:custom"))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:status"))
    b.row(*_cancel_row())
    return b.as_markup()


def kb_interval() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="⏱ 2 мин", callback_data="lot_interval:2"),
        InlineKeyboardButton(text="⏱ 3 мин", callback_data="lot_interval:3"),
        InlineKeyboardButton(text="⏱ 5 мин", callback_data="lot_interval:5"),
    )
    b.row(InlineKeyboardButton(text="✏️ Свой интервал", callback_data="lot_interval:custom"))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:price_step"))
    b.row(*_cancel_row())
    return b.as_markup()


def kb_confirm() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🚀 Активировать аукцион",   callback_data="lot:launch"))
    b.row(InlineKeyboardButton(text="🕐 Запланировать старт",    callback_data="lot:schedule"))
    b.row(InlineKeyboardButton(text="💾 Сохранить как черновик", callback_data="lot:save_draft"))
    b.row(InlineKeyboardButton(text="✏️ Редактировать",          callback_data="lot:edit"))
    b.row(InlineKeyboardButton(text="← Назад",                   callback_data="lot:back:interval"))
    b.row(InlineKeyboardButton(text="🗑 Отмена",                 callback_data=CANCEL_CB))
    return b.as_markup()


def kb_media(photo_count: int, has_video: bool) -> InlineKeyboardMarkup:
    """Клавиатура во время загрузки медиа."""
    b = InlineKeyboardBuilder()
    status_parts = []
    if photo_count > 0:
        status_parts.append(f"📷 {photo_count} фото")
    if has_video:
        status_parts.append("🎥 видео")
    if status_parts:
        b.row(InlineKeyboardButton(
            text="✅ Готово (" + ", ".join(status_parts) + ")",
            callback_data="lot_media_done"
        ))
    b.row(InlineKeyboardButton(text="⏭ Пропустить", callback_data="lot_skip"))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:title"))
    b.row(*_cancel_row())
    return b.as_markup()


def kb_skip_cancel() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="⏭ Пропустить", callback_data="lot_skip"))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back:title"))
    b.row(*_cancel_row())
    return b.as_markup()


# ── Утилиты ───────────────────────────────────────────────────

def _fmt_aed(amount: int) -> str:
    return f"AED {amount:,}".replace(",", " ")


def _parse_aed(text: str) -> Optional[int]:
    clean = text.strip().upper().replace("AED","").replace(" ","").replace(",","").replace(".","")
    if not clean.isdigit():
        return None
    val = int(clean)
    if not (MIN_AED <= val <= MAX_AED):
        return None
    return val


def _summary_text(d: dict) -> str:
    discount_line = ""
    if d.get("discount_pct") is not None and d.get("market_price"):
        calc = round(d["market_price"] * (1 - d["discount_pct"] / 100))
        discount_line = (
            f"• Скидка к рынку: <b>{d['discount_pct']}%</b> "
            f"→ расчётная: <b>{_fmt_aed(calc)}</b>\n"
        )

    # Медиа summary
    photos    = d.get("media_photos", [])
    has_video = bool(d.get("media_video"))
    media_line = ""
    if photos or has_video:
        parts = []
        if photos:    parts.append(f"📷 {len(photos)} фото")
        if has_video: parts.append("🎥 видео")
        media_line = f"• Медиа: {', '.join(parts)}\n"
    else:
        media_line = "• Медиа: —\n"

    return (
        f"✅ <b>Проверка лота</b>\n\n─────────────────\n\n"
        f"<b>Объект</b>\n"
        f"• Название: <b>{d.get('title','—')}</b>\n"
        f"• Тип: <b>{d.get('property_type','—')}</b>  "
        f"· Площадь: <b>{d.get('area_sqft','—')} sqft</b>\n"
        f"• Этаж: <b>{d.get('floor_level','—')}</b>  "
        f"· Вид: <b>{d.get('view_type','—')}</b>\n"
        f"• Парковка: <b>{d.get('parking_spots','—')}</b>  "
        f"· Статус: <b>{d.get('property_status','—')}</b>\n"
        f"• Описание: {d.get('description') or '—'}\n"
        f"{media_line}\n"
        f"<b>Цены</b>\n"
        f"• Цена покупки: <b>{_fmt_aed(d['purchase_price'])}</b>\n"
        f"• Рыночная: <b>{_fmt_aed(d['market_price'])}</b>\n"
        f"• Старт аукциона: <b>{_fmt_aed(d['start_price'])}</b>\n"
        f"{discount_line}"
        f"\n<b>Dutch-аукцион</b>\n"
        f"• Шаг снижения: <b>{_fmt_aed(d['bid_step'])}</b>\n"
        f"• Интервал: <b>{d.get('price_drop_interval_minutes','—')} мин</b>\n"
        f"• Мин. цена (резерв): <b>{_fmt_aed(d['min_price'])}</b>\n"
    )




# ── Кнопки "← Назад" ──────────────────────────────────────────

@router.callback_query(F.data == "lot:back:title")
async def cb_back_title(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 1 — название."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("title", "")
    await state.set_state(CreateLotFSM.entering_title)
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="❌ Отмена", callback_data=CANCEL_CB))
    await callback.message.answer(
        f"<b>Шаг 1/17 — Название</b>\n\n"
        f"Текущее: <b>{cur or '—'}</b>\n\nВведите новое название:",
        reply_markup=b.as_markup(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:media")
async def cb_back_media(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 3 — медиа."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    await state.set_state(CreateLotFSM.uploading_media)
    # Сбрасываем media_msg_id чтобы новые фото создали новое сообщение
    await state.update_data(media_msg_id=None)
    photos = data.get("media_photos", [])
    has_video = bool(data.get("media_video"))
    sent = await callback.message.answer(
        _media_prompt(data),
        reply_markup=kb_media(len(photos), has_video), parse_mode="HTML",
    )
    await state.update_data(media_msg_id=sent.message_id)
    await callback.answer()


@router.callback_query(F.data == "lot:back:type")
async def cb_back_type(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 4 — тип."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("property_type", "")
    await state.set_state(CreateLotFSM.choosing_type)
    await callback.message.answer(
        f"<b>Шаг 4/17 — Тип недвижимости</b>\n\nТекущее: <b>{cur or '—'}</b>\n\nВыберите тип:",
        reply_markup=kb_property_type(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:floor")
async def cb_back_floor(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 6 — этаж."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("floor_level", "")
    await state.set_state(CreateLotFSM.choosing_floor)
    await callback.message.answer(
        f"<b>Шаг 6/17 — Этаж</b>\n\nТекущее: <b>{cur or '—'}</b>\n\nВыберите уровень:",
        reply_markup=kb_floor(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:view")
async def cb_back_view(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 7 — вид."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("view_type", "")
    await state.set_state(CreateLotFSM.choosing_view)
    await callback.message.answer(
        f"<b>Шаг 7/17 — Вид</b>\n\nТекущее: <b>{cur or '—'}</b>\n\nВыберите вид:",
        reply_markup=kb_view(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:parking")
async def cb_back_parking(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 8 — парковка."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("parking_spots")
    await state.set_state(CreateLotFSM.choosing_parking)
    await callback.message.answer(
        f"<b>Шаг 8/17 — Парковка</b>\n\nТекущее: <b>{cur if cur is not None else '—'}</b>\n\nКоличество мест:",
        reply_markup=kb_parking(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:status")
async def cb_back_status(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 9 — статус."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("property_status", "")
    await state.set_state(CreateLotFSM.choosing_status)
    await callback.message.answer(
        f"<b>Шаг 9/17 — Статус</b>\n\nТекущее: <b>{cur or '—'}</b>\n\nВыберите статус:",
        reply_markup=kb_property_status(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:purchase_price")
async def cb_back_purchase_price(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 10 — цена покупки."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("purchase_price")
    await state.set_state(CreateLotFSM.entering_purchase_price)
    await callback.message.answer(
        f"<b>Шаг 10/17 — Цена покупки</b>\n\nТекущее: <b>{_fmt_aed(cur) if cur else '—'}</b>\n\nВведите цену покупки (AED):",
        reply_markup=kb_back_cancel("lot:back:status"), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:market_price")
async def cb_back_market_price(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 11 — рыночная цена."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("market_price")
    await state.set_state(CreateLotFSM.entering_market_price)
    await callback.message.answer(
        f"<b>Шаг 11/17 — Рыночная цена</b>\n\nТекущее: <b>{_fmt_aed(cur) if cur else '—'}</b>\n\nВведите рыночную стоимость (AED):",
        reply_markup=kb_back_cancel("lot:back:purchase_price"), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:start_price")
async def cb_back_start_price(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 12 — старт цена."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("start_price")
    await state.set_state(CreateLotFSM.entering_start_price)
    await callback.message.answer(
        f"<b>Шаг 12/17 — Старт цена</b>\n\nТекущее: <b>{_fmt_aed(cur) if cur else '—'}</b>\n\nВведите стартовую цену аукциона (AED):",
        reply_markup=kb_back_cancel("lot:back:market_price"), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:price_step")
async def cb_back_price_step(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 14 — шаг снижения."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("bid_step")
    await state.set_state(CreateLotFSM.choosing_price_step)
    await callback.message.answer(
        f"<b>Шаг 14/17 — Шаг снижения</b>\n\nТекущее: <b>{_fmt_aed(cur) if cur else '—'}</b>\n\nВыберите или введите шаг:",
        reply_markup=kb_price_step(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "lot:back:interval")
async def cb_back_interval(callback: CallbackQuery, state: FSMContext):
    """Назад к шагу 15 — интервал."""
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    cur = data.get("price_drop_interval_minutes")
    await state.set_state(CreateLotFSM.choosing_interval)
    await callback.message.answer(
        f"<b>Шаг 15/17 — Интервал снижения</b>\n\nТекущее: <b>{cur if cur else '—'} мин</b>\n\nКак часто снижается цена?",
        reply_markup=kb_interval(), parse_mode="HTML",
    )
    await callback.answer()

# ── Шаг 1 — Старт / Название ──────────────────────────────────

@router.callback_query(F.data == "menu:create")
async def cb_create_start(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.clear()
    await state.update_data(
        emoji=DEFAULT_EMOJI, category=DEFAULT_CATEGORY,
        media_photos=[], media_video=None,
    )
    await state.set_state(CreateLotFSM.entering_title)
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="❌ Отмена", callback_data=CANCEL_CB))
    await callback.message.edit_text(
        "➕ <b>Создание лота — шаг 1/17</b>\n\n"
        "Введите <b>название объекта</b> недвижимости:\n\n"
        "<i>Мин. 5 · Макс. 80 символов</i>",
        reply_markup=b.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(CreateLotFSM.entering_title)
async def msg_title(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    title = (message.text or "").strip()
    if not (5 <= len(title) <= 80):
        await message.answer("❌ Название должно быть от 5 до 80 символов.\nПопробуйте снова:")
        return
    await state.update_data(title=title, description="")
    await state.set_state(CreateLotFSM.uploading_media)
    data = await state.get_data()
    await message.answer(
        f"✅ Название: <b>{title}</b>\n\n─────────────────\n\n"
        + _media_prompt(data),
        reply_markup=kb_media(0, False), parse_mode="HTML",
    )


# ── Шаг 2 — Описание ──────────────────────────────────────────

@router.callback_query(F.data == "lot_skip", CreateLotFSM.entering_description)
async def cb_skip_desc(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.update_data(description=None)
    await state.set_state(CreateLotFSM.uploading_media)
    data = await state.get_data()
    await callback.message.edit_text(
        _media_prompt(data), reply_markup=kb_media(0, False), parse_mode="HTML",
    )
    await callback.answer()


@router.message(CreateLotFSM.entering_description)
async def msg_description(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    desc = (message.text or "").strip()
    if not (10 <= len(desc) <= 500):
        await message.answer("❌ Описание от 10 до 500 символов.\nПопробуйте снова:")
        return
    await state.update_data(description=desc)
    await state.set_state(CreateLotFSM.uploading_media)
    await message.answer(
        _media_prompt({"media_photos": [], "media_video": None}),
        reply_markup=kb_media(0, False), parse_mode="HTML",
    )


def _media_prompt(data: dict) -> str:
    photos    = data.get("media_photos", [])
    has_video = bool(data.get("media_video"))
    lines = ["🖼 <b>Шаг 3/17 — Медиафайлы</b>\n"]
    lines.append(f"Отправьте фото (до {MAX_PHOTOS} штук) и/или видео.\n")
    if photos or has_video:
        parts = []
        if photos:    parts.append(f"📷 {len(photos)} фото")
        if has_video: parts.append("🎥 1 видео")
        lines.append(f"Загружено: {', '.join(parts)}\n")
    lines.append("<i>Когда всё загружено — нажмите Готово.</i>")
    return "\n".join(lines)


# ── Шаг 3 — Медиа ─────────────────────────────────────────────

@router.callback_query(F.data == "lot_skip", CreateLotFSM.uploading_media)
async def cb_skip_media(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.update_data(media_photos=[], media_video=None)
    await _go_to_type(callback.message, state, edit=True)
    await callback.answer()


@router.callback_query(F.data == "lot_media_done", CreateLotFSM.uploading_media)
async def cb_media_done(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await _go_to_type(callback.message, state, edit=True)
    await callback.answer()


@router.message(CreateLotFSM.uploading_media)
async def msg_media(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    data = await state.get_data()
    photos    = list(data.get("media_photos", []))
    has_video = bool(data.get("media_video"))

    if message.photo:
        if len(photos) >= MAX_PHOTOS:
            await message.answer(f"❌ Максимум {MAX_PHOTOS} фото. Нажмите Готово.")
            return

        file_id = message.photo[-1].file_id
        user_id = message.from_user.id

        # Используем lock на пользователя для атомарного обновления state
        if user_id not in _media_locks:
            _media_locks[user_id] = _asyncio.Lock()
        async with _media_locks[user_id]:
            # Читаем актуальный state внутри lock
            fresh = await state.get_data()
            fresh_photos = list(fresh.get("media_photos", []))
            if file_id not in fresh_photos:
                fresh_photos.append(file_id)
            media_msg_id = fresh.get("media_msg_id")

            await state.update_data(media_photos=fresh_photos)

            new_text = _media_prompt({"media_photos": fresh_photos, "media_video": fresh.get("media_video")})
            new_kb   = kb_media(len(fresh_photos), bool(fresh.get("media_video")))

            if media_msg_id:
                try:
                    await message.bot.edit_message_text(
                        chat_id=message.chat.id, message_id=media_msg_id,
                        text=new_text, reply_markup=new_kb, parse_mode="HTML",
                    )
                except Exception:
                    pass
            else:
                sent = await message.answer(new_text, reply_markup=new_kb, parse_mode="HTML")
                await state.update_data(media_msg_id=sent.message_id)

    elif message.video:
        if has_video:
            await message.answer("❌ Видео уже загружено. Можно добавить только одно.")
            return
        MAX_VIDEO_BYTES = 200 * 1024 * 1024  # 200 MB
        if message.video.file_size and message.video.file_size > MAX_VIDEO_BYTES:
            size_mb = message.video.file_size // (1024 * 1024)
            await message.answer(
                f"❌ Видео слишком большое: <b>{size_mb} MB</b>.\nМаксимум: 200 MB.",
                parse_mode="HTML",
            )
            return
        file_id = message.video.file_id
        wait_msg = await message.answer("⏳ Скачиваю видео на сервер...")
        try:
            local_path = await _download_video(message.bot, file_id)
            await state.update_data(media_video=file_id, media_video_path=str(local_path))
            size_mb = (message.video.file_size or 0) // (1024 * 1024)
            await wait_msg.edit_text(f"✅ Видео загружено ({size_mb} MB)")
        except Exception as e:
            logger.error(f"Video download failed: {e}")
            await wait_msg.edit_text("❌ Не удалось скачать видео. Попробуйте снова.")
            return
        await message.answer(
            _media_prompt({"media_photos": photos, "media_video": file_id}),
            reply_markup=kb_media(len(photos), True), parse_mode="HTML",
        )

    elif message.document and message.document.mime_type and message.document.mime_type.startswith("video/"):
        # Видео отправлено как файл без сжатия
        if has_video:
            await message.answer("❌ Видео уже загружено. Можно добавить только одно.")
            return
        MAX_VIDEO_BYTES = 200 * 1024 * 1024
        if message.document.file_size and message.document.file_size > MAX_VIDEO_BYTES:
            size_mb = message.document.file_size // (1024 * 1024)
            await message.answer(
                f"❌ Видео слишком большое: <b>{size_mb} MB</b>.\nМаксимум: 200 MB.",
                parse_mode="HTML",
            )
            return
        file_id = message.document.file_id
        wait_msg = await message.answer("⏳ Скачиваю видео на сервер...")
        try:
            local_path = await _download_video(message.bot, file_id)
            await state.update_data(media_video=file_id, media_video_path=str(local_path))
            size_mb = (message.document.file_size or 0) // (1024 * 1024)
            await wait_msg.edit_text(f"✅ Видео загружено ({size_mb} MB)")
        except Exception as e:
            logger.error(f"Video download failed: {e}")
            await wait_msg.edit_text("❌ Не удалось скачать видео. Попробуйте снова.")
            return
        await message.answer(
            _media_prompt({"media_photos": photos, "media_video": file_id}),
            reply_markup=kb_media(len(photos), True), parse_mode="HTML",
        )

    else:
        await message.answer(
            "❌ Отправьте фото или видео.\nИли нажмите <b>Пропустить</b>.",
            parse_mode="HTML",
        )


async def _download_video(bot, file_id: str) -> Path:
    """Скачать видео с Telegram на локальный диск."""
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    # Получаем уникальное имя файла из file_id
    safe_name = file_id.replace("/", "_").replace("\\", "_")[:50]
    dest = VIDEOS_DIR / f"{safe_name}.mp4"
    if dest.exists():
        return dest
    # Скачиваем через aiogram
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, destination=str(dest))
    return dest


async def _go_to_type(target, state: FSMContext, edit: bool = False):
    await state.set_state(CreateLotFSM.choosing_type)
    text = "<b>Шаг 4/17 — Тип недвижимости</b>\n\nВыберите тип объекта:"
    if edit:
        await target.edit_text(text, reply_markup=kb_property_type(), parse_mode="HTML")
    else:
        await target.answer(text, reply_markup=kb_property_type(), parse_mode="HTML")


# ── Шаги 4–9: выбор кнопками ──────────────────────────────────

@router.callback_query(F.data.startswith("lot_type:"), CreateLotFSM.choosing_type)
async def cb_type(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    prop_type = callback.data.split(":", 1)[1]
    await state.update_data(property_type=prop_type)
    await state.set_state(CreateLotFSM.entering_area)
    await callback.message.answer(
        f"✅ Тип: <b>{prop_type}</b>\n\n─────────────────\n\n<b>Шаг 5/17 — Площадь</b>\n\n"
        f"Введите площадь объекта:\n<i>Диапазон: {MIN_AREA:,} – {MAX_AREA:,} sqft</i>",
        reply_markup=kb_back_cancel("lot:back:type"),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(CreateLotFSM.entering_area)
async def msg_area(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = (message.text or "").strip().replace(" ","").replace(",","")
    if not raw.isdigit() or not (MIN_AREA <= int(raw) <= MAX_AREA):
        await message.answer(f"❌ Введите целое число от {MIN_AREA:,} до {MAX_AREA:,} sqft.")
        return
    area = int(raw)
    await state.update_data(area_sqft=area)
    await state.set_state(CreateLotFSM.choosing_floor)
    await message.answer(
        f"✅ Площадь: <b>{area:,} sqft</b>\n\n─────────────────\n\n<b>Шаг 6/17 — Этаж</b>\n\nВыберите уровень:",
        reply_markup=kb_floor(), parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("lot_floor:"), CreateLotFSM.choosing_floor)
async def cb_floor(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    floor = callback.data.split(":", 1)[1]
    await state.update_data(floor_level=floor)
    await state.set_state(CreateLotFSM.choosing_view)
    await callback.message.answer(
        f"✅ Этаж: <b>{floor} floor</b>\n\n─────────────────\n\n<b>Шаг 7/17 — Вид</b>\n\nВыберите вид:",
        reply_markup=kb_view(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lot_view:"), CreateLotFSM.choosing_view)
async def cb_view(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    view = callback.data.split(":", 1)[1]
    await state.update_data(view_type=view)
    await state.set_state(CreateLotFSM.choosing_parking)
    await callback.message.answer(
        f"✅ Вид: <b>{view}</b>\n\n─────────────────\n\n<b>Шаг 8/17 — Парковка</b>\n\nКоличество мест:",
        reply_markup=kb_parking(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lot_parking:"), CreateLotFSM.choosing_parking)
async def cb_parking(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    spots = int(callback.data.split(":", 1)[1])
    await state.update_data(parking_spots=spots)
    await state.set_state(CreateLotFSM.choosing_status)
    await callback.message.answer(
        f"✅ Парковка: <b>{spots}</b>\n\n─────────────────\n\n<b>Шаг 9/17 — Статус</b>\n\nВыберите статус:",
        reply_markup=kb_property_status(), parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lot_status:"), CreateLotFSM.choosing_status)
async def cb_prop_status(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    status = callback.data.split(":", 1)[1]
    await state.update_data(property_status=status)
    await state.set_state(CreateLotFSM.entering_purchase_price)
    await callback.message.answer(
        f"✅ Статус: <b>{status}</b>\n\n─────────────────\n\n<b>Шаг 10/17 — Original Purchase Price</b>\n\n"
        f"Введите цену покупки:\n<i>AED · Мин. {MIN_AED_DIGITS} знаков</i>",
        reply_markup=kb_back_cancel("lot:back:status"),
        parse_mode="HTML",
    )
    await callback.answer()


# ── Шаги 10–12: цены ─────────────────────────────────────────

@router.message(CreateLotFSM.entering_purchase_price)
async def msg_purchase_price(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    val = _parse_aed(message.text or "")
    if val is None:
        await message.answer(f"❌ Введите сумму в AED от {_fmt_aed(MIN_AED)}.")
        return
    await state.update_data(purchase_price=val)
    await state.set_state(CreateLotFSM.entering_market_price)
    await message.answer(
        f"✅ Цена покупки: <b>{_fmt_aed(val)}</b>\n\n─────────────────\n\n<b>Шаг 11/17 — Current Market Price</b>\n\n"
        f"Введите рыночную стоимость:",
        reply_markup=kb_back_cancel("lot:back:purchase_price"),
        parse_mode="HTML",
    )

@router.message(CreateLotFSM.entering_market_price)
async def msg_market_price(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    val = _parse_aed(message.text or "")
    if val is None:
        await message.answer(f"❌ Введите сумму в AED от {_fmt_aed(MIN_AED)}.")
        return
    await state.update_data(market_price=val)
    await state.set_state(CreateLotFSM.entering_start_price)
    await message.answer(
        f"✅ Рыночная: <b>{_fmt_aed(val)}</b>\n\n─────────────────\n\n<b>Шаг 12/17 — Auction Start Price</b>\n\n"
        f"Введите стартовую цену аукциона:",
        reply_markup=kb_back_cancel("lot:back:market_price"),
        parse_mode="HTML",
    )

@router.message(CreateLotFSM.entering_start_price)
async def msg_start_price(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    val = _parse_aed(message.text or "")
    if val is None:
        await message.answer(f"❌ Введите сумму в AED от {_fmt_aed(MIN_AED)}.")
        return
    data = await state.get_data()
    market = data.get("market_price", 0)
    await state.update_data(start_price=val)
    await state.set_state(CreateLotFSM.choosing_price_step)
    await message.answer(
        f"✅ Старт: <b>{_fmt_aed(val)}</b>\n\n─────────────────\n\n<b>Шаг 14/17 — Шаг снижения</b>\n\nВыберите или введите шаг:",
        reply_markup=kb_price_step(),
        parse_mode="HTML",
    )


# ── Шаг 13 — Скидка ───────────────────────────────────────────

@router.message(CreateLotFSM.entering_discount)
async def msg_discount(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = (message.text or "").strip().replace("%","")
    if not raw.isdigit() or not (1 <= int(raw) <= 99):
        await message.answer("❌ Введите число от 1 до 99.")
        return
    discount = int(raw)
    data   = await state.get_data()
    market = data.get("market_price", 0)
    calc   = round(market * (1 - discount / 100)) if market else 0
    await state.update_data(discount_pct=discount)
    await state.set_state(CreateLotFSM.choosing_price_step)
    await message.answer(
        f"✅ Скидка: <b>{discount}%</b> → <b>{_fmt_aed(calc)}</b>\n\n─────────────────\n\n"
        f"<b>Шаг 14/17 — Шаг снижения</b>\n\nВыберите или введите шаг:",
        reply_markup=kb_price_step(), parse_mode="HTML",
    )


# ── Шаг 14 — Шаг снижения ────────────────────────────────────

@router.callback_query(F.data.startswith("lot_step:"), CreateLotFSM.choosing_price_step)
async def cb_price_step(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    val = callback.data.split(":", 1)[1]
    if val == "custom":
        await state.set_state(CreateLotFSM.entering_price_step)
        await callback.message.answer(
            f"<b>Шаг 14/17 — Свой шаг</b>\n\nВведите шаг в AED (мин. {MIN_PRICE_STEP:,}):",
            parse_mode="HTML",
        )
    else:
        step = int(val)
        await state.update_data(bid_step=step)
        await state.set_state(CreateLotFSM.choosing_interval)
        await callback.message.answer(
            f"✅ Шаг: <b>{_fmt_aed(step)}</b>\n\n─────────────────\n\n<b>Шаг 15/17 — Интервал снижения</b>\n\n"
            f"Как часто снижается цена?",
            reply_markup=kb_interval(), parse_mode="HTML",
        )
    await callback.answer()


@router.message(CreateLotFSM.entering_price_step)
async def msg_price_step(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = (message.text or "").strip().replace(" ","").replace(",","")
    if not raw.isdigit() or int(raw) < MIN_PRICE_STEP:
        await message.answer(f"❌ Минимальный шаг: {MIN_PRICE_STEP:,} AED.")
        return
    step = int(raw)
    await state.update_data(bid_step=step)
    await state.set_state(CreateLotFSM.choosing_interval)
    await message.answer(
        f"✅ Шаг: <b>{_fmt_aed(step)}</b>\n\n─────────────────\n\n<b>Шаг 15/17 — Интервал снижения</b>",
        reply_markup=kb_interval(), parse_mode="HTML",
    )


# ── Шаг 15 — Интервал ─────────────────────────────────────────

@router.callback_query(F.data.startswith("lot_interval:"), CreateLotFSM.choosing_interval)
async def cb_interval(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    val = callback.data.split(":", 1)[1]
    if val == "custom":
        await state.set_state(CreateLotFSM.entering_interval)
        await callback.message.answer(
            f"<b>Шаг 15/17 — Свой интервал</b>\n\nВведите минуты ({MIN_INTERVAL_MINUTES}–{MAX_INTERVAL_MINUTES}):",
            parse_mode="HTML",
        )
    else:
        minutes = int(val)
        await state.update_data(price_drop_interval_minutes=minutes)
        await state.set_state(CreateLotFSM.entering_min_price)
        await callback.message.answer(
            f"✅ Интервал: <b>{minutes} мин</b>\n\n─────────────────\n\n<b>Шаг 16/17 — Минимальная цена</b>\n\n"
            f"Резервная цена — если достигнет этой отметки без покупки, аукцион не состоится:",
            reply_markup=kb_back_cancel("lot:back:interval"),
            parse_mode="HTML",
        )
    await callback.answer()


@router.message(CreateLotFSM.entering_interval)
async def msg_interval(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = (message.text or "").strip()
    if not raw.isdigit() or not (MIN_INTERVAL_MINUTES <= int(raw) <= MAX_INTERVAL_MINUTES):
        await message.answer(f"❌ От {MIN_INTERVAL_MINUTES} до {MAX_INTERVAL_MINUTES}.")
        return
    minutes = int(raw)
    await state.update_data(price_drop_interval_minutes=minutes)
    await state.set_state(CreateLotFSM.entering_min_price)
    await message.answer(
        f"✅ Интервал: <b>{minutes} мин</b>\n\n─────────────────\n\n<b>Шаг 16/17 — Минимальная цена</b>",
        reply_markup=kb_back_cancel("lot:back:interval"),
        parse_mode="HTML",
    )


# ── Шаг 16 — Мин. цена ───────────────────────────────────────

@router.message(CreateLotFSM.entering_min_price)
async def msg_min_price(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    val = _parse_aed(message.text or "")
    if val is None:
        await message.answer(f"❌ Введите сумму в AED от {_fmt_aed(MIN_AED)}.")
        return
    data  = await state.get_data()
    start = data.get("start_price", 0)
    if val >= start:
        await message.answer(
            f"❌ Мин. цена должна быть ниже стартовой ({_fmt_aed(start)}).",
            parse_mode="HTML",
        )
        return
    await state.update_data(min_price=val)
    await state.set_state(CreateLotFSM.confirming)
    data = await state.get_data()
    data["min_price"] = val
    await message.answer(_summary_text(data), reply_markup=kb_confirm(), parse_mode="HTML")


# ── Шаг 17 — Подтверждение ───────────────────────────────────

@router.callback_query(F.data == "lot:launch", CreateLotFSM.confirming)
async def cb_launch(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    await state.clear()

    lot = await create_lot(
        created_by=callback.from_user.id,
        category=data["category"],
        emoji=data["emoji"],
        title=data["title"],
        description=data.get("description", ""),
        start_price=data["start_price"],
        bid_step=data["bid_step"],
        duration_hours=0,
        blitz_price=None,
        photo_file_id=(data.get("media_photos") or [None])[0],  # первое фото как превью
        property_type=data.get("property_type"),
        area_sqft=data.get("area_sqft"),
        floor_level=data.get("floor_level"),
        view_type=data.get("view_type"),
        parking_spots=data.get("parking_spots"),
        property_status=data.get("property_status"),
        purchase_price=data.get("purchase_price"),
        market_price=data.get("market_price"),
        discount_pct=data.get("discount_pct"),
        price_drop_interval_minutes=data.get("price_drop_interval_minutes"),
        min_price=data.get("min_price"),
    )

    # Сохранить медиа в lot_media
    media_photos    = data.get("media_photos", [])
    media_video     = data.get("media_video")
    media_video_path = data.get("media_video_path")
    if media_photos or media_video:
        await _save_lot_media(lot.id, media_photos, media_video, media_video_path)

    await _do_launch(callback, lot)
    await callback.answer()


async def _save_lot_media(lot_id: int, photos: list[str], video: Optional[str], video_path: Optional[str] = None):
    """Сохранить все медиафайлы лота в таблицу lot_media."""
    from db.database import AsyncSessionLocal, LotMedia
    async with AsyncSessionLocal() as s:
        order = 0
        for file_id in photos:
            s.add(LotMedia(lot_id=lot_id, file_id=file_id, media_type="photo", order=order))
            order += 1
        if video:
            s.add(LotMedia(
                lot_id=lot_id, file_id=video,
                file_path=video_path,  # локальный путь на диске
                media_type="video", order=order
            ))
        await s.commit()


@router.callback_query(F.data == "lot:save_draft", CreateLotFSM.confirming)
async def cb_save_draft(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    await state.clear()

    lot = await create_lot(
        created_by=callback.from_user.id,
        category=data["category"],
        emoji=data["emoji"],
        title=data["title"],
        description=data.get("description", ""),
        start_price=data["start_price"],
        bid_step=data["bid_step"],
        duration_hours=0,
        blitz_price=None,
        photo_file_id=(data.get("media_photos") or [None])[0],
        property_type=data.get("property_type"),
        area_sqft=data.get("area_sqft"),
        floor_level=data.get("floor_level"),
        view_type=data.get("view_type"),
        parking_spots=data.get("parking_spots"),
        property_status=data.get("property_status"),
        purchase_price=data.get("purchase_price"),
        market_price=data.get("market_price"),
        discount_pct=data.get("discount_pct"),
        price_drop_interval_minutes=data.get("price_drop_interval_minutes"),
        min_price=data.get("min_price"),
    )

    # Сохранить медиа
    media_photos    = data.get("media_photos", [])
    media_video     = data.get("media_video")
    media_video_path = data.get("media_video_path")
    if media_photos or media_video:
        await _save_lot_media(lot.id, media_photos, media_video, media_video_path)

    from keyboards.inline import kb_draft_actions
    await callback.message.edit_text(
        f"💾 <b>Лот сохранён как черновик</b>\n\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"{lot.emoji} <b>{lot.title}</b>\n\n"
        f"<i>Запустить можно в разделе «Активные лоты → Черновики»</i>",
        reply_markup=kb_draft_actions(lot.id),
        parse_mode="HTML",
    )
    await callback.answer("💾 Сохранено")


@router.callback_query(F.data == "lot:schedule", CreateLotFSM.confirming)
async def cb_schedule(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.set_state(CreateLotFSM.entering_schedule_time)
    await callback.message.edit_text(
        "🕐 <b>Запланировать старт аукциона</b>\n\n"
        "Введите дату и время начала:\n\n"
        "<b>Формат:</b> ДД.ММ.ГГГГ ЧЧ:ММ\n"
        "<b>Пример:</b> 20.03.2026 15:00\n\n"
        "<i>Время московское (МСК, UTC+3)</i>",
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(CreateLotFSM.entering_schedule_time)
async def msg_schedule_time(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = (message.text or "").strip()
    try:
        MSK = timezone(timedelta(hours=3))
        dt_msk = datetime.strptime(raw, "%d.%m.%Y %H:%M").replace(tzinfo=MSK)
        dt_utc = dt_msk.astimezone(timezone.utc)
        if dt_utc <= datetime.now(timezone.utc):
            await message.answer("❌ Дата должна быть в будущем. Попробуйте снова:")
            return
    except ValueError:
        await message.answer(
            "❌ Неверный формат. Используйте: <b>ДД.ММ.ГГГГ ЧЧ:ММ</b>\n"
            "Например: <b>20.03.2026 15:00</b>",
            parse_mode="HTML",
        )
        return

    await state.update_data(schedule_time=dt_utc.isoformat())

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="✅ Подтвердить", callback_data="lot:schedule_confirm"))
    b.row(InlineKeyboardButton(text="✏️ Изменить время", callback_data="lot:schedule"))
    b.row(InlineKeyboardButton(text="← Назад", callback_data="lot:back_to_confirm"))

    await message.answer(
        f"🕐 <b>Аукцион будет запущен:</b>\n\n"
        f"📅 <b>{raw} МСК</b>\n\n"
        f"Подтвердить?",
        reply_markup=b.as_markup(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "lot:schedule_confirm")
async def cb_schedule_confirm(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    data = await state.get_data()
    await state.clear()

    schedule_time = datetime.fromisoformat(data["schedule_time"])

    lot = await create_lot(
        created_by=callback.from_user.id,
        category=data["category"],
        emoji=data["emoji"],
        title=data["title"],
        description=data.get("description", ""),
        start_price=data["start_price"],
        bid_step=data["bid_step"],
        duration_hours=0,
        blitz_price=None,
        photo_file_id=(data.get("media_photos") or [None])[0],
        property_type=data.get("property_type"),
        area_sqft=data.get("area_sqft"),
        floor_level=data.get("floor_level"),
        view_type=data.get("view_type"),
        parking_spots=data.get("parking_spots"),
        property_status=data.get("property_status"),
        purchase_price=data.get("purchase_price"),
        market_price=data.get("market_price"),
        discount_pct=data.get("discount_pct"),
        price_drop_interval_minutes=data.get("price_drop_interval_minutes"),
        min_price=data.get("min_price"),
    )

    # Сохранить медиа
    media_photos     = data.get("media_photos", [])
    media_video      = data.get("media_video")
    media_video_path = data.get("media_video_path")
    if media_photos or media_video:
        await _save_lot_media(lot.id, media_photos, media_video, media_video_path)

    # Запланировать старт
    from db.queries import schedule_lot as db_schedule_lot
    await db_schedule_lot(lot.id, topic_id=0, starts_at=schedule_time)
    from utils.scheduler import schedule_lot_start
    schedule_lot_start(lot.id, schedule_time, callback.bot)

    MSK = timezone(timedelta(hours=3))
    dt_msk = schedule_time.astimezone(MSK).strftime("%d.%m.%Y в %H:%M МСК")

    from keyboards.inline import kb_monitor
    await callback.message.edit_text(
        f"🕐 <b>Аукцион запланирован!</b>\n\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"{lot.emoji} <b>{lot.title}</b>\n"
        f"📅 Старт: <b>{dt_msk}</b>\n"
        f"Старт цена: <b>{_fmt_aed(lot.start_price)}</b>\n"
        f"Шаг: {_fmt_aed(lot.bid_step)} / {lot.price_drop_interval_minutes} мин",
        reply_markup=kb_monitor(lot.id),
        parse_mode="HTML",
    )
    await callback.answer("🕐 Запланирован")


@router.callback_query(F.data == "lot:back_to_confirm")
async def cb_back_to_confirm(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.set_state(CreateLotFSM.confirming)
    data = await state.get_data()
    await callback.message.edit_text(
        _summary_text(data), reply_markup=kb_confirm(), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "lot:edit")
async def cb_edit(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.clear()
    await state.update_data(
        emoji=DEFAULT_EMOJI, category=DEFAULT_CATEGORY,
        media_photos=[], media_video=None,
    )
    await state.set_state(CreateLotFSM.entering_title)
    await callback.message.edit_text(
        "➕ <b>Создание лота — шаг 1/17</b>\n\nВведите <b>название объекта</b>:",
        parse_mode="HTML",
    )
    await callback.answer()


async def _do_launch(callback, lot):
    from datetime import datetime, timezone
    from db.queries import launch_lot
    from keyboards.inline import kb_monitor
    from utils.scheduler import schedule_dutch_drop

    lot = await launch_lot(lot.id, topic_id=0, ends_at=None)
    if lot.price_drop_interval_minutes:
        schedule_dutch_drop(lot.id, lot.price_drop_interval_minutes, callback.bot)

    text = (
        f"🚀 <b>Dutch-аукцион запущен!</b>\n\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"{lot.emoji} <b>{lot.title}</b>\n"
        f"Тип: {lot.property_type}  ·  {lot.area_sqft:,} sqft\n"
        f"Старт: <b>{_fmt_aed(lot.start_price)}</b>\n"
        f"Шаг: {_fmt_aed(lot.bid_step)} / {lot.price_drop_interval_minutes} мин\n\n"
        f"<i>Лот опубликован в Mini App 📱</i>"
    )
    await callback.message.edit_text(text, reply_markup=kb_monitor(lot.id), parse_mode="HTML")
