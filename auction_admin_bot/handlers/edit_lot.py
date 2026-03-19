"""
handlers/edit_lot.py — редактирование полей существующего лота.
Доступно в любой момент (активный, на паузе, запланированный).
"""
from __future__ import annotations
import logging
from typing import Optional

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.queries import get_lot
from utils.guards import admin_only_callback, admin_only_message

logger = logging.getLogger(__name__)
router = Router()


class EditLotFSM(StatesGroup):
    choosing_field = State()
    entering_value = State()


# ── Клавиатуры ────────────────────────────────────────────────

def kb_edit_menu(lot_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="📝 Название",          callback_data=f"edit:{lot_id}:title"))
    b.row(InlineKeyboardButton(text="📋 Описание",          callback_data=f"edit:{lot_id}:description"))
    b.row(InlineKeyboardButton(text="🖼 Медиа",             callback_data=f"edit:{lot_id}:media"))
    b.row(
        InlineKeyboardButton(text="💰 Старт цена",          callback_data=f"edit:{lot_id}:start_price"),
        InlineKeyboardButton(text="📉 Шаг",                 callback_data=f"edit:{lot_id}:bid_step"),
    )
    b.row(
        InlineKeyboardButton(text="⏱ Интервал",             callback_data=f"edit:{lot_id}:interval"),
        InlineKeyboardButton(text="🔻 Мин. цена",           callback_data=f"edit:{lot_id}:min_price"),
    )
    b.row(InlineKeyboardButton(text="🏠 Тип",               callback_data=f"edit:{lot_id}:property_type"))
    b.row(
        InlineKeyboardButton(text="📐 Площадь",             callback_data=f"edit:{lot_id}:area_sqft"),
        InlineKeyboardButton(text="🏗 Этаж",                callback_data=f"edit:{lot_id}:floor_level"),
    )
    b.row(
        InlineKeyboardButton(text="🌅 Вид",                 callback_data=f"edit:{lot_id}:view_type"),
        InlineKeyboardButton(text="🅿️ Парковка",            callback_data=f"edit:{lot_id}:parking_spots"),
    )
    b.row(InlineKeyboardButton(text="🔑 Статус объекта",    callback_data=f"edit:{lot_id}:property_status"))
    b.row(
        InlineKeyboardButton(text="🏷 Цена покупки",        callback_data=f"edit:{lot_id}:purchase_price"),
        InlineKeyboardButton(text="📊 Рыночная",            callback_data=f"edit:{lot_id}:market_price"),
    )
    b.row(InlineKeyboardButton(text="← Назад",             callback_data=f"lot:open:{lot_id}"))
    return b.as_markup()


def kb_floor() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="⬆️ High", callback_data="editval:High"),
        InlineKeyboardButton(text="➡️ Mid",  callback_data="editval:Mid"),
        InlineKeyboardButton(text="⬇️ Low",  callback_data="editval:Low"),
    )
    return b.as_markup()


def kb_view() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="🌊 Sea",   callback_data="editval:Sea"),
        InlineKeyboardButton(text="🏙 City",  callback_data="editval:City"),
        InlineKeyboardButton(text="🏗 Facilities", callback_data="editval:Facilities"),
    )
    b.row(
        InlineKeyboardButton(text="🚫 No view",      callback_data="editval:No view"),
        InlineKeyboardButton(text="🌆 Burj Khalifa", callback_data="editval:Burj Khalifa"),
    )
    return b.as_markup()


def kb_property_type() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for t in ["1BR","2BR","3BR","4BR","5BR","6BR","7BR","8BR","9BR"]:
        b.add(InlineKeyboardButton(text=t, callback_data=f"editval:{t}"))
    b.adjust(5, 4)
    b.row(InlineKeyboardButton(text="🏢 Studio", callback_data="editval:Studio"))
    return b.as_markup()


def kb_parking() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for n in range(0, 10):
        b.add(InlineKeyboardButton(text=str(n), callback_data=f"editval:{n}"))
    b.adjust(5, 5)
    return b.as_markup()


