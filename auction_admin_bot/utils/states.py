from aiogram.fsm.state import State, StatesGroup


class CreateLotFSM(StatesGroup):
    # Шаг 1 — Название
    entering_title = State()
    # Шаг 2 — Описание
    entering_description = State()
    # Шаг 3 — Медиа (фото/видео)
    uploading_media = State()
    # Шаг 4 — Тип (кнопки: 1BR–9BR, Studio)
    choosing_type = State()
    # Шаг 5 — Площадь (sqft, текст)
    entering_area = State()
    # Шаг 6 — Этаж (кнопки: High/Mid/Low)
    choosing_floor = State()
    # Шаг 7 — Вид (кнопки: Sea/City/Facilities/No view/Burj Khalifa)
    choosing_view = State()
    # Шаг 8 — Парковка (кнопки: 0–9)
    choosing_parking = State()
    # Шаг 9 — Статус (кнопки: Vacant/Tenanted)
    choosing_status = State()
    # Шаг 10 — Original Purchase Price (AED, текст)
    entering_purchase_price = State()
    # Шаг 11 — Current Market Price (AED, текст)
    entering_market_price = State()
    # Шаг 12 — Auction Start Price (AED, текст)
    entering_start_price = State()
    # Шаг 13 — Discount to Market (%, текст — вводит вручную)
    entering_discount = State()
    # Шаг 14 — Шаг снижения цены (кнопки или текст)
    choosing_price_step = State()
    entering_price_step = State()
    # Шаг 15 — Интервал снижения (кнопки или текст)
    choosing_interval = State()
    entering_interval = State()
    # Шаг 16 — Минимальная цена (AED, текст)
    entering_min_price = State()
    # Шаг 17 — Подтверждение
    confirming = State()
    # Ввод времени запланированного старта
    entering_schedule_time = State()


class BanFSM(StatesGroup):
    choosing_user = State()
    confirming = State()


class ExtendFSM(StatesGroup):
    choosing_hours = State()


class CustomBidFSM(StatesGroup):
    waiting_for_amount = State()
