import texts as T
from datetime import datetime, timezone, timedelta
from typing import Optional

from db.database import Bid, Lot


# ── Базовые форматтеры ────────────────────────────────────────

def fmt_price(amount: int) -> str:
    """Рублёвый формат (используется в старых местах)."""
    return f"₽\u00A0{amount:,}".replace(",", "\u202F")


def fmt_aed(amount: int) -> str:
    """Форматировать сумму в AED."""
    return f"AED {amount:,}".replace(",", " ")


def fmt_time_left(ends_at: Optional[datetime]) -> str:
    if not ends_at:
        return "—"
    now = datetime.now(timezone.utc)
    if ends_at.tzinfo is None:
        ends_at = ends_at.replace(tzinfo=timezone.utc)
    diff = ends_at - now
    if diff.total_seconds() <= 0:
        return "истёк"
    total = int(diff.total_seconds())
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h}ч {m:02d}м {s:02d}с"


def fmt_duration(hours: float) -> str:
    total_minutes = round(hours * 60)
    if total_minutes < 60:
        return f"{total_minutes} мин"
    h = total_minutes // 60
    m = total_minutes % 60
    if h < 24:
        return f"{h}ч {m}м" if m else f"{h} ч"
    days = h // 24
    rem_h = h % 24
    return f"{days}д {rem_h}ч" if rem_h else f"{days} д"


# ── Карточка лота (недвижимость) ──────────────────────────────

def lot_card_text(lot: Lot, bid_count: int, top_bid: Optional[Bid] = None) -> str:
    """Карточка лота для топика / мониторинга."""
    leader = (
        f"@{top_bid.username}" if (top_bid and top_bid.username)
        else f"id{top_bid.user_id}" if top_bid
        else "нет покупателя"
    )

    # Строки с полями недвижимости
    prop_line = ""
    if lot.property_type:
        prop_line += f"🏠 {lot.property_type}"
    if lot.area_sqft:
        prop_line += f"  ·  {lot.area_sqft:,} sqft"
    if lot.floor_level:
        prop_line += f"  ·  {lot.floor_level} floor"

    detail_line = ""
    if lot.view_type:
        detail_line += f"🌅 {lot.view_type}"
    if lot.parking_spots is not None:
        detail_line += f"  ·  🅿️ {lot.parking_spots}"
    if lot.property_status:
        st_emoji = "🟢" if lot.property_status == "Vacant" else "🔴"
        detail_line += f"  ·  {st_emoji} {lot.property_status}"

    price_section = ""
    if lot.purchase_price:
        price_section += f"💵 Куплено за: {fmt_aed(lot.purchase_price)}\n"
    if lot.market_price:
        price_section += f"📊 Рынок: {fmt_aed(lot.market_price)}\n"
    if lot.discount_pct:
        price_section += f"📉 Скидка: {lot.discount_pct}%\n"

    dutch_section = ""
    if lot.price_drop_interval_minutes:
        dutch_section += f"⏱ Снижение: {fmt_aed(lot.bid_step)} / {lot.price_drop_interval_minutes} мин\n"
    if lot.min_price:
        dutch_section += f"🔻 Мин. цена: {fmt_aed(lot.min_price)}\n"

    return (
        f"{lot.emoji} <b>{lot.title}</b>\n"
        f"<code>{lot.lot_code}</code>  ·  Топик #{lot.topic_id}\n"
        f"\n{prop_line}\n"
        f"{detail_line}\n\n"
        f"📋 {lot.description or '—'}\n\n"
        f"{price_section}"
        f"\n💰 Текущая цена: <b>{fmt_aed(lot.current_price)}</b>\n"
        f"👤 Лидер: {leader}\n"
        f"{dutch_section}"
        f"🔢 Ставок: {bid_count}"
    )


# ── Мониторинг (Dutch) ────────────────────────────────────────