def kb_property_status() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="🟢 Vacant",   callback_data="editval:Vacant"),
        InlineKeyboardButton(text="🔴 Tenanted", callback_data="editval:Tenanted"),
    )
    return b.as_markup()


def kb_price_step() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="10 000 AED", callback_data="editval:step:10000"),
        InlineKeyboardButton(text="25 000 AED", callback_data="editval:step:25000"),
        InlineKeyboardButton(text="50 000 AED", callback_data="editval:step:50000"),
    )
    b.row(InlineKeyboardButton(text="✏️ Свой шаг", callback_data="editval:step:custom"))
    return b.as_markup()


def kb_interval() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.row(
        InlineKeyboardButton(text="⏱ 2 мин", callback_data="editval:interval:2"),
        InlineKeyboardButton(text="⏱ 3 мин", callback_data="editval:interval:3"),
        InlineKeyboardButton(text="⏱ 5 мин", callback_data="editval:interval:5"),
    )
    b.row(InlineKeyboardButton(text="✏️ Свой интервал", callback_data="editval:interval:custom"))
    return b.as_markup()


# Описание полей
FIELD_LABELS = {
    "title":           "Название",
    "description":     "Описание",
    "media":           "Медиа",
    "start_price":     "Стартовая цена (AED)",
    "bid_step":        "Шаг снижения (AED)",
    "interval":        "Интервал снижения (мин)",
    "min_price":       "Минимальная цена (AED)",
    "property_type":   "Тип недвижимости",
    "area_sqft":       "Площадь (sqft)",
    "floor_level":     "Этаж",
    "view_type":       "Вид",
    "parking_spots":   "Парковка (мест)",
    "property_status": "Статус объекта",
    "purchase_price":  "Цена покупки (AED)",
    "market_price":    "Рыночная цена (AED)",
}

# Поля с кнопками (не текстовый ввод)
BUTTON_FIELDS = {"floor_level", "view_type", "property_type", "parking_spots",
                 "property_status", "bid_step", "interval"}
# Поля с числовым вводом
INT_FIELDS    = {"start_price", "bid_step", "min_price", "purchase_price", "market_price",
                 "area_sqft", "parking_spots", "interval"}
AED_FIELDS    = {"start_price", "min_price", "purchase_price", "market_price"}


# ── Открыть меню редактирования ───────────────────────────────

