from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS, MIN_BID_STEP
from db.queries import create_lot
from keyboards.inline import (
    kb_bid_step, kb_confirm_lot,
    kb_duration, kb_main_menu,
)
from utils.formatting import fmt_price
from utils.guards import admin_only_callback, admin_only_message
from utils.states import CreateLotFSM

router = Router()

# Фиксированная категория
DEFAULT_EMOJI = "🏷"
DEFAULT_CATEGORY = "Аукцион"


# ── Entry point ───────────────────────────────────────────────

@router.callback_query(F.data == "menu:create")
async def cb_create_start(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.clear()
    await state.update_data(emoji=DEFAULT_EMOJI, category=DEFAULT_CATEGORY)
    await state.set_state(CreateLotFSM.entering_title)
    await callback.message.edit_text(
        "➕ <b>Создание лота</b>\n\nВведите <b>название лота</b>:",
        parse_mode="HTML",
    )
    await callback.answer()


# ── Title ─────────────────────────────────────────────────────

@router.message(CreateLotFSM.entering_title)
async def msg_title(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    title = message.text.strip()
    if len(title) < 3:
        await message.answer("Название слишком короткое. Введите минимум 3 символа.")
        return
    await state.update_data(title=title)
    await state.set_state(CreateLotFSM.entering_price)
    await message.answer(
        f"Название: <b>{title}</b> ✅\n\nУкажите <b>стартовую цену</b> (₽):",
        parse_mode="HTML",
    )


# ── Start price ───────────────────────────────────────────────

@router.message(CreateLotFSM.entering_price)
async def msg_price(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = message.text.strip().replace(" ", "").replace("\u202f", "")
    if not raw.isdigit() or int(raw) < 1000:
        await message.answer("Введите корректную цену от 1 000 ₽")
        return
    price = int(raw)
    await state.update_data(start_price=price)
    await state.set_state(CreateLotFSM.choosing_step)
    await message.answer(
        f"Старт: <b>{fmt_price(price)}</b> ✅\n\nВыберите <b>шаг ставки</b>:",
        reply_markup=kb_bid_step(),
        parse_mode="HTML",
    )


# ── Bid step — preset buttons ─────────────────────────────────

@router.callback_query(F.data.startswith("step:"), CreateLotFSM.choosing_step)
async def cb_step(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    value = callback.data.split(":")[1]
    if value == "custom":
        await state.set_state(CreateLotFSM.entering_step)
        await callback.message.edit_text(
            "Введите шаг ставки (₽), минимум 500:",
            parse_mode="HTML",
        )
    else:
        step = int(value)
        await state.update_data(bid_step=step)
        await state.set_state(CreateLotFSM.choosing_duration)
        await callback.message.edit_text(
            f"Шаг: <b>{fmt_price(step)}</b> ✅\n\nВыберите <b>длительность</b> аукциона:",
            reply_markup=kb_duration(),
            parse_mode="HTML",
        )
    await callback.answer()


# ── Bid step — custom text ────────────────────────────────────

@router.message(CreateLotFSM.entering_step)
async def msg_step(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = message.text.strip().replace(" ", "")
    if not raw.isdigit() or int(raw) < MIN_BID_STEP:
        await message.answer(f"Минимальный шаг — {MIN_BID_STEP:,} ₽")
        return
    step = int(raw)
    await state.update_data(bid_step=step)
    await state.set_state(CreateLotFSM.choosing_duration)
    await message.answer(
        f"Шаг: <b>{fmt_price(step)}</b> ✅\n\nВыберите <b>длительность</b> аукциона:",
        reply_markup=kb_duration(),
        parse_mode="HTML",
    )


# ── Duration ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("dur:"), CreateLotFSM.choosing_duration)
async def cb_duration(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    hours = int(callback.data.split(":")[1])
    await state.update_data(duration_hours=hours, blitz_price=None)
    await state.set_state(CreateLotFSM.entering_desc)
    await callback.message.edit_text(
        f"Длительность: <b>{hours}ч</b> ✅\n\nДобавьте краткое <b>описание</b> лота:",
        parse_mode="HTML",
    )
    await callback.answer()


# ── Description ───────────────────────────────────────────────

@router.message(CreateLotFSM.entering_desc)
async def msg_desc(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    desc = message.text.strip()
    await state.update_data(description=desc)
    await state.set_state(CreateLotFSM.uploading_photo)
    await message.answer(
        "📸 Отправьте <b>фото лота</b>.\n\n"
        "Или нажмите /skip чтобы пропустить.",
        parse_mode="HTML",
    )


# ── Photo ──────────────────────────────────────────────────────

@router.message(CreateLotFSM.uploading_photo)
async def msg_photo(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return

    if message.text and message.text.strip() == "/skip":
        await state.update_data(photo_file_id=None)
    elif message.photo:
        file_id = message.photo[-1].file_id  # берём максимальное разрешение
        await state.update_data(photo_file_id=file_id)
    else:
        await message.answer(
            "Пожалуйста, отправьте фото или напишите /skip чтобы пропустить.",
        )
        return

    await state.set_state(CreateLotFSM.choosing_start_time)
    from keyboards.inline import kb_start_time
    await message.answer("🕐 Когда начать аукцион?", reply_markup=kb_start_time())


# ── Start time ─────────────────────────────────────────────────

@router.callback_query(F.data == "start:now", CreateLotFSM.choosing_start_time)
async def cb_start_now(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.update_data(starts_at=None)
    await state.set_state(CreateLotFSM.confirming)
    data = await state.get_data()
    await _show_confirm(callback.message, data, edit=True)
    await callback.answer()


@router.callback_query(F.data == "start:custom", CreateLotFSM.choosing_start_time)
async def cb_start_custom(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.set_state(CreateLotFSM.entering_start_time)
    text = (
        "🕐 Введите время начала аукциона по МСК в формате:\n\n"
        "<code>ДД.ММ ЧЧ:ММ</code>\n\n"
        "Например: <code>25.03 15:00</code>"
    )
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML")
    else:
        await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


@router.message(CreateLotFSM.entering_start_time)
async def msg_start_time(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    from datetime import datetime, timezone, timedelta
    import re
    raw = (message.text or "").strip()
    # Парсим "ДД.ММ ЧЧ:ММ"
    m = re.match(r"^(\d{1,2})\.(\d{1,2})\s+(\d{1,2}):(\d{2})$", raw)
    if not m:
        await message.answer(
            "Неверный формат. Введите дату и время так:\n"
            "<code>25.03 15:00</code>",
            parse_mode="HTML",
        )
        return
    day, month, hour, minute = int(m[1]), int(m[2]), int(m[3]), int(m[4])
    now_msk = datetime.now(timezone(timedelta(hours=3)))
    year = now_msk.year
    try:
        msk = datetime(year, month, day, hour, minute,
                       tzinfo=timezone(timedelta(hours=3)))
        # Если дата уже прошла — берём следующий год
        if msk <= now_msk:
            msk = msk.replace(year=year + 1)
    except ValueError:
        await message.answer("Неверная дата. Проверьте день и месяц.")
        return

    utc = msk.astimezone(timezone.utc)
    await state.update_data(starts_at=utc.isoformat())
    await state.set_state(CreateLotFSM.confirming)
    data = await state.get_data()
    await message.answer(
        f"🕐 Начало: <b>{msk.strftime('%d.%m в %H:%M')} МСК</b> ✅",
        parse_mode="HTML",
    )
    await _show_confirm(message, data)


async def _show_confirm(target, data: dict, edit: bool = False):
    from datetime import datetime, timezone, timedelta
    photo = data.get("photo_file_id")
    starts_at_iso = data.get("starts_at")
    if starts_at_iso:
        dt_utc = datetime.fromisoformat(starts_at_iso)
        dt_msk = dt_utc.astimezone(timezone(timedelta(hours=3)))
        start_line = f"• Начало: <b>{dt_msk.strftime('%d.%m в %H:%M')} МСК</b>\n"
    else:
        start_line = "• Начало: <b>сразу после запуска</b>\n"

    text = (
        f"✅ <b>Проверьте данные лота</b>\n\n"
        f"• Название: <b>{data['emoji']} {data['title']}</b>\n"
        f"• Описание: {data.get('description', '—')}\n"
        f"• Фото: {'✅' if photo else '—'}\n"
        f"{start_line}"
        f"• Стартовая цена: <b>{fmt_price(data['start_price'])}</b>\n"
        f"• Шаг ставки: {fmt_price(data['bid_step'])}\n"
        f"• Длительность: {data['duration_hours']}ч"
    )
    kb = kb_confirm_lot()
    if edit:
        if getattr(target, "photo", None):
            await target.edit_caption(caption=text, reply_markup=kb, parse_mode="HTML")
        else:
            await target.edit_text(text, reply_markup=kb, parse_mode="HTML")
        return
    if photo:
        send = getattr(target, "answer_photo", None)
        if send:
            await send(photo=photo, caption=text, reply_markup=kb, parse_mode="HTML")
            return
    send = getattr(target, "answer", None) or getattr(target, "edit_text", None)
    await send(text, reply_markup=kb, parse_mode="HTML")


# ── Confirm → Launch ──────────────────────────────────────────

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
        duration_hours=data["duration_hours"],
        blitz_price=None,
        photo_file_id=data.get("photo_file_id"),
    )

    from keyboards.inline import kb_back_to_main
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="🔗 Привязать топик и запустить",
        callback_data=f"lot:bind_topic:{lot.id}"
    ))
    builder.row(InlineKeyboardButton(text="← Главное меню", callback_data="menu:main"))

    text = (
        f"✅ <b>Лот создан!</b>  <code>{lot.lot_code}</code>\n\n"
        f"{lot.emoji} <b>{lot.title}</b>\n\n"
        f"Теперь <b>перешлите любое сообщение из нужного топика</b> — "
        f"бот определит ID топика и запустит аукцион.\n\n"
        f"<i>Или нажмите кнопку ниже если ID топика вам известен.</i>"
    )
    kb = builder.as_markup()
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, reply_markup=kb, parse_mode="HTML")
    else:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()

    await state.update_data(pending_lot_id=lot.id, starts_at=data.get("starts_at"))


@router.callback_query(F.data == "lot:edit")
async def cb_edit(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    await state.clear()
    await state.update_data(emoji=DEFAULT_EMOJI, category=DEFAULT_CATEGORY)
    await state.set_state(CreateLotFSM.entering_title)
    text = "➕ <b>Создание лота</b>\n\nВведите <b>название лота</b>:"
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML")
    else:
        await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


# ── Topic binding ─────────────────────────────────────────────

@router.callback_query(F.data.startswith("lot:bind_topic:"))
async def cb_bind_topic_prompt(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await state.update_data(pending_lot_id=lot_id)
    await state.set_state(CreateLotFSM.entering_topic_id)

    text = (
        "📌 <b>Привяжите топик группы</b>\n\n"
        "Введите <b>числовой ID топика</b> (message_thread_id).\n\n"
        "<b>Как узнать ID:</b>\n"
        "1. Откройте группу в Telegram Web (web.telegram.org)\n"
        "2. Перейдите в нужный топик\n"
        "3. В адресной строке будет: <code>...?thread=<b>12345</b></code>\n"
        "   — это и есть ID топика\n\n"
        "<i>Либо напишите боту из топика — он определит ID автоматически.</i>"
    )
    if callback.message.photo:
        await callback.message.edit_caption(caption=text, parse_mode="HTML")
    else:
        await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


@router.message(CreateLotFSM.entering_topic_id)
async def msg_topic_id_input(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    data = await state.get_data()
    lot_id = data.get("pending_lot_id")
    starts_at_iso = data.get("starts_at")
    if not lot_id:
        await message.answer("Что-то пошло не так. Начните создание лота заново /start")
        return

    if message.message_thread_id:
        topic_id = message.message_thread_id
        await message.answer(
            f"✅ Топик определён автоматически: <code>#{topic_id}</code>",
            parse_mode="HTML",
        )
        await _do_launch(message, state, lot_id, topic_id, starts_at_iso)
        return

    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer(
            "Введите <b>только число</b> — ID топика.\n"
            "Пример: <code>12345</code>",
            parse_mode="HTML",
        )
        return

    topic_id = int(raw)
    await _do_launch(message, state, lot_id, topic_id, starts_at_iso)


async def _do_launch(target, state: FSMContext, lot_id: int, topic_id: int, starts_at_iso: str = None):
    from datetime import datetime, timedelta, timezone
    from db.queries import get_lot, launch_lot, schedule_lot
    from utils.scheduler import schedule_auction_finish, schedule_lot_start
    from utils.formatting import fmt_price
    from keyboards.inline import kb_monitor
    import logging
    logger = logging.getLogger(__name__)

    bot = target.bot if hasattr(target, "bot") else None
    if bot is None:
        from aiogram import Bot
        bot = Bot.get_current()

    lot = await get_lot(lot_id)
    if not lot:
        return

    logger.info(f"_do_launch: lot_id={lot_id}, topic_id={topic_id}, starts_at_iso={starts_at_iso!r}")

    if starts_at_iso:
        starts_at = datetime.fromisoformat(starts_at_iso)
        lot = await schedule_lot(lot_id, topic_id, starts_at)
        schedule_lot_start(lot_id, starts_at, bot)

        msk = starts_at.astimezone(timezone(timedelta(hours=3)))
        reply_text = (
            f"🕐 <b>Аукцион запланирован!</b>\n\n"
            f"<code>{lot.lot_code}</code>  ·  Топик <b>#{topic_id}</b>\n\n"
            f"{lot.emoji} <b>{lot.title}</b>\n"
            f"Старт: <b>{msk.strftime('%d.%m в %H:%M')} МСК</b>\n"
            f"Длительность: {lot.duration_hours}ч\n\n"
            f"<i>Карточка уже опубликована в топике</i>"
        )
    else:
        ends_at = datetime.now(timezone.utc) + timedelta(hours=lot.duration_hours)
        lot = await launch_lot(lot_id, topic_id, ends_at)
        schedule_auction_finish(lot_id, ends_at, bot)
        reply_text = (
            f"🚀 <b>Аукцион запущен!</b>\n\n"
            f"<code>{lot.lot_code}</code>  ·  Топик <b>#{topic_id}</b>\n\n"
            f"{lot.emoji} <b>{lot.title}</b>\n"
            f"Старт: <b>{fmt_price(lot.start_price)}</b>\n"
            f"Длительность: {lot.duration_hours}ч\n\n"
            f"<i>Участники уведомлены 🔔</i>"
        )

    await state.clear()
    send_fn = getattr(target, "answer", None)
    await send_fn(reply_text, reply_markup=kb_monitor(lot_id), parse_mode="HTML")