def monitor_text(lot: Lot, bid_count: int, user_count: int,
                 top_bid: Optional[Bid], recent: list[Bid]) -> str:
    leader = (
        f"@{top_bid.username}" if (top_bid and top_bid.username)
        else f"id{top_bid.user_id}" if top_bid
        else "нет покупателя"
    )
    status_emoji = {
        "active": "🟢", "finished": "✅",
        "cancelled": "🚫", "paused": "⏸", "scheduled": "🕐"
    }.get(lot.status, "❓")

    if lot.status == "scheduled" and lot.starts_at:
        starts = lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc)
        msk = starts.astimezone(timezone(timedelta(hours=3)))
        time_line = f"🕐 Начало: {msk.strftime('%d.%m в %H:%M')} МСК"
    elif lot.ends_at:
        time_line = f"⏱ Осталось: {fmt_time_left(lot.ends_at)}"
    else:
        time_line = "⏱ Dutch-режим (без таймера)"

    feed = ""
    for b in recent:
        name = f"@{b.username}" if b.username else f"id{b.user_id}"
        feed += f"\n  {name} → {fmt_aed(b.amount)}"

    prop_line = ""
    if lot.property_type:
        prop_line = f"Тип: {lot.property_type}"
        if lot.area_sqft:
            prop_line += f"  ·  {lot.area_sqft:,} sqft"

    dutch_line = ""
    if lot.price_drop_interval_minutes:
        dutch_line = (
            f"📉 Снижение: {fmt_aed(lot.bid_step)} / {lot.price_drop_interval_minutes} мин\n"
        )
    min_line = f"🔻 Мин. цена: {fmt_aed(lot.min_price)}\n" if lot.min_price else ""

    return (
        f"{status_emoji} <b>Мониторинг · {lot.emoji} {lot.title}</b>\n"
        f"<code>{lot.lot_code}</code>\n"
        f"{prop_line}\n\n"
        f"💰 Цена: <b>{fmt_aed(lot.current_price)}</b>\n"
        f"👤 Лидер: {leader}\n"
        f"{time_line}\n"
        f"{dutch_line}"
        f"{min_line}"
        f"📊 Ставок: {bid_count}  ·  Участников: {user_count}\n"
        f"\n<b>Последние ставки:</b>{feed if feed else ' —'}"
    )


# ── Итог аукциона ─────────────────────────────────────────────

def winner_text(lot: Lot, bid_count: int, user_count: int) -> str:
    no_winner = not lot.winner_user_id or lot.winner_user_id == 0
    if no_winner:
        return (
            f"📭 <b>АУКЦИОН ЗАВЕРШЁН БЕЗ СТАВОК</b>\n\n"
            f"{lot.emoji} {lot.title}\n"
            f"<code>{lot.lot_code}</code>\n\n"
            f"Победитель не определён.\n"
            f"🔢 Ставок: {bid_count}"
        )
    winner = f"@{lot.winner_username}" if lot.winner_username else f"id{lot.winner_user_id}"
    growth = 0
    if lot.purchase_price and lot.final_price:
        growth = round((lot.final_price / lot.purchase_price - 1) * 100)
    return (
        f"🏆 <b>АУКЦИОН ЗАВЕРШЁН</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"🥇 Победитель: <b>{winner}</b>\n"
        f"💰 Финальная цена: <b>{fmt_aed(lot.final_price or 0)}</b>\n"
        f"📈 Старт: {fmt_aed(lot.start_price)}  ·  +{growth}% к покупке\n"
        f"🔢 Ставок: {bid_count}  ·  Участников: {user_count}"
    )


def report_text(lot: Lot, bid_count: int, user_count: int) -> str:
    sold = bool(
        (lot.winner_user_id and lot.winner_user_id != 0)
        or (lot.final_price and lot.status in ("finished",))
    )
    winner_str = (
        f"@{lot.winner_username}" if lot.winner_username
        else f"id{lot.winner_user_id}" if sold
        else None
    )
    final_discount = None
    if lot.market_price and lot.final_price:
        final_discount = round((1 - lot.final_price / lot.market_price) * 100)
    drop_from_start = None
    if lot.final_price and lot.start_price and lot.final_price < lot.start_price:
        drop_from_start = fmt_aed(lot.start_price - lot.final_price)

    # Объект
    obj = f"• {lot.emoji} {lot.title}\n"
    if lot.property_type:
        area = f"{lot.area_sqft:,} sqft" if lot.area_sqft else "—"
        obj += f"• {lot.property_type}  ·  {area}\n"
    if lot.floor_level:
        obj += f"• {lot.floor_level} floor  ·  {lot.view_type}\n"
    if lot.parking_spots is not None:
        obj += f"• Парковка: {lot.parking_spots}  ·  {lot.property_status}\n"

    # Параметры
    params = ""
    if lot.purchase_price:
        params += f"• Цена покупки: {fmt_aed(lot.purchase_price)}\n"
    if lot.market_price:
        params += f"• Рыночная: {fmt_aed(lot.market_price)}\n"
    if lot.discount_pct:
        params += f"• Скидка к рынку: {lot.discount_pct}%\n"
    params += f"• Старт: {fmt_aed(lot.start_price)}\n"
    params += f"• Шаг: {fmt_aed(lot.bid_step)} / {lot.price_drop_interval_minutes} мин\n"

    # Итог
    if sold:
        result = f"✅ Продан за: <b>{fmt_aed(lot.final_price)}</b>\n"
        result += f"• Победитель: <b>{winner_str}</b>\n"
        if drop_from_start:
            result += f"• Снижение от старта: {drop_from_start}\n"
        if final_discount:
            result += f"• Скидка от рынка: {final_discount}%\n"
    else:
        result = "📭 Аукцион не состоялся\n"
        result += f"• Цена дошла до: {fmt_aed(lot.current_price)}\n"
        result += "• Победитель: —\\n"

    return (
        f"📊 <b>Отчёт по лоту {lot.lot_code}</b>\n\n"
        f"<b>Объект</b>\n{obj}\n"
        f"<b>Параметры аукциона</b>\n{params}\n"
        f"<b>Итог</b>\n{result}"
    )