@router.callback_query(F.data.startswith("lot:edit:"))
async def cb_open_edit(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    await state.clear()
    await callback.message.edit_text(
        f"✏️ <b>Редактирование лота</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"Выберите поле для изменения:",
        reply_markup=kb_edit_menu(lot_id),
        parse_mode="HTML",
    )
    await callback.answer()


# ── Выбор поля ────────────────────────────────────────────────

@router.callback_query(F.data.startswith("edit:"))
async def cb_edit_field(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    parts  = callback.data.split(":")
    lot_id = int(parts[1])
    field  = parts[2]
    lot    = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    label = FIELD_LABELS.get(field, field)

    # Текущее значение
    current = getattr(lot, field if field != "interval" else "price_drop_interval_minutes", None)
    current_str = str(current) if current is not None else "—"

    await state.set_state(EditLotFSM.entering_value)
    await state.update_data(lot_id=lot_id, field=field)

    # Медиа — отдельная логика
    if field == "media":
        await _start_media_edit(callback, state, lot_id, lot)
        return

    # Поля с кнопками
    if field == "floor_level":
        await callback.message.edit_text(
            f"✏️ <b>{label}</b>\nТекущее: <b>{current_str}</b>",
            reply_markup=kb_floor(), parse_mode="HTML",
        )
    elif field == "view_type":
        await callback.message.edit_text(
            f"✏️ <b>{label}</b>\nТекущее: <b>{current_str}</b>",
            reply_markup=kb_view(), parse_mode="HTML",
        )
    elif field == "property_type":
        await callback.message.edit_text(
            f"✏️ <b>{label}</b>\nТекущее: <b>{current_str}</b>",
            reply_markup=kb_property_type(), parse_mode="HTML",
        )
    elif field == "parking_spots":
        await callback.message.edit_text(
            f"✏️ <b>{label}</b>\nТекущее: <b>{current_str}</b>",
            reply_markup=kb_parking(), parse_mode="HTML",
        )
    elif field == "property_status":
        await callback.message.edit_text(
            f"✏️ <b>{label}</b>\nТекущее: <b>{current_str}</b>",
            reply_markup=kb_property_status(), parse_mode="HTML",
        )
    elif field == "bid_step":
        await callback.message.edit_text(
            f"✏️ <b>{label}</b>\nТекущее: <b>AED {current_str}</b>\n\nВыберите шаг снижения:",
            reply_markup=kb_price_step(), parse_mode="HTML",
        )
    elif field == "interval":
        await callback.message.edit_text(
            f"✏️ <b>{label}</b>\nТекущее: <b>{current_str} мин</b>\n\nВыберите интервал:",
            reply_markup=kb_interval(), parse_mode="HTML",
        )
    else:
        # Текстовый ввод
        hint = " (AED)" if field in AED_FIELDS else ""
        await callback.message.edit_text(
            f"✏️ <b>{label}</b>\nТекущее: <b>{current_str}</b>\n\n"
            f"Введите новое значение{hint}:",
            parse_mode="HTML",
        )
    await callback.answer()


# ── Значение выбрано кнопкой ──────────────────────────────────

@router.callback_query(F.data.startswith("editval:"), EditLotFSM.entering_value)
async def cb_editval(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    data   = await state.get_data()
    parts  = callback.data.split(":")
    field  = data.get("field")
    lot_id = data.get("lot_id")

    # editval:step:10000 или editval:interval:2 или editval:step:custom
    if len(parts) == 3 and parts[1] in ("step", "interval"):
        val_str = parts[2]
        if val_str == "custom":
            # Переключаем в режим ввода своего значения
            hint = "шаг снижения (AED, минимум 500)" if parts[1] == "step" else "интервал (минуты, 1–60)"
            await callback.message.edit_text(
                f"✏️ Введите {hint}:",
                parse_mode="HTML",
            )
            await state.update_data(custom_input=parts[1])
            await callback.answer()
            return
        value = int(val_str)
    else:
        value = parts[1] if len(parts) == 2 else ":".join(parts[1:])
        # parking_spots — число
        if field == "parking_spots":
            value = int(value)

    await _save_field(lot_id, field, value)
    await state.clear()
    await callback.message.edit_text(
        f"✅ <b>{FIELD_LABELS.get(field, field)}</b> обновлено: <b>{value}</b>\n\n"
        f"Продолжить редактирование?",
        reply_markup=kb_edit_menu(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("✅ Сохранено")


# ── Значение введено текстом ──────────────────────────────────

@router.message(EditLotFSM.entering_value)
async def msg_edit_value(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    data   = await state.get_data()
    field  = data.get("field")
    lot_id = data.get("lot_id")

    if not field or not lot_id:
        await state.clear()
        return

    raw = (message.text or "").strip()
    label = FIELD_LABELS.get(field, field)

    # Валидация и конвертация
    value = None

    # Обработка custom ввода для step/interval
    custom = data.get("custom_input")
    if custom:
        raw2 = (message.text or "").strip().replace(" ","").replace(",","")
        if custom == "step":
            if not raw2.isdigit() or int(raw2) < 500:
                await message.answer("❌ Минимальный шаг 500 AED.")
                return
            value = int(raw2)
            await _save_field(lot_id, "bid_step", value)
        else:  # interval
            if not raw2.isdigit() or not (1 <= int(raw2) <= 60):
                await message.answer("❌ Интервал от 1 до 60 минут.")
                return
            value = int(raw2)
            await _save_field(lot_id, "price_drop_interval_minutes", value)
        await state.clear()
        label2 = "Шаг снижения" if custom == "step" else "Интервал снижения"
        await message.answer(
            f"✅ <b>{label2}</b> обновлено: <b>{value}</b>\n\nПродолжить редактирование?",
            reply_markup=kb_edit_menu(lot_id),
            parse_mode="HTML",
        )
        return

    if field == "title":
        if not (5 <= len(raw) <= 80):
            await message.answer("❌ Название от 5 до 80 символов.")
            return
        value = raw

    elif field == "description":
        if len(raw) > 500:
            await message.answer("❌ Описание не более 500 символов.")
            return
        value = raw

    elif field in AED_FIELDS:
        clean = raw.upper().replace("AED","").replace(" ","").replace(",","")
        if not clean.isdigit():
            await message.answer("❌ Введите сумму числом.")
            return
        value = int(clean)
        if value < 10_000:
            await message.answer("❌ Минимум 10 000 AED.")
            return

    elif field == "area_sqft":
        clean = raw.replace(" ","").replace(",","")
        if not clean.isdigit() or not (999 <= int(clean) <= 99_999):
            await message.answer("❌ Площадь от 999 до 99 999 sqft.")
            return
        value = int(clean)

    elif field == "interval":
        if not raw.isdigit() or not (1 <= int(raw) <= 60):
            await message.answer("❌ Интервал от 1 до 60 минут.")
            return
        value = int(raw)

    else:
        value = raw

    await _save_field(lot_id, field, value)
    await state.clear()

    await message.answer(
        f"✅ <b>{label}</b> обновлено: <b>{value}</b>\n\nПродолжить редактирование?",
        reply_markup=kb_edit_menu(lot_id),
        parse_mode="HTML",
    )


# ── Медиа: сброс и повторная загрузка ────────────────────────

async def _start_media_edit(callback: CallbackQuery, state: FSMContext, lot_id: int, lot):
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="🗑 Удалить все медиа и загрузить заново",
                               callback_data=f"edit_media_reset:{lot_id}"))
    b.row(InlineKeyboardButton(text="← Отмена", callback_data=f"lot:edit:{lot_id}"))
    await callback.message.edit_text(
        f"🖼 <b>Медиа лота</b>\n\n"
        f"Для изменения медиа нужно удалить текущие файлы и загрузить новые.\n\n"
        f"<i>Это не влияет на аукцион.</i>",
        reply_markup=b.as_markup(),
        parse_mode="HTML",
    )
    await state.clear()


@router.callback_query(F.data.startswith("edit_media_reset:"))
async def cb_media_reset(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[1])

    # Удалить все медиа из БД
    from db.database import AsyncSessionLocal, LotMedia
    from sqlalchemy import delete as sa_delete
    async with AsyncSessionLocal() as s:
        await s.execute(sa_delete(LotMedia).where(LotMedia.lot_id == lot_id))
        await s.commit()

    # Переключить в режим загрузки медиа
    await state.update_data(
        lot_id=lot_id, field="media",
        media_photos=[], media_video=None,
    )
    await state.set_state(EditLotFSM.entering_value)

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    b = InlineKeyboardBuilder()
    b.row(InlineKeyboardButton(text="✅ Готово", callback_data=f"edit_media_done:{lot_id}"))
    b.row(InlineKeyboardButton(text="← Отмена", callback_data=f"lot:edit:{lot_id}"))

    await callback.message.edit_text(
        f"🖼 <b>Загрузите новые медиафайлы</b>\n\n"
        f"Отправляйте фото (до 10) и/или видео (до 200 MB).\n"
        f"Когда готово — нажмите Готово.",
        reply_markup=b.as_markup(),
        parse_mode="HTML",
    )
    await callback.answer("Медиа удалены")


@router.message(EditLotFSM.entering_value)
async def msg_edit_media(message: Message, state: FSMContext):
    """Перехватывает фото/видео при редактировании медиа."""
    data  = await state.get_data()
    field = data.get("field")
    if field != "media":
        return  # передать дальше (обрабатывается выше)

    lot_id     = data.get("lot_id")
    photos     = list(data.get("media_photos", []))
    has_video  = bool(data.get("media_video"))

    if message.photo:
        if len(photos) >= 10:
            await message.answer("❌ Максимум 10 фото.")
            return
        photos.append(message.photo[-1].file_id)
        await state.update_data(media_photos=photos)
        await message.answer(f"📷 Фото добавлено ({len(photos)} всего)")

    elif message.video or (message.document and
         message.document.mime_type and
         message.document.mime_type.startswith("video/")):
        if has_video:
            await message.answer("❌ Видео уже загружено.")
            return
        file_obj = message.video or message.document
        file_id  = file_obj.file_id

        MAX_VIDEO_BYTES = 200 * 1024 * 1024
        if file_obj.file_size and file_obj.file_size > MAX_VIDEO_BYTES:
            await message.answer("❌ Видео слишком большое. Максимум 200 MB.")
            return

        wait_msg = await message.answer("⏳ Скачиваю видео...")
        try:
            from pathlib import Path
            import os
            VIDEOS_DIR = Path(os.getenv("VIDEOS_DIR", "./videos"))
            VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
            safe_name = file_id.replace("/", "_").replace("\\", "_")[:50]
            dest = VIDEOS_DIR / f"{safe_name}.mp4"
            if not dest.exists():
                file = await message.bot.get_file(file_id)
                await message.bot.download_file(file.file_path, destination=str(dest))
            await state.update_data(media_video=file_id, media_video_path=str(dest))
            size_mb = (file_obj.file_size or 0) // (1024 * 1024)
            await wait_msg.edit_text(f"✅ Видео загружено ({size_mb} MB)")
        except Exception as e:
            logger.error(f"Video download in edit failed: {e}")
            await wait_msg.edit_text("❌ Не удалось скачать видео.")
    else:
        await message.answer("❌ Отправьте фото или видео.")


@router.callback_query(F.data.startswith("edit_media_done:"))
async def cb_media_done(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[1])
    data   = await state.get_data()
    photos = data.get("media_photos", [])
    video  = data.get("media_video")
    video_path = data.get("media_video_path")

    if not photos and not video:
        await callback.answer("Добавьте хотя бы одно фото или видео.", show_alert=True)
        return

    # Сохранить в lot_media
    from db.database import AsyncSessionLocal, LotMedia
    async with AsyncSessionLocal() as s:
        order = 0
        for fid in photos:
            s.add(LotMedia(lot_id=lot_id, file_id=fid, media_type="photo", order=order))
            order += 1
        if video:
            s.add(LotMedia(lot_id=lot_id, file_id=video,
                           file_path=video_path, media_type="video", order=order))
        await s.commit()

    # Обновить photo_file_id лота (первое фото как превью)
    if photos:
        from sqlalchemy import update as sa_update
        from db.database import Lot as LotModel
        async with AsyncSessionLocal() as s:
            await s.execute(
                sa_update(LotModel).where(LotModel.id == lot_id)
                .values(photo_file_id=photos[0])
            )
            await s.commit()

    await state.clear()
    parts = []
    if photos: parts.append(f"📷 {len(photos)} фото")
    if video:  parts.append("🎥 видео")

    await callback.message.edit_text(
        f"✅ Медиа обновлено: {', '.join(parts)}\n\nПродолжить редактирование?",
        reply_markup=kb_edit_menu(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("✅ Сохранено")


# ── Сохранение поля в БД ──────────────────────────────────────

async def _save_field(lot_id: int, field: str, value):
    from sqlalchemy import update as sa_update
    from db.database import AsyncSessionLocal, Lot as LotModel

    # Маппинг field → column
    db_field = "price_drop_interval_minutes" if field == "interval" else field

    async with AsyncSessionLocal() as s:
        await s.execute(
            sa_update(LotModel)
            .where(LotModel.id == lot_id)
            .values(**{db_field: value})
        )
        await s.commit()
    logger.info(f"Lot {lot_id} field '{db_field}' updated to {value!r}")