def auction_finished_text(lot: Lot, final_price: int) -> str:
    return T.AUCTION_FINISHED.format(
        emoji=lot.emoji,
        title=lot.title,
        lot_code=lot.lot_code,
        description=lot.description or "—",
        final_price=fmt_aed(final_price),
    )


def lot_list_text(lots: list) -> str:
    if not lots:
        return "📭 <b>Активных лотов нет.</b>\n\nСледите за анонсами."
    lines = []
    for lot in lots:
        status = "🟢" if lot.status == "active" else "🕐"
        time_line = fmt_time_left(lot.ends_at) if lot.status == "active" else "ожидает"
        prop = f"{lot.property_type}  ·  " if lot.property_type else ""
        lines.append(
            f"{status} {lot.emoji} <b>{lot.title}</b>\n"
            f"   <code>{lot.lot_code}</code>  ·  {prop}{fmt_aed(lot.current_price)}  ·  ⏱ {time_line}"
        )
    return "🏷 <b>Активные аукционы</b>\n\n" + "\n\n".join(lines)


def lot_detail_text(lot: Lot, bid_count: int, user_count: int) -> str:
    prop_line = ""
    if lot.property_type:
        prop_line = (
            f"\n🏠 {lot.property_type}  ·  {lot.area_sqft or '—'} sqft\n"
            f"🏗 {lot.floor_level or '—'}  ·  🌅 {lot.view_type or '—'}\n"
            f"🅿️ {lot.parking_spots if lot.parking_spots is not None else '—'}  ·  "
            f"{'🟢' if lot.property_status == 'Vacant' else '🔴'} {lot.property_status or '—'}\n"
        )
    return (
        f"📋 <b>Детали лота {lot.lot_code}</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"{prop_line}\n"
        f"Описание:\n{lot.description or '—'}\n\n"
        f"• Стартовая цена: {fmt_aed(lot.start_price)}\n"
        f"• Текущая цена: <b>{fmt_aed(lot.current_price)}</b>\n"
        f"• Шаг снижения: {fmt_aed(lot.bid_step)}\n"
        f"• Интервал: {lot.price_drop_interval_minutes or '—'} мин\n"
        f"• Мин. цена: {fmt_aed(lot.min_price) if lot.min_price else '—'}\n"
        f"• Ставок: {bid_count}  ·  Участников: {user_count}"
    )


def bid_accepted_text(lot: Lot, amount: int, is_blitz: bool = False) -> str:
    return (
        f"✅ <b>Ставка принята!</b>\n\n"
        f"<code>{lot.lot_code}</code> · {lot.emoji} {lot.title}\n"
        f"Ваша ставка: <b>{fmt_aed(amount)}</b>\n"
        f"Вы сейчас <b>лидируете</b> 🏆\n\n"
        f"<i>Если вас перебьют — сразу уведомим в личку</i>"
    )


def overbid_notify_text(lot: Lot, new_price: int) -> str:
    return (
        f"⚠️ <b>Вашу ставку перебили!</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"Новая цена: <b>{fmt_aed(new_price)}</b>\n\n"
        f"Хотите ответить?"
    )
