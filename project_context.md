# PROJECT STRUCTURE
```text
    README.md
    ngrok.yml
    requirements.txt
    run.py
    texts.py
    auction_admin_bot/
        README.md
        bot.py
        config.py
        requirements.txt
        db/
            __init__.py
            database.py
            queries.py
        handlers/
            __init__.py
            bidding.py
            create_lot.py
            finish.py
            lots.py
            main_menu.py
            manage.py
            monitor.py
            notifications.py
            welcome.py
        keyboards/
            inline.py
        utils/
            __init__.py
            formatting.py
            guards.py
            scheduler.py
            states.py
    auction_group_bot/
        README.md
        bot.py
        config.py
        requirements.txt
        db/
            __init__.py
            database.py
            queries.py
        handlers/
            __init__.py
            bidding.py
            create_lot.py
            finish.py
            lots.py
            main_menu.py
            manage.py
            monitor.py
            notifications.py
            welcome.py
        keyboards/
            __init__.py
            inline.py
        utils/
            __init__.py
            formatting.py
            guards.py
            scheduler.py
            states.py
    miniapp/
        README.md
        backend/
            database.py
            main.py
            requirements.txt
        frontend/
            package-lock.json
            package.json
            public/
                index.html
            src/
                index.css
                index.js
                components/
                hooks/
                    useTelegram.js
                    useTimer.js
                pages/
                utils/
                    api.js
                    format.js
```

## File: README.md
```markdown
# Auction Bot + Mini App — Локальный запуск из PyCharm

## Структура проекта

```
auction/
├── auction_admin_bot/      ← Административный бот (управление лотами)
├── auction_group_bot/      ← Клиентский бот (уведомления, ставки через Telegram)
├── miniapp/
│   ├── backend/            ← FastAPI API для Mini App
│   └── frontend/           ← React Mini App (UI)
├── texts.py                ← Общие тексты (shared между ботами)
└── requirements.txt        ← Общие зависимости
```

---

## Требования

| Инструмент | Версия | Зачем |
|---|---|---|
| Python | 3.11+ | Боты и бэкенд |
| Node.js | 18+ | React фронтенд |
| PyCharm | любая | IDE |
| Git | любая | Опционально |

> **БД для локальной разработки:** SQLite (файл `auction.db` в папке каждого бота).
> Не нужно устанавливать PostgreSQL или Redis.

---

## Шаг 1 — Создать токены ботов

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте **первого бота** — это будет `auction_admin_bot`:
   ```
   /newbot → введите имя → получите токен: 1234567890:AAxxxxxxx
   ```
3. Создайте **второго бота** — это будет `auction_group_bot`:
   ```
   /newbot → введите имя → получите токен: 9876543210:AAxxxxxxx
   ```
4. Узнайте свой **Telegram user_id**: напишите [@userinfobot](https://t.me/userinfobot)
   — он ответит вашим ID, например `123456789`

---

## Шаг 2 — Открыть проект в PyCharm

1. **File → Open** → выберите папку `auction/`
2. PyCharm предложит создать Virtual Environment — соглашайтесь
   (или сделайте вручную: **File → Settings → Python Interpreter → Add**)

---

## Шаг 3 — Установить зависимости Python

### Вариант A — через PyCharm Terminal

Откройте **Terminal** (Alt+F12) в PyCharm и выполните:

```bash
# Зависимости admin бота
pip install -r auction_admin_bot/requirements.txt

# Зависимости group бота
pip install -r auction_group_bot/requirements.txt

# Зависимости бэкенда
pip install -r miniapp/backend/requirements.txt
```

### Вариант B — через Settings

**File → Settings → Python Interpreter → "+" → Install Package**
— введите по очереди: `aiogram`, `sqlalchemy`, `aiosqlite`, `apscheduler`,
`python-dotenv`, `fastapi`, `uvicorn`

---

## Шаг 4 — Создать файлы `.env`

### `auction_admin_bot/.env`

Скопируйте `.env.example` и заполните:
```
ADMIN_BOT_TOKEN=1234567890:AAxxxxxxx   ← токен admin бота
GROUP_BOT_TOKEN=9876543210:AAxxxxxxx   ← токен group бота
ADMIN_IDS=123456789                    ← ваш Telegram user_id
GROUP_ID=0                             ← пока 0 (настроим после)
DATABASE_URL=sqlite+aiosqlite:///./auction.db
```

### `auction_group_bot/.env`

```
GROUP_BOT_TOKEN=9876543210:AAxxxxxxx   ← токен group бота
ADMIN_BOT_TOKEN=1234567890:AAxxxxxxx   ← токен admin бота (для фото)
ADMIN_IDS=123456789
GROUP_ID=0
MINIAPP_URL=                           ← пока пусто
DATABASE_URL=sqlite+aiosqlite:///./auction.db
```

> ⚠️ **Важно:** оба бота должны использовать **один и тот же** `DATABASE_URL`,
> чтобы читать/писать в одну базу.

### `miniapp/backend/.env`

```
DATABASE_URL=sqlite+aiosqlite:///../../auction_admin_bot/auction.db
GROUP_BOT_TOKEN=9876543210:AAxxxxxxx
```

> Путь к БД — относительно `miniapp/backend/`. Укажите абсолютный путь
> если удобнее: `sqlite+aiosqlite:////home/user/auction/auction_admin_bot/auction.db`

---

## Шаг 5 — Настроить Run Configurations в PyCharm

Перейдите в **Run → Edit Configurations → "+" → Python**

### Конфигурация 1: Admin Bot

| Поле | Значение |
|---|---|
| Name | `Admin Bot` |
| Script path | `auction_admin_bot/bot.py` |
| Working directory | `auction_admin_bot/` |
| Environment variables | *(пусто — читает из .env)* |
| Python interpreter | ваш venv |

### Конфигурация 2: Group Bot

| Поле | Значение |
|---|---|
| Name | `Group Bot` |
| Script path | `auction_group_bot/bot.py` |
| Working directory | `auction_group_bot/` |
| Python interpreter | ваш venv |

### Конфигурация 3: Mini App Backend

| Поле | Значение |
|---|---|
| Name | `Mini App API` |
| Module name | `uvicorn` |
| Parameters | `main:app --reload --port 8000` |
| Working directory | `miniapp/backend/` |
| Python interpreter | ваш venv |

> Вместо Module name можно использовать Script path с `uvicorn` из venv,
> или просто запустить в терминале: `cd miniapp/backend && uvicorn main:app --reload`

---

## Шаг 6 — Запустить все три процесса

В PyCharm можно запускать несколько конфигураций одновременно.

1. **Run → Run 'Admin Bot'** — запустите первым
2. **Run → Run 'Group Bot'** — запустите вторым  
3. **Run → Run 'Mini App API'** — запустите третьим

После запуска в консоли должно появиться:
```
Admin Bot:   INFO - Admin bot starting...
Group Bot:   INFO - Group bot starting...
Mini App API: INFO - Application startup complete.
             INFO - Uvicorn running on http://127.0.0.1:8000
```

---

## Шаг 7 — Запустить React фронтенд

В отдельном терминале:
```bash
cd miniapp/frontend
npm install
npm start
```

Фронтенд откроется на [http://localhost:3000](http://localhost:3000).

> **Примечание:** В браузере Telegram WebApp SDK не работает (нет `window.Telegram`).
> Фронтенд покажет заглушку. Для полного тестирования нужен ngrok (см. Шаг 9).

---

## Шаг 8 — Первый тест (без группы)

Напишите `/start` каждому боту в личку в Telegram:

**Admin Bot** (`@ваш_admin_bot`):
- должен ответить «👑 Панель администратора» с кнопками
- создайте тестовый лот через «➕ Создать новый лот»
- пропустите фото (`/skip`), выберите «Начать сразу»

**Group Bot** (`@ваш_group_bot`):
- должен ответить приветственным сообщением
- если `MINIAPP_URL` задан — появится кнопка «🔨 Открыть аукционы»

---

## Шаг 9 — Тест с Mini App через ngrok (опционально)

Telegram Mini App требует HTTPS. Для локального тестирования используйте ngrok.

1. Установите [ngrok](https://ngrok.com/download)
2. Запустите туннели:
   ```bash
   # Туннель для бэкенда
   ngrok http 8000
   # Туннель для фронтенда  
   ngrok http 3000
   ```
3. ngrok даст URL вида `https://xxxx.ngrok-free.app`
4. В `miniapp/frontend/src/utils/api.js` замените `REACT_APP_API_URL` на URL бэкенда
5. В `auction_group_bot/.env` задайте:
   ```
   MINIAPP_URL=https://xxxx.ngrok-free.app   ← URL фронтенда
   ```
6. Перезапустите Group Bot
7. В [@BotFather](https://t.me/BotFather): `/newapp` → выберите group бота → укажите URL фронтенда

---

## Шаг 10 — Подключить реальную группу (опционально)

1. Создайте Telegram-группу (или используйте существующую)
2. Включите топики: **Настройки группы → Темы**
3. Добавьте оба бота в группу как **администраторов**
   (нужны права: отправка сообщений, редактирование сообщений, удаление сообщений)
4. Узнайте `GROUP_ID`: добавьте [@getmyid_bot](https://t.me/getmyid_bot) в группу
   — он напишет ID группы (начинается с `-100...`)
5. Создайте топик в группе для аукциона
6. Обновите `GROUP_ID` в `.env` обоих ботов, перезапустите их
7. При создании лота в admin боте — перешлите сообщение из нужного топика
   (бот определит ID топика автоматически)

---

## Быстрый старт (TL;DR)

```bash
# 1. Зависимости
pip install -r auction_admin_bot/requirements.txt
pip install -r auction_group_bot/requirements.txt
pip install -r miniapp/backend/requirements.txt

# 2. .env файлы (скопируйте .env → .env, заполните токены)
cp auction_admin_bot/.env auction_admin_bot/.env
cp auction_group_bot/.env auction_group_bot/.env
cp miniapp/backend/.env miniapp/backend/.env

# 3. Запустить (3 терминала)
cd auction_admin_bot && python bot.py
cd auction_group_bot && python bot.py
cd miniapp/backend && uvicorn main:app --reload

# 4. Фронтенд (4-й терминал)
cd miniapp/frontend && npm install && npm start
```

---

## Частые проблемы

### `ModuleNotFoundError: No module named 'texts'`
Admin бот и group бот импортируют `texts.py` из родительской директории.
**Решение:** установите Working directory в Run Configuration как `auction_admin_bot/`
(или `auction_group_bot/`) — НЕ корень проекта. В `bot.py` уже есть `sys.path.insert(0, "..")`.

### `sqlite3.OperationalError: no such table`
БД создаётся автоматически при первом запуске через `init_db()`.
Если таблицы не создались — проверьте что `DATABASE_URL` в `.env` правильный
и Working directory выставлен корректно.

### `TelegramForbiddenError: bot was blocked by the user`
Уведомления не доходят — пользователь заблокировал бота. Это нормально,
ошибки логируются на уровне `DEBUG` и не прерывают работу.

### `asyncpg` vs `aiosqlite`
- Для SQLite в `DATABASE_URL` используйте `sqlite+aiosqlite://`
- Для PostgreSQL — `postgresql+asyncpg://`
- Не смешивайте: если URL sqlite, пакет asyncpg не нужен запускаться

### Бот не отвечает на команды
- Убедитесь что токен правильный (без пробелов)
- Проверьте что бот запущен и нет ошибок в консоли
- Admin бот принимает команды **только от ADMIN_IDS** — проверьте что ваш ID в списке

---

## Переменные окружения — сводная таблица

| Переменная | Admin Bot | Group Bot | Mini App API |
|---|---|---|---|
| `ADMIN_BOT_TOKEN` | ✅ обязательно | ✅ (для фото) | — |
| `GROUP_BOT_TOKEN` | ✅ обязательно | ✅ обязательно | ✅ обязательно |
| `ADMIN_IDS` | ✅ обязательно | ✅ обязательно | — |
| `GROUP_ID` | ✅ обязательно | ✅ обязательно | — |
| `DATABASE_URL` | ✅ обязательно | ✅ **тот же файл** | ✅ **тот же файл** |
| `MINIAPP_URL` | — | опционально | — |
| `ANTISNIPE_MINUTES` | опционально (default: 2) | опционально (default: 2) | — |

```


## File: ngrok.yml
```yaml
version: "2"
tunnels:
  frontend:
    addr: 3000
    proto: http
  backend:
    addr: 8000
    proto: http
```


## File: requirements.txt
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.36
aiosqlite==0.20.0
asyncpg==0.30.0
python-dotenv==1.0.1
pydantic==2.9.2
httpx==0.27.0
```


## File: run.py
```python
"""
run.py — запускает всё одной командой:
  • auction_admin_bot
  • auction_group_bot
  • miniapp/backend (uvicorn)

Запуск:  python run.py
Стоп:    Ctrl+C  (останавливает все процессы)
"""
import subprocess
import sys
import os
import signal
import time

ROOT = os.path.dirname(os.path.abspath(__file__))

PYTHON = sys.executable

processes = []


def start():
    procs = [
        {
            "name": "Admin Bot",
            "cmd": [PYTHON, "bot.py"],
            "cwd": os.path.join(ROOT, "auction_admin_bot"),
        },
        {
            "name": "Group Bot",
            "cmd": [PYTHON, "bot.py"],
            "cwd": os.path.join(ROOT, "auction_group_bot"),
        },
        {
            "name": "Mini App API",
            "cmd": [PYTHON, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
            "cwd": os.path.join(ROOT, "miniapp", "backend"),
        },
    ]

    for p in procs:
        print(f"▶  Starting {p['name']}...")
        proc = subprocess.Popen(
            p["cmd"],
            cwd=p["cwd"],
            # Каждый процесс пишет в свой лог-файл И в консоль
            stdout=None,
            stderr=None,
        )
        processes.append((p["name"], proc))
        time.sleep(0.5)  # небольшая пауза между стартами

    print("\n✅ Все процессы запущены. Ctrl+C для остановки.\n")

    try:
        while True:
            for name, proc in processes:
                if proc.poll() is not None:
                    print(f"\n⚠️  {name} завершился с кодом {proc.returncode}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n⏹  Остановка...")
        for name, proc in processes:
            print(f"   Stopping {name}...")
            proc.terminate()
        for name, proc in processes:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        print("✅ Остановлено.")


if __name__ == "__main__":
    start()

```


## File: texts.py
```python
# =============================================================
#  Все пользовательские тексты — общий файл для обоих ботов.
#  Редактируйте здесь. Для применения нужен перезапуск ботов.
# =============================================================


# ── Админский бот: главное меню ───────────────────────────────

ADMIN_WELCOME = (
    "👑 <b>Панель администратора</b>\n\n"
    "Добро пожаловать! Управляйте аукционами группы через кнопки ниже."
)

ADMIN_NO_ACTIVE_LOTS = "📭 <b>Нет активных лотов.</b>\n\nСоздайте новый аукцион."
ADMIN_NO_FINISHED_LOTS = "📭 <b>Завершённых лотов пока нет.</b>"


# ── Админский бот: создание лота ──────────────────────────────

CREATE_ENTER_TITLE   = "➕ <b>Создание лота</b>\n\nВведите <b>название лота</b>:"
CREATE_TITLE_SHORT   = "Название слишком короткое. Введите минимум 3 символа."
CREATE_TITLE_TOO_SHORT = "Название слишком короткое. Введите минимум 3 символа."
CREATE_TITLE_OK      = "Название: <b>{title}</b> ✅\n\nУкажите <b>стартовую цену</b> (₽):"
CREATE_PRICE_INVALID = "Введите корректную цену от 1 000 ₽"
CREATE_PRICE_OK      = "Старт: <b>{price}</b> ✅\n\nВыберите <b>шаг ставки</b>:"
CREATE_STEP_MIN      = "Минимальный шаг — {min_step:,} ₽"
CREATE_STEP_ENTER    = "Введите шаг ставки (₽), минимум 500:"
CREATE_STEP_OK       = "Шаг: <b>{step}</b> ✅\n\nВыберите <b>длительность</b> аукциона:"
CREATE_DURATION_OK   = "Длительность: <b>{hours}ч</b> ✅\n\nДобавьте краткое <b>описание</b> лота:"
CREATE_PHOTO_PROMPT  = "📸 Отправьте <b>фото лота</b>.\n\nИли нажмите /skip чтобы пропустить."
CREATE_PHOTO_INVALID = "Пожалуйста, отправьте фото или напишите /skip чтобы пропустить."
CREATE_PHOTO_TOO_LONG = (
    "⚠️ Описание слишком длинное для лота с фото.\n\n"
    "Максимум: <b>{max_len} символов</b>\n"
    "Сейчас: <b>{current_len} символов</b>\n\n"
    "Вернитесь и сократите описание — нажмите /start чтобы начать заново."
)
CREATE_START_TIME_PROMPT      = "🕐 Когда начать аукцион?"
CREATE_START_TIME_FORMAT_ERR  = "Неверный формат. Введите дату и время так:\n<code>25.03 15:00</code>"
CREATE_START_TIME_DATE_ERR    = "Неверная дата. Проверьте день и месяц."
CREATE_START_TIME_PAST_ERR    = "❌ Указанное время уже прошло. Введите время <b>в будущем</b>."
CREATE_CONFIRM_START_NOW      = "• Начало: <b>сразу после запуска</b>\n"
CREATE_CONFIRM_START_AT       = "• Начало: <b>{time} МСК</b>\n"
CREATE_CONFIRM_TEXT = (
    "✅ <b>Проверьте данные лота</b>\n\n"
    "• Название: <b>{emoji} {title}</b>\n"
    "• Описание: {description}\n"
    "• Фото: {photo}\n"
    "{start_line}"
    "• Стартовая цена: <b>{start_price}</b>\n"
    "• Шаг ставки: {bid_step}\n"
    "• Длительность: {duration_hours}ч\n\n"
    "<i>Лот будет опубликован в Мини Апп 📱</i>"
)
CREATE_LOT_CREATED = (
    "✅ <b>Лот создан!</b>  <code>{lot_code}</code>\n\n"
    "{emoji} <b>{title}</b>\n\n"
    "<i>Лот будет опубликован в Мини Апп 📱</i>"
)
# Оставлены для обратной совместимости (не используются при запуске через Мини Апп)
CREATE_TOPIC_AUTO    = "✅ Топик определён автоматически: <code>#{topic_id}</code>"
CREATE_TOPIC_ENTER   = (
    "Введите <b>числовой ID топика</b> (message_thread_id).\n\n"
    "<b>Как узнать ID:</b>\n"
    "1. Откройте группу в Telegram Web (web.telegram.org)\n"
    "2. Перейдите в нужный топик\n"
    "3. В адресной строке будет: <code>...?thread=<b>12345</b></code>\n"
    "   — это и есть ID топика"
)
CREATE_TOPIC_INVALID = "Введите <b>только число</b> — ID топика.\nПример: <code>12345</code>"
CREATE_TOPIC_ERROR   = "Что-то пошло не так. Начните создание лота заново /start"
CREATE_LAUNCHED = (
    "🚀 <b>Аукцион запущен в Мини Апп!</b>\n\n"
    "<code>{lot_code}</code>\n\n"
    "{emoji} <b>{title}</b>\n"
    "Старт: <b>{start_price}</b>\n"
    "Длительность: {duration_hours}ч\n\n"
    "<i>Участники видят лот в Мини Апп 📱</i>"
)
CREATE_SCHEDULED = (
    "🕐 <b>Аукцион запланирован!</b>\n\n"
    "<code>{lot_code}</code>\n\n"
    "{emoji} <b>{title}</b>\n"
    "Старт: <b>{start_time} МСК</b>\n"
    "Длительность: {duration_hours}ч\n\n"
    "<i>Лот появится в Мини Апп в указанное время 📱</i>"
)


# ── Админский бот: управление лотом ──────────────────────────

MANAGE_LOT_NOT_FOUND    = "Лот не найден."
MANAGE_CANNOT_PAUSE     = "Нельзя поставить на паузу."
MANAGE_NOT_PAUSED       = "Лот не на паузе."
MANAGE_PAUSED           = "⏸ Приостановлен\nТаймер остановлен. Ставки заморожены.\nОсталось: {time_left}"
MANAGE_RESUMED          = "▶️ Возобновлён\nТаймер продолжается. Новое время окончания: {ends_at}"
MANAGE_EXTENDED         = "+{hours}ч добавлено\nНовое время окончания: {ends_at}\nУчастники уведомлены."
MANAGE_CANCELLED        = "Лот отменён"
MANAGE_FINISHED         = "Завершено"
MANAGE_BLOCKED          = "Заблокирован"
MANAGE_NO_PARTICIPANTS  = "Нет участников для блокировки."
MANAGE_REFRESHED        = "Обновлено ✓"
MANAGE_CANCEL_CONFIRM = (
    "⚠️ <b>Отменить аукцион?</b>\n\n"
    "Все ставки будут аннулированы. Участники получат уведомление."
)
MANAGE_EARLY_FINISH_CONFIRM = (
    "⚠️ <b>Завершить досрочно?</b>\n\n"
    "{price_line}"
    "Победителем становится текущий лидер.\n"
)
MANAGE_TOPIC_CLOSED     = "Топик #{topic_id} закрыт. {bid_count} участников уведомлены."


# ── Клиентский бот: приветствие ───────────────────────────────

GROUP_WELCOME = (
    "👋 Привет! Я бот аукциона.\n\n"
    "Участвуйте в торгах прямо из группы — нажимайте кнопки на карточках лотов.\n\n"
    "Чтобы получать уведомления о ставках и победах, вы должны написать мне сюда хотя бы раз."
)
GROUP_NO_ACTIVE_LOTS = "Сейчас нет активных аукционов."


# ── Клиентский бот: ставки ────────────────────────────────────

BID_LOT_NOT_FOUND   = "Лот не найден."
BID_NOT_ACTIVE      = "⛔ Аукцион не активен."
BID_NOT_STARTED     = "⏳ Аукцион ещё не начался."
BID_CONFIRM_PROMPT  = (
    "💬 <b>Подтвердите ставку</b>\n\n"
    "{emoji} {title}\n"
    "Ваша ставка: <b>{amount}</b>\n\n"
    "⚠️ После подтверждения ставку нельзя отозвать."
)
BID_TOO_LOW = (
    "⚠️ Ставка слишком маленькая.\n\n"
    "Текущая цена: <b>{current_price}</b>\n"
    "Минимальная ставка: <b>{min_bid}</b>\n\n"
    "Напишите сумму числом (например: <code>{min_bid_raw}</code>)"
)
BID_ENTER_AMOUNT    = "Введите сумму ставки (₽):"
BID_INVALID_AMOUNT  = "Введите корректную сумму числом."
BID_ACCEPTED        = (
    "✅ <b>Ставка принята!</b>\n\n"
    "{emoji} <b>{title}</b>\n"
    "Ваша ставка: <b>{amount}</b>\n"
    "Вы сейчас <b>лидируете</b> 🏆\n\n"
    "<i>Вы получите уведомление если вас перебьют.</i>"
)
BID_OVERBID         = (
    "⚡ <b>Вас перебили!</b>\n\n"
    "{emoji} {title}\n"
    "Финальная цена: <b>{new_price}</b>\n\n"
    "Вернитесь в топик чтобы сделать новую ставку."
)
BID_CANCELLED       = "Ставка отменена."
BID_START_FIRST     = "Напишите боту /start в личку чтобы получить правила"


# ── Клиентский бот: победитель ────────────────────────────────

WINNER_DM = (
    "🏆 <b>Поздравляем! Вы победили!</b>\n\n"
    "{emoji} <b>{title}</b>\n"
    "Финальная ставка: <b>{amount}</b>\n\n"
    "Администратор свяжется с вами для оформления покупки."
)
WINNER_FALLBACK_TOPIC = (
    "🏆 Победитель аукциона, поздравляем!\n\n"
    "Напишите <b>/start</b> нашему боту в личку, "
    "чтобы получить детали покупки."
)


# ── Завершение аукциона (топик) ───────────────────────────────

AUCTION_FINISHED = (
    "🏁 <b>Аукцион завершён</b>\n\n"
    "{emoji} <b>{title}</b>\n"
    "<code>{lot_code}</code>\n\n"
    "📋 {description}\n\n"
    "💰 Финальная цена: <b>{final_price}</b>"
)
AUCTION_NO_BIDS = "📭 Аукцион завершился без ставок.\n{emoji} {title}"


# ── Клиентский бот: наблюдатели ───────────────────────────────

WATCHER_OVERBID   = (
    "⚡ <b>Ставку перебили!</b>\n\n"
    "{emoji} {title}\n"
    "Новая цена: <b>{new_price}</b>"
)
WATCHER_FINISHED  = (
    "🏁 <b>Аукцион завершён</b>\n\n"
    "{emoji} {title}\n"
    "Финальная цена: {final_price}"
)
AUCTION_STARTED_TOPIC = "🔔 <b>Аукцион начался!</b>\n{emoji} {title}"


# ── Клиентский бот: оценка ────────────────────────────────────

RATING_PROMPT = (
    "⭐ <b>Оцените аукцион</b>\n\n"
    "{emoji} {title}\n"
    "Итоговая цена: <b>{final_price}</b>\n\n"
    "Пожалуйста, оцените ваш опыт участия в аукционе:"
)
RATING_THANKS = (
    "Спасибо за оценку! {stars} {emoji}\n\n"
    "До следующего аукциона! Следите за новыми лотами в группе."
)


# ── Клавиатура (кнопки) ───────────────────────────────────────

# Админский бот
KB_CREATE           = "➕ Создать новый лот"
KB_ACTIVE_LOTS      = "📋 Активные лоты"
KB_FINISHED_LOTS    = "🏁 Завершённые лоты"
KB_MAIN_MENU        = "← Главное меню"
KB_MANAGE           = "⚙️ Управление"
KB_REFRESH          = "🔄 Обновить"
KB_ALL_LOTS         = "← Все лоты"
KB_EXTEND           = "⏱ Продлить"
KB_EARLY_FINISH     = "⏹ Завершить досрочно"
KB_PAUSE            = "⏸ Приостановить"
KB_RESUME           = "▶️ Возобновить"
KB_CANCEL_LOT       = "🚫 Отменить лот"
KB_MONITOR          = "← Мониторинг"
KB_START_NOW        = "🚀 Сразу после запуска"
KB_START_CUSTOM     = "🕐 Выбрать время (МСК)"
KB_CANCEL_ACTION    = "❌ Отмена"
KB_CONFIRM_YES      = "✅ Да, подтверждаю"
KB_CONFIRM_NO       = "❌ Нет, отмена"
KB_BIND_TOPIC       = "🔗 Привязать топик и запустить"  # оставлен для совместимости
KB_REPORT           = "📊 Полный отчёт"
KB_BACK             = "← Назад"

# Клиентский бот
KB_HELP             = "❓ Помощь"
KB_CUSTOM_BID       = "✏️ Своя сумма"
KB_CONFIRM_BID      = "✅ Да, ставлю {amount}"
KB_CANCEL_BID       = "❌ Отмена"
KB_RATE             = "⭐ Оценить аукцион"
KB_TO_START         = "🏠 В начало"
KB_CONFIRM_WIN      = "✅ Подтверждаю покупку"
KB_SCHEDULED_BTN    = "🕐 Аукцион начнётся в {start_time} МСК"

```


## File: auction_admin_bot\README.md
```markdown
# Auction Admin Bot

Telegram-бот для управления аукционами в закрытой группе с топиками.

## Структура файлов


```


## File: auction_admin_bot\bot.py
```python
"""
auction_admin_bot/bot.py
────────────────────────
Изменения по сравнению с оригиналом:
  1. Добавлен import sync_overbid_notifications из utils.scheduler.
  2. После restore_scheduled_jobs запускаются три фоновых таска:
       – sync_finish_jobs          (был в оригинале)
       – sync_overbid_notifications (НОВЫЙ — для ставок из Mini App)
  3. winner_bot теперь передаётся во все функции scheduler.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, GROUP_BOT_TOKEN
from db.database import init_db
from handlers import main_menu, create_lot, monitor, manage, finish
from utils.scheduler import (
    setup_scheduler,
    restore_scheduled_jobs,
    sync_finish_jobs,
    sync_overbid_notifications,   # ← НОВЫЙ ИМПОРТ
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=BOT_TOKEN)

    # Клиентский бот — для отправки уведомлений победителям и обновления карточек
    winner_bot = Bot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    await init_db()

    scheduler = setup_scheduler(bot)
    scheduler.start()

    # Восстановить таймеры и инициализировать кеш цен
    await restore_scheduled_jobs(bot, winner_bot)

    # Фоновые задачи
    asyncio.create_task(sync_finish_jobs(bot, winner_bot))
    asyncio.create_task(sync_overbid_notifications(bot, winner_bot))  # ← НОВЫЙ ТАСК

    dp.include_router(main_menu.router)
    dp.include_router(create_lot.router)
    dp.include_router(monitor.router)
    dp.include_router(manage.router)
    dp.include_router(finish.router)

    logger.info("Admin bot starting...")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=["message", "callback_query", "chat_member"],
        )
    finally:
        scheduler.shutdown()
        await bot.session.close()
        if winner_bot:
            await winner_bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

```


## File: auction_admin_bot\config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

# ── Telegram ──────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("ADMIN_BOT_TOKEN", "")

# Токен клиентского бота — для отправки уведомлений победителям
GROUP_BOT_TOKEN: str = os.getenv("GROUP_BOT_TOKEN", "")

# Admin Telegram user IDs (comma-separated in .env)
_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: list[int] = [int(x.strip()) for x in _raw.split(",") if x.strip()]

# The closed group where auctions happen
GROUP_ID: int = int(os.getenv("GROUP_ID", "0"))

# ── Database ──────────────────────────────────────────────────
DATABASE_URL: str = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/auction"
)

# ── Redis ─────────────────────────────────────────────────────
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# ── Auction defaults ─────────────────────────────────────────
ANTISNIPE_MINUTES: int = int(os.getenv("ANTISNIPE_MINUTES", "2"))
MIN_BID_STEP: int = int(os.getenv("MIN_BID_STEP", "500"))


```


## File: auction_admin_bot\requirements.txt
```
aiogram==3.13.1
sqlalchemy==2.0.36
asyncpg==0.30.0
apscheduler==3.10.4
python-dotenv==1.0.1
redis==5.2.0

aiosqlite==0.20.0

```


## File: auction_admin_bot\db\__init__.py
```python


```


## File: auction_admin_bot\db\database.py
```python
from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum, ForeignKey,
    Float, Integer, String, Text, func,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class LotStatus(str, enum.Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    FINISHED = "finished"
    CANCELLED = "cancelled"


# ── Models ────────────────────────────────────────────────────

class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_code: Mapped[str] = mapped_column(String(20), unique=True)  # LOT-123

    # Meta
    category: Mapped[str] = mapped_column(String(64))
    emoji: Mapped[str] = mapped_column(String(8))
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo_file_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    client_photo_file_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    # Pricing
    start_price: Mapped[int] = mapped_column(Integer)
    bid_step: Mapped[int] = mapped_column(Integer)
    blitz_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    current_price: Mapped[int] = mapped_column(Integer)

    # Timing
    duration_hours: Mapped[float] = mapped_column(Float)
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    seconds_left: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # используется при паузе

    # Telegram references
    topic_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    card_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # State
    status: Mapped[LotStatus] = mapped_column(Enum(LotStatus), default=LotStatus.PENDING)
    created_by: Mapped[int] = mapped_column(BigInteger)  # admin user_id
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Winner (set on finish)
    winner_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    winner_username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    final_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    bids: Mapped[list[Bid]] = relationship("Bid", back_populates="lot", order_by="Bid.id.desc()")


class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"))
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    amount: Mapped[int] = mapped_column(Integer)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    lot: Mapped[Lot] = relationship("Lot", back_populates="bids")


class BannedUser(Base):
    __tablename__ = "banned_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    banned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    banned_by: Mapped[int] = mapped_column(BigInteger)


class WatchList(Base):
    """Участники, подписанные на уведомления по лоту."""
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"))
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)


# Alias for compatibility with queries that use Watchlist (lowercase L)
Watchlist = WatchList


class Rating(Base):
    """Оценки аукционов от участников."""
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"))
    user_id: Mapped[int] = mapped_column(BigInteger)
    stars: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ── Session helper ─────────────────────────────────────────────

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        return session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _migrate(conn)


async def _migrate(conn):
    """
    Добавляет новые колонки в существующую БД (если их нет).
    SQLite не поддерживает изменение типов, но ADD COLUMN работает.
    """
    import sqlalchemy as sa
    migrations = [
        ("lots", "seconds_left",         "INTEGER"),
        ("lots", "starts_at",            "DATETIME"),
        ("lots", "client_photo_file_id", "VARCHAR(256)"),
        ("lots", "photo_file_id",        "VARCHAR(256)"),
        ("lots", "card_message_id",      "BIGINT"),
    ]
    for table, column, col_def in migrations:
        try:
            await conn.execute(sa.text(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}"))
        except Exception:
            pass  # колонка уже существует — игнорируем



```


## File: auction_admin_bot\db\queries.py
```python
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.database import AsyncSessionLocal, Bid, BannedUser, Lot, LotStatus


# ── Helpers ───────────────────────────────────────────────────

async def _gen_code(session: AsyncSession) -> str:
    """Генерирует следующий порядковый номер лота: LOT-0001, LOT-0002, ..."""
    result = await session.execute(select(func.count()).select_from(Lot))
    count = result.scalar_one()
    return f"LOT-{count + 1:04d}"


# ── Lot CRUD ──────────────────────────────────────────────────

async def create_lot(
    *,
    created_by: int,
    category: str,
    emoji: str,
    title: str,
    description: str,
    start_price: int,
    bid_step: int,
    duration_hours: int,
    blitz_price: Optional[int] = None,
    photo_file_id: Optional[str] = None,
) -> Lot:
    async with AsyncSessionLocal() as s:
        lot = Lot(
            lot_code=await _gen_code(s),
            created_by=created_by,
            category=category,
            emoji=emoji,
            title=title,
            description=description,
            start_price=start_price,
            bid_step=bid_step,
            duration_hours=duration_hours,
            blitz_price=blitz_price,
            photo_file_id=photo_file_id,
            current_price=start_price,
            status=LotStatus.PENDING,
        )
        s.add(lot)
        await s.commit()
        await s.refresh(lot)
        return lot


async def get_lot(lot_id: int) -> Optional[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot).options(selectinload(Lot.bids)).where(Lot.id == lot_id)
        )
        return result.scalar_one_or_none()


async def get_active_lots() -> list[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot)
            .where(Lot.status.in_([LotStatus.SCHEDULED, LotStatus.ACTIVE]))
            .order_by(Lot.created_at)
        )
        return list(result.scalars().all())


async def get_all_lots(limit: int = 20) -> list[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot).order_by(Lot.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())


async def get_finished_lots(limit: int = 10, offset: int = 0) -> tuple[list[Lot], int]:
    async with AsyncSessionLocal() as s:
        count_result = await s.execute(
            select(func.count()).select_from(Lot).where(Lot.status == LotStatus.FINISHED)
        )
        total = count_result.scalar_one()
        result = await s.execute(
            select(Lot)
            .where(Lot.status == LotStatus.FINISHED)
            .order_by(Lot.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all()), total


async def schedule_lot(lot_id: int, topic_id: int, starts_at: datetime) -> Lot:
    """Привязать топик и перевести в SCHEDULED — карточка публикуется сразу."""
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.SCHEDULED,
                topic_id=topic_id,
                starts_at=starts_at,
                card_message_id=None,
            )
        )
        await s.commit()
    return await get_lot(lot_id)


async def activate_scheduled_lot(lot_id: int, ends_at: datetime) -> Lot:
    """Перевести из SCHEDULED в ACTIVE когда наступило время."""
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.ACTIVE,
                ends_at=ends_at,
            )
        )
        await s.commit()
    return await get_lot(lot_id)


async def launch_lot(lot_id: int, topic_id: int, ends_at: datetime) -> Lot:
    """Немедленный запуск без отложенного старта."""
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.ACTIVE,
                topic_id=topic_id,
                starts_at=None,
                ends_at=ends_at,
                card_message_id=None,
            )
        )
        await s.commit()
    return await get_lot(lot_id)


async def set_card_message_id(lot_id: int, message_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(card_message_id=message_id)
        )
        await s.commit()


async def extend_lot(lot_id: int, new_ends_at: datetime):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(ends_at=new_ends_at)
        )
        await s.commit()


async def finish_lot(lot_id: int, winner_user_id: int, winner_username: str, final_price: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.FINISHED,
                winner_user_id=winner_user_id,
                winner_username=winner_username,
                final_price=final_price,
            )
        )
        await s.commit()


async def cancel_lot(lot_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(status=LotStatus.CANCELLED)
        )
        await s.commit()


# ── Bids ──────────────────────────────────────────────────────

async def get_top_bid(lot_id: int) -> Optional[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.amount.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


async def get_bid_count(lot_id: int) -> int:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(func.count()).where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
        )
        return result.scalar_one()


async def get_unique_bidder_count(lot_id: int) -> int:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(func.count(Bid.user_id.distinct()))
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
        )
        return result.scalar_one()


async def get_recent_bids(lot_id: int, limit: int = 5) -> list[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())


async def cancel_user_bids(lot_id: int, user_id: int):
    """Аннулировать все ставки участника по лоту (при бане)."""
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Bid)
            .where(Bid.lot_id == lot_id, Bid.user_id == user_id)
            .values(is_cancelled=True)
        )
        await s.commit()


async def get_bidders_for_lot(lot_id: int) -> list[dict]:
    """Список уникальных участников с их максимальными ставками."""
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid.user_id, Bid.username, func.max(Bid.amount).label("max_amount"))
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .group_by(Bid.user_id, Bid.username)
            .order_by(func.max(Bid.amount).desc())
        )
        return [{"user_id": r.user_id, "username": r.username, "amount": r.max_amount}
                for r in result.all()]


# ── Stats ─────────────────────────────────────────────────────

async def get_stats() -> dict:
    async with AsyncSessionLocal() as s:
        total_lots = (await s.execute(select(func.count()).select_from(Lot))).scalar_one()
        finished_lots = (await s.execute(
            select(func.count()).where(Lot.status == LotStatus.FINISHED)
        )).scalar_one()
        total_turnover = (await s.execute(
            select(func.sum(Lot.final_price)).where(Lot.status == LotStatus.FINISHED)
        )).scalar_one() or 0
        total_bids = (await s.execute(
            select(func.count()).select_from(Bid).where(Bid.is_cancelled == False)
        )).scalar_one()
        unique_bidders = (await s.execute(
            select(func.count(Bid.user_id.distinct())).where(Bid.is_cancelled == False)
        )).scalar_one()

    return {
        "total_lots": total_lots,
        "finished_lots": finished_lots,
        "total_turnover": total_turnover,
        "total_bids": total_bids,
        "unique_bidders": unique_bidders,
    }


# ── Bans ──────────────────────────────────────────────────────

async def ban_user(user_id: int, username: Optional[str], banned_by: int):
    async with AsyncSessionLocal() as s:
        existing = await s.get(BannedUser, user_id)
        if not existing:
            s.add(BannedUser(user_id=user_id, username=username, banned_by=banned_by))
            await s.commit()


async def is_banned(user_id: int) -> bool:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(BannedUser).where(BannedUser.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None


async def get_lot_bids(lot_id: int, limit: int = 50) -> list[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id)
            .order_by(Bid.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())



# ── Pause / Resume (добавлено для handlers/manage.py) ─────────

async def pause_lot(lot_id: int, seconds_left: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(status=LotStatus.PAUSED, seconds_left=seconds_left)
        )
        await s.commit()


async def resume_lot(lot_id: int, new_ends_at: datetime):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(status=LotStatus.ACTIVE, ends_at=new_ends_at, seconds_left=None)
        )
        await s.commit()


# ── Watchlist (добавлено для handlers/lots.py и handlers/bidding.py) ──

async def is_watching(lot_id: int, user_id: int) -> bool:
    """Проверить, следит ли пользователь за лотом."""
    from db.database import Watchlist
    async with AsyncSessionLocal() as s:
        from sqlalchemy import select as sa_select
        result = await s.execute(
            sa_select(Watchlist).where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        return result.scalar_one_or_none() is not None


async def add_to_watchlist(lot_id: int, user_id: int, username: Optional[str] = None):
    """Добавить лот в список отслеживания."""
    from db.database import Watchlist
    async with AsyncSessionLocal() as s:
        from sqlalchemy import select as sa_select
        existing = await s.execute(
            sa_select(Watchlist).where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        if existing.scalar_one_or_none() is None:
            s.add(Watchlist(lot_id=lot_id, user_id=user_id, username=username))
            await s.commit()


async def remove_from_watchlist(lot_id: int, user_id: int):
    """Убрать лот из списка отслеживания."""
    from db.database import Watchlist
    async with AsyncSessionLocal() as s:
        from sqlalchemy import delete as sa_delete
        await s.execute(
            sa_delete(Watchlist).where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        await s.commit()


# ── Rating (добавлено для handlers/notifications.py) ─────────

async def save_rating(lot_id: int, user_id: int, stars: int):
    """Сохранить оценку пользователя."""
    from db.database import Rating
    async with AsyncSessionLocal() as s:
        from sqlalchemy import select as sa_select
        existing = await s.execute(
            sa_select(Rating).where(
                Rating.lot_id == lot_id, Rating.user_id == user_id
            )
        )
        rating = existing.scalar_one_or_none()
        if rating:
            rating.stars = stars
        else:
            s.add(Rating(lot_id=lot_id, user_id=user_id, stars=stars))
        await s.commit()


# ── place_bid, get_watchers (добавлено для handlers/bidding.py) ──

async def place_bid(
    lot_id: int,
    user_id: int,
    username: Optional[str],
    amount: int,
) -> tuple[bool, Optional[str], None]:
    """
    Разместить ставку с SELECT FOR UPDATE против race condition.
    Возвращает (success, error_message, bid_or_None).
    """
    async with AsyncSessionLocal() as s:
        async with s.begin():
            banned = await s.get(BannedUser, user_id)
            if banned:
                return False, "Вы заблокированы", None

            result = await s.execute(
                select(Lot).where(Lot.id == lot_id).with_for_update()
            )
            lot = result.scalar_one_or_none()

            if not lot:
                return False, "Лот не найден", None
            if lot.status != LotStatus.ACTIVE:
                return False, "Аукцион не активен", None

            from datetime import timezone as _tz
            if lot.ends_at:
                ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=_tz.utc)
                if ends <= datetime.now(_tz.utc):
                    return False, "Время аукциона истекло", None

            min_bid = lot.current_price + lot.bid_step
            if amount < min_bid:
                return False, f"Минимальная ставка: {min_bid:,} ₽", None

            bid = Bid(lot_id=lot_id, user_id=user_id, username=username, amount=amount)
            s.add(bid)
            lot.current_price = amount

    # Перечитать bid для получения id
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.user_id == user_id,
                   Bid.amount == amount, Bid.is_cancelled == False)
            .order_by(Bid.id.desc()).limit(1)
        )
        bid = result.scalar_one_or_none()

    return True, None, bid


async def get_watchers(lot_id: int) -> list:
    """Список пользователей, следящих за лотом."""
    from db.database import WatchList
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(WatchList).where(WatchList.lot_id == lot_id)
        )
        return list(result.scalars().all())


async def remove_from_watchlist(lot_id: int, user_id: int):
    from db.database import WatchList
    async with AsyncSessionLocal() as s:
        from sqlalchemy import delete as sa_delete
        await s.execute(
            sa_delete(WatchList).where(
                WatchList.lot_id == lot_id, WatchList.user_id == user_id
            )
        )
        await s.commit()


async def update_card_message_id(lot_id: int, message_id: int):
    """Alias для set_card_message_id."""
    await set_card_message_id(lot_id, message_id)


async def save_client_photo_file_id(lot_id: int, file_id: str):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(client_photo_file_id=file_id)
        )
        await s.commit()

```


## File: auction_admin_bot\handlers\__init__.py
```python


```


## File: auction_admin_bot\handlers\bidding.py
```python
import asyncio
import logging
from datetime import timezone
from typing import Dict, Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db.queries import (
    add_to_watchlist, get_bid_count, get_lot, get_top_bid,
    place_bid, remove_from_watchlist, get_watchers,
)
from db.database import LotStatus
from keyboards.inline import (
    kb_after_bid, kb_overbid, kb_lot_card,
    kb_rating, kb_back_to_start, kb_cancel_custom_bid,
    kb_confirm_bid, kb_winner,
)
from utils.formatting import (
    bid_accepted_text, fmt_price, lot_card_text, overbid_notify_text,
)
from utils.scheduler import apply_antisnipe
from utils.states import CustomBidFSM

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer("⏳ Аукцион ещё не начался", show_alert=False)

# Хранилище pending-подтверждений: {user_id: {lot_id, amount, is_blitz, task}}
_pending: Dict[int, Dict[str, Any]] = {}

CONFIRM_TIMEOUT = 30  # секунд до автоотмены


# ─────────────────────────────────────────────────────────────
# ПОРЯДОК ВАЖЕН: специфичные фильтры — ВЫШЕ общих
# ─────────────────────────────────────────────────────────────


# ── Custom bid — шаг 1: кнопка «✏️ Своя сумма» ───────────────

@router.callback_query(F.data.regexp(r"^bid:custom:\d+$"))
async def cb_custom_bid_start(callback: CallbackQuery, state: FSMContext):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    if lot.status != LotStatus.ACTIVE:
        await callback.answer("Аукцион не активен.", show_alert=True)
        return

    await state.set_state(CustomBidFSM.waiting_for_amount)
    await state.update_data(lot_id=lot_id)

    min_bid = lot.current_price + lot.bid_step
    blitz_line = f"\n🔥 Блиц-цена: <b>{fmt_price(lot.blitz_price)}</b>" if lot.blitz_price else ""

    try:
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=(
                f"✏️ <b>Введите сумму ставки</b>\n\n"
                f"{lot.emoji} {lot.title}\n"
                f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
                f"Минимальная ставка: <b>{fmt_price(min_bid)}</b>"
                f"{blitz_line}\n\n"
                f"Напишите сумму числом (например: <code>{min_bid}</code>)"
            ),
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        await callback.answer("✏️ Напишите сумму в личку боту")
    except Exception as e:
        logger.debug(f"Custom bid DM failed: {e}")
        await state.clear()
        await callback.answer(
            "❌ Сначала напишите боту /start в личку — иначе он не сможет написать вам.",
            show_alert=True,
        )


# ── Custom bid — отмена ───────────────────────────────────────

@router.callback_query(F.data.regexp(r"^bid:custom:cancel:\d+$"))
async def cb_custom_bid_cancel(callback: CallbackQuery, state: FSMContext):
    lot_id = int(callback.data.split(":")[3])
    await state.clear()
    await callback.message.edit_text(
        "❌ Ввод ставки отменён.",
        reply_markup=kb_after_bid(lot_id),
    )
    await callback.answer()


# ── Custom bid — шаг 2: получить сумму ───────────────────────

@router.message(CustomBidFSM.waiting_for_amount)
async def msg_custom_bid_amount(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return

    data = await state.get_data()
    lot_id = data.get("lot_id")
    if not lot_id:
        await state.clear()
        return

    raw = (message.text or "").strip()
    raw = raw.replace(" ", "").replace(",", "").replace(".", "").replace("\u202f", "").replace("\xa0", "")

    if not raw.isdigit():
        lot = await get_lot(lot_id)
        min_bid = (lot.current_price + lot.bid_step) if lot else 0
        await message.answer(
            f"❌ Введите число без букв.\nНапример: <code>{min_bid}</code>",
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        return

    amount = int(raw)
    lot = await get_lot(lot_id)

    if not lot:
        await state.clear()
        await message.answer("Лот не найден.")
        return

    min_bid = lot.current_price + lot.bid_step
    if amount < min_bid:
        await message.answer(
            f"❌ Ставка слишком низкая.\n"
            f"Минимум: <b>{fmt_price(min_bid)}</b>\n\n"
            f"Введите другую сумму:",
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        return

    await state.clear()

    # Отправить подтверждение в личку
    is_blitz = bool(lot.blitz_price and amount >= lot.blitz_price)
    await _send_confirm_dm(message.bot, message.from_user.id, lot, amount, is_blitz)


# ── Ставка по кнопке из топика — отправить подтверждение в личку

@router.callback_query(F.data.regexp(r"^bid:\d+:\d+(:\w+)?$"))
async def cb_bid_request(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id = int(parts[1])
    amount = int(parts[2])
    is_blitz = len(parts) > 3 and parts[3] == "blitz"
    from_topic = callback.message.chat.type in ("group", "supergroup")

    # Из личного чата (кнопки перебития) — тоже через подтверждение
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    if lot.status != LotStatus.ACTIVE:
        await callback.answer("Аукцион завершён.", show_alert=True)
        return

    user_id = callback.from_user.id

    # Отменить предыдущий pending если был
    old = _pending.pop(user_id, None)
    if old and old.get("task"):
        old["task"].cancel()

    try:
        await _send_confirm_dm(callback.bot, user_id, lot, amount, is_blitz)
        await callback.answer("📩 Подтвердите ставку в личке бота", show_alert=False)
    except Exception as e:
        logger.debug(f"Confirm DM failed: {e}")
        await callback.answer(
            "❌ Сначала напишите боту /start в личку — иначе он не сможет написать вам.",
            show_alert=True,
        )


# ── Подтверждение ставки (из лички) ──────────────────────────

@router.callback_query(F.data.regexp(r"^bid:confirm:\d+:\d+$"))
async def cb_bid_confirmed(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id = int(parts[2])
    amount = int(parts[3])
    user_id = callback.from_user.id

    pending = _pending.pop(user_id, None)
    if pending and pending.get("task"):
        pending["task"].cancel()

    is_blitz = pending.get("is_blitz", False) if pending else False

    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        await callback.message.edit_text(
            "❌ Аукцион уже завершён, ставка не принята.",
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await _execute_bid(
        bot=callback.bot,
        lot_id=lot_id,
        user_id=user_id,
        username=callback.from_user.username,
        amount=amount,
        reply_fn=callback.message.edit_text,
        from_topic=False,
        callback=callback,
        is_blitz=is_blitz,
    )


# ── Отмена подтверждения (из лички) ──────────────────────────

@router.callback_query(F.data.regexp(r"^bid:cancel_confirm:\d+$"))
async def cb_bid_cancel_confirm(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    user_id = callback.from_user.id

    pending = _pending.pop(user_id, None)
    if pending and pending.get("task"):
        pending["task"].cancel()

    lot = await get_lot(lot_id)
    lot_name = f"{lot.emoji} {lot.title}" if lot else "лот"
    await callback.message.edit_text(
        f"❌ Ставка отменена.\n\n{lot_name}",
        parse_mode="HTML",
    )
    await callback.answer("Ставка отменена.")


# ── Watch ─────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("watch:on:"))
async def cb_watch_on(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    await add_to_watchlist(lot_id, callback.from_user.id, callback.from_user.username)
    await callback.answer("🔔 Пришлём результат в личку!", show_alert=True)


# ── Helpers ───────────────────────────────────────────────────

async def _send_confirm_dm(bot, user_id: int, lot, amount: int, is_blitz: bool):
    """Отправить сообщение с подтверждением в личку и запустить таймер."""
    blitz_note = "\n\n🔥 <b>Это блиц-цена — аукцион завершится мгновенно!</b>" if is_blitz else ""
    confirm_text = (
        f"⚡ <b>Подтвердите ставку</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"Ваша ставка: <b>{fmt_price(amount)}</b>"
        f"{blitz_note}\n\n"
        f"⏱ У вас {CONFIRM_TIMEOUT} секунд"
    )
    msg = await bot.send_message(
        chat_id=user_id,
        text=confirm_text,
        reply_markup=kb_confirm_bid(lot.id, amount, is_blitz),
        parse_mode="HTML",
    )

    # Сохранить pending
    old = _pending.pop(user_id, None)
    if old and old.get("task"):
        old["task"].cancel()

    task = asyncio.create_task(
        _auto_expire_confirm(bot, user_id, lot.id, msg.chat.id, msg.message_id)
    )
    _pending[user_id] = {
        "lot_id": lot.id,
        "amount": amount,
        "is_blitz": is_blitz,
        "task": task,
    }


async def _auto_expire_confirm(bot, user_id: int, lot_id: int, chat_id: int, message_id: int):
    """Через CONFIRM_TIMEOUT сек убрать кнопки и сообщить об истечении."""
    await asyncio.sleep(CONFIRM_TIMEOUT)
    if user_id in _pending and _pending[user_id].get("lot_id") == lot_id:
        _pending.pop(user_id, None)
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="⌛ Время на подтверждение истекло. Сделайте ставку заново.",
                parse_mode="HTML",
            )
        except Exception:
            pass


async def _execute_bid(
    bot, lot_id: int, user_id: int, username,
    amount: int, reply_fn, from_topic: bool,
    callback=None, is_blitz: bool = False,
):
    prev_top = await get_top_bid(lot_id)
    prev_leader_id = prev_top.user_id if (prev_top and prev_top.user_id != user_id) else None

    success, reason, bid = await place_bid(lot_id, user_id, username, amount)
    if not success:
        if callback:
            await callback.answer(f"❌ {reason}", show_alert=True)
        await reply_fn(f"❌ {reason}", parse_mode="HTML")
        return

    lot = await get_lot(lot_id)
    bid_count = await get_bid_count(lot_id)

    # Антиснайпинг
    antisnipe_triggered = False
    if lot.ends_at and not is_blitz:
        ends_at = lot.ends_at
        if ends_at.tzinfo is None:
            ends_at = ends_at.replace(tzinfo=timezone.utc)
        new_ends_at = await apply_antisnipe(lot_id, ends_at, bot)
        if new_ends_at != ends_at:
            antisnipe_triggered = True
            lot = await get_lot(lot_id)

    if not is_blitz and lot.blitz_price and amount >= lot.blitz_price:
        is_blitz = True

    # ── БЛИЦ ──────────────────────────────────────────────────
    if is_blitz and lot.blitz_price and amount >= lot.blitz_price:
        from db.queries import finish_lot
        from utils.scheduler import cancel_auction_job
        from utils.formatting import winner_text

        await finish_lot(lot_id, user_id, username or "", amount)
        lot = await get_lot(lot_id)
        cancel_auction_job(lot_id)
        winner_name = f"@{username}" if username else f"id{user_id}"

        await _update_group_card(bot, lot, bid_count, finished=True)

        await reply_fn(
            bid_accepted_text(lot, amount, is_blitz=True),
            reply_markup=kb_rating(lot_id),
            parse_mode="HTML",
        )
        if callback:
            await callback.answer("🔥 Блиц! Вы победили!")

        try:
            await bot.send_message(
                chat_id=user_id,
                text=winner_text(lot, amount),
                reply_markup=kb_winner(lot_id),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.debug(f"Winner DM failed: {e}")

        await _notify_watchers_finish(bot, lot, amount, user_id)
        return

    # ── ОБЫЧНАЯ СТАВКА ────────────────────────────────────────
    antisnipe_note = "\n\n⏱ <i>Антиснайпинг: таймер продлён на 2 мин</i>" if antisnipe_triggered else ""

    await _update_group_card(bot, lot, bid_count)

    await reply_fn(
        bid_accepted_text(lot, amount) + antisnipe_note,
        reply_markup=kb_after_bid(lot_id),
        parse_mode="HTML",
    )
    if callback:
        await callback.answer("✅ Ставка принята!")

    await add_to_watchlist(lot_id, user_id, username)

    if prev_leader_id and prev_leader_id != user_id:
        try:
            await bot.send_message(
                chat_id=prev_leader_id,
                text=overbid_notify_text(lot, amount),
                reply_markup=kb_overbid(lot_id, amount, lot.bid_step),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.debug(f"Overbid notify failed: {e}")


async def _update_group_card(bot, lot, bid_count: int, finished: bool = False):
    from config import GROUP_ID
    from db.queries import get_top_bid
    from utils.formatting import lot_card_text, auction_finished_text

    if not GROUP_ID or not lot.topic_id or not lot.card_message_id:
        return

    top_bid = await get_top_bid(lot.id)

    if finished and top_bid:
        text = auction_finished_text(lot, top_bid.amount)
        reply_markup = None
    else:
        text = lot_card_text(lot, bid_count, top_bid)
        reply_markup = kb_lot_card(lot)

    try:
        if lot.client_photo_file_id:
            await bot.edit_message_caption(
                chat_id=GROUP_ID,
                message_id=lot.card_message_id,
                caption=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
        else:
            await bot.edit_message_text(
                chat_id=GROUP_ID,
                message_id=lot.card_message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
    except Exception as e:
        logger.debug(f"Card update failed: {e}")


async def _notify_watchers_finish(bot, lot, final_price: int, winner_id: int):
    watchers = await get_watchers(lot.id)
    for w in watchers:
        if w.user_id == winner_id:
            continue
        try:
            await bot.send_message(
                chat_id=w.user_id,
                text=(
                    f"🏁 <b>Аукцион завершён</b>\n\n"
                    f"{lot.emoji} {lot.title}\n"
                    f"Финальная цена: {fmt_price(final_price)}"
                ),
                reply_markup=kb_back_to_start(),
                parse_mode="HTML",
            )
        except Exception:
            pass


```


## File: auction_admin_bot\handlers\create_lot.py
```python
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS, MIN_BID_STEP
from db.queries import create_lot
from keyboards.inline import (
    kb_bid_step, kb_confirm_lot,
    kb_duration, kb_main_menu,
)
from utils.formatting import fmt_price, fmt_duration
from utils.guards import admin_only_callback, admin_only_message
from utils.states import CreateLotFSM
import texts as T

router = Router()

DEFAULT_EMOJI = "🏷"
DEFAULT_CATEGORY = "Аукцион"


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


@router.message(CreateLotFSM.entering_title)
async def msg_title(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    title = message.text.strip()
    if len(title) < 3:
        await message.answer(T.CREATE_TITLE_TOO_SHORT)
        return
    await state.update_data(title=title)
    await state.set_state(CreateLotFSM.entering_price)
    await message.answer(T.CREATE_TITLE_OK.format(title=title), parse_mode="HTML")


@router.message(CreateLotFSM.entering_price)
async def msg_price(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = message.text.strip().replace(" ", "").replace("\u202f", "")
    if not raw.isdigit() or int(raw) < 1000:
        await message.answer(T.CREATE_PRICE_INVALID)
        return
    price = int(raw)
    await state.update_data(start_price=price)
    await state.set_state(CreateLotFSM.choosing_step)
    await message.answer(T.CREATE_PRICE_OK.format(price=fmt_price(price)), reply_markup=kb_bid_step(), parse_mode="HTML")


@router.callback_query(F.data.startswith("step:"), CreateLotFSM.choosing_step)
async def cb_step(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    value = callback.data.split(":")[1]
    if value == "custom":
        await state.set_state(CreateLotFSM.entering_step)
        await callback.message.edit_text(T.CREATE_STEP_ENTER, parse_mode="HTML")
    else:
        step = int(value)
        await state.update_data(bid_step=step)
        await state.set_state(CreateLotFSM.choosing_duration)
        await callback.message.edit_text(
            T.CREATE_STEP_OK.format(step=fmt_price(step)),
            reply_markup=kb_duration(), parse_mode="HTML",
        )
    await callback.answer()


@router.message(CreateLotFSM.entering_step)
async def msg_step(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = message.text.strip().replace(" ", "")
    if not raw.isdigit() or int(raw) < MIN_BID_STEP:
        await message.answer(T.CREATE_STEP_MIN.format(min_step=MIN_BID_STEP))
        return
    step = int(raw)
    await state.update_data(bid_step=step)
    await state.set_state(CreateLotFSM.choosing_duration)
    await message.answer(
        T.CREATE_STEP_OK.format(step=fmt_price(step)),
        reply_markup=kb_duration(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("dur:"), CreateLotFSM.choosing_duration)
async def cb_duration(callback: CallbackQuery, state: FSMContext):
    if not await admin_only_callback(callback):
        return
    value = callback.data.split(":")[1]
    if value == "custom":
        await state.set_state(CreateLotFSM.entering_duration)
        await callback.message.edit_text(
            "Введите длительность аукциона в часах (целое число, от 1 до 720):",
            parse_mode="HTML",
        )
        await callback.answer()
        return
    hours = float(value)
    await state.update_data(duration_hours=hours, blitz_price=None)
    await state.set_state(CreateLotFSM.entering_desc)
    await callback.message.edit_text(
        T.CREATE_DURATION_OK.format(hours=fmt_duration(hours)),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(CreateLotFSM.entering_duration)
async def msg_duration(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    raw = message.text.strip()
    if not raw.isdigit() or not (1 <= int(raw) <= 720):
        await message.answer("Введите целое число от 1 до 720.")
        return
    hours = int(raw)
    await state.update_data(duration_hours=hours, blitz_price=None)
    await state.set_state(CreateLotFSM.entering_desc)
    await message.answer(T.CREATE_DURATION_OK.format(hours=fmt_duration(hours)), parse_mode="HTML")


@router.message(CreateLotFSM.entering_desc)
async def msg_desc(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    desc = message.text.strip()
    await state.update_data(description=desc)
    await state.set_state(CreateLotFSM.uploading_photo)
    await message.answer(T.CREATE_PHOTO_PROMPT, parse_mode="HTML")


@router.message(CreateLotFSM.uploading_photo)
async def msg_photo(message: Message, state: FSMContext):
    if not await admin_only_message(message):
        return
    if message.text and message.text.strip() == "/skip":
        await state.update_data(photo_file_id=None)
    elif message.photo:
        file_id = message.photo[-1].file_id
        data = await state.get_data()
        desc = data.get("description") or "—"
        CAPTION_LIMIT = 1024
        CARD_OVERHEAD = 200
        if len(desc) > CAPTION_LIMIT - CARD_OVERHEAD:
            max_len = CAPTION_LIMIT - CARD_OVERHEAD
            await message.answer(
                f"⚠️ Описание слишком длинное для лота с фото.\n\n"
                f"Максимум: <b>{max_len} символов</b>\n"
                f"Сейчас: <b>{len(desc)} символов</b>\n\n"
                f"Вернитесь и сократите описание — нажмите /start чтобы начать заново.",
                parse_mode="HTML",
            )
            return
        await state.update_data(photo_file_id=file_id)
    else:
        await message.answer(T.CREATE_PHOTO_INVALID)
        return
    await state.set_state(CreateLotFSM.choosing_start_time)
    from keyboards.inline import kb_start_time
    await message.answer(T.CREATE_START_TIME_PROMPT, reply_markup=kb_start_time())


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
    m = re.match(r"^(\d{1,2})\.(\d{1,2})\s+(\d{1,2}):(\d{2})$", raw)
    if not m:
        await message.answer(
            "Неверный формат. Введите дату и время так:\n<code>25.03 15:00</code>",
            parse_mode="HTML",
        )
        return
    day, month, hour, minute = int(m[1]), int(m[2]), int(m[3]), int(m[4])
    now_msk = datetime.now(timezone(timedelta(hours=3)))
    year = now_msk.year
    try:
        msk = datetime(year, month, day, hour, minute, tzinfo=timezone(timedelta(hours=3)))
        if msk < now_msk:
            msk = msk.replace(year=year + 1)
    except ValueError:
        await message.answer(T.CREATE_START_TIME_DATE_ERR)
        return
    utc = msk.astimezone(timezone.utc)
    if utc <= datetime.now(timezone.utc):
        await message.answer("❌ Указанное время уже прошло. Введите время <b>в будущем</b>.", parse_mode="HTML")
        return
    await state.update_data(starts_at=utc.isoformat())
    await state.set_state(CreateLotFSM.confirming)
    data = await state.get_data()
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
        f"• Длительность: {fmt_duration(data['duration_hours'])}\n\n"
        f"<i>Лот будет опубликован в Мини Апп 📱</i>"
    )
    kb = kb_confirm_lot()
    if edit:
        if getattr(target, "photo", None):
            await target.edit_caption(caption=text, reply_markup=kb, parse_mode="HTML")
        else:
            await target.edit_text(text, reply_markup=kb, parse_mode="HTML")
        return
    await target.answer(text, reply_markup=kb, parse_mode="HTML")


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
    await _do_launch_miniapp(callback, lot, starts_at_iso=data.get("starts_at"))
    await callback.answer()


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


async def _do_launch_miniapp(callback, lot, starts_at_iso: str = None):
    from datetime import datetime, timedelta, timezone
    from db.queries import launch_lot, schedule_lot
    from utils.scheduler import schedule_auction_finish, schedule_lot_start
    from keyboards.inline import kb_monitor
    import logging
    logger = logging.getLogger(__name__)

    bot = callback.bot
    logger.info(f"_do_launch_miniapp: lot_id={lot.id}, starts_at_iso={starts_at_iso!r}")

    if starts_at_iso:
        starts_at = datetime.fromisoformat(starts_at_iso)
        lot = await schedule_lot(lot.id, topic_id=0, starts_at=starts_at)
        schedule_lot_start(lot.id, starts_at, bot)
        msk = starts_at.astimezone(timezone(timedelta(hours=3)))
        reply_text = (
            f"🕐 <b>Аукцион запланирован!</b>\n\n"
            f"<code>{lot.lot_code}</code>\n\n"
            f"{lot.emoji} <b>{lot.title}</b>\n"
            f"Старт: <b>{msk.strftime('%d.%m в %H:%M')} МСК</b>\n"
            f"Длительность: {fmt_duration(lot.duration_hours)}\n\n"
            f"<i>Лот появится в Мини Апп в указанное время 📱</i>"
        )
    else:
        ends_at = datetime.now(timezone.utc) + timedelta(hours=lot.duration_hours)
        lot = await launch_lot(lot.id, topic_id=0, ends_at=ends_at)
        schedule_auction_finish(lot.id, ends_at, bot)
        reply_text = (
            f"🚀 <b>Аукцион запущен в Мини Апп!</b>\n\n"
            f"<code>{lot.lot_code}</code>\n\n"
            f"{lot.emoji} <b>{lot.title}</b>\n"
            f"Стартовая цена: <b>{fmt_price(lot.start_price)}</b>\n"
            f"Длительность: {fmt_duration(lot.duration_hours)}\n\n"
            f"<i>Участники видят лот в Мини Апп 📱</i>"
        )

    kb = kb_monitor(lot.id)
    if callback.message.photo:
        await callback.message.edit_caption(caption=reply_text, reply_markup=kb, parse_mode="HTML")
    else:
        await callback.message.edit_text(reply_text, reply_markup=kb, parse_mode="HTML")
```


## File: auction_admin_bot\handlers\finish.py
```python
import texts as T
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_bid_count, get_lot, get_unique_bidder_count
from keyboards.inline import kb_back_to_main, kb_winner
from utils.formatting import report_text
from utils.guards import admin_only_callback

router = Router()


@router.callback_query(F.data.startswith("win:report:"))
async def cb_report(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer(T.MANAGE_LOT_NOT_FOUND, show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    await callback.message.edit_text(
        report_text(lot, bid_count, user_count),
        reply_markup=kb_back_to_main(),
        parse_mode="HTML",
    )
    await callback.answer()


```


## File: auction_admin_bot\handlers\lots.py
```python
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import (
    get_active_lots, get_bid_count, get_lot,
    get_top_bid, get_unique_bidder_count, is_watching,
)
from keyboards.inline import kb_lot_card_dm, kb_lots_list
from utils.formatting import lot_card_text, lot_detail_text, lot_list_text

router = Router()


# ── Lots list ─────────────────────────────────────────────────

@router.callback_query(F.data == "lots:list")
async def cb_lots_list(callback: CallbackQuery):
    lots = await get_active_lots()
    text = lot_list_text(lots)
    try:
        await callback.message.edit_text(
            text,
            reply_markup=kb_lots_list(lots),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer()


# ── Open lot card ─────────────────────────────────────────────

@router.callback_query(F.data.startswith("lot:view:"))
async def cb_view_lot(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    top_bid = await get_top_bid(lot_id)
    watching = await is_watching(lot_id, callback.from_user.id)

    user_is_leader = top_bid and top_bid.user_id == callback.from_user.id

    text = lot_card_text(lot, bid_count, top_bid, watching)
    kb = kb_lot_card_dm(lot, watching=watching)

    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer()


# ── Lot details ───────────────────────────────────────────────

@router.callback_query(F.data.startswith("lot:detail:"))
async def cb_lot_detail(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="← Назад к карточке", callback_data=f"lot:view:{lot_id}"))

    try:
        await callback.message.edit_text(
            lot_detail_text(lot, bid_count, user_count),
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer()


```


## File: auction_admin_bot\handlers\main_menu.py
```python
import texts as T
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS
from db.queries import get_active_lots, get_stats, get_finished_lots
from keyboards.inline import kb_active_lots, kb_back_to_main, kb_main_menu, kb_finished_lots
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
            T.ADMIN_NO_ACTIVE_LOTS,
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


# ── Finished lots ─────────────────────────────────────────────

PAGE_SIZE = 8

async def _render_finished(callback: CallbackQuery, page: int = 0):
    from utils.formatting import fmt_price
    lots, total = await get_finished_lots(limit=PAGE_SIZE, offset=page * PAGE_SIZE)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    if not lots:
        await callback.message.edit_text(
            T.ADMIN_NO_FINISHED_LOTS,
            reply_markup=kb_main_menu(),
            parse_mode="HTML",
        )
        return

    lines = []
    for lot in lots:
        winner = f"@{lot.winner_username}" if lot.winner_username else (
            f"id{lot.winner_user_id}" if lot.winner_user_id else "нет ставок"
        )
        price = fmt_price(lot.final_price or lot.current_price)
        lines.append(f"{lot.emoji} <b>{lot.title}</b>\n   💰 {price}  ·  🏆 {winner}")

    text = (
        f"🏁 <b>Завершённые лоты</b>  "
        f"<i>({page * PAGE_SIZE + 1}–{min((page+1) * PAGE_SIZE, total)} из {total})</i>\n\n"
        + "\n\n".join(lines)
    )
    await callback.message.edit_text(
        text,
        reply_markup=kb_finished_lots(lots, page, total_pages),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "menu:finished_lots")
async def cb_finished_lots(callback: CallbackQuery):
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


@router.callback_query(F.data.startswith("finished:open:"))
async def cb_finished_open(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from db.queries import get_lot, get_bid_count, get_unique_bidder_count
    from utils.formatting import report_text
    from keyboards.inline import kb_back_to_main
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton

    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer(T.MANAGE_LOT_NOT_FOUND, show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)
    text = report_text(lot, bid_count, user_count)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📜 Все ставки", callback_data=f"mon:bids:{lot_id}"))
    builder.row(InlineKeyboardButton(text=T.KB_BACK, callback_data="menu:finished_lots"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


```


## File: auction_admin_bot\handlers\manage.py
```python
"""
auction_admin_bot/handlers/manage.py
──────────────────────────────────────
Изменения по сравнению с оригиналом:
  1. cb_ban_confirm — после аннулирования ставок забаненного
     новый лидер получает уведомление «Вы снова лидируете!»
     (через winner_bot / клиентский бот).
  2. После бана карточка лота в топике обновляется через _update_group_card.
  Остальное без изменений.
"""
from datetime import datetime, timedelta, timezone

from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.database import LotStatus
from db.queries import (
    ban_user, cancel_lot, cancel_user_bids, extend_lot,
    get_bid_count, get_bidders_for_lot, get_lot, get_top_bid,
    get_unique_bidder_count, pause_lot, resume_lot,
)
from keyboards.inline import (
    kb_ban_confirm, kb_ban_pick, kb_back_to_main, kb_confirm_action,
    kb_extend_pick, kb_manage, kb_manage_paused, kb_monitor,
)
from utils.formatting import fmt_price, fmt_time_left
from utils.guards import admin_only_callback
from utils.scheduler import cancel_auction_job, schedule_auction_finish

router = Router()


# ── Open manage panel ─────────────────────────────────────────

@router.callback_query(F.data.startswith("mon:manage:"))
async def cb_open_manage(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _show_manage(callback, lot_id)
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:menu:"))
async def cb_manage_menu(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _show_manage(callback, lot_id)
    await callback.answer()


async def _show_manage(callback: CallbackQuery, lot_id: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    bid_count = await get_bid_count(lot_id)
    top_bid   = await get_top_bid(lot_id)
    leader = (
        f"@{top_bid.username}" if (top_bid and top_bid.username)
        else (f"id{top_bid.user_id}" if top_bid else "нет ставок")
    )
    text = (
        f"⚙️ <b>Управление · {lot.emoji} {lot.title}</b>\n\n"
        f"Статус: {'⏸ на паузе' if lot.status == LotStatus.PAUSED else '🟢 активен'}\n"
        f"Цена: <b>{fmt_price(lot.current_price)}</b>  ·  {bid_count} ставок\n"
        f"Лидер: {leader}\n"
        f"Осталось: {fmt_time_left(lot.ends_at)}"
    )
    kb = kb_manage_paused(lot_id) if lot.status == LotStatus.PAUSED else kb_manage(lot_id)
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass


# ── Pause ─────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:pause:"))
async def cb_pause(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot    = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        await callback.answer("Нельзя поставить на паузу.", show_alert=True)
        return

    now = datetime.now(timezone.utc)
    seconds_left = max(0, int((lot.ends_at - now).total_seconds())) if lot.ends_at else 0
    await pause_lot(lot_id, seconds_left)
    cancel_auction_job(lot_id)

    await _notify_group(callback, lot, "⏸ Аукцион временно приостановлен.")

    await callback.message.edit_text(
        f"⏸ <b>Аукцион приостановлен.</b>\n\n"
        f"Таймер остановлен. Ставки заморожены.\n"
        f"Осталось: {seconds_left // 3600}ч {(seconds_left % 3600) // 60}м",
        reply_markup=kb_manage_paused(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("⏸ Приостановлен")


# ── Resume ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:resume:"))
async def cb_resume(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot    = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.PAUSED:
        await callback.answer("Лот не на паузе.", show_alert=True)
        return

    secs        = lot.seconds_left or 3600
    new_ends_at = datetime.now(timezone.utc) + timedelta(seconds=secs)
    await resume_lot(lot_id, new_ends_at)

    from config import GROUP_BOT_TOKEN
    from aiogram import Bot as AiogramBot
    winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
    schedule_auction_finish(lot_id, new_ends_at, callback.bot, winner_bot)

    await _notify_group(callback, lot, "▶️ Аукцион возобновлён.")

    await callback.message.edit_text(
        f"▶️ <b>Аукцион возобновлён!</b>\n\n"
        f"Таймер продолжается. Новое время окончания: {fmt_time_left(new_ends_at)}",
        reply_markup=kb_monitor(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("▶️ Возобновлён")


# ── Extend ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:extend2:"))
async def cb_extend_2h(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _do_extend(callback, lot_id, 2)


@router.callback_query(F.data.startswith("mgmt:extend_pick:"))
async def cb_extend_pick(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "⏱ <b>Выберите, на сколько продлить:</b>",
        reply_markup=kb_extend_pick(lot_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:extend:"))
async def cb_extend_hours(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts  = callback.data.split(":")
    lot_id = int(parts[2])
    hours  = int(parts[3])
    await _do_extend(callback, lot_id, hours)


async def _do_extend(callback: CallbackQuery, lot_id: int, hours: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    base        = lot.ends_at or datetime.now(timezone.utc)
    new_ends_at = base + timedelta(hours=hours)
    await extend_lot(lot_id, new_ends_at)

    if lot.status == LotStatus.ACTIVE:
        from config import GROUP_BOT_TOKEN
        from aiogram import Bot as AiogramBot
        winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
        schedule_auction_finish(lot_id, new_ends_at, callback.bot, winner_bot)

    await _notify_group(callback, lot, f"⏱ Время аукциона продлено на {hours}ч.")

    await callback.message.edit_text(
        f"✅ <b>Время продлено на {hours}ч.</b>\n\n"
        f"Новое время окончания: {fmt_time_left(new_ends_at)}\n"
        f"Участники уведомлены.",
        reply_markup=kb_manage(lot_id),
        parse_mode="HTML",
    )
    await callback.answer(f"+{hours}ч добавлено")


# ── Cancel lot ────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:cancel:"))
async def cb_cancel_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "⚠️ <b>Подтвердите отмену лота</b>\n\n"
        "Все ставки будут аннулированы. Участники получат уведомление.",
        reply_markup=kb_confirm_action(
            yes_cb=f"mgmt:cancel_confirm:{lot_id}",
            no_cb=f"mgmt:menu:{lot_id}",
        ),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:cancel_confirm:"))
async def cb_cancel_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot    = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    await cancel_lot(lot_id)
    cancel_auction_job(lot_id)
    bid_count = await get_bid_count(lot_id)

    await _notify_group(callback, lot, "🚫 Аукцион отменён администратором.")

    await callback.message.edit_text(
        f"🚫 Лот <code>{lot.lot_code}</code> <b>отменён</b>.\n\n"
        f"Топик #{lot.topic_id} закрыт. {bid_count} участников уведомлены.",
        reply_markup=kb_back_to_main(),
        parse_mode="HTML",
    )
    await callback.answer("Лот отменён")


# ── Early finish ──────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:early_finish:"))
async def cb_early_finish_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id  = int(callback.data.split(":")[2])
    lot     = await get_lot(lot_id)
    top_bid = await get_top_bid(lot_id)
    price_line = f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>" if lot else ""
    leader = ""
    if top_bid:
        name   = f"@{top_bid.username}" if top_bid.username else f"id{top_bid.user_id}"
        leader = f"\nЛидер: <b>{name}</b>"

    await callback.message.edit_text(
        f"⚠️ <b>Завершить аукцион досрочно?</b>\n\n"
        f"Победителем становится текущий лидер.\n"
        f"{price_line}{leader}",
        reply_markup=kb_confirm_action(
            yes_cb=f"mgmt:early_confirm:{lot_id}",
            no_cb=f"mgmt:menu:{lot_id}",
        ),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:early_confirm:"))
async def cb_early_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])

    from utils.scheduler import _finish_auction_job
    cancel_auction_job(lot_id)

    lot = await get_lot(lot_id)
    if lot and lot.status == LotStatus.PAUSED:
        from db.queries import resume_lot
        await resume_lot(lot_id, datetime.now(timezone.utc))

    from config import GROUP_BOT_TOKEN
    from aiogram import Bot as AiogramBot
    group_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
    try:
        await _finish_auction_job(lot_id, callback.bot, winner_bot=group_bot, force=True)
    finally:
        if group_bot:
            await group_bot.session.close()

    lot       = await get_lot(lot_id)
    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    from utils.formatting import winner_text
    from keyboards.inline import kb_winner
    await callback.message.edit_text(
        winner_text(lot, bid_count, user_count),
        reply_markup=kb_winner(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("Завершено")


# ── Ban user ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:ban_pick:"))
async def cb_ban_pick(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id  = int(callback.data.split(":")[2])
    bidders = await get_bidders_for_lot(lot_id)
    if not bidders:
        await callback.answer("Нет участников для блокировки.", show_alert=True)
        return
    await callback.message.edit_text(
        "👤 <b>Выберите участника для блокировки:</b>",
        reply_markup=kb_ban_pick(lot_id, bidders),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ban:user:"))
async def cb_ban_user_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts   = callback.data.split(":")
    lot_id  = int(parts[2])
    user_id = int(parts[3])
    bidders = await get_bidders_for_lot(lot_id)
    target  = next((b for b in bidders if b["user_id"] == user_id), None)
    name    = (
        f"@{target['username']}" if (target and target["username"])
        else f"id{user_id}"
    )
    await callback.message.edit_text(
        f"⚠️ <b>Подтвердите блокировку</b>\n\n"
        f"Пользователь: {name}\n"
        f"Все ставки по этому лоту будут аннулированы.",
        reply_markup=kb_ban_confirm(lot_id, user_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ban:confirm:"))
async def cb_ban_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts   = callback.data.split(":")
    lot_id  = int(parts[2])
    user_id = int(parts[3])

    # 1. Аннулировать ставки забаненного
    await cancel_user_bids(lot_id, user_id)

    # 2. Пересчитать текущую цену
    top_bid = await get_top_bid(lot_id)
    lot     = await get_lot(lot_id)
    if lot and top_bid:
        from sqlalchemy import update as sa_update
        from db.database import AsyncSessionLocal, Lot as LotModel
        async with AsyncSessionLocal() as s:
            await s.execute(
                sa_update(LotModel)
                .where(LotModel.id == lot_id)
                .values(current_price=top_bid.amount)
            )
            await s.commit()
    elif lot and not top_bid:
        # Ставок не осталось — сбросить до стартовой цены
        from sqlalchemy import update as sa_update
        from db.database import AsyncSessionLocal, Lot as LotModel
        async with AsyncSessionLocal() as s:
            await s.execute(
                sa_update(LotModel)
                .where(LotModel.id == lot_id)
                .values(current_price=lot.start_price)
            )
            await s.commit()

    # 3. Добавить в список забаненных
    bidders  = await get_bidders_for_lot(lot_id)
    username = None
    for b in bidders:
        if b["user_id"] == user_id:
            username = b["username"]
            break
    await ban_user(user_id, username, callback.from_user.id)

    # 4. Кикнуть из группы
    try:
        from config import GROUP_ID
        await callback.bot.ban_chat_member(chat_id=GROUP_ID, user_id=user_id)
    except Exception:
        pass

    # ── НОВОЕ: уведомить нового лидера и обновить карточку ──────────────────
    lot = await get_lot(lot_id)  # свежие данные после обновления цены

    # 5. Уведомить нового лидера (если он есть)
    if top_bid and lot:
        try:
            from config import GROUP_BOT_TOKEN
            from aiogram import Bot as AiogramBot
            notify_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else callback.bot

            new_leader_name = (
                f"@{top_bid.username}" if top_bid.username else f"id{top_bid.user_id}"
            )
            await notify_bot.send_message(
                chat_id=top_bid.user_id,
                text=(
                    f"🏆 <b>Вы снова лидируете!</b>\n\n"
                    f"{lot.emoji} {lot.title}\n"
                    f"<code>{lot.lot_code}</code>\n\n"
                    f"Участник был заблокирован, его ставки аннулированы.\n"
                    f"Текущая цена: <b>{fmt_price(top_bid.amount)}</b>"
                ),
                parse_mode="HTML",
            )
            if GROUP_BOT_TOKEN:
                await notify_bot.session.close()
        except Exception as e:
            import logging as _logging
            _logging.getLogger(__name__).debug(
                f"New leader notify after ban failed: {e}"
            )

    # 6. Обновить карточку в топике группы
    if lot:
        try:
            from config import GROUP_ID, GROUP_BOT_TOKEN
            from aiogram import Bot as AiogramBot
            from utils.formatting import lot_card_text
            from keyboards.inline import kb_lot_card

            card_bot = (
                AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN
                else callback.bot
            )
            bid_count = await get_bid_count(lot_id)
            fresh_top  = await get_top_bid(lot_id)

            if GROUP_ID and lot.topic_id and lot.card_message_id:
                text = lot_card_text(lot, bid_count, fresh_top)
                kb   = kb_lot_card(lot)
                if lot.client_photo_file_id:
                    await card_bot.edit_message_caption(
                        chat_id=GROUP_ID,
                        message_id=lot.card_message_id,
                        caption=text,
                        reply_markup=kb,
                        parse_mode="HTML",
                    )
                else:
                    await card_bot.edit_message_text(
                        chat_id=GROUP_ID,
                        message_id=lot.card_message_id,
                        text=text,
                        reply_markup=kb,
                        parse_mode="HTML",
                    )
            if GROUP_BOT_TOKEN:
                await card_bot.session.close()
        except Exception as e:
            import logging as _logging
            _logging.getLogger(__name__).debug(f"Card update after ban failed: {e}")
    # ── конец нового блока ───────────────────────────────────────────────────

    name = f"@{username}" if username else f"id{user_id}"
    await callback.message.edit_text(
        f"🚫 <b>{name} заблокирован.</b>\n\n"
        f"• Ставки аннулированы\n"
        f"• Участник исключён из группы\n"
        f"• Лидерство пересчитано\n"
        f"• Новый лидер уведомлён",
        reply_markup=kb_manage(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("Заблокирован")


# ── Helper: notify group topic ─────────────────────────────────

async def _notify_group(callback: CallbackQuery, lot, text: str):
    from config import GROUP_ID
    if not GROUP_ID or not lot.topic_id:
        return
    try:
        await callback.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=lot.topic_id,
            text=text,
        )
    except Exception:
        pass

```


## File: auction_admin_bot\handlers\monitor.py
```python
import texts as T
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_bid_count, get_lot, get_recent_bids, get_top_bid, get_unique_bidder_count
from keyboards.inline import kb_monitor
from utils.formatting import monitor_text
from utils.guards import admin_only_callback

router = Router()


async def _render_monitor(callback: CallbackQuery, lot_id: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer(T.MANAGE_LOT_NOT_FOUND, show_alert=True)
        return

    top_bid = await get_top_bid(lot_id)
    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)
    recent = await get_recent_bids(lot_id, 5)

    text = monitor_text(lot, bid_count, user_count, top_bid, recent)

    try:
        await callback.message.edit_text(
            text,
            reply_markup=kb_monitor(lot_id),
            parse_mode="HTML",
        )
    except Exception:
        pass  # "message not modified" — ignore


# Open monitor from lot list
@router.callback_query(F.data.startswith("lot:open:"))
async def cb_open_lot(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _render_monitor(callback, lot_id)
    await callback.answer()


# Refresh button
@router.callback_query(F.data.startswith("mon:refresh:"))
async def cb_refresh(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _render_monitor(callback, lot_id)
    await callback.answer(T.MANAGE_REFRESHED)


# Bid history
@router.callback_query(F.data.startswith("mon:bids:"))
async def cb_bid_history(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    from db.queries import get_lot_bids
    from utils.formatting import fmt_price
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    from datetime import timezone, timedelta

    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer(T.MANAGE_LOT_NOT_FOUND, show_alert=True)
        return

    bids = await get_lot_bids(lot_id)

    if not bids:
        await callback.answer("Ставок пока нет.", show_alert=True)
        return

    msk = timezone(timedelta(hours=3))
    lines = []
    for i, bid in enumerate(bids, 1):
        user = f"@{bid.username}" if bid.username else f"id{bid.user_id}"
        time_str = bid.created_at.astimezone(msk).strftime("%d.%m %H:%M")
        lines.append(f"{i}. <b>{fmt_price(bid.amount)}</b> — {user} <i>{time_str}</i>")

    text = (
        f"📜 <b>История ставок</b>\n"
        f"{lot.emoji} {lot.title}\n\n"
        + "\n".join(lines)
    )

    builder = InlineKeyboardBuilder()
    if lot.status == "finished":
        builder.row(InlineKeyboardButton(text=T.KB_BACK, callback_data=f"finished:open:{lot_id}"))
    else:
        builder.row(InlineKeyboardButton(text="← Мониторинг", callback_data=f"lot:open:{lot_id}"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


```


## File: auction_admin_bot\handlers\notifications.py
```python
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_lot, save_rating
from keyboards.inline import kb_rating, kb_back_to_start
from utils.formatting import fmt_price

router = Router()


# ── Winner confirms purchase ───────────────────────────────────

@router.callback_query(F.data.startswith("win:confirm:"))
async def cb_win_confirm(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    username = callback.from_user.username
    name = f"@{username}" if username else f"id{callback.from_user.id}"

    # Notify group that winner confirmed
    from config import GROUP_ID
    if GROUP_ID and lot.topic_id:
        try:
            await callback.bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=lot.topic_id,
                text=f"✅ Победитель {name} подтвердил покупку.",
                parse_mode="HTML",
            )
        except Exception:
            pass

    await callback.message.edit_text(
        f"✅ <b>Покупка подтверждена!</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"Итоговая цена: <b>{fmt_price(lot.final_price or 0)}</b>\n\n"
        f"👤 <b>Менеджер уже уведомлён</b> и свяжется с вами в ближайшее время.\n\n"
        f"Пожалуйста, оцените ваш опыт участия в аукционе:",
        reply_markup=kb_rating(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("✅ Подтверждено!")


# ── Rating ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("rate:"))
async def cb_rate(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id, stars = int(parts[1]), int(parts[2])

    await save_rating(lot_id, callback.from_user.id, stars)

    emoji = "🙌" if stars >= 4 else "🙏" if stars >= 3 else "😔"
    star_str = "⭐" * stars

    lots = await __import__("db.queries", fromlist=["get_active_lots"]).get_active_lots()

    await callback.message.edit_text(
        f"Спасибо за оценку! {star_str} {emoji}\n\n"
        f"До следующего аукциона! Следите за новыми лотами в группе.",
        reply_markup=kb_back_to_start(),
        parse_mode="HTML",
    )
    await callback.answer(f"Оценка {stars}/5 принята!")


```


## File: auction_admin_bot\handlers\welcome.py
```python
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.type != "private":
        return

    await message.answer(
        "👋 <b>Привет!</b>\n\n"
        "Этот бот обслуживает аукцион.\n\n"
        "• Все лоты и ставки — в <b>топиках группы</b>\n"
        "• Сюда придут уведомления если вашу ставку перебьют или вы победите\n"
        "• Здесь же вводится произвольная сумма ставки\n\n"
        "<i>Перейдите в группу и выберите интересующий лот.</i>",
        parse_mode="HTML",
    )


```


## File: auction_admin_bot\keyboards\inline.py
```python
import texts as T
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# ── Main menu ─────────────────────────────────────────────────

def kb_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=T.KB_CREATE,   callback_data="menu:create"))
    builder.row(InlineKeyboardButton(text=T.KB_ACTIVE_LOTS,       callback_data="menu:active_lots"))
    builder.row(InlineKeyboardButton(text=T.KB_FINISHED_LOTS,    callback_data="menu:finished_lots"))
    return builder.as_markup()


# ── Create lot — start time ───────────────────────────────────

def kb_start_time() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=T.KB_START_NOW, callback_data="start:now"))
    builder.row(InlineKeyboardButton(text=T.KB_START_CUSTOM,  callback_data="start:custom"))
    builder.row(InlineKeyboardButton(text=T.KB_CANCEL_ACTION,                callback_data="menu:main"))
    return builder.as_markup()


# ── Create lot — bid step ─────────────────────────────────────

def kb_bid_step() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="+ 1 000 ₽",  callback_data="step:1000"))
    builder.add(InlineKeyboardButton(text="+ 5 000 ₽",  callback_data="step:5000"))
    builder.add(InlineKeyboardButton(text="+ 10 000 ₽", callback_data="step:10000"))
    builder.adjust(3)
    builder.row(InlineKeyboardButton(text="✏️ Свой шаг", callback_data="step:custom"))
    builder.row(InlineKeyboardButton(text=T.KB_CANCEL_ACTION,    callback_data="menu:main"))
    return builder.as_markup()


# ── Create lot — duration ─────────────────────────────────────

def kb_duration() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⏱ 3м",  callback_data="dur:0.05"))
    builder.add(InlineKeyboardButton(text="⏱ 6ч",  callback_data="dur:6"))
    builder.add(InlineKeyboardButton(text="⏱ 12ч", callback_data="dur:12"))
    builder.add(InlineKeyboardButton(text="⏱ 24ч", callback_data="dur:24"))
    builder.add(InlineKeyboardButton(text="⏱ 48ч", callback_data="dur:48"))
    builder.adjust(5)
    builder.row(InlineKeyboardButton(text="✏️ Произвольное", callback_data="dur:custom"))
    builder.row(InlineKeyboardButton(text=T.KB_CANCEL_ACTION, callback_data="menu:main"))
    return builder.as_markup()


# ── Create lot — confirm ──────────────────────────────────────

def kb_confirm_lot() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🚀 Запустить аукцион", callback_data="lot:launch"))
    builder.row(InlineKeyboardButton(text="✏️ Редактировать",     callback_data="lot:edit"))
    builder.row(InlineKeyboardButton(text="🗑 Отмена",             callback_data="menu:main"))
    return builder.as_markup()


# ── Active lots list ──────────────────────────────────────────

def kb_active_lots(lots) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lot in lots:
        builder.row(InlineKeyboardButton(
            text=f"{lot.emoji} {lot.title[:30]} — ₽{lot.current_price:,}",
            callback_data=f"lot:open:{lot.id}"
        ))
    builder.row(InlineKeyboardButton(text=T.KB_MAIN_MENU, callback_data="menu:main"))
    return builder.as_markup()


def kb_finished_lots(lots, page: int = 0, total_pages: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for lot in lots:
        builder.row(InlineKeyboardButton(
            text=f"{lot.emoji} {lot.title[:28]} — ₽{(lot.final_price or lot.current_price):,}",
            callback_data=f"finished:open:{lot.id}"
        ))
    # Пагинация
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"finished:page:{page-1}"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"finished:page:{page+1}"))
    if nav:
        builder.row(*nav)
    builder.row(InlineKeyboardButton(text=T.KB_MAIN_MENU, callback_data="menu:main"))
    return builder.as_markup()


# ── Monitor ───────────────────────────────────────────────────

def kb_monitor(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=T.KB_REFRESH,       callback_data=f"mon:refresh:{lot_id}"))
    builder.row(InlineKeyboardButton(text=T.KB_MANAGE,        callback_data=f"mon:manage:{lot_id}"))
    builder.row(InlineKeyboardButton(text="📜 История ставок", callback_data=f"mon:bids:{lot_id}"))
    builder.row(InlineKeyboardButton(text=T.KB_ALL_LOTS,      callback_data="menu:active_lots"))
    return builder.as_markup()


# ── Manage ────────────────────────────────────────────────────

def kb_manage(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=T.KB_EXTEND,       callback_data=f"mgmt:extend_pick:{lot_id}"))
    builder.row(InlineKeyboardButton(text=T.KB_EARLY_FINISH, callback_data=f"mgmt:early_finish:{lot_id}"))
    builder.row(InlineKeyboardButton(text=T.KB_CANCEL_LOT,   callback_data=f"mgmt:cancel:{lot_id}"))
    builder.row(InlineKeyboardButton(text=T.KB_MONITOR,      callback_data=f"lot:open:{lot_id}"))
    return builder.as_markup()


def kb_extend_pick(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for h in [1, 2, 6, 12, 24]:
        builder.add(InlineKeyboardButton(text=f"+{h}ч", callback_data=f"mgmt:extend:{lot_id}:{h}"))
    builder.adjust(5)
    builder.row(InlineKeyboardButton(text=T.KB_BACK, callback_data=f"mgmt:menu:{lot_id}"))
    return builder.as_markup()


def kb_confirm_action(yes_cb: str, no_cb: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Подтвердить", callback_data=yes_cb))
    builder.row(InlineKeyboardButton(text="← Нет, назад",  callback_data=no_cb))
    return builder.as_markup()


# ── Ban user pick ─────────────────────────────────────────────

def kb_ban_pick(lot_id: int, bidders: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for b in bidders[:8]:
        name = b["username"] or str(b["user_id"])
        builder.row(InlineKeyboardButton(
            text=f"🚫 @{name} — ₽{b['amount']:,}",
            callback_data=f"ban:user:{lot_id}:{b['user_id']}"
        ))
    builder.row(InlineKeyboardButton(text="← Отмена", callback_data=f"mgmt:menu:{lot_id}"))
    return builder.as_markup()


def kb_ban_confirm(lot_id: int, user_id: int) -> InlineKeyboardMarkup:
    return kb_confirm_action(
        yes_cb=f"ban:confirm:{lot_id}:{user_id}",
        no_cb=f"mgmt:ban_pick:{lot_id}",
    )


# ── Winner / finish ───────────────────────────────────────────

def kb_winner(lot_id: int) -> InlineKeyboardMarkup:
    """Кнопки для админа после завершения аукциона."""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=T.KB_REPORT,        callback_data=f"win:report:{lot_id}"))
    builder.row(InlineKeyboardButton(text="📜 Все ставки",    callback_data=f"mon:bids:{lot_id}"))
    builder.row(InlineKeyboardButton(text="➕ Новый лот",      callback_data="menu:create"))
    builder.row(InlineKeyboardButton(text=T.KB_MAIN_MENU,     callback_data="menu:main"))
    return builder.as_markup()


def kb_back_to_main() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=T.KB_MAIN_MENU, callback_data="menu:main"))
    return builder.as_markup()


# ══ Функции добавлены для совместимости с handlers ════════════
# (используются в handlers/lots.py, handlers/bidding.py,
#  handlers/notifications.py, utils/scheduler.py)

import texts as T
from db.database import Lot, LotStatus
from datetime import timezone, timedelta


def kb_manage_paused(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="▶️ Возобновить",        callback_data=f"mgmt:resume:{lot_id}"))
    builder.row(InlineKeyboardButton(text="⏹ Завершить досрочно", callback_data=f"mgmt:early_finish:{lot_id}"))
    builder.row(InlineKeyboardButton(text="← Мониторинг",          callback_data=f"lot:open:{lot_id}"))
    return builder.as_markup()


def kb_lot_card(lot: Lot) -> InlineKeyboardMarkup:
    """Клавиатура карточки лота в топике."""
    if lot.status == LotStatus.SCHEDULED and lot.starts_at:
        builder = InlineKeyboardBuilder()
        starts = lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc)
        msk = starts.astimezone(timezone(timedelta(hours=3)))
        builder.row(InlineKeyboardButton(
            text=f"🕐 Начнётся {msk.strftime('%d.%m в %H:%M')} МСК",
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
    builder.row(InlineKeyboardButton(text="✏️ Своя сумма", callback_data=f"bid:custom:{lot.id}"))
    return builder.as_markup()


def kb_lot_card_dm(lot: Lot, watching: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура карточки лота в личке."""
    builder = InlineKeyboardBuilder()
    step = lot.bid_step
    cur  = lot.current_price
    if lot.status == LotStatus.ACTIVE:
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
        InlineKeyboardButton(text=watch_text, callback_data=f"watch:toggle:{lot.id}"),
        InlineKeyboardButton(text="📋 Подробнее", callback_data=f"lot:detail:{lot.id}"),
    )
    builder.row(InlineKeyboardButton(text="← Все лоты", callback_data="lots:list"))
    return builder.as_markup()


def kb_lots_list(lots: list) -> InlineKeyboardMarkup:
    """Список лотов в личке."""
    builder = InlineKeyboardBuilder()
    for lot in lots:
        status = "🟢" if lot.status == LotStatus.ACTIVE else "🕐"
        builder.row(InlineKeyboardButton(
            text=f"{status} {lot.emoji} {lot.title[:28]} — ₽{lot.current_price:,}",
            callback_data=f"lot:view:{lot.id}",
        ))
    if not lots:
        builder.row(InlineKeyboardButton(text="Нет активных лотов", callback_data="noop"))
    return builder.as_markup()


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
    builder.row(InlineKeyboardButton(text="✏️ Своя сумма", callback_data=f"bid:custom:{lot_id}"))
    return builder.as_markup()


def kb_after_bid(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✏️ Повысить ставку", callback_data=f"bid:custom:{lot_id}"))
    return builder.as_markup()


def kb_cancel_custom_bid(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="❌ Отмена", callback_data=f"bid:custom:cancel:{lot_id}"))
    return builder.as_markup()


def kb_rating(lot_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.add(InlineKeyboardButton(text="⭐" * i, callback_data=f"rate:{lot_id}:{i}"))
    builder.adjust(5)
    return builder.as_markup()


def kb_back_to_start() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="👋 Следите за новыми лотами", callback_data="noop"))
    return builder.as_markup()


def kb_confirm_bid(lot_id: int, amount: int, is_blitz: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    confirm_text = f"{'🔥 ' if is_blitz else '✅ '}Да, ставлю {amount:,} ₽"
    builder.row(
        InlineKeyboardButton(text=confirm_text, callback_data=f"bid:confirm:{lot_id}:{amount}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data=f"bid:cancel_confirm:{lot_id}"),
    )
    return builder.as_markup()

```


## File: auction_admin_bot\utils\__init__.py
```python


```


## File: auction_admin_bot\utils\formatting.py
```python
import texts as T
from datetime import datetime, timezone
from typing import Optional

from db.database import Bid, Lot


def fmt_price(amount: int) -> str:
    return f"₽\u00A0{amount:,}".replace(",", "\u202F")


def fmt_time_left(ends_at: Optional[datetime]) -> str:
    if not ends_at:
        return "—"
    now = datetime.now(timezone.utc)
    # SQLite возвращает naive datetime — добавляем UTC
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


def lot_card_text(lot: Lot, bid_count: int, top_bid: Optional[Bid] = None) -> str:
    leader = f"@{top_bid.username}" if (top_bid and top_bid.username) else (
        f"id{top_bid.user_id}" if top_bid else "нет ставок"
    )
    blitz_line = (
        f"\n🔥 Блиц: <b>{fmt_price(lot.blitz_price)}</b>"
        if lot.blitz_price else ""
    )
    time_left = fmt_time_left(lot.ends_at)

    return (
        f"{lot.emoji} <b>{lot.title}</b>\n"
        f"<code>{lot.lot_code}</code>  ·  Топик #{lot.topic_id}\n\n"
        f"📋 {lot.description or '—'}\n\n"
        f"💰 Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"👤 Лидер: {leader}\n"
        f"📈 Шаг: {fmt_price(lot.bid_step)}\n"
        f"⏱ Осталось: {time_left}{blitz_line}\n"
        f"🔢 Ставок: {bid_count}"
    )


def monitor_text(lot: Lot, bid_count: int, user_count: int, top_bid: Optional[Bid], recent: list[Bid]) -> str:
    from datetime import datetime, timezone, timedelta
    leader = f"@{top_bid.username}" if (top_bid and top_bid.username) else (
        f"id{top_bid.user_id}" if top_bid else "нет ставок"
    )
    status_emoji = {"active": "🟢", "finished": "✅", "cancelled": "🚫", "scheduled": "🕐"}.get(lot.status, "❓")

    if lot.status == "scheduled" and lot.starts_at:
        starts = lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc)
        msk = starts.astimezone(timezone(timedelta(hours=3)))
        time_line = f"🕐 Начало: {msk.strftime('%d.%m в %H:%M')} МСК"
    else:
        time_line = f"⏱ Осталось: {fmt_time_left(lot.ends_at)}"

    feed = ""
    for b in recent:
        name = f"@{b.username}" if b.username else f"id{b.user_id}"
        feed += f"\n  {name} → {fmt_price(b.amount)}"

    return (
        f"{status_emoji} <b>Мониторинг · {lot.emoji} {lot.title}</b>\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"💰 Цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"👤 Лидер: {leader}\n"
        f"{time_line}\n"
        f"📊 Ставок: {bid_count}  ·  Участников: {user_count}\n"
        f"\n<b>Последние ставки:</b>{feed if feed else ' —'}"
    )


def winner_text(lot: Lot, bid_count: int, user_count: int) -> str:
    winner = f"@{lot.winner_username}" if lot.winner_username else f"id{lot.winner_user_id}"
    growth = 0
    if lot.start_price and lot.final_price:
        growth = round((lot.final_price / lot.start_price - 1) * 100)
    return (
        f"🏆 <b>АУКЦИОН ЗАВЕРШЁН</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"🥇 Победитель: <b>{winner}</b>\n"
        f"💰 Финальная цена: <b>{fmt_price(lot.final_price or 0)}</b>\n"
        f"📈 Старт: {fmt_price(lot.start_price)}  →  +{growth}%\n"
        f"🔢 Ставок: {bid_count}  ·  Участников: {user_count}\n"
        f"⏱ Длился: {fmt_duration(lot.duration_hours)}"
    )


def report_text(lot: Lot, bid_count: int, user_count: int) -> str:
    growth = 0
    if lot.start_price and lot.final_price:
        growth = round((lot.final_price / lot.start_price - 1) * 100)
    winner = f"@{lot.winner_username}" if lot.winner_username else (
        f"id{lot.winner_user_id}" if lot.winner_user_id else "—"
    )
    return (
        f"📊 <b>Отчёт по лоту {lot.lot_code}</b>\n\n"
        f"• Название: {lot.emoji} {lot.title}\n"
        f"• Категория: {lot.category}\n"
        f"• Описание: {lot.description or '—'}\n"
        f"• Старт: {fmt_price(lot.start_price)}\n"
        f"• Финал: {fmt_price(lot.final_price or lot.current_price)}\n"
        f"• Рост: +{growth}%\n"
        f"• Шаг: {fmt_price(lot.bid_step)}\n"
        f"• Длительность: {fmt_duration(lot.duration_hours)}\n"
        f"• Ставок: {bid_count}\n"
        f"• Участников: {user_count}\n"
        f"• Победитель: {winner}\n"
        f"• Топик: #{lot.topic_id}"
    )


def auction_finished_text(lot, final_price: int) -> str:
    """Объявление в топике — без имени победителя."""
    return T.AUCTION_FINISHED.format(
        emoji=lot.emoji,
        title=lot.title,
        lot_code=lot.lot_code,
        description=lot.description or "—",
        final_price=fmt_price(final_price),
    )



# ── Добавлено для handlers/lots.py ────────────────────────────

def lot_list_text(lots: list) -> str:
    if not lots:
        return "📭 <b>Активных лотов нет.</b>\n\nСледите за анонсами в группе."
    lines = []
    for lot in lots:
        status = "🟢" if lot.status == "active" else "🕐"
        time_line = fmt_time_left(lot.ends_at) if lot.status == "active" else "ожидает"
        lines.append(
            f"{status} {lot.emoji} <b>{lot.title}</b>\n"
            f"   <code>{lot.lot_code}</code>  ·  {fmt_price(lot.current_price)}  ·  ⏱ {time_line}"
        )
    return "🏷 <b>Активные аукционы</b>\n\n" + "\n\n".join(lines)


def lot_detail_text(lot, bid_count: int, user_count: int) -> str:
    blitz_line = f"\n🔥 Блиц-цена: {fmt_price(lot.blitz_price)}" if lot.blitz_price else ""
    return (
        f"📋 <b>Детали лота {lot.lot_code}</b>\n\n"
        f"{lot.emoji} {lot.title}\n\n"
        f"Описание:\n{lot.description or '—'}\n\n"
        f"• Стартовая цена: {fmt_price(lot.start_price)}\n"
        f"• Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"• Шаг ставки: {fmt_price(lot.bid_step)}\n"
        f"• Ставок: {bid_count}\n"
        f"• Участников: {user_count}"
        f"{blitz_line}"
    )


def bid_accepted_text(lot, amount: int, is_blitz: bool = False) -> str:
    if is_blitz:
        return (
            f"⚡ <b>БЛИЦ! Вы победили мгновенно!</b>\n\n"
            f"{lot.emoji} {lot.title}\n"
            f"Финальная цена: <b>{fmt_price(amount)}</b>\n\n"
            f"📦 Менеджер свяжется в течение 1 часа."
        )
    return (
        f"✅ <b>Ставка принята!</b>\n\n"
        f"<code>{lot.lot_code}</code> · {lot.emoji} {lot.title}\n"
        f"Ваша ставка: <b>{fmt_price(amount)}</b>\n"
        f"Вы сейчас <b>лидируете</b> 🏆\n\n"
        f"<i>Если вас перебьют — сразу уведомим в личку</i>"
    )


def overbid_notify_text(lot, new_price: int) -> str:
    return (
        f"⚠️ <b>Вашу ставку перебили!</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"Новая цена: <b>{fmt_price(new_price)}</b>\n\n"
        f"Хотите ответить?"
    )

```


## File: auction_admin_bot\utils\guards.py
```python
from functools import wraps
from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def admin_only_message(message: Message) -> bool:
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return False
    return True


async def admin_only_callback(callback: CallbackQuery) -> bool:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён.", show_alert=True)
        return False
    return True


```


## File: auction_admin_bot\utils\scheduler.py
```python
"""
auction_admin_bot/utils/scheduler.py
─────────────────────────────────────
Изменения по сравнению с оригиналом:
  1. Добавлен глобальный кеш _price_cache для отслеживания изменений цены.
  2. Добавлена корутина sync_overbid_notifications() — фоновый polling,
     который каждые 5 секунд проверяет текущую цену активных лотов.
     При обнаружении изменения (ставка из Mini App):
       – обновляет карточку лота в топике группы;
       – отправляет уведомление вытесненному лидеру.
  3. Функция restore_scheduled_jobs обновлена: принимает winner_bot.
  Всё остальное — без изменений.
"""
import asyncio
import texts as T
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

logger = logging.getLogger(__name__)

_scheduler: AsyncIOScheduler = None

# ── Кеш: lot_id → (last_price, last_leader_id) ───────────────────────────────
# Заполняется при старте и обновляется в sync_overbid_notifications.
_price_cache: dict[int, tuple[int, Optional[int]]] = {}


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    global _scheduler
    _scheduler = AsyncIOScheduler(timezone="UTC")
    return _scheduler


def get_scheduler() -> AsyncIOScheduler:
    return _scheduler


# ══════════════════════════════════════════════════════════════════════════════
#  Auction finish job
# ══════════════════════════════════════════════════════════════════════════════

async def _finish_auction_job(
    lot_id: int,
    bot: Bot,
    winner_bot: Bot = None,
    force: bool = False,
):
    """
    Вызывается планировщиком по истечении таймера, либо напрямую при
    досрочном завершении (force=True).

    bot        — для обновления карточки и уведомления топика/админов
    winner_bot — для уведомлений победителю/проигравшим (клиентский бот);
                 если не передан, используется bot
    """
    from db.queries import (
        get_lot, finish_lot, get_top_bid,
        get_bid_count, get_unique_bidder_count, get_bidders_for_lot,
    )
    from db.database import LotStatus
    from utils.formatting import winner_text, fmt_price, auction_finished_text
    from keyboards.inline import kb_winner
    from config import GROUP_ID

    _winner_bot = winner_bot or bot

    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        return

    # Проверяем, не сдвинул ли антиснайпинг ends_at пока job ждал.
    # При force=True (досрочное завершение) — пропускаем.
    if not force:
        now = datetime.now(timezone.utc)
        if lot.ends_at:
            actual_ends = (
                lot.ends_at if lot.ends_at.tzinfo
                else lot.ends_at.replace(tzinfo=timezone.utc)
            )
            if actual_ends > now + timedelta(seconds=2):
                logger.info(
                    f"_finish_auction_job: lot {lot_id} ends_at moved to "
                    f"{actual_ends}, rescheduling"
                )
                schedule_auction_finish(lot_id, actual_ends, bot, winner_bot)
                return

    top_bid = await get_top_bid(lot_id)
    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    # Убираем лот из кеша — он больше не активен
    _price_cache.pop(lot_id, None)

    if top_bid:
        await finish_lot(lot_id, top_bid.user_id, top_bid.username or "", top_bid.amount)
        lot = await get_lot(lot_id)

        # Удалить старую карточку из топика (её заменит объявление)
        _client_bot = winner_bot or bot
        if lot.topic_id and GROUP_ID and lot.card_message_id:
            try:
                await _client_bot.delete_message(
                    chat_id=GROUP_ID,
                    message_id=lot.card_message_id,
                )
                logger.info(f"Card deleted for lot {lot_id}")
            except Exception as e:
                logger.warning(f"Card delete failed: {e}")

        # Объявление победителя в топике
        if lot.topic_id and GROUP_ID:
            try:
                finished_text = auction_finished_text(lot, top_bid.amount)
                if lot.client_photo_file_id:
                    await _client_bot.send_photo(
                        chat_id=GROUP_ID,
                        message_thread_id=lot.topic_id,
                        photo=lot.client_photo_file_id,
                        caption=finished_text,
                        parse_mode="HTML",
                    )
                else:
                    await _client_bot.send_message(
                        chat_id=GROUP_ID,
                        message_thread_id=lot.topic_id,
                        text=finished_text,
                        parse_mode="HTML",
                    )
            except Exception as e:
                logger.warning(f"Failed to post winner in topic: {e}")

        # Уведомление победителю в ЛС
        winner_text_str = (
            f"🏆 <b>ВЫ ПОБЕДИЛИ!</b>\n\n"
            f"{lot.emoji} <b>{lot.title}</b>\n"
            f"<code>{lot.lot_code}</code>\n\n"
            f"📋 {lot.description or '—'}\n\n"
            f"💰 Финальная цена: <b>{fmt_price(top_bid.amount)}</b>\n\n"
            f"📦 Менеджер свяжется с вами в ближайшее время."
        )
        try:
            if lot.client_photo_file_id:
                await _winner_bot.send_photo(
                    chat_id=top_bid.user_id,
                    photo=lot.client_photo_file_id,
                    caption=winner_text_str,
                    parse_mode="HTML",
                )
            else:
                await _winner_bot.send_message(
                    chat_id=top_bid.user_id,
                    text=winner_text_str,
                    parse_mode="HTML",
                )
        except Exception as e:
            logger.warning(f"Failed to notify winner {top_bid.user_id}: {e}")

        # Уведомление проигравшим
        bidders = await get_bidders_for_lot(lot_id)
        for bidder in bidders:
            if bidder["user_id"] == top_bid.user_id:
                continue
            try:
                await _winner_bot.send_message(
                    chat_id=bidder["user_id"],
                    text=(
                        f"🏁 <b>Аукцион завершён</b>\n\n"
                        f"{lot.emoji} {lot.title}\n"
                        f"<code>{lot.lot_code}</code>\n\n"
                        f"К сожалению, вы не победили.\n"
                        f"Финальная цена: <b>{fmt_price(top_bid.amount)}</b>\n\n"
                        f"<i>Следите за новыми лотами в группе!</i>"
                    ),
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.debug(f"Loser notify failed for {bidder['user_id']}: {e}")

        # Уведомление всех администраторов
        from config import ADMIN_IDS
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=winner_text(lot, bid_count, user_count),
                    parse_mode="HTML",
                    reply_markup=kb_winner(lot_id),
                )
            except Exception as e:
                logger.warning(f"Failed to notify admin {admin_id}: {e}")
    else:
        from db.queries import cancel_lot
        await cancel_lot(lot_id)
        from config import ADMIN_IDS
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    chat_id=admin_id,
                    text=(
                        f"📭 Аукцион <code>{lot.lot_code}</code> "
                        f"завершился без ставок.\n{lot.emoji} {lot.title}"
                    ),
                    parse_mode="HTML",
                )
            except Exception:
                pass


# ══════════════════════════════════════════════════════════════════════════════
#  Lot start job (для SCHEDULED → ACTIVE)
# ══════════════════════════════════════════════════════════════════════════════

async def _start_auction_job(lot_id: int, bot: Bot, winner_bot: Bot = None):
    """Активирует запланированный лот — меняет статус на ACTIVE и запускает таймер финиша."""
    from datetime import timedelta
    from db.queries import get_lot, activate_scheduled_lot
    from db.database import LotStatus

    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.SCHEDULED:
        return

    ends_at = datetime.now(timezone.utc) + timedelta(hours=lot.duration_hours)
    await activate_scheduled_lot(lot_id, ends_at)
    lot = await get_lot(lot_id)

    schedule_auction_finish(lot_id, ends_at, bot, winner_bot)
    logger.info(f"Lot {lot_id} activated by scheduler, ends at {ends_at}")

    # Немедленно обновить карточку в топике
    _client_bot = winner_bot or bot
    from config import GROUP_ID
    from db.queries import get_bid_count, get_top_bid
    from utils.formatting import lot_card_text
    from keyboards.inline import kb_lot_card
    if GROUP_ID and lot.topic_id and lot.card_message_id:
        try:
            bid_count = await get_bid_count(lot_id)
            top_bid   = await get_top_bid(lot_id)
            text = lot_card_text(lot, bid_count, top_bid)
            kb   = kb_lot_card(lot)
            if lot.client_photo_file_id:
                await _client_bot.edit_message_caption(
                    chat_id=GROUP_ID, message_id=lot.card_message_id,
                    caption=text, reply_markup=kb, parse_mode="HTML",
                )
            else:
                await _client_bot.edit_message_text(
                    chat_id=GROUP_ID, message_id=lot.card_message_id,
                    text=text, reply_markup=kb, parse_mode="HTML",
                )
            logger.info(f"Card updated on lot {lot_id} start")
        except Exception as e:
            logger.warning(f"Card update failed for lot {lot_id}: {e}")

    if GROUP_ID and lot.topic_id:
        try:
            await _client_bot.send_message(
                chat_id=GROUP_ID,
                message_thread_id=lot.topic_id,
                text=f"🔔 <b>Аукцион начался!</b>\n{lot.emoji} {lot.title}",
                parse_mode="HTML",
            )
        except Exception as e:
            logger.warning(f"Start notify failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  Public scheduling helpers
# ══════════════════════════════════════════════════════════════════════════════

def schedule_auction_finish(
    lot_id: int,
    ends_at: datetime,
    bot: Bot,
    winner_bot: Bot = None,
):
    if _scheduler is None:
        return
    job_id = f"finish_lot_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)
    _scheduler.add_job(
        _finish_auction_job,
        trigger="date",
        run_date=ends_at,
        args=[lot_id, bot, winner_bot],
        id=job_id,
        replace_existing=True,
    )
    logger.info(f"Scheduled finish for lot {lot_id} at {ends_at}")


def schedule_lot_start(
    lot_id: int,
    starts_at: datetime,
    bot: Bot,
    winner_bot: Bot = None,
):
    if _scheduler is None:
        return
    now = datetime.now(timezone.utc)
    starts = starts_at if starts_at.tzinfo else starts_at.replace(tzinfo=timezone.utc)
    if starts <= now:
        logger.warning(
            f"schedule_lot_start: starts_at {starts} is in the past, skipping"
        )
        return
    job_id = f"start_lot_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)
    _scheduler.add_job(
        _start_auction_job,
        trigger="date",
        run_date=starts_at,
        args=[lot_id, bot, winner_bot],
        id=job_id,
        replace_existing=True,
    )
    logger.info(f"Scheduled start for lot {lot_id} at {starts_at}")


def cancel_auction_job(lot_id: int):
    if _scheduler is None:
        return
    for prefix in ("finish_lot_", "start_lot_"):
        job_id = f"{prefix}{lot_id}"
        if _scheduler.get_job(job_id):
            _scheduler.remove_job(job_id)


# ══════════════════════════════════════════════════════════════════════════════
#  Restore on restart
# ══════════════════════════════════════════════════════════════════════════════

async def restore_scheduled_jobs(bot: Bot, winner_bot: Bot = None):
    """
    При рестарте бота восстанавливает таймеры из БД.
    Также инициализирует _price_cache для sync_overbid_notifications.
    """
    from db.queries import get_active_lots, get_top_bid
    from db.database import LotStatus

    now  = datetime.now(timezone.utc)
    lots = await get_active_lots()

    for lot in lots:
        if lot.status == LotStatus.SCHEDULED and lot.starts_at:
            starts = (
                lot.starts_at if lot.starts_at.tzinfo
                else lot.starts_at.replace(tzinfo=timezone.utc)
            )
            if starts > now:
                schedule_lot_start(lot.id, starts, bot, winner_bot)
            else:
                await _start_auction_job(lot.id, bot, winner_bot)

        elif lot.status == LotStatus.ACTIVE and lot.ends_at:
            ends = (
                lot.ends_at if lot.ends_at.tzinfo
                else lot.ends_at.replace(tzinfo=timezone.utc)
            )
            if ends > now:
                schedule_auction_finish(lot.id, ends, bot, winner_bot)
                logger.info(f"Restored timer for lot {lot.id} ({lot.lot_code})")
            else:
                await _finish_auction_job(lot.id, bot, winner_bot)

        # Инициализация кеша для обнаружения ставок из Mini App
        try:
            top = await get_top_bid(lot.id)
            _price_cache[lot.id] = (
                lot.current_price,
                top.user_id if top else None,
            )
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════════════
#  NEW: sync_finish_jobs — перепланирование при изменении ends_at
# ══════════════════════════════════════════════════════════════════════════════

async def sync_finish_jobs(bot: Bot, winner_bot: Bot = None):
    """
    Каждые 15 сек сверяет ends_at активных лотов с запланированными job-ами.
    Нужно для корректного перепланирования после антиснайпинга.
    """
    from db.queries import get_active_lots
    from db.database import LotStatus

    while True:
        await asyncio.sleep(15)
        try:
            lots = await get_active_lots()
            for lot in lots:
                if lot.status != LotStatus.ACTIVE or not lot.ends_at:
                    continue
                ends = (
                    lot.ends_at if lot.ends_at.tzinfo
                    else lot.ends_at.replace(tzinfo=timezone.utc)
                )
                job_id = f"finish_lot_{lot.id}"
                job = _scheduler.get_job(job_id) if _scheduler else None
                if job is None:
                    schedule_auction_finish(lot.id, ends, bot, winner_bot)
                    logger.info(f"sync_finish_jobs: restored missing job for lot {lot.id}")
                elif abs((job.next_run_time - ends).total_seconds()) > 5:
                    schedule_auction_finish(lot.id, ends, bot, winner_bot)
                    logger.info(
                        f"sync_finish_jobs: rescheduled lot {lot.id} "
                        f"from {job.next_run_time} to {ends}"
                    )
        except Exception as e:
            logger.warning(f"sync_finish_jobs error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  NEW: sync_overbid_notifications — ключевое изменение для Mini App
# ══════════════════════════════════════════════════════════════════════════════

async def sync_overbid_notifications(bot: Bot, winner_bot: Bot = None):
    """
    Фоновый polling для обработки ставок, сделанных через Mini App.

    Каждые 5 секунд:
      1. Читает current_price и top bid всех активных лотов из БД.
      2. Сравнивает с кешем _price_cache.
      3. Если цена выросла — это ставка из Mini App (иначе бот обработал бы её сам):
         a) Обновляет карточку лота в топике группы (цена, количество ставок).
         b) Отправляет уведомление вытесненному лидеру.
         c) Обновляет кеш.
      4. Если лот исчез из активных — удаляет из кеша.

    Уведомления используют тот же формат, что и бот при обычных ставках,
    поэтому пользователи не увидят разницы в источнике ставки.
    """
    from db.queries import get_active_lots, get_top_bid, get_bid_count
    from db.database import LotStatus
    from utils.formatting import fmt_price, lot_card_text
    from keyboards.inline import kb_lot_card
    from config import GROUP_ID

    notify_bot = winner_bot or bot

    logger.info("sync_overbid_notifications started")

    while True:
        await asyncio.sleep(5)
        try:
            lots = await get_active_lots()
            active_ids = {lot.id for lot in lots}

            # Убрать завершённые/отменённые лоты из кеша
            for stale_id in list(_price_cache.keys()):
                if stale_id not in active_ids:
                    _price_cache.pop(stale_id, None)

            for lot in lots:
                if lot.status != LotStatus.ACTIVE:
                    continue

                top_bid   = await get_top_bid(lot.id)
                bid_count = await get_bid_count(lot.id)

                new_price     = lot.current_price
                new_leader_id = top_bid.user_id if top_bid else None

                cached = _price_cache.get(lot.id)

                if cached is None:
                    # Первый раз видим лот — просто сохранить
                    _price_cache[lot.id] = (new_price, new_leader_id)
                    continue

                prev_price, prev_leader_id = cached

                if new_price <= prev_price:
                    # Цена не изменилась — ничего делать не нужно
                    continue

                # ── Цена выросла: ставка из Mini App ──────────────────────
                logger.info(
                    f"Mini App bid detected: lot {lot.lot_code} "
                    f"{prev_price} → {new_price} "
                    f"(leader: {prev_leader_id} → {new_leader_id})"
                )

                # 1. Обновить карточку лота в топике группы
                if GROUP_ID and lot.topic_id and lot.card_message_id:
                    try:
                        text = lot_card_text(lot, bid_count, top_bid)
                        kb   = kb_lot_card(lot)
                        if lot.client_photo_file_id:
                            await notify_bot.edit_message_caption(
                                chat_id=GROUP_ID,
                                message_id=lot.card_message_id,
                                caption=text,
                                reply_markup=kb,
                                parse_mode="HTML",
                            )
                        else:
                            await notify_bot.edit_message_text(
                                chat_id=GROUP_ID,
                                message_id=lot.card_message_id,
                                text=text,
                                reply_markup=kb,
                                parse_mode="HTML",
                            )
                        logger.debug(f"Card updated for lot {lot.id} after Mini App bid")
                    except Exception as e:
                        logger.debug(f"Card update failed for lot {lot.id}: {e}")

                # 2. Уведомить вытесненного лидера
                if prev_leader_id and prev_leader_id != new_leader_id:
                    try:
                        from keyboards.inline import kb_overbid
                        await notify_bot.send_message(
                            chat_id=prev_leader_id,
                            text=(
                                f"⚡ <b>Вас перебили!</b>\n\n"
                                f"{lot.emoji} {lot.title}\n"
                                f"<code>{lot.lot_code}</code>\n\n"
                                f"Новая цена: <b>{fmt_price(new_price)}</b>\n\n"
                                f"<i>Откройте мини-апп или вернитесь в топик чтобы сделать ставку.</i>"
                            ),
                            reply_markup=kb_overbid(lot.id, new_price, lot.bid_step),
                            parse_mode="HTML",
                        )
                        logger.debug(
                            f"Overbid notify sent to user {prev_leader_id} "
                            f"for lot {lot.id}"
                        )
                    except Exception as e:
                        logger.debug(
                            f"Overbid notify failed for user {prev_leader_id}: {e}"
                        )

                # 3. Обновить кеш
                _price_cache[lot.id] = (new_price, new_leader_id)

        except Exception as e:
            logger.warning(f"sync_overbid_notifications error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  Antisnipe (используется group bot)
# ══════════════════════════════════════════════════════════════════════════════

async def apply_antisnipe(lot_id: int, ends_at: datetime, bot: Bot) -> datetime:
    """Если ставка сделана менее чем за ANTISNIPE_SECONDS до конца — продлить."""
    from config import ANTISNIPE_MINUTES
    from db.queries import extend_lot

    antisnipe_seconds = ANTISNIPE_MINUTES * 60
    now = datetime.now(timezone.utc)
    if ends_at.tzinfo is None:
        ends_at = ends_at.replace(tzinfo=timezone.utc)

    time_left = (ends_at - now).total_seconds()
    if time_left < antisnipe_seconds:
        new_ends_at = now + timedelta(seconds=antisnipe_seconds)
        await extend_lot(lot_id, new_ends_at)
        logger.info(
            f"Antisnipe triggered for lot {lot_id}, extended to {new_ends_at}"
        )
        return new_ends_at
    return ends_at

```


## File: auction_admin_bot\utils\states.py
```python
from aiogram.fsm.state import State, StatesGroup


class CreateLotFSM(StatesGroup):
    entering_title      = State()
    entering_price      = State()
    choosing_step       = State()
    entering_step       = State()
    choosing_duration   = State()
    entering_duration   = State()
    entering_desc       = State()
    uploading_photo     = State()
    choosing_start_time = State()
    entering_start_time = State()
    confirming          = State()
    # entering_topic_id удалён — лоты запускаются в Мини Апп без топика


class BanFSM(StatesGroup):
    choosing_user = State()
    confirming    = State()


class ExtendFSM(StatesGroup):
    choosing_hours = State()


class CustomBidFSM(StatesGroup):
    waiting_for_amount = State()

```


## File: auction_group_bot\README.md
```markdown
# Auction Group Bot — клиентский бот

Telegram-бот для участников закрытого аукциона. Работает в паре с `auction_admin_bot` через общую БД.

## Структура


```


## File: auction_group_bot\bot.py
```python
import asyncio
import logging
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from typing import Any, Dict, Optional

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import StorageKey, StateType

from config import GROUP_BOT_TOKEN
from db.database import init_db
from handlers import welcome, bidding, notifications
from utils.scheduler import setup_scheduler, restore_scheduled_jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
)

class UserStorage(MemoryStorage):
    """
    FSM-хранилище только по user_id, без привязки к chat_id.
    Нужно чтобы состояние установленное при нажатии кнопки в топике группы
    было доступно когда пользователь пишет боту в личку.
    """

    def _user_key(self, key: StorageKey) -> StorageKey:
        """Заменяет chat_id на user_id во всех операциях."""
        return StorageKey(
            bot_id=key.bot_id,
            chat_id=key.user_id,
            user_id=key.user_id,
        )

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        await super().set_state(self._user_key(key), state)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        return await super().get_state(self._user_key(key))

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        await super().set_data(self._user_key(key), data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        return await super().get_data(self._user_key(key))

    async def update_data(self, key: StorageKey, data: Dict[str, Any]) -> Dict[str, Any]:
        return await super().update_data(self._user_key(key), data)

    async def close(self) -> None:
        await super().close()


async def publish_pending_cards(bot: Bot):
    """
    Публикует карточки активных лотов у которых ещё нет card_message_id.
    Запускается при старте и каждые 10 секунд — чтобы подхватывать
    лоты запущенные админ-ботом.
    """
    from db.database import LotStatus
    from db.queries import get_active_lots, get_bid_count, get_top_bid, update_card_message_id
    from utils.formatting import lot_card_text
    from keyboards.inline import kb_lot_card
    from config import GROUP_ID

    if not GROUP_ID:
        return

    lots_list = await get_active_lots()
    for lot in lots_list:
        if lot.status not in (LotStatus.ACTIVE, LotStatus.SCHEDULED):
            continue
        if lot.card_message_id:
            continue  # карточка уже есть
        if not lot.topic_id:
            continue  # топик не задан

        try:
            bid_count = await get_bid_count(lot.id)
            top_bid = await get_top_bid(lot.id)
            is_caption = bool(lot.photo_file_id)
            text = lot_card_text(lot, bid_count, top_bid, is_caption=is_caption)
            kb = kb_lot_card(lot)

            if lot.photo_file_id:
                # file_id привязан к боту который его получил (админскому).
                # Скачиваем файл через админский бот и шлём байтами через клиентский.
                from config import ADMIN_BOT_TOKEN
                from aiogram import Bot as AiogramBot
                import io
                photo = None
                try:
                    admin_bot = AiogramBot(token=ADMIN_BOT_TOKEN)
                    file = await admin_bot.get_file(lot.photo_file_id)
                    buf = io.BytesIO()
                    await admin_bot.download_file(file.file_path, buf)
                    buf.seek(0)
                    await admin_bot.session.close()
                    from aiogram.types import BufferedInputFile
                    photo = BufferedInputFile(buf.read(), filename="photo.jpg")
                    logger.info(f"Photo downloaded for lot {lot.id}, size={buf.getbuffer().nbytes if hasattr(buf, 'getbuffer') else '?'}")
                except Exception as e:
                    logger.warning(f"Photo download failed for lot {lot.id}: {e}")

                if photo:
                    msg = await bot.send_photo(
                        chat_id=GROUP_ID,
                        message_thread_id=lot.topic_id,
                        photo=photo,
                        caption=text,
                        reply_markup=kb,
                        parse_mode="HTML",
                    )
                    # Сохраняем file_id от клиентского бота для последующих edit_message_caption
                    if msg.photo:
                        from db.queries import save_client_photo_file_id
                        await save_client_photo_file_id(lot.id, msg.photo[-1].file_id)
                else:
                    msg = await bot.send_message(
                        chat_id=GROUP_ID,
                        message_thread_id=lot.topic_id,
                        text=text,
                        reply_markup=kb,
                        parse_mode="HTML",
                    )
            else:
                msg = await bot.send_message(
                    chat_id=GROUP_ID,
                    message_thread_id=lot.topic_id,
                    text=text,
                    reply_markup=kb,
                    parse_mode="HTML",
                )
            await update_card_message_id(lot.id, msg.message_id)
            logger.info(f"Published card for lot {lot.id} in topic {lot.topic_id}")
        except Exception as e:
            logger.warning(f"Failed to publish card for lot {lot.id}: {e}")


async def card_publisher_loop(bot: Bot):
    """Каждые 10 секунд проверяет появились ли новые лоты без карточки."""
    while True:
        await asyncio.sleep(10)
        try:
            await publish_pending_cards(bot)
        except Exception as e:
            logger.warning(f"Card publisher error: {e}")


async def card_updater_loop(bot: Bot):
    """Каждые 60 секунд обновляет карточки активных лотов — для обратного отсчёта."""
    from db.database import LotStatus
    from db.queries import get_active_lots, get_bid_count, get_top_bid
    from utils.formatting import lot_card_text
    from keyboards.inline import kb_lot_card
    from config import GROUP_ID

    while True:
        await asyncio.sleep(60)
        if not GROUP_ID:
            continue
        try:
            lots_list = await get_active_lots()
            for lot in lots_list:
                if lot.status not in (LotStatus.ACTIVE, LotStatus.SCHEDULED):
                    continue
                if not lot.card_message_id or not lot.topic_id:
                    continue
                try:
                    bid_count = await get_bid_count(lot.id)
                    top_bid = await get_top_bid(lot.id)
                    text = lot_card_text(lot, bid_count, top_bid)
                    kb = kb_lot_card(lot)
                    if lot.client_photo_file_id:
                        await bot.edit_message_caption(
                            chat_id=GROUP_ID,
                            message_id=lot.card_message_id,
                            caption=text,
                            reply_markup=kb,
                            parse_mode="HTML",
                        )
                    else:
                        await bot.edit_message_text(
                            chat_id=GROUP_ID,
                            message_id=lot.card_message_id,
                            text=text,
                            reply_markup=kb,
                            parse_mode="HTML",
                        )
                except Exception as e:
                    # MessageNotModified — текст не изменился, это норма
                    if "message is not modified" not in str(e).lower():
                        logger.debug(f"Card timer update failed for lot {lot.id}: {e}")
        except Exception as e:
            logger.warning(f"Card updater error: {e}")


async def main():
    bot = Bot(token=GROUP_BOT_TOKEN)
    storage = UserStorage()
    dp = Dispatcher(storage=storage)

    await init_db()

    scheduler = setup_scheduler(bot)
    scheduler.start()
    await restore_scheduled_jobs(bot)

    dp.include_router(welcome.router)
    dp.include_router(bidding.router)
    dp.include_router(notifications.router)

    # Опубликовать карточки для уже активных лотов без карточки
    await publish_pending_cards(bot)

    # Запустить фоновый цикл публикации
    asyncio.create_task(card_publisher_loop(bot))
    # Запустить фоновый цикл обновления таймера
    asyncio.create_task(card_updater_loop(bot))

    logger.info("Group bot starting...")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=["message", "callback_query", "chat_member"],
        )
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())


```


## File: auction_group_bot\config.py
```python
"""
auction_group_bot/config.py
────────────────────────────
Изменения:
  1. Добавлена переменная MINIAPP_URL — URL задеплоенного Mini App.
     Используется в handlers/welcome.py для кнопки WebApp.
     Если переменная не задана, кнопка не отображается (graceful degradation).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Telegram ──────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("GROUP_BOT_TOKEN", "")
GROUP_BOT_TOKEN: str = BOT_TOKEN  # alias — используется в bot.py и handlers
ADMIN_BOT_TOKEN: str = os.getenv("ADMIN_BOT_TOKEN", "")  # для скачивания фото
HELP_URL: str = os.getenv("HELP_URL", "https://t.me/")

# Admin Telegram user IDs (comma-separated in .env)
_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: list[int] = [int(x.strip()) for x in _raw.split(",") if x.strip()]

# The closed group where auctions happen
GROUP_ID: int = int(os.getenv("GROUP_ID", "0"))

# ── Mini App ──────────────────────────────────────────────────
# URL задеплоенного Mini App — например https://auction.example.com
# Если не задан — кнопка в /start не показывается.
MINIAPP_URL: str = os.getenv("MINIAPP_URL", "")

# ── Database ──────────────────────────────────────────────────
DATABASE_URL: str = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/auction"
)

# ── Redis ─────────────────────────────────────────────────────
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# ── Auction defaults ─────────────────────────────────────────
ANTISNIPE_MINUTES: int = int(os.getenv("ANTISNIPE_MINUTES", "2"))
ANTISNIPE_SECONDS: int = ANTISNIPE_MINUTES * 60
MIN_BID_STEP: int = int(os.getenv("MIN_BID_STEP", "500"))

# ── Help text (shown on "help:" button) ──────────────────────
HELP_TEXT: str = os.getenv(
    "HELP_TEXT",
    (
        "📖 <b>Как участвовать в аукционе</b>\n\n"
        "1. Нажмите кнопку «Открыть аукционы» в боте\n"
        "2. Выберите интересующий лот\n"
        "3. Нажмите «Сделать ставку» и подтвердите сумму\n\n"
        "• Ставка не ниже текущей цены + шаг\n"
        "• При перебитии ставки вы получите уведомление сюда\n"
        "• Победитель объявляется по истечении таймера\n\n"
        "<i>Удачи на торгах!</i>"
    ),
)

```


## File: auction_group_bot\requirements.txt
```
aiogram==3.13.1
sqlalchemy==2.0.36
aiosqlite==0.20.0
apscheduler==3.10.4
python-dotenv==1.0.1


```


## File: auction_group_bot\db\__init__.py
```python


```


## File: auction_group_bot\db\database.py
```python
"""
Общая БД с админ-ботом.
Модели идентичны auction_admin_bot/db/database.py.
При деплое оба бота используют один DATABASE_URL.
"""
from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum, ForeignKey,
    Float, Integer, String, Text, func,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class LotStatus(str, enum.Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_code: Mapped[str] = mapped_column(String(20), unique=True)

    category: Mapped[str] = mapped_column(String(64))
    emoji: Mapped[str] = mapped_column(String(8))
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo_file_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    client_photo_file_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    start_price: Mapped[int] = mapped_column(Integer)
    bid_step: Mapped[int] = mapped_column(Integer)
    blitz_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    current_price: Mapped[int] = mapped_column(Integer)

    duration_hours: Mapped[float] = mapped_column(Float)
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    seconds_left: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    topic_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    card_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    status: Mapped[LotStatus] = mapped_column(Enum(LotStatus), default=LotStatus.PENDING)
    created_by: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    winner_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    winner_username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    final_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    bids: Mapped[list[Bid]] = relationship("Bid", back_populates="lot", order_by="Bid.id.desc()")


class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"))
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    amount: Mapped[int] = mapped_column(Integer)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    lot: Mapped[Lot] = relationship("Lot", back_populates="bids")


class BannedUser(Base):
    __tablename__ = "banned_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    banned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    banned_by: Mapped[int] = mapped_column(BigInteger)


class WatchList(Base):
    """Участники, подписанные на уведомления по лоту."""
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"))
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)


# Alias for compatibility
Watchlist = WatchList


class Rating(Base):
    """Оценки аукционов от участников."""
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"))
    user_id: Mapped[int] = mapped_column(BigInteger)
    stars: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _migrate(conn)


async def _migrate(conn):
    """Добавляет новые колонки если их нет (safe ALTER TABLE ADD COLUMN)."""
    import sqlalchemy as sa
    migrations = [
        ("lots", "seconds_left",         "INTEGER"),
        ("lots", "starts_at",            "DATETIME"),
        ("lots", "client_photo_file_id", "VARCHAR(256)"),
        ("lots", "photo_file_id",        "VARCHAR(256)"),
        ("lots", "card_message_id",      "BIGINT"),
    ]
    for table, column, col_def in migrations:
        try:
            await conn.execute(sa.text(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}"))
        except Exception:
            pass  # already exists


```


## File: auction_group_bot\db\queries.py
```python
"""
auction_group_bot/db/queries.py
────────────────────────────────
Изменения:
  1. place_bid — добавлен SELECT ... FOR UPDATE внутри begin()-транзакции.
     Это предотвращает race condition при одновременных ставках из бота
     и мини-аппа, которые оба пишут в одну таблицу.
  Всё остальное без изменений.
"""
from __future__ import annotations

import random
import string
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.database import AsyncSessionLocal, Bid, BannedUser, Lot, LotStatus, Watchlist


# ── Helpers ───────────────────────────────────────────────────

def _gen_code() -> str:
    digits = "".join(random.choices(string.digits, k=3))
    return f"LOT-{digits}"


# ── Lot ───────────────────────────────────────────────────────

async def get_lot(lot_id: int) -> Optional[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot).options(selectinload(Lot.bids)).where(Lot.id == lot_id)
        )
        return result.scalar_one_or_none()


async def get_active_lots() -> list[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot)
            .where(Lot.status.in_([LotStatus.ACTIVE, LotStatus.SCHEDULED]))
            .order_by(Lot.ends_at.nullslast())
        )
        return list(result.scalars().all())


async def create_lot(
    *,
    created_by: int,
    category: str,
    emoji: str,
    title: str,
    description: str,
    start_price: int,
    bid_step: int,
    duration_hours: int,
    blitz_price: Optional[int] = None,
    photo_file_id: Optional[str] = None,
) -> Lot:
    async with AsyncSessionLocal() as s:
        lot = Lot(
            lot_code=_gen_code(),
            created_by=created_by,
            category=category,
            emoji=emoji,
            title=title,
            description=description,
            start_price=start_price,
            bid_step=bid_step,
            duration_hours=duration_hours,
            blitz_price=blitz_price,
            current_price=start_price,
            status=LotStatus.PENDING,
            photo_file_id=photo_file_id,
        )
        s.add(lot)
        await s.commit()
        await s.refresh(lot)
        return lot


async def launch_lot(lot_id: int, topic_id: int, ends_at: datetime) -> Lot:
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.ACTIVE,
                topic_id=topic_id,
                starts_at=None,
                ends_at=ends_at,
                card_message_id=None,
            )
        )
        await s.commit()
    return await get_lot(lot_id)


async def schedule_lot(lot_id: int, topic_id: int, starts_at: datetime) -> Lot:
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.SCHEDULED,
                topic_id=topic_id,
                starts_at=starts_at,
                card_message_id=None,
            )
        )
        await s.commit()
    return await get_lot(lot_id)


async def activate_scheduled_lot(lot_id: int, ends_at: datetime) -> Lot:
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(status=LotStatus.ACTIVE, ends_at=ends_at, starts_at=None)
        )
        await s.commit()
    return await get_lot(lot_id)


async def set_card_message_id(lot_id: int, message_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(card_message_id=message_id)
        )
        await s.commit()


async def finish_lot(lot_id: int, winner_user_id: int, winner_username: str, final_price: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot)
            .where(Lot.id == lot_id)
            .values(
                status=LotStatus.FINISHED,
                winner_user_id=winner_user_id,
                winner_username=winner_username,
                final_price=final_price,
            )
        )
        await s.commit()


async def cancel_lot(lot_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(status=LotStatus.CANCELLED)
        )
        await s.commit()


async def cancel_lot_no_bids(lot_id: int):
    await cancel_lot(lot_id)


async def extend_lot(lot_id: int, new_ends_at: datetime):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Lot).where(Lot.id == lot_id).values(ends_at=new_ends_at)
        )
        await s.commit()


# Alias used by antisnipe
extend_lot_timer = extend_lot


async def get_pending_lot_by_admin(admin_id: int) -> Optional[Lot]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot)
            .where(
                Lot.created_by == admin_id,
                Lot.status == LotStatus.PENDING,
                Lot.topic_id == None,
            )
            .order_by(Lot.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


# ── Bids ──────────────────────────────────────────────────────

async def get_top_bid(lot_id: int) -> Optional[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.amount.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


async def get_bid_count(lot_id: int) -> int:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(func.count()).where(
                Bid.lot_id == lot_id, Bid.is_cancelled == False
            )
        )
        return result.scalar_one()


async def get_unique_bidder_count(lot_id: int) -> int:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(func.count(Bid.user_id.distinct()))
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
        )
        return result.scalar_one()


async def get_recent_bids(lot_id: int, limit: int = 5) -> list[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.id.desc())
            .limit(limit)
        )
        return list(result.scalars().all())


async def get_lot_bids(lot_id: int) -> list[Bid]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.amount.desc())
        )
        return list(result.scalars().all())


async def cancel_user_bids(lot_id: int, user_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            update(Bid)
            .where(Bid.lot_id == lot_id, Bid.user_id == user_id)
            .values(is_cancelled=True)
        )
        await s.commit()


async def get_bidders_for_lot(lot_id: int) -> list[dict]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(
                Bid.user_id,
                Bid.username,
                func.max(Bid.amount).label("max_amount"),
            )
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .group_by(Bid.user_id, Bid.username)
            .order_by(func.max(Bid.amount).desc())
        )
        return [
            {"user_id": r.user_id, "username": r.username, "amount": r.max_amount}
            for r in result.all()
        ]


async def place_bid(
    lot_id: int,
    user_id: int,
    username: Optional[str],
    amount: int,
) -> tuple[bool, Optional[str], Optional[Bid]]:
    """
    Разместить ставку.

    ИЗМЕНЕНИЕ: теперь использует SELECT ... FOR UPDATE в рамках одной
    транзакции — это полностью исключает race condition при ставках
    из мини-аппа и бота одновременно.

    Возвращает (success, error_message, bid).
    """
    async with AsyncSessionLocal() as s:
        async with s.begin():
            # Проверка бана
            banned = await s.get(BannedUser, user_id)
            if banned:
                return False, "Вы заблокированы", None

            # Блокировка строки лота — никакая другая транзакция
            # не сможет изменить её до коммита/роллбэка.
            result = await s.execute(
                select(Lot)
                .where(Lot.id == lot_id)
                .with_for_update()
            )
            lot = result.scalar_one_or_none()

            if not lot:
                return False, "Лот не найден", None

            if lot.status != LotStatus.ACTIVE:
                return False, "Аукцион не активен", None

            # Проверить время
            if lot.ends_at:
                ends = (
                    lot.ends_at if lot.ends_at.tzinfo
                    else lot.ends_at.replace(tzinfo=timezone.utc)
                )
                if ends <= datetime.now(timezone.utc):
                    return False, "Время аукциона истекло", None

            # Проверить минимальную сумму по актуальной (заблокированной) цене
            min_bid = lot.current_price + lot.bid_step
            if amount < min_bid:
                return False, f"Минимальная ставка: {min_bid:,} ₽", None

            # Создать ставку и обновить цену
            bid = Bid(
                lot_id=lot_id,
                user_id=user_id,
                username=username,
                amount=amount,
            )
            s.add(bid)
            lot.current_price = amount
            # begin() коммитит автоматически при выходе из блока

    # Перечитать bid из БД (нужен id и created_at)
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Bid)
            .where(
                Bid.lot_id == lot_id,
                Bid.user_id == user_id,
                Bid.amount == amount,
                Bid.is_cancelled == False,
            )
            .order_by(Bid.id.desc())
            .limit(1)
        )
        bid = result.scalar_one_or_none()

    return True, None, bid


# ── Bans ──────────────────────────────────────────────────────

async def ban_user(user_id: int, username: Optional[str], banned_by: int):
    async with AsyncSessionLocal() as s:
        existing = await s.get(BannedUser, user_id)
        if not existing:
            s.add(BannedUser(user_id=user_id, username=username, banned_by=banned_by))
            await s.commit()


async def is_banned(user_id: int) -> bool:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(BannedUser).where(BannedUser.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None


# ── Watchlist ─────────────────────────────────────────────────

async def add_to_watchlist(lot_id: int, user_id: int, username: Optional[str]):
    async with AsyncSessionLocal() as s:
        existing = await s.execute(
            select(Watchlist).where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        if existing.scalar_one_or_none() is None:
            s.add(Watchlist(lot_id=lot_id, user_id=user_id, username=username))
            await s.commit()


async def remove_from_watchlist(lot_id: int, user_id: int):
    async with AsyncSessionLocal() as s:
        await s.execute(
            Watchlist.__table__.delete().where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        await s.commit()


async def is_watching(lot_id: int, user_id: int) -> bool:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Watchlist).where(
                Watchlist.lot_id == lot_id, Watchlist.user_id == user_id
            )
        )
        return result.scalar_one_or_none() is not None


async def get_watchers(lot_id: int) -> list[Watchlist]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Watchlist).where(Watchlist.lot_id == lot_id)
        )
        return list(result.scalars().all())


# ── Stats ─────────────────────────────────────────────────────

async def get_stats() -> dict:
    async with AsyncSessionLocal() as s:
        total_lots = (
            await s.execute(select(func.count()).select_from(Lot))
        ).scalar_one()
        finished_lots = (
            await s.execute(
                select(func.count()).where(Lot.status == LotStatus.FINISHED)
            )
        ).scalar_one()
        total_turnover = (
            await s.execute(
                select(func.sum(Lot.final_price)).where(
                    Lot.status == LotStatus.FINISHED
                )
            )
        ).scalar_one() or 0
        total_bids = (
            await s.execute(
                select(func.count()).select_from(Bid).where(Bid.is_cancelled == False)
            )
        ).scalar_one()
        unique_bidders = (
            await s.execute(
                select(func.count(Bid.user_id.distinct())).where(
                    Bid.is_cancelled == False
                )
            )
        ).scalar_one()

    return {
        "total_lots":    total_lots,
        "finished_lots": finished_lots,
        "total_turnover": total_turnover,
        "total_bids":    total_bids,
        "unique_bidders": unique_bidders,
    }


# ── Lots by user bids (Mini App «Мои аукционы») ───────────────

async def get_lots_by_user(user_id: int, limit: int = 50) -> list[dict]:
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(
                Bid.lot_id,
                Lot.title,
                Lot.emoji,
                Lot.status,
                Lot.winner_user_id,
                Lot.final_price,
                func.max(Bid.amount).label("my_max"),
            )
            .join(Lot, Lot.id == Bid.lot_id)
            .where(Bid.user_id == user_id, Bid.is_cancelled == False)
            .group_by(
                Bid.lot_id, Lot.title, Lot.emoji,
                Lot.status, Lot.winner_user_id, Lot.final_price,
            )
            .order_by(Bid.lot_id.desc())
            .limit(limit)
        )
        rows = result.all()
        return [
            {
                "lot_id":      r.lot_id,
                "title":       r.title,
                "emoji":       r.emoji,
                "status":      r.status,
                "won":         r.winner_user_id == user_id,
                "my_max":      r.my_max,
                "final_price": r.final_price,
            }
            for r in rows
        ]


# ── Rating ────────────────────────────────────────────────────

async def save_rating(lot_id: int, user_id: int, stars: int):
    from db.database import Rating
    async with AsyncSessionLocal() as s:
        existing = await s.execute(
            select(Rating).where(
                Rating.lot_id == lot_id, Rating.user_id == user_id
            )
        )
        rating = existing.scalar_one_or_none()
        if rating:
            rating.stars = stars
        else:
            s.add(Rating(lot_id=lot_id, user_id=user_id, stars=stars))
        await s.commit()


# ── Aliases (для совместимости с bot.py) ──────────────────────

async def update_card_message_id(lot_id: int, message_id: int):
    await set_card_message_id(lot_id, message_id)


async def save_client_photo_file_id(lot_id: int, file_id: str):
    from sqlalchemy import update as sa_update
    async with AsyncSessionLocal() as s:
        await s.execute(
            sa_update(Lot).where(Lot.id == lot_id).values(client_photo_file_id=file_id)
        )
        await s.commit()


# ── pause / resume (добавлено для handlers/manage.py) ─────────

async def pause_lot(lot_id: int, seconds_left: int):
    async with AsyncSessionLocal() as s:
        from sqlalchemy import update as sa_update
        from db.database import LotStatus as _LS
        await s.execute(
            sa_update(Lot).where(Lot.id == lot_id)
            .values(status=_LS.PAUSED, seconds_left=seconds_left)
        )
        await s.commit()


async def resume_lot(lot_id: int, new_ends_at):
    async with AsyncSessionLocal() as s:
        from sqlalchemy import update as sa_update
        from db.database import LotStatus as _LS
        await s.execute(
            sa_update(Lot).where(Lot.id == lot_id)
            .values(status=_LS.ACTIVE, ends_at=new_ends_at, seconds_left=None)
        )
        await s.commit()

```


## File: auction_group_bot\handlers\__init__.py
```python


```


## File: auction_group_bot\handlers\bidding.py
```python
import texts as T
import asyncio
import logging
from datetime import timezone
from typing import Dict, Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db.queries import (
    add_to_watchlist, get_bid_count, get_lot, get_top_bid,
    place_bid, remove_from_watchlist, get_watchers,
)
from db.database import LotStatus
from keyboards.inline import (
    kb_after_bid, kb_overbid, kb_lot_card,
    kb_rating, kb_back_to_start, kb_cancel_custom_bid,
    kb_confirm_bid, kb_winner,
)
from utils.formatting import (
    bid_accepted_text, fmt_price, lot_card_text, overbid_notify_text,
)
from utils.scheduler import apply_antisnipe
from utils.states import CustomBidFSM

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "noop")
async def cb_noop(callback: CallbackQuery):
    await callback.answer(T.BID_NOT_STARTED, show_alert=False)


@router.callback_query(F.data.startswith("help:"))
async def cb_help(callback: CallbackQuery):
    from config import HELP_TEXT
    try:
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=HELP_TEXT,
            parse_mode="HTML",
        )
        await callback.answer("📩 Правила отправлены в личку", show_alert=False)
    except Exception:
        # Если бот не может написать в личку — показываем короткий текст
        await callback.answer(T.BID_START_FIRST, show_alert=True)

# Хранилище pending-подтверждений: {user_id: {lot_id, amount, is_blitz, task}}
_pending: Dict[int, Dict[str, Any]] = {}

CONFIRM_TIMEOUT = 30  # секунд до автоотмены


# ─────────────────────────────────────────────────────────────
# ПОРЯДОК ВАЖЕН: специфичные фильтры — ВЫШЕ общих
# ─────────────────────────────────────────────────────────────


# ── Custom bid — шаг 1: кнопка «✏️ Своя сумма» ───────────────

@router.callback_query(F.data.regexp(r"^bid:custom:\d+$"))
async def cb_custom_bid_start(callback: CallbackQuery, state: FSMContext):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer(T.MANAGE_LOT_NOT_FOUND, show_alert=True)
        return
    if lot.status != LotStatus.ACTIVE:
        await callback.answer("Аукцион не активен.", show_alert=True)
        return

    await state.set_state(CustomBidFSM.waiting_for_amount)
    await state.update_data(lot_id=lot_id)

    min_bid = lot.current_price + lot.bid_step
    blitz_line = f"\n🔥 Блиц-цена: <b>{fmt_price(lot.blitz_price)}</b>" if lot.blitz_price else ""

    try:
        await callback.bot.send_message(
            chat_id=callback.from_user.id,
            text=(
                f"✏️ <b>Введите сумму ставки</b>\n\n"
                f"{lot.emoji} {lot.title}\n"
                f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
                f"Минимальная ставка: <b>{fmt_price(min_bid)}</b>"
                f"{blitz_line}\n\n"
                f"Напишите сумму числом (например: <code>{min_bid}</code>)"
            ),
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        await callback.answer("✏️ Напишите сумму в личку боту")
    except Exception as e:
        logger.debug(f"Custom bid DM failed: {e}")
        await state.clear()
        await callback.answer(
            "❌ Сначала напишите боту /start в личку — иначе он не сможет написать вам.",
            show_alert=True,
        )


# ── Custom bid — отмена ───────────────────────────────────────

@router.callback_query(F.data.regexp(r"^bid:custom:cancel:\d+$"))
async def cb_custom_bid_cancel(callback: CallbackQuery, state: FSMContext):
    lot_id = int(callback.data.split(":")[3])
    await state.clear()
    await callback.message.edit_text(
        "❌ Ввод ставки отменён.",
        reply_markup=kb_after_bid(lot_id),
    )
    await callback.answer()


# ── Custom bid — шаг 2: получить сумму ───────────────────────

@router.message(CustomBidFSM.waiting_for_amount)
async def msg_custom_bid_amount(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return

    data = await state.get_data()
    lot_id = data.get("lot_id")
    if not lot_id:
        await state.clear()
        return

    raw = (message.text or "").strip()
    raw = raw.replace(" ", "").replace(",", "").replace(".", "").replace("\u202f", "").replace("\xa0", "")

    if not raw.isdigit():
        lot = await get_lot(lot_id)
        min_bid = (lot.current_price + lot.bid_step) if lot else 0
        await message.answer(
            f"❌ Введите число без букв.\nНапример: <code>{min_bid}</code>",
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        return

    amount = int(raw)
    lot = await get_lot(lot_id)

    if not lot:
        await state.clear()
        await message.answer(T.MANAGE_LOT_NOT_FOUND)
        return

    min_bid = lot.current_price + lot.bid_step
    if amount < min_bid:
        await message.answer(
            f"❌ Ставка слишком низкая.\n"
            f"Минимум: <b>{fmt_price(min_bid)}</b>\n\n"
            f"Введите другую сумму:",
            reply_markup=kb_cancel_custom_bid(lot_id),
            parse_mode="HTML",
        )
        return

    await state.clear()

    # Отправить подтверждение в личку
    is_blitz = bool(lot.blitz_price and amount >= lot.blitz_price)
    await _send_confirm_dm(message.bot, message.from_user.id, lot, amount, is_blitz)


# ── Ставка по кнопке из топика — отправить подтверждение в личку

@router.callback_query(F.data.regexp(r"^bid:\d+:\d+(:\w+)?$"))
async def cb_bid_request(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id = int(parts[1])
    amount = int(parts[2])
    is_blitz = len(parts) > 3 and parts[3] == "blitz"
    from_topic = callback.message.chat.type in ("group", "supergroup")

    # Из личного чата (кнопки перебития) — тоже через подтверждение
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer(T.MANAGE_LOT_NOT_FOUND, show_alert=True)
        return
    if lot.status != LotStatus.ACTIVE:
        await callback.answer("Аукцион завершён.", show_alert=True)
        return

    user_id = callback.from_user.id

    # Отменить предыдущий pending если был
    old = _pending.pop(user_id, None)
    if old and old.get("task"):
        old["task"].cancel()

    try:
        await _send_confirm_dm(callback.bot, user_id, lot, amount, is_blitz)
        await callback.answer("📩 Подтвердите ставку в личке бота", show_alert=False)
    except Exception as e:
        logger.debug(f"Confirm DM failed: {e}")
        await callback.answer(
            "❌ Сначала напишите боту /start в личку — иначе он не сможет написать вам.",
            show_alert=True,
        )


# ── Подтверждение ставки (из лички) ──────────────────────────

@router.callback_query(F.data.regexp(r"^bid:confirm:\d+:\d+$"))
async def cb_bid_confirmed(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id = int(parts[2])
    amount = int(parts[3])
    user_id = callback.from_user.id

    pending = _pending.pop(user_id, None)
    if pending and pending.get("task"):
        pending["task"].cancel()

    is_blitz = pending.get("is_blitz", False) if pending else False

    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        await callback.message.edit_text(
            "❌ Аукцион уже завершён, ставка не принята.",
            parse_mode="HTML",
        )
        await callback.answer()
        return

    await _execute_bid(
        bot=callback.bot,
        lot_id=lot_id,
        user_id=user_id,
        username=callback.from_user.username,
        amount=amount,
        reply_fn=callback.message.edit_text,
        from_topic=False,
        callback=callback,
        is_blitz=is_blitz,
    )


# ── Отмена подтверждения (из лички) ──────────────────────────

@router.callback_query(F.data.regexp(r"^bid:cancel_confirm:\d+$"))
async def cb_bid_cancel_confirm(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    user_id = callback.from_user.id

    pending = _pending.pop(user_id, None)
    if pending and pending.get("task"):
        pending["task"].cancel()

    lot = await get_lot(lot_id)
    lot_name = f"{lot.emoji} {lot.title}" if lot else "лот"
    await callback.message.edit_text(
        f"❌ Ставка отменена.\n\n{lot_name}",
        parse_mode="HTML",
    )
    await callback.answer(T.BID_CANCELLED)


# ── Watch ─────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("watch:on:"))
async def cb_watch_on(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer(T.MANAGE_LOT_NOT_FOUND, show_alert=True)
        return
    await add_to_watchlist(lot_id, callback.from_user.id, callback.from_user.username)
    await callback.answer("🔔 Пришлём результат в личку!", show_alert=True)


# ── Helpers ───────────────────────────────────────────────────

async def _send_confirm_dm(bot, user_id: int, lot, amount: int, is_blitz: bool):
    """Отправить сообщение с подтверждением в личку и запустить таймер."""
    blitz_note = "\n\n🔥 <b>Это блиц-цена — аукцион завершится мгновенно!</b>" if is_blitz else ""
    confirm_text = (
        f"⚡ <b>Подтвердите ставку</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"Ваша ставка: <b>{fmt_price(amount)}</b>"
        f"{blitz_note}\n\n"
        f"⏱ У вас {CONFIRM_TIMEOUT} секунд"
    )
    msg = await bot.send_message(
        chat_id=user_id,
        text=confirm_text,
        reply_markup=kb_confirm_bid(lot.id, amount, is_blitz),
        parse_mode="HTML",
    )

    # Сохранить pending
    old = _pending.pop(user_id, None)
    if old and old.get("task"):
        old["task"].cancel()

    task = asyncio.create_task(
        _auto_expire_confirm(bot, user_id, lot.id, msg.chat.id, msg.message_id)
    )
    _pending[user_id] = {
        "lot_id": lot.id,
        "amount": amount,
        "is_blitz": is_blitz,
        "task": task,
    }


async def _auto_expire_confirm(bot, user_id: int, lot_id: int, chat_id: int, message_id: int):
    """Через CONFIRM_TIMEOUT сек убрать кнопки и сообщить об истечении."""
    await asyncio.sleep(CONFIRM_TIMEOUT)
    if user_id in _pending and _pending[user_id].get("lot_id") == lot_id:
        _pending.pop(user_id, None)
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="⌛ Время на подтверждение истекло. Сделайте ставку заново.",
                parse_mode="HTML",
            )
        except Exception:
            pass


async def _execute_bid(
    bot, lot_id: int, user_id: int, username,
    amount: int, reply_fn, from_topic: bool,
    callback=None, is_blitz: bool = False,
):
    prev_top = await get_top_bid(lot_id)
    prev_leader_id = prev_top.user_id if (prev_top and prev_top.user_id != user_id) else None

    success, reason, bid = await place_bid(lot_id, user_id, username, amount)
    if not success:
        if callback:
            await callback.answer(f"❌ {reason}", show_alert=True)
        await reply_fn(f"❌ {reason}", parse_mode="HTML")
        return

    lot = await get_lot(lot_id)
    bid_count = await get_bid_count(lot_id)

    # Антиснайпинг
    antisnipe_triggered = False
    if lot.ends_at and not is_blitz:
        ends_at = lot.ends_at
        if ends_at.tzinfo is None:
            ends_at = ends_at.replace(tzinfo=timezone.utc)
        new_ends_at = await apply_antisnipe(lot_id, ends_at, bot)
        if new_ends_at != ends_at:
            antisnipe_triggered = True
            lot = await get_lot(lot_id)

    if not is_blitz and lot.blitz_price and amount >= lot.blitz_price:
        is_blitz = True

    # ── БЛИЦ ──────────────────────────────────────────────────
    if is_blitz and lot.blitz_price and amount >= lot.blitz_price:
        from db.queries import finish_lot
        from utils.scheduler import cancel_auction_job
        from utils.formatting import winner_text

        await finish_lot(lot_id, user_id, username or "", amount)
        lot = await get_lot(lot_id)
        cancel_auction_job(lot_id)
        winner_name = f"@{username}" if username else f"id{user_id}"

        await _update_group_card(bot, lot, bid_count, finished=True)

        await reply_fn(
            bid_accepted_text(lot, amount, is_blitz=True),
            reply_markup=kb_rating(lot_id),
            parse_mode="HTML",
        )
        if callback:
            await callback.answer("🔥 Блиц! Вы победили!")

        try:
            await bot.send_message(
                chat_id=user_id,
                text=winner_text(lot, amount),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.debug(f"Winner DM failed: {e}")

        await _notify_watchers_finish(bot, lot, amount, user_id)
        return

    # ── ОБЫЧНАЯ СТАВКА ────────────────────────────────────────
    antisnipe_note = "\n\n⏱ <i>Антиснайпинг: таймер продлён на 2 мин</i>" if antisnipe_triggered else ""

    if antisnipe_triggered:
        from config import GROUP_ID
        if GROUP_ID and lot.topic_id:
            try:
                from utils.formatting import fmt_time_left
                new_ends = lot.ends_at
                await bot.send_message(
                    chat_id=GROUP_ID,
                    message_thread_id=lot.topic_id,
                    text=(
                        f"⏱ <b>Антиснайпинг!</b>\n\n"
                        f"Ставка сделана в последние минуты — таймер продлён.\n"
                        f"Новое время окончания: <b>{fmt_time_left(new_ends)}</b>"
                    ),
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.debug(f"Antisnipe topic notify failed: {e}")

    await _update_group_card(bot, lot, bid_count)

    await reply_fn(
        bid_accepted_text(lot, amount) + antisnipe_note,
        reply_markup=kb_after_bid(lot_id),
        parse_mode="HTML",
    )
    if callback:
        await callback.answer("✅ Ставка принята!")

    await add_to_watchlist(lot_id, user_id, username)

    if prev_leader_id and prev_leader_id != user_id:
        try:
            await bot.send_message(
                chat_id=prev_leader_id,
                text=overbid_notify_text(lot, amount),
                reply_markup=kb_overbid(lot_id, amount, lot.bid_step),
                parse_mode="HTML",
            )
        except Exception as e:
            logger.debug(f"Overbid notify failed: {e}")


async def _update_group_card(bot, lot, bid_count: int, finished: bool = False):
    from config import GROUP_ID
    from db.queries import get_top_bid
    from utils.formatting import lot_card_text, auction_finished_text

    if not GROUP_ID or not lot.topic_id or not lot.card_message_id:
        return

    top_bid = await get_top_bid(lot.id)

    if finished and top_bid:
        text = auction_finished_text(lot, top_bid.amount)
        reply_markup = None
    else:
        text = lot_card_text(lot, bid_count, top_bid)
        reply_markup = kb_lot_card(lot)

    try:
        if lot.client_photo_file_id:
            await bot.edit_message_caption(
                chat_id=GROUP_ID,
                message_id=lot.card_message_id,
                caption=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
        else:
            await bot.edit_message_text(
                chat_id=GROUP_ID,
                message_id=lot.card_message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
    except Exception as e:
        logger.debug(f"Card update failed: {e}")


async def _notify_watchers_finish(bot, lot, final_price: int, winner_id: int):
    watchers = await get_watchers(lot.id)
    for w in watchers:
        if w.user_id == winner_id:
            continue
        try:
            await bot.send_message(
                chat_id=w.user_id,
                text=T.WATCHER_FINISHED.format(
                    emoji=lot.emoji,
                    title=lot.title,
                    final_price=fmt_price(final_price),
                ),
                reply_markup=kb_back_to_start(),
                parse_mode="HTML",
            )
        except Exception:
            pass


```


## File: auction_group_bot\handlers\create_lot.py
```python
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


```


## File: auction_group_bot\handlers\finish.py
```python
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_bid_count, get_lot, get_unique_bidder_count
from keyboards.inline import kb_back_to_main, kb_winner
from utils.formatting import report_text
from utils.guards import admin_only_callback

router = Router()


@router.callback_query(F.data.startswith("win:report:"))
async def cb_report(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    await callback.message.edit_text(
        report_text(lot, bid_count, user_count),
        reply_markup=kb_back_to_main(),
        parse_mode="HTML",
    )
    await callback.answer()


```


## File: auction_group_bot\handlers\lots.py
```python
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import (
    get_active_lots, get_bid_count, get_lot,
    get_top_bid, get_unique_bidder_count, is_watching,
)
from keyboards.inline import kb_lot_card_dm, kb_lots_list
from utils.formatting import lot_card_text, lot_detail_text, lot_list_text

router = Router()


# ── Lots list ─────────────────────────────────────────────────

@router.callback_query(F.data == "lots:list")
async def cb_lots_list(callback: CallbackQuery):
    lots = await get_active_lots()
    text = lot_list_text(lots)
    try:
        await callback.message.edit_text(
            text,
            reply_markup=kb_lots_list(lots),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer()


# ── Open lot card ─────────────────────────────────────────────

@router.callback_query(F.data.startswith("lot:view:"))
async def cb_view_lot(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    top_bid = await get_top_bid(lot_id)
    watching = await is_watching(lot_id, callback.from_user.id)

    user_is_leader = top_bid and top_bid.user_id == callback.from_user.id

    text = lot_card_text(lot, bid_count, top_bid, watching)
    kb = kb_lot_card_dm(lot, watching=watching)

    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer()


# ── Lot details ───────────────────────────────────────────────

@router.callback_query(F.data.startswith("lot:detail:"))
async def cb_lot_detail(callback: CallbackQuery):
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)

    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="← Назад к карточке", callback_data=f"lot:view:{lot_id}"))

    try:
        await callback.message.edit_text(
            lot_detail_text(lot, bid_count, user_count),
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )
    except Exception:
        pass
    await callback.answer()


```


## File: auction_group_bot\handlers\main_menu.py
```python
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


```


## File: auction_group_bot\handlers\manage.py
```python
from datetime import datetime, timedelta, timezone

from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.database import LotStatus
from db.queries import (
    ban_user, cancel_lot, cancel_user_bids, extend_lot,
    get_bid_count, get_bidders_for_lot, get_lot, get_top_bid,
    get_unique_bidder_count, pause_lot, resume_lot,
)
from keyboards.inline import (
    kb_ban_confirm, kb_ban_pick, kb_back_to_main, kb_confirm_action,
    kb_extend_pick, kb_manage, kb_manage_paused, kb_monitor,
)
from utils.formatting import fmt_price, fmt_time_left
from utils.guards import admin_only_callback
from utils.scheduler import cancel_auction_job, schedule_auction_finish

router = Router()


# ── Open manage panel ─────────────────────────────────────────

@router.callback_query(F.data.startswith("mon:manage:"))
async def cb_open_manage(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _show_manage(callback, lot_id)
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:menu:"))
async def cb_manage_menu(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _show_manage(callback, lot_id)
    await callback.answer()


async def _show_manage(callback: CallbackQuery, lot_id: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    bid_count = await get_bid_count(lot_id)
    top_bid = await get_top_bid(lot_id)
    leader = f"@{top_bid.username}" if (top_bid and top_bid.username) else (
        f"id{top_bid.user_id}" if top_bid else "нет ставок"
    )
    text = (
        f"⚙️ <b>Управление · {lot.emoji} {lot.title}</b>\n\n"
        f"Статус: {'⏸ на паузе' if lot.status == LotStatus.PAUSED else '🟢 активен'}\n"
        f"Цена: <b>{fmt_price(lot.current_price)}</b>  ·  {bid_count} ставок\n"
        f"Лидер: {leader}\n"
        f"Осталось: {fmt_time_left(lot.ends_at)}"
    )
    kb = kb_manage_paused(lot_id) if lot.status == LotStatus.PAUSED else kb_manage(lot_id)
    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except Exception:
        pass


# ── Pause ─────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:pause:"))
async def cb_pause(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        await callback.answer("Нельзя поставить на паузу.", show_alert=True)
        return

    # Calculate remaining seconds
    now = datetime.now(timezone.utc)
    seconds_left = max(0, int((lot.ends_at - now).total_seconds())) if lot.ends_at else 0
    await pause_lot(lot_id, seconds_left)
    cancel_auction_job(lot_id)

    # Notify group
    await _notify_group(callback, lot, "⏸ Аукцион временно приостановлен.")

    await callback.message.edit_text(
        f"⏸ <b>Аукцион приостановлен.</b>\n\n"
        f"Таймер остановлен. Ставки заморожены.\n"
        f"Осталось: {seconds_left // 3600}ч {(seconds_left % 3600) // 60}м",
        reply_markup=kb_manage_paused(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("⏸ Приостановлен")


# ── Resume ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:resume:"))
async def cb_resume(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.PAUSED:
        await callback.answer("Лот не на паузе.", show_alert=True)
        return

    secs = lot.seconds_left or 3600
    new_ends_at = datetime.now(timezone.utc) + timedelta(seconds=secs)
    await resume_lot(lot_id, new_ends_at)

    bot = callback.bot
    from config import GROUP_BOT_TOKEN
    from aiogram import Bot as AiogramBot
    winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
    schedule_auction_finish(lot_id, new_ends_at, bot, winner_bot)

    await _notify_group(callback, lot, "▶️ Аукцион возобновлён.")

    await callback.message.edit_text(
        f"▶️ <b>Аукцион возобновлён!</b>\n\n"
        f"Таймер продолжается. Новое время окончания: {fmt_time_left(new_ends_at)}",
        reply_markup=kb_monitor(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("▶️ Возобновлён")


# ── Extend ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:extend_pick:"))
async def cb_extend_pick(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "⏱ <b>Выберите, на сколько продлить:</b>",
        reply_markup=kb_extend_pick(lot_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:extend:"))
async def cb_extend_hours(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts = callback.data.split(":")
    lot_id, hours = int(parts[2]), int(parts[3])
    await _do_extend(callback, lot_id, hours)


async def _do_extend(callback: CallbackQuery, lot_id: int, hours: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return
    base = lot.ends_at or datetime.now(timezone.utc)
    new_ends_at = base + timedelta(hours=hours)
    await extend_lot(lot_id, new_ends_at)

    bot = callback.bot
    if lot.status == LotStatus.ACTIVE:
        from config import GROUP_BOT_TOKEN
        from aiogram import Bot as AiogramBot
        winner_bot = AiogramBot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None
        schedule_auction_finish(lot_id, new_ends_at, bot, winner_bot)

    await _notify_group(callback, lot, f"⏱ Время аукциона продлено на {hours}ч.")

    await callback.message.edit_text(
        f"✅ <b>Время продлено на {hours}ч.</b>\n\n"
        f"Новое время окончания: {fmt_time_left(new_ends_at)}\n"
        f"Участники уведомлены.",
        reply_markup=kb_manage(lot_id),
        parse_mode="HTML",
    )
    await callback.answer(f"+{hours}ч добавлено")


# ── Cancel lot ────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:cancel:"))
async def cb_cancel_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "⚠️ <b>Подтвердите отмену лота</b>\n\n"
        "Все ставки будут аннулированы. Участники получат уведомление.",
        reply_markup=kb_confirm_action(
            yes_cb=f"mgmt:cancel_confirm:{lot_id}",
            no_cb=f"mgmt:menu:{lot_id}",
        ),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:cancel_confirm:"))
async def cb_cancel_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    await cancel_lot(lot_id)
    cancel_auction_job(lot_id)
    bid_count = await get_bid_count(lot_id)

    await _notify_group(callback, lot, f"🚫 Аукцион отменён администратором.")

    await callback.message.edit_text(
        f"🚫 Лот <code>{lot.lot_code}</code> <b>отменён</b>.\n\n"
        f"Топик #{lot.topic_id} закрыт. {bid_count} участников уведомлены.",
        reply_markup=kb_back_to_main(),
        parse_mode="HTML",
    )
    await callback.answer("Лот отменён")


# ── Early finish ──────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:early_finish:"))
async def cb_early_finish_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    top_bid = await get_top_bid(lot_id)
    price_line = f"Текущая цена: <b>{fmt_price(lot.current_price)}</b>" if lot else ""
    leader = ""
    if top_bid:
        name = f"@{top_bid.username}" if top_bid.username else f"id{top_bid.user_id}"
        leader = f"\nЛидер: <b>{name}</b>"

    await callback.message.edit_text(
        f"⚠️ <b>Завершить аукцион досрочно?</b>\n\n"
        f"Победителем становится текущий лидер.\n"
        f"{price_line}{leader}",
        reply_markup=kb_confirm_action(
            yes_cb=f"mgmt:early_confirm:{lot_id}",
            no_cb=f"mgmt:menu:{lot_id}",
        ),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mgmt:early_confirm:"))
async def cb_early_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    from utils.scheduler import _finish_auction_job
    cancel_auction_job(lot_id)

    lot = await get_lot(lot_id)
    if lot and lot.status == LotStatus.PAUSED:
        from db.queries import resume_lot
        await resume_lot(lot_id, datetime.now(timezone.utc))

    # Завершаем через админский бот (обновляет карточку группы),
    # победителю пишем через клиентский бот
    from config import GROUP_BOT_TOKEN
    from aiogram import Bot as AiogramBot
    group_bot = AiogramBot(token=GROUP_BOT_TOKEN)
    try:
        await _finish_auction_job(lot_id, callback.bot, winner_bot=group_bot)
    finally:
        await group_bot.session.close()

    lot = await get_lot(lot_id)
    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)

    from utils.formatting import winner_text
    from keyboards.inline import kb_winner
    await callback.message.edit_text(
        winner_text(lot, bid_count, user_count),
        reply_markup=kb_winner(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("Завершено")


# ── Ban user ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("mgmt:ban_pick:"))
async def cb_ban_pick(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    bidders = await get_bidders_for_lot(lot_id)
    if not bidders:
        await callback.answer("Нет участников для блокировки.", show_alert=True)
        return
    await callback.message.edit_text(
        "👤 <b>Выберите участника для блокировки:</b>",
        reply_markup=kb_ban_pick(lot_id, bidders),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ban:user:"))
async def cb_ban_user_prompt(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts = callback.data.split(":")
    lot_id, user_id = int(parts[2]), int(parts[3])
    bidders = await get_bidders_for_lot(lot_id)
    target = next((b for b in bidders if b["user_id"] == user_id), None)
    name = f"@{target['username']}" if (target and target["username"]) else f"id{user_id}"
    await callback.message.edit_text(
        f"⚠️ <b>Подтвердите блокировку</b>\n\n"
        f"Пользователь: {name}\n"
        f"Все ставки по этому лоту будут аннулированы.",
        reply_markup=kb_ban_confirm(lot_id, user_id),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ban:confirm:"))
async def cb_ban_confirm(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    parts = callback.data.split(":")
    lot_id, user_id = int(parts[2]), int(parts[3])

    # Cancel their bids
    await cancel_user_bids(lot_id, user_id)

    # Recalculate current price
    top_bid = await get_top_bid(lot_id)
    lot = await get_lot(lot_id)
    if lot and top_bid:
        from sqlalchemy import update
        from db.database import AsyncSessionLocal, Lot
        async with AsyncSessionLocal() as s:
            await s.execute(
                update(Lot).where(Lot.id == lot_id).values(current_price=top_bid.amount)
            )
            await s.commit()

    # Add to banned list
    bidders = await get_bidders_for_lot(lot_id)
    username = None
    for b in bidders:
        if b["user_id"] == user_id:
            username = b["username"]
            break
    await ban_user(user_id, username, callback.from_user.id)

    # Try to kick from group
    try:
        from config import GROUP_ID
        await callback.bot.ban_chat_member(chat_id=GROUP_ID, user_id=user_id)
    except Exception:
        pass

    name = f"@{username}" if username else f"id{user_id}"
    await callback.message.edit_text(
        f"🚫 <b>{name} заблокирован.</b>\n\n"
        f"• Ставки аннулированы\n"
        f"• Участник исключён из группы\n"
        f"• Лидерство пересчитано",
        reply_markup=kb_manage(lot_id),
        parse_mode="HTML",
    )
    await callback.answer("Заблокирован")


# ── Repost card with bid buttons ──────────────────────────────

@router.callback_query(F.data.startswith("mgmt:repost:"))
async def cb_repost_card(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    from config import GROUP_ID
    from utils.formatting import lot_card_text
    from db.queries import set_card_message_id
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton

    # Построить клавиатуру ставок
    step = lot.bid_step
    cur = lot.current_price
    builder = InlineKeyboardBuilder()
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
    builder.row(InlineKeyboardButton(
        text="🔔 Уведомить меня",
        callback_data=f"watch:on:{lot.id}",
    ))

    bid_count = await get_bid_count(lot_id)
    top_bid = await get_top_bid(lot_id)
    text = lot_card_text(lot, bid_count, top_bid)

    try:
        # Удалить старую карточку если есть
        if lot.card_message_id and GROUP_ID:
            try:
                await callback.bot.delete_message(
                    chat_id=GROUP_ID,
                    message_id=lot.card_message_id,
                )
            except Exception:
                pass

        # Опубликовать новую
        msg = await callback.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=lot.topic_id,
            text=text,
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
        )
        await set_card_message_id(lot_id, msg.message_id)
        await callback.answer("✅ Карточка переопубликована с кнопками!")
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {e}", show_alert=True)

async def _notify_group(callback: CallbackQuery, lot, text: str):
    from config import GROUP_ID
    if not GROUP_ID or not lot.topic_id:
        return
    try:
        await callback.bot.send_message(
            chat_id=GROUP_ID,
            message_thread_id=lot.topic_id,
            text=text,
        )
    except Exception:
        pass


```


## File: auction_group_bot\handlers\monitor.py
```python
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_bid_count, get_lot, get_recent_bids, get_top_bid, get_unique_bidder_count
from keyboards.inline import kb_monitor
from utils.formatting import monitor_text
from utils.guards import admin_only_callback

router = Router()


async def _render_monitor(callback: CallbackQuery, lot_id: int):
    lot = await get_lot(lot_id)
    if not lot:
        await callback.answer("Лот не найден.", show_alert=True)
        return

    top_bid = await get_top_bid(lot_id)
    bid_count = await get_bid_count(lot_id)
    user_count = await get_unique_bidder_count(lot_id)
    recent = await get_recent_bids(lot_id, 5)

    text = monitor_text(lot, bid_count, user_count, top_bid, recent)

    try:
        await callback.message.edit_text(
            text,
            reply_markup=kb_monitor(lot_id),
            parse_mode="HTML",
        )
    except Exception:
        pass  # "message not modified" — ignore


# Open monitor from lot list
@router.callback_query(F.data.startswith("lot:open:"))
async def cb_open_lot(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _render_monitor(callback, lot_id)
    await callback.answer()


# Refresh button
@router.callback_query(F.data.startswith("mon:refresh:"))
async def cb_refresh(callback: CallbackQuery):
    if not await admin_only_callback(callback):
        return
    lot_id = int(callback.data.split(":")[2])
    await _render_monitor(callback, lot_id)
    await callback.answer("Обновлено ✓")


```


## File: auction_group_bot\handlers\notifications.py
```python
import texts as T
from aiogram import F, Router
from aiogram.types import CallbackQuery

from db.queries import get_lot, save_rating
from keyboards.inline import kb_back_to_start
from utils.formatting import fmt_price

router = Router()


# ── Rating ────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("rate:"))
async def cb_rate(callback: CallbackQuery):
    parts = callback.data.split(":")
    lot_id, stars = int(parts[1]), int(parts[2])

    await save_rating(lot_id, callback.from_user.id, stars)

    emoji = "🙌" if stars >= 4 else "🙏" if stars >= 3 else "😔"
    star_str = "⭐" * stars

    lots = await __import__("db.queries", fromlist=["get_active_lots"]).get_active_lots()

    await callback.message.edit_text(
        f"Спасибо за оценку! {star_str} {emoji}\n\n"
        f"До следующего аукциона! Следите за новыми лотами в группе.",
        reply_markup=kb_back_to_start(),
        parse_mode="HTML",
    )
    await callback.answer(f"Оценка {stars}/5 принята!")


```


## File: auction_group_bot\handlers\welcome.py
```python
"""
auction_group_bot/handlers/welcome.py
──────────────────────────────────────
Изменения:
  1. /start в личке теперь показывает кнопку «Открыть аукционы» (WebApp),
     если MINIAPP_URL задан в .env.
  2. Текст приветствия обновлён под Mini App.
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from config import MINIAPP_URL  # новая переменная — см. config.py

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.type != "private":
        return

    kb = None
    if MINIAPP_URL:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="🔨 Открыть аукционы",
                web_app=WebAppInfo(url=MINIAPP_URL),
            )
        ]])

    await message.answer(
        "👋 <b>Привет!</b>\n\n"
        "Участвуйте в аукционах прямо здесь — делайте ставки, "
        "следите за лотами и получайте уведомления.\n\n"
        "• Сюда придут уведомления если вашу ставку перебьют или вы победите\n"
        "• В мини-аппе видны все активные лоты и ваша история участий\n\n"
        "<i>Нажмите кнопку ниже чтобы открыть список аукционов.</i>",
        reply_markup=kb,
        parse_mode="HTML",
    )

```


## File: auction_group_bot\keyboards\__init__.py
```python


```


## File: auction_group_bot\keyboards\inline.py
```python
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

```


## File: auction_group_bot\utils\__init__.py
```python


```


## File: auction_group_bot\utils\formatting.py
```python
import texts as T
from datetime import datetime, timezone
from typing import Optional

from db.database import Bid, Lot


def fmt_price(amount: int) -> str:
    return f"₽\u00A0{amount:,}".replace(",", "\u202F")


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
    if h > 0:
        return f"{h}ч {m:02d}м"
    return f"{m}:{s:02d}"


def lot_card_text(lot: Lot, bid_count: int, top_bid: Optional[Bid], watching: bool = False, is_caption: bool = False) -> str:
    from datetime import timedelta
    has_bids = top_bid is not None
    blitz_line = f"\n🔥 Блиц-цена: <b>{fmt_price(lot.blitz_price)}</b>" if lot.blitz_price else ""
    watch_line = "\n🔔 <i>Вы следите за лотом</i>" if watching else ""
    status_line = ""
    bids_line = f"🔢 Ставок: {bid_count}" if has_bids else "🔢 Ставок пока нет"

    if lot.status == "scheduled" and lot.starts_at:
        starts = lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc)
        msk = starts.astimezone(timezone(timedelta(hours=3)))
        timer_line = f"🕐 Начало: <b>{msk.strftime('%d.%m в %H:%M')} МСК</b>\n"
    else:
        timer_line = f"⏱ Осталось: {fmt_time_left(lot.ends_at)}\n"

    desc = lot.description or "—"

    return (
        f"{status_line}"
        f"{lot.emoji} <b>{lot.title}</b>\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"📋 {desc}\n\n"
        f"💰 Текущая ставка: <b>{fmt_price(lot.current_price)}</b>\n"
        f"📈 Шаг: {fmt_price(lot.bid_step)}\n"
        f"{timer_line}"
        f"{bids_line}"
        f"{blitz_line}"
        f"{watch_line}"
    )


def lot_detail_text(lot: Lot, bid_count: int, user_count: int) -> str:
    blitz_line = f"\n🔥 Блиц-цена: {fmt_price(lot.blitz_price)}" if lot.blitz_price else ""
    return (
        f"📋 <b>Детали лота {lot.lot_code}</b>\n\n"
        f"{lot.emoji} {lot.title}\n\n"
        f"Описание:\n{lot.description or '—'}\n\n"
        f"• Стартовая цена: {fmt_price(lot.start_price)}\n"
        f"• Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"• Шаг ставки: {fmt_price(lot.bid_step)}\n"
        f"• Ставок: {bid_count}\n"
        f"• Участников: {user_count}"
        f"{blitz_line}"
    )


def bid_accepted_text(lot: Lot, amount: int, is_blitz: bool = False) -> str:
    if is_blitz:
        return (
            f"⚡ <b>БЛИЦ! Вы победили мгновенно!</b>\n\n"
            f"{lot.emoji} {lot.title}\n"
            f"Финальная цена: <b>{fmt_price(amount)}</b>\n\n"
            f"📦 Менеджер свяжется в течение 1 часа."
        )
    return (
        f"✅ <b>Ставка принята!</b>\n\n"
        f"<code>{lot.lot_code}</code> · {lot.emoji} {lot.title}\n"
        f"Ваша ставка: <b>{fmt_price(amount)}</b>\n"
        f"Вы сейчас <b>лидируете</b> 🏆\n\n"
        f"<i>Если вас перебьют — сразу уведомим в личку</i>"
    )


def overbid_notify_text(lot: Lot, new_price: int) -> str:
    """Уведомление о перебитии — без имени того кто перебил."""
    return (
        f"⚠️ <b>Вашу ставку перебили!</b>\n\n"
        f"{lot.emoji} {lot.title}\n"
        f"Новая цена: <b>{fmt_price(new_price)}</b>\n\n"
        f"Хотите ответить?"
    )


def winner_text(lot: Lot, final_price: int) -> str:
    return (
        f"🏆 <b>ВЫ ПОБЕДИЛИ!</b>\n\n"
        f"{lot.emoji} <b>{lot.title}</b>\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"📋 {lot.description or '—'}\n\n"
        f"💰 Финальная цена: <b>{fmt_price(final_price)}</b>\n\n"
        f"📦 Менеджер свяжется с вами в ближайшее время."
    )


def auction_finished_text(lot: Lot, final_price: int) -> str:
    """Объявление в топике — без имени победителя."""
    return T.AUCTION_FINISHED.format(
        emoji=lot.emoji,
        title=lot.title,
        lot_code=lot.lot_code,
        description=lot.description or "—",
        final_price=fmt_price(final_price),
    )



# ── Добавлено для handlers (monitor, finish, lots) ────────────

def monitor_text(lot, bid_count: int, user_count: int, top_bid, recent: list) -> str:
    from datetime import datetime, timezone, timedelta
    leader = (f"@{top_bid.username}" if (top_bid and top_bid.username)
              else (f"id{top_bid.user_id}" if top_bid else "нет ставок"))
    status_emoji = {"active": "🟢", "finished": "✅", "cancelled": "🚫", "scheduled": "🕐"}.get(lot.status, "❓")
    if lot.status == "scheduled" and lot.starts_at:
        starts = lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc)
        msk = starts.astimezone(timezone(timedelta(hours=3)))
        time_line = f"🕐 Начало: {msk.strftime('%d.%m в %H:%M')} МСК"
    else:
        time_line = f"⏱ Осталось: {fmt_time_left(lot.ends_at)}"
    feed = ""
    for b in recent:
        name = f"@{b.username}" if b.username else f"id{b.user_id}"
        feed += f"\n  {name} → {fmt_price(b.amount)}"
    return (
        f"{status_emoji} <b>Мониторинг · {lot.emoji} {lot.title}</b>\n"
        f"<code>{lot.lot_code}</code>\n\n"
        f"💰 Цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"👤 Лидер: {leader}\n"
        f"{time_line}\n"
        f"📊 Ставок: {bid_count}  ·  Участников: {user_count}\n"
        f"\n<b>Последние ставки:</b>{feed if feed else ' —'}"
    )


def report_text(lot, bid_count: int, user_count: int) -> str:
    growth = 0
    if lot.start_price and lot.final_price:
        growth = round((lot.final_price / lot.start_price - 1) * 100)
    winner = (f"@{lot.winner_username}" if lot.winner_username
              else (f"id{lot.winner_user_id}" if lot.winner_user_id else "—"))
    return (
        f"📊 <b>Отчёт по лоту {lot.lot_code}</b>\n\n"
        f"• Название: {lot.emoji} {lot.title}\n"
        f"• Старт: {fmt_price(lot.start_price)}\n"
        f"• Финал: {fmt_price(lot.final_price or lot.current_price)}\n"
        f"• Рост: +{growth}%\n"
        f"• Ставок: {bid_count}  ·  Участников: {user_count}\n"
        f"• Победитель: {winner}"
    )


def lot_list_text(lots: list) -> str:
    if not lots:
        return "📭 <b>Активных лотов нет.</b>\n\nСледите за анонсами в группе."
    lines = []
    for lot in lots:
        status = "🟢" if lot.status == "active" else "🕐"
        time_line = fmt_time_left(lot.ends_at) if lot.status == "active" else "ожидает"
        lines.append(
            f"{status} {lot.emoji} <b>{lot.title}</b>\n"
            f"   <code>{lot.lot_code}</code>  ·  {fmt_price(lot.current_price)}  ·  ⏱ {time_line}"
        )
    return "🏷 <b>Активные аукционы</b>\n\n" + "\n\n".join(lines)


def lot_detail_text(lot, bid_count: int, user_count: int) -> str:
    blitz_line = f"\n🔥 Блиц-цена: {fmt_price(lot.blitz_price)}" if lot.blitz_price else ""
    return (
        f"📋 <b>Детали лота {lot.lot_code}</b>\n\n"
        f"{lot.emoji} {lot.title}\n\n"
        f"Описание:\n{lot.description or '—'}\n\n"
        f"• Стартовая цена: {fmt_price(lot.start_price)}\n"
        f"• Текущая цена: <b>{fmt_price(lot.current_price)}</b>\n"
        f"• Шаг ставки: {fmt_price(lot.bid_step)}\n"
        f"• Ставок: {bid_count}\n"
        f"• Участников: {user_count}"
        f"{blitz_line}"
    )

```


## File: auction_group_bot\utils\guards.py
```python
from functools import wraps
from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def admin_only_message(message: Message) -> bool:
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return False
    return True


async def admin_only_callback(callback: CallbackQuery) -> bool:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён.", show_alert=True)
        return False
    return True


```


## File: auction_group_bot\utils\scheduler.py
```python
import texts as T
import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

logger = logging.getLogger(__name__)

_scheduler: AsyncIOScheduler = None


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    global _scheduler
    _scheduler = AsyncIOScheduler(timezone="UTC")
    return _scheduler


def get_scheduler() -> AsyncIOScheduler:
    return _scheduler


# ── Finish auction ─────────────────────────────────────────────

async def _finish_auction_job(lot_id: int, bot: Bot, winner_bot: Bot = None):
    """
    bot        — бот для обновления карточки группы (может быть админский или клиентский)
    winner_bot — бот для отправки уведомления победителю (всегда клиентский)
                 если не передан — используется bot
    """
    from db.queries import (
        get_lot, get_top_bid, get_bid_count, get_unique_bidder_count,
        finish_lot, cancel_lot_no_bids, get_watchers,
    )
    from db.database import LotStatus
    from utils.formatting import winner_text, auction_finished_text, fmt_price
    from keyboards.inline import kb_back_to_start
    from config import GROUP_ID

    lot = await get_lot(lot_id)
    if not lot or lot.status != LotStatus.ACTIVE:
        return

    top_bid = await get_top_bid(lot_id)
    bid_count = await get_bid_count(lot_id)

    if top_bid:
        await finish_lot(lot_id, top_bid.user_id, top_bid.username or "", top_bid.amount)
        lot = await get_lot(lot_id)

        # Delete card from topic — announcement below will replace it
        if GROUP_ID and lot.topic_id and lot.card_message_id:
            logger.info(f"Deleting card message_id={lot.card_message_id} in chat={GROUP_ID}")
            try:
                await bot.delete_message(
                    chat_id=GROUP_ID,
                    message_id=lot.card_message_id,
                )
                logger.info(f"Card deleted for lot {lot_id}")
            except Exception as e:
                logger.warning(f"Card delete failed: {e}")
        else:
            logger.warning(f"Skip card delete: GROUP_ID={GROUP_ID}, topic_id={lot.topic_id}, card_message_id={lot.card_message_id}")

        # Announce in topic
        if GROUP_ID and lot.topic_id:
            try:
                await bot.send_message(
                    chat_id=GROUP_ID,
                    message_thread_id=lot.topic_id,
                    text=auction_finished_text(lot, top_bid.amount),
                    parse_mode="HTML",
                )
            except Exception as e:
                logger.warning(f"Topic announce failed: {e}")

        # Notify winner in DM
        _winner_bot = winner_bot or bot
        try:
            if lot.client_photo_file_id:
                await _winner_bot.send_photo(
                    chat_id=top_bid.user_id,
                    photo=lot.client_photo_file_id,
                    caption=winner_text(lot, top_bid.amount),
                    parse_mode="HTML",
                )
            else:
                await _winner_bot.send_message(
                    chat_id=top_bid.user_id,
                    text=winner_text(lot, top_bid.amount),
                    parse_mode="HTML",
                )
        except Exception as e:
            logger.warning(f"Winner DM failed for user {top_bid.user_id}: {e}")
            if GROUP_ID and lot.topic_id:
                try:
                    await bot.send_message(
                        chat_id=GROUP_ID,
                        message_thread_id=lot.topic_id,
                        text=(
                            T.WINNER_FALLBACK_TOPIC
                        ),
                        parse_mode="HTML",
                    )
                except Exception:
                    pass

        # Notify watchers (non-winners)
        watchers = await get_watchers(lot_id)
        for w in watchers:
            if w.user_id == top_bid.user_id:
                continue
            try:
                await bot.send_message(
                    chat_id=w.user_id,
                    text=(
                        f"🏁 <b>Аукцион завершён</b>\n\n"
                        f"{lot.emoji} {lot.title}\n"
                        f"Финальная цена: {fmt_price(top_bid.amount)}"
                    ),
                    reply_markup=kb_back_to_start(),
                    parse_mode="HTML",
                )
            except Exception:
                pass

    else:
        # No bids
        await cancel_lot_no_bids(lot_id)
        if GROUP_ID and lot.topic_id:
            try:
                await bot.send_message(
                    chat_id=GROUP_ID,
                    message_thread_id=lot.topic_id,
                    text=T.AUCTION_NO_BIDS.format(emoji=lot.emoji, title=lot.title),
                    parse_mode="HTML",
                )
            except Exception:
                pass


def schedule_auction_finish(lot_id: int, ends_at: datetime, bot: Bot):
    if _scheduler is None:
        return
    job_id = f"finish_lot_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)
    _scheduler.add_job(
        _finish_auction_job,
        trigger="date",
        run_date=ends_at,
        args=[lot_id, bot],
        id=job_id,
        replace_existing=True,
    )


def cancel_auction_job(lot_id: int):
    if _scheduler is None:
        return
    job_id = f"finish_lot_{lot_id}"
    if _scheduler.get_job(job_id):
        _scheduler.remove_job(job_id)


async def apply_antisnipe(lot_id: int, ends_at: datetime, bot: Bot) -> datetime:
    """Если ставка сделана менее чем за ANTISNIPE_SECONDS до конца — продлить."""
    from config import ANTISNIPE_SECONDS
    from db.queries import extend_lot_timer

    now = datetime.now(timezone.utc)
    if ends_at.tzinfo is None:
        ends_at = ends_at.replace(tzinfo=timezone.utc)

    time_left = (ends_at - now).total_seconds()
    if time_left < ANTISNIPE_SECONDS:
        # Всегда устанавливаем ровно ANTISNIPE_SECONDS от текущего момента,
        # а не прибавляем к ends_at — чтобы не накапливалось при нескольких ставках подряд
        new_ends_at = now + timedelta(seconds=ANTISNIPE_SECONDS)
        await extend_lot_timer(lot_id, new_ends_at)
        # Финиш перепланирует admin bot через sync_finish_jobs
        logger.info(f"Antisnipe triggered for lot {lot_id}, extended to {new_ends_at}")
        return new_ends_at
    return ends_at


async def restore_scheduled_jobs(bot: Bot):
    from db.queries import get_active_lots
    from db.database import LotStatus

    now = datetime.now(timezone.utc)
    lots = await get_active_lots()
    for lot in lots:
        if lot.status == LotStatus.ACTIVE and lot.ends_at:
            ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=timezone.utc)
            if ends > now:
                schedule_auction_finish(lot.id, ends, bot)
                logger.info(f"Restored timer for lot {lot.id}")
            else:
                await _finish_auction_job(lot.id, bot)


```


## File: auction_group_bot\utils\states.py
```python
from aiogram.fsm.state import State, StatesGroup


class CustomBidFSM(StatesGroup):
    waiting_for_amount = State()



class CreateLotFSM(StatesGroup):
    entering_title      = State()
    entering_price      = State()
    choosing_step       = State()
    entering_step       = State()
    choosing_duration   = State()
    entering_duration   = State()
    entering_desc       = State()
    uploading_photo     = State()
    choosing_start_time = State()
    entering_start_time = State()
    confirming          = State()
    entering_topic_id   = State()


class CustomBidFSM(StatesGroup):
    waiting_for_amount = State()

```


## File: miniapp\README.md
```markdown
# Auction Mini App

Telegram Mini App для участия в аукционах.  
Работает поверх существующей БД ботов — никаких изменений в боте не требуется.

## Структура

```
miniapp/
├── backend/          # FastAPI — API сервер
│   ├── main.py       # Все эндпоинты
│   ├── database.py   # Копия моделей из бота (держать в синхронизации)
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/         # React SPA
    ├── src/
    │   ├── App.jsx               # Корень, роутинг экранов
    │   ├── pages/
    │   │   ├── LotList.jsx       # Экран списка (Все / Мои аукционы)
    │   │   └── LotDetail.jsx     # Экран лота + кнопка ставки
    │   ├── components/
    │   │   ├── LotCard.jsx       # Компактная карточка
    │   │   └── BidSheet.jsx      # Bottom sheet ставки
    │   ├── hooks/
    │   │   ├── useTelegram.js    # Telegram WebApp SDK
    │   │   └── useTimer.js       # Countdown таймер
    │   └── utils/
    │       ├── api.js            # Запросы к бэкенду
    │       └── format.js         # Форматирование цен, времени
    └── public/index.html         # Подключает telegram-web-app.js
```

## Быстрый старт

### 1. Бэкенд

```bash
cd backend
pip install -r requirements.txt
cp .env .env
# Заполните DATABASE_URL и GROUP_BOT_TOKEN
uvicorn main:app --host 0.0.0.0 --port 8000
```

`.env`:
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/auction
GROUP_BOT_TOKEN=токен_группового_бота
```

### 2. Фронтенд

```bash
cd frontend
npm install
REACT_APP_API_URL=https://your-domain.com npm run build
# Раздавайте папку build/ через nginx
```

Для разработки:
```bash
npm start   # Запустится на :3000, проксирует /api на :8000
```

### 3. Nginx (пример)

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    # Frontend (React build)
    root /var/www/miniapp/frontend/build;
    index index.html;
    location / { try_files $uri /index.html; }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

### 4. Регистрация Mini App в BotFather

```
/newapp  (или /editapp для существующего бота)
→ Выбрать бота
→ Указать URL: https://your-domain.com
```

Добавьте кнопку в группового бота (`auction_group_bot/handlers/welcome.py`):
```python
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(
        text="🔨 Открыть аукционы",
        web_app=WebAppInfo(url="https://your-domain.com")
    )
]])
```

## API

| Метод | Путь | Описание |
|-------|------|----------|
| GET   | `/api/lots`        | Все активные и запланированные лоты |
| GET   | `/api/lots/mine`   | Лоты, где пользователь делал ставки |
| GET   | `/api/lots/{id}`   | Один лот |
| POST  | `/api/bids`        | Сделать ставку `{lot_id, amount}` |

Все запросы требуют заголовок `x-tg-init-data` с данными из `Telegram.WebApp.initData`.

## Аутентификация

Бэкенд верифицирует подпись Telegram через HMAC-SHA256.  
В dev-режиме (без `GROUP_BOT_TOKEN`) верификация пропускается.

## Что остаётся в боте

Административная часть (`auction_admin_bot`) не затрагивается:
- создание лотов
- управление (пауза, продление, досрочное завершение)
- уведомления победителям
- антиснайпинг

Mini App только **читает** данные и **принимает ставки** — всё остальное делают боты.

## Синхронизация моделей

`backend/database.py` — точная копия `auction_admin_bot/db/database.py`.  
При изменении схемы БД обновляйте оба файла.  
В production рекомендуется вынести модели в shared-пакет.

```


## File: miniapp\backend\database.py
```python
"""
Shared database models.
This file mirrors auction_admin_bot/db/database.py — keep in sync.
In production: install as a shared package or symlink.
"""
from __future__ import annotations

import enum
import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum, ForeignKey,
    Float, Integer, String, Text, func,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./auction.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class LotStatus(str, enum.Enum):
    PENDING   = "pending"
    SCHEDULED = "scheduled"
    ACTIVE    = "active"
    FINISHED  = "finished"
    CANCELLED = "cancelled"


class Lot(Base):
    __tablename__ = "lots"

    id:           Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_code:     Mapped[str]           = mapped_column(String(20), unique=True)
    category:     Mapped[str]           = mapped_column(String(64))
    emoji:        Mapped[str]           = mapped_column(String(8))
    title:        Mapped[str]           = mapped_column(String(256))
    description:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo_file_id:        Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    client_photo_file_id: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    start_price:   Mapped[int]           = mapped_column(Integer)
    bid_step:      Mapped[int]           = mapped_column(Integer)
    blitz_price:   Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    current_price: Mapped[int]           = mapped_column(Integer)

    duration_hours: Mapped[float]              = mapped_column(Float)
    starts_at:      Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ends_at:        Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    topic_id:        Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    card_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    status:     Mapped[LotStatus] = mapped_column(Enum(LotStatus), default=LotStatus.PENDING)
    created_by: Mapped[int]       = mapped_column(BigInteger)
    created_at: Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now())

    winner_user_id:  Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    winner_username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    final_price:     Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    bids: Mapped[list[Bid]] = relationship("Bid", back_populates="lot", order_by="Bid.id.desc()")


class Bid(Base):
    __tablename__ = "bids"

    id:           Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    lot_id:       Mapped[int]           = mapped_column(ForeignKey("lots.id"))
    user_id:      Mapped[int]           = mapped_column(BigInteger)
    username:     Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    amount:       Mapped[int]           = mapped_column(Integer)
    is_cancelled: Mapped[bool]          = mapped_column(Boolean, default=False)
    created_at:   Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())

    lot: Mapped[Lot] = relationship("Lot", back_populates="bids")


class BannedUser(Base):
    __tablename__ = "banned_users"

    id:        Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:   Mapped[int]           = mapped_column(BigInteger, unique=True)
    username:  Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    banned_at: Mapped[datetime]      = mapped_column(DateTime(timezone=True), server_default=func.now())
    banned_by: Mapped[int]           = mapped_column(BigInteger)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```


## File: miniapp\backend\main.py
```python
"""
miniapp/backend/main.py
"""
import hashlib
import hmac
import json
import logging
import os
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import parse_qsl
from dotenv import load_dotenv
load_dotenv()

import httpx
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select, update

from database import (
    AsyncSessionLocal, Base, Bid, BannedUser, Lot, LotStatus,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Auction Mini App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROUP_BOT_TOKEN = os.getenv("GROUP_BOT_TOKEN", "")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "")


def verify_telegram_init_data(init_data: str, bot_token: str) -> Optional[dict]:
    try:
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        hash_value = parsed.pop("hash", "")
        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed.items())
        )
        secret_key = hmac.new(
            b"WebAppData", bot_token.encode(), hashlib.sha256
        ).digest()
        expected = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(expected, hash_value):
            return None
        user_data = json.loads(parsed.get("user", "{}"))
        return user_data
    except Exception:
        return None


def get_current_user(x_tg_init_data: Optional[str] = Header(None)) -> dict:
    if not GROUP_BOT_TOKEN:
        return {"id": 0, "username": "dev_user"}
    if not x_tg_init_data:
        return {"id": 0, "username": "dev_user"}
    user = verify_telegram_init_data(x_tg_init_data, GROUP_BOT_TOKEN)
    if not user:
        return {"id": 0, "username": "dev_user"}
    return user


class BidRequest(BaseModel):
    lot_id: int
    amount: int


def fmt_price(amount: int) -> str:
    return f"₽\u00A0{amount:,}".replace(",", "\u202F")


def lot_to_dict(lot: Lot, user_id: int, top_bid: Optional[Bid] = None) -> dict:
    now = datetime.now(timezone.utc)
    seconds_left = 0
    if lot.ends_at:
        ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=timezone.utc)
        seconds_left = max(0, int((ends - now).total_seconds()))

    my_bid = None
    is_leading = False
    if top_bid:
        is_leading = top_bid.user_id == user_id
        if is_leading:
            my_bid = top_bid.amount

    return {
        "id":             lot.id,
        "lot_code":       lot.lot_code,
        "emoji":          lot.emoji,
        "title":          lot.title,
        "description":    lot.description or "",
        "photo_file_id":  lot.photo_file_id,
        "start_price":    lot.start_price,
        "current_price":  lot.current_price,
        "bid_step":       lot.bid_step,
        "blitz_price":    lot.blitz_price,
        "status":         lot.status.value if hasattr(lot.status, "value") else lot.status,
        "seconds_left":   seconds_left,
        "ends_at":        lot.ends_at.isoformat() if lot.ends_at else None,
        "starts_at":      lot.starts_at.isoformat() if lot.starts_at else None,
        "topic_id":       lot.topic_id,
        "my_bid":         my_bid,
        "is_leading":     is_leading,
        "winner_user_id": lot.winner_user_id,
        "final_price":    lot.final_price,
    }


@app.get("/api/photo/{file_id:path}")
async def get_photo(file_id: str):
    token = ADMIN_BOT_TOKEN or GROUP_BOT_TOKEN
    logger.info(f"get_photo: token={token[:10] if token else None}, file_id={file_id[:20]}")
    if not token:
        raise HTTPException(status_code=500, detail="No bot token configured")
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.telegram.org/bot{token}/getFile",
                params={"file_id": file_id}
            )
            data = r.json()
            logger.info(f"getFile response: {data}")
            if not data.get("ok"):
                raise HTTPException(status_code=404, detail=str(data))
            file_path = data["result"]["file_path"]
            img = await client.get(
                f"https://api.telegram.org/file/bot{token}/{file_path}"
            )
            return StreamingResponse(
                iter([img.content]),
                media_type="image/jpeg"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"get_photo error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/lots")
async def get_lots(x_tg_init_data: Optional[str] = Header(None)):
    user = get_current_user(x_tg_init_data)
    user_id = user.get("id", 0)

    async with AsyncSessionLocal() as s:
        result = await s.execute(
            select(Lot).where(
                Lot.status.in_([LotStatus.ACTIVE, LotStatus.SCHEDULED])
            ).order_by(Lot.ends_at.nullslast())
        )
        lots = result.scalars().all()

        output = []
        for lot in lots:
            top_bid_result = await s.execute(
                select(Bid)
                .where(Bid.lot_id == lot.id, Bid.is_cancelled == False)
                .order_by(Bid.amount.desc())
                .limit(1)
            )
            top_bid = top_bid_result.scalar_one_or_none()

            bid_count_result = await s.execute(
                select(Bid).where(
                    Bid.lot_id == lot.id, Bid.is_cancelled == False
                )
            )
            bid_count = len(bid_count_result.scalars().all())

            d = lot_to_dict(lot, user_id, top_bid)
            d["bid_count"] = bid_count
            output.append(d)

    return {"lots": output}


@app.get("/api/lots/mine")
async def get_my_lots(x_tg_init_data: Optional[str] = Header(None)):
    user = get_current_user(x_tg_init_data)
    user_id = user.get("id", 0)

    async with AsyncSessionLocal() as s:
        bids_result = await s.execute(
            select(Bid.lot_id).where(
                Bid.user_id == user_id,
                Bid.is_cancelled == False,
            ).distinct()
        )
        lot_ids = [r[0] for r in bids_result.all()]

        if not lot_ids:
            return {"lots": []}

        result = await s.execute(
            select(Lot).where(Lot.id.in_(lot_ids)).order_by(Lot.id.desc())
        )
        lots = result.scalars().all()

        output = []
        for lot in lots:
            top_bid_result = await s.execute(
                select(Bid)
                .where(Bid.lot_id == lot.id, Bid.is_cancelled == False)
                .order_by(Bid.amount.desc())
                .limit(1)
            )
            top_bid = top_bid_result.scalar_one_or_none()

            bid_count_result = await s.execute(
                select(Bid).where(
                    Bid.lot_id == lot.id, Bid.is_cancelled == False
                )
            )
            bid_count = len(bid_count_result.scalars().all())

            d = lot_to_dict(lot, user_id, top_bid)
            d["bid_count"] = bid_count
            output.append(d)

    return {"lots": output}


@app.get("/api/lots/{lot_id}")
async def get_lot(lot_id: int, x_tg_init_data: Optional[str] = Header(None)):
    user = get_current_user(x_tg_init_data)
    user_id = user.get("id", 0)

    async with AsyncSessionLocal() as s:
        lot = await s.get(Lot, lot_id)
        if not lot:
            raise HTTPException(status_code=404, detail="Lot not found")

        top_bid_result = await s.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id, Bid.is_cancelled == False)
            .order_by(Bid.amount.desc())
            .limit(1)
        )
        top_bid = top_bid_result.scalar_one_or_none()

        bid_count_result = await s.execute(
            select(Bid).where(
                Bid.lot_id == lot_id, Bid.is_cancelled == False
            )
        )
        bid_count = len(bid_count_result.scalars().all())

        d = lot_to_dict(lot, user_id, top_bid)
        d["bid_count"] = bid_count

    return d


@app.post("/api/bids")
async def place_bid(
    req: BidRequest,
    x_tg_init_data: Optional[str] = Header(None),
):
    user = get_current_user(x_tg_init_data)
    user_id  = user.get("id", 0)
    username = user.get("username")

    async with AsyncSessionLocal() as s:
        async with s.begin():
            banned = await s.get(BannedUser, user_id)
            if banned:
                raise HTTPException(status_code=403, detail="Вы заблокированы")

            result = await s.execute(
                select(Lot)
                .where(Lot.id == req.lot_id)
                .with_for_update()
            )
            lot = result.scalar_one_or_none()

            if not lot:
                raise HTTPException(status_code=404, detail="Лот не найден")

            if lot.status != LotStatus.ACTIVE:
                raise HTTPException(status_code=400, detail="Аукцион не активен")

            if lot.ends_at:
                ends = (
                    lot.ends_at if lot.ends_at.tzinfo
                    else lot.ends_at.replace(tzinfo=timezone.utc)
                )
                if ends <= datetime.now(timezone.utc):
                    raise HTTPException(status_code=400, detail="Время аукциона истекло")

            min_bid = lot.current_price + lot.bid_step
            if req.amount < min_bid:
                raise HTTPException(
                    status_code=400,
                    detail=f"Минимальная ставка: {fmt_price(min_bid)}",
                )

            bid = Bid(
                lot_id=req.lot_id,
                user_id=user_id,
                username=username,
                amount=req.amount,
            )
            s.add(bid)

            await s.execute(
                update(Lot)
                .where(Lot.id == req.lot_id)
                .values(current_price=req.amount)
            )

    logger.info(f"Bid placed via Mini App: lot={req.lot_id} user={user_id} amount={req.amount}")

    return {
        "ok": True,
        "lot_id": req.lot_id,
        "amount": req.amount,
        "amount_fmt": fmt_price(req.amount),
    }


@app.on_event("startup")
async def on_startup():
    from database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Mini App API started")


@app.get("/debug")
async def debug():
    from sqlalchemy import text
    async with AsyncSessionLocal() as s:
        result = await s.execute(text("SELECT id, lot_code, status, topic_id FROM lots"))
        rows = result.fetchall()
    return {"db": os.getenv("DATABASE_URL"), "rows": [list(r) for r in rows]}
```


## File: miniapp\backend\requirements.txt
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.36
aiosqlite==0.20.0
asyncpg==0.30.0
python-dotenv==1.0.1
pydantic==2.9.2

```


## File: miniapp\frontend\package-lock.json
```json
{
  "name": "auction-miniapp",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "auction-miniapp",
      "version": "1.0.0",
      "dependencies": {
        "react": "^18.3.1",
        "react-dom": "^18.3.1",
        "react-scripts": "5.0.1"
      }
    },
    "node_modules/@alloc/quick-lru": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/@alloc/quick-lru/-/quick-lru-5.2.0.tgz",
      "integrity": "sha512-UrcABB+4bUrFABwbluTIBErXwvbsU/V7TZWfmbgJfbkwiBuziS9gxdODUyuiecfdGQ85jglMW6juS3+z5TsKLw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@babel/code-frame": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.29.0.tgz",
      "integrity": "sha512-9NhCeYjq9+3uxgdtp20LSiJXJvN0FeCtNGpJxuMFZ1Kv3cWUNb6DOhJwUvcVCzKGR66cw4njwM6hrJLqgOwbcw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.28.5",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/compat-data": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/compat-data/-/compat-data-7.29.0.tgz",
      "integrity": "sha512-T1NCJqT/j9+cn8fvkt7jtwbLBfLC/1y1c7NtCeXFRgzGTsafi68MRv8yzkYSapBnFA6L3U2VSc02ciDzoAJhJg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/core": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/core/-/core-7.29.0.tgz",
      "integrity": "sha512-CGOfOJqWjg2qW/Mb6zNsDm+u5vFQ8DxXfbM09z69p5Z6+mE1ikP2jUXw+j42Pf1XTYED2Rni5f95npYeuwMDQA==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.0",
        "@babel/generator": "^7.29.0",
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-module-transforms": "^7.28.6",
        "@babel/helpers": "^7.28.6",
        "@babel/parser": "^7.29.0",
        "@babel/template": "^7.28.6",
        "@babel/traverse": "^7.29.0",
        "@babel/types": "^7.29.0",
        "@jridgewell/remapping": "^2.3.5",
        "convert-source-map": "^2.0.0",
        "debug": "^4.1.0",
        "gensync": "^1.0.0-beta.2",
        "json5": "^2.2.3",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/babel"
      }
    },
    "node_modules/@babel/core/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/eslint-parser": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/eslint-parser/-/eslint-parser-7.28.6.tgz",
      "integrity": "sha512-QGmsKi2PBO/MHSQk+AAgA9R6OHQr+VqnniFE0eMWZcVcfBZoA2dKn2hUsl3Csg/Plt9opRUWdY7//VXsrIlEiA==",
      "license": "MIT",
      "dependencies": {
        "@nicolo-ribaudo/eslint-scope-5-internals": "5.1.1-v1",
        "eslint-visitor-keys": "^2.1.0",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || >=14.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.11.0",
        "eslint": "^7.5.0 || ^8.0.0 || ^9.0.0"
      }
    },
    "node_modules/@babel/eslint-parser/node_modules/eslint-visitor-keys": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-2.1.0.tgz",
      "integrity": "sha512-0rSmRBzXgDzIsD6mGdJgevzgezI534Cer5L/vyMX0kHzT/jiB43jRhd9YUlMGYLQy2zprNmoT8qasCGtY+QaKw==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/@babel/eslint-parser/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/generator": {
      "version": "7.29.1",
      "resolved": "https://registry.npmjs.org/@babel/generator/-/generator-7.29.1.tgz",
      "integrity": "sha512-qsaF+9Qcm2Qv8SRIMMscAvG4O3lJ0F1GuMo5HR/Bp02LopNgnZBC/EkbevHFeGs4ls/oPz9v+Bsmzbkbe+0dUw==",
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.29.0",
        "@babel/types": "^7.29.0",
        "@jridgewell/gen-mapping": "^0.3.12",
        "@jridgewell/trace-mapping": "^0.3.28",
        "jsesc": "^3.0.2"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-annotate-as-pure": {
      "version": "7.27.3",
      "resolved": "https://registry.npmjs.org/@babel/helper-annotate-as-pure/-/helper-annotate-as-pure-7.27.3.tgz",
      "integrity": "sha512-fXSwMQqitTGeHLBC08Eq5yXz2m37E4pJX1qAU1+2cNedz/ifv/bVXft90VeSav5nFO61EcNgwr0aJxbyPaWBPg==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.27.3"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-compilation-targets": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-compilation-targets/-/helper-compilation-targets-7.28.6.tgz",
      "integrity": "sha512-JYtls3hqi15fcx5GaSNL7SCTJ2MNmjrkHXg4FSpOA/grxK8KwyZ5bubHsCq8FXCkua6xhuaaBit+3b7+VZRfcA==",
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.28.6",
        "@babel/helper-validator-option": "^7.27.1",
        "browserslist": "^4.24.0",
        "lru-cache": "^5.1.1",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-compilation-targets/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/helper-create-class-features-plugin": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-create-class-features-plugin/-/helper-create-class-features-plugin-7.28.6.tgz",
      "integrity": "sha512-dTOdvsjnG3xNT9Y0AUg1wAl38y+4Rl4sf9caSQZOXdNqVn+H+HbbJ4IyyHaIqNR6SW9oJpA/RuRjsjCw2IdIow==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-member-expression-to-functions": "^7.28.5",
        "@babel/helper-optimise-call-expression": "^7.27.1",
        "@babel/helper-replace-supers": "^7.28.6",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1",
        "@babel/traverse": "^7.28.6",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-create-class-features-plugin/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/helper-create-regexp-features-plugin": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-create-regexp-features-plugin/-/helper-create-regexp-features-plugin-7.28.5.tgz",
      "integrity": "sha512-N1EhvLtHzOvj7QQOUCCS3NrPJP8c5W6ZXCHDn7Yialuy1iu4r5EmIYkXlKNqT99Ciw+W0mDqWoR6HWMZlFP3hw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "regexpu-core": "^6.3.1",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-create-regexp-features-plugin/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/helper-define-polyfill-provider": {
      "version": "0.6.7",
      "resolved": "https://registry.npmjs.org/@babel/helper-define-polyfill-provider/-/helper-define-polyfill-provider-0.6.7.tgz",
      "integrity": "sha512-6Fqi8MtQ/PweQ9xvux65emkLQ83uB+qAVtfHkC9UodyHMIZdxNI01HjLCLUtybElp2KY2XNE0nOgyP1E1vXw9w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "debug": "^4.4.3",
        "lodash.debounce": "^4.0.8",
        "resolve": "^1.22.11"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/@babel/helper-globals": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/helper-globals/-/helper-globals-7.28.0.tgz",
      "integrity": "sha512-+W6cISkXFa1jXsDEdYA8HeevQT/FULhxzR99pxphltZcVaugps53THCeiWA8SguxxpSp3gKPiuYfSWopkLQ4hw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-member-expression-to-functions": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-member-expression-to-functions/-/helper-member-expression-to-functions-7.28.5.tgz",
      "integrity": "sha512-cwM7SBRZcPCLgl8a7cY0soT1SptSzAlMH39vwiRpOQkJlh53r5hdHwLSCZpQdVLT39sZt+CRpNwYG4Y2v77atg==",
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.28.5",
        "@babel/types": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-imports": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-imports/-/helper-module-imports-7.28.6.tgz",
      "integrity": "sha512-l5XkZK7r7wa9LucGw9LwZyyCUscb4x37JWTPz7swwFE/0FMQAGpiWUZn8u9DzkSBWEcK25jmvubfpw2dnAMdbw==",
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-transforms": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-transforms/-/helper-module-transforms-7.28.6.tgz",
      "integrity": "sha512-67oXFAYr2cDLDVGLXTEABjdBJZ6drElUSI7WKp70NrpyISso3plG9SAGEF6y7zbha/wOzUByWWTJvEDVNIUGcA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.28.6",
        "@babel/helper-validator-identifier": "^7.28.5",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-optimise-call-expression": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-optimise-call-expression/-/helper-optimise-call-expression-7.27.1.tgz",
      "integrity": "sha512-URMGH08NzYFhubNSGJrpUEphGKQwMQYBySzat5cAByY1/YgIRkULnIy3tAMeszlL/so2HbeilYloUmSpd7GdVw==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-plugin-utils": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-plugin-utils/-/helper-plugin-utils-7.28.6.tgz",
      "integrity": "sha512-S9gzZ/bz83GRysI7gAD4wPT/AI3uCnY+9xn+Mx/KPs2JwHJIz1W8PZkg2cqyt3RNOBM8ejcXhV6y8Og7ly/Dug==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-remap-async-to-generator": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-remap-async-to-generator/-/helper-remap-async-to-generator-7.27.1.tgz",
      "integrity": "sha512-7fiA521aVw8lSPeI4ZOD3vRFkoqkJcS+z4hFo82bFSH/2tNd6eJ5qCVMS5OzDmZh/kaHQeBaeyxK6wljcPtveA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.1",
        "@babel/helper-wrap-function": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-replace-supers": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-replace-supers/-/helper-replace-supers-7.28.6.tgz",
      "integrity": "sha512-mq8e+laIk94/yFec3DxSjCRD2Z0TAjhVbEJY3UQrlwVo15Lmt7C2wAUbK4bjnTs4APkwsYLTahXRraQXhb1WCg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-member-expression-to-functions": "^7.28.5",
        "@babel/helper-optimise-call-expression": "^7.27.1",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-skip-transparent-expression-wrappers": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-skip-transparent-expression-wrappers/-/helper-skip-transparent-expression-wrappers-7.27.1.tgz",
      "integrity": "sha512-Tub4ZKEXqbPjXgWLl2+3JpQAYBJ8+ikpQ2Ocj/q/r0LwE3UhENh7EUabyHjz2kCEsrRY83ew2DQdHluuiDQFzg==",
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.27.1",
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-string-parser": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-string-parser/-/helper-string-parser-7.27.1.tgz",
      "integrity": "sha512-qMlSxKbpRlAridDExk92nSobyDdpPijUq2DW6oDnUqd0iOGxmQjyqhMIihI9+zv4LPyZdRje2cavWPbCbWm3eA==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.28.5.tgz",
      "integrity": "sha512-qSs4ifwzKJSV39ucNjsvc6WVHs6b7S03sOh2OcHF9UHfVPqWWALUsNUVzhSBiItjRZoLHx7nIarVjqKVusUZ1Q==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-option": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-option/-/helper-validator-option-7.27.1.tgz",
      "integrity": "sha512-YvjJow9FxbhFFKDSuFnVCe2WxXk1zWc22fFePVNEaWJEu8IrZVlda6N0uHwzZrUM1il7NC9Mlp4MaJYbYd9JSg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-wrap-function": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-wrap-function/-/helper-wrap-function-7.28.6.tgz",
      "integrity": "sha512-z+PwLziMNBeSQJonizz2AGnndLsP2DeGHIxDAn+wdHOGuo4Fo1x1HBPPXeE9TAOPHNNWQKCSlA2VZyYyyibDnQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.28.6",
        "@babel/traverse": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helpers": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helpers/-/helpers-7.28.6.tgz",
      "integrity": "sha512-xOBvwq86HHdB7WUDTfKfT/Vuxh7gElQ+Sfti2Cy6yIWNW05P8iUslOVcZ4/sKbE+/jQaukQAdz/gf3724kYdqw==",
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/parser": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/parser/-/parser-7.29.0.tgz",
      "integrity": "sha512-IyDgFV5GeDUVX4YdF/3CPULtVGSXXMLh1xVIgdCgxApktqnQV0r7/8Nqthg+8YLGaAtdyIlo2qIdZrbCv4+7ww==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.29.0"
      },
      "bin": {
        "parser": "bin/babel-parser.js"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-firefox-class-in-computed-class-key": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-firefox-class-in-computed-class-key/-/plugin-bugfix-firefox-class-in-computed-class-key-7.28.5.tgz",
      "integrity": "sha512-87GDMS3tsmMSi/3bWOte1UblL+YUTFMV8SZPZ2eSEL17s74Cw/l63rR6NmGVKMYW2GYi85nE+/d6Hw5N0bEk2Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-safari-class-field-initializer-scope": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-safari-class-field-initializer-scope/-/plugin-bugfix-safari-class-field-initializer-scope-7.27.1.tgz",
      "integrity": "sha512-qNeq3bCKnGgLkEXUuFry6dPlGfCdQNZbn7yUAPCInwAJHMU7THJfrBSozkcWq5sNM6RcF3S8XyQL2A52KNR9IA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression/-/plugin-bugfix-safari-id-destructuring-collision-in-function-expression-7.27.1.tgz",
      "integrity": "sha512-g4L7OYun04N1WyqMNjldFwlfPCLVkgB54A/YCXICZYBsvJJE3kByKv9c9+R/nAfmIfjl2rKYLNyMHboYbZaWaA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining/-/plugin-bugfix-v8-spread-parameters-in-optional-chaining-7.27.1.tgz",
      "integrity": "sha512-oO02gcONcD5O1iTLi/6frMJBIwWEHceWGSGqrpCmEL8nogiS6J9PBlE48CaK20/Jx1LuRml9aDftLgdjXT8+Cw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1",
        "@babel/plugin-transform-optional-chaining": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.13.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly/-/plugin-bugfix-v8-static-class-fields-redefine-readonly-7.28.6.tgz",
      "integrity": "sha512-a0aBScVTlNaiUe35UtfxAN7A/tehvvG4/ByO6+46VPKTRSlfnAFsgKy0FUh+qAkQrDTmhDkT+IBOKlOoMUxQ0g==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-proposal-class-properties": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-class-properties/-/plugin-proposal-class-properties-7.18.6.tgz",
      "integrity": "sha512-cumfXOF0+nzZrrN8Rf0t7M+tF6sZc7vhQwYQck9q1/5w2OExlD+b4v4RpMJFaV1Z7WcDRgO6FqvxqxGlwo+RHQ==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-class-properties instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.18.6",
        "@babel/helper-plugin-utils": "^7.18.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-decorators": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-decorators/-/plugin-proposal-decorators-7.29.0.tgz",
      "integrity": "sha512-CVBVv3VY/XRMxRYq5dwr2DS7/MvqPm23cOCjbwNnVrfOqcWlnefua1uUs0sjdKOGjvPUG633o07uWzJq4oI6dA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/plugin-syntax-decorators": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-nullish-coalescing-operator": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-nullish-coalescing-operator/-/plugin-proposal-nullish-coalescing-operator-7.18.6.tgz",
      "integrity": "sha512-wQxQzxYeJqHcfppzBDnm1yAY0jSRkUXR2z8RePZYrKwMKgMlE8+Z6LUno+bd6LvbGh8Gltvy74+9pIYkr+XkKA==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-nullish-coalescing-operator instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.18.6",
        "@babel/plugin-syntax-nullish-coalescing-operator": "^7.8.3"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-numeric-separator": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-numeric-separator/-/plugin-proposal-numeric-separator-7.18.6.tgz",
      "integrity": "sha512-ozlZFogPqoLm8WBr5Z8UckIoE4YQ5KESVcNudyXOR8uqIkliTEgJ3RoketfG6pmzLdeZF0H/wjE9/cCEitBl7Q==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-numeric-separator instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.18.6",
        "@babel/plugin-syntax-numeric-separator": "^7.10.4"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-optional-chaining": {
      "version": "7.21.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-optional-chaining/-/plugin-proposal-optional-chaining-7.21.0.tgz",
      "integrity": "sha512-p4zeefM72gpmEe2fkUr/OnOXpWEf8nAgk7ZYVqqfFiyIG7oFfVZcCrU64hWn5xp4tQ9LkV4bTIa5rD0KANpKNA==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-optional-chaining instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.20.2",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.20.0",
        "@babel/plugin-syntax-optional-chaining": "^7.8.3"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-private-methods": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-private-methods/-/plugin-proposal-private-methods-7.18.6.tgz",
      "integrity": "sha512-nutsvktDItsNn4rpGItSNV2sz1XwS+nfU0Rg8aCx3W3NOKVzdMjJRu0O5OkgDp3ZGICSTbgRpxZoWsxoKRvbeA==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-methods instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.18.6",
        "@babel/helper-plugin-utils": "^7.18.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-private-property-in-object": {
      "version": "7.21.0-placeholder-for-preset-env.2",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-private-property-in-object/-/plugin-proposal-private-property-in-object-7.21.0-placeholder-for-preset-env.2.tgz",
      "integrity": "sha512-SOSkfJDddaM7mak6cPEpswyTRnuRltl429hMraQEglW+OkovnCzsiszTmsrlY//qLFjCpQDFRvjdm2wA5pPm9w==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-async-generators": {
      "version": "7.8.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-async-generators/-/plugin-syntax-async-generators-7.8.4.tgz",
      "integrity": "sha512-tycmZxkGfZaxhMRbXlPXuVFpdWlXpir2W4AMhSJgRKzk/eDlIXOhb2LHWoLpDF7TEHylV5zNhykX6KAgHJmTNw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-bigint": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-bigint/-/plugin-syntax-bigint-7.8.3.tgz",
      "integrity": "sha512-wnTnFlG+YxQm3vDxpGE57Pj0srRU4sHE/mDkt1qv2YJJSeUAec2ma4WLUnUPeKjyrfntVwe/N6dCXpU+zL3Npg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-class-properties": {
      "version": "7.12.13",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-class-properties/-/plugin-syntax-class-properties-7.12.13.tgz",
      "integrity": "sha512-fm4idjKla0YahUNgFNLCB0qySdsoPiZP3iQE3rky0mBUtMZ23yDJ9SJdg6dXTSDnulOVqiF3Hgr9nbXvXTQZYA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.12.13"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-class-static-block": {
      "version": "7.14.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-class-static-block/-/plugin-syntax-class-static-block-7.14.5.tgz",
      "integrity": "sha512-b+YyPmr6ldyNnM6sqYeMWE+bgJcJpO6yS4QD7ymxgH34GBPNDM/THBh8iunyvKIZztiwLH4CJZ0RxTk9emgpjw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.14.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-decorators": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-decorators/-/plugin-syntax-decorators-7.28.6.tgz",
      "integrity": "sha512-71EYI0ONURHJBL4rSFXnITXqXrrY8q4P0q006DPfN+Rk+ASM+++IBXem/ruokgBZR8YNEWZ8R6B+rCb8VcUTqA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-flow": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-flow/-/plugin-syntax-flow-7.28.6.tgz",
      "integrity": "sha512-D+OrJumc9McXNEBI/JmFnc/0uCM2/Y3PEBG3gfV3QIYkKv5pvnpzFrl1kYCrcHJP8nOeFB/SHi1IHz29pNGuew==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-import-assertions": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-import-assertions/-/plugin-syntax-import-assertions-7.28.6.tgz",
      "integrity": "sha512-pSJUpFHdx9z5nqTSirOCMtYVP2wFgoWhP0p3g8ONK/4IHhLIBd0B9NYqAvIUAhq+OkhO4VM1tENCt0cjlsNShw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-import-attributes": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-import-attributes/-/plugin-syntax-import-attributes-7.28.6.tgz",
      "integrity": "sha512-jiLC0ma9XkQT3TKJ9uYvlakm66Pamywo+qwL+oL8HJOvc6TWdZXVfhqJr8CCzbSGUAbDOzlGHJC1U+vRfLQDvw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-import-meta": {
      "version": "7.10.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-import-meta/-/plugin-syntax-import-meta-7.10.4.tgz",
      "integrity": "sha512-Yqfm+XDx0+Prh3VSeEQCPU81yC+JWZ2pDPFSS4ZdpfZhp4MkFMaDC1UqseovEKwSUpnIL7+vK+Clp7bfh0iD7g==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.10.4"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-json-strings": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-json-strings/-/plugin-syntax-json-strings-7.8.3.tgz",
      "integrity": "sha512-lY6kdGpWHvjoe2vk4WrAapEuBR69EMxZl+RoGRhrFGNYVK8mOPAW8VfbT/ZgrFbXlDNiiaxQnAtgVCZ6jv30EA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-jsx": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-jsx/-/plugin-syntax-jsx-7.28.6.tgz",
      "integrity": "sha512-wgEmr06G6sIpqr8YDwA2dSRTE3bJ+V0IfpzfSY3Lfgd7YWOaAdlykvJi13ZKBt8cZHfgH1IXN+CL656W3uUa4w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-logical-assignment-operators": {
      "version": "7.10.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-logical-assignment-operators/-/plugin-syntax-logical-assignment-operators-7.10.4.tgz",
      "integrity": "sha512-d8waShlpFDinQ5MtvGU9xDAOzKH47+FFoney2baFIoMr952hKOLp1HR7VszoZvOsV/4+RRszNY7D17ba0te0ig==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.10.4"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-nullish-coalescing-operator": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-nullish-coalescing-operator/-/plugin-syntax-nullish-coalescing-operator-7.8.3.tgz",
      "integrity": "sha512-aSff4zPII1u2QD7y+F8oDsz19ew4IGEJg9SVW+bqwpwtfFleiQDMdzA/R+UlWDzfnHFCxxleFT0PMIrR36XLNQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-numeric-separator": {
      "version": "7.10.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-numeric-separator/-/plugin-syntax-numeric-separator-7.10.4.tgz",
      "integrity": "sha512-9H6YdfkcK/uOnY/K7/aA2xpzaAgkQn37yzWUMRK7OaPOqOpGS1+n0H5hxT9AUw9EsSjPW8SVyMJwYRtWs3X3ug==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.10.4"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-object-rest-spread": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-object-rest-spread/-/plugin-syntax-object-rest-spread-7.8.3.tgz",
      "integrity": "sha512-XoqMijGZb9y3y2XskN+P1wUGiVwWZ5JmoDRwx5+3GmEplNyVM2s2Dg8ILFQm8rWM48orGy5YpI5Bl8U1y7ydlA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-optional-catch-binding": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-optional-catch-binding/-/plugin-syntax-optional-catch-binding-7.8.3.tgz",
      "integrity": "sha512-6VPD0Pc1lpTqw0aKoeRTMiB+kWhAoT24PA+ksWSBrFtl5SIRVpZlwN3NNPQjehA2E/91FV3RjLWoVTglWcSV3Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-optional-chaining": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-optional-chaining/-/plugin-syntax-optional-chaining-7.8.3.tgz",
      "integrity": "sha512-KoK9ErH1MBlCPxV0VANkXW2/dw4vlbGDrFgz8bmUsBGYkFRcbRwMh6cIJubdPrkxRwuGdtCk0v/wPTKbQgBjkg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-private-property-in-object": {
      "version": "7.14.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-private-property-in-object/-/plugin-syntax-private-property-in-object-7.14.5.tgz",
      "integrity": "sha512-0wVnp9dxJ72ZUJDV27ZfbSj6iHLoytYZmh3rFcxNnvsJF3ktkzLDZPy/mA17HGsaQT3/DQsWYX1f1QGWkCoVUg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.14.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-top-level-await": {
      "version": "7.14.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-top-level-await/-/plugin-syntax-top-level-await-7.14.5.tgz",
      "integrity": "sha512-hx++upLv5U1rgYfwe1xBQUhRmU41NEvpUvrp8jkrSCdvGSnM5/qdRMtylJ6PG5OFkBaHkbTAKTnd3/YyESRHFw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.14.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-typescript": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-typescript/-/plugin-syntax-typescript-7.28.6.tgz",
      "integrity": "sha512-+nDNmQye7nlnuuHDboPbGm00Vqg3oO8niRRL27/4LYHUsHYh0zJ1xWOz0uRwNFmM1Avzk8wZbc6rdiYhomzv/A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-unicode-sets-regex": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-unicode-sets-regex/-/plugin-syntax-unicode-sets-regex-7.18.6.tgz",
      "integrity": "sha512-727YkEAPwSIQTv5im8QHz3upqp92JTWhidIC81Tdx4VJYIte/VndKf1qKrfnnhPLiPghStWfvC/iFaMCQu7Nqg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.18.6",
        "@babel/helper-plugin-utils": "^7.18.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-arrow-functions": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-arrow-functions/-/plugin-transform-arrow-functions-7.27.1.tgz",
      "integrity": "sha512-8Z4TGic6xW70FKThA5HYEKKyBpOOsucTOD1DjU3fZxDg+K3zBJcXMFnt/4yQiZnf5+MiOMSXQ9PaEK/Ilh1DeA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-async-generator-functions": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-async-generator-functions/-/plugin-transform-async-generator-functions-7.29.0.tgz",
      "integrity": "sha512-va0VdWro4zlBr2JsXC+ofCPB2iG12wPtVGTWFx2WLDOM3nYQZZIGP82qku2eW/JR83sD+k2k+CsNtyEbUqhU6w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-remap-async-to-generator": "^7.27.1",
        "@babel/traverse": "^7.29.0"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-async-to-generator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-async-to-generator/-/plugin-transform-async-to-generator-7.28.6.tgz",
      "integrity": "sha512-ilTRcmbuXjsMmcZ3HASTe4caH5Tpo93PkTxF9oG2VZsSWsahydmcEHhix9Ik122RcTnZnUzPbmux4wh1swfv7g==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-remap-async-to-generator": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-block-scoped-functions": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-block-scoped-functions/-/plugin-transform-block-scoped-functions-7.27.1.tgz",
      "integrity": "sha512-cnqkuOtZLapWYZUYM5rVIdv1nXYuFVIltZ6ZJ7nIj585QsjKM5dhL2Fu/lICXZ1OyIAFc7Qy+bvDAtTXqGrlhg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-block-scoping": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-block-scoping/-/plugin-transform-block-scoping-7.28.6.tgz",
      "integrity": "sha512-tt/7wOtBmwHPNMPu7ax4pdPz6shjFrmHDghvNC+FG9Qvj7D6mJcoRQIF5dy4njmxR941l6rgtvfSB2zX3VlUIw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-class-properties": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-class-properties/-/plugin-transform-class-properties-7.28.6.tgz",
      "integrity": "sha512-dY2wS3I2G7D697VHndN91TJr8/AAfXQNt5ynCTI/MpxMsSzHp+52uNivYT5wCPax3whc47DR8Ba7cmlQMg24bw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-class-static-block": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-class-static-block/-/plugin-transform-class-static-block-7.28.6.tgz",
      "integrity": "sha512-rfQ++ghVwTWTqQ7w8qyDxL1XGihjBss4CmTgGRCTAC9RIbhVpyp4fOeZtta0Lbf+dTNIVJer6ych2ibHwkZqsQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.12.0"
      }
    },
    "node_modules/@babel/plugin-transform-classes": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-classes/-/plugin-transform-classes-7.28.6.tgz",
      "integrity": "sha512-EF5KONAqC5zAqT783iMGuM2ZtmEBy+mJMOKl2BCvPZ2lVrwvXnB6o+OBWCS+CoeCCpVRF2sA2RBKUxvT8tQT5Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-globals": "^7.28.0",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-replace-supers": "^7.28.6",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-computed-properties": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-computed-properties/-/plugin-transform-computed-properties-7.28.6.tgz",
      "integrity": "sha512-bcc3k0ijhHbc2lEfpFHgx7eYw9KNXqOerKWfzbxEHUGKnS3sz9C4CNL9OiFN1297bDNfUiSO7DaLzbvHQQQ1BQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/template": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-destructuring": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-destructuring/-/plugin-transform-destructuring-7.28.5.tgz",
      "integrity": "sha512-Kl9Bc6D0zTUcFUvkNuQh4eGXPKKNDOJQXVyyM4ZAQPMveniJdxi8XMJwLo+xSoW3MIq81bD33lcUe9kZpl0MCw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-dotall-regex": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-dotall-regex/-/plugin-transform-dotall-regex-7.28.6.tgz",
      "integrity": "sha512-SljjowuNKB7q5Oayv4FoPzeB74g3QgLt8IVJw9ADvWy3QnUb/01aw8I4AVv8wYnPvQz2GDDZ/g3GhcNyDBI4Bg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-duplicate-keys": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-duplicate-keys/-/plugin-transform-duplicate-keys-7.27.1.tgz",
      "integrity": "sha512-MTyJk98sHvSs+cvZ4nOauwTTG1JeonDjSGvGGUNHreGQns+Mpt6WX/dVzWBHgg+dYZhkC4X+zTDfkTU+Vy9y7Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-duplicate-named-capturing-groups-regex": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-duplicate-named-capturing-groups-regex/-/plugin-transform-duplicate-named-capturing-groups-regex-7.29.0.tgz",
      "integrity": "sha512-zBPcW2lFGxdiD8PUnPwJjag2J9otbcLQzvbiOzDxpYXyCuYX9agOwMPGn1prVH0a4qzhCKu24rlH4c1f7yA8rw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-dynamic-import": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-dynamic-import/-/plugin-transform-dynamic-import-7.27.1.tgz",
      "integrity": "sha512-MHzkWQcEmjzzVW9j2q8LGjwGWpG2mjwaaB0BNQwst3FIjqsg8Ct/mIZlvSPJvfi9y2AC8mi/ktxbFVL9pZ1I4A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-explicit-resource-management": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-explicit-resource-management/-/plugin-transform-explicit-resource-management-7.28.6.tgz",
      "integrity": "sha512-Iao5Konzx2b6g7EPqTy40UZbcdXE126tTxVFr/nAIj+WItNxjKSYTEw3RC+A2/ZetmdJsgueL1KhaMCQHkLPIg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/plugin-transform-destructuring": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-exponentiation-operator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-exponentiation-operator/-/plugin-transform-exponentiation-operator-7.28.6.tgz",
      "integrity": "sha512-WitabqiGjV/vJ0aPOLSFfNY1u9U3R7W36B03r5I2KoNix+a3sOhJ3pKFB3R5It9/UiK78NiO0KE9P21cMhlPkw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-export-namespace-from": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-export-namespace-from/-/plugin-transform-export-namespace-from-7.27.1.tgz",
      "integrity": "sha512-tQvHWSZ3/jH2xuq/vZDy0jNn+ZdXJeM8gHvX4lnJmsc3+50yPlWdZXIc5ay+umX+2/tJIqHqiEqcJvxlmIvRvQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-flow-strip-types": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-flow-strip-types/-/plugin-transform-flow-strip-types-7.27.1.tgz",
      "integrity": "sha512-G5eDKsu50udECw7DL2AcsysXiQyB7Nfg521t2OAJ4tbfTJ27doHLeF/vlI1NZGlLdbb/v+ibvtL1YBQqYOwJGg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/plugin-syntax-flow": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-for-of": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-for-of/-/plugin-transform-for-of-7.27.1.tgz",
      "integrity": "sha512-BfbWFFEJFQzLCQ5N8VocnCtA8J1CLkNTe2Ms2wocj75dd6VpiqS5Z5quTYcUoo4Yq+DN0rtikODccuv7RU81sw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-function-name": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-function-name/-/plugin-transform-function-name-7.27.1.tgz",
      "integrity": "sha512-1bQeydJF9Nr1eBCMMbC+hdwmRlsv5XYOMu03YSWFwNs0HsAmtSxxF1fyuYPqemVldVyFmlCU7w8UE14LupUSZQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-json-strings": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-json-strings/-/plugin-transform-json-strings-7.28.6.tgz",
      "integrity": "sha512-Nr+hEN+0geQkzhbdgQVPoqr47lZbm+5fCUmO70722xJZd0Mvb59+33QLImGj6F+DkK3xgDi1YVysP8whD6FQAw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-literals/-/plugin-transform-literals-7.27.1.tgz",
      "integrity": "sha512-0HCFSepIpLTkLcsi86GG3mTUzxV5jpmbv97hTETW3yzrAij8aqlD36toB1D0daVFJM8NK6GvKO0gslVQmm+zZA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-logical-assignment-operators": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-logical-assignment-operators/-/plugin-transform-logical-assignment-operators-7.28.6.tgz",
      "integrity": "sha512-+anKKair6gpi8VsM/95kmomGNMD0eLz1NQ8+Pfw5sAwWH9fGYXT50E55ZpV0pHUHWf6IUTWPM+f/7AAff+wr9A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-member-expression-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-member-expression-literals/-/plugin-transform-member-expression-literals-7.27.1.tgz",
      "integrity": "sha512-hqoBX4dcZ1I33jCSWcXrP+1Ku7kdqXf1oeah7ooKOIiAdKQ+uqftgCFNOSzA5AMS2XIHEYeGFg4cKRCdpxzVOQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-amd": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-amd/-/plugin-transform-modules-amd-7.27.1.tgz",
      "integrity": "sha512-iCsytMg/N9/oFq6n+gFTvUYDZQOMK5kEdeYxmxt91fcJGycfxVP9CnrxoliM0oumFERba2i8ZtwRUCMhvP1LnA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-commonjs": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-commonjs/-/plugin-transform-modules-commonjs-7.28.6.tgz",
      "integrity": "sha512-jppVbf8IV9iWWwWTQIxJMAJCWBuuKx71475wHwYytrRGQ2CWiDvYlADQno3tcYpS/T2UUWFQp3nVtYfK/YBQrA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-systemjs": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-systemjs/-/plugin-transform-modules-systemjs-7.29.0.tgz",
      "integrity": "sha512-PrujnVFbOdUpw4UHiVwKvKRLMMic8+eC0CuNlxjsyZUiBjhFdPsewdXCkveh2KqBA9/waD0W1b4hXSOBQJezpQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-validator-identifier": "^7.28.5",
        "@babel/traverse": "^7.29.0"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-umd": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-umd/-/plugin-transform-modules-umd-7.27.1.tgz",
      "integrity": "sha512-iQBE/xC5BV1OxJbp6WG7jq9IWiD+xxlZhLrdwpPkTX3ydmXdvoCpyfJN7acaIBZaOqTfr76pgzqBJflNbeRK+w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-named-capturing-groups-regex": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-named-capturing-groups-regex/-/plugin-transform-named-capturing-groups-regex-7.29.0.tgz",
      "integrity": "sha512-1CZQA5KNAD6ZYQLPw7oi5ewtDNxH/2vuCh+6SmvgDfhumForvs8a1o9n0UrEoBD8HU4djO2yWngTQlXl1NDVEQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-new-target": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-new-target/-/plugin-transform-new-target-7.27.1.tgz",
      "integrity": "sha512-f6PiYeqXQ05lYq3TIfIDu/MtliKUbNwkGApPUvyo6+tc7uaR4cPjPe7DFPr15Uyycg2lZU6btZ575CuQoYh7MQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-nullish-coalescing-operator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-nullish-coalescing-operator/-/plugin-transform-nullish-coalescing-operator-7.28.6.tgz",
      "integrity": "sha512-3wKbRgmzYbw24mDJXT7N+ADXw8BC/imU9yo9c9X9NKaLF1fW+e5H1U5QjMUBe4Qo4Ox/o++IyUkl1sVCLgevKg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-numeric-separator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-numeric-separator/-/plugin-transform-numeric-separator-7.28.6.tgz",
      "integrity": "sha512-SJR8hPynj8outz+SlStQSwvziMN4+Bq99it4tMIf5/Caq+3iOc0JtKyse8puvyXkk3eFRIA5ID/XfunGgO5i6w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-object-rest-spread": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-object-rest-spread/-/plugin-transform-object-rest-spread-7.28.6.tgz",
      "integrity": "sha512-5rh+JR4JBC4pGkXLAcYdLHZjXudVxWMXbB6u6+E9lRL5TrGVbHt1TjxGbZ8CkmYw9zjkB7jutzOROArsqtncEA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/plugin-transform-destructuring": "^7.28.5",
        "@babel/plugin-transform-parameters": "^7.27.7",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-object-super": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-object-super/-/plugin-transform-object-super-7.27.1.tgz",
      "integrity": "sha512-SFy8S9plRPbIcxlJ8A6mT/CxFdJx/c04JEctz4jf8YZaVS2px34j7NXRrlGlHkN/M2gnpL37ZpGRGVFLd3l8Ng==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-replace-supers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-optional-catch-binding": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-optional-catch-binding/-/plugin-transform-optional-catch-binding-7.28.6.tgz",
      "integrity": "sha512-R8ja/Pyrv0OGAvAXQhSTmWyPJPml+0TMqXlO5w+AsMEiwb2fg3WkOvob7UxFSL3OIttFSGSRFKQsOhJ/X6HQdQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-optional-chaining": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-optional-chaining/-/plugin-transform-optional-chaining-7.28.6.tgz",
      "integrity": "sha512-A4zobikRGJTsX9uqVFdafzGkqD30t26ck2LmOzAuLL8b2x6k3TIqRiT2xVvA9fNmFeTX484VpsdgmKNA0bS23w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-parameters": {
      "version": "7.27.7",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-parameters/-/plugin-transform-parameters-7.27.7.tgz",
      "integrity": "sha512-qBkYTYCb76RRxUM6CcZA5KRu8K4SM8ajzVeUgVdMVO9NN9uI/GaVmBg/WKJJGnNokV9SY8FxNOVWGXzqzUidBg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-private-methods": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-private-methods/-/plugin-transform-private-methods-7.28.6.tgz",
      "integrity": "sha512-piiuapX9CRv7+0st8lmuUlRSmX6mBcVeNQ1b4AYzJxfCMuBfB0vBXDiGSmm03pKJw1v6cZ8KSeM+oUnM6yAExg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-private-property-in-object": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-private-property-in-object/-/plugin-transform-private-property-in-object-7.28.6.tgz",
      "integrity": "sha512-b97jvNSOb5+ehyQmBpmhOCiUC5oVK4PMnpRvO7+ymFBoqYjeDHIU9jnrNUuwHOiL9RpGDoKBpSViarV+BU+eVA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-property-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-property-literals/-/plugin-transform-property-literals-7.27.1.tgz",
      "integrity": "sha512-oThy3BCuCha8kDZ8ZkgOg2exvPYUlprMukKQXI1r1pJ47NCvxfkEy8vK+r/hT9nF0Aa4H1WUPZZjHTFtAhGfmQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-constant-elements": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-constant-elements/-/plugin-transform-react-constant-elements-7.27.1.tgz",
      "integrity": "sha512-edoidOjl/ZxvYo4lSBOQGDSyToYVkTAwyVoa2tkuYTSmjrB1+uAedoL5iROVLXkxH+vRgA7uP4tMg2pUJpZ3Ug==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-display-name": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-display-name/-/plugin-transform-react-display-name-7.28.0.tgz",
      "integrity": "sha512-D6Eujc2zMxKjfa4Zxl4GHMsmhKKZ9VpcqIchJLvwTxad9zWIYulwYItBovpDOoNLISpcZSXoDJ5gaGbQUDqViA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-jsx": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-jsx/-/plugin-transform-react-jsx-7.28.6.tgz",
      "integrity": "sha512-61bxqhiRfAACulXSLd/GxqmAedUSrRZIu/cbaT18T1CetkTmtDN15it7i80ru4DVqRK1WMxQhXs+Lf9kajm5Ow==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-module-imports": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/plugin-syntax-jsx": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-jsx-development": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-jsx-development/-/plugin-transform-react-jsx-development-7.27.1.tgz",
      "integrity": "sha512-ykDdF5yI4f1WrAolLqeF3hmYU12j9ntLQl/AOG1HAS21jxyg1Q0/J/tpREuYLfatGdGmXp/3yS0ZA76kOlVq9Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/plugin-transform-react-jsx": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-pure-annotations": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-pure-annotations/-/plugin-transform-react-pure-annotations-7.27.1.tgz",
      "integrity": "sha512-JfuinvDOsD9FVMTHpzA/pBLisxpv1aSf+OIV8lgH3MuWrks19R27e6a6DipIg4aX1Zm9Wpb04p8wljfKrVSnPA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-regenerator": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-regenerator/-/plugin-transform-regenerator-7.29.0.tgz",
      "integrity": "sha512-FijqlqMA7DmRdg/aINBSs04y8XNTYw/lr1gJ2WsmBnnaNw1iS43EPkJW+zK7z65auG3AWRFXWj+NcTQwYptUog==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-regexp-modifiers": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-regexp-modifiers/-/plugin-transform-regexp-modifiers-7.28.6.tgz",
      "integrity": "sha512-QGWAepm9qxpaIs7UM9FvUSnCGlb8Ua1RhyM4/veAxLwt3gMat/LSGrZixyuj4I6+Kn9iwvqCyPTtbdxanYoWYg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-reserved-words": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-reserved-words/-/plugin-transform-reserved-words-7.27.1.tgz",
      "integrity": "sha512-V2ABPHIJX4kC7HegLkYoDpfg9PVmuWy/i6vUM5eGK22bx4YVFD3M5F0QQnWQoDs6AGsUWTVOopBiMFQgHaSkVw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-runtime": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-runtime/-/plugin-transform-runtime-7.29.0.tgz",
      "integrity": "sha512-jlaRT5dJtMaMCV6fAuLbsQMSwz/QkvaHOHOSXRitGGwSpR1blCY4KUKoyP2tYO8vJcqYe8cEj96cqSztv3uF9w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "babel-plugin-polyfill-corejs2": "^0.4.14",
        "babel-plugin-polyfill-corejs3": "^0.13.0",
        "babel-plugin-polyfill-regenerator": "^0.6.5",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-runtime/node_modules/babel-plugin-polyfill-corejs3": {
      "version": "0.13.0",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-corejs3/-/babel-plugin-polyfill-corejs3-0.13.0.tgz",
      "integrity": "sha512-U+GNwMdSFgzVmfhNm8GJUX88AadB3uo9KpJqS3FaqNIPKgySuvMb+bHPsOmmuWyIcuqZj/pzt1RUIUZns4y2+A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-define-polyfill-provider": "^0.6.5",
        "core-js-compat": "^3.43.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-runtime/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/plugin-transform-shorthand-properties": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-shorthand-properties/-/plugin-transform-shorthand-properties-7.27.1.tgz",
      "integrity": "sha512-N/wH1vcn4oYawbJ13Y/FxcQrWk63jhfNa7jef0ih7PHSIHX2LB7GWE1rkPrOnka9kwMxb6hMl19p7lidA+EHmQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-spread": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-spread/-/plugin-transform-spread-7.28.6.tgz",
      "integrity": "sha512-9U4QObUC0FtJl05AsUcodau/RWDytrU6uKgkxu09mLR9HLDAtUMoPuuskm5huQsoktmsYpI+bGmq+iapDcriKA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-sticky-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-sticky-regex/-/plugin-transform-sticky-regex-7.27.1.tgz",
      "integrity": "sha512-lhInBO5bi/Kowe2/aLdBAawijx+q1pQzicSgnkB6dUPc1+RC8QmJHKf2OjvU+NZWitguJHEaEmbV6VWEouT58g==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-template-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-template-literals/-/plugin-transform-template-literals-7.27.1.tgz",
      "integrity": "sha512-fBJKiV7F2DxZUkg5EtHKXQdbsbURW3DZKQUWphDum0uRP6eHGGa/He9mc0mypL680pb+e/lDIthRohlv8NCHkg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-typeof-symbol": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-typeof-symbol/-/plugin-transform-typeof-symbol-7.27.1.tgz",
      "integrity": "sha512-RiSILC+nRJM7FY5srIyc4/fGIwUhyDuuBSdWn4y6yT6gm652DpCHZjIipgn6B7MQ1ITOUnAKWixEUjQRIBIcLw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-typescript": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-typescript/-/plugin-transform-typescript-7.28.6.tgz",
      "integrity": "sha512-0YWL2RFxOqEm9Efk5PvreamxPME8OyY0wM5wh5lHjF+VtVhdneCWGzZeSqzOfiobVqQaNCd2z0tQvnI9DaPWPw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1",
        "@babel/plugin-syntax-typescript": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-escapes": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-escapes/-/plugin-transform-unicode-escapes-7.27.1.tgz",
      "integrity": "sha512-Ysg4v6AmF26k9vpfFuTZg8HRfVWzsh1kVfowA23y9j/Gu6dOuahdUVhkLqpObp3JIv27MLSii6noRnuKN8H0Mg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-property-regex": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-property-regex/-/plugin-transform-unicode-property-regex-7.28.6.tgz",
      "integrity": "sha512-4Wlbdl/sIZjzi/8St0evF0gEZrgOswVO6aOzqxh1kDZOl9WmLrHq2HtGhnOJZmHZYKP8WZ1MDLCt5DAWwRo57A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-regex/-/plugin-transform-unicode-regex-7.27.1.tgz",
      "integrity": "sha512-xvINq24TRojDuyt6JGtHmkVkrfVV3FPT16uytxImLeBZqW3/H52yN+kM1MGuyPkIQxrzKwPHs5U/MP3qKyzkGw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-sets-regex": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-sets-regex/-/plugin-transform-unicode-sets-regex-7.28.6.tgz",
      "integrity": "sha512-/wHc/paTUmsDYN7SZkpWxogTOBNnlx7nBQYfy6JJlCT7G3mVhltk3e++N7zV0XfgGsrqBxd4rJQt9H16I21Y1Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/preset-env": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/preset-env/-/preset-env-7.29.0.tgz",
      "integrity": "sha512-fNEdfc0yi16lt6IZo2Qxk3knHVdfMYX33czNb4v8yWhemoBhibCpQK/uYHtSKIiO+p/zd3+8fYVXhQdOVV608w==",
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.29.0",
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-validator-option": "^7.27.1",
        "@babel/plugin-bugfix-firefox-class-in-computed-class-key": "^7.28.5",
        "@babel/plugin-bugfix-safari-class-field-initializer-scope": "^7.27.1",
        "@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression": "^7.27.1",
        "@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining": "^7.27.1",
        "@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly": "^7.28.6",
        "@babel/plugin-proposal-private-property-in-object": "7.21.0-placeholder-for-preset-env.2",
        "@babel/plugin-syntax-import-assertions": "^7.28.6",
        "@babel/plugin-syntax-import-attributes": "^7.28.6",
        "@babel/plugin-syntax-unicode-sets-regex": "^7.18.6",
        "@babel/plugin-transform-arrow-functions": "^7.27.1",
        "@babel/plugin-transform-async-generator-functions": "^7.29.0",
        "@babel/plugin-transform-async-to-generator": "^7.28.6",
        "@babel/plugin-transform-block-scoped-functions": "^7.27.1",
        "@babel/plugin-transform-block-scoping": "^7.28.6",
        "@babel/plugin-transform-class-properties": "^7.28.6",
        "@babel/plugin-transform-class-static-block": "^7.28.6",
        "@babel/plugin-transform-classes": "^7.28.6",
        "@babel/plugin-transform-computed-properties": "^7.28.6",
        "@babel/plugin-transform-destructuring": "^7.28.5",
        "@babel/plugin-transform-dotall-regex": "^7.28.6",
        "@babel/plugin-transform-duplicate-keys": "^7.27.1",
        "@babel/plugin-transform-duplicate-named-capturing-groups-regex": "^7.29.0",
        "@babel/plugin-transform-dynamic-import": "^7.27.1",
        "@babel/plugin-transform-explicit-resource-management": "^7.28.6",
        "@babel/plugin-transform-exponentiation-operator": "^7.28.6",
        "@babel/plugin-transform-export-namespace-from": "^7.27.1",
        "@babel/plugin-transform-for-of": "^7.27.1",
        "@babel/plugin-transform-function-name": "^7.27.1",
        "@babel/plugin-transform-json-strings": "^7.28.6",
        "@babel/plugin-transform-literals": "^7.27.1",
        "@babel/plugin-transform-logical-assignment-operators": "^7.28.6",
        "@babel/plugin-transform-member-expression-literals": "^7.27.1",
        "@babel/plugin-transform-modules-amd": "^7.27.1",
        "@babel/plugin-transform-modules-commonjs": "^7.28.6",
        "@babel/plugin-transform-modules-systemjs": "^7.29.0",
        "@babel/plugin-transform-modules-umd": "^7.27.1",
        "@babel/plugin-transform-named-capturing-groups-regex": "^7.29.0",
        "@babel/plugin-transform-new-target": "^7.27.1",
        "@babel/plugin-transform-nullish-coalescing-operator": "^7.28.6",
        "@babel/plugin-transform-numeric-separator": "^7.28.6",
        "@babel/plugin-transform-object-rest-spread": "^7.28.6",
        "@babel/plugin-transform-object-super": "^7.27.1",
        "@babel/plugin-transform-optional-catch-binding": "^7.28.6",
        "@babel/plugin-transform-optional-chaining": "^7.28.6",
        "@babel/plugin-transform-parameters": "^7.27.7",
        "@babel/plugin-transform-private-methods": "^7.28.6",
        "@babel/plugin-transform-private-property-in-object": "^7.28.6",
        "@babel/plugin-transform-property-literals": "^7.27.1",
        "@babel/plugin-transform-regenerator": "^7.29.0",
        "@babel/plugin-transform-regexp-modifiers": "^7.28.6",
        "@babel/plugin-transform-reserved-words": "^7.27.1",
        "@babel/plugin-transform-shorthand-properties": "^7.27.1",
        "@babel/plugin-transform-spread": "^7.28.6",
        "@babel/plugin-transform-sticky-regex": "^7.27.1",
        "@babel/plugin-transform-template-literals": "^7.27.1",
        "@babel/plugin-transform-typeof-symbol": "^7.27.1",
        "@babel/plugin-transform-unicode-escapes": "^7.27.1",
        "@babel/plugin-transform-unicode-property-regex": "^7.28.6",
        "@babel/plugin-transform-unicode-regex": "^7.27.1",
        "@babel/plugin-transform-unicode-sets-regex": "^7.28.6",
        "@babel/preset-modules": "0.1.6-no-external-plugins",
        "babel-plugin-polyfill-corejs2": "^0.4.15",
        "babel-plugin-polyfill-corejs3": "^0.14.0",
        "babel-plugin-polyfill-regenerator": "^0.6.6",
        "core-js-compat": "^3.48.0",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/preset-env/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/preset-modules": {
      "version": "0.1.6-no-external-plugins",
      "resolved": "https://registry.npmjs.org/@babel/preset-modules/-/preset-modules-0.1.6-no-external-plugins.tgz",
      "integrity": "sha512-HrcgcIESLm9aIR842yhJ5RWan/gebQUJ6E/E5+rf0y9o6oj7w0Br+sWuL6kEQ/o/AdfvR1Je9jG18/gnpwjEyA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.0.0",
        "@babel/types": "^7.4.4",
        "esutils": "^2.0.2"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/@babel/preset-react": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/preset-react/-/preset-react-7.28.5.tgz",
      "integrity": "sha512-Z3J8vhRq7CeLjdC58jLv4lnZ5RKFUJWqH5emvxmv9Hv3BD1T9R/Im713R4MTKwvFaV74ejZ3sM01LyEKk4ugNQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-validator-option": "^7.27.1",
        "@babel/plugin-transform-react-display-name": "^7.28.0",
        "@babel/plugin-transform-react-jsx": "^7.27.1",
        "@babel/plugin-transform-react-jsx-development": "^7.27.1",
        "@babel/plugin-transform-react-pure-annotations": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/preset-typescript": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/preset-typescript/-/preset-typescript-7.28.5.tgz",
      "integrity": "sha512-+bQy5WOI2V6LJZpPVxY+yp66XdZ2yifu0Mc1aP5CQKgjn4QM5IN2i5fAZ4xKop47pr8rpVhiAeu+nDQa12C8+g==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-validator-option": "^7.27.1",
        "@babel/plugin-syntax-jsx": "^7.27.1",
        "@babel/plugin-transform-modules-commonjs": "^7.27.1",
        "@babel/plugin-transform-typescript": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/runtime": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/runtime/-/runtime-7.28.6.tgz",
      "integrity": "sha512-05WQkdpL9COIMz4LjTxGpPNCdlpyimKppYNoJ5Di5EUObifl8t4tuLuUBBZEpoLYOmfvIWrsp9fCl0HoPRVTdA==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/template": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/template/-/template-7.28.6.tgz",
      "integrity": "sha512-YA6Ma2KsCdGb+WC6UpBVFJGXL58MDA6oyONbjyF/+5sBgxY/dwkhLogbMT2GXXyU84/IhRw/2D1Os1B/giz+BQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.28.6",
        "@babel/parser": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/traverse": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/traverse/-/traverse-7.29.0.tgz",
      "integrity": "sha512-4HPiQr0X7+waHfyXPZpWPfWL/J7dcN1mx9gL6WdQVMbPnF3+ZhSMs8tCxN7oHddJE9fhNE7+lxdnlyemKfJRuA==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.0",
        "@babel/generator": "^7.29.0",
        "@babel/helper-globals": "^7.28.0",
        "@babel/parser": "^7.29.0",
        "@babel/template": "^7.28.6",
        "@babel/types": "^7.29.0",
        "debug": "^4.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/types": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/types/-/types-7.29.0.tgz",
      "integrity": "sha512-LwdZHpScM4Qz8Xw2iKSzS+cfglZzJGvofQICy7W7v4caru4EaAmyUuO6BGrbyQ2mYV11W0U8j5mBhd14dd3B0A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-string-parser": "^7.27.1",
        "@babel/helper-validator-identifier": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@bcoe/v8-coverage": {
      "version": "0.2.3",
      "resolved": "https://registry.npmjs.org/@bcoe/v8-coverage/-/v8-coverage-0.2.3.tgz",
      "integrity": "sha512-0hYQ8SB4Db5zvZB4axdMHGwEaQjkZzFjQiN9LVYvIFB2nSUHW9tYpxWriPrWDASIxiaXax83REcLxuSdnGPZtw==",
      "license": "MIT"
    },
    "node_modules/@csstools/normalize.css": {
      "version": "12.1.1",
      "resolved": "https://registry.npmjs.org/@csstools/normalize.css/-/normalize.css-12.1.1.tgz",
      "integrity": "sha512-YAYeJ+Xqh7fUou1d1j9XHl44BmsuThiTr4iNrgCQ3J27IbhXsxXDGZ1cXv8Qvs99d4rBbLiSKy3+WZiet32PcQ==",
      "license": "CC0-1.0"
    },
    "node_modules/@csstools/postcss-cascade-layers": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-cascade-layers/-/postcss-cascade-layers-1.1.1.tgz",
      "integrity": "sha512-+KdYrpKC5TgomQr2DlZF4lDEpHcoxnj5IGddYYfBWJAKfj1JtuHUIqMa+E1pJJ+z3kvDViWMqyqPlG4Ja7amQA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/selector-specificity": "^2.0.2",
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-color-function": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-color-function/-/postcss-color-function-1.1.1.tgz",
      "integrity": "sha512-Bc0f62WmHdtRDjf5f3e2STwRAl89N2CLb+9iAwzrv4L2hncrbDwnQD9PCq0gtAt7pOI2leIV08HIBUd4jxD8cw==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-font-format-keywords": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-font-format-keywords/-/postcss-font-format-keywords-1.0.1.tgz",
      "integrity": "sha512-ZgrlzuUAjXIOc2JueK0X5sZDjCtgimVp/O5CEqTcs5ShWBa6smhWYbS0x5cVc/+rycTDbjjzoP0KTDnUneZGOg==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-hwb-function": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-hwb-function/-/postcss-hwb-function-1.0.2.tgz",
      "integrity": "sha512-YHdEru4o3Rsbjmu6vHy4UKOXZD+Rn2zmkAmLRfPet6+Jz4Ojw8cbWxe1n42VaXQhD3CQUXXTooIy8OkVbUcL+w==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-ic-unit": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-ic-unit/-/postcss-ic-unit-1.0.1.tgz",
      "integrity": "sha512-Ot1rcwRAaRHNKC9tAqoqNZhjdYBzKk1POgWfhN4uCOE47ebGcLRqXjKkApVDpjifL6u2/55ekkpnFcp+s/OZUw==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-is-pseudo-class": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-is-pseudo-class/-/postcss-is-pseudo-class-2.0.7.tgz",
      "integrity": "sha512-7JPeVVZHd+jxYdULl87lvjgvWldYu+Bc62s9vD/ED6/QTGjy0jy0US/f6BG53sVMTBJ1lzKZFpYmofBN9eaRiA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/selector-specificity": "^2.0.0",
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-nested-calc": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-nested-calc/-/postcss-nested-calc-1.0.0.tgz",
      "integrity": "sha512-JCsQsw1wjYwv1bJmgjKSoZNvf7R6+wuHDAbi5f/7MbFhl2d/+v+TvBTU4BJH3G1X1H87dHl0mh6TfYogbT/dJQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-normalize-display-values": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-normalize-display-values/-/postcss-normalize-display-values-1.0.1.tgz",
      "integrity": "sha512-jcOanIbv55OFKQ3sYeFD/T0Ti7AMXc9nM1hZWu8m/2722gOTxFg7xYu4RDLJLeZmPUVQlGzo4jhzvTUq3x4ZUw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-oklab-function": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-oklab-function/-/postcss-oklab-function-1.1.1.tgz",
      "integrity": "sha512-nJpJgsdA3dA9y5pgyb/UfEzE7W5Ka7u0CX0/HIMVBNWzWemdcTH3XwANECU6anWv/ao4vVNLTMxhiPNZsTK6iA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-progressive-custom-properties": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-progressive-custom-properties/-/postcss-progressive-custom-properties-1.3.0.tgz",
      "integrity": "sha512-ASA9W1aIy5ygskZYuWams4BzafD12ULvSypmaLJT2jvQ8G0M3I8PRQhC0h7mG0Z3LI05+agZjqSR9+K9yaQQjA==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.3"
      }
    },
    "node_modules/@csstools/postcss-stepped-value-functions": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-stepped-value-functions/-/postcss-stepped-value-functions-1.0.1.tgz",
      "integrity": "sha512-dz0LNoo3ijpTOQqEJLY8nyaapl6umbmDcgj4AD0lgVQ572b2eqA1iGZYTTWhrcrHztWDDRAX2DGYyw2VBjvCvQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-text-decoration-shorthand": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-text-decoration-shorthand/-/postcss-text-decoration-shorthand-1.0.0.tgz",
      "integrity": "sha512-c1XwKJ2eMIWrzQenN0XbcfzckOLLJiczqy+YvfGmzoVXd7pT9FfObiSEfzs84bpE/VqfpEuAZ9tCRbZkZxxbdw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-trigonometric-functions": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-trigonometric-functions/-/postcss-trigonometric-functions-1.0.2.tgz",
      "integrity": "sha512-woKaLO///4bb+zZC2s80l+7cm07M7268MsyG3M0ActXXEFi6SuhvriQYcb58iiKGbjwwIU7n45iRLEHypB47Og==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-unset-value": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-unset-value/-/postcss-unset-value-1.0.2.tgz",
      "integrity": "sha512-c8J4roPBILnelAsdLr4XOAR/GsTm0GJi4XpcfvoWk3U6KiTCqiFYc63KhRMQQX35jYMp4Ao8Ij9+IZRgMfJp1g==",
      "license": "CC0-1.0",
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/selector-specificity": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/@csstools/selector-specificity/-/selector-specificity-2.2.0.tgz",
      "integrity": "sha512-+OJ9konv95ClSTOJCmMZqpd5+YGsB2S+x6w3E1oaM8UuR5j8nTNHYSz8c9BEPGDOCMQYIEEGlVPj/VY64iTbGw==",
      "license": "CC0-1.0",
      "engines": {
        "node": "^14 || ^16 || >=18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss-selector-parser": "^6.0.10"
      }
    },
    "node_modules/@eslint-community/eslint-utils": {
      "version": "4.9.1",
      "resolved": "https://registry.npmjs.org/@eslint-community/eslint-utils/-/eslint-utils-4.9.1.tgz",
      "integrity": "sha512-phrYmNiYppR7znFEdqgfWHXR6NCkZEK7hwWDHZUjit/2/U0r6XvkDl0SYnoM51Hq7FhCGdLDT6zxCCOY1hexsQ==",
      "license": "MIT",
      "dependencies": {
        "eslint-visitor-keys": "^3.4.3"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || >=8.0.0"
      }
    },
    "node_modules/@eslint-community/regexpp": {
      "version": "4.12.2",
      "resolved": "https://registry.npmjs.org/@eslint-community/regexpp/-/regexpp-4.12.2.tgz",
      "integrity": "sha512-EriSTlt5OC9/7SXkRSCAhfSxxoSUgBm33OH+IkwbdpgoqsSsUg7y3uh+IICI/Qg4BBWr3U2i39RpmycbxMq4ew==",
      "license": "MIT",
      "engines": {
        "node": "^12.0.0 || ^14.0.0 || >=16.0.0"
      }
    },
    "node_modules/@eslint/eslintrc": {
      "version": "2.1.4",
      "resolved": "https://registry.npmjs.org/@eslint/eslintrc/-/eslintrc-2.1.4.tgz",
      "integrity": "sha512-269Z39MS6wVJtsoUl10L60WdkhJVdPG24Q4eZTH3nnF6lpvSShEK3wQjDX9JRWAUPvPh7COouPpU9IrqaZFvtQ==",
      "license": "MIT",
      "dependencies": {
        "ajv": "^6.12.4",
        "debug": "^4.3.2",
        "espree": "^9.6.0",
        "globals": "^13.19.0",
        "ignore": "^5.2.0",
        "import-fresh": "^3.2.1",
        "js-yaml": "^4.1.0",
        "minimatch": "^3.1.2",
        "strip-json-comments": "^3.1.1"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint/eslintrc/node_modules/argparse": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/argparse/-/argparse-2.0.1.tgz",
      "integrity": "sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q==",
      "license": "Python-2.0"
    },
    "node_modules/@eslint/eslintrc/node_modules/js-yaml": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/js-yaml/-/js-yaml-4.1.1.tgz",
      "integrity": "sha512-qQKT4zQxXl8lLwBtHMWwaTcGfFOZviOJet3Oy/xmGk2gZH677CJM9EvtfdSkgWcATZhj/55JZ0rmy3myCT5lsA==",
      "license": "MIT",
      "dependencies": {
        "argparse": "^2.0.1"
      },
      "bin": {
        "js-yaml": "bin/js-yaml.js"
      }
    },
    "node_modules/@eslint/js": {
      "version": "8.57.1",
      "resolved": "https://registry.npmjs.org/@eslint/js/-/js-8.57.1.tgz",
      "integrity": "sha512-d9zaMRSTIKDLhctzH12MtXvJKSSUhaHcjV+2Z+GK+EEY7XKpP5yR4x+N3TAcHTcu963nIr+TMcCb4DBCYX1z6Q==",
      "license": "MIT",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      }
    },
    "node_modules/@humanwhocodes/config-array": {
      "version": "0.13.0",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/config-array/-/config-array-0.13.0.tgz",
      "integrity": "sha512-DZLEEqFWQFiyK6h5YIeynKx7JlvCYWL0cImfSRXZ9l4Sg2efkFGTuFf6vzXjK1cq6IYkU+Eg/JizXw+TD2vRNw==",
      "deprecated": "Use @eslint/config-array instead",
      "license": "Apache-2.0",
      "dependencies": {
        "@humanwhocodes/object-schema": "^2.0.3",
        "debug": "^4.3.1",
        "minimatch": "^3.0.5"
      },
      "engines": {
        "node": ">=10.10.0"
      }
    },
    "node_modules/@humanwhocodes/module-importer": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/module-importer/-/module-importer-1.0.1.tgz",
      "integrity": "sha512-bxveV4V8v5Yb4ncFTT3rPSgZBOpCkjfK0y4oVVVJwIuDVBRMDXrPyXRL988i5ap9m9bnyEEjWfm5WkBmtffLfA==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=12.22"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@humanwhocodes/object-schema": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/object-schema/-/object-schema-2.0.3.tgz",
      "integrity": "sha512-93zYdMES/c1D69yZiKDBj0V24vqNzB/koF26KPaagAfd3P/4gUlh3Dys5ogAK+Exi9QyzlD8x/08Zt7wIKcDcA==",
      "deprecated": "Use @eslint/object-schema instead",
      "license": "BSD-3-Clause"
    },
    "node_modules/@istanbuljs/load-nyc-config": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@istanbuljs/load-nyc-config/-/load-nyc-config-1.1.0.tgz",
      "integrity": "sha512-VjeHSlIzpv/NyD3N0YuHfXOPDIixcA1q2ZV98wsMqcYlPmv2n3Yb2lYP9XMElnaFVXg5A7YLTeLu6V84uQDjmQ==",
      "license": "ISC",
      "dependencies": {
        "camelcase": "^5.3.1",
        "find-up": "^4.1.0",
        "get-package-type": "^0.1.0",
        "js-yaml": "^3.13.1",
        "resolve-from": "^5.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/@istanbuljs/load-nyc-config/node_modules/camelcase": {
      "version": "5.3.1",
      "resolved": "https://registry.npmjs.org/camelcase/-/camelcase-5.3.1.tgz",
      "integrity": "sha512-L28STB170nwWS63UjtlEOE3dldQApaJXZkOI1uMFfzf3rRuPegHaHesyee+YxQ+W6SvRDQV6UrdOdRiR153wJg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/@istanbuljs/schema": {
      "version": "0.1.3",
      "resolved": "https://registry.npmjs.org/@istanbuljs/schema/-/schema-0.1.3.tgz",
      "integrity": "sha512-ZXRY4jNvVgSVQ8DL3LTcakaAtXwTVUxE81hslsyD2AtoXW/wVob10HkOJ1X/pAlcI7D+2YoZKg5do8G/w6RYgA==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/@jest/console": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/console/-/console-27.5.1.tgz",
      "integrity": "sha512-kZ/tNpS3NXn0mlXXXPNuDZnb4c0oZ20r4K5eemM2k30ZC3G0T02nXUvyhf5YdbXWHPEJLc9qGLxEZ216MdL+Zg==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "jest-message-util": "^27.5.1",
        "jest-util": "^27.5.1",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/core": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/core/-/core-27.5.1.tgz",
      "integrity": "sha512-AK6/UTrvQD0Cd24NSqmIA6rKsu0tKIxfiCducZvqxYdmMisOYAsdItspT+fQDQYARPf8XgjAFZi0ogW2agH5nQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/console": "^27.5.1",
        "@jest/reporters": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "ansi-escapes": "^4.2.1",
        "chalk": "^4.0.0",
        "emittery": "^0.8.1",
        "exit": "^0.1.2",
        "graceful-fs": "^4.2.9",
        "jest-changed-files": "^27.5.1",
        "jest-config": "^27.5.1",
        "jest-haste-map": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-resolve-dependencies": "^27.5.1",
        "jest-runner": "^27.5.1",
        "jest-runtime": "^27.5.1",
        "jest-snapshot": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-validate": "^27.5.1",
        "jest-watcher": "^27.5.1",
        "micromatch": "^4.0.4",
        "rimraf": "^3.0.0",
        "slash": "^3.0.0",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "node-notifier": "^8.0.1 || ^9.0.0 || ^10.0.0"
      },
      "peerDependenciesMeta": {
        "node-notifier": {
          "optional": true
        }
      }
    },
    "node_modules/@jest/environment": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/environment/-/environment-27.5.1.tgz",
      "integrity": "sha512-/WQjhPJe3/ghaol/4Bq480JKXV/Rfw8nQdN7f41fM8VDHLcxKXou6QyXAh3EFr9/bVG3x74z1NWDkP87EiY8gA==",
      "license": "MIT",
      "dependencies": {
        "@jest/fake-timers": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "jest-mock": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/fake-timers": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/fake-timers/-/fake-timers-27.5.1.tgz",
      "integrity": "sha512-/aPowoolwa07k7/oM3aASneNeBGCmGQsc3ugN4u6s4C/+s5M64MFo/+djTdiwcbQlRfFElGuDXWzaWj6QgKObQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@sinonjs/fake-timers": "^8.0.1",
        "@types/node": "*",
        "jest-message-util": "^27.5.1",
        "jest-mock": "^27.5.1",
        "jest-util": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/globals": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/globals/-/globals-27.5.1.tgz",
      "integrity": "sha512-ZEJNB41OBQQgGzgyInAv0UUfDDj3upmHydjieSxFvTRuZElrx7tXg/uVQ5hYVEwiXs3+aMsAeEc9X7xiSKCm4Q==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/types": "^27.5.1",
        "expect": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/reporters": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/reporters/-/reporters-27.5.1.tgz",
      "integrity": "sha512-cPXh9hWIlVJMQkVk84aIvXuBB4uQQmFqZiacloFuGiP3ah1sbCxCosidXFDfqG8+6fO1oR2dTJTlsOy4VFmUfw==",
      "license": "MIT",
      "dependencies": {
        "@bcoe/v8-coverage": "^0.2.3",
        "@jest/console": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "collect-v8-coverage": "^1.0.0",
        "exit": "^0.1.2",
        "glob": "^7.1.2",
        "graceful-fs": "^4.2.9",
        "istanbul-lib-coverage": "^3.0.0",
        "istanbul-lib-instrument": "^5.1.0",
        "istanbul-lib-report": "^3.0.0",
        "istanbul-lib-source-maps": "^4.0.0",
        "istanbul-reports": "^3.1.3",
        "jest-haste-map": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-worker": "^27.5.1",
        "slash": "^3.0.0",
        "source-map": "^0.6.0",
        "string-length": "^4.0.1",
        "terminal-link": "^2.0.0",
        "v8-to-istanbul": "^8.1.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "node-notifier": "^8.0.1 || ^9.0.0 || ^10.0.0"
      },
      "peerDependenciesMeta": {
        "node-notifier": {
          "optional": true
        }
      }
    },
    "node_modules/@jest/reporters/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/@jest/schemas": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/@jest/schemas/-/schemas-28.1.3.tgz",
      "integrity": "sha512-/l/VWsdt/aBXgjshLWOFyFt3IVdYypu5y2Wn2rOO1un6nkqIn8SLXzgIMYXFyYsRWDyF5EthmKJMIdJvk08grg==",
      "license": "MIT",
      "dependencies": {
        "@sinclair/typebox": "^0.24.1"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/@jest/source-map": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/source-map/-/source-map-27.5.1.tgz",
      "integrity": "sha512-y9NIHUYF3PJRlHk98NdC/N1gl88BL08aQQgu4k4ZopQkCw9t9cV8mtl3TV8b/YCB8XaVTFrmUTAJvjsntDireg==",
      "license": "MIT",
      "dependencies": {
        "callsites": "^3.0.0",
        "graceful-fs": "^4.2.9",
        "source-map": "^0.6.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/source-map/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/@jest/test-result": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/test-result/-/test-result-27.5.1.tgz",
      "integrity": "sha512-EW35l2RYFUcUQxFJz5Cv5MTOxlJIQs4I7gxzi2zVU7PJhOwfYq1MdC5nhSmYjX1gmMmLPvB3sIaC+BkcHRBfag==",
      "license": "MIT",
      "dependencies": {
        "@jest/console": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/istanbul-lib-coverage": "^2.0.0",
        "collect-v8-coverage": "^1.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/test-sequencer": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/test-sequencer/-/test-sequencer-27.5.1.tgz",
      "integrity": "sha512-LCheJF7WB2+9JuCS7VB/EmGIdQuhtqjRNI9A43idHv3E4KltCTsPsLxvdaubFHSYwY/fNjMWjl6vNRhDiN7vpQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/test-result": "^27.5.1",
        "graceful-fs": "^4.2.9",
        "jest-haste-map": "^27.5.1",
        "jest-runtime": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/transform": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/transform/-/transform-27.5.1.tgz",
      "integrity": "sha512-ipON6WtYgl/1329g5AIJVbUuEh0wZVbdpGwC99Jw4LwuoBNS95MVphU6zOeD9pDkon+LLbFL7lOQRapbB8SCHw==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.1.0",
        "@jest/types": "^27.5.1",
        "babel-plugin-istanbul": "^6.1.1",
        "chalk": "^4.0.0",
        "convert-source-map": "^1.4.0",
        "fast-json-stable-stringify": "^2.0.0",
        "graceful-fs": "^4.2.9",
        "jest-haste-map": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-util": "^27.5.1",
        "micromatch": "^4.0.4",
        "pirates": "^4.0.4",
        "slash": "^3.0.0",
        "source-map": "^0.6.1",
        "write-file-atomic": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/transform/node_modules/convert-source-map": {
      "version": "1.9.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-1.9.0.tgz",
      "integrity": "sha512-ASFBup0Mz1uyiIjANan1jzLQami9z1PoYSZCiiYW2FczPbenXc45FZdBZLzOT+r6+iciuEModtmCti+hjaAk0A==",
      "license": "MIT"
    },
    "node_modules/@jest/transform/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/@jest/types": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/types/-/types-27.5.1.tgz",
      "integrity": "sha512-Cx46iJ9QpwQTjIdq5VJu2QTMMs3QlEjI0x1QbBP5W1+nMzyc2XmimiRR/CbX9TO0cPTeUlxWMOu8mslYsJ8DEw==",
      "license": "MIT",
      "dependencies": {
        "@types/istanbul-lib-coverage": "^2.0.0",
        "@types/istanbul-reports": "^3.0.0",
        "@types/node": "*",
        "@types/yargs": "^16.0.0",
        "chalk": "^4.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jridgewell/gen-mapping": {
      "version": "0.3.13",
      "resolved": "https://registry.npmjs.org/@jridgewell/gen-mapping/-/gen-mapping-0.3.13.tgz",
      "integrity": "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.0",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/remapping": {
      "version": "2.3.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/remapping/-/remapping-2.3.5.tgz",
      "integrity": "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/source-map": {
      "version": "0.3.11",
      "resolved": "https://registry.npmjs.org/@jridgewell/source-map/-/source-map-0.3.11.tgz",
      "integrity": "sha512-ZMp1V8ZFcPG5dIWnQLr3NSI1MiCU7UETdS/A0G8V/XWHvJv3ZsFqutJn1Y5RPmAPX6F3BiE397OqveU/9NCuIA==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.25"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "license": "MIT"
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@leichtgewicht/ip-codec": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@leichtgewicht/ip-codec/-/ip-codec-2.0.5.tgz",
      "integrity": "sha512-Vo+PSpZG2/fmgmiNzYK9qWRh8h/CHrwD0mo1h1DzL4yzHNSfWYujGTYsWGreD000gcgmZ7K4Ys6Tx9TxtsKdDw==",
      "license": "MIT"
    },
    "node_modules/@nicolo-ribaudo/eslint-scope-5-internals": {
      "version": "5.1.1-v1",
      "resolved": "https://registry.npmjs.org/@nicolo-ribaudo/eslint-scope-5-internals/-/eslint-scope-5-internals-5.1.1-v1.tgz",
      "integrity": "sha512-54/JRvkLIzzDWshCWfuhadfrfZVPiElY8Fcgmg1HroEly/EDSszzhBAsarCux+D/kOslTRquNzuyGSmUSTTHGg==",
      "license": "MIT",
      "dependencies": {
        "eslint-scope": "5.1.1"
      }
    },
    "node_modules/@nicolo-ribaudo/eslint-scope-5-internals/node_modules/eslint-scope": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-5.1.1.tgz",
      "integrity": "sha512-2NxwbF/hZ0KpepYN0cNbo+FN6XoK7GaHlQhgx/hIZl6Va0bF45RQOOwhLIy8lQDbuCiadSLCBnH2CFYquit5bw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^4.1.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/@nicolo-ribaudo/eslint-scope-5-internals/node_modules/estraverse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-4.3.0.tgz",
      "integrity": "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/@nodelib/fs.scandir": {
      "version": "2.1.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.scandir/-/fs.scandir-2.1.5.tgz",
      "integrity": "sha512-vq24Bq3ym5HEQm2NKCr3yXDwjc7vTsEThRDnkp2DK9p1uqLR+DHurm/NOTo0KG7HYHU7eppKZj3MyqYuMBf62g==",
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "2.0.5",
        "run-parallel": "^1.1.9"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.stat": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.stat/-/fs.stat-2.0.5.tgz",
      "integrity": "sha512-RkhPPp2zrqDAQA/2jNhnztcPAlv64XdhIp7a7454A5ovI7Bukxgt7MX7udwAu3zg1DcpPU0rz3VV1SeaqvY4+A==",
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.walk": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.walk/-/fs.walk-1.2.8.tgz",
      "integrity": "sha512-oGB+UxlgWcgQkgwo8GcEGwemoTFt3FIO9ababBmaGwXIoBKZ+GTy0pP185beGg7Llih/NSHSV2XAs1lnznocSg==",
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.scandir": "2.1.5",
        "fastq": "^1.6.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@pmmmwh/react-refresh-webpack-plugin": {
      "version": "0.5.17",
      "resolved": "https://registry.npmjs.org/@pmmmwh/react-refresh-webpack-plugin/-/react-refresh-webpack-plugin-0.5.17.tgz",
      "integrity": "sha512-tXDyE1/jzFsHXjhRZQ3hMl0IVhYe5qula43LDWIhVfjp9G/nT5OQY5AORVOrkEGAUltBJOfOWeETbmhm6kHhuQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-html": "^0.0.9",
        "core-js-pure": "^3.23.3",
        "error-stack-parser": "^2.0.6",
        "html-entities": "^2.1.0",
        "loader-utils": "^2.0.4",
        "schema-utils": "^4.2.0",
        "source-map": "^0.7.3"
      },
      "engines": {
        "node": ">= 10.13"
      },
      "peerDependencies": {
        "@types/webpack": "4.x || 5.x",
        "react-refresh": ">=0.10.0 <1.0.0",
        "sockjs-client": "^1.4.0",
        "type-fest": ">=0.17.0 <5.0.0",
        "webpack": ">=4.43.0 <6.0.0",
        "webpack-dev-server": "3.x || 4.x || 5.x",
        "webpack-hot-middleware": "2.x",
        "webpack-plugin-serve": "0.x || 1.x"
      },
      "peerDependenciesMeta": {
        "@types/webpack": {
          "optional": true
        },
        "sockjs-client": {
          "optional": true
        },
        "type-fest": {
          "optional": true
        },
        "webpack-dev-server": {
          "optional": true
        },
        "webpack-hot-middleware": {
          "optional": true
        },
        "webpack-plugin-serve": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/plugin-babel": {
      "version": "5.3.1",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-babel/-/plugin-babel-5.3.1.tgz",
      "integrity": "sha512-WFfdLWU/xVWKeRQnKmIAQULUI7Il0gZnBIH/ZFO069wYIfPu+8zrfp/KMW0atmELoRDq8FbiP3VCss9MhCut7Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.10.4",
        "@rollup/pluginutils": "^3.1.0"
      },
      "engines": {
        "node": ">= 10.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0",
        "@types/babel__core": "^7.1.9",
        "rollup": "^1.20.0||^2.0.0"
      },
      "peerDependenciesMeta": {
        "@types/babel__core": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/plugin-node-resolve": {
      "version": "11.2.1",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-node-resolve/-/plugin-node-resolve-11.2.1.tgz",
      "integrity": "sha512-yc2n43jcqVyGE2sqV5/YCmocy9ArjVAP/BeXyTtADTBBX6V0e5UMqwO8CdQ0kzjb6zu5P1qMzsScCMRvE9OlVg==",
      "license": "MIT",
      "dependencies": {
        "@rollup/pluginutils": "^3.1.0",
        "@types/resolve": "1.17.1",
        "builtin-modules": "^3.1.0",
        "deepmerge": "^4.2.2",
        "is-module": "^1.0.0",
        "resolve": "^1.19.0"
      },
      "engines": {
        "node": ">= 10.0.0"
      },
      "peerDependencies": {
        "rollup": "^1.20.0||^2.0.0"
      }
    },
    "node_modules/@rollup/plugin-replace": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-replace/-/plugin-replace-2.4.2.tgz",
      "integrity": "sha512-IGcu+cydlUMZ5En85jxHH4qj2hta/11BHq95iHEyb2sbgiN0eCdzvUcHw5gt9pBL5lTi4JDYJ1acCoMGpTvEZg==",
      "license": "MIT",
      "dependencies": {
        "@rollup/pluginutils": "^3.1.0",
        "magic-string": "^0.25.7"
      },
      "peerDependencies": {
        "rollup": "^1.20.0 || ^2.0.0"
      }
    },
    "node_modules/@rollup/pluginutils": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/@rollup/pluginutils/-/pluginutils-3.1.0.tgz",
      "integrity": "sha512-GksZ6pr6TpIjHm8h9lSQ8pi8BE9VeubNT0OMJ3B5uZJ8pz73NPiqOtCog/x2/QzM1ENChPKxMDhiQuRHsqc+lg==",
      "license": "MIT",
      "dependencies": {
        "@types/estree": "0.0.39",
        "estree-walker": "^1.0.1",
        "picomatch": "^2.2.2"
      },
      "engines": {
        "node": ">= 8.0.0"
      },
      "peerDependencies": {
        "rollup": "^1.20.0||^2.0.0"
      }
    },
    "node_modules/@rollup/pluginutils/node_modules/@types/estree": {
      "version": "0.0.39",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-0.0.39.tgz",
      "integrity": "sha512-EYNwp3bU+98cpU4lAWYYL7Zz+2gryWH1qbdDTidVd6hkiR6weksdbMadyXKXNPEkQFhXM+hVO9ZygomHXp+AIw==",
      "license": "MIT"
    },
    "node_modules/@rtsao/scc": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@rtsao/scc/-/scc-1.1.0.tgz",
      "integrity": "sha512-zt6OdqaDoOnJ1ZYsCYGt9YmWzDXl4vQdKTyJev62gFhRGKdx7mcT54V9KIjg+d2wi9EXsPvAPKe7i7WjfVWB8g==",
      "license": "MIT"
    },
    "node_modules/@rushstack/eslint-patch": {
      "version": "1.16.1",
      "resolved": "https://registry.npmjs.org/@rushstack/eslint-patch/-/eslint-patch-1.16.1.tgz",
      "integrity": "sha512-TvZbIpeKqGQQ7X0zSCvPH9riMSFQFSggnfBjFZ1mEoILW+UuXCKwOoPcgjMwiUtRqFZ8jWhPJc4um14vC6I4ag==",
      "license": "MIT"
    },
    "node_modules/@sinclair/typebox": {
      "version": "0.24.51",
      "resolved": "https://registry.npmjs.org/@sinclair/typebox/-/typebox-0.24.51.tgz",
      "integrity": "sha512-1P1OROm/rdubP5aFDSZQILU0vrLCJ4fvHt6EoqHEM+2D/G5MK3bIaymUKLit8Js9gbns5UyJnkP/TZROLw4tUA==",
      "license": "MIT"
    },
    "node_modules/@sinonjs/commons": {
      "version": "1.8.6",
      "resolved": "https://registry.npmjs.org/@sinonjs/commons/-/commons-1.8.6.tgz",
      "integrity": "sha512-Ky+XkAkqPZSm3NLBeUng77EBQl3cmeJhITaGHdYH8kjVB+aun3S4XBRti2zt17mtt0mIUDiNxYeoJm6drVvBJQ==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "type-detect": "4.0.8"
      }
    },
    "node_modules/@sinonjs/fake-timers": {
      "version": "8.1.0",
      "resolved": "https://registry.npmjs.org/@sinonjs/fake-timers/-/fake-timers-8.1.0.tgz",
      "integrity": "sha512-OAPJUAtgeINhh/TAlUID4QTs53Njm7xzddaVlEs/SXwgtiD1tW22zAB/W1wdqfrpmikgaWQ9Fw6Ws+hsiRm5Vg==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "@sinonjs/commons": "^1.7.0"
      }
    },
    "node_modules/@surma/rollup-plugin-off-main-thread": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/@surma/rollup-plugin-off-main-thread/-/rollup-plugin-off-main-thread-2.2.3.tgz",
      "integrity": "sha512-lR8q/9W7hZpMWweNiAKU7NQerBnzQQLvi8qnTDU/fxItPhtZVMbPV3lbCwjhIlNBe9Bbr5V+KHshvWmVSG9cxQ==",
      "license": "Apache-2.0",
      "dependencies": {
        "ejs": "^3.1.6",
        "json5": "^2.2.0",
        "magic-string": "^0.25.0",
        "string.prototype.matchall": "^4.0.6"
      }
    },
    "node_modules/@svgr/babel-plugin-add-jsx-attribute": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-add-jsx-attribute/-/babel-plugin-add-jsx-attribute-5.4.0.tgz",
      "integrity": "sha512-ZFf2gs/8/6B8PnSofI0inYXr2SDNTDScPXhN7k5EqD4aZ3gi6u+rbmZHVB8IM3wDyx8ntKACZbtXSm7oZGRqVg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-remove-jsx-attribute": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-remove-jsx-attribute/-/babel-plugin-remove-jsx-attribute-5.4.0.tgz",
      "integrity": "sha512-yaS4o2PgUtwLFGTKbsiAy6D0o3ugcUhWK0Z45umJ66EPWunAz9fuFw2gJuje6wqQvQWOTJvIahUwndOXb7QCPg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-remove-jsx-empty-expression": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-remove-jsx-empty-expression/-/babel-plugin-remove-jsx-empty-expression-5.0.1.tgz",
      "integrity": "sha512-LA72+88A11ND/yFIMzyuLRSMJ+tRKeYKeQ+mR3DcAZ5I4h5CPWN9AHyUzJbWSYp/u2u0xhmgOe0+E41+GjEueA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-replace-jsx-attribute-value": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-replace-jsx-attribute-value/-/babel-plugin-replace-jsx-attribute-value-5.0.1.tgz",
      "integrity": "sha512-PoiE6ZD2Eiy5mK+fjHqwGOS+IXX0wq/YDtNyIgOrc6ejFnxN4b13pRpiIPbtPwHEc+NT2KCjteAcq33/F1Y9KQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-svg-dynamic-title": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-svg-dynamic-title/-/babel-plugin-svg-dynamic-title-5.4.0.tgz",
      "integrity": "sha512-zSOZH8PdZOpuG1ZVx/cLVePB2ibo3WPpqo7gFIjLV9a0QsuQAzJiwwqmuEdTaW2pegyBE17Uu15mOgOcgabQZg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-svg-em-dimensions": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-svg-em-dimensions/-/babel-plugin-svg-em-dimensions-5.4.0.tgz",
      "integrity": "sha512-cPzDbDA5oT/sPXDCUYoVXEmm3VIoAWAPT6mSPTJNbQaBNUuEKVKyGH93oDY4e42PYHRW67N5alJx/eEol20abw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-transform-react-native-svg": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-transform-react-native-svg/-/babel-plugin-transform-react-native-svg-5.4.0.tgz",
      "integrity": "sha512-3eYP/SaopZ41GHwXma7Rmxcv9uRslRDTY1estspeB1w1ueZWd/tPlMfEOoccYpEMZU3jD4OU7YitnXcF5hLW2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-transform-svg-component": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-transform-svg-component/-/babel-plugin-transform-svg-component-5.5.0.tgz",
      "integrity": "sha512-q4jSH1UUvbrsOtlo/tKcgSeiCHRSBdXoIoqX1pgcKK/aU3JD27wmMKwGtpB8qRYUYoyXvfGxUVKchLuR5pB3rQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-preset": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-preset/-/babel-preset-5.5.0.tgz",
      "integrity": "sha512-4FiXBjvQ+z2j7yASeGPEi8VD/5rrGQk4Xrq3EdJmoZgz/tpqChpo5hgXDvmEauwtvOc52q8ghhZK4Oy7qph4ig==",
      "license": "MIT",
      "dependencies": {
        "@svgr/babel-plugin-add-jsx-attribute": "^5.4.0",
        "@svgr/babel-plugin-remove-jsx-attribute": "^5.4.0",
        "@svgr/babel-plugin-remove-jsx-empty-expression": "^5.0.1",
        "@svgr/babel-plugin-replace-jsx-attribute-value": "^5.0.1",
        "@svgr/babel-plugin-svg-dynamic-title": "^5.4.0",
        "@svgr/babel-plugin-svg-em-dimensions": "^5.4.0",
        "@svgr/babel-plugin-transform-react-native-svg": "^5.4.0",
        "@svgr/babel-plugin-transform-svg-component": "^5.5.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/core": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/core/-/core-5.5.0.tgz",
      "integrity": "sha512-q52VOcsJPvV3jO1wkPtzTuKlvX7Y3xIcWRpCMtBF3MrteZJtBfQw/+u0B1BHy5ColpQc1/YVTrPEtSYIMNZlrQ==",
      "license": "MIT",
      "dependencies": {
        "@svgr/plugin-jsx": "^5.5.0",
        "camelcase": "^6.2.0",
        "cosmiconfig": "^7.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/hast-util-to-babel-ast": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/hast-util-to-babel-ast/-/hast-util-to-babel-ast-5.5.0.tgz",
      "integrity": "sha512-cAaR/CAiZRB8GP32N+1jocovUtvlj0+e65TB50/6Lcime+EA49m/8l+P2ko+XPJ4dw3xaPS3jOL4F2X4KWxoeQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.12.6"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/plugin-jsx": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/plugin-jsx/-/plugin-jsx-5.5.0.tgz",
      "integrity": "sha512-V/wVh33j12hGh05IDg8GpIUXbjAPnTdPTKuP4VNLggnwaHMPNQNae2pRnyTAILWCQdz5GyMqtO488g7CKM8CBA==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.12.3",
        "@svgr/babel-preset": "^5.5.0",
        "@svgr/hast-util-to-babel-ast": "^5.5.0",
        "svg-parser": "^2.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/plugin-svgo": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/plugin-svgo/-/plugin-svgo-5.5.0.tgz",
      "integrity": "sha512-r5swKk46GuQl4RrVejVwpeeJaydoxkdwkM1mBKOgJLBUJPGaLci6ylg/IjhrRsREKDkr4kbMWdgOtbXEh0fyLQ==",
      "license": "MIT",
      "dependencies": {
        "cosmiconfig": "^7.0.0",
        "deepmerge": "^4.2.2",
        "svgo": "^1.2.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/webpack": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/webpack/-/webpack-5.5.0.tgz",
      "integrity": "sha512-DOBOK255wfQxguUta2INKkzPj6AIS6iafZYiYmHn6W3pHlycSRRlvWKCfLDG10fXfLWqE3DJHgRUOyJYmARa7g==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.12.3",
        "@babel/plugin-transform-react-constant-elements": "^7.12.1",
        "@babel/preset-env": "^7.12.1",
        "@babel/preset-react": "^7.12.5",
        "@svgr/core": "^5.5.0",
        "@svgr/plugin-jsx": "^5.5.0",
        "@svgr/plugin-svgo": "^5.5.0",
        "loader-utils": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@tootallnate/once": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/@tootallnate/once/-/once-1.1.2.tgz",
      "integrity": "sha512-RbzJvlNzmRq5c3O09UipeuXno4tA1FE6ikOjxZK0tuxVv3412l64l5t1W5pj4+rJq9vpkm/kwiR07aZXnsKPxw==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/@types/babel__core": {
      "version": "7.20.5",
      "resolved": "https://registry.npmjs.org/@types/babel__core/-/babel__core-7.20.5.tgz",
      "integrity": "sha512-qoQprZvz5wQFJwMDqeseRXWv3rqMvhgpbXFfVyWhbx9X47POIA6i/+dXefEmZKoAgOaTdaIgNSMqMIU61yRyzA==",
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.20.7",
        "@babel/types": "^7.20.7",
        "@types/babel__generator": "*",
        "@types/babel__template": "*",
        "@types/babel__traverse": "*"
      }
    },
    "node_modules/@types/babel__generator": {
      "version": "7.27.0",
      "resolved": "https://registry.npmjs.org/@types/babel__generator/-/babel__generator-7.27.0.tgz",
      "integrity": "sha512-ufFd2Xi92OAVPYsy+P4n7/U7e68fex0+Ee8gSG9KX7eo084CWiQ4sdxktvdl0bOPupXtVJPY19zk6EwWqUQ8lg==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.0.0"
      }
    },
    "node_modules/@types/babel__template": {
      "version": "7.4.4",
      "resolved": "https://registry.npmjs.org/@types/babel__template/-/babel__template-7.4.4.tgz",
      "integrity": "sha512-h/NUaSyG5EyxBIp8YRxo4RMe2/qQgvyowRwVMzhYhBCONbW8PUsg4lkFMrhgZhUe5z3L3MiLDuvyJ/CaPa2A8A==",
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.1.0",
        "@babel/types": "^7.0.0"
      }
    },
    "node_modules/@types/babel__traverse": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@types/babel__traverse/-/babel__traverse-7.28.0.tgz",
      "integrity": "sha512-8PvcXf70gTDZBgt9ptxJ8elBeBjcLOAcOtoO/mPJjtji1+CdGbHgm77om1GrsPxsiE+uXIpNSK64UYaIwQXd4Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.28.2"
      }
    },
    "node_modules/@types/body-parser": {
      "version": "1.19.6",
      "resolved": "https://registry.npmjs.org/@types/body-parser/-/body-parser-1.19.6.tgz",
      "integrity": "sha512-HLFeCYgz89uk22N5Qg3dvGvsv46B8GLvKKo1zKG4NybA8U2DiEO3w9lqGg29t/tfLRJpJ6iQxnVw4OnB7MoM9g==",
      "license": "MIT",
      "dependencies": {
        "@types/connect": "*",
        "@types/node": "*"
      }
    },
    "node_modules/@types/bonjour": {
      "version": "3.5.13",
      "resolved": "https://registry.npmjs.org/@types/bonjour/-/bonjour-3.5.13.tgz",
      "integrity": "sha512-z9fJ5Im06zvUL548KvYNecEVlA7cVDkGUi6kZusb04mpyEFKCIZJvloCcmpmLaIahDpOQGHaHmG6imtPMmPXGQ==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/connect": {
      "version": "3.4.38",
      "resolved": "https://registry.npmjs.org/@types/connect/-/connect-3.4.38.tgz",
      "integrity": "sha512-K6uROf1LD88uDQqJCktA4yzL1YYAK6NgfsI0v/mTgyPKWsX1CnJ0XPSDhViejru1GcRkLWb8RlzFYJRqGUbaug==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/connect-history-api-fallback": {
      "version": "1.5.4",
      "resolved": "https://registry.npmjs.org/@types/connect-history-api-fallback/-/connect-history-api-fallback-1.5.4.tgz",
      "integrity": "sha512-n6Cr2xS1h4uAulPRdlw6Jl6s1oG8KrVilPN2yUITEs+K48EzMJJ3W1xy8K5eWuFvjp3R74AOIGSmp2UfBJ8HFw==",
      "license": "MIT",
      "dependencies": {
        "@types/express-serve-static-core": "*",
        "@types/node": "*"
      }
    },
    "node_modules/@types/eslint": {
      "version": "8.56.12",
      "resolved": "https://registry.npmjs.org/@types/eslint/-/eslint-8.56.12.tgz",
      "integrity": "sha512-03ruubjWyOHlmljCVoxSuNDdmfZDzsrrz0P2LeJsOXr+ZwFQ+0yQIwNCwt/GYhV7Z31fgtXJTAEs+FYlEL851g==",
      "license": "MIT",
      "dependencies": {
        "@types/estree": "*",
        "@types/json-schema": "*"
      }
    },
    "node_modules/@types/eslint-scope": {
      "version": "3.7.7",
      "resolved": "https://registry.npmjs.org/@types/eslint-scope/-/eslint-scope-3.7.7.tgz",
      "integrity": "sha512-MzMFlSLBqNF2gcHWO0G1vP/YQyfvrxZ0bF+u7mzUdZ1/xK4A4sru+nraZz5i3iEIk1l1uyicaDVTB4QbbEkAYg==",
      "license": "MIT",
      "dependencies": {
        "@types/eslint": "*",
        "@types/estree": "*"
      }
    },
    "node_modules/@types/estree": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-1.0.8.tgz",
      "integrity": "sha512-dWHzHa2WqEXI/O1E9OjrocMTKJl2mSrEolh1Iomrv6U+JuNwaHXsXx9bLu5gG7BUWFIN0skIQJQ/L1rIex4X6w==",
      "license": "MIT"
    },
    "node_modules/@types/express": {
      "version": "4.17.25",
      "resolved": "https://registry.npmjs.org/@types/express/-/express-4.17.25.tgz",
      "integrity": "sha512-dVd04UKsfpINUnK0yBoYHDF3xu7xVH4BuDotC/xGuycx4CgbP48X/KF/586bcObxT0HENHXEU8Nqtu6NR+eKhw==",
      "license": "MIT",
      "dependencies": {
        "@types/body-parser": "*",
        "@types/express-serve-static-core": "^4.17.33",
        "@types/qs": "*",
        "@types/serve-static": "^1"
      }
    },
    "node_modules/@types/express-serve-static-core": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/@types/express-serve-static-core/-/express-serve-static-core-5.1.1.tgz",
      "integrity": "sha512-v4zIMr/cX7/d2BpAEX3KNKL/JrT1s43s96lLvvdTmza1oEvDudCqK9aF/djc/SWgy8Yh0h30TZx5VpzqFCxk5A==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "@types/qs": "*",
        "@types/range-parser": "*",
        "@types/send": "*"
      }
    },
    "node_modules/@types/express/node_modules/@types/express-serve-static-core": {
      "version": "4.19.8",
      "resolved": "https://registry.npmjs.org/@types/express-serve-static-core/-/express-serve-static-core-4.19.8.tgz",
      "integrity": "sha512-02S5fmqeoKzVZCHPZid4b8JH2eM5HzQLZWN2FohQEy/0eXTq8VXZfSN6Pcr3F6N9R/vNrj7cpgbhjie6m/1tCA==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "@types/qs": "*",
        "@types/range-parser": "*",
        "@types/send": "*"
      }
    },
    "node_modules/@types/graceful-fs": {
      "version": "4.1.9",
      "resolved": "https://registry.npmjs.org/@types/graceful-fs/-/graceful-fs-4.1.9.tgz",
      "integrity": "sha512-olP3sd1qOEe5dXTSaFvQG+02VdRXcdytWLAZsAq1PecU8uqQAhkrnbli7DagjtXKW/Bl7YJbUsa8MPcuc8LHEQ==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/html-minifier-terser": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/@types/html-minifier-terser/-/html-minifier-terser-6.1.0.tgz",
      "integrity": "sha512-oh/6byDPnL1zeNXFrDXFLyZjkr1MsBG667IM792caf1L2UPOOMf65NFzjUH/ltyfwjAGfs1rsX1eftK0jC/KIg==",
      "license": "MIT"
    },
    "node_modules/@types/http-errors": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@types/http-errors/-/http-errors-2.0.5.tgz",
      "integrity": "sha512-r8Tayk8HJnX0FztbZN7oVqGccWgw98T/0neJphO91KkmOzug1KkofZURD4UaD5uH8AqcFLfdPErnBod0u71/qg==",
      "license": "MIT"
    },
    "node_modules/@types/http-proxy": {
      "version": "1.17.17",
      "resolved": "https://registry.npmjs.org/@types/http-proxy/-/http-proxy-1.17.17.tgz",
      "integrity": "sha512-ED6LB+Z1AVylNTu7hdzuBqOgMnvG/ld6wGCG8wFnAzKX5uyW2K3WD52v0gnLCTK/VLpXtKckgWuyScYK6cSPaw==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/istanbul-lib-coverage": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/@types/istanbul-lib-coverage/-/istanbul-lib-coverage-2.0.6.tgz",
      "integrity": "sha512-2QF/t/auWm0lsy8XtKVPG19v3sSOQlJe/YHZgfjb/KBBHOGSV+J2q/S671rcq9uTBrLAXmZpqJiaQbMT+zNU1w==",
      "license": "MIT"
    },
    "node_modules/@types/istanbul-lib-report": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/@types/istanbul-lib-report/-/istanbul-lib-report-3.0.3.tgz",
      "integrity": "sha512-NQn7AHQnk/RSLOxrBbGyJM/aVQ+pjj5HCgasFxc0K/KhoATfQ/47AyUl15I2yBUpihjmas+a+VJBOqecrFH+uA==",
      "license": "MIT",
      "dependencies": {
        "@types/istanbul-lib-coverage": "*"
      }
    },
    "node_modules/@types/istanbul-reports": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/@types/istanbul-reports/-/istanbul-reports-3.0.4.tgz",
      "integrity": "sha512-pk2B1NWalF9toCRu6gjBzR69syFjP4Od8WRAX+0mmf9lAjCRicLOWc+ZrxZHx/0XRjotgkF9t6iaMJ+aXcOdZQ==",
      "license": "MIT",
      "dependencies": {
        "@types/istanbul-lib-report": "*"
      }
    },
    "node_modules/@types/json-schema": {
      "version": "7.0.15",
      "resolved": "https://registry.npmjs.org/@types/json-schema/-/json-schema-7.0.15.tgz",
      "integrity": "sha512-5+fP8P8MFNC+AyZCDxrB2pkZFPGzqQWUzpSeuuVLvm8VMcorNYavBqoFcxK8bQz4Qsbn4oUEEem4wDLfcysGHA==",
      "license": "MIT"
    },
    "node_modules/@types/json5": {
      "version": "0.0.29",
      "resolved": "https://registry.npmjs.org/@types/json5/-/json5-0.0.29.tgz",
      "integrity": "sha512-dRLjCWHYg4oaA77cxO64oO+7JwCwnIzkZPdrrC71jQmQtlhM556pwKo5bUzqvZndkVbeFLIIi+9TC40JNF5hNQ==",
      "license": "MIT"
    },
    "node_modules/@types/mime": {
      "version": "1.3.5",
      "resolved": "https://registry.npmjs.org/@types/mime/-/mime-1.3.5.tgz",
      "integrity": "sha512-/pyBZWSLD2n0dcHE3hq8s8ZvcETHtEuF+3E7XVt0Ig2nvsVQXdghHVcEkIWjy9A0wKfTn97a/PSDYohKIlnP/w==",
      "license": "MIT"
    },
    "node_modules/@types/node": {
      "version": "25.4.0",
      "resolved": "https://registry.npmjs.org/@types/node/-/node-25.4.0.tgz",
      "integrity": "sha512-9wLpoeWuBlcbBpOY3XmzSTG3oscB6xjBEEtn+pYXTfhyXhIxC5FsBer2KTopBlvKEiW9l13po9fq+SJY/5lkhw==",
      "license": "MIT",
      "dependencies": {
        "undici-types": "~7.18.0"
      }
    },
    "node_modules/@types/node-forge": {
      "version": "1.3.14",
      "resolved": "https://registry.npmjs.org/@types/node-forge/-/node-forge-1.3.14.tgz",
      "integrity": "sha512-mhVF2BnD4BO+jtOp7z1CdzaK4mbuK0LLQYAvdOLqHTavxFNq4zA1EmYkpnFjP8HOUzedfQkRnp0E2ulSAYSzAw==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/parse-json": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/@types/parse-json/-/parse-json-4.0.2.tgz",
      "integrity": "sha512-dISoDXWWQwUquiKsyZ4Ng+HX2KsPL7LyHKHQwgGFEA3IaKac4Obd+h2a/a6waisAoepJlBcx9paWqjA8/HVjCw==",
      "license": "MIT"
    },
    "node_modules/@types/prettier": {
      "version": "2.7.3",
      "resolved": "https://registry.npmjs.org/@types/prettier/-/prettier-2.7.3.tgz",
      "integrity": "sha512-+68kP9yzs4LMp7VNh8gdzMSPZFL44MLGqiHWvttYJe+6qnuVr4Ek9wSBQoveqY/r+LwjCcU29kNVkidwim+kYA==",
      "license": "MIT"
    },
    "node_modules/@types/q": {
      "version": "1.5.8",
      "resolved": "https://registry.npmjs.org/@types/q/-/q-1.5.8.tgz",
      "integrity": "sha512-hroOstUScF6zhIi+5+x0dzqrHA1EJi+Irri6b1fxolMTqqHIV/Cg77EtnQcZqZCu8hR3mX2BzIxN4/GzI68Kfw==",
      "license": "MIT"
    },
    "node_modules/@types/qs": {
      "version": "6.15.0",
      "resolved": "https://registry.npmjs.org/@types/qs/-/qs-6.15.0.tgz",
      "integrity": "sha512-JawvT8iBVWpzTrz3EGw9BTQFg3BQNmwERdKE22vlTxawwtbyUSlMppvZYKLZzB5zgACXdXxbD3m1bXaMqP/9ow==",
      "license": "MIT"
    },
    "node_modules/@types/range-parser": {
      "version": "1.2.7",
      "resolved": "https://registry.npmjs.org/@types/range-parser/-/range-parser-1.2.7.tgz",
      "integrity": "sha512-hKormJbkJqzQGhziax5PItDUTMAM9uE2XXQmM37dyd4hVM+5aVl7oVxMVUiVQn2oCQFN/LKCZdvSM0pFRqbSmQ==",
      "license": "MIT"
    },
    "node_modules/@types/resolve": {
      "version": "1.17.1",
      "resolved": "https://registry.npmjs.org/@types/resolve/-/resolve-1.17.1.tgz",
      "integrity": "sha512-yy7HuzQhj0dhGpD8RLXSZWEkLsV9ibvxvi6EiJ3bkqLAO1RGo0WbkWQiwpRlSFymTJRz0d3k5LM3kkx8ArDbLw==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/retry": {
      "version": "0.12.0",
      "resolved": "https://registry.npmjs.org/@types/retry/-/retry-0.12.0.tgz",
      "integrity": "sha512-wWKOClTTiizcZhXnPY4wikVAwmdYHp8q6DmC+EJUzAMsycb7HB32Kh9RN4+0gExjmPmZSAQjgURXIGATPegAvA==",
      "license": "MIT"
    },
    "node_modules/@types/semver": {
      "version": "7.7.1",
      "resolved": "https://registry.npmjs.org/@types/semver/-/semver-7.7.1.tgz",
      "integrity": "sha512-FmgJfu+MOcQ370SD0ev7EI8TlCAfKYU+B4m5T3yXc1CiRN94g/SZPtsCkk506aUDtlMnFZvasDwHHUcZUEaYuA==",
      "license": "MIT"
    },
    "node_modules/@types/send": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/@types/send/-/send-1.2.1.tgz",
      "integrity": "sha512-arsCikDvlU99zl1g69TcAB3mzZPpxgw0UQnaHeC1Nwb015xp8bknZv5rIfri9xTOcMuaVgvabfIRA7PSZVuZIQ==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/serve-index": {
      "version": "1.9.4",
      "resolved": "https://registry.npmjs.org/@types/serve-index/-/serve-index-1.9.4.tgz",
      "integrity": "sha512-qLpGZ/c2fhSs5gnYsQxtDEq3Oy8SXPClIXkW5ghvAvsNuVSA8k+gCONcUCS/UjLEYvYps+e8uBtfgXgvhwfNug==",
      "license": "MIT",
      "dependencies": {
        "@types/express": "*"
      }
    },
    "node_modules/@types/serve-static": {
      "version": "1.15.10",
      "resolved": "https://registry.npmjs.org/@types/serve-static/-/serve-static-1.15.10.tgz",
      "integrity": "sha512-tRs1dB+g8Itk72rlSI2ZrW6vZg0YrLI81iQSTkMmOqnqCaNr/8Ek4VwWcN5vZgCYWbg/JJSGBlUaYGAOP73qBw==",
      "license": "MIT",
      "dependencies": {
        "@types/http-errors": "*",
        "@types/node": "*",
        "@types/send": "<1"
      }
    },
    "node_modules/@types/serve-static/node_modules/@types/send": {
      "version": "0.17.6",
      "resolved": "https://registry.npmjs.org/@types/send/-/send-0.17.6.tgz",
      "integrity": "sha512-Uqt8rPBE8SY0RK8JB1EzVOIZ32uqy8HwdxCnoCOsYrvnswqmFZ/k+9Ikidlk/ImhsdvBsloHbAlewb2IEBV/Og==",
      "license": "MIT",
      "dependencies": {
        "@types/mime": "^1",
        "@types/node": "*"
      }
    },
    "node_modules/@types/sockjs": {
      "version": "0.3.36",
      "resolved": "https://registry.npmjs.org/@types/sockjs/-/sockjs-0.3.36.tgz",
      "integrity": "sha512-MK9V6NzAS1+Ud7JV9lJLFqW85VbC9dq3LmwZCuBe4wBDgKC0Kj/jd8Xl+nSviU+Qc3+m7umHHyHg//2KSa0a0Q==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/stack-utils": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/@types/stack-utils/-/stack-utils-2.0.3.tgz",
      "integrity": "sha512-9aEbYZ3TbYMznPdcdr3SmIrLXwC/AKZXQeCf9Pgao5CKb8CyHuEX5jzWPTkvregvhRJHcpRO6BFoGW9ycaOkYw==",
      "license": "MIT"
    },
    "node_modules/@types/trusted-types": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/@types/trusted-types/-/trusted-types-2.0.7.tgz",
      "integrity": "sha512-ScaPdn1dQczgbl0QFTeTOmVHFULt394XJgOQNoyVhZ6r2vLnMLJfBPd53SB52T/3G36VI1/g2MZaX0cwDuXsfw==",
      "license": "MIT"
    },
    "node_modules/@types/ws": {
      "version": "8.18.1",
      "resolved": "https://registry.npmjs.org/@types/ws/-/ws-8.18.1.tgz",
      "integrity": "sha512-ThVF6DCVhA8kUGy+aazFQ4kXQ7E1Ty7A3ypFOe0IcJV8O/M511G99AW24irKrW56Wt44yG9+ij8FaqoBGkuBXg==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/yargs": {
      "version": "16.0.11",
      "resolved": "https://registry.npmjs.org/@types/yargs/-/yargs-16.0.11.tgz",
      "integrity": "sha512-sbtvk8wDN+JvEdabmZExoW/HNr1cB7D/j4LT08rMiuikfA7m/JNJg7ATQcgzs34zHnoScDkY0ZRSl29Fkmk36g==",
      "license": "MIT",
      "dependencies": {
        "@types/yargs-parser": "*"
      }
    },
    "node_modules/@types/yargs-parser": {
      "version": "21.0.3",
      "resolved": "https://registry.npmjs.org/@types/yargs-parser/-/yargs-parser-21.0.3.tgz",
      "integrity": "sha512-I4q9QU9MQv4oEOz4tAHJtNz1cwuLxn2F3xcc2iV5WdqLPpUnj30aUuxt1mAxYTG+oe8CZMV/+6rU4S4gRDzqtQ==",
      "license": "MIT"
    },
    "node_modules/@typescript-eslint/eslint-plugin": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/eslint-plugin/-/eslint-plugin-5.62.0.tgz",
      "integrity": "sha512-TiZzBSJja/LbhNPvk6yc0JrX9XqhQ0hdh6M2svYfsHGejaKFIAGd9MQ+ERIMzLGlN/kZoYIgdxFV0PuljTKXag==",
      "license": "MIT",
      "dependencies": {
        "@eslint-community/regexpp": "^4.4.0",
        "@typescript-eslint/scope-manager": "5.62.0",
        "@typescript-eslint/type-utils": "5.62.0",
        "@typescript-eslint/utils": "5.62.0",
        "debug": "^4.3.4",
        "graphemer": "^1.4.0",
        "ignore": "^5.2.0",
        "natural-compare-lite": "^1.4.0",
        "semver": "^7.3.7",
        "tsutils": "^3.21.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "@typescript-eslint/parser": "^5.0.0",
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@typescript-eslint/experimental-utils": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/experimental-utils/-/experimental-utils-5.62.0.tgz",
      "integrity": "sha512-RTXpeB3eMkpoclG3ZHft6vG/Z30azNHuqY6wKPBHlVMZFuEvrtlEDe8gMqDb+SO+9hjC/pLekeSCryf9vMZlCw==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/utils": "5.62.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      }
    },
    "node_modules/@typescript-eslint/parser": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/parser/-/parser-5.62.0.tgz",
      "integrity": "sha512-VlJEV0fOQ7BExOsHYAGrgbEiZoi8D+Bl2+f6V2RrXerRSylnp+ZBHmPvaIa8cz0Ajx7WO7Z5RqfgYg7ED1nRhA==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "@typescript-eslint/scope-manager": "5.62.0",
        "@typescript-eslint/types": "5.62.0",
        "@typescript-eslint/typescript-estree": "5.62.0",
        "debug": "^4.3.4"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@typescript-eslint/scope-manager": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/scope-manager/-/scope-manager-5.62.0.tgz",
      "integrity": "sha512-VXuvVvZeQCQb5Zgf4HAxc04q5j+WrNAtNh9OwCsCgpKqESMTu3tF/jhZ3xG6T4NZwWl65Bg8KuS2uEvhSfLl0w==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/types": "5.62.0",
        "@typescript-eslint/visitor-keys": "5.62.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@typescript-eslint/type-utils": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/type-utils/-/type-utils-5.62.0.tgz",
      "integrity": "sha512-xsSQreu+VnfbqQpW5vnCJdq1Z3Q0U31qiWmRhr98ONQmcp/yhiPJFPq8MXiJVLiksmOKSjIldZzkebzHuCGzew==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/typescript-estree": "5.62.0",
        "@typescript-eslint/utils": "5.62.0",
        "debug": "^4.3.4",
        "tsutils": "^3.21.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "*"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@typescript-eslint/types": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/types/-/types-5.62.0.tgz",
      "integrity": "sha512-87NVngcbVXUahrRTqIK27gD2t5Cu1yuCXxbLcFtCzZGlfyVWWh8mLHkoxzjsB6DDNnvdL+fW8MiwPEJyGJQDgQ==",
      "license": "MIT",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@typescript-eslint/typescript-estree": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/typescript-estree/-/typescript-estree-5.62.0.tgz",
      "integrity": "sha512-CmcQ6uY7b9y694lKdRB8FEel7JbU/40iSAPomu++SjLMntB+2Leay2LO6i8VnJk58MtE9/nQSFIH6jpyRWyYzA==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "@typescript-eslint/types": "5.62.0",
        "@typescript-eslint/visitor-keys": "5.62.0",
        "debug": "^4.3.4",
        "globby": "^11.1.0",
        "is-glob": "^4.0.3",
        "semver": "^7.3.7",
        "tsutils": "^3.21.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@typescript-eslint/utils": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/utils/-/utils-5.62.0.tgz",
      "integrity": "sha512-n8oxjeb5aIbPFEtmQxQYOLI0i9n5ySBEY/ZEHHZqKQSFnxio1rv6dthascc9dLuwrL0RC5mPCxB7vnAVGAYWAQ==",
      "license": "MIT",
      "dependencies": {
        "@eslint-community/eslint-utils": "^4.2.0",
        "@types/json-schema": "^7.0.9",
        "@types/semver": "^7.3.12",
        "@typescript-eslint/scope-manager": "5.62.0",
        "@typescript-eslint/types": "5.62.0",
        "@typescript-eslint/typescript-estree": "5.62.0",
        "eslint-scope": "^5.1.1",
        "semver": "^7.3.7"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      }
    },
    "node_modules/@typescript-eslint/utils/node_modules/eslint-scope": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-5.1.1.tgz",
      "integrity": "sha512-2NxwbF/hZ0KpepYN0cNbo+FN6XoK7GaHlQhgx/hIZl6Va0bF45RQOOwhLIy8lQDbuCiadSLCBnH2CFYquit5bw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^4.1.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/@typescript-eslint/utils/node_modules/estraverse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-4.3.0.tgz",
      "integrity": "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/@typescript-eslint/visitor-keys": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/visitor-keys/-/visitor-keys-5.62.0.tgz",
      "integrity": "sha512-07ny+LHRzQXepkGg6w0mFY41fVUNBrL2Roj/++7V1txKugfjm/Ci/qSND03r2RhlJhJYMcTn9AhhSSqQp0Ysyw==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/types": "5.62.0",
        "eslint-visitor-keys": "^3.3.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@ungap/structured-clone": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/@ungap/structured-clone/-/structured-clone-1.3.0.tgz",
      "integrity": "sha512-WmoN8qaIAo7WTYWbAZuG8PYEhn5fkz7dZrqTBZ7dtt//lL2Gwms1IcnQ5yHqjDfX8Ft5j4YzDM23f87zBfDe9g==",
      "license": "ISC"
    },
    "node_modules/@webassemblyjs/ast": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/ast/-/ast-1.14.1.tgz",
      "integrity": "sha512-nuBEDgQfm1ccRp/8bCQrx1frohyufl4JlbMMZ4P1wpeOfDhF6FQkxZJ1b/e+PLwr6X1Nhw6OLme5usuBWYBvuQ==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/helper-numbers": "1.13.2",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2"
      }
    },
    "node_modules/@webassemblyjs/floating-point-hex-parser": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/floating-point-hex-parser/-/floating-point-hex-parser-1.13.2.tgz",
      "integrity": "sha512-6oXyTOzbKxGH4steLbLNOu71Oj+C8Lg34n6CqRvqfS2O71BxY6ByfMDRhBytzknj9yGUPVJ1qIKhRlAwO1AovA==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/helper-api-error": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-api-error/-/helper-api-error-1.13.2.tgz",
      "integrity": "sha512-U56GMYxy4ZQCbDZd6JuvvNV/WFildOjsaWD3Tzzvmw/mas3cXzRJPMjP83JqEsgSbyrmaGjBfDtV7KDXV9UzFQ==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/helper-buffer": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-buffer/-/helper-buffer-1.14.1.tgz",
      "integrity": "sha512-jyH7wtcHiKssDtFPRB+iQdxlDf96m0E39yb0k5uJVhFGleZFoNw1c4aeIcVUPPbXUVJ94wwnMOAqUHyzoEPVMA==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/helper-numbers": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-numbers/-/helper-numbers-1.13.2.tgz",
      "integrity": "sha512-FE8aCmS5Q6eQYcV3gI35O4J789wlQA+7JrqTTpJqn5emA4U2hvwJmvFRC0HODS+3Ye6WioDklgd6scJ3+PLnEA==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/floating-point-hex-parser": "1.13.2",
        "@webassemblyjs/helper-api-error": "1.13.2",
        "@xtuc/long": "4.2.2"
      }
    },
    "node_modules/@webassemblyjs/helper-wasm-bytecode": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-wasm-bytecode/-/helper-wasm-bytecode-1.13.2.tgz",
      "integrity": "sha512-3QbLKy93F0EAIXLh0ogEVR6rOubA9AoZ+WRYhNbFyuB70j3dRdwH9g+qXhLAO0kiYGlg3TxDV+I4rQTr/YNXkA==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/helper-wasm-section": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-wasm-section/-/helper-wasm-section-1.14.1.tgz",
      "integrity": "sha512-ds5mXEqTJ6oxRoqjhWDU83OgzAYjwsCV8Lo/N+oRsNDmx/ZDpqalmrtgOMkHwxsG0iI//3BwWAErYRHtgn0dZw==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-buffer": "1.14.1",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2",
        "@webassemblyjs/wasm-gen": "1.14.1"
      }
    },
    "node_modules/@webassemblyjs/ieee754": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/ieee754/-/ieee754-1.13.2.tgz",
      "integrity": "sha512-4LtOzh58S/5lX4ITKxnAK2USuNEvpdVV9AlgGQb8rJDHaLeHciwG4zlGr0j/SNWlr7x3vO1lDEsuePvtcDNCkw==",
      "license": "MIT",
      "dependencies": {
        "@xtuc/ieee754": "^1.2.0"
      }
    },
    "node_modules/@webassemblyjs/leb128": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/leb128/-/leb128-1.13.2.tgz",
      "integrity": "sha512-Lde1oNoIdzVzdkNEAWZ1dZ5orIbff80YPdHx20mrHwHrVNNTjNr8E3xz9BdpcGqRQbAEa+fkrCb+fRFTl/6sQw==",
      "license": "Apache-2.0",
      "dependencies": {
        "@xtuc/long": "4.2.2"
      }
    },
    "node_modules/@webassemblyjs/utf8": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/utf8/-/utf8-1.13.2.tgz",
      "integrity": "sha512-3NQWGjKTASY1xV5m7Hr0iPeXD9+RDobLll3T9d2AO+g3my8xy5peVyjSag4I50mR1bBSN/Ct12lo+R9tJk0NZQ==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/wasm-edit": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wasm-edit/-/wasm-edit-1.14.1.tgz",
      "integrity": "sha512-RNJUIQH/J8iA/1NzlE4N7KtyZNHi3w7at7hDjvRNm5rcUXa00z1vRz3glZoULfJ5mpvYhLybmVcwcjGrC1pRrQ==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-buffer": "1.14.1",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2",
        "@webassemblyjs/helper-wasm-section": "1.14.1",
        "@webassemblyjs/wasm-gen": "1.14.1",
        "@webassemblyjs/wasm-opt": "1.14.1",
        "@webassemblyjs/wasm-parser": "1.14.1",
        "@webassemblyjs/wast-printer": "1.14.1"
      }
    },
    "node_modules/@webassemblyjs/wasm-gen": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wasm-gen/-/wasm-gen-1.14.1.tgz",
      "integrity": "sha512-AmomSIjP8ZbfGQhumkNvgC33AY7qtMCXnN6bL2u2Js4gVCg8fp735aEiMSBbDR7UQIj90n4wKAFUSEd0QN2Ukg==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2",
        "@webassemblyjs/ieee754": "1.13.2",
        "@webassemblyjs/leb128": "1.13.2",
        "@webassemblyjs/utf8": "1.13.2"
      }
    },
    "node_modules/@webassemblyjs/wasm-opt": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wasm-opt/-/wasm-opt-1.14.1.tgz",
      "integrity": "sha512-PTcKLUNvBqnY2U6E5bdOQcSM+oVP/PmrDY9NzowJjislEjwP/C4an2303MCVS2Mg9d3AJpIGdUFIQQWbPds0Sw==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-buffer": "1.14.1",
        "@webassemblyjs/wasm-gen": "1.14.1",
        "@webassemblyjs/wasm-parser": "1.14.1"
      }
    },
    "node_modules/@webassemblyjs/wasm-parser": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wasm-parser/-/wasm-parser-1.14.1.tgz",
      "integrity": "sha512-JLBl+KZ0R5qB7mCnud/yyX08jWFw5MsoalJ1pQ4EdFlgj9VdXKGuENGsiCIjegI1W7p91rUlcB/LB5yRJKNTcQ==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-api-error": "1.13.2",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2",
        "@webassemblyjs/ieee754": "1.13.2",
        "@webassemblyjs/leb128": "1.13.2",
        "@webassemblyjs/utf8": "1.13.2"
      }
    },
    "node_modules/@webassemblyjs/wast-printer": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wast-printer/-/wast-printer-1.14.1.tgz",
      "integrity": "sha512-kPSSXE6De1XOR820C90RIo2ogvZG+c3KiHzqUoO/F34Y2shGzesfqv7o57xrxovZJH/MetF5UjroJ/R/3isoiw==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@xtuc/long": "4.2.2"
      }
    },
    "node_modules/@xtuc/ieee754": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/@xtuc/ieee754/-/ieee754-1.2.0.tgz",
      "integrity": "sha512-DX8nKgqcGwsc0eJSqYt5lwP4DH5FlHnmuWWBRy7X0NcaGR0ZtuyeESgMwTYVEtxmsNGY+qit4QYT/MIYTOTPeA==",
      "license": "BSD-3-Clause"
    },
    "node_modules/@xtuc/long": {
      "version": "4.2.2",
      "resolved": "https://registry.npmjs.org/@xtuc/long/-/long-4.2.2.tgz",
      "integrity": "sha512-NuHqBY1PB/D8xU6s/thBgOAiAP7HOYDQ32+BFZILJ8ivkUkAHQnWfn6WhL79Owj1qmUnoN/YPhktdIoucipkAQ==",
      "license": "Apache-2.0"
    },
    "node_modules/abab": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/abab/-/abab-2.0.6.tgz",
      "integrity": "sha512-j2afSsaIENvHZN2B8GOpF566vZ5WVk5opAiMTvWgaQT8DkbOqsTfvNAvHoRGU2zzP8cPoqys+xHTRDWW8L+/BA==",
      "deprecated": "Use your platform's native atob() and btoa() methods instead",
      "license": "BSD-3-Clause"
    },
    "node_modules/accepts": {
      "version": "1.3.8",
      "resolved": "https://registry.npmjs.org/accepts/-/accepts-1.3.8.tgz",
      "integrity": "sha512-PYAthTa2m2VKxuvSD3DPC/Gy+U+sOA1LAuT8mkmRuvw+NACSaeXEQ+NHcVF7rONl6qcaxV3Uuemwawk+7+SJLw==",
      "license": "MIT",
      "dependencies": {
        "mime-types": "~2.1.34",
        "negotiator": "0.6.3"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/accepts/node_modules/negotiator": {
      "version": "0.6.3",
      "resolved": "https://registry.npmjs.org/negotiator/-/negotiator-0.6.3.tgz",
      "integrity": "sha512-+EUsqGPLsM+j/zdChZjsnX51g4XrHFOIXwfnCVPGlQk/k5giakcKsuxCObBRu6DSm9opw/O6slWbJdghQM4bBg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/acorn": {
      "version": "8.16.0",
      "resolved": "https://registry.npmjs.org/acorn/-/acorn-8.16.0.tgz",
      "integrity": "sha512-UVJyE9MttOsBQIDKw1skb9nAwQuR5wuGD3+82K6JgJlm/Y+KI92oNsMNGZCYdDsVtRHSak0pcV5Dno5+4jh9sw==",
      "license": "MIT",
      "bin": {
        "acorn": "bin/acorn"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/acorn-globals": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/acorn-globals/-/acorn-globals-6.0.0.tgz",
      "integrity": "sha512-ZQl7LOWaF5ePqqcX4hLuv/bLXYQNfNWw2c0/yX/TsPRKamzHcTGQnlCjHT3TsmkOUVEPS3crCxiPfdzE/Trlhg==",
      "license": "MIT",
      "dependencies": {
        "acorn": "^7.1.1",
        "acorn-walk": "^7.1.1"
      }
    },
    "node_modules/acorn-globals/node_modules/acorn": {
      "version": "7.4.1",
      "resolved": "https://registry.npmjs.org/acorn/-/acorn-7.4.1.tgz",
      "integrity": "sha512-nQyp0o1/mNdbTO1PO6kHkwSrmgZ0MT/jCCpNiwbUjGoRN4dlBhqJtoQuCnEOKzgTVwg0ZWiCoQy6SxMebQVh8A==",
      "license": "MIT",
      "bin": {
        "acorn": "bin/acorn"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/acorn-import-phases": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/acorn-import-phases/-/acorn-import-phases-1.0.4.tgz",
      "integrity": "sha512-wKmbr/DDiIXzEOiWrTTUcDm24kQ2vGfZQvM2fwg2vXqR5uW6aapr7ObPtj1th32b9u90/Pf4AItvdTh42fBmVQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10.13.0"
      },
      "peerDependencies": {
        "acorn": "^8.14.0"
      }
    },
    "node_modules/acorn-jsx": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/acorn-jsx/-/acorn-jsx-5.3.2.tgz",
      "integrity": "sha512-rq9s+JNhf0IChjtDXxllJ7g41oZk5SlXtp0LHwyA5cejwn7vKmKp4pPri6YEePv2PU65sAsegbXtIinmDFDXgQ==",
      "license": "MIT",
      "peerDependencies": {
        "acorn": "^6.0.0 || ^7.0.0 || ^8.0.0"
      }
    },
    "node_modules/acorn-walk": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/acorn-walk/-/acorn-walk-7.2.0.tgz",
      "integrity": "sha512-OPdCF6GsMIP+Az+aWfAAOEt2/+iVDKE7oy6lJ098aoe59oAmK76qV6Gw60SbZ8jHuG2wH058GF4pLFbYamYrVA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/address": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/address/-/address-1.2.2.tgz",
      "integrity": "sha512-4B/qKCfeE/ODUaAUpSwfzazo5x29WD4r3vXiWsB7I2mSDAihwEqKO+g8GELZUQSSAo5e1XTYh3ZVfLyxBc12nA==",
      "license": "MIT",
      "engines": {
        "node": ">= 10.0.0"
      }
    },
    "node_modules/adjust-sourcemap-loader": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/adjust-sourcemap-loader/-/adjust-sourcemap-loader-4.0.0.tgz",
      "integrity": "sha512-OXwN5b9pCUXNQHJpwwD2qP40byEmSgzj8B4ydSN0uMNYWiFmJ6x6KwUllMmfk8Rwu/HJDFR7U8ubsWBoN0Xp0A==",
      "license": "MIT",
      "dependencies": {
        "loader-utils": "^2.0.0",
        "regex-parser": "^2.2.11"
      },
      "engines": {
        "node": ">=8.9"
      }
    },
    "node_modules/agent-base": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/agent-base/-/agent-base-6.0.2.tgz",
      "integrity": "sha512-RZNwNclF7+MS/8bDg70amg32dyeZGZxiDuQmZxKLAlQjr3jGyLx+4Kkk58UO7D2QdgFIQCovuSuZESne6RG6XQ==",
      "license": "MIT",
      "dependencies": {
        "debug": "4"
      },
      "engines": {
        "node": ">= 6.0.0"
      }
    },
    "node_modules/ajv": {
      "version": "6.14.0",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-6.14.0.tgz",
      "integrity": "sha512-IWrosm/yrn43eiKqkfkHis7QioDleaXQHdDVPKg0FSwwd/DuvyX79TZnFOnYpB7dcsFAMmtFztZuXPDvSePkFw==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.1",
        "fast-json-stable-stringify": "^2.0.0",
        "json-schema-traverse": "^0.4.1",
        "uri-js": "^4.2.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/ajv-formats": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/ajv-formats/-/ajv-formats-2.1.1.tgz",
      "integrity": "sha512-Wx0Kx52hxE7C18hkMEggYlEifqWZtYaRgouJor+WMdPnQyEK13vgEWyVNup7SoeeoLMsr4kf5h6dOW11I15MUA==",
      "license": "MIT",
      "dependencies": {
        "ajv": "^8.0.0"
      },
      "peerDependencies": {
        "ajv": "^8.0.0"
      },
      "peerDependenciesMeta": {
        "ajv": {
          "optional": true
        }
      }
    },
    "node_modules/ajv-formats/node_modules/ajv": {
      "version": "8.18.0",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-8.18.0.tgz",
      "integrity": "sha512-PlXPeEWMXMZ7sPYOHqmDyCJzcfNrUr3fGNKtezX14ykXOEIvyK81d+qydx89KY5O71FKMPaQ2vBfBFI5NHR63A==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "fast-uri": "^3.0.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/ajv-formats/node_modules/json-schema-traverse": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-1.0.0.tgz",
      "integrity": "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug==",
      "license": "MIT"
    },
    "node_modules/ajv-keywords": {
      "version": "3.5.2",
      "resolved": "https://registry.npmjs.org/ajv-keywords/-/ajv-keywords-3.5.2.tgz",
      "integrity": "sha512-5p6WTN0DdTGVQk6VjcEju19IgaHudalcfabD7yhDGeA6bcQnmL+CpveLJq/3hvfwd1aof6L386Ougkx6RfyMIQ==",
      "license": "MIT",
      "peerDependencies": {
        "ajv": "^6.9.1"
      }
    },
    "node_modules/ansi-escapes": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/ansi-escapes/-/ansi-escapes-4.3.2.tgz",
      "integrity": "sha512-gKXj5ALrKWQLsYG9jlTRmR/xKluxHV+Z9QEwNIgCfM1/uwPMCuzVVnh5mwTd+OuBZcwSIMbqssNWRm1lE51QaQ==",
      "license": "MIT",
      "dependencies": {
        "type-fest": "^0.21.3"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/ansi-escapes/node_modules/type-fest": {
      "version": "0.21.3",
      "resolved": "https://registry.npmjs.org/type-fest/-/type-fest-0.21.3.tgz",
      "integrity": "sha512-t0rzBq87m3fVcduHDUFhKmyyX+9eo6WQjZvf51Ea/M0Q7+T374Jp1aUiyUl0GKxp8M/OETVHSDvmkyPgvX+X2w==",
      "license": "(MIT OR CC0-1.0)",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/ansi-html": {
      "version": "0.0.9",
      "resolved": "https://registry.npmjs.org/ansi-html/-/ansi-html-0.0.9.tgz",
      "integrity": "sha512-ozbS3LuenHVxNRh/wdnN16QapUHzauqSomAl1jwwJRRsGwFwtj644lIhxfWu0Fy0acCij2+AEgHvjscq3dlVXg==",
      "engines": [
        "node >= 0.8.0"
      ],
      "license": "Apache-2.0",
      "bin": {
        "ansi-html": "bin/ansi-html"
      }
    },
    "node_modules/ansi-html-community": {
      "version": "0.0.8",
      "resolved": "https://registry.npmjs.org/ansi-html-community/-/ansi-html-community-0.0.8.tgz",
      "integrity": "sha512-1APHAyr3+PCamwNw3bXCPp4HFLONZt/yIH0sZp0/469KWNTEy+qN5jQ3GVX6DMZ1UXAi34yVwtTeaG/HpBuuzw==",
      "engines": [
        "node >= 0.8.0"
      ],
      "license": "Apache-2.0",
      "bin": {
        "ansi-html": "bin/ansi-html"
      }
    },
    "node_modules/ansi-regex": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-5.0.1.tgz",
      "integrity": "sha512-quJQXlTSUGL2LH9SUXo8VwsY4soanhgo6LNSm84E1LBcE8s3O0wpdiRzyR9z/ZZJMlMWv37qOOb9pdJlMUEKFQ==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/ansi-styles": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-4.3.0.tgz",
      "integrity": "sha512-zbB9rCJAT1rbjiVDb2hqKFHNYLxgtk8NURxZ3IZwD3F6NtxbXZQCnnSi1Lkx+IDohdPlFp222wVALIheZJQSEg==",
      "license": "MIT",
      "dependencies": {
        "color-convert": "^2.0.1"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/any-promise": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/any-promise/-/any-promise-1.3.0.tgz",
      "integrity": "sha512-7UvmKalWRt1wgjL1RrGxoSJW/0QZFIegpeGvZG9kjp8vrRu55XTHbwnqq2GpXm9uLbcuhxm3IqX9OB4MZR1b2A==",
      "license": "MIT"
    },
    "node_modules/anymatch": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/anymatch/-/anymatch-3.1.3.tgz",
      "integrity": "sha512-KMReFUr0B4t+D+OBkjR3KYqvocp2XaSzO55UcB6mgQMd3KbcE+mWTyvVV7D/zsdEbNnV6acZUutkiHQXvTr1Rw==",
      "license": "ISC",
      "dependencies": {
        "normalize-path": "^3.0.0",
        "picomatch": "^2.0.4"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/arg": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/arg/-/arg-5.0.2.tgz",
      "integrity": "sha512-PYjyFOLKQ9y57JvQ6QLo8dAgNqswh8M1RMJYdQduT6xbWSgK36P/Z/v+p888pM69jMMfS8Xd8F6I1kQ/I9HUGg==",
      "license": "MIT"
    },
    "node_modules/argparse": {
      "version": "1.0.10",
      "resolved": "https://registry.npmjs.org/argparse/-/argparse-1.0.10.tgz",
      "integrity": "sha512-o5Roy6tNG4SL/FOkCAN6RzjiakZS25RLYFrcMttJqbdd8BWrnA+fGz57iN5Pb06pvBGvl5gQ0B48dJlslXvoTg==",
      "license": "MIT",
      "dependencies": {
        "sprintf-js": "~1.0.2"
      }
    },
    "node_modules/aria-query": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/aria-query/-/aria-query-5.3.2.tgz",
      "integrity": "sha512-COROpnaoap1E2F000S62r6A60uHZnmlvomhfyT2DlTcrY1OrBKn2UhH7qn5wTC9zMvD0AY7csdPSNwKP+7WiQw==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/array-buffer-byte-length": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/array-buffer-byte-length/-/array-buffer-byte-length-1.0.2.tgz",
      "integrity": "sha512-LHE+8BuR7RYGDKvnrmcuSq3tDcKv9OFEXQt/HpbZhY7V6h0zlUXutnAD82GiFx9rdieCMjkvtcsPqBwgUl1Iiw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "is-array-buffer": "^3.0.5"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array-flatten": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/array-flatten/-/array-flatten-1.1.1.tgz",
      "integrity": "sha512-PCVAQswWemu6UdxsDFFX/+gVeYqKAod3D3UVm91jHwynguOwAvYPhx8nNlM++NqRcK6CxxpUafjmhIdKiHibqg==",
      "license": "MIT"
    },
    "node_modules/array-includes": {
      "version": "3.1.9",
      "resolved": "https://registry.npmjs.org/array-includes/-/array-includes-3.1.9.tgz",
      "integrity": "sha512-FmeCCAenzH0KH381SPT5FZmiA/TmpndpcaShhfgEN9eCVjnFBqq3l1xrI42y8+PPLI6hypzou4GXw00WHmPBLQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.24.0",
        "es-object-atoms": "^1.1.1",
        "get-intrinsic": "^1.3.0",
        "is-string": "^1.1.1",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array-union": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/array-union/-/array-union-2.1.0.tgz",
      "integrity": "sha512-HGyxoOTYUyCM6stUe6EJgnd4EoewAI7zMdfqO+kGjnlZmBDz/cR5pf8r/cR4Wq60sL/p0IkcjUEEPwS3GFrIyw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/array.prototype.findlast": {
      "version": "1.2.5",
      "resolved": "https://registry.npmjs.org/array.prototype.findlast/-/array.prototype.findlast-1.2.5.tgz",
      "integrity": "sha512-CVvd6FHg1Z3POpBLxO6E6zr+rSKEQ9L6rZHAaY7lLfhKsWYUBBOuMs0e9o24oopj6H+geRCX0YJ+TJLBK2eHyQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.findlastindex": {
      "version": "1.2.6",
      "resolved": "https://registry.npmjs.org/array.prototype.findlastindex/-/array.prototype.findlastindex-1.2.6.tgz",
      "integrity": "sha512-F/TKATkzseUExPlfvmwQKGITM3DGTK+vkAsCZoDc5daVygbJBnjEUCbgkAvVFsgfXfX4YIqZ/27G3k3tdXrTxQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "es-shim-unscopables": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.flat": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/array.prototype.flat/-/array.prototype.flat-1.3.3.tgz",
      "integrity": "sha512-rwG/ja1neyLqCuGZ5YYrznA62D4mZXg0i1cIskIUKSiqF3Cje9/wXAls9B9s1Wa2fomMsIv8czB8jZcPmxCXFg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.flatmap": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/array.prototype.flatmap/-/array.prototype.flatmap-1.3.3.tgz",
      "integrity": "sha512-Y7Wt51eKJSyi80hFrJCePGGNo5ktJCslFuboqJsbf57CCPcm5zztluPlc4/aD8sWsKvlwatezpV4U1efk8kpjg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.reduce": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/array.prototype.reduce/-/array.prototype.reduce-1.0.8.tgz",
      "integrity": "sha512-DwuEqgXFBwbmZSRqt3BpQigWNUoqw9Ml2dTWdF3B2zQlQX4OeUE0zyuzX0fX0IbTvjdkZbcBTU3idgpO78qkTw==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-array-method-boxes-properly": "^1.0.0",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "is-string": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.tosorted": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/array.prototype.tosorted/-/array.prototype.tosorted-1.1.4.tgz",
      "integrity": "sha512-p6Fx8B7b7ZhL/gmUsAy0D15WhvDccw3mnGNbZpi3pmeJdxtWsj2jEaI4Y6oo3XiHfzuSgPwKc04MYt6KgvC/wA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.3",
        "es-errors": "^1.3.0",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/arraybuffer.prototype.slice": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/arraybuffer.prototype.slice/-/arraybuffer.prototype.slice-1.0.4.tgz",
      "integrity": "sha512-BNoCY6SXXPQ7gF2opIP4GBE+Xw7U+pHMYKuzjgCN3GwiaIR09UUeKfheyIry77QtrCBlC0KK0q5/TER/tYh3PQ==",
      "license": "MIT",
      "dependencies": {
        "array-buffer-byte-length": "^1.0.1",
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "is-array-buffer": "^3.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/asap": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/asap/-/asap-2.0.6.tgz",
      "integrity": "sha512-BSHWgDSAiKs50o2Re8ppvp3seVHXSRM44cdSsT9FfNEUUZLOGWVCsiWaRPWM1Znn+mqZ1OfVZ3z3DWEzSp7hRA==",
      "license": "MIT"
    },
    "node_modules/ast-types-flow": {
      "version": "0.0.8",
      "resolved": "https://registry.npmjs.org/ast-types-flow/-/ast-types-flow-0.0.8.tgz",
      "integrity": "sha512-OH/2E5Fg20h2aPrbe+QL8JZQFko0YZaF+j4mnQ7BGhfavO7OpSLa8a0y9sBwomHdSbkhTS8TQNayBfnW5DwbvQ==",
      "license": "MIT"
    },
    "node_modules/async": {
      "version": "3.2.6",
      "resolved": "https://registry.npmjs.org/async/-/async-3.2.6.tgz",
      "integrity": "sha512-htCUDlxyyCLMgaM3xXg0C0LW2xqfuQ6p05pCEIsXuyQ+a1koYKTuBMzRNwmybfLgvJDMd0r1LTn4+E0Ti6C2AA==",
      "license": "MIT"
    },
    "node_modules/async-function": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/async-function/-/async-function-1.0.0.tgz",
      "integrity": "sha512-hsU18Ae8CDTR6Kgu9DYf0EbCr/a5iGL0rytQDobUcdpYOKokk8LEjVphnXkDkgpi0wYVsqrXuP0bZxJaTqdgoA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/asynckit": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/asynckit/-/asynckit-0.4.0.tgz",
      "integrity": "sha512-Oei9OH4tRh0YqU3GxhX79dM/mwVgvbZJaSNaRk+bshkj0S5cfHcgYakreBjrHwatXKbz+IoIdYLxrKim2MjW0Q==",
      "license": "MIT"
    },
    "node_modules/at-least-node": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/at-least-node/-/at-least-node-1.0.0.tgz",
      "integrity": "sha512-+q/t7Ekv1EDY2l6Gda6LLiX14rU9TV20Wa3ofeQmwPFZbOMo9DXrLbOjFaaclkXKWidIaopwAObQDqwWtGUjqg==",
      "license": "ISC",
      "engines": {
        "node": ">= 4.0.0"
      }
    },
    "node_modules/autoprefixer": {
      "version": "10.4.27",
      "resolved": "https://registry.npmjs.org/autoprefixer/-/autoprefixer-10.4.27.tgz",
      "integrity": "sha512-NP9APE+tO+LuJGn7/9+cohklunJsXWiaWEfV3si4Gi/XHDwVNgkwr1J3RQYFIvPy76GmJ9/bW8vyoU1LcxwKHA==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/autoprefixer"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.28.1",
        "caniuse-lite": "^1.0.30001774",
        "fraction.js": "^5.3.4",
        "picocolors": "^1.1.1",
        "postcss-value-parser": "^4.2.0"
      },
      "bin": {
        "autoprefixer": "bin/autoprefixer"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/available-typed-arrays": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/available-typed-arrays/-/available-typed-arrays-1.0.7.tgz",
      "integrity": "sha512-wvUjBtSGN7+7SjNpq/9M2Tg350UZD3q62IFZLbRAR1bSMlCo1ZaeW+BJ+D090e4hIIZLBcTDWe4Mh4jvUDajzQ==",
      "license": "MIT",
      "dependencies": {
        "possible-typed-array-names": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/axe-core": {
      "version": "4.11.1",
      "resolved": "https://registry.npmjs.org/axe-core/-/axe-core-4.11.1.tgz",
      "integrity": "sha512-BASOg+YwO2C+346x3LZOeoovTIoTrRqEsqMa6fmfAV0P+U9mFr9NsyOEpiYvFjbc64NMrSswhV50WdXzdb/Z5A==",
      "license": "MPL-2.0",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/axobject-query": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/axobject-query/-/axobject-query-4.1.0.tgz",
      "integrity": "sha512-qIj0G9wZbMGNLjLmg1PT6v2mE9AH2zlnADJD/2tC6E00hgmhUOfEB6greHPAfLRSufHqROIUTkw6E+M3lH0PTQ==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/babel-jest": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/babel-jest/-/babel-jest-27.5.1.tgz",
      "integrity": "sha512-cdQ5dXjGRd0IBRATiQ4mZGlGlRE8kJpjPOixdNRdT+m3UcNqmYWN6rK6nvtXYfY3D76cb8s/O1Ss8ea24PIwcg==",
      "license": "MIT",
      "dependencies": {
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/babel__core": "^7.1.14",
        "babel-plugin-istanbul": "^6.1.1",
        "babel-preset-jest": "^27.5.1",
        "chalk": "^4.0.0",
        "graceful-fs": "^4.2.9",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.8.0"
      }
    },
    "node_modules/babel-loader": {
      "version": "8.4.1",
      "resolved": "https://registry.npmjs.org/babel-loader/-/babel-loader-8.4.1.tgz",
      "integrity": "sha512-nXzRChX+Z1GoE6yWavBQg6jDslyFF3SDjl2paADuoQtQW10JqShJt62R6eJQ5m/pjJFDT8xgKIWSP85OY8eXeA==",
      "license": "MIT",
      "dependencies": {
        "find-cache-dir": "^3.3.1",
        "loader-utils": "^2.0.4",
        "make-dir": "^3.1.0",
        "schema-utils": "^2.6.5"
      },
      "engines": {
        "node": ">= 8.9"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0",
        "webpack": ">=2"
      }
    },
    "node_modules/babel-loader/node_modules/schema-utils": {
      "version": "2.7.1",
      "resolved": "https://registry.npmjs.org/schema-utils/-/schema-utils-2.7.1.tgz",
      "integrity": "sha512-SHiNtMOUGWBQJwzISiVYKu82GiV4QYGePp3odlY1tuKO7gPtphAT5R/py0fA6xtbgLL/RvtJZnU9b8s0F1q0Xg==",
      "license": "MIT",
      "dependencies": {
        "@types/json-schema": "^7.0.5",
        "ajv": "^6.12.4",
        "ajv-keywords": "^3.5.2"
      },
      "engines": {
        "node": ">= 8.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/babel-plugin-istanbul": {
      "version": "6.1.1",
      "resolved": "https://registry.npmjs.org/babel-plugin-istanbul/-/babel-plugin-istanbul-6.1.1.tgz",
      "integrity": "sha512-Y1IQok9821cC9onCx5otgFfRm7Lm+I+wwxOx738M/WLPZ9Q42m4IG5W0FNX8WLL2gYMZo3JkuXIH2DOpWM+qwA==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.0.0",
        "@istanbuljs/load-nyc-config": "^1.0.0",
        "@istanbuljs/schema": "^0.1.2",
        "istanbul-lib-instrument": "^5.0.4",
        "test-exclude": "^6.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/babel-plugin-jest-hoist": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/babel-plugin-jest-hoist/-/babel-plugin-jest-hoist-27.5.1.tgz",
      "integrity": "sha512-50wCwD5EMNW4aRpOwtqzyZHIewTYNxLA4nhB+09d8BIssfNfzBRhkBIHiaPv1Si226TQSvp8gxAJm2iY2qs2hQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.3.3",
        "@babel/types": "^7.3.3",
        "@types/babel__core": "^7.0.0",
        "@types/babel__traverse": "^7.0.6"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/babel-plugin-macros": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/babel-plugin-macros/-/babel-plugin-macros-3.1.0.tgz",
      "integrity": "sha512-Cg7TFGpIr01vOQNODXOOaGz2NpCU5gl8x1qJFbb6hbZxR7XrcE2vtbAsTAbJ7/xwJtUuJEw8K8Zr/AE0LHlesg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.12.5",
        "cosmiconfig": "^7.0.0",
        "resolve": "^1.19.0"
      },
      "engines": {
        "node": ">=10",
        "npm": ">=6"
      }
    },
    "node_modules/babel-plugin-named-asset-import": {
      "version": "0.3.8",
      "resolved": "https://registry.npmjs.org/babel-plugin-named-asset-import/-/babel-plugin-named-asset-import-0.3.8.tgz",
      "integrity": "sha512-WXiAc++qo7XcJ1ZnTYGtLxmBCVbddAml3CEXgWaBzNzLNoxtQ8AiGEFDMOhot9XjTCQbvP5E77Fj9Gk924f00Q==",
      "license": "MIT",
      "peerDependencies": {
        "@babel/core": "^7.1.0"
      }
    },
    "node_modules/babel-plugin-polyfill-corejs2": {
      "version": "0.4.16",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-corejs2/-/babel-plugin-polyfill-corejs2-0.4.16.tgz",
      "integrity": "sha512-xaVwwSfebXf0ooE11BJovZYKhFjIvQo7TsyVpETuIeH2JHv0k/T6Y5j22pPTvqYqmpkxdlPAJlyJ0tfOJAoMxw==",
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.28.6",
        "@babel/helper-define-polyfill-provider": "^0.6.7",
        "semver": "^6.3.1"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/babel-plugin-polyfill-corejs2/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/babel-plugin-polyfill-corejs3": {
      "version": "0.14.1",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-corejs3/-/babel-plugin-polyfill-corejs3-0.14.1.tgz",
      "integrity": "sha512-ENp89vM9Pw4kv/koBb5N2f9bDZsR0hpf3BdPMOg/pkS3pwO4dzNnQZVXtBbeyAadgm865DmQG2jMMLqmZXvuCw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-define-polyfill-provider": "^0.6.7",
        "core-js-compat": "^3.48.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/babel-plugin-polyfill-regenerator": {
      "version": "0.6.7",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-regenerator/-/babel-plugin-polyfill-regenerator-0.6.7.tgz",
      "integrity": "sha512-OTYbUlSwXhNgr4g6efMZgsO8//jA61P7ZbRX3iTT53VON8l+WQS8IAUEVo4a4cWknrg2W8Cj4gQhRYNCJ8GkAA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-define-polyfill-provider": "^0.6.7"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/babel-plugin-transform-react-remove-prop-types": {
      "version": "0.4.24",
      "resolved": "https://registry.npmjs.org/babel-plugin-transform-react-remove-prop-types/-/babel-plugin-transform-react-remove-prop-types-0.4.24.tgz",
      "integrity": "sha512-eqj0hVcJUR57/Ug2zE1Yswsw4LhuqqHhD+8v120T1cl3kjg76QwtyBrdIk4WVwK+lAhBJVYCd/v+4nc4y+8JsA==",
      "license": "MIT"
    },
    "node_modules/babel-preset-current-node-syntax": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/babel-preset-current-node-syntax/-/babel-preset-current-node-syntax-1.2.0.tgz",
      "integrity": "sha512-E/VlAEzRrsLEb2+dv8yp3bo4scof3l9nR4lrld+Iy5NyVqgVYUJnDAmunkhPMisRI32Qc4iRiz425d8vM++2fg==",
      "license": "MIT",
      "dependencies": {
        "@babel/plugin-syntax-async-generators": "^7.8.4",
        "@babel/plugin-syntax-bigint": "^7.8.3",
        "@babel/plugin-syntax-class-properties": "^7.12.13",
        "@babel/plugin-syntax-class-static-block": "^7.14.5",
        "@babel/plugin-syntax-import-attributes": "^7.24.7",
        "@babel/plugin-syntax-import-meta": "^7.10.4",
        "@babel/plugin-syntax-json-strings": "^7.8.3",
        "@babel/plugin-syntax-logical-assignment-operators": "^7.10.4",
        "@babel/plugin-syntax-nullish-coalescing-operator": "^7.8.3",
        "@babel/plugin-syntax-numeric-separator": "^7.10.4",
        "@babel/plugin-syntax-object-rest-spread": "^7.8.3",
        "@babel/plugin-syntax-optional-catch-binding": "^7.8.3",
        "@babel/plugin-syntax-optional-chaining": "^7.8.3",
        "@babel/plugin-syntax-private-property-in-object": "^7.14.5",
        "@babel/plugin-syntax-top-level-await": "^7.14.5"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0 || ^8.0.0-0"
      }
    },
    "node_modules/babel-preset-jest": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/babel-preset-jest/-/babel-preset-jest-27.5.1.tgz",
      "integrity": "sha512-Nptf2FzlPCWYuJg41HBqXVT8ym6bXOevuCTbhxlUpjwtysGaIWFvDEjp4y+G7fl13FgOdjs7P/DmErqH7da0Ag==",
      "license": "MIT",
      "dependencies": {
        "babel-plugin-jest-hoist": "^27.5.1",
        "babel-preset-current-node-syntax": "^1.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/babel-preset-react-app": {
      "version": "10.1.0",
      "resolved": "https://registry.npmjs.org/babel-preset-react-app/-/babel-preset-react-app-10.1.0.tgz",
      "integrity": "sha512-f9B1xMdnkCIqe+2dHrJsoQFRz7reChaAHE/65SdaykPklQqhme2WaC08oD3is77x9ff98/9EazAKFDZv5rFEQg==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.16.0",
        "@babel/plugin-proposal-class-properties": "^7.16.0",
        "@babel/plugin-proposal-decorators": "^7.16.4",
        "@babel/plugin-proposal-nullish-coalescing-operator": "^7.16.0",
        "@babel/plugin-proposal-numeric-separator": "^7.16.0",
        "@babel/plugin-proposal-optional-chaining": "^7.16.0",
        "@babel/plugin-proposal-private-methods": "^7.16.0",
        "@babel/plugin-proposal-private-property-in-object": "^7.16.7",
        "@babel/plugin-transform-flow-strip-types": "^7.16.0",
        "@babel/plugin-transform-react-display-name": "^7.16.0",
        "@babel/plugin-transform-runtime": "^7.16.4",
        "@babel/preset-env": "^7.16.4",
        "@babel/preset-react": "^7.16.0",
        "@babel/preset-typescript": "^7.16.0",
        "@babel/runtime": "^7.16.3",
        "babel-plugin-macros": "^3.1.0",
        "babel-plugin-transform-react-remove-prop-types": "^0.4.24"
      }
    },
    "node_modules/babel-preset-react-app/node_modules/@babel/plugin-proposal-private-property-in-object": {
      "version": "7.21.11",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-private-property-in-object/-/plugin-proposal-private-property-in-object-7.21.11.tgz",
      "integrity": "sha512-0QZ8qP/3RLDVBwBFoWAwCtgcDZJVwA5LUJRZU8x2YFfKNuFq161wK3cuGrALu5yiPu+vzwTAg/sMWVNeWeNyaw==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-property-in-object instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.18.6",
        "@babel/helper-create-class-features-plugin": "^7.21.0",
        "@babel/helper-plugin-utils": "^7.20.2",
        "@babel/plugin-syntax-private-property-in-object": "^7.14.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/balanced-match": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/balanced-match/-/balanced-match-1.0.2.tgz",
      "integrity": "sha512-3oSeUO0TMV67hN1AmbXsK4yaqU7tjiHlbxRDZOpH0KW9+CeX4bRAaX0Anxt0tx2MrpRpWwQaPwIlISEJhYU5Pw==",
      "license": "MIT"
    },
    "node_modules/baseline-browser-mapping": {
      "version": "2.10.0",
      "resolved": "https://registry.npmjs.org/baseline-browser-mapping/-/baseline-browser-mapping-2.10.0.tgz",
      "integrity": "sha512-lIyg0szRfYbiy67j9KN8IyeD7q7hcmqnJ1ddWmNt19ItGpNN64mnllmxUNFIOdOm6by97jlL6wfpTTJrmnjWAA==",
      "license": "Apache-2.0",
      "bin": {
        "baseline-browser-mapping": "dist/cli.cjs"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/batch": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/batch/-/batch-0.6.1.tgz",
      "integrity": "sha512-x+VAiMRL6UPkx+kudNvxTl6hB2XNNCG2r+7wixVfIYwu/2HKRXimwQyaumLjMveWvT2Hkd/cAJw+QBMfJ/EKVw==",
      "license": "MIT"
    },
    "node_modules/bfj": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/bfj/-/bfj-7.1.0.tgz",
      "integrity": "sha512-I6MMLkn+anzNdCUp9hMRyui1HaNEUCco50lxbvNS4+EyXg8lN3nJ48PjPWtbH8UVS9CuMoaKE9U2V3l29DaRQw==",
      "license": "MIT",
      "dependencies": {
        "bluebird": "^3.7.2",
        "check-types": "^11.2.3",
        "hoopy": "^0.1.4",
        "jsonpath": "^1.1.1",
        "tryer": "^1.0.1"
      },
      "engines": {
        "node": ">= 8.0.0"
      }
    },
    "node_modules/big.js": {
      "version": "5.2.2",
      "resolved": "https://registry.npmjs.org/big.js/-/big.js-5.2.2.tgz",
      "integrity": "sha512-vyL2OymJxmarO8gxMr0mhChsO9QGwhynfuu4+MHTAW6czfq9humCB7rKpUjDd9YUiDPU4mzpyupFSvOClAwbmQ==",
      "license": "MIT",
      "engines": {
        "node": "*"
      }
    },
    "node_modules/binary-extensions": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/binary-extensions/-/binary-extensions-2.3.0.tgz",
      "integrity": "sha512-Ceh+7ox5qe7LJuLHoY0feh3pHuUDHAcRUeyL2VYghZwfpkNIy/+8Ocg0a3UuSoYzavmylwuLWQOf3hl0jjMMIw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/bluebird": {
      "version": "3.7.2",
      "resolved": "https://registry.npmjs.org/bluebird/-/bluebird-3.7.2.tgz",
      "integrity": "sha512-XpNj6GDQzdfW+r2Wnn7xiSAd7TM3jzkxGXBGTtWKuSXv1xUV+azxAm8jdWZN06QTQk+2N2XB9jRDkvbmQmcRtg==",
      "license": "MIT"
    },
    "node_modules/body-parser": {
      "version": "1.20.4",
      "resolved": "https://registry.npmjs.org/body-parser/-/body-parser-1.20.4.tgz",
      "integrity": "sha512-ZTgYYLMOXY9qKU/57FAo8F+HA2dGX7bqGc71txDRC1rS4frdFI5R7NhluHxH6M0YItAP0sHB4uqAOcYKxO6uGA==",
      "license": "MIT",
      "dependencies": {
        "bytes": "~3.1.2",
        "content-type": "~1.0.5",
        "debug": "2.6.9",
        "depd": "2.0.0",
        "destroy": "~1.2.0",
        "http-errors": "~2.0.1",
        "iconv-lite": "~0.4.24",
        "on-finished": "~2.4.1",
        "qs": "~6.14.0",
        "raw-body": "~2.5.3",
        "type-is": "~1.6.18",
        "unpipe": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.8",
        "npm": "1.2.8000 || >= 1.4.16"
      }
    },
    "node_modules/body-parser/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/body-parser/node_modules/iconv-lite": {
      "version": "0.4.24",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.4.24.tgz",
      "integrity": "sha512-v3MXnZAcvnywkTUEZomIActle7RXXeedOR31wwl7VlyoXO4Qi9arvSenNQWne1TcRwhCL1HwLI21bEqdpj8/rA==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/body-parser/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/bonjour-service": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/bonjour-service/-/bonjour-service-1.3.0.tgz",
      "integrity": "sha512-3YuAUiSkWykd+2Azjgyxei8OWf8thdn8AITIog2M4UICzoqfjlqr64WIjEXZllf/W6vK1goqleSR6brGomxQqA==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "multicast-dns": "^7.2.5"
      }
    },
    "node_modules/boolbase": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/boolbase/-/boolbase-1.0.0.tgz",
      "integrity": "sha512-JZOSA7Mo9sNGB8+UjSgzdLtokWAky1zbztM3WRLCbZ70/3cTANmQmOdR7y2g+J0e2WXywy1yS468tY+IruqEww==",
      "license": "ISC"
    },
    "node_modules/brace-expansion": {
      "version": "1.1.12",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.12.tgz",
      "integrity": "sha512-9T9UjW3r0UW5c1Q7GTwllptXwhvYmEzFhzMfZ9H7FQWt+uZePjZPjBP/W1ZEyZ1twGWom5/56TF4lPcqjnDHcg==",
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^1.0.0",
        "concat-map": "0.0.1"
      }
    },
    "node_modules/braces": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/braces/-/braces-3.0.3.tgz",
      "integrity": "sha512-yQbXgO/OSZVD2IsiLlro+7Hf6Q18EJrKSEsdoMzKePKXct3gvD8oLcOQdIzGupr5Fj+EDe8gO/lxc1BzfMpxvA==",
      "license": "MIT",
      "dependencies": {
        "fill-range": "^7.1.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/browser-process-hrtime": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/browser-process-hrtime/-/browser-process-hrtime-1.0.0.tgz",
      "integrity": "sha512-9o5UecI3GhkpM6DrXr69PblIuWxPKk9Y0jHBRhdocZ2y7YECBFCsHm79Pr3OyR2AvjhDkabFJaDJMYRazHgsow==",
      "license": "BSD-2-Clause"
    },
    "node_modules/browserslist": {
      "version": "4.28.1",
      "resolved": "https://registry.npmjs.org/browserslist/-/browserslist-4.28.1.tgz",
      "integrity": "sha512-ZC5Bd0LgJXgwGqUknZY/vkUQ04r8NXnJZ3yYi4vDmSiZmC/pdSN0NbNRPxZpbtO4uAfDUAFffO8IZoM3Gj8IkA==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "baseline-browser-mapping": "^2.9.0",
        "caniuse-lite": "^1.0.30001759",
        "electron-to-chromium": "^1.5.263",
        "node-releases": "^2.0.27",
        "update-browserslist-db": "^1.2.0"
      },
      "bin": {
        "browserslist": "cli.js"
      },
      "engines": {
        "node": "^6 || ^7 || ^8 || ^9 || ^10 || ^11 || ^12 || >=13.7"
      }
    },
    "node_modules/bser": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/bser/-/bser-2.1.1.tgz",
      "integrity": "sha512-gQxTNE/GAfIIrmHLUE3oJyp5FO6HRBfhjnw4/wMmA63ZGDJnWBmgY/lyQBpnDUkGmAhbSe39tx2d/iTOAfglwQ==",
      "license": "Apache-2.0",
      "dependencies": {
        "node-int64": "^0.4.0"
      }
    },
    "node_modules/buffer-from": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/buffer-from/-/buffer-from-1.1.2.tgz",
      "integrity": "sha512-E+XQCRwSbaaiChtv6k6Dwgc+bx+Bs6vuKJHHl5kox/BaKbhiXzqQOwK4cO22yElGp2OCmjwVhT3HmxgyPGnJfQ==",
      "license": "MIT"
    },
    "node_modules/builtin-modules": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/builtin-modules/-/builtin-modules-3.3.0.tgz",
      "integrity": "sha512-zhaCDicdLuWN5UbN5IMnFqNMhNfo919sH85y2/ea+5Yg9TsTkeZxpL+JLbp6cgYFS4sRLp3YV4S6yDuqVWHYOw==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/bytes": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/bytes/-/bytes-3.1.2.tgz",
      "integrity": "sha512-/Nf7TyzTx6S3yRJObOAV7956r8cr2+Oj8AC5dt8wSP3BQAoeX58NoHyCU8P8zGkNXStjTSi6fzO6F0pBdcYbEg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/call-bind": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/call-bind/-/call-bind-1.0.8.tgz",
      "integrity": "sha512-oKlSFMcMwpUg2ednkhQ454wfWiU/ul3CkJe/PEHcTKuiX6RpbehUiFMXu13HalGZxfUwCQzZG747YXBn1im9ww==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.0",
        "es-define-property": "^1.0.0",
        "get-intrinsic": "^1.2.4",
        "set-function-length": "^1.2.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/call-bind-apply-helpers": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/call-bind-apply-helpers/-/call-bind-apply-helpers-1.0.2.tgz",
      "integrity": "sha512-Sp1ablJ0ivDkSzjcaJdxEunN5/XvksFJ2sMBFfq6x0ryhQV/2b/KwFe21cMpmHtPOSij8K99/wSfoEuTObmuMQ==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/call-bound": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/call-bound/-/call-bound-1.0.4.tgz",
      "integrity": "sha512-+ys997U96po4Kx/ABpBCqhA9EuxJaQWDQg7295H4hBphv3IZg0boBKuwYpt4YXp6MZ5AmZQnU/tyMTlRpaSejg==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "get-intrinsic": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/callsites": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/callsites/-/callsites-3.1.0.tgz",
      "integrity": "sha512-P8BjAsXvZS+VIDUI11hHCQEv74YT67YUi5JJFNWIqL235sBmjX4+qx9Muvls5ivyNENctx46xQLQ3aTuE7ssaQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/camel-case": {
      "version": "4.1.2",
      "resolved": "https://registry.npmjs.org/camel-case/-/camel-case-4.1.2.tgz",
      "integrity": "sha512-gxGWBrTT1JuMx6R+o5PTXMmUnhnVzLQ9SNutD4YqKtI6ap897t3tKECYla6gCWEkplXnlNybEkZg9GEGxKFCgw==",
      "license": "MIT",
      "dependencies": {
        "pascal-case": "^3.1.2",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/camelcase": {
      "version": "6.3.0",
      "resolved": "https://registry.npmjs.org/camelcase/-/camelcase-6.3.0.tgz",
      "integrity": "sha512-Gmy6FhYlCY7uOElZUSbxo2UCDH8owEk996gkbrpsgGtrJLM3J7jGxl9Ic7Qwwj4ivOE5AWZWRMecDdF7hqGjFA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/camelcase-css": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/camelcase-css/-/camelcase-css-2.0.1.tgz",
      "integrity": "sha512-QOSvevhslijgYwRx6Rv7zKdMF8lbRmx+uQGx2+vDc+KI/eBnsy9kit5aj23AgGu3pa4t9AgwbnXWqS+iOY+2aA==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/caniuse-api": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/caniuse-api/-/caniuse-api-3.0.0.tgz",
      "integrity": "sha512-bsTwuIg/BZZK/vreVTYYbSWoe2F+71P7K5QGEX+pT250DZbfU1MQ5prOKpPR+LL6uWKK3KMwMCAS74QB3Um1uw==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.0.0",
        "caniuse-lite": "^1.0.0",
        "lodash.memoize": "^4.1.2",
        "lodash.uniq": "^4.5.0"
      }
    },
    "node_modules/caniuse-lite": {
      "version": "1.0.30001777",
      "resolved": "https://registry.npmjs.org/caniuse-lite/-/caniuse-lite-1.0.30001777.tgz",
      "integrity": "sha512-tmN+fJxroPndC74efCdp12j+0rk0RHwV5Jwa1zWaFVyw2ZxAuPeG8ZgWC3Wz7uSjT3qMRQ5XHZ4COgQmsCMJAQ==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/caniuse-lite"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "CC-BY-4.0"
    },
    "node_modules/case-sensitive-paths-webpack-plugin": {
      "version": "2.4.0",
      "resolved": "https://registry.npmjs.org/case-sensitive-paths-webpack-plugin/-/case-sensitive-paths-webpack-plugin-2.4.0.tgz",
      "integrity": "sha512-roIFONhcxog0JSSWbvVAh3OocukmSgpqOH6YpMkCvav/ySIV3JKg4Dc8vYtQjYi/UxpNE36r/9v+VqTQqgkYmw==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/chalk": {
      "version": "4.1.2",
      "resolved": "https://registry.npmjs.org/chalk/-/chalk-4.1.2.tgz",
      "integrity": "sha512-oKnbhFyRIXpUuez8iBMmyEa4nbj4IOQyuhc/wy9kY7/WVPcwIO9VA668Pu8RkO7+0G76SLROeyw9CpQ061i4mA==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^4.1.0",
        "supports-color": "^7.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/chalk?sponsor=1"
      }
    },
    "node_modules/char-regex": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/char-regex/-/char-regex-1.0.2.tgz",
      "integrity": "sha512-kWWXztvZ5SBQV+eRgKFeh8q5sLuZY2+8WUIzlxWVTg+oGwY14qylx1KbKzHd8P6ZYkAg0xyIDU9JMHhyJMZ1jw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/check-types": {
      "version": "11.2.3",
      "resolved": "https://registry.npmjs.org/check-types/-/check-types-11.2.3.tgz",
      "integrity": "sha512-+67P1GkJRaxQD6PKK0Et9DhwQB+vGg3PM5+aavopCpZT1lj9jeqfvpgTLAWErNj8qApkkmXlu/Ug74kmhagkXg==",
      "license": "MIT"
    },
    "node_modules/chokidar": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/chokidar/-/chokidar-3.6.0.tgz",
      "integrity": "sha512-7VT13fmjotKpGipCW9JEQAusEPE+Ei8nl6/g4FBAmIm0GOOLMua9NDDo/DWp0ZAxCr3cPq5ZpBqmPAQgDda2Pw==",
      "license": "MIT",
      "dependencies": {
        "anymatch": "~3.1.2",
        "braces": "~3.0.2",
        "glob-parent": "~5.1.2",
        "is-binary-path": "~2.1.0",
        "is-glob": "~4.0.1",
        "normalize-path": "~3.0.0",
        "readdirp": "~3.6.0"
      },
      "engines": {
        "node": ">= 8.10.0"
      },
      "funding": {
        "url": "https://paulmillr.com/funding/"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/chokidar/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/chrome-trace-event": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/chrome-trace-event/-/chrome-trace-event-1.0.4.tgz",
      "integrity": "sha512-rNjApaLzuwaOTjCiT8lSDdGN1APCiqkChLMJxJPWLunPAt5fy8xgU9/jNOchV84wfIxrA0lRQB7oCT8jrn/wrQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6.0"
      }
    },
    "node_modules/ci-info": {
      "version": "3.9.0",
      "resolved": "https://registry.npmjs.org/ci-info/-/ci-info-3.9.0.tgz",
      "integrity": "sha512-NIxF55hv4nSqQswkAeiOi1r83xy8JldOFDTWiug55KBu9Jnblncd2U6ViHmYgHf01TPZS77NJBhBMKdWj9HQMQ==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/sibiraj-s"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/cjs-module-lexer": {
      "version": "1.4.3",
      "resolved": "https://registry.npmjs.org/cjs-module-lexer/-/cjs-module-lexer-1.4.3.tgz",
      "integrity": "sha512-9z8TZaGM1pfswYeXrUpzPrkx8UnWYdhJclsiYMm6x/w5+nN+8Tf/LnAgfLGQCm59qAOxU8WwHEq2vNwF6i4j+Q==",
      "license": "MIT"
    },
    "node_modules/clean-css": {
      "version": "5.3.3",
      "resolved": "https://registry.npmjs.org/clean-css/-/clean-css-5.3.3.tgz",
      "integrity": "sha512-D5J+kHaVb/wKSFcyyV75uCn8fiY4sV38XJoe4CUyGQ+mOU/fMVYUdH1hJC+CJQ5uY3EnW27SbJYS4X8BiLrAFg==",
      "license": "MIT",
      "dependencies": {
        "source-map": "~0.6.0"
      },
      "engines": {
        "node": ">= 10.0"
      }
    },
    "node_modules/clean-css/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/cliui": {
      "version": "7.0.4",
      "resolved": "https://registry.npmjs.org/cliui/-/cliui-7.0.4.tgz",
      "integrity": "sha512-OcRE68cOsVMXp1Yvonl/fzkQOyjLSu/8bhPDfQt0e0/Eb283TKP20Fs2MqoPsr9SwA595rRCA+QMzYc9nBP+JQ==",
      "license": "ISC",
      "dependencies": {
        "string-width": "^4.2.0",
        "strip-ansi": "^6.0.0",
        "wrap-ansi": "^7.0.0"
      }
    },
    "node_modules/co": {
      "version": "4.6.0",
      "resolved": "https://registry.npmjs.org/co/-/co-4.6.0.tgz",
      "integrity": "sha512-QVb0dM5HvG+uaxitm8wONl7jltx8dqhfU33DcqtOZcLSVIKSDDLDi7+0LbAKiyI8hD9u42m2YxXSkMGWThaecQ==",
      "license": "MIT",
      "engines": {
        "iojs": ">= 1.0.0",
        "node": ">= 0.12.0"
      }
    },
    "node_modules/coa": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/coa/-/coa-2.0.2.tgz",
      "integrity": "sha512-q5/jG+YQnSy4nRTV4F7lPepBJZ8qBNJJDBuJdoejDyLXgmL7IEo+Le2JDZudFTFt7mrCqIRaSjws4ygRCTCAXA==",
      "license": "MIT",
      "dependencies": {
        "@types/q": "^1.5.1",
        "chalk": "^2.4.1",
        "q": "^1.1.2"
      },
      "engines": {
        "node": ">= 4.0"
      }
    },
    "node_modules/coa/node_modules/ansi-styles": {
      "version": "3.2.1",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-3.2.1.tgz",
      "integrity": "sha512-VT0ZI6kZRdTh8YyJw3SMbYm/u+NqfsAxEpWO0Pf9sq8/e94WxxOpPKx9FR1FlyCtOVDNOQ+8ntlqFxiRc+r5qA==",
      "license": "MIT",
      "dependencies": {
        "color-convert": "^1.9.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/coa/node_modules/chalk": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/chalk/-/chalk-2.4.2.tgz",
      "integrity": "sha512-Mti+f9lpJNcwF4tWV8/OrTTtF1gZi+f8FqlyAdouralcFWFQWF2+NgCHShjkCb+IFBLq9buZwE1xckQU4peSuQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^3.2.1",
        "escape-string-regexp": "^1.0.5",
        "supports-color": "^5.3.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/coa/node_modules/color-convert": {
      "version": "1.9.3",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-1.9.3.tgz",
      "integrity": "sha512-QfAUtd+vFdAtFQcC8CCyYt1fYWxSqAiK2cSD6zDB8N3cpsEBAvRxp9zOGg6G/SHHJYAT88/az/IuDGALsNVbGg==",
      "license": "MIT",
      "dependencies": {
        "color-name": "1.1.3"
      }
    },
    "node_modules/coa/node_modules/color-name": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.3.tgz",
      "integrity": "sha512-72fSenhMw2HZMTVHeCA9KCmpEIbzWiQsjN+BHcBbS9vr1mtt+vJjPdksIBNUmKAW8TFUDPJK5SUU3QhE9NEXDw==",
      "license": "MIT"
    },
    "node_modules/coa/node_modules/escape-string-regexp": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-1.0.5.tgz",
      "integrity": "sha512-vbRorB5FUQWvla16U8R/qgaFIya2qGzwDrNmCZuYKrbdSUMG6I1ZCGQRefkRVhuOkIGVne7BQ35DSfo1qvJqFg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/coa/node_modules/has-flag": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/has-flag/-/has-flag-3.0.0.tgz",
      "integrity": "sha512-sKJf1+ceQBr4SMkvQnBDNDtf4TXpVhVGateu0t918bl30FnbE2m4vNLX+VWe/dpjlb+HugGYzW7uQXH98HPEYw==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/coa/node_modules/supports-color": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-5.5.0.tgz",
      "integrity": "sha512-QjVjwdXIt408MIiAqCX4oUKsgU2EqAGzs2Ppkm4aQYbjm+ZEWEcW4SfFNTr4uMNZma0ey4f5lgLrkB0aX0QMow==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^3.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/collect-v8-coverage": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/collect-v8-coverage/-/collect-v8-coverage-1.0.3.tgz",
      "integrity": "sha512-1L5aqIkwPfiodaMgQunkF1zRhNqifHBmtbbbxcr6yVxxBnliw4TDOW6NxpO8DJLgJ16OT+Y4ztZqP6p/FtXnAw==",
      "license": "MIT"
    },
    "node_modules/color-convert": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-2.0.1.tgz",
      "integrity": "sha512-RRECPsj7iu/xb5oKYcsFHSppFNnsj/52OVTRKb4zP5onXwVF3zVmmToNcOfGC+CRDpfK/U584fMg38ZHCaElKQ==",
      "license": "MIT",
      "dependencies": {
        "color-name": "~1.1.4"
      },
      "engines": {
        "node": ">=7.0.0"
      }
    },
    "node_modules/color-name": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.4.tgz",
      "integrity": "sha512-dOy+3AuW3a2wNbZHIuMZpTcgjGuLU/uBL/ubcZF9OXbDo8ff4O8yVp5Bf0efS8uEoYo5q4Fx7dY9OgQGXgAsQA==",
      "license": "MIT"
    },
    "node_modules/colord": {
      "version": "2.9.3",
      "resolved": "https://registry.npmjs.org/colord/-/colord-2.9.3.tgz",
      "integrity": "sha512-jeC1axXpnb0/2nn/Y1LPuLdgXBLH7aDcHu4KEKfqw3CUhX7ZpfBSlPKyqXE6btIgEzfWtrX3/tyBCaCvXvMkOw==",
      "license": "MIT"
    },
    "node_modules/colorette": {
      "version": "2.0.20",
      "resolved": "https://registry.npmjs.org/colorette/-/colorette-2.0.20.tgz",
      "integrity": "sha512-IfEDxwoWIjkeXL1eXcDiow4UbKjhLdq6/EuSVR9GMN7KVH3r9gQ83e73hsz1Nd1T3ijd5xv1wcWRYO+D6kCI2w==",
      "license": "MIT"
    },
    "node_modules/combined-stream": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/combined-stream/-/combined-stream-1.0.8.tgz",
      "integrity": "sha512-FQN4MRfuJeHf7cBbBMJFXhKSDq+2kAArBlmRBvcvFE5BB1HZKXtSFASDhdlz9zOYwxh8lDdnvmMOe/+5cdoEdg==",
      "license": "MIT",
      "dependencies": {
        "delayed-stream": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/commander": {
      "version": "8.3.0",
      "resolved": "https://registry.npmjs.org/commander/-/commander-8.3.0.tgz",
      "integrity": "sha512-OkTL9umf+He2DZkUq8f8J9of7yL6RJKI24dVITBmNfZBmri9zYZQrKkuXiKhyfPSu8tUhnVBB1iKXevvnlR4Ww==",
      "license": "MIT",
      "engines": {
        "node": ">= 12"
      }
    },
    "node_modules/common-tags": {
      "version": "1.8.2",
      "resolved": "https://registry.npmjs.org/common-tags/-/common-tags-1.8.2.tgz",
      "integrity": "sha512-gk/Z852D2Wtb//0I+kRFNKKE9dIIVirjoqPoA1wJU+XePVXZfGeBpk45+A1rKO4Q43prqWBNY/MiIeRLbPWUaA==",
      "license": "MIT",
      "engines": {
        "node": ">=4.0.0"
      }
    },
    "node_modules/commondir": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/commondir/-/commondir-1.0.1.tgz",
      "integrity": "sha512-W9pAhw0ja1Edb5GVdIF1mjZw/ASI0AlShXM83UUGe2DVr5TdAPEA1OA8m/g8zWp9x6On7gqufY+FatDbC3MDQg==",
      "license": "MIT"
    },
    "node_modules/compressible": {
      "version": "2.0.18",
      "resolved": "https://registry.npmjs.org/compressible/-/compressible-2.0.18.tgz",
      "integrity": "sha512-AF3r7P5dWxL8MxyITRMlORQNaOA2IkAFaTr4k7BUumjPtRpGDTZpl0Pb1XCO6JeDCBdp126Cgs9sMxqSjgYyRg==",
      "license": "MIT",
      "dependencies": {
        "mime-db": ">= 1.43.0 < 2"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/compression": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/compression/-/compression-1.8.1.tgz",
      "integrity": "sha512-9mAqGPHLakhCLeNyxPkK4xVo746zQ/czLH1Ky+vkitMnWfWZps8r0qXuwhwizagCRttsL4lfG4pIOvaWLpAP0w==",
      "license": "MIT",
      "dependencies": {
        "bytes": "3.1.2",
        "compressible": "~2.0.18",
        "debug": "2.6.9",
        "negotiator": "~0.6.4",
        "on-headers": "~1.1.0",
        "safe-buffer": "5.2.1",
        "vary": "~1.1.2"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/compression/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/compression/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/concat-map": {
      "version": "0.0.1",
      "resolved": "https://registry.npmjs.org/concat-map/-/concat-map-0.0.1.tgz",
      "integrity": "sha512-/Srv4dswyQNBfohGpz9o6Yb3Gz3SrUDqBH5rTuhGR7ahtlbYKnVxw2bCFMRljaA7EXHaXZ8wsHdodFvbkhKmqg==",
      "license": "MIT"
    },
    "node_modules/confusing-browser-globals": {
      "version": "1.0.11",
      "resolved": "https://registry.npmjs.org/confusing-browser-globals/-/confusing-browser-globals-1.0.11.tgz",
      "integrity": "sha512-JsPKdmh8ZkmnHxDk55FZ1TqVLvEQTvoByJZRN9jzI0UjxK/QgAmsphz7PGtqgPieQZ/CQcHWXCR7ATDNhGe+YA==",
      "license": "MIT"
    },
    "node_modules/connect-history-api-fallback": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/connect-history-api-fallback/-/connect-history-api-fallback-2.0.0.tgz",
      "integrity": "sha512-U73+6lQFmfiNPrYbXqr6kZ1i1wiRqXnp2nhMsINseWXO8lDau0LGEffJ8kQi4EjLZympVgRdvqjAgiZ1tgzDDA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8"
      }
    },
    "node_modules/content-disposition": {
      "version": "0.5.4",
      "resolved": "https://registry.npmjs.org/content-disposition/-/content-disposition-0.5.4.tgz",
      "integrity": "sha512-FveZTNuGw04cxlAiWbzi6zTAL/lhehaWbTtgluJh4/E95DqMwTmha3KZN1aAWA8cFIhHzMZUvLevkw5Rqk+tSQ==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "5.2.1"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/content-type": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/content-type/-/content-type-1.0.5.tgz",
      "integrity": "sha512-nTjqfcBFEipKdXCv4YDQWCfmcLZKm81ldF0pAopTvyrFGVbcR6P/VAAd5G7N+0tTr8QqiU0tFadD6FK4NtJwOA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/convert-source-map": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-2.0.0.tgz",
      "integrity": "sha512-Kvp459HrV2FEJ1CAsi1Ku+MY3kasH19TFykTz2xWmMeq6bk2NU3XXvfJ+Q61m0xktWwt+1HSYf3JZsTms3aRJg==",
      "license": "MIT"
    },
    "node_modules/cookie": {
      "version": "0.7.2",
      "resolved": "https://registry.npmjs.org/cookie/-/cookie-0.7.2.tgz",
      "integrity": "sha512-yki5XnKuf750l50uGTllt6kKILY4nQ1eNIQatoXEByZ5dWgnKqbnqmTrBE5B4N7lrMJKQ2ytWMiTO2o0v6Ew/w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/cookie-signature": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/cookie-signature/-/cookie-signature-1.0.7.tgz",
      "integrity": "sha512-NXdYc3dLr47pBkpUCHtKSwIOQXLVn8dZEuywboCOJY/osA0wFSLlSawr3KN8qXJEyX66FcONTH8EIlVuK0yyFA==",
      "license": "MIT"
    },
    "node_modules/core-js": {
      "version": "3.48.0",
      "resolved": "https://registry.npmjs.org/core-js/-/core-js-3.48.0.tgz",
      "integrity": "sha512-zpEHTy1fjTMZCKLHUZoVeylt9XrzaIN2rbPXEt0k+q7JE5CkCZdo6bNq55bn24a69CH7ErAVLKijxJja4fw+UQ==",
      "hasInstallScript": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/core-js"
      }
    },
    "node_modules/core-js-compat": {
      "version": "3.48.0",
      "resolved": "https://registry.npmjs.org/core-js-compat/-/core-js-compat-3.48.0.tgz",
      "integrity": "sha512-OM4cAF3D6VtH/WkLtWvyNC56EZVXsZdU3iqaMG2B4WvYrlqU831pc4UtG5yp0sE9z8Y02wVN7PjW5Zf9Gt0f1Q==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.28.1"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/core-js"
      }
    },
    "node_modules/core-js-pure": {
      "version": "3.48.0",
      "resolved": "https://registry.npmjs.org/core-js-pure/-/core-js-pure-3.48.0.tgz",
      "integrity": "sha512-1slJgk89tWC51HQ1AEqG+s2VuwpTRr8ocu4n20QUcH1v9lAN0RXen0Q0AABa/DK1I7RrNWLucplOHMx8hfTGTw==",
      "hasInstallScript": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/core-js"
      }
    },
    "node_modules/core-util-is": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/core-util-is/-/core-util-is-1.0.3.tgz",
      "integrity": "sha512-ZQBvi1DcpJ4GDqanjucZ2Hj3wEO5pZDS89BWbkcrvdxksJorwUDDZamX9ldFkp9aw2lmBDLgkObEA4DWNJ9FYQ==",
      "license": "MIT"
    },
    "node_modules/cosmiconfig": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/cosmiconfig/-/cosmiconfig-7.1.0.tgz",
      "integrity": "sha512-AdmX6xUzdNASswsFtmwSt7Vj8po9IuqXm0UXz7QKPuEUmPB4XyjGfaAr2PSuELMwkRMVH1EpIkX5bTZGRB3eCA==",
      "license": "MIT",
      "dependencies": {
        "@types/parse-json": "^4.0.0",
        "import-fresh": "^3.2.1",
        "parse-json": "^5.0.0",
        "path-type": "^4.0.0",
        "yaml": "^1.10.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/cross-spawn": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz",
      "integrity": "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==",
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.1.0",
        "shebang-command": "^2.0.0",
        "which": "^2.0.1"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/crypto-random-string": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/crypto-random-string/-/crypto-random-string-2.0.0.tgz",
      "integrity": "sha512-v1plID3y9r/lPhviJ1wrXpLeyUIGAZ2SHNYTEapm7/8A9nLPoyvVp3RK/EPFqn5kEznyWgYZNsRtYYIWbuG8KA==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/css-blank-pseudo": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/css-blank-pseudo/-/css-blank-pseudo-3.0.3.tgz",
      "integrity": "sha512-VS90XWtsHGqoM0t4KpH053c4ehxZ2E6HtGI7x68YFV0pTo/QmkV/YFA+NnlvK8guxZVNWGQhVNJGC39Q8XF4OQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9"
      },
      "bin": {
        "css-blank-pseudo": "dist/cli.cjs"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/css-declaration-sorter": {
      "version": "6.4.1",
      "resolved": "https://registry.npmjs.org/css-declaration-sorter/-/css-declaration-sorter-6.4.1.tgz",
      "integrity": "sha512-rtdthzxKuyq6IzqX6jEcIzQF/YqccluefyCYheovBOLhFT/drQA9zj/UbRAa9J7C0o6EG6u3E6g+vKkay7/k3g==",
      "license": "ISC",
      "engines": {
        "node": "^10 || ^12 || >=14"
      },
      "peerDependencies": {
        "postcss": "^8.0.9"
      }
    },
    "node_modules/css-has-pseudo": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/css-has-pseudo/-/css-has-pseudo-3.0.4.tgz",
      "integrity": "sha512-Vse0xpR1K9MNlp2j5w1pgWIJtm1a8qS0JwS9goFYcImjlHEmywP9VUF05aGBXzGpDJF86QXk4L0ypBmwPhGArw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9"
      },
      "bin": {
        "css-has-pseudo": "dist/cli.cjs"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/css-loader": {
      "version": "6.11.0",
      "resolved": "https://registry.npmjs.org/css-loader/-/css-loader-6.11.0.tgz",
      "integrity": "sha512-CTJ+AEQJjq5NzLga5pE39qdiSV56F8ywCIsqNIRF0r7BDgWsN25aazToqAFg7ZrtA/U016xudB3ffgweORxX7g==",
      "license": "MIT",
      "dependencies": {
        "icss-utils": "^5.1.0",
        "postcss": "^8.4.33",
        "postcss-modules-extract-imports": "^3.1.0",
        "postcss-modules-local-by-default": "^4.0.5",
        "postcss-modules-scope": "^3.2.0",
        "postcss-modules-values": "^4.0.0",
        "postcss-value-parser": "^4.2.0",
        "semver": "^7.5.4"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "@rspack/core": "0.x || 1.x",
        "webpack": "^5.0.0"
      },
      "peerDependenciesMeta": {
        "@rspack/core": {
          "optional": true
        },
        "webpack": {
          "optional": true
        }
      }
    },
    "node_modules/css-minimizer-webpack-plugin": {
      "version": "3.4.1",
      "resolved": "https://registry.npmjs.org/css-minimizer-webpack-plugin/-/css-minimizer-webpack-plugin-3.4.1.tgz",
      "integrity": "sha512-1u6D71zeIfgngN2XNRJefc/hY7Ybsxd74Jm4qngIXyUEk7fss3VUzuHxLAq/R8NAba4QU9OUSaMZlbpRc7bM4Q==",
      "license": "MIT",
      "dependencies": {
        "cssnano": "^5.0.6",
        "jest-worker": "^27.0.2",
        "postcss": "^8.3.5",
        "schema-utils": "^4.0.0",
        "serialize-javascript": "^6.0.0",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.0.0"
      },
      "peerDependenciesMeta": {
        "@parcel/css": {
          "optional": true
        },
        "clean-css": {
          "optional": true
        },
        "csso": {
          "optional": true
        },
        "esbuild": {
          "optional": true
        }
      }
    },
    "node_modules/css-minimizer-webpack-plugin/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/css-prefers-color-scheme": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/css-prefers-color-scheme/-/css-prefers-color-scheme-6.0.3.tgz",
      "integrity": "sha512-4BqMbZksRkJQx2zAjrokiGMd07RqOa2IxIrrN10lyBe9xhn9DEvjUK79J6jkeiv9D9hQFXKb6g1jwU62jziJZA==",
      "license": "CC0-1.0",
      "bin": {
        "css-prefers-color-scheme": "dist/cli.cjs"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/css-select": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/css-select/-/css-select-4.3.0.tgz",
      "integrity": "sha512-wPpOYtnsVontu2mODhA19JrqWxNsfdatRKd64kmpRbQgh1KtItko5sTnEpPdpSaJszTOhEMlF/RPz28qj4HqhQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "boolbase": "^1.0.0",
        "css-what": "^6.0.1",
        "domhandler": "^4.3.1",
        "domutils": "^2.8.0",
        "nth-check": "^2.0.1"
      },
      "funding": {
        "url": "https://github.com/sponsors/fb55"
      }
    },
    "node_modules/css-select-base-adapter": {
      "version": "0.1.1",
      "resolved": "https://registry.npmjs.org/css-select-base-adapter/-/css-select-base-adapter-0.1.1.tgz",
      "integrity": "sha512-jQVeeRG70QI08vSTwf1jHxp74JoZsr2XSgETae8/xC8ovSnL2WF87GTLO86Sbwdt2lK4Umg4HnnwMO4YF3Ce7w==",
      "license": "MIT"
    },
    "node_modules/css-tree": {
      "version": "1.0.0-alpha.37",
      "resolved": "https://registry.npmjs.org/css-tree/-/css-tree-1.0.0-alpha.37.tgz",
      "integrity": "sha512-DMxWJg0rnz7UgxKT0Q1HU/L9BeJI0M6ksor0OgqOnF+aRCDWg/N2641HmVyU9KVIu0OVVWOb2IpC9A+BJRnejg==",
      "license": "MIT",
      "dependencies": {
        "mdn-data": "2.0.4",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/css-tree/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/css-what": {
      "version": "6.2.2",
      "resolved": "https://registry.npmjs.org/css-what/-/css-what-6.2.2.tgz",
      "integrity": "sha512-u/O3vwbptzhMs3L1fQE82ZSLHQQfto5gyZzwteVIEyeaY5Fc7R4dapF/BvRoSYFeqfBk4m0V1Vafq5Pjv25wvA==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">= 6"
      },
      "funding": {
        "url": "https://github.com/sponsors/fb55"
      }
    },
    "node_modules/cssdb": {
      "version": "7.11.2",
      "resolved": "https://registry.npmjs.org/cssdb/-/cssdb-7.11.2.tgz",
      "integrity": "sha512-lhQ32TFkc1X4eTefGfYPvgovRSzIMofHkigfH8nWtyRL4XJLsRhJFreRvEgKzept7x1rjBuy3J/MurXLaFxW/A==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/csstools"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/csstools"
        }
      ],
      "license": "CC0-1.0"
    },
    "node_modules/cssesc": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/cssesc/-/cssesc-3.0.0.tgz",
      "integrity": "sha512-/Tb/JcjK111nNScGob5MNtsntNM1aCNUDipB/TkwZFhyDrrE47SOx/18wF2bbjgc3ZzCSKW1T5nt5EbFoAz/Vg==",
      "license": "MIT",
      "bin": {
        "cssesc": "bin/cssesc"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/cssnano": {
      "version": "5.1.15",
      "resolved": "https://registry.npmjs.org/cssnano/-/cssnano-5.1.15.tgz",
      "integrity": "sha512-j+BKgDcLDQA+eDifLx0EO4XSA56b7uut3BQFH+wbSaSTuGLuiyTa/wbRYthUXX8LC9mLg+WWKe8h+qJuwTAbHw==",
      "license": "MIT",
      "dependencies": {
        "cssnano-preset-default": "^5.2.14",
        "lilconfig": "^2.0.3",
        "yaml": "^1.10.2"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/cssnano"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/cssnano-preset-default": {
      "version": "5.2.14",
      "resolved": "https://registry.npmjs.org/cssnano-preset-default/-/cssnano-preset-default-5.2.14.tgz",
      "integrity": "sha512-t0SFesj/ZV2OTylqQVOrFgEh5uanxbO6ZAdeCrNsUQ6fVuXwYTxJPNAGvGTxHbD68ldIJNec7PyYZDBrfDQ+6A==",
      "license": "MIT",
      "dependencies": {
        "css-declaration-sorter": "^6.3.1",
        "cssnano-utils": "^3.1.0",
        "postcss-calc": "^8.2.3",
        "postcss-colormin": "^5.3.1",
        "postcss-convert-values": "^5.1.3",
        "postcss-discard-comments": "^5.1.2",
        "postcss-discard-duplicates": "^5.1.0",
        "postcss-discard-empty": "^5.1.1",
        "postcss-discard-overridden": "^5.1.0",
        "postcss-merge-longhand": "^5.1.7",
        "postcss-merge-rules": "^5.1.4",
        "postcss-minify-font-values": "^5.1.0",
        "postcss-minify-gradients": "^5.1.1",
        "postcss-minify-params": "^5.1.4",
        "postcss-minify-selectors": "^5.2.1",
        "postcss-normalize-charset": "^5.1.0",
        "postcss-normalize-display-values": "^5.1.0",
        "postcss-normalize-positions": "^5.1.1",
        "postcss-normalize-repeat-style": "^5.1.1",
        "postcss-normalize-string": "^5.1.0",
        "postcss-normalize-timing-functions": "^5.1.0",
        "postcss-normalize-unicode": "^5.1.1",
        "postcss-normalize-url": "^5.1.0",
        "postcss-normalize-whitespace": "^5.1.1",
        "postcss-ordered-values": "^5.1.3",
        "postcss-reduce-initial": "^5.1.2",
        "postcss-reduce-transforms": "^5.1.0",
        "postcss-svgo": "^5.1.0",
        "postcss-unique-selectors": "^5.1.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/cssnano-utils": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/cssnano-utils/-/cssnano-utils-3.1.0.tgz",
      "integrity": "sha512-JQNR19/YZhz4psLX/rQ9M83e3z2Wf/HdJbryzte4a3NSuafyp9w/I4U+hx5C2S9g41qlstH7DEWnZaaj83OuEA==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/csso": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/csso/-/csso-4.2.0.tgz",
      "integrity": "sha512-wvlcdIbf6pwKEk7vHj8/Bkc0B4ylXZruLvOgs9doS5eOsOpuodOV2zJChSpkp+pRpYQLQMeF04nr3Z68Sta9jA==",
      "license": "MIT",
      "dependencies": {
        "css-tree": "^1.1.2"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/csso/node_modules/css-tree": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/css-tree/-/css-tree-1.1.3.tgz",
      "integrity": "sha512-tRpdppF7TRazZrjJ6v3stzv93qxRcSsFmW6cX0Zm2NVKpxE1WV1HblnghVv9TreireHkqI/VDEsfolRF1p6y7Q==",
      "license": "MIT",
      "dependencies": {
        "mdn-data": "2.0.14",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/csso/node_modules/mdn-data": {
      "version": "2.0.14",
      "resolved": "https://registry.npmjs.org/mdn-data/-/mdn-data-2.0.14.tgz",
      "integrity": "sha512-dn6wd0uw5GsdswPFfsgMp5NSB0/aDe6fK94YJV/AJDYXL6HVLWBsxeq7js7Ad+mU2K9LAlwpk6kN2D5mwCPVow==",
      "license": "CC0-1.0"
    },
    "node_modules/csso/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/cssom": {
      "version": "0.4.4",
      "resolved": "https://registry.npmjs.org/cssom/-/cssom-0.4.4.tgz",
      "integrity": "sha512-p3pvU7r1MyyqbTk+WbNJIgJjG2VmTIaB10rI93LzVPrmDJKkzKYMtxxyAvQXR/NS6otuzveI7+7BBq3SjBS2mw==",
      "license": "MIT"
    },
    "node_modules/cssstyle": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/cssstyle/-/cssstyle-2.3.0.tgz",
      "integrity": "sha512-AZL67abkUzIuvcHqk7c09cezpGNcxUxU4Ioi/05xHk4DQeTkWmGYftIE6ctU6AEt+Gn4n1lDStOtj7FKycP71A==",
      "license": "MIT",
      "dependencies": {
        "cssom": "~0.3.6"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/cssstyle/node_modules/cssom": {
      "version": "0.3.8",
      "resolved": "https://registry.npmjs.org/cssom/-/cssom-0.3.8.tgz",
      "integrity": "sha512-b0tGHbfegbhPJpxpiBPU2sCkigAqtM9O121le6bbOlgyV+NyGyCmVfJ6QW9eRjz8CpNfWEOYBIMIGRYkLwsIYg==",
      "license": "MIT"
    },
    "node_modules/damerau-levenshtein": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/damerau-levenshtein/-/damerau-levenshtein-1.0.8.tgz",
      "integrity": "sha512-sdQSFB7+llfUcQHUQO3+B8ERRj0Oa4w9POWMI/puGtuf7gFywGmkaLCElnudfTiKZV+NvHqL0ifzdrI8Ro7ESA==",
      "license": "BSD-2-Clause"
    },
    "node_modules/data-urls": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/data-urls/-/data-urls-2.0.0.tgz",
      "integrity": "sha512-X5eWTSXO/BJmpdIKCRuKUgSCgAN0OwliVK3yPKbwIWU1Tdw5BRajxlzMidvh+gwko9AfQ9zIj52pzF91Q3YAvQ==",
      "license": "MIT",
      "dependencies": {
        "abab": "^2.0.3",
        "whatwg-mimetype": "^2.3.0",
        "whatwg-url": "^8.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/data-view-buffer": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/data-view-buffer/-/data-view-buffer-1.0.2.tgz",
      "integrity": "sha512-EmKO5V3OLXh1rtK2wgXRansaK1/mtVdTUEiEI0W8RkvgT05kfxaH29PliLnpLP73yYO6142Q72QNa8Wx/A5CqQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/data-view-byte-length": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/data-view-byte-length/-/data-view-byte-length-1.0.2.tgz",
      "integrity": "sha512-tuhGbE6CfTM9+5ANGf+oQb72Ky/0+s3xKUpHvShfiz2RxMFgFPjsXuRLBVMtvMs15awe45SRb83D6wH4ew6wlQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/inspect-js"
      }
    },
    "node_modules/data-view-byte-offset": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/data-view-byte-offset/-/data-view-byte-offset-1.0.1.tgz",
      "integrity": "sha512-BS8PfmtDGnrgYdOonGZQdLZslWIeCGFP9tpan0hi1Co2Zr2NKADsvGYA8XxuG/4UWgJ6Cjtv+YJnB6MM69QGlQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/decimal.js": {
      "version": "10.6.0",
      "resolved": "https://registry.npmjs.org/decimal.js/-/decimal.js-10.6.0.tgz",
      "integrity": "sha512-YpgQiITW3JXGntzdUmyUR1V812Hn8T1YVXhCu+wO3OpS4eU9l4YdD3qjyiKdV6mvV29zapkMeD390UVEf2lkUg==",
      "license": "MIT"
    },
    "node_modules/dedent": {
      "version": "0.7.0",
      "resolved": "https://registry.npmjs.org/dedent/-/dedent-0.7.0.tgz",
      "integrity": "sha512-Q6fKUPqnAHAyhiUgFU7BUzLiv0kd8saH9al7tnu5Q/okj6dnupxyTgFIBjVzJATdfIAm9NAsvXNzjaKa+bxVyA==",
      "license": "MIT"
    },
    "node_modules/deep-is": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/deep-is/-/deep-is-0.1.4.tgz",
      "integrity": "sha512-oIPzksmTg4/MriiaYGO+okXDT7ztn/w3Eptv/+gSIdMdKsJo0u4CfYNFJPy+4SKMuCqGw2wxnA+URMg3t8a/bQ==",
      "license": "MIT"
    },
    "node_modules/deepmerge": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/deepmerge/-/deepmerge-4.3.1.tgz",
      "integrity": "sha512-3sUqbMEc77XqpdNO7FRyRog+eW3ph+GYCbj+rK+uYyRMuwsVy0rMiVtPn+QJlKFvWP/1PYpapqYn0Me2knFn+A==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/default-gateway": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/default-gateway/-/default-gateway-6.0.3.tgz",
      "integrity": "sha512-fwSOJsbbNzZ/CUFpqFBqYfYNLj1NbMPm8MMCIzHjC83iSJRBEGmDUxU+WP661BaBQImeC2yHwXtz+P/O9o+XEg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "execa": "^5.0.0"
      },
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/define-data-property": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/define-data-property/-/define-data-property-1.1.4.tgz",
      "integrity": "sha512-rBMvIzlpA8v6E+SJZoo++HAYqsLrkg7MSfIinMPFhmkorw7X+dOXVJQs+QT69zGkzMyfDnIMN2Wid1+NbL3T+A==",
      "license": "MIT",
      "dependencies": {
        "es-define-property": "^1.0.0",
        "es-errors": "^1.3.0",
        "gopd": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/define-lazy-prop": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/define-lazy-prop/-/define-lazy-prop-2.0.0.tgz",
      "integrity": "sha512-Ds09qNh8yw3khSjiJjiUInaGX9xlqZDY7JVryGxdxV7NPeuqQfplOpQ66yJFZut3jLa5zOwkXw1g9EI2uKh4Og==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/define-properties": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/define-properties/-/define-properties-1.2.1.tgz",
      "integrity": "sha512-8QmQKqEASLd5nx0U1B1okLElbUuuttJ/AnYmRXbbbGDWh6uS208EjD4Xqq/I9wK7u0v6O08XhTWnt5XtEbR6Dg==",
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.0.1",
        "has-property-descriptors": "^1.0.0",
        "object-keys": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/delayed-stream": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/delayed-stream/-/delayed-stream-1.0.0.tgz",
      "integrity": "sha512-ZySD7Nf91aLB0RxL4KGrKHBXl7Eds1DAmEdcoVawXnLD7SDhpNgtuII2aAkg7a7QS41jxPSZ17p4VdGnMHk3MQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/depd": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/depd/-/depd-2.0.0.tgz",
      "integrity": "sha512-g7nH6P6dyDioJogAAGprGpCtVImJhpPk/roCzdb3fIh61/s/nPsfR6onyMwkCAR/OlC3yBC0lESvUoQEAssIrw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/destroy": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/destroy/-/destroy-1.2.0.tgz",
      "integrity": "sha512-2sJGJTaXIIaR1w4iJSNoN0hnMY7Gpc/n8D4qSCJw8QqFWXf7cuAgnEHxBpweaVcPevC2l3KpjYCx3NypQQgaJg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8",
        "npm": "1.2.8000 || >= 1.4.16"
      }
    },
    "node_modules/detect-newline": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/detect-newline/-/detect-newline-3.1.0.tgz",
      "integrity": "sha512-TLz+x/vEXm/Y7P7wn1EJFNLxYpUD4TgMosxY6fAVJUnJMbupHBOncxyWUG9OpTaH9EBD7uFI5LfEgmMOc54DsA==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/detect-node": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/detect-node/-/detect-node-2.1.0.tgz",
      "integrity": "sha512-T0NIuQpnTvFDATNuHN5roPwSBG83rFsuO+MXXH9/3N1eFbn4wcPjttvjMLEPWJ0RGUYgQE7cGgS3tNxbqCGM7g==",
      "license": "MIT"
    },
    "node_modules/detect-port-alt": {
      "version": "1.1.6",
      "resolved": "https://registry.npmjs.org/detect-port-alt/-/detect-port-alt-1.1.6.tgz",
      "integrity": "sha512-5tQykt+LqfJFBEYaDITx7S7cR7mJ/zQmLXZ2qt5w04ainYZw6tBf9dBunMjVeVOdYVRUzUOE4HkY5J7+uttb5Q==",
      "license": "MIT",
      "dependencies": {
        "address": "^1.0.1",
        "debug": "^2.6.0"
      },
      "bin": {
        "detect": "bin/detect-port",
        "detect-port": "bin/detect-port"
      },
      "engines": {
        "node": ">= 4.2.1"
      }
    },
    "node_modules/detect-port-alt/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/detect-port-alt/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/didyoumean": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/didyoumean/-/didyoumean-1.2.2.tgz",
      "integrity": "sha512-gxtyfqMg7GKyhQmb056K7M3xszy/myH8w+B4RT+QXBQsvAOdc3XymqDDPHx1BgPgsdAA5SIifona89YtRATDzw==",
      "license": "Apache-2.0"
    },
    "node_modules/diff-sequences": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/diff-sequences/-/diff-sequences-27.5.1.tgz",
      "integrity": "sha512-k1gCAXAsNgLwEL+Y8Wvl+M6oEFj5bgazfZULpS5CneoPPXRaCCW7dm+q21Ky2VEE5X+VeRDBVg1Pcvvsr4TtNQ==",
      "license": "MIT",
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/dir-glob": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/dir-glob/-/dir-glob-3.0.1.tgz",
      "integrity": "sha512-WkrWp9GR4KXfKGYzOLmTuGVi1UWFfws377n9cc55/tb6DuqyF6pcQ5AbiHEshaDpY9v6oaSr2XCDidGmMwdzIA==",
      "license": "MIT",
      "dependencies": {
        "path-type": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/dlv": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/dlv/-/dlv-1.1.3.tgz",
      "integrity": "sha512-+HlytyjlPKnIG8XuRG8WvmBP8xs8P71y+SKKS6ZXWoEgLuePxtDoUEiH7WkdePWrQ5JBpE6aoVqfZfJUQkjXwA==",
      "license": "MIT"
    },
    "node_modules/dns-packet": {
      "version": "5.6.1",
      "resolved": "https://registry.npmjs.org/dns-packet/-/dns-packet-5.6.1.tgz",
      "integrity": "sha512-l4gcSouhcgIKRvyy99RNVOgxXiicE+2jZoNmaNmZ6JXiGajBOJAesk1OBlJuM5k2c+eudGdLxDqXuPCKIj6kpw==",
      "license": "MIT",
      "dependencies": {
        "@leichtgewicht/ip-codec": "^2.0.1"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/doctrine": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/doctrine/-/doctrine-3.0.0.tgz",
      "integrity": "sha512-yS+Q5i3hBf7GBkd4KG8a7eBNNWNGLTaEwwYWUijIYM7zrlYDM0BFXHjjPWlWZ1Rg7UaddZeIDmi9jF3HmqiQ2w==",
      "license": "Apache-2.0",
      "dependencies": {
        "esutils": "^2.0.2"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/dom-converter": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/dom-converter/-/dom-converter-0.2.0.tgz",
      "integrity": "sha512-gd3ypIPfOMr9h5jIKq8E3sHOTCjeirnl0WK5ZdS1AW0Odt0b1PaWaHdJ4Qk4klv+YB9aJBS7mESXjFoDQPu6DA==",
      "license": "MIT",
      "dependencies": {
        "utila": "~0.4"
      }
    },
    "node_modules/dom-serializer": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/dom-serializer/-/dom-serializer-1.4.1.tgz",
      "integrity": "sha512-VHwB3KfrcOOkelEG2ZOfxqLZdfkil8PtJi4P8N2MMXucZq2yLp75ClViUlOVwyoHEDjYU433Aq+5zWP61+RGag==",
      "license": "MIT",
      "dependencies": {
        "domelementtype": "^2.0.1",
        "domhandler": "^4.2.0",
        "entities": "^2.0.0"
      },
      "funding": {
        "url": "https://github.com/cheeriojs/dom-serializer?sponsor=1"
      }
    },
    "node_modules/domelementtype": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/domelementtype/-/domelementtype-2.3.0.tgz",
      "integrity": "sha512-OLETBj6w0OsagBwdXnPdN0cnMfF9opN69co+7ZrbfPGrdpPVNBUj02spi6B1N7wChLQiPn4CSH/zJvXw56gmHw==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/fb55"
        }
      ],
      "license": "BSD-2-Clause"
    },
    "node_modules/domexception": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/domexception/-/domexception-2.0.1.tgz",
      "integrity": "sha512-yxJ2mFy/sibVQlu5qHjOkf9J3K6zgmCxgJ94u2EdvDOV09H+32LtRswEcUsmUWN72pVLOEnTSRaIVVzVQgS0dg==",
      "deprecated": "Use your platform's native DOMException instead",
      "license": "MIT",
      "dependencies": {
        "webidl-conversions": "^5.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/domexception/node_modules/webidl-conversions": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/webidl-conversions/-/webidl-conversions-5.0.0.tgz",
      "integrity": "sha512-VlZwKPCkYKxQgeSbH5EyngOmRp7Ww7I9rQLERETtf5ofd9pGeswWiOtogpEO850jziPRarreGxn5QIiTqpb2wA==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/domhandler": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/domhandler/-/domhandler-4.3.1.tgz",
      "integrity": "sha512-GrwoxYN+uWlzO8uhUXRl0P+kHE4GtVPfYzVLcUxPL7KNdHKj66vvlhiweIHqYYXWlw+T8iLMp42Lm67ghw4WMQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "domelementtype": "^2.2.0"
      },
      "engines": {
        "node": ">= 4"
      },
      "funding": {
        "url": "https://github.com/fb55/domhandler?sponsor=1"
      }
    },
    "node_modules/domutils": {
      "version": "2.8.0",
      "resolved": "https://registry.npmjs.org/domutils/-/domutils-2.8.0.tgz",
      "integrity": "sha512-w96Cjofp72M5IIhpjgobBimYEfoPjx1Vx0BSX9P30WBdZW2WIKU0T1Bd0kz2eNZ9ikjKgHbEyKx8BB6H1L3h3A==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "dom-serializer": "^1.0.1",
        "domelementtype": "^2.2.0",
        "domhandler": "^4.2.0"
      },
      "funding": {
        "url": "https://github.com/fb55/domutils?sponsor=1"
      }
    },
    "node_modules/dot-case": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/dot-case/-/dot-case-3.0.4.tgz",
      "integrity": "sha512-Kv5nKlh6yRrdrGvxeJ2e5y2eRUpkUosIW4A2AS38zwSz27zu7ufDwQPi5Jhs3XAlGNetl3bmnGhQsMtkKJnj3w==",
      "license": "MIT",
      "dependencies": {
        "no-case": "^3.0.4",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/dotenv": {
      "version": "10.0.0",
      "resolved": "https://registry.npmjs.org/dotenv/-/dotenv-10.0.0.tgz",
      "integrity": "sha512-rlBi9d8jpv9Sf1klPjNfFAuWDjKLwTIJJ/VxtoTwIR6hnZxcEOQCZg2oIL3MWBYw5GpUDKOEnND7LXTbIpQ03Q==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/dotenv-expand": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/dotenv-expand/-/dotenv-expand-5.1.0.tgz",
      "integrity": "sha512-YXQl1DSa4/PQyRfgrv6aoNjhasp/p4qs9FjJ4q4cQk+8m4r6k4ZSiEyytKG8f8W9gi8WsQtIObNmKd+tMzNTmA==",
      "license": "BSD-2-Clause"
    },
    "node_modules/dunder-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/dunder-proto/-/dunder-proto-1.0.1.tgz",
      "integrity": "sha512-KIN/nDJBQRcXw0MLVhZE9iQHmG68qAVIBg9CqmUYjmQIhgij9U5MFvrqkUL5FbtyyzZuOeOt0zdeRe4UY7ct+A==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.1",
        "es-errors": "^1.3.0",
        "gopd": "^1.2.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/duplexer": {
      "version": "0.1.2",
      "resolved": "https://registry.npmjs.org/duplexer/-/duplexer-0.1.2.tgz",
      "integrity": "sha512-jtD6YG370ZCIi/9GTaJKQxWTZD045+4R4hTk/x1UyoqadyJ9x9CgSi1RlVDQF8U2sxLLSnFkCaMihqljHIWgMg==",
      "license": "MIT"
    },
    "node_modules/ee-first": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/ee-first/-/ee-first-1.1.1.tgz",
      "integrity": "sha512-WMwm9LhRUo+WUaRN+vRuETqG89IgZphVSNkdFgeb6sS/E4OrDIN7t48CAewSHXc6C8lefD8KKfr5vY61brQlow==",
      "license": "MIT"
    },
    "node_modules/ejs": {
      "version": "3.1.10",
      "resolved": "https://registry.npmjs.org/ejs/-/ejs-3.1.10.tgz",
      "integrity": "sha512-UeJmFfOrAQS8OJWPZ4qtgHyWExa088/MtK5UEyoJGFH67cDEXkZSviOiKRCZ4Xij0zxI3JECgYs3oKx+AizQBA==",
      "license": "Apache-2.0",
      "dependencies": {
        "jake": "^10.8.5"
      },
      "bin": {
        "ejs": "bin/cli.js"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/electron-to-chromium": {
      "version": "1.5.307",
      "resolved": "https://registry.npmjs.org/electron-to-chromium/-/electron-to-chromium-1.5.307.tgz",
      "integrity": "sha512-5z3uFKBWjiNR44nFcYdkcXjKMbg5KXNdciu7mhTPo9tB7NbqSNP2sSnGR+fqknZSCwKkBN+oxiiajWs4dT6ORg==",
      "license": "ISC"
    },
    "node_modules/emittery": {
      "version": "0.8.1",
      "resolved": "https://registry.npmjs.org/emittery/-/emittery-0.8.1.tgz",
      "integrity": "sha512-uDfvUjVrfGJJhymx/kz6prltenw1u7WrCg1oa94zYY8xxVpLLUu045LAT0dhDZdXG58/EpPL/5kA180fQ/qudg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sindresorhus/emittery?sponsor=1"
      }
    },
    "node_modules/emoji-regex": {
      "version": "9.2.2",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-9.2.2.tgz",
      "integrity": "sha512-L18DaJsXSUk2+42pv8mLs5jJT2hqFkFE4j21wOmgbUqsZ2hL72NsUU785g9RXgo3s0ZNgVl42TiHp3ZtOv/Vyg==",
      "license": "MIT"
    },
    "node_modules/emojis-list": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/emojis-list/-/emojis-list-3.0.0.tgz",
      "integrity": "sha512-/kyM18EfinwXZbno9FyUGeFh87KC8HRQBQGildHZbEuRyWFOmv1U10o9BBp8XVZDVNNuQKyIGIu5ZYAAXJ0V2Q==",
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/encodeurl": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/encodeurl/-/encodeurl-2.0.0.tgz",
      "integrity": "sha512-Q0n9HRi4m6JuGIV1eFlmvJB7ZEVxu93IrMyiMsGC0lrMJMWzRgx6WGquyfQgZVb31vhGgXnfmPNNXmxnOkRBrg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/enhanced-resolve": {
      "version": "5.20.0",
      "resolved": "https://registry.npmjs.org/enhanced-resolve/-/enhanced-resolve-5.20.0.tgz",
      "integrity": "sha512-/ce7+jQ1PQ6rVXwe+jKEg5hW5ciicHwIQUagZkp6IufBoY3YDgdTTY1azVs0qoRgVmvsNB+rbjLJxDAeHHtwsQ==",
      "license": "MIT",
      "dependencies": {
        "graceful-fs": "^4.2.4",
        "tapable": "^2.3.0"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/entities": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/entities/-/entities-2.2.0.tgz",
      "integrity": "sha512-p92if5Nz619I0w+akJrLZH0MX0Pb5DX39XOwQTtXSdQQOaYH03S1uIQp4mhOZtAXrxq4ViO67YTiLBo2638o9A==",
      "license": "BSD-2-Clause",
      "funding": {
        "url": "https://github.com/fb55/entities?sponsor=1"
      }
    },
    "node_modules/error-ex": {
      "version": "1.3.4",
      "resolved": "https://registry.npmjs.org/error-ex/-/error-ex-1.3.4.tgz",
      "integrity": "sha512-sqQamAnR14VgCr1A618A3sGrygcpK+HEbenA/HiEAkkUwcZIIB/tgWqHFxWgOyDh4nB4JCRimh79dR5Ywc9MDQ==",
      "license": "MIT",
      "dependencies": {
        "is-arrayish": "^0.2.1"
      }
    },
    "node_modules/error-stack-parser": {
      "version": "2.1.4",
      "resolved": "https://registry.npmjs.org/error-stack-parser/-/error-stack-parser-2.1.4.tgz",
      "integrity": "sha512-Sk5V6wVazPhq5MhpO+AUxJn5x7XSXGl1R93Vn7i+zS15KDVxQijejNCrz8340/2bgLBjR9GtEG8ZVKONDjcqGQ==",
      "license": "MIT",
      "dependencies": {
        "stackframe": "^1.3.4"
      }
    },
    "node_modules/es-abstract": {
      "version": "1.24.1",
      "resolved": "https://registry.npmjs.org/es-abstract/-/es-abstract-1.24.1.tgz",
      "integrity": "sha512-zHXBLhP+QehSSbsS9Pt23Gg964240DPd6QCf8WpkqEXxQ7fhdZzYsocOr5u7apWonsS5EjZDmTF+/slGMyasvw==",
      "license": "MIT",
      "dependencies": {
        "array-buffer-byte-length": "^1.0.2",
        "arraybuffer.prototype.slice": "^1.0.4",
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "data-view-buffer": "^1.0.2",
        "data-view-byte-length": "^1.0.2",
        "data-view-byte-offset": "^1.0.1",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "es-set-tostringtag": "^2.1.0",
        "es-to-primitive": "^1.3.0",
        "function.prototype.name": "^1.1.8",
        "get-intrinsic": "^1.3.0",
        "get-proto": "^1.0.1",
        "get-symbol-description": "^1.1.0",
        "globalthis": "^1.0.4",
        "gopd": "^1.2.0",
        "has-property-descriptors": "^1.0.2",
        "has-proto": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "internal-slot": "^1.1.0",
        "is-array-buffer": "^3.0.5",
        "is-callable": "^1.2.7",
        "is-data-view": "^1.0.2",
        "is-negative-zero": "^2.0.3",
        "is-regex": "^1.2.1",
        "is-set": "^2.0.3",
        "is-shared-array-buffer": "^1.0.4",
        "is-string": "^1.1.1",
        "is-typed-array": "^1.1.15",
        "is-weakref": "^1.1.1",
        "math-intrinsics": "^1.1.0",
        "object-inspect": "^1.13.4",
        "object-keys": "^1.1.1",
        "object.assign": "^4.1.7",
        "own-keys": "^1.0.1",
        "regexp.prototype.flags": "^1.5.4",
        "safe-array-concat": "^1.1.3",
        "safe-push-apply": "^1.0.0",
        "safe-regex-test": "^1.1.0",
        "set-proto": "^1.0.0",
        "stop-iteration-iterator": "^1.1.0",
        "string.prototype.trim": "^1.2.10",
        "string.prototype.trimend": "^1.0.9",
        "string.prototype.trimstart": "^1.0.8",
        "typed-array-buffer": "^1.0.3",
        "typed-array-byte-length": "^1.0.3",
        "typed-array-byte-offset": "^1.0.4",
        "typed-array-length": "^1.0.7",
        "unbox-primitive": "^1.1.0",
        "which-typed-array": "^1.1.19"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/es-array-method-boxes-properly": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/es-array-method-boxes-properly/-/es-array-method-boxes-properly-1.0.0.tgz",
      "integrity": "sha512-wd6JXUmyHmt8T5a2xreUwKcGPq6f1f+WwIJkijUqiGcJz1qqnZgP6XIK+QyIWU5lT7imeNxUll48bziG+TSYcA==",
      "license": "MIT"
    },
    "node_modules/es-define-property": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/es-define-property/-/es-define-property-1.0.1.tgz",
      "integrity": "sha512-e3nRfgfUZ4rNGL232gUgX06QNyyez04KdjFrF+LTRoOXmrOgFKDg4BCdsjW8EnT69eqdYGmRpJwiPVYNrCaW3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-iterator-helpers": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/es-iterator-helpers/-/es-iterator-helpers-1.2.2.tgz",
      "integrity": "sha512-BrUQ0cPTB/IwXj23HtwHjS9n7O4h9FX94b4xc5zlTHxeLgTAdzYUDyy6KdExAl9lbN5rtfe44xpjpmj9grxs5w==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.24.1",
        "es-errors": "^1.3.0",
        "es-set-tostringtag": "^2.1.0",
        "function-bind": "^1.1.2",
        "get-intrinsic": "^1.3.0",
        "globalthis": "^1.0.4",
        "gopd": "^1.2.0",
        "has-property-descriptors": "^1.0.2",
        "has-proto": "^1.2.0",
        "has-symbols": "^1.1.0",
        "internal-slot": "^1.1.0",
        "iterator.prototype": "^1.1.5",
        "safe-array-concat": "^1.1.3"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-module-lexer": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/es-module-lexer/-/es-module-lexer-2.0.0.tgz",
      "integrity": "sha512-5POEcUuZybH7IdmGsD8wlf0AI55wMecM9rVBTI/qEAy2c1kTOm3DjFYjrBdI2K3BaJjJYfYFeRtM0t9ssnRuxw==",
      "license": "MIT"
    },
    "node_modules/es-object-atoms": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/es-object-atoms/-/es-object-atoms-1.1.1.tgz",
      "integrity": "sha512-FGgH2h8zKNim9ljj7dankFPcICIK9Cp5bm+c2gQSYePhpaG5+esrLODihIorn+Pe6FGJzWhXQotPv73jTaldXA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-set-tostringtag": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/es-set-tostringtag/-/es-set-tostringtag-2.1.0.tgz",
      "integrity": "sha512-j6vWzfrGVfyXxge+O0x5sh6cvxAog0a/4Rdd2K36zCMV5eJ+/+tOAngRO8cODMNWbVRdVlmGZQL2YS3yR8bIUA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-shim-unscopables": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/es-shim-unscopables/-/es-shim-unscopables-1.1.0.tgz",
      "integrity": "sha512-d9T8ucsEhh8Bi1woXCf+TIKDIROLG5WCkxg8geBCbvk22kzwC5G2OnXVMO6FUsvQlgUUXQ2itephWDLqDzbeCw==",
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-to-primitive": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-to-primitive/-/es-to-primitive-1.3.0.tgz",
      "integrity": "sha512-w+5mJ3GuFL+NjVtJlvydShqE1eN3h3PbI7/5LAsYJP/2qtuMXjfL2LpHSRqo4b4eSF5K/DH1JXKUAHSB2UW50g==",
      "license": "MIT",
      "dependencies": {
        "is-callable": "^1.2.7",
        "is-date-object": "^1.0.5",
        "is-symbol": "^1.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/escalade": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/escalade/-/escalade-3.2.0.tgz",
      "integrity": "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/escape-html": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/escape-html/-/escape-html-1.0.3.tgz",
      "integrity": "sha512-NiSupZ4OeuGwr68lGIeym/ksIZMJodUGOSCZ/FSnTxcrekbvqrgdUxlJOMpijaKZVjAJrWrGs/6Jy8OMuyj9ow==",
      "license": "MIT"
    },
    "node_modules/escape-string-regexp": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-4.0.0.tgz",
      "integrity": "sha512-TtpcNJ3XAzx3Gq8sWRzJaVajRs0uVxA2YAkdb1jm2YkPz4G6egUFAyA3n5vtEIZefPk5Wa4UXbKuS5fKkJWdgA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/escodegen": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/escodegen/-/escodegen-2.1.0.tgz",
      "integrity": "sha512-2NlIDTwUWJN0mRPQOdtQBzbUHvdGY2P1VXSyU83Q3xKxM7WHX2Ql8dKq782Q9TgQUNOLEzEYu9bzLNj1q88I5w==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esprima": "^4.0.1",
        "estraverse": "^5.2.0",
        "esutils": "^2.0.2"
      },
      "bin": {
        "escodegen": "bin/escodegen.js",
        "esgenerate": "bin/esgenerate.js"
      },
      "engines": {
        "node": ">=6.0"
      },
      "optionalDependencies": {
        "source-map": "~0.6.1"
      }
    },
    "node_modules/escodegen/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "optional": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/eslint": {
      "version": "8.57.1",
      "resolved": "https://registry.npmjs.org/eslint/-/eslint-8.57.1.tgz",
      "integrity": "sha512-ypowyDxpVSYpkXr9WPv2PAZCtNip1Mv5KTW0SCurXv/9iOpcrH9PaqUElksqEB6pChqHGDRCFTyrZlGhnLNGiA==",
      "deprecated": "This version is no longer supported. Please see https://eslint.org/version-support for other options.",
      "license": "MIT",
      "dependencies": {
        "@eslint-community/eslint-utils": "^4.2.0",
        "@eslint-community/regexpp": "^4.6.1",
        "@eslint/eslintrc": "^2.1.4",
        "@eslint/js": "8.57.1",
        "@humanwhocodes/config-array": "^0.13.0",
        "@humanwhocodes/module-importer": "^1.0.1",
        "@nodelib/fs.walk": "^1.2.8",
        "@ungap/structured-clone": "^1.2.0",
        "ajv": "^6.12.4",
        "chalk": "^4.0.0",
        "cross-spawn": "^7.0.2",
        "debug": "^4.3.2",
        "doctrine": "^3.0.0",
        "escape-string-regexp": "^4.0.0",
        "eslint-scope": "^7.2.2",
        "eslint-visitor-keys": "^3.4.3",
        "espree": "^9.6.1",
        "esquery": "^1.4.2",
        "esutils": "^2.0.2",
        "fast-deep-equal": "^3.1.3",
        "file-entry-cache": "^6.0.1",
        "find-up": "^5.0.0",
        "glob-parent": "^6.0.2",
        "globals": "^13.19.0",
        "graphemer": "^1.4.0",
        "ignore": "^5.2.0",
        "imurmurhash": "^0.1.4",
        "is-glob": "^4.0.0",
        "is-path-inside": "^3.0.3",
        "js-yaml": "^4.1.0",
        "json-stable-stringify-without-jsonify": "^1.0.1",
        "levn": "^0.4.1",
        "lodash.merge": "^4.6.2",
        "minimatch": "^3.1.2",
        "natural-compare": "^1.4.0",
        "optionator": "^0.9.3",
        "strip-ansi": "^6.0.1",
        "text-table": "^0.2.0"
      },
      "bin": {
        "eslint": "bin/eslint.js"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/eslint-config-react-app": {
      "version": "7.0.1",
      "resolved": "https://registry.npmjs.org/eslint-config-react-app/-/eslint-config-react-app-7.0.1.tgz",
      "integrity": "sha512-K6rNzvkIeHaTd8m/QEh1Zko0KI7BACWkkneSs6s9cKZC/J27X3eZR6Upt1jkmZ/4FK+XUOPPxMEN7+lbUXfSlA==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.16.0",
        "@babel/eslint-parser": "^7.16.3",
        "@rushstack/eslint-patch": "^1.1.0",
        "@typescript-eslint/eslint-plugin": "^5.5.0",
        "@typescript-eslint/parser": "^5.5.0",
        "babel-preset-react-app": "^10.0.1",
        "confusing-browser-globals": "^1.0.11",
        "eslint-plugin-flowtype": "^8.0.3",
        "eslint-plugin-import": "^2.25.3",
        "eslint-plugin-jest": "^25.3.0",
        "eslint-plugin-jsx-a11y": "^6.5.1",
        "eslint-plugin-react": "^7.27.1",
        "eslint-plugin-react-hooks": "^4.3.0",
        "eslint-plugin-testing-library": "^5.0.1"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "eslint": "^8.0.0"
      }
    },
    "node_modules/eslint-import-resolver-node": {
      "version": "0.3.9",
      "resolved": "https://registry.npmjs.org/eslint-import-resolver-node/-/eslint-import-resolver-node-0.3.9.tgz",
      "integrity": "sha512-WFj2isz22JahUv+B788TlO3N6zL3nNJGU8CcZbPZvVEkBPaJdCV4vy5wyghty5ROFbCRnm132v8BScu5/1BQ8g==",
      "license": "MIT",
      "dependencies": {
        "debug": "^3.2.7",
        "is-core-module": "^2.13.0",
        "resolve": "^1.22.4"
      }
    },
    "node_modules/eslint-import-resolver-node/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-module-utils": {
      "version": "2.12.1",
      "resolved": "https://registry.npmjs.org/eslint-module-utils/-/eslint-module-utils-2.12.1.tgz",
      "integrity": "sha512-L8jSWTze7K2mTg0vos/RuLRS5soomksDPoJLXIslC7c8Wmut3bx7CPpJijDcBZtxQ5lrbUdM+s0OlNbz0DCDNw==",
      "license": "MIT",
      "dependencies": {
        "debug": "^3.2.7"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependenciesMeta": {
        "eslint": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-module-utils/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-plugin-flowtype": {
      "version": "8.0.3",
      "resolved": "https://registry.npmjs.org/eslint-plugin-flowtype/-/eslint-plugin-flowtype-8.0.3.tgz",
      "integrity": "sha512-dX8l6qUL6O+fYPtpNRideCFSpmWOUVx5QcaGLVqe/vlDiBSe4vYljDWDETwnyFzpl7By/WVIu6rcrniCgH9BqQ==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "lodash": "^4.17.21",
        "string-natural-compare": "^3.0.1"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "@babel/plugin-syntax-flow": "^7.14.5",
        "@babel/plugin-transform-react-jsx": "^7.14.9",
        "eslint": "^8.1.0"
      }
    },
    "node_modules/eslint-plugin-import": {
      "version": "2.32.0",
      "resolved": "https://registry.npmjs.org/eslint-plugin-import/-/eslint-plugin-import-2.32.0.tgz",
      "integrity": "sha512-whOE1HFo/qJDyX4SnXzP4N6zOWn79WhnCUY/iDR0mPfQZO8wcYE4JClzI2oZrhBnnMUCBCHZhO6VQyoBU95mZA==",
      "license": "MIT",
      "dependencies": {
        "@rtsao/scc": "^1.1.0",
        "array-includes": "^3.1.9",
        "array.prototype.findlastindex": "^1.2.6",
        "array.prototype.flat": "^1.3.3",
        "array.prototype.flatmap": "^1.3.3",
        "debug": "^3.2.7",
        "doctrine": "^2.1.0",
        "eslint-import-resolver-node": "^0.3.9",
        "eslint-module-utils": "^2.12.1",
        "hasown": "^2.0.2",
        "is-core-module": "^2.16.1",
        "is-glob": "^4.0.3",
        "minimatch": "^3.1.2",
        "object.fromentries": "^2.0.8",
        "object.groupby": "^1.0.3",
        "object.values": "^1.2.1",
        "semver": "^6.3.1",
        "string.prototype.trimend": "^1.0.9",
        "tsconfig-paths": "^3.15.0"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependencies": {
        "eslint": "^2 || ^3 || ^4 || ^5 || ^6 || ^7.2.0 || ^8 || ^9"
      }
    },
    "node_modules/eslint-plugin-import/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-plugin-import/node_modules/doctrine": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/doctrine/-/doctrine-2.1.0.tgz",
      "integrity": "sha512-35mSku4ZXK0vfCuHEDAwt55dg2jNajHZ1odvF+8SSr82EsZY4QmXfuWso8oEd8zRhVObSN18aM0CjSdoBX7zIw==",
      "license": "Apache-2.0",
      "dependencies": {
        "esutils": "^2.0.2"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/eslint-plugin-import/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/eslint-plugin-jest": {
      "version": "25.7.0",
      "resolved": "https://registry.npmjs.org/eslint-plugin-jest/-/eslint-plugin-jest-25.7.0.tgz",
      "integrity": "sha512-PWLUEXeeF7C9QGKqvdSbzLOiLTx+bno7/HC9eefePfEb257QFHg7ye3dh80AZVkaa/RQsBB1Q/ORQvg2X7F0NQ==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/experimental-utils": "^5.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || >=16.0.0"
      },
      "peerDependencies": {
        "@typescript-eslint/eslint-plugin": "^4.0.0 || ^5.0.0",
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      },
      "peerDependenciesMeta": {
        "@typescript-eslint/eslint-plugin": {
          "optional": true
        },
        "jest": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-plugin-jsx-a11y": {
      "version": "6.10.2",
      "resolved": "https://registry.npmjs.org/eslint-plugin-jsx-a11y/-/eslint-plugin-jsx-a11y-6.10.2.tgz",
      "integrity": "sha512-scB3nz4WmG75pV8+3eRUQOHZlNSUhFNq37xnpgRkCCELU3XMvXAxLk1eqWWyE22Ki4Q01Fnsw9BA3cJHDPgn2Q==",
      "license": "MIT",
      "dependencies": {
        "aria-query": "^5.3.2",
        "array-includes": "^3.1.8",
        "array.prototype.flatmap": "^1.3.2",
        "ast-types-flow": "^0.0.8",
        "axe-core": "^4.10.0",
        "axobject-query": "^4.1.0",
        "damerau-levenshtein": "^1.0.8",
        "emoji-regex": "^9.2.2",
        "hasown": "^2.0.2",
        "jsx-ast-utils": "^3.3.5",
        "language-tags": "^1.0.9",
        "minimatch": "^3.1.2",
        "object.fromentries": "^2.0.8",
        "safe-regex-test": "^1.0.3",
        "string.prototype.includes": "^2.0.1"
      },
      "engines": {
        "node": ">=4.0"
      },
      "peerDependencies": {
        "eslint": "^3 || ^4 || ^5 || ^6 || ^7 || ^8 || ^9"
      }
    },
    "node_modules/eslint-plugin-react": {
      "version": "7.37.5",
      "resolved": "https://registry.npmjs.org/eslint-plugin-react/-/eslint-plugin-react-7.37.5.tgz",
      "integrity": "sha512-Qteup0SqU15kdocexFNAJMvCJEfa2xUKNV4CC1xsVMrIIqEy3SQ/rqyxCWNzfrd3/ldy6HMlD2e0JDVpDg2qIA==",
      "license": "MIT",
      "dependencies": {
        "array-includes": "^3.1.8",
        "array.prototype.findlast": "^1.2.5",
        "array.prototype.flatmap": "^1.3.3",
        "array.prototype.tosorted": "^1.1.4",
        "doctrine": "^2.1.0",
        "es-iterator-helpers": "^1.2.1",
        "estraverse": "^5.3.0",
        "hasown": "^2.0.2",
        "jsx-ast-utils": "^2.4.1 || ^3.0.0",
        "minimatch": "^3.1.2",
        "object.entries": "^1.1.9",
        "object.fromentries": "^2.0.8",
        "object.values": "^1.2.1",
        "prop-types": "^15.8.1",
        "resolve": "^2.0.0-next.5",
        "semver": "^6.3.1",
        "string.prototype.matchall": "^4.0.12",
        "string.prototype.repeat": "^1.0.0"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependencies": {
        "eslint": "^3 || ^4 || ^5 || ^6 || ^7 || ^8 || ^9.7"
      }
    },
    "node_modules/eslint-plugin-react-hooks": {
      "version": "4.6.2",
      "resolved": "https://registry.npmjs.org/eslint-plugin-react-hooks/-/eslint-plugin-react-hooks-4.6.2.tgz",
      "integrity": "sha512-QzliNJq4GinDBcD8gPB5v0wh6g8q3SUi6EFF0x8N/BL9PoVs0atuGc47ozMRyOWAKdwaZ5OnbOEa3WR+dSGKuQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "eslint": "^3.0.0 || ^4.0.0 || ^5.0.0 || ^6.0.0 || ^7.0.0 || ^8.0.0-0"
      }
    },
    "node_modules/eslint-plugin-react/node_modules/doctrine": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/doctrine/-/doctrine-2.1.0.tgz",
      "integrity": "sha512-35mSku4ZXK0vfCuHEDAwt55dg2jNajHZ1odvF+8SSr82EsZY4QmXfuWso8oEd8zRhVObSN18aM0CjSdoBX7zIw==",
      "license": "Apache-2.0",
      "dependencies": {
        "esutils": "^2.0.2"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/eslint-plugin-react/node_modules/resolve": {
      "version": "2.0.0-next.6",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-2.0.0-next.6.tgz",
      "integrity": "sha512-3JmVl5hMGtJ3kMmB3zi3DL25KfkCEyy3Tw7Gmw7z5w8M9WlwoPFnIvwChzu1+cF3iaK3sp18hhPz8ANeimdJfA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "is-core-module": "^2.16.1",
        "node-exports-info": "^1.6.0",
        "object-keys": "^1.1.1",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/eslint-plugin-react/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/eslint-plugin-testing-library": {
      "version": "5.11.1",
      "resolved": "https://registry.npmjs.org/eslint-plugin-testing-library/-/eslint-plugin-testing-library-5.11.1.tgz",
      "integrity": "sha512-5eX9e1Kc2PqVRed3taaLnAAqPZGEX75C+M/rXzUAI3wIg/ZxzUm1OVAwfe/O+vE+6YXOLetSe9g5GKD2ecXipw==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/utils": "^5.58.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0",
        "npm": ">=6"
      },
      "peerDependencies": {
        "eslint": "^7.5.0 || ^8.0.0"
      }
    },
    "node_modules/eslint-scope": {
      "version": "7.2.2",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-7.2.2.tgz",
      "integrity": "sha512-dOt21O7lTMhDM+X9mB4GX+DZrZtCUJPL/wlcTqxyrx5IvO0IYtILdtrQGQp+8n5S0gwSVmOf9NQrjMOgfQZlIg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^5.2.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/eslint-visitor-keys": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-3.4.3.tgz",
      "integrity": "sha512-wpc+LXeiyiisxPlEkUzU6svyS1frIO3Mgxj1fdy7Pm8Ygzguax2N3Fa/D/ag1WqbOprdI+uY6wMUl8/a2G+iag==",
      "license": "Apache-2.0",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/eslint-webpack-plugin": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/eslint-webpack-plugin/-/eslint-webpack-plugin-3.2.0.tgz",
      "integrity": "sha512-avrKcGncpPbPSUHX6B3stNGzkKFto3eL+DKM4+VyMrVnhPc3vRczVlCq3uhuFOdRvDHTVXuzwk1ZKUrqDQHQ9w==",
      "license": "MIT",
      "dependencies": {
        "@types/eslint": "^7.29.0 || ^8.4.1",
        "jest-worker": "^28.0.2",
        "micromatch": "^4.0.5",
        "normalize-path": "^3.0.0",
        "schema-utils": "^4.0.0"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "eslint": "^7.0.0 || ^8.0.0",
        "webpack": "^5.0.0"
      }
    },
    "node_modules/eslint-webpack-plugin/node_modules/jest-worker": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/jest-worker/-/jest-worker-28.1.3.tgz",
      "integrity": "sha512-CqRA220YV/6jCo8VWvAt1KKx6eek1VIHMPeLEbpcfSfkEeWyBNppynM/o6q+Wmw+sOhos2ml34wZbSX3G13//g==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "merge-stream": "^2.0.0",
        "supports-color": "^8.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/eslint-webpack-plugin/node_modules/supports-color": {
      "version": "8.1.1",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-8.1.1.tgz",
      "integrity": "sha512-MpUEN2OodtUzxvKQl72cUF7RQ5EiHsGvSsVG0ia9c5RbWGL2CI4C7EpPS8UTBIplnlzZiNuV56w+FuNxy3ty2Q==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/supports-color?sponsor=1"
      }
    },
    "node_modules/eslint/node_modules/argparse": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/argparse/-/argparse-2.0.1.tgz",
      "integrity": "sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q==",
      "license": "Python-2.0"
    },
    "node_modules/eslint/node_modules/find-up": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-5.0.0.tgz",
      "integrity": "sha512-78/PXT1wlLLDgTzDs7sjq9hzz0vXD+zn+7wypEe4fXQxCmdmqfGsEPQxmiCSQI3ajFV91bVSsvNtrJRiW6nGng==",
      "license": "MIT",
      "dependencies": {
        "locate-path": "^6.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint/node_modules/js-yaml": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/js-yaml/-/js-yaml-4.1.1.tgz",
      "integrity": "sha512-qQKT4zQxXl8lLwBtHMWwaTcGfFOZviOJet3Oy/xmGk2gZH677CJM9EvtfdSkgWcATZhj/55JZ0rmy3myCT5lsA==",
      "license": "MIT",
      "dependencies": {
        "argparse": "^2.0.1"
      },
      "bin": {
        "js-yaml": "bin/js-yaml.js"
      }
    },
    "node_modules/eslint/node_modules/locate-path": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-6.0.0.tgz",
      "integrity": "sha512-iPZK6eYjbxRu3uB4/WZ3EsEIMJFMqAoopl3R+zuq0UjcAm/MO6KCweDgPfP3elTztoKP3KtnVHxTn2NHBSDVUw==",
      "license": "MIT",
      "dependencies": {
        "p-locate": "^5.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint/node_modules/p-limit": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-3.1.0.tgz",
      "integrity": "sha512-TYOanM3wGwNGsZN2cVTYPArw454xnXj5qmWF1bEoAc4+cU/ol7GVh7odevjp1FNHduHc3KZMcFduxU5Xc6uJRQ==",
      "license": "MIT",
      "dependencies": {
        "yocto-queue": "^0.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint/node_modules/p-locate": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-5.0.0.tgz",
      "integrity": "sha512-LaNjtRWUBY++zB5nE/NwcaoMylSPk+S+ZHNB1TzdbMJMny6dynpAGt7X/tl/QYq3TIeE6nxHppbo2LGymrG5Pw==",
      "license": "MIT",
      "dependencies": {
        "p-limit": "^3.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/espree": {
      "version": "9.6.1",
      "resolved": "https://registry.npmjs.org/espree/-/espree-9.6.1.tgz",
      "integrity": "sha512-oruZaFkjorTpF32kDSI5/75ViwGeZginGGy2NoOSg3Q9bnwlnmDm4HLnkl0RE3n+njDXR037aY1+x58Z/zFdwQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "acorn": "^8.9.0",
        "acorn-jsx": "^5.3.2",
        "eslint-visitor-keys": "^3.4.1"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/esprima": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/esprima/-/esprima-4.0.1.tgz",
      "integrity": "sha512-eGuFFw7Upda+g4p+QHvnW0RyTX/SVeJBDM/gCtMARO0cLuT2HcEKnTPvhjV6aGeqrCB/sbNop0Kszm0jsaWU4A==",
      "license": "BSD-2-Clause",
      "bin": {
        "esparse": "bin/esparse.js",
        "esvalidate": "bin/esvalidate.js"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/esquery": {
      "version": "1.7.0",
      "resolved": "https://registry.npmjs.org/esquery/-/esquery-1.7.0.tgz",
      "integrity": "sha512-Ap6G0WQwcU/LHsvLwON1fAQX9Zp0A2Y6Y/cJBl9r/JbW90Zyg4/zbG6zzKa2OTALELarYHmKu0GhpM5EO+7T0g==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "estraverse": "^5.1.0"
      },
      "engines": {
        "node": ">=0.10"
      }
    },
    "node_modules/esrecurse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/esrecurse/-/esrecurse-4.3.0.tgz",
      "integrity": "sha512-KmfKL3b6G+RXvP8N1vr3Tq1kL/oCFgn2NYXEtqP8/L3pKapUA4G8cFVaoF3SU323CD4XypR/ffioHmkti6/Tag==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "estraverse": "^5.2.0"
      },
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/estraverse": {
      "version": "5.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-5.3.0.tgz",
      "integrity": "sha512-MMdARuVEQziNTeJD8DgMqmhwR11BRQ/cBP+pLtYdSTnf3MIO8fFeiINEbX36ZdNlfU/7A9f3gUw49B3oQsvwBA==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/estree-walker": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/estree-walker/-/estree-walker-1.0.1.tgz",
      "integrity": "sha512-1fMXF3YP4pZZVozF8j/ZLfvnR8NSIljt56UhbZ5PeeDmmGHpgpdwQt7ITlGvYaQukCvuBRMLEiKiYC+oeIg4cg==",
      "license": "MIT"
    },
    "node_modules/esutils": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/esutils/-/esutils-2.0.3.tgz",
      "integrity": "sha512-kVscqXk4OCp68SZ0dkgEKVi6/8ij300KBWTJq32P/dYeWTSwK41WyTxalN1eRmA5Z9UU/LX9D7FWSmV9SAYx6g==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/etag": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/etag/-/etag-1.8.1.tgz",
      "integrity": "sha512-aIL5Fx7mawVa300al2BnEE4iNvo1qETxLrPI/o05L7z6go7fCw1J6EQmbK4FmJ2AS7kgVF/KEZWufBfdClMcPg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/eventemitter3": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/eventemitter3/-/eventemitter3-4.0.7.tgz",
      "integrity": "sha512-8guHBZCwKnFhYdHr2ysuRWErTwhoN2X8XELRlrRwpmfeY2jjuUN4taQMsULKUVo1K4DvZl+0pgfyoysHxvmvEw==",
      "license": "MIT"
    },
    "node_modules/events": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/events/-/events-3.3.0.tgz",
      "integrity": "sha512-mQw+2fkQbALzQ7V0MY0IqdnXNOeTtP4r0lN9z7AAawCXgqea7bDii20AYrIBrFd/Hx0M2Ocz6S111CaFkUcb0Q==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8.x"
      }
    },
    "node_modules/execa": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/execa/-/execa-5.1.1.tgz",
      "integrity": "sha512-8uSpZZocAZRBAPIEINJj3Lo9HyGitllczc27Eh5YYojjMFMn8yHMDMaUHE2Jqfq05D/wucwI4JGURyXt1vchyg==",
      "license": "MIT",
      "dependencies": {
        "cross-spawn": "^7.0.3",
        "get-stream": "^6.0.0",
        "human-signals": "^2.1.0",
        "is-stream": "^2.0.0",
        "merge-stream": "^2.0.0",
        "npm-run-path": "^4.0.1",
        "onetime": "^5.1.2",
        "signal-exit": "^3.0.3",
        "strip-final-newline": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sindresorhus/execa?sponsor=1"
      }
    },
    "node_modules/exit": {
      "version": "0.1.2",
      "resolved": "https://registry.npmjs.org/exit/-/exit-0.1.2.tgz",
      "integrity": "sha512-Zk/eNKV2zbjpKzrsQ+n1G6poVbErQxJ0LBOJXaKZ1EViLzH+hrLu9cdXI4zw9dBQJslwBEpbQ2P1oS7nDxs6jQ==",
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/expect": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/expect/-/expect-27.5.1.tgz",
      "integrity": "sha512-E1q5hSUG2AmYQwQJ041nvgpkODHQvB+RKlB4IYdru6uJsyFTRyZAP463M+1lINorwbqAmUggi6+WwkD8lCS/Dw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "jest-matcher-utils": "^27.5.1",
        "jest-message-util": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/express": {
      "version": "4.22.1",
      "resolved": "https://registry.npmjs.org/express/-/express-4.22.1.tgz",
      "integrity": "sha512-F2X8g9P1X7uCPZMA3MVf9wcTqlyNp7IhH5qPCI0izhaOIYXaW9L535tGA3qmjRzpH+bZczqq7hVKxTR4NWnu+g==",
      "license": "MIT",
      "dependencies": {
        "accepts": "~1.3.8",
        "array-flatten": "1.1.1",
        "body-parser": "~1.20.3",
        "content-disposition": "~0.5.4",
        "content-type": "~1.0.4",
        "cookie": "~0.7.1",
        "cookie-signature": "~1.0.6",
        "debug": "2.6.9",
        "depd": "2.0.0",
        "encodeurl": "~2.0.0",
        "escape-html": "~1.0.3",
        "etag": "~1.8.1",
        "finalhandler": "~1.3.1",
        "fresh": "~0.5.2",
        "http-errors": "~2.0.0",
        "merge-descriptors": "1.0.3",
        "methods": "~1.1.2",
        "on-finished": "~2.4.1",
        "parseurl": "~1.3.3",
        "path-to-regexp": "~0.1.12",
        "proxy-addr": "~2.0.7",
        "qs": "~6.14.0",
        "range-parser": "~1.2.1",
        "safe-buffer": "5.2.1",
        "send": "~0.19.0",
        "serve-static": "~1.16.2",
        "setprototypeof": "1.2.0",
        "statuses": "~2.0.1",
        "type-is": "~1.6.18",
        "utils-merge": "1.0.1",
        "vary": "~1.1.2"
      },
      "engines": {
        "node": ">= 0.10.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/express/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/express/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/fast-deep-equal": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/fast-deep-equal/-/fast-deep-equal-3.1.3.tgz",
      "integrity": "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==",
      "license": "MIT"
    },
    "node_modules/fast-glob": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/fast-glob/-/fast-glob-3.3.3.tgz",
      "integrity": "sha512-7MptL8U0cqcFdzIzwOTHoilX9x5BrNqye7Z/LuC7kCMRio1EMSyqRK3BEAUD7sXRq4iT4AzTVuZdhgQ2TCvYLg==",
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "^2.0.2",
        "@nodelib/fs.walk": "^1.2.3",
        "glob-parent": "^5.1.2",
        "merge2": "^1.3.0",
        "micromatch": "^4.0.8"
      },
      "engines": {
        "node": ">=8.6.0"
      }
    },
    "node_modules/fast-glob/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/fast-json-stable-stringify": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/fast-json-stable-stringify/-/fast-json-stable-stringify-2.1.0.tgz",
      "integrity": "sha512-lhd/wF+Lk98HZoTCtlVraHtfh5XYijIjalXck7saUtuanSDyLMxnHhSXEDJqHxD7msR8D0uCmqlkwjCV8xvwHw==",
      "license": "MIT"
    },
    "node_modules/fast-levenshtein": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/fast-levenshtein/-/fast-levenshtein-2.0.6.tgz",
      "integrity": "sha512-DCXu6Ifhqcks7TZKY3Hxp3y6qphY5SJZmrWMDrKcERSOXWQdMhU9Ig/PYrzyw/ul9jOIyh0N4M0tbC5hodg8dw==",
      "license": "MIT"
    },
    "node_modules/fast-uri": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/fast-uri/-/fast-uri-3.1.0.tgz",
      "integrity": "sha512-iPeeDKJSWf4IEOasVVrknXpaBV0IApz/gp7S2bb7Z4Lljbl2MGJRqInZiUrQwV16cpzw/D3S5j5Julj/gT52AA==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/fastify"
        },
        {
          "type": "opencollective",
          "url": "https://opencollective.com/fastify"
        }
      ],
      "license": "BSD-3-Clause"
    },
    "node_modules/fastq": {
      "version": "1.20.1",
      "resolved": "https://registry.npmjs.org/fastq/-/fastq-1.20.1.tgz",
      "integrity": "sha512-GGToxJ/w1x32s/D2EKND7kTil4n8OVk/9mycTc4VDza13lOvpUZTGX3mFSCtV9ksdGBVzvsyAVLM6mHFThxXxw==",
      "license": "ISC",
      "dependencies": {
        "reusify": "^1.0.4"
      }
    },
    "node_modules/faye-websocket": {
      "version": "0.11.4",
      "resolved": "https://registry.npmjs.org/faye-websocket/-/faye-websocket-0.11.4.tgz",
      "integrity": "sha512-CzbClwlXAuiRQAlUyfqPgvPoNKTckTPGfwZV4ZdAhVcP2lh9KUxJg2b5GkE7XbjKQ3YJnQ9z6D9ntLAlB+tP8g==",
      "license": "Apache-2.0",
      "dependencies": {
        "websocket-driver": ">=0.5.1"
      },
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/fb-watchman": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/fb-watchman/-/fb-watchman-2.0.2.tgz",
      "integrity": "sha512-p5161BqbuCaSnB8jIbzQHOlpgsPmK5rJVDfDKO91Axs5NC1uu3HRQm6wt9cd9/+GtQQIO53JdGXXoyDpTAsgYA==",
      "license": "Apache-2.0",
      "dependencies": {
        "bser": "2.1.1"
      }
    },
    "node_modules/file-entry-cache": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/file-entry-cache/-/file-entry-cache-6.0.1.tgz",
      "integrity": "sha512-7Gps/XWymbLk2QLYK4NzpMOrYjMhdIxXuIvy2QBsLE6ljuodKvdkWs/cpyJJ3CVIVpH0Oi1Hvg1ovbMzLdFBBg==",
      "license": "MIT",
      "dependencies": {
        "flat-cache": "^3.0.4"
      },
      "engines": {
        "node": "^10.12.0 || >=12.0.0"
      }
    },
    "node_modules/file-loader": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/file-loader/-/file-loader-6.2.0.tgz",
      "integrity": "sha512-qo3glqyTa61Ytg4u73GultjHGjdRyig3tG6lPtyX/jOEJvHif9uB0/OCI2Kif6ctF3caQTW2G5gym21oAsI4pw==",
      "license": "MIT",
      "dependencies": {
        "loader-utils": "^2.0.0",
        "schema-utils": "^3.0.0"
      },
      "engines": {
        "node": ">= 10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^4.0.0 || ^5.0.0"
      }
    },
    "node_modules/file-loader/node_modules/schema-utils": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/schema-utils/-/schema-utils-3.3.0.tgz",
      "integrity": "sha512-pN/yOAvcC+5rQ5nERGuwrjLlYvLTbCibnZ1I7B1LaiAz9BRBlE9GMgE/eqV30P7aJQUf7Ddimy/RsbYO/GrVGg==",
      "license": "MIT",
      "dependencies": {
        "@types/json-schema": "^7.0.8",
        "ajv": "^6.12.5",
        "ajv-keywords": "^3.5.2"
      },
      "engines": {
        "node": ">= 10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/filelist": {
      "version": "1.0.6",
      "resolved": "https://registry.npmjs.org/filelist/-/filelist-1.0.6.tgz",
      "integrity": "sha512-5giy2PkLYY1cP39p17Ech+2xlpTRL9HLspOfEgm0L6CwBXBTgsK5ou0JtzYuepxkaQ/tvhCFIJ5uXo0OrM2DxA==",
      "license": "Apache-2.0",
      "dependencies": {
        "minimatch": "^5.0.1"
      }
    },
    "node_modules/filelist/node_modules/brace-expansion": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.0.2.tgz",
      "integrity": "sha512-Jt0vHyM+jmUBqojB7E1NIYadt0vI0Qxjxd2TErW94wDz+E2LAm5vKMXXwg6ZZBTHPuUlDgQHKXvjGBdfcF1ZDQ==",
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^1.0.0"
      }
    },
    "node_modules/filelist/node_modules/minimatch": {
      "version": "5.1.9",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-5.1.9.tgz",
      "integrity": "sha512-7o1wEA2RyMP7Iu7GNba9vc0RWWGACJOCZBJX2GJWip0ikV+wcOsgVuY9uE8CPiyQhkGFSlhuSkZPavN7u1c2Fw==",
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^2.0.1"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/filesize": {
      "version": "8.0.7",
      "resolved": "https://registry.npmjs.org/filesize/-/filesize-8.0.7.tgz",
      "integrity": "sha512-pjmC+bkIF8XI7fWaH8KxHcZL3DPybs1roSKP4rKDvy20tAWwIObE4+JIseG2byfGKhud5ZnM4YSGKBz7Sh0ndQ==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">= 0.4.0"
      }
    },
    "node_modules/fill-range": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/fill-range/-/fill-range-7.1.1.tgz",
      "integrity": "sha512-YsGpe3WHLK8ZYi4tWDg2Jy3ebRz2rXowDxnld4bkQB00cc/1Zw9AWnC0i9ztDJitivtQvaI9KaLyKrc+hBW0yg==",
      "license": "MIT",
      "dependencies": {
        "to-regex-range": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/finalhandler": {
      "version": "1.3.2",
      "resolved": "https://registry.npmjs.org/finalhandler/-/finalhandler-1.3.2.tgz",
      "integrity": "sha512-aA4RyPcd3badbdABGDuTXCMTtOneUCAYH/gxoYRTZlIJdF0YPWuGqiAsIrhNnnqdXGswYk6dGujem4w80UJFhg==",
      "license": "MIT",
      "dependencies": {
        "debug": "2.6.9",
        "encodeurl": "~2.0.0",
        "escape-html": "~1.0.3",
        "on-finished": "~2.4.1",
        "parseurl": "~1.3.3",
        "statuses": "~2.0.2",
        "unpipe": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/finalhandler/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/finalhandler/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/find-cache-dir": {
      "version": "3.3.2",
      "resolved": "https://registry.npmjs.org/find-cache-dir/-/find-cache-dir-3.3.2.tgz",
      "integrity": "sha512-wXZV5emFEjrridIgED11OoUKLxiYjAcqot/NJdAkOhlJ+vGzwhOAfcG5OX1jP+S0PcjEn8bdMJv+g2jwQ3Onig==",
      "license": "MIT",
      "dependencies": {
        "commondir": "^1.0.1",
        "make-dir": "^3.0.2",
        "pkg-dir": "^4.1.0"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/avajs/find-cache-dir?sponsor=1"
      }
    },
    "node_modules/find-up": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-4.1.0.tgz",
      "integrity": "sha512-PpOwAdQ/YlXQ2vj8a3h8IipDuYRi3wceVQQGYWxNINccq40Anw7BlsEXCMbt1Zt+OLA6Fq9suIpIWD0OsnISlw==",
      "license": "MIT",
      "dependencies": {
        "locate-path": "^5.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/flat-cache": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/flat-cache/-/flat-cache-3.2.0.tgz",
      "integrity": "sha512-CYcENa+FtcUKLmhhqyctpclsq7QF38pKjZHsGNiSQF5r4FtoKDWabFDl3hzaEQMvT1LHEysw5twgLvpYYb4vbw==",
      "license": "MIT",
      "dependencies": {
        "flatted": "^3.2.9",
        "keyv": "^4.5.3",
        "rimraf": "^3.0.2"
      },
      "engines": {
        "node": "^10.12.0 || >=12.0.0"
      }
    },
    "node_modules/flatted": {
      "version": "3.4.1",
      "resolved": "https://registry.npmjs.org/flatted/-/flatted-3.4.1.tgz",
      "integrity": "sha512-IxfVbRFVlV8V/yRaGzk0UVIcsKKHMSfYw66T/u4nTwlWteQePsxe//LjudR1AMX4tZW3WFCh3Zqa/sjlqpbURQ==",
      "license": "ISC"
    },
    "node_modules/follow-redirects": {
      "version": "1.15.11",
      "resolved": "https://registry.npmjs.org/follow-redirects/-/follow-redirects-1.15.11.tgz",
      "integrity": "sha512-deG2P0JfjrTxl50XGCDyfI97ZGVCxIpfKYmfyrQ54n5FO/0gfIES8C/Psl6kWVDolizcaaxZJnTS0QSMxvnsBQ==",
      "funding": [
        {
          "type": "individual",
          "url": "https://github.com/sponsors/RubenVerborgh"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": ">=4.0"
      },
      "peerDependenciesMeta": {
        "debug": {
          "optional": true
        }
      }
    },
    "node_modules/for-each": {
      "version": "0.3.5",
      "resolved": "https://registry.npmjs.org/for-each/-/for-each-0.3.5.tgz",
      "integrity": "sha512-dKx12eRCVIzqCxFGplyFKJMPvLEWgmNtUrpTiJIR5u97zEhRG8ySrtboPHZXx7daLxQVrl643cTzbab2tkQjxg==",
      "license": "MIT",
      "dependencies": {
        "is-callable": "^1.2.7"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin": {
      "version": "6.5.3",
      "resolved": "https://registry.npmjs.org/fork-ts-checker-webpack-plugin/-/fork-ts-checker-webpack-plugin-6.5.3.tgz",
      "integrity": "sha512-SbH/l9ikmMWycd5puHJKTkZJKddF4iRLyW3DeZ08HTI7NGyLS38MXd/KGgeWumQO7YNQbW2u/NtPT2YowbPaGQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.8.3",
        "@types/json-schema": "^7.0.5",
        "chalk": "^4.1.0",
        "chokidar": "^3.4.2",
        "cosmiconfig": "^6.0.0",
        "deepmerge": "^4.2.2",
        "fs-extra": "^9.0.0",
        "glob": "^7.1.6",
        "memfs": "^3.1.2",
        "minimatch": "^3.0.4",
        "schema-utils": "2.7.0",
        "semver": "^7.3.2",
        "tapable": "^1.0.0"
      },
      "engines": {
        "node": ">=10",
        "yarn": ">=1.0.0"
      },
      "peerDependencies": {
        "eslint": ">= 6",
        "typescript": ">= 2.7",
        "vue-template-compiler": "*",
        "webpack": ">= 4"
      },
      "peerDependenciesMeta": {
        "eslint": {
          "optional": true
        },
        "vue-template-compiler": {
          "optional": true
        }
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin/node_modules/cosmiconfig": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/cosmiconfig/-/cosmiconfig-6.0.0.tgz",
      "integrity": "sha512-xb3ZL6+L8b9JLLCx3ZdoZy4+2ECphCMo2PwqgP1tlfVq6M6YReyzBJtvWWtbDSpNr9hn96pkCiZqUcFEc+54Qg==",
      "license": "MIT",
      "dependencies": {
        "@types/parse-json": "^4.0.0",
        "import-fresh": "^3.1.0",
        "parse-json": "^5.0.0",
        "path-type": "^4.0.0",
        "yaml": "^1.7.2"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin/node_modules/fs-extra": {
      "version": "9.1.0",
      "resolved": "https://registry.npmjs.org/fs-extra/-/fs-extra-9.1.0.tgz",
      "integrity": "sha512-hcg3ZmepS30/7BSFqRvoo3DOMQu7IjqxO5nCDt+zM9XWjb33Wg7ziNT+Qvqbuc3+gWpzO02JubVyk2G4Zvo1OQ==",
      "license": "MIT",
      "dependencies": {
        "at-least-node": "^1.0.0",
        "graceful-fs": "^4.2.0",
        "jsonfile": "^6.0.1",
        "universalify": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin/node_modules/schema-utils": {
      "version": "2.7.0",
      "resolved": "https://registry.npmjs.org/schema-utils/-/schema-utils-2.7.0.tgz",
      "integrity": "sha512-0ilKFI6QQF5nxDZLFn2dMjvc4hjg/Wkg7rHd3jK6/A4a1Hl9VFdQWvgB1UMGoU94pad1P/8N7fMcEnLnSiju8A==",
      "license": "MIT",
      "dependencies": {
        "@types/json-schema": "^7.0.4",
        "ajv": "^6.12.2",
        "ajv-keywords": "^3.4.1"
      },
      "engines": {
        "node": ">= 8.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin/node_modules/tapable": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/tapable/-/tapable-1.1.3.tgz",
      "integrity": "sha512-4WK/bYZmj8xLr+HUCODHGF1ZFzsYffasLUgEiMBY4fgtltdO6B4WJtlSbPaDTLpYTcGVwM2qLnFTICEcNxs3kA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/form-data": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/form-data/-/form-data-3.0.4.tgz",
      "integrity": "sha512-f0cRzm6dkyVYV3nPoooP8XlccPQukegwhAnpoLcXy+X+A8KfpGOoXwDr9FLZd3wzgLaBGQBE3lY93Zm/i1JvIQ==",
      "license": "MIT",
      "dependencies": {
        "asynckit": "^0.4.0",
        "combined-stream": "^1.0.8",
        "es-set-tostringtag": "^2.1.0",
        "hasown": "^2.0.2",
        "mime-types": "^2.1.35"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/forwarded": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/forwarded/-/forwarded-0.2.0.tgz",
      "integrity": "sha512-buRG0fpBtRHSTCOASe6hD258tEubFoRLb4ZNA6NxMVHNw2gOcwHo9wyablzMzOA5z9xA9L1KNjk/Nt6MT9aYow==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/fraction.js": {
      "version": "5.3.4",
      "resolved": "https://registry.npmjs.org/fraction.js/-/fraction.js-5.3.4.tgz",
      "integrity": "sha512-1X1NTtiJphryn/uLQz3whtY6jK3fTqoE3ohKs0tT+Ujr1W59oopxmoEh7Lu5p6vBaPbgoM0bzveAW4Qi5RyWDQ==",
      "license": "MIT",
      "engines": {
        "node": "*"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/rawify"
      }
    },
    "node_modules/fresh": {
      "version": "0.5.2",
      "resolved": "https://registry.npmjs.org/fresh/-/fresh-0.5.2.tgz",
      "integrity": "sha512-zJ2mQYM18rEFOudeV4GShTGIQ7RbzA7ozbU9I/XBpm7kqgMywgmylMwXHxZJmkVoYkna9d2pVXVXPdYTP9ej8Q==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/fs-extra": {
      "version": "10.1.0",
      "resolved": "https://registry.npmjs.org/fs-extra/-/fs-extra-10.1.0.tgz",
      "integrity": "sha512-oRXApq54ETRj4eMiFzGnHWGy+zo5raudjuxN0b8H7s/RU2oW0Wvsx9O0ACRN/kRq9E8Vu/ReskGB5o3ji+FzHQ==",
      "license": "MIT",
      "dependencies": {
        "graceful-fs": "^4.2.0",
        "jsonfile": "^6.0.1",
        "universalify": "^2.0.0"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/fs-monkey": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/fs-monkey/-/fs-monkey-1.1.0.tgz",
      "integrity": "sha512-QMUezzXWII9EV5aTFXW1UBVUO77wYPpjqIF8/AviUCThNeSYZykpoTixUeaNNBwmCev0AMDWMAni+f8Hxb1IFw==",
      "license": "Unlicense"
    },
    "node_modules/fs.realpath": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/fs.realpath/-/fs.realpath-1.0.0.tgz",
      "integrity": "sha512-OO0pH2lK6a0hZnAdau5ItzHPI6pUlvI7jMVnxUQRtw4owF2wk8lOSabtGDCTP4Ggrg2MbGnWO9X8K1t4+fGMDw==",
      "license": "ISC"
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/function.prototype.name": {
      "version": "1.1.8",
      "resolved": "https://registry.npmjs.org/function.prototype.name/-/function.prototype.name-1.1.8.tgz",
      "integrity": "sha512-e5iwyodOHhbMr/yNrc7fDYG4qlbIvI5gajyzPnb5TCwyhjApznQh1BMFou9b30SevY43gCJKXycoCBjMbsuW0Q==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "functions-have-names": "^1.2.3",
        "hasown": "^2.0.2",
        "is-callable": "^1.2.7"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/functions-have-names": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/functions-have-names/-/functions-have-names-1.2.3.tgz",
      "integrity": "sha512-xckBUXyTIqT97tq2x2AMb+g163b5JFysYk0x4qxNFwbfQkmNZoiRHb6sPzI9/QV33WeuvVYBUIiD4NzNIyqaRQ==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/generator-function": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/generator-function/-/generator-function-2.0.1.tgz",
      "integrity": "sha512-SFdFmIJi+ybC0vjlHN0ZGVGHc3lgE0DxPAT0djjVg+kjOnSqclqmj0KQ7ykTOLP6YxoqOvuAODGdcHJn+43q3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/gensync": {
      "version": "1.0.0-beta.2",
      "resolved": "https://registry.npmjs.org/gensync/-/gensync-1.0.0-beta.2.tgz",
      "integrity": "sha512-3hN7NaskYvMDLQY55gnW3NQ+mesEAepTqlg+VEbj7zzqEMBVNhzcGYYeqFo/TlYz6eQiFcp1HcsCZO+nGgS8zg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/get-caller-file": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/get-caller-file/-/get-caller-file-2.0.5.tgz",
      "integrity": "sha512-DyFP3BM/3YHTQOCUL/w0OZHR0lpKeGrxotcHWcqNEdnltqFwXVfhEBQ94eIo34AfQpo0rGki4cyIiftY06h2Fg==",
      "license": "ISC",
      "engines": {
        "node": "6.* || 8.* || >= 10.*"
      }
    },
    "node_modules/get-intrinsic": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.3.0.tgz",
      "integrity": "sha512-9fSjSaos/fRIVIp+xSJlE6lfwhES7LNtKaCBIamHsjr2na1BiABJPo0mOjjz8GJDURarmCPGqaiVg5mfjb98CQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "function-bind": "^1.1.2",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-own-enumerable-property-symbols": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/get-own-enumerable-property-symbols/-/get-own-enumerable-property-symbols-3.0.2.tgz",
      "integrity": "sha512-I0UBV/XOz1XkIJHEUDMZAbzCThU/H8DxmSfmdGcKPnVhu2VfFqr34jr9777IyaTYvxjedWhqVIilEDsCdP5G6g==",
      "license": "ISC"
    },
    "node_modules/get-package-type": {
      "version": "0.1.0",
      "resolved": "https://registry.npmjs.org/get-package-type/-/get-package-type-0.1.0.tgz",
      "integrity": "sha512-pjzuKtY64GYfWizNAJ0fr9VqttZkNiK2iS430LtIHzjBEr6bX8Am2zm4sW4Ro5wjWW5cAlRL1qAMTcXbjNAO2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/get-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/get-proto/-/get-proto-1.0.1.tgz",
      "integrity": "sha512-sTSfBjoXBp89JvIKIefqw7U2CCebsc74kiY6awiGogKtoSGbgjYE/G/+l9sF3MWFPNc9IcoOC4ODfKHfxFmp0g==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/get-stream": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/get-stream/-/get-stream-6.0.1.tgz",
      "integrity": "sha512-ts6Wi+2j3jQjqi70w5AlN8DFnkSwC+MqmxEzdEALB2qXZYV3X/b1CTfgPLGJNMeAWxdPfU8FO1ms3NUfaHCPYg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/get-symbol-description": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/get-symbol-description/-/get-symbol-description-1.1.0.tgz",
      "integrity": "sha512-w9UMqWwJxHNOvoNzSJ2oPF5wvYcvP7jUvYzhp67yEhTi17ZDBBC1z9pTdGuzjD+EFIqLSYRweZjqfiPzQ06Ebg==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/glob": {
      "version": "7.2.3",
      "resolved": "https://registry.npmjs.org/glob/-/glob-7.2.3.tgz",
      "integrity": "sha512-nFR0zLpU2YCaRxwoCJvL6UvCH2JFyFVIvwTLsIf21AuHlMskA1hhTdk+LlYJtOlYt9v6dvszD2BGRqBL+iQK9Q==",
      "deprecated": "Old versions of glob are not supported, and contain widely publicized security vulnerabilities, which have been fixed in the current version. Please update. Support for old versions may be purchased (at exorbitant rates) by contacting i@izs.me",
      "license": "ISC",
      "dependencies": {
        "fs.realpath": "^1.0.0",
        "inflight": "^1.0.4",
        "inherits": "2",
        "minimatch": "^3.1.1",
        "once": "^1.3.0",
        "path-is-absolute": "^1.0.0"
      },
      "engines": {
        "node": "*"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/glob-parent": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-6.0.2.tgz",
      "integrity": "sha512-XxwI8EOhVQgWp6iDL+3b0r86f4d6AX6zSU55HfB4ydCEuXLXc5FcYeOu+nnGftS4TEju/11rt4KJPTMgbfmv4A==",
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.3"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/glob-to-regexp": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/glob-to-regexp/-/glob-to-regexp-0.4.1.tgz",
      "integrity": "sha512-lkX1HJXwyMcprw/5YUZc2s7DrpAiHB21/V+E1rHUrVNokkvB6bqMzT0VfV6/86ZNabt1k14YOIaT7nDvOX3Iiw==",
      "license": "BSD-2-Clause"
    },
    "node_modules/global-modules": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/global-modules/-/global-modules-2.0.0.tgz",
      "integrity": "sha512-NGbfmJBp9x8IxyJSd1P+otYK8vonoJactOogrVfFRIAEY1ukil8RSKDz2Yo7wh1oihl51l/r6W4epkeKJHqL8A==",
      "license": "MIT",
      "dependencies": {
        "global-prefix": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/global-prefix": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/global-prefix/-/global-prefix-3.0.0.tgz",
      "integrity": "sha512-awConJSVCHVGND6x3tmMaKcQvwXLhjdkmomy2W+Goaui8YPgYgXJZewhg3fWC+DlfqqQuWg8AwqjGTD2nAPVWg==",
      "license": "MIT",
      "dependencies": {
        "ini": "^1.3.5",
        "kind-of": "^6.0.2",
        "which": "^1.3.1"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/global-prefix/node_modules/which": {
      "version": "1.3.1",
      "resolved": "https://registry.npmjs.org/which/-/which-1.3.1.tgz",
      "integrity": "sha512-HxJdYWq1MTIQbJ3nw0cqssHoTNU267KlrDuGZ1WYlxDStUtKUhOaJmh112/TZmHxxUfuJqPXSOm7tDyas0OSIQ==",
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "which": "bin/which"
      }
    },
    "node_modules/globals": {
      "version": "13.24.0",
      "resolved": "https://registry.npmjs.org/globals/-/globals-13.24.0.tgz",
      "integrity": "sha512-AhO5QUcj8llrbG09iWhPU2B204J1xnPeL8kQmVorSsy+Sjj1sk8gIyh6cUocGmH4L0UuhAJy+hJMRA4mgA4mFQ==",
      "license": "MIT",
      "dependencies": {
        "type-fest": "^0.20.2"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/globalthis": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/globalthis/-/globalthis-1.0.4.tgz",
      "integrity": "sha512-DpLKbNU4WylpxJykQujfCcwYWiV/Jhm50Goo0wrVILAv5jOr9d+H+UR3PhSCD2rCCEIg0uc+G+muBTwD54JhDQ==",
      "license": "MIT",
      "dependencies": {
        "define-properties": "^1.2.1",
        "gopd": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/globby": {
      "version": "11.1.0",
      "resolved": "https://registry.npmjs.org/globby/-/globby-11.1.0.tgz",
      "integrity": "sha512-jhIXaOzy1sb8IyocaruWSn1TjmnBVs8Ayhcy83rmxNJ8q2uWKCAj3CnJY+KpGSXCueAPc0i05kVvVKtP1t9S3g==",
      "license": "MIT",
      "dependencies": {
        "array-union": "^2.1.0",
        "dir-glob": "^3.0.1",
        "fast-glob": "^3.2.9",
        "ignore": "^5.2.0",
        "merge2": "^1.4.1",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/gopd": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/gopd/-/gopd-1.2.0.tgz",
      "integrity": "sha512-ZUKRh6/kUFoAiTAtTYPZJ3hw9wNxx+BIBOijnlG9PnrJsCcSjs1wyyD6vJpaYtgnzDrKYRSqf3OO6Rfa93xsRg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/graceful-fs": {
      "version": "4.2.11",
      "resolved": "https://registry.npmjs.org/graceful-fs/-/graceful-fs-4.2.11.tgz",
      "integrity": "sha512-RbJ5/jmFcNNCcDV5o9eTnBLJ/HszWV0P73bc+Ff4nS/rJj+YaS6IGyiOL0VoBYX+l1Wrl3k63h/KrH+nhJ0XvQ==",
      "license": "ISC"
    },
    "node_modules/graphemer": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/graphemer/-/graphemer-1.4.0.tgz",
      "integrity": "sha512-EtKwoO6kxCL9WO5xipiHTZlSzBm7WLT627TqC/uVRd0HKmq8NXyebnNYxDoBi7wt8eTWrUrKXCOVaFq9x1kgag==",
      "license": "MIT"
    },
    "node_modules/gzip-size": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/gzip-size/-/gzip-size-6.0.0.tgz",
      "integrity": "sha512-ax7ZYomf6jqPTQ4+XCpUGyXKHk5WweS+e05MBO4/y3WJ5RkmPXNKvX+bx1behVILVwr6JSQvZAku021CHPXG3Q==",
      "license": "MIT",
      "dependencies": {
        "duplexer": "^0.1.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/handle-thing": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/handle-thing/-/handle-thing-2.0.1.tgz",
      "integrity": "sha512-9Qn4yBxelxoh2Ow62nP+Ka/kMnOXRi8BXnRaUwezLNhqelnN49xKz4F/dPP8OYLxLxq6JDtZb2i9XznUQbNPTg==",
      "license": "MIT"
    },
    "node_modules/harmony-reflect": {
      "version": "1.6.2",
      "resolved": "https://registry.npmjs.org/harmony-reflect/-/harmony-reflect-1.6.2.tgz",
      "integrity": "sha512-HIp/n38R9kQjDEziXyDTuW3vvoxxyxjxFzXLrBr18uB47GnSt+G9D29fqrpM5ZkspMcPICud3XsBJQ4Y2URg8g==",
      "license": "(Apache-2.0 OR MPL-1.1)"
    },
    "node_modules/has-bigints": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-bigints/-/has-bigints-1.1.0.tgz",
      "integrity": "sha512-R3pbpkcIqv2Pm3dUwgjclDRVmWpTJW2DcMzcIhEXEx1oh/CEMObMm3KLmRJOdvhM7o4uQBnwr8pzRK2sJWIqfg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-flag": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/has-flag/-/has-flag-4.0.0.tgz",
      "integrity": "sha512-EykJT/Q1KjTWctppgIAgfSO0tKVuZUjhgMr17kqTumMl6Afv3EISleU7qZUzoXDFTAHTDC4NOoG/ZxU3EvlMPQ==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/has-property-descriptors": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-property-descriptors/-/has-property-descriptors-1.0.2.tgz",
      "integrity": "sha512-55JNKuIW+vq4Ke1BjOTjM2YctQIvCT7GFzHwmfZPGo5wnrgkid0YQtnAleFSqumZm4az3n2BS+erby5ipJdgrg==",
      "license": "MIT",
      "dependencies": {
        "es-define-property": "^1.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-proto": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/has-proto/-/has-proto-1.2.0.tgz",
      "integrity": "sha512-KIL7eQPfHQRC8+XluaIw7BHUwwqL19bQn4hzNgdr+1wXoU0KKj6rufu47lhY7KbJR2C6T6+PfyN0Ea7wkSS+qQ==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-symbols": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-symbols/-/has-symbols-1.1.0.tgz",
      "integrity": "sha512-1cDNdwJ2Jaohmb3sg4OmKaMBwuC48sYni5HUw2DvsC8LjGTLK9h+eb1X6RyuOHe4hT0ULCW68iomhjUoKUqlPQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-tostringtag": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-tostringtag/-/has-tostringtag-1.0.2.tgz",
      "integrity": "sha512-NqADB8VjPFLM2V0VvHUewwwsw0ZWBaIdgo+ieHtK3hasLz4qeCRjYcqfB6AQrBggRKppKF8L52/VqdVsO47Dlw==",
      "license": "MIT",
      "dependencies": {
        "has-symbols": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/hasown": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.2.tgz",
      "integrity": "sha512-0hJU9SCPvmMzIBdZFqNPXWa6dqh7WdH0cII9y+CyS8rG3nL48Bclra9HmKhVVUHyPWNH5Y7xDwAB7bfgSjkUMQ==",
      "license": "MIT",
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/he": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/he/-/he-1.2.0.tgz",
      "integrity": "sha512-F/1DnUGPopORZi0ni+CvrCgHQ5FyEAHRLSApuYWMmrbSwoN2Mn/7k+Gl38gJnR7yyDZk6WLXwiGod1JOWNDKGw==",
      "license": "MIT",
      "bin": {
        "he": "bin/he"
      }
    },
    "node_modules/hoopy": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/hoopy/-/hoopy-0.1.4.tgz",
      "integrity": "sha512-HRcs+2mr52W0K+x8RzcLzuPPmVIKMSv97RGHy0Ea9y/mpcaK+xTrjICA04KAHi4GRzxliNqNJEFYWHghy3rSfQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 6.0.0"
      }
    },
    "node_modules/hpack.js": {
      "version": "2.1.6",
      "resolved": "https://registry.npmjs.org/hpack.js/-/hpack.js-2.1.6.tgz",
      "integrity": "sha512-zJxVehUdMGIKsRaNt7apO2Gqp0BdqW5yaiGHXXmbpvxgBYVZnAql+BJb4RO5ad2MgpbZKn5G6nMnegrH1FcNYQ==",
      "license": "MIT",
      "dependencies": {
        "inherits": "^2.0.1",
        "obuf": "^1.0.0",
        "readable-stream": "^2.0.1",
        "wbuf": "^1.1.0"
      }
    },
    "node_modules/hpack.js/node_modules/isarray": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/isarray/-/isarray-1.0.0.tgz",
      "integrity": "sha512-VLghIWNM6ELQzo7zwmcg0NmTVyWKYjvIeM83yjp0wRDTmUnrM678fQbcKBo6n2CJEF0szoG//ytg+TKla89ALQ==",
      "license": "MIT"
    },
    "node_modules/hpack.js/node_modules/readable-stream": {
      "version": "2.3.8",
      "resolved": "https://registry.npmjs.org/readable-stream/-/readable-stream-2.3.8.tgz",
      "integrity": "sha512-8p0AUk4XODgIewSi0l8Epjs+EVnWiK7NoDIEGU0HhE7+ZyY8D1IMY7odu5lRrFXGg71L15KG8QrPmum45RTtdA==",
      "license": "MIT",
      "dependencies": {
        "core-util-is": "~1.0.0",
        "inherits": "~2.0.3",
        "isarray": "~1.0.0",
        "process-nextick-args": "~2.0.0",
        "safe-buffer": "~5.1.1",
        "string_decoder": "~1.1.1",
        "util-deprecate": "~1.0.1"
      }
    },
    "node_modules/hpack.js/node_modules/safe-buffer": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/safe-buffer/-/safe-buffer-5.1.2.tgz",
      "integrity": "sha512-Gd2UZBJDkXlY7GbJxfsE8/nvKkUEU1G38c1siN6QP6a9PT9MmHB8GnpscSmMJSoF8LOIrt8ud/wPtojys4G6+g==",
      "license": "MIT"
    },
    "node_modules/hpack.js/node_modules/string_decoder": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/string_decoder/-/string_decoder-1.1.1.tgz",
      "integrity": "sha512-n/ShnvDi6FHbbVfviro+WojiFzv+s8MPMHBczVePfUpDJLwoLT0ht1l4YwBCbi8pJAveEEdnkHyPyTP/mzRfwg==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "~5.1.0"
      }
    },
    "node_modules/html-encoding-sniffer": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/html-encoding-sniffer/-/html-encoding-sniffer-2.0.1.tgz",
      "integrity": "sha512-D5JbOMBIR/TVZkubHT+OyT2705QvogUW4IBn6nHd756OwieSF9aDYFj4dv6HHEVGYbHaLETa3WggZYWWMyy3ZQ==",
      "license": "MIT",
      "dependencies": {
        "whatwg-encoding": "^1.0.5"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/html-entities": {
      "version": "2.6.0",
      "resolved": "https://registry.npmjs.org/html-entities/-/html-entities-2.6.0.tgz",
      "integrity": "sha512-kig+rMn/QOVRvr7c86gQ8lWXq+Hkv6CbAH1hLu+RG338StTpE8Z0b44SDVaqVu7HGKf27frdmUYEs9hTUX/cLQ==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/mdevils"
        },
        {
          "type": "patreon",
          "url": "https://patreon.com/mdevils"
        }
      ],
      "license": "MIT"
    },
    "node_modules/html-escaper": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/html-escaper/-/html-escaper-2.0.2.tgz",
      "integrity": "sha512-H2iMtd0I4Mt5eYiapRdIDjp+XzelXQ0tFE4JS7YFwFevXXMmOp9myNrUvCg0D6ws8iqkRPBfKHgbwig1SmlLfg==",
      "license": "MIT"
    },
    "node_modules/html-minifier-terser": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/html-minifier-terser/-/html-minifier-terser-6.1.0.tgz",
      "integrity": "sha512-YXxSlJBZTP7RS3tWnQw74ooKa6L9b9i9QYXY21eUEvhZ3u9XLfv6OnFsQq6RxkhHygsaUMvYsZRV5rU/OVNZxw==",
      "license": "MIT",
      "dependencies": {
        "camel-case": "^4.1.2",
        "clean-css": "^5.2.2",
        "commander": "^8.3.0",
        "he": "^1.2.0",
        "param-case": "^3.0.4",
        "relateurl": "^0.2.7",
        "terser": "^5.10.0"
      },
      "bin": {
        "html-minifier-terser": "cli.js"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/html-webpack-plugin": {
      "version": "5.6.6",
      "resolved": "https://registry.npmjs.org/html-webpack-plugin/-/html-webpack-plugin-5.6.6.tgz",
      "integrity": "sha512-bLjW01UTrvoWTJQL5LsMRo1SypHW80FTm12OJRSnr3v6YHNhfe+1r0MYUZJMACxnCHURVnBWRwAsWs2yPU9Ezw==",
      "license": "MIT",
      "dependencies": {
        "@types/html-minifier-terser": "^6.0.0",
        "html-minifier-terser": "^6.0.2",
        "lodash": "^4.17.21",
        "pretty-error": "^4.0.0",
        "tapable": "^2.0.0"
      },
      "engines": {
        "node": ">=10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/html-webpack-plugin"
      },
      "peerDependencies": {
        "@rspack/core": "0.x || 1.x",
        "webpack": "^5.20.0"
      },
      "peerDependenciesMeta": {
        "@rspack/core": {
          "optional": true
        },
        "webpack": {
          "optional": true
        }
      }
    },
    "node_modules/htmlparser2": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/htmlparser2/-/htmlparser2-6.1.0.tgz",
      "integrity": "sha512-gyyPk6rgonLFEDGoeRgQNaEUvdJ4ktTmmUh/h2t7s+M8oPpIPxgNACWa+6ESR57kXstwqPiCut0V8NRpcwgU7A==",
      "funding": [
        "https://github.com/fb55/htmlparser2?sponsor=1",
        {
          "type": "github",
          "url": "https://github.com/sponsors/fb55"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "domelementtype": "^2.0.1",
        "domhandler": "^4.0.0",
        "domutils": "^2.5.2",
        "entities": "^2.0.0"
      }
    },
    "node_modules/http-deceiver": {
      "version": "1.2.7",
      "resolved": "https://registry.npmjs.org/http-deceiver/-/http-deceiver-1.2.7.tgz",
      "integrity": "sha512-LmpOGxTfbpgtGVxJrj5k7asXHCgNZp5nLfp+hWc8QQRqtb7fUy6kRY3BO1h9ddF6yIPYUARgxGOwB42DnxIaNw==",
      "license": "MIT"
    },
    "node_modules/http-errors": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/http-errors/-/http-errors-2.0.1.tgz",
      "integrity": "sha512-4FbRdAX+bSdmo4AUFuS0WNiPz8NgFt+r8ThgNWmlrjQjt1Q7ZR9+zTlce2859x4KSXrwIsaeTqDoKQmtP8pLmQ==",
      "license": "MIT",
      "dependencies": {
        "depd": "~2.0.0",
        "inherits": "~2.0.4",
        "setprototypeof": "~1.2.0",
        "statuses": "~2.0.2",
        "toidentifier": "~1.0.1"
      },
      "engines": {
        "node": ">= 0.8"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/http-parser-js": {
      "version": "0.5.10",
      "resolved": "https://registry.npmjs.org/http-parser-js/-/http-parser-js-0.5.10.tgz",
      "integrity": "sha512-Pysuw9XpUq5dVc/2SMHpuTY01RFl8fttgcyunjL7eEMhGM3cI4eOmiCycJDVCo/7O7ClfQD3SaI6ftDzqOXYMA==",
      "license": "MIT"
    },
    "node_modules/http-proxy": {
      "version": "1.18.1",
      "resolved": "https://registry.npmjs.org/http-proxy/-/http-proxy-1.18.1.tgz",
      "integrity": "sha512-7mz/721AbnJwIVbnaSv1Cz3Am0ZLT/UBwkC92VlxhXv/k/BBQfM2fXElQNC27BVGr0uwUpplYPQM9LnaBMR5NQ==",
      "license": "MIT",
      "dependencies": {
        "eventemitter3": "^4.0.0",
        "follow-redirects": "^1.0.0",
        "requires-port": "^1.0.0"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/http-proxy-agent": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/http-proxy-agent/-/http-proxy-agent-4.0.1.tgz",
      "integrity": "sha512-k0zdNgqWTGA6aeIRVpvfVob4fL52dTfaehylg0Y4UvSySvOq/Y+BOyPrgpUrA7HylqvU8vIZGsRuXmspskV0Tg==",
      "license": "MIT",
      "dependencies": {
        "@tootallnate/once": "1",
        "agent-base": "6",
        "debug": "4"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/http-proxy-middleware": {
      "version": "2.0.9",
      "resolved": "https://registry.npmjs.org/http-proxy-middleware/-/http-proxy-middleware-2.0.9.tgz",
      "integrity": "sha512-c1IyJYLYppU574+YI7R4QyX2ystMtVXZwIdzazUIPIJsHuWNd+mho2j+bKoHftndicGj9yh+xjd+l0yj7VeT1Q==",
      "license": "MIT",
      "dependencies": {
        "@types/http-proxy": "^1.17.8",
        "http-proxy": "^1.18.1",
        "is-glob": "^4.0.1",
        "is-plain-obj": "^3.0.0",
        "micromatch": "^4.0.2"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "@types/express": "^4.17.13"
      },
      "peerDependenciesMeta": {
        "@types/express": {
          "optional": true
        }
      }
    },
    "node_modules/https-proxy-agent": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/https-proxy-agent/-/https-proxy-agent-5.0.1.tgz",
      "integrity": "sha512-dFcAjpTQFgoLMzC2VwU+C/CbS7uRL0lWmxDITmqm7C+7F0Odmj6s9l6alZc6AELXhrnggM2CeWSXHGOdX2YtwA==",
      "license": "MIT",
      "dependencies": {
        "agent-base": "6",
        "debug": "4"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/human-signals": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/human-signals/-/human-signals-2.1.0.tgz",
      "integrity": "sha512-B4FFZ6q/T2jhhksgkbEW3HBvWIfDW85snkQgawt07S7J5QXTk6BkNV+0yAeZrM5QpMAdYlocGoljn0sJ/WQkFw==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=10.17.0"
      }
    },
    "node_modules/iconv-lite": {
      "version": "0.6.3",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.6.3.tgz",
      "integrity": "sha512-4fCk79wshMdzMp2rH06qWrJE4iolqLhCUH+OiuIgU++RB0+94NlDL81atO7GX55uUKueo0txHNtvEyI6D7WdMw==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3.0.0"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/icss-utils": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/icss-utils/-/icss-utils-5.1.0.tgz",
      "integrity": "sha512-soFhflCVWLfRNOPU3iv5Z9VUdT44xFRbzjLsEzSr5AQmgqPMTHdU3PMT1Cf1ssx8fLNJDA1juftYl+PUcv3MqA==",
      "license": "ISC",
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/idb": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/idb/-/idb-7.1.1.tgz",
      "integrity": "sha512-gchesWBzyvGHRO9W8tzUWFDycow5gwjvFKfyV9FF32Y7F50yZMp7mP+T2mJIWFx49zicqyC4uefHM17o6xKIVQ==",
      "license": "ISC"
    },
    "node_modules/identity-obj-proxy": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/identity-obj-proxy/-/identity-obj-proxy-3.0.0.tgz",
      "integrity": "sha512-00n6YnVHKrinT9t0d9+5yZC6UBNJANpYEQvL2LlX6Ab9lnmxzIRcEmTPuyGScvl1+jKuCICX1Z0Ab1pPKKdikA==",
      "license": "MIT",
      "dependencies": {
        "harmony-reflect": "^1.4.6"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/ignore": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/ignore/-/ignore-5.3.2.tgz",
      "integrity": "sha512-hsBTNUqQTDwkWtcdYI2i06Y/nUBEsNEDJKjWdigLvegy8kDuJAS8uRlpkkcQpyEXL0Z/pjDy5HBmMjRCJ2gq+g==",
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/immer": {
      "version": "9.0.21",
      "resolved": "https://registry.npmjs.org/immer/-/immer-9.0.21.tgz",
      "integrity": "sha512-bc4NBHqOqSfRW7POMkHd51LvClaeMXpm8dx0e8oE2GORbq5aRK7Bxl4FyzVLdGtLmvLKL7BTDBG5ACQm4HWjTA==",
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/immer"
      }
    },
    "node_modules/import-fresh": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/import-fresh/-/import-fresh-3.3.1.tgz",
      "integrity": "sha512-TR3KfrTZTYLPB6jUjfx6MF9WcWrHL9su5TObK4ZkYgBdWKPOFoSoQIdEuTuR82pmtxH2spWG9h6etwfr1pLBqQ==",
      "license": "MIT",
      "dependencies": {
        "parent-module": "^1.0.0",
        "resolve-from": "^4.0.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/import-fresh/node_modules/resolve-from": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/resolve-from/-/resolve-from-4.0.0.tgz",
      "integrity": "sha512-pb/MYmXstAkysRFx8piNI1tGFNQIFA3vkE3Gq4EuA1dF6gHp/+vgZqsCGJapvy8N3Q+4o7FwvquPJcnZ7RYy4g==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/import-local": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/import-local/-/import-local-3.2.0.tgz",
      "integrity": "sha512-2SPlun1JUPWoM6t3F0dw0FkCF/jWY8kttcY4f599GLTSjh2OCuuhdTkJQsEcZzBqbXZGKMK2OqW1oZsjtf/gQA==",
      "license": "MIT",
      "dependencies": {
        "pkg-dir": "^4.2.0",
        "resolve-cwd": "^3.0.0"
      },
      "bin": {
        "import-local-fixture": "fixtures/cli.js"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/imurmurhash": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/imurmurhash/-/imurmurhash-0.1.4.tgz",
      "integrity": "sha512-JmXMZ6wuvDmLiHEml9ykzqO6lwFbof0GG4IkcGaENdCRDDmMVnny7s5HsIgHCbaq0w2MyPhDqkhTUgS2LU2PHA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8.19"
      }
    },
    "node_modules/inflight": {
      "version": "1.0.6",
      "resolved": "https://registry.npmjs.org/inflight/-/inflight-1.0.6.tgz",
      "integrity": "sha512-k92I/b08q4wvFscXCLvqfsHCrjrF7yiXsQuIVvVE7N82W3+aqpzuUdBbfhWcy/FZR3/4IgflMgKLOsvPDrGCJA==",
      "deprecated": "This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.",
      "license": "ISC",
      "dependencies": {
        "once": "^1.3.0",
        "wrappy": "1"
      }
    },
    "node_modules/inherits": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/inherits/-/inherits-2.0.4.tgz",
      "integrity": "sha512-k/vGaX4/Yla3WzyMCvTQOXYeIHvqOKtnqBduzTHpzpQZzAskKMhZ2K+EnBiSM9zGSoIFeMpXKxa4dYeZIQqewQ==",
      "license": "ISC"
    },
    "node_modules/ini": {
      "version": "1.3.8",
      "resolved": "https://registry.npmjs.org/ini/-/ini-1.3.8.tgz",
      "integrity": "sha512-JV/yugV2uzW5iMRSiZAyDtQd+nxtUnjeLt0acNdw98kKLrvuRVyB80tsREOE7yvGVgalhZ6RNXCmEHkUKBKxew==",
      "license": "ISC"
    },
    "node_modules/internal-slot": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/internal-slot/-/internal-slot-1.1.0.tgz",
      "integrity": "sha512-4gd7VpWNQNB4UKKCFFVcp1AVv+FMOgs9NKzjHKusc8jTMhd5eL1NqQqOpE0KzMds804/yHlglp3uxgluOqAPLw==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "hasown": "^2.0.2",
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/ipaddr.js": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/ipaddr.js/-/ipaddr.js-2.3.0.tgz",
      "integrity": "sha512-Zv/pA+ciVFbCSBBjGfaKUya/CcGmUHzTydLMaTwrUUEM2DIEO3iZvueGxmacvmN50fGpGVKeTXpb2LcYQxeVdg==",
      "license": "MIT",
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/is-array-buffer": {
      "version": "3.0.5",
      "resolved": "https://registry.npmjs.org/is-array-buffer/-/is-array-buffer-3.0.5.tgz",
      "integrity": "sha512-DDfANUiiG2wC1qawP66qlTugJeL5HyzMpfr8lLK+jMQirGzNod0B12cFB/9q838Ru27sBwfw78/rdoU7RERz6A==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-arrayish": {
      "version": "0.2.1",
      "resolved": "https://registry.npmjs.org/is-arrayish/-/is-arrayish-0.2.1.tgz",
      "integrity": "sha512-zz06S8t0ozoDXMG+ube26zeCTNXcKIPJZJi8hBrF4idCLms4CG9QtK7qBl1boi5ODzFpjswb5JPmHCbMpjaYzg==",
      "license": "MIT"
    },
    "node_modules/is-async-function": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-async-function/-/is-async-function-2.1.1.tgz",
      "integrity": "sha512-9dgM/cZBnNvjzaMYHVoxxfPj2QXt22Ev7SuuPrs+xav0ukGB0S6d4ydZdEiM48kLx5kDV+QBPrpVnFyefL8kkQ==",
      "license": "MIT",
      "dependencies": {
        "async-function": "^1.0.0",
        "call-bound": "^1.0.3",
        "get-proto": "^1.0.1",
        "has-tostringtag": "^1.0.2",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-bigint": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-bigint/-/is-bigint-1.1.0.tgz",
      "integrity": "sha512-n4ZT37wG78iz03xPRKJrHTdZbe3IicyucEtdRsV5yglwc3GyUfbAfpSeD0FJ41NbUNSt5wbhqfp1fS+BgnvDFQ==",
      "license": "MIT",
      "dependencies": {
        "has-bigints": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-binary-path": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-binary-path/-/is-binary-path-2.1.0.tgz",
      "integrity": "sha512-ZMERYes6pDydyuGidse7OsHxtbI7WVeUEozgR/g7rd0xUimYNlvZRE/K2MgZTjWy725IfelLeVcEM97mmtRGXw==",
      "license": "MIT",
      "dependencies": {
        "binary-extensions": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-boolean-object": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/is-boolean-object/-/is-boolean-object-1.2.2.tgz",
      "integrity": "sha512-wa56o2/ElJMYqjCjGkXri7it5FbebW5usLw/nPmCMs5DeZ7eziSYZhSmPRn0txqeW4LnAmQQU7FgqLpsEFKM4A==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-callable": {
      "version": "1.2.7",
      "resolved": "https://registry.npmjs.org/is-callable/-/is-callable-1.2.7.tgz",
      "integrity": "sha512-1BC0BVFhS/p0qtw6enp8e+8OD0UrK0oFLztSjNzhcKA3WDuJxxAPXzPuPtKkjEY9UUoEWlX/8fgKeu2S8i9JTA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-core-module": {
      "version": "2.16.1",
      "resolved": "https://registry.npmjs.org/is-core-module/-/is-core-module-2.16.1.tgz",
      "integrity": "sha512-UfoeMA6fIJ8wTYFEUjelnaGI67v6+N7qXJEvQuIGa99l4xsCruSYOVSQ0uPANn4dAzm8lkYPaKLrrijLq7x23w==",
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-data-view": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/is-data-view/-/is-data-view-1.0.2.tgz",
      "integrity": "sha512-RKtWF8pGmS87i2D6gqQu/l7EYRlVdfzemCJN/P3UOs//x1QE7mfhvzHIApBTRf7axvT6DMGwSwBXYCT0nfB9xw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "get-intrinsic": "^1.2.6",
        "is-typed-array": "^1.1.13"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-date-object": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-date-object/-/is-date-object-1.1.0.tgz",
      "integrity": "sha512-PwwhEakHVKTdRNVOw+/Gyh0+MzlCl4R6qKvkhuvLtPMggI1WAHt9sOwZxQLSGpUaDnrdyDsomoRgNnCfKNSXXg==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-docker": {
      "version": "2.2.1",
      "resolved": "https://registry.npmjs.org/is-docker/-/is-docker-2.2.1.tgz",
      "integrity": "sha512-F+i2BKsFrH66iaUFc0woD8sLy8getkwTwtOBjvs56Cx4CgJDeKQeqfz8wAYiSb8JOprWhHH5p77PbmYCvvUuXQ==",
      "license": "MIT",
      "bin": {
        "is-docker": "cli.js"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-extglob": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-extglob/-/is-extglob-2.1.1.tgz",
      "integrity": "sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-finalizationregistry": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-finalizationregistry/-/is-finalizationregistry-1.1.1.tgz",
      "integrity": "sha512-1pC6N8qWJbWoPtEjgcL2xyhQOP491EQjeUo3qTKcmV8YSDDJrOepfG8pcC7h/QgnQHYSv0mJ3Z/ZWxmatVrysg==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-fullwidth-code-point": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/is-fullwidth-code-point/-/is-fullwidth-code-point-3.0.0.tgz",
      "integrity": "sha512-zymm5+u+sCsSWyD9qNaejV3DFvhCKclKdizYaJUuHA83RLjb7nSuGnddCHGv0hk+KY7BMAlsWeK4Ueg6EV6XQg==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-generator-fn": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-generator-fn/-/is-generator-fn-2.1.0.tgz",
      "integrity": "sha512-cTIB4yPYL/Grw0EaSzASzg6bBy9gqCofvWN8okThAYIxKJZC+udlRAmGbM0XLeniEJSs8uEgHPGuHSe1XsOLSQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/is-generator-function": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/is-generator-function/-/is-generator-function-1.1.2.tgz",
      "integrity": "sha512-upqt1SkGkODW9tsGNG5mtXTXtECizwtS2kA161M+gJPc1xdb/Ax629af6YrTwcOeQHbewrPNlE5Dx7kzvXTizA==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.4",
        "generator-function": "^2.0.0",
        "get-proto": "^1.0.1",
        "has-tostringtag": "^1.0.2",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-glob": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/is-glob/-/is-glob-4.0.3.tgz",
      "integrity": "sha512-xelSayHH36ZgE7ZWhli7pW34hNbNl8Ojv5KVmkJD4hBdD3th8Tfk9vYasLM+mXWOZhFkgZfxhLSnrwRr4elSSg==",
      "license": "MIT",
      "dependencies": {
        "is-extglob": "^2.1.1"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-map": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-map/-/is-map-2.0.3.tgz",
      "integrity": "sha512-1Qed0/Hr2m+YqxnM09CjA2d/i6YZNfF6R2oRAOj36eUdS6qIV/huPJNSEpKbupewFs+ZsJlxsjjPbc0/afW6Lw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-module": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/is-module/-/is-module-1.0.0.tgz",
      "integrity": "sha512-51ypPSPCoTEIN9dy5Oy+h4pShgJmPCygKfyRCISBI+JoWT/2oJvK8QPxmwv7b/p239jXrm9M1mlQbyKJ5A152g==",
      "license": "MIT"
    },
    "node_modules/is-negative-zero": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-negative-zero/-/is-negative-zero-2.0.3.tgz",
      "integrity": "sha512-5KoIu2Ngpyek75jXodFvnafB6DJgr3u8uuK0LEZJjrU19DrMD3EVERaR8sjz8CCGgpZvxPl9SuE1GMVPFHx1mw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-number": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/is-number/-/is-number-7.0.0.tgz",
      "integrity": "sha512-41Cifkg6e8TylSpdtTpeLVMqvSBEVzTttHvERD741+pnZ8ANv0004MRL43QKPDlK9cGvNp6NZWZUBlbGXYxxng==",
      "license": "MIT",
      "engines": {
        "node": ">=0.12.0"
      }
    },
    "node_modules/is-number-object": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-number-object/-/is-number-object-1.1.1.tgz",
      "integrity": "sha512-lZhclumE1G6VYD8VHe35wFaIif+CTy5SJIi5+3y4psDgWu4wPDoBhF8NxUOinEc7pHgiTsT6MaBb92rKhhD+Xw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-obj": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/is-obj/-/is-obj-1.0.1.tgz",
      "integrity": "sha512-l4RyHgRqGN4Y3+9JHVrNqO+tN0rV5My76uW5/nuO4K1b6vw5G8d/cmFjP9tRfEsdhZNt0IFdZuK/c2Vr4Nb+Qg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-path-inside": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/is-path-inside/-/is-path-inside-3.0.3.tgz",
      "integrity": "sha512-Fd4gABb+ycGAmKou8eMftCupSir5lRxqf4aD/vd0cD2qc4HL07OjCeuHMr8Ro4CoMaeCKDB0/ECBOVWjTwUvPQ==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-plain-obj": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/is-plain-obj/-/is-plain-obj-3.0.0.tgz",
      "integrity": "sha512-gwsOE28k+23GP1B6vFl1oVh/WOzmawBrKwo5Ev6wMKzPkaXaCDIQKzLnvsA42DRlbVTWorkgTKIviAKCWkfUwA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-potential-custom-element-name": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/is-potential-custom-element-name/-/is-potential-custom-element-name-1.0.1.tgz",
      "integrity": "sha512-bCYeRA2rVibKZd+s2625gGnGF/t7DSqDs4dP7CrLA1m7jKWz6pps0LpYLJN8Q64HtmPKJ1hrN3nzPNKFEKOUiQ==",
      "license": "MIT"
    },
    "node_modules/is-regex": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/is-regex/-/is-regex-1.2.1.tgz",
      "integrity": "sha512-MjYsKHO5O7mCsmRGxWcLWheFqN9DJ/2TmngvjKXihe6efViPqc274+Fx/4fYj/r03+ESvBdTXK0V6tA3rgez1g==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "gopd": "^1.2.0",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-regexp": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/is-regexp/-/is-regexp-1.0.0.tgz",
      "integrity": "sha512-7zjFAPO4/gwyQAAgRRmqeEeyIICSdmCqa3tsVHMdBzaXXRiqopZL4Cyghg/XulGWrtABTpbnYYzzIRffLkP4oA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-root": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-root/-/is-root-2.1.0.tgz",
      "integrity": "sha512-AGOriNp96vNBd3HtU+RzFEc75FfR5ymiYv8E553I71SCeXBiMsVDUtdio1OEFvrPyLIQ9tVR5RxXIFe5PUFjMg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/is-set": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-set/-/is-set-2.0.3.tgz",
      "integrity": "sha512-iPAjerrse27/ygGLxw+EBR9agv9Y6uLeYVJMu+QNCoouJ1/1ri0mGrcWpfCqFZuzzx3WjtwxG098X+n4OuRkPg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-shared-array-buffer": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/is-shared-array-buffer/-/is-shared-array-buffer-1.0.4.tgz",
      "integrity": "sha512-ISWac8drv4ZGfwKl5slpHG9OwPNty4jOWPRIhBpxOoD+hqITiwuipOQ2bNthAzwA3B4fIjO4Nln74N0S9byq8A==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-stream": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/is-stream/-/is-stream-2.0.1.tgz",
      "integrity": "sha512-hFoiJiTl63nn+kstHGBtewWSKnQLpyb155KHheA1l39uvtO9nWIop1p3udqPcUd/xbF1VLMO4n7OI6p7RbngDg==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-string": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-string/-/is-string-1.1.1.tgz",
      "integrity": "sha512-BtEeSsoaQjlSPBemMQIrY1MY0uM6vnS1g5fmufYOtnxLGUZM2178PKbhsk7Ffv58IX+ZtcvoGwccYsh0PglkAA==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-symbol": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-symbol/-/is-symbol-1.1.1.tgz",
      "integrity": "sha512-9gGx6GTtCQM73BgmHQXfDmLtfjjTUDSyoxTCbp5WtoixAhfgsDirWIcVQ/IHpvI5Vgd5i/J5F7B9cN/WlVbC/w==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-symbols": "^1.1.0",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-typed-array": {
      "version": "1.1.15",
      "resolved": "https://registry.npmjs.org/is-typed-array/-/is-typed-array-1.1.15.tgz",
      "integrity": "sha512-p3EcsicXjit7SaskXHs1hA91QxgTw46Fv6EFKKGS5DRFLD8yKnohjF3hxoju94b/OcMZoQukzpPpBE9uLVKzgQ==",
      "license": "MIT",
      "dependencies": {
        "which-typed-array": "^1.1.16"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-typedarray": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/is-typedarray/-/is-typedarray-1.0.0.tgz",
      "integrity": "sha512-cyA56iCMHAh5CdzjJIa4aohJyeO1YbwLi3Jc35MmRU6poroFjIGZzUzupGiRPOjgHg9TLu43xbpwXk523fMxKA==",
      "license": "MIT"
    },
    "node_modules/is-weakmap": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/is-weakmap/-/is-weakmap-2.0.2.tgz",
      "integrity": "sha512-K5pXYOm9wqY1RgjpL3YTkF39tni1XajUIkawTLUo9EZEVUFga5gSQJF8nNS7ZwJQ02y+1YCNYcMh+HIf1ZqE+w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakref": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-weakref/-/is-weakref-1.1.1.tgz",
      "integrity": "sha512-6i9mGWSlqzNMEqpCp93KwRS1uUOodk2OJ6b+sq7ZPDSy2WuI5NFIxp/254TytR8ftefexkWn5xNiHUNpPOfSew==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakset": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/is-weakset/-/is-weakset-2.0.4.tgz",
      "integrity": "sha512-mfcwb6IzQyOKTs84CQMrOwW4gQcaTOAWJ0zzJCl2WSPDrWk/OzDaImWFH3djXhb24g4eudZfLRozAvPGw4d9hQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-wsl": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/is-wsl/-/is-wsl-2.2.0.tgz",
      "integrity": "sha512-fKzAra0rGJUUBwGBgNkHZuToZcn+TtXHpeCgmkMJMMYx1sQDYaCSyjJBSCa2nH1DGm7s3n1oBnohoVTBaN7Lww==",
      "license": "MIT",
      "dependencies": {
        "is-docker": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/isarray": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/isarray/-/isarray-2.0.5.tgz",
      "integrity": "sha512-xHjhDr3cNBK0BzdUJSPXZntQUx/mwMS5Rw4A7lPJ90XGAO6ISP/ePDNuo0vhqOZU+UD5JoodwCAAoZQd3FeAKw==",
      "license": "MIT"
    },
    "node_modules/isexe": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/isexe/-/isexe-2.0.0.tgz",
      "integrity": "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw==",
      "license": "ISC"
    },
    "node_modules/istanbul-lib-coverage": {
      "version": "3.2.2",
      "resolved": "https://registry.npmjs.org/istanbul-lib-coverage/-/istanbul-lib-coverage-3.2.2.tgz",
      "integrity": "sha512-O8dpsF+r0WV/8MNRKfnmrtCWhuKjxrq2w+jpzBL5UZKTi2LeVWnWOmWRxFlesJONmc+wLAGvKQZEOanko0LFTg==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/istanbul-lib-instrument": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/istanbul-lib-instrument/-/istanbul-lib-instrument-5.2.1.tgz",
      "integrity": "sha512-pzqtp31nLv/XFOzXGuvhCb8qhjmTVo5vjVk19XE4CRlSWz0KoeJ3bw9XsA7nOp9YBf4qHjwBxkDzKcME/J29Yg==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "@babel/core": "^7.12.3",
        "@babel/parser": "^7.14.7",
        "@istanbuljs/schema": "^0.1.2",
        "istanbul-lib-coverage": "^3.2.0",
        "semver": "^6.3.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/istanbul-lib-instrument/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/istanbul-lib-report": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/istanbul-lib-report/-/istanbul-lib-report-3.0.1.tgz",
      "integrity": "sha512-GCfE1mtsHGOELCU8e/Z7YWzpmybrx/+dSTfLrvY8qRmaY6zXTKWn6WQIjaAFw069icm6GVMNkgu0NzI4iPZUNw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "istanbul-lib-coverage": "^3.0.0",
        "make-dir": "^4.0.0",
        "supports-color": "^7.1.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/istanbul-lib-report/node_modules/make-dir": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/make-dir/-/make-dir-4.0.0.tgz",
      "integrity": "sha512-hXdUTZYIVOt1Ex//jAQi+wTZZpUpwBj/0QsOzqegb3rGMMeJiSEu5xLHnYfBrRV4RH2+OCSOO95Is/7x1WJ4bw==",
      "license": "MIT",
      "dependencies": {
        "semver": "^7.5.3"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/istanbul-lib-source-maps": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/istanbul-lib-source-maps/-/istanbul-lib-source-maps-4.0.1.tgz",
      "integrity": "sha512-n3s8EwkdFIJCG3BPKBYvskgXGoy88ARzvegkitk60NxRdwltLOTaH7CUiMRXvwYorl0Q712iEjcWB+fK/MrWVw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "debug": "^4.1.1",
        "istanbul-lib-coverage": "^3.0.0",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/istanbul-lib-source-maps/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/istanbul-reports": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/istanbul-reports/-/istanbul-reports-3.2.0.tgz",
      "integrity": "sha512-HGYWWS/ehqTV3xN10i23tkPkpH46MLCIMFNCaaKNavAXTF1RkqxawEPtnjnGZ6XKSInBKkiOA5BKS+aZiY3AvA==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "html-escaper": "^2.0.0",
        "istanbul-lib-report": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/iterator.prototype": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/iterator.prototype/-/iterator.prototype-1.1.5.tgz",
      "integrity": "sha512-H0dkQoCa3b2VEeKQBOxFph+JAbcrQdE7KC0UkqwpLmv2EC4P41QXP+rqo9wYodACiG5/WM5s9oDApTU8utwj9g==",
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.6",
        "get-proto": "^1.0.0",
        "has-symbols": "^1.1.0",
        "set-function-name": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/jake": {
      "version": "10.9.4",
      "resolved": "https://registry.npmjs.org/jake/-/jake-10.9.4.tgz",
      "integrity": "sha512-wpHYzhxiVQL+IV05BLE2Xn34zW1S223hvjtqk0+gsPrwd/8JNLXJgZZM/iPFsYc1xyphF+6M6EvdE5E9MBGkDA==",
      "license": "Apache-2.0",
      "dependencies": {
        "async": "^3.2.6",
        "filelist": "^1.0.4",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "jake": "bin/cli.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/jest": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest/-/jest-27.5.1.tgz",
      "integrity": "sha512-Yn0mADZB89zTtjkPJEXwrac3LHudkQMR+Paqa8uxJHCBr9agxztUifWCyiYrjhMPBoUVBjyny0I7XH6ozDr7QQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/core": "^27.5.1",
        "import-local": "^3.0.2",
        "jest-cli": "^27.5.1"
      },
      "bin": {
        "jest": "bin/jest.js"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "node-notifier": "^8.0.1 || ^9.0.0 || ^10.0.0"
      },
      "peerDependenciesMeta": {
        "node-notifier": {
          "optional": true
        }
      }
    },
    "node_modules/jest-changed-files": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-changed-files/-/jest-changed-files-27.5.1.tgz",
      "integrity": "sha512-buBLMiByfWGCoMsLLzGUUSpAmIAGnbR2KJoMN10ziLhOLvP4e0SlypHnAel8iqQXTrcbmfEY9sSqae5sgUsTvw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "execa": "^5.0.0",
        "throat": "^6.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-circus": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-circus/-/jest-circus-27.5.1.tgz",
      "integrity": "sha512-D95R7x5UtlMA5iBYsOHFFbMD/GVA4R/Kdq15f7xYWUfWHBto9NYRsOvnSauTgdF+ogCpJ4tyKOXhUifxS65gdw==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "co": "^4.6.0",
        "dedent": "^0.7.0",
        "expect": "^27.5.1",
        "is-generator-fn": "^2.0.0",
        "jest-each": "^27.5.1",
        "jest-matcher-utils": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-runtime": "^27.5.1",
        "jest-snapshot": "^27.5.1",
        "jest-util": "^27.5.1",
        "pretty-format": "^27.5.1",
        "slash": "^3.0.0",
        "stack-utils": "^2.0.3",
        "throat": "^6.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-cli": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-cli/-/jest-cli-27.5.1.tgz",
      "integrity": "sha512-Hc6HOOwYq4/74/c62dEE3r5elx8wjYqxY0r0G/nFrLDPMFRu6RA/u8qINOIkvhxG7mMQ5EJsOGfRpI8L6eFUVw==",
      "license": "MIT",
      "dependencies": {
        "@jest/core": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/types": "^27.5.1",
        "chalk": "^4.0.0",
        "exit": "^0.1.2",
        "graceful-fs": "^4.2.9",
        "import-local": "^3.0.2",
        "jest-config": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-validate": "^27.5.1",
        "prompts": "^2.0.1",
        "yargs": "^16.2.0"
      },
      "bin": {
        "jest": "bin/jest.js"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "node-notifier": "^8.0.1 || ^9.0.0 || ^10.0.0"
      },
      "peerDependenciesMeta": {
        "node-notifier": {
          "optional": true
        }
      }
    },
    "node_modules/jest-config": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-config/-/jest-config-27.5.1.tgz",
      "integrity": "sha512-5sAsjm6tGdsVbW9ahcChPAFCk4IlkQUknH5AvKjuLTSlcO/wCZKyFdn7Rg0EkC+OGgWODEy2hDpWB1PgzH0JNA==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.8.0",
        "@jest/test-sequencer": "^27.5.1",
        "@jest/types": "^27.5.1",
        "babel-jest": "^27.5.1",
        "chalk": "^4.0.0",
        "ci-info": "^3.2.0",
        "deepmerge": "^4.2.2",
        "glob": "^7.1.1",
        "graceful-fs": "^4.2.9",
        "jest-circus": "^27.5.1",
        "jest-environment-jsdom": "^27.5.1",
        "jest-environment-node": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "jest-jasmine2": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-runner": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-validate": "^27.5.1",
        "micromatch": "^4.0.4",
        "parse-json": "^5.2.0",
        "pretty-format": "^27.5.1",
        "slash": "^3.0.0",
        "strip-json-comments": "^3.1.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "ts-node": ">=9.0.0"
      },
      "peerDependenciesMeta": {
        "ts-node": {
          "optional": true
        }
      }
    },
    "node_modules/jest-diff": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-diff/-/jest-diff-27.5.1.tgz",
      "integrity": "sha512-m0NvkX55LDt9T4mctTEgnZk3fmEg3NRYutvMPWM/0iPnkFj2wIeF45O1718cMSOFO1vINkqmxqD8vE37uTEbqw==",
      "license": "MIT",
      "dependencies": {
        "chalk": "^4.0.0",
        "diff-sequences": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-docblock": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-docblock/-/jest-docblock-27.5.1.tgz",
      "integrity": "sha512-rl7hlABeTsRYxKiUfpHrQrG4e2obOiTQWfMEH3PxPjOtdsfLQO4ReWSZaQ7DETm4xu07rl4q/h4zcKXyU0/OzQ==",
      "license": "MIT",
      "dependencies": {
        "detect-newline": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-each": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-each/-/jest-each-27.5.1.tgz",
      "integrity": "sha512-1Ff6p+FbhT/bXQnEouYy00bkNSY7OUpfIcmdl8vZ31A1UUaurOLPA8a8BbJOF2RDUElwJhmeaV7LnagI+5UwNQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "chalk": "^4.0.0",
        "jest-get-type": "^27.5.1",
        "jest-util": "^27.5.1",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-environment-jsdom": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-environment-jsdom/-/jest-environment-jsdom-27.5.1.tgz",
      "integrity": "sha512-TFBvkTC1Hnnnrka/fUb56atfDtJ9VMZ94JkjTbggl1PEpwrYtUBKMezB3inLmWqQsXYLcMwNoDQwoBTAvFfsfw==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/fake-timers": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "jest-mock": "^27.5.1",
        "jest-util": "^27.5.1",
        "jsdom": "^16.6.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-environment-node": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-environment-node/-/jest-environment-node-27.5.1.tgz",
      "integrity": "sha512-Jt4ZUnxdOsTGwSRAfKEnE6BcwsSPNOijjwifq5sDFSA2kesnXTvNqKHYgM0hDq3549Uf/KzdXNYn4wMZJPlFLw==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/fake-timers": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "jest-mock": "^27.5.1",
        "jest-util": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-get-type": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-get-type/-/jest-get-type-27.5.1.tgz",
      "integrity": "sha512-2KY95ksYSaK7DMBWQn6dQz3kqAf3BB64y2udeG+hv4KfSOb9qwcYQstTJc1KCbsix+wLZWZYN8t7nwX3GOBLRw==",
      "license": "MIT",
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-haste-map": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-haste-map/-/jest-haste-map-27.5.1.tgz",
      "integrity": "sha512-7GgkZ4Fw4NFbMSDSpZwXeBiIbx+t/46nJ2QitkOjvwPYyZmqttu2TDSimMHP1EkPOi4xUZAN1doE5Vd25H4Jng==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@types/graceful-fs": "^4.1.2",
        "@types/node": "*",
        "anymatch": "^3.0.3",
        "fb-watchman": "^2.0.0",
        "graceful-fs": "^4.2.9",
        "jest-regex-util": "^27.5.1",
        "jest-serializer": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-worker": "^27.5.1",
        "micromatch": "^4.0.4",
        "walker": "^1.0.7"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "optionalDependencies": {
        "fsevents": "^2.3.2"
      }
    },
    "node_modules/jest-jasmine2": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-jasmine2/-/jest-jasmine2-27.5.1.tgz",
      "integrity": "sha512-jtq7VVyG8SqAorDpApwiJJImd0V2wv1xzdheGHRGyuT7gZm6gG47QEskOlzsN1PG/6WNaCo5pmwMHDf3AkG2pQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/source-map": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "co": "^4.6.0",
        "expect": "^27.5.1",
        "is-generator-fn": "^2.0.0",
        "jest-each": "^27.5.1",
        "jest-matcher-utils": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-runtime": "^27.5.1",
        "jest-snapshot": "^27.5.1",
        "jest-util": "^27.5.1",
        "pretty-format": "^27.5.1",
        "throat": "^6.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-leak-detector": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-leak-detector/-/jest-leak-detector-27.5.1.tgz",
      "integrity": "sha512-POXfWAMvfU6WMUXftV4HolnJfnPOGEu10fscNCA76KBpRRhcMN2c8d3iT2pxQS3HLbA+5X4sOUPzYO2NUyIlHQ==",
      "license": "MIT",
      "dependencies": {
        "jest-get-type": "^27.5.1",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-matcher-utils": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-matcher-utils/-/jest-matcher-utils-27.5.1.tgz",
      "integrity": "sha512-z2uTx/T6LBaCoNWNFWwChLBKYxTMcGBRjAt+2SbP929/Fflb9aa5LGma654Rz8z9HLxsrUaYzxE9T/EFIL/PAw==",
      "license": "MIT",
      "dependencies": {
        "chalk": "^4.0.0",
        "jest-diff": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-message-util": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-message-util/-/jest-message-util-27.5.1.tgz",
      "integrity": "sha512-rMyFe1+jnyAAf+NHwTclDz0eAaLkVDdKVHHBFWsBWHnnh5YeJMNWWsv7AbFYXfK3oTqvL7VTWkhNLu1jX24D+g==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.12.13",
        "@jest/types": "^27.5.1",
        "@types/stack-utils": "^2.0.0",
        "chalk": "^4.0.0",
        "graceful-fs": "^4.2.9",
        "micromatch": "^4.0.4",
        "pretty-format": "^27.5.1",
        "slash": "^3.0.0",
        "stack-utils": "^2.0.3"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-mock": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-mock/-/jest-mock-27.5.1.tgz",
      "integrity": "sha512-K4jKbY1d4ENhbrG2zuPWaQBvDly+iZ2yAW+T1fATN78hc0sInwn7wZB8XtlNnvHug5RMwV897Xm4LqmPM4e2Og==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@types/node": "*"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-pnp-resolver": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/jest-pnp-resolver/-/jest-pnp-resolver-1.2.3.tgz",
      "integrity": "sha512-+3NpwQEnRoIBtx4fyhblQDPgJI0H1IEIkX7ShLUjPGA7TtUTvI1oiKi3SR4oBR0hQhQR80l4WAe5RrXBwWMA8w==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "peerDependencies": {
        "jest-resolve": "*"
      },
      "peerDependenciesMeta": {
        "jest-resolve": {
          "optional": true
        }
      }
    },
    "node_modules/jest-regex-util": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-regex-util/-/jest-regex-util-27.5.1.tgz",
      "integrity": "sha512-4bfKq2zie+x16okqDXjXn9ql2B0dScQu+vcwe4TvFVhkVyuWLqpZrZtXxLLWoXYgn0E87I6r6GRYHF7wFZBUvg==",
      "license": "MIT",
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-resolve": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-resolve/-/jest-resolve-27.5.1.tgz",
      "integrity": "sha512-FFDy8/9E6CV83IMbDpcjOhumAQPDyETnU2KZ1O98DwTnz8AOBsW/Xv3GySr1mOZdItLR+zDZ7I/UdTFbgSOVCw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "chalk": "^4.0.0",
        "graceful-fs": "^4.2.9",
        "jest-haste-map": "^27.5.1",
        "jest-pnp-resolver": "^1.2.2",
        "jest-util": "^27.5.1",
        "jest-validate": "^27.5.1",
        "resolve": "^1.20.0",
        "resolve.exports": "^1.1.0",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-resolve-dependencies": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-resolve-dependencies/-/jest-resolve-dependencies-27.5.1.tgz",
      "integrity": "sha512-QQOOdY4PE39iawDn5rzbIePNigfe5B9Z91GDD1ae/xNDlu9kaat8QQ5EKnNmVWPV54hUdxCVwwj6YMgR2O7IOg==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-snapshot": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-runner": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-runner/-/jest-runner-27.5.1.tgz",
      "integrity": "sha512-g4NPsM4mFCOwFKXO4p/H/kWGdJp9V8kURY2lX8Me2drgXqG7rrZAx5kv+5H7wtt/cdFIjhqYx1HrlqWHaOvDaQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/console": "^27.5.1",
        "@jest/environment": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "emittery": "^0.8.1",
        "graceful-fs": "^4.2.9",
        "jest-docblock": "^27.5.1",
        "jest-environment-jsdom": "^27.5.1",
        "jest-environment-node": "^27.5.1",
        "jest-haste-map": "^27.5.1",
        "jest-leak-detector": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-runtime": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-worker": "^27.5.1",
        "source-map-support": "^0.5.6",
        "throat": "^6.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-runtime": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-runtime/-/jest-runtime-27.5.1.tgz",
      "integrity": "sha512-o7gxw3Gf+H2IGt8fv0RiyE1+r83FJBRruoA+FXrlHw6xEyBsU8ugA6IPfTdVyA0w8HClpbK+DGJxH59UrNMx8A==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/fake-timers": "^27.5.1",
        "@jest/globals": "^27.5.1",
        "@jest/source-map": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "chalk": "^4.0.0",
        "cjs-module-lexer": "^1.0.0",
        "collect-v8-coverage": "^1.0.0",
        "execa": "^5.0.0",
        "glob": "^7.1.3",
        "graceful-fs": "^4.2.9",
        "jest-haste-map": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-mock": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-snapshot": "^27.5.1",
        "jest-util": "^27.5.1",
        "slash": "^3.0.0",
        "strip-bom": "^4.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-serializer": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-serializer/-/jest-serializer-27.5.1.tgz",
      "integrity": "sha512-jZCyo6iIxO1aqUxpuBlwTDMkzOAJS4a3eYz3YzgxxVQFwLeSA7Jfq5cbqCY+JLvTDrWirgusI/0KwxKMgrdf7w==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "graceful-fs": "^4.2.9"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-snapshot": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-snapshot/-/jest-snapshot-27.5.1.tgz",
      "integrity": "sha512-yYykXI5a0I31xX67mgeLw1DZ0bJB+gpq5IpSuCAoyDi0+BhgU/RIrL+RTzDmkNTchvDFWKP8lp+w/42Z3us5sA==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.7.2",
        "@babel/generator": "^7.7.2",
        "@babel/plugin-syntax-typescript": "^7.7.2",
        "@babel/traverse": "^7.7.2",
        "@babel/types": "^7.0.0",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/babel__traverse": "^7.0.4",
        "@types/prettier": "^2.1.5",
        "babel-preset-current-node-syntax": "^1.0.0",
        "chalk": "^4.0.0",
        "expect": "^27.5.1",
        "graceful-fs": "^4.2.9",
        "jest-diff": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "jest-haste-map": "^27.5.1",
        "jest-matcher-utils": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-util": "^27.5.1",
        "natural-compare": "^1.4.0",
        "pretty-format": "^27.5.1",
        "semver": "^7.3.2"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-util": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-util/-/jest-util-27.5.1.tgz",
      "integrity": "sha512-Kv2o/8jNvX1MQ0KGtw480E/w4fBCDOnH6+6DmeKi6LZUIlKA5kwY0YNdlzaWTiVgxqAqik11QyxDOKk543aKXw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "ci-info": "^3.2.0",
        "graceful-fs": "^4.2.9",
        "picomatch": "^2.2.3"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-validate": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-validate/-/jest-validate-27.5.1.tgz",
      "integrity": "sha512-thkNli0LYTmOI1tDB3FI1S1RTp/Bqyd9pTarJwL87OIBFuqEb5Apv5EaApEudYg4g86e3CT6kM0RowkhtEnCBQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "camelcase": "^6.2.0",
        "chalk": "^4.0.0",
        "jest-get-type": "^27.5.1",
        "leven": "^3.1.0",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-watch-typeahead": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/jest-watch-typeahead/-/jest-watch-typeahead-1.1.0.tgz",
      "integrity": "sha512-Va5nLSJTN7YFtC2jd+7wsoe1pNe5K4ShLux/E5iHEwlB9AxaxmggY7to9KUqKojhaJw3aXqt5WAb4jGPOolpEw==",
      "license": "MIT",
      "dependencies": {
        "ansi-escapes": "^4.3.1",
        "chalk": "^4.0.0",
        "jest-regex-util": "^28.0.0",
        "jest-watcher": "^28.0.0",
        "slash": "^4.0.0",
        "string-length": "^5.0.1",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "peerDependencies": {
        "jest": "^27.0.0 || ^28.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@jest/console": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/@jest/console/-/console-28.1.3.tgz",
      "integrity": "sha512-QPAkP5EwKdK/bxIr6C1I4Vs0rm2nHiANzj/Z5X2JQkrZo6IqvC4ldZ9K95tF0HdidhA8Bo6egxSzUFPYKcEXLw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^28.1.3",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "jest-message-util": "^28.1.3",
        "jest-util": "^28.1.3",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@jest/console/node_modules/slash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-3.0.0.tgz",
      "integrity": "sha512-g9Q1haeby36OSStwb4ntCGGGaKsaVSjQ68fBxoQcutl5fS1vuY18H3wSt3jFyFtrkx+Kz0V1G85A4MyAdDMi2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@jest/test-result": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/@jest/test-result/-/test-result-28.1.3.tgz",
      "integrity": "sha512-kZAkxnSE+FqE8YjW8gNuoVkkC9I7S1qmenl8sGcDOLropASP+BkcGKwhXoyqQuGOGeYY0y/ixjrd/iERpEXHNg==",
      "license": "MIT",
      "dependencies": {
        "@jest/console": "^28.1.3",
        "@jest/types": "^28.1.3",
        "@types/istanbul-lib-coverage": "^2.0.0",
        "collect-v8-coverage": "^1.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@jest/types": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/@jest/types/-/types-28.1.3.tgz",
      "integrity": "sha512-RyjiyMUZrKz/c+zlMFO1pm70DcIlST8AeWTkoUdZevew44wcNZQHsEVOiCVtgVnlFFD82FPaXycys58cf2muVQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/schemas": "^28.1.3",
        "@types/istanbul-lib-coverage": "^2.0.0",
        "@types/istanbul-reports": "^3.0.0",
        "@types/node": "*",
        "@types/yargs": "^17.0.8",
        "chalk": "^4.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@types/yargs": {
      "version": "17.0.35",
      "resolved": "https://registry.npmjs.org/@types/yargs/-/yargs-17.0.35.tgz",
      "integrity": "sha512-qUHkeCyQFxMXg79wQfTtfndEC+N9ZZg76HJftDJp+qH2tV7Gj4OJi7l+PiWwJ+pWtW8GwSmqsDj/oymhrTWXjg==",
      "license": "MIT",
      "dependencies": {
        "@types/yargs-parser": "*"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/ansi-styles": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-5.2.0.tgz",
      "integrity": "sha512-Cxwpt2SfTzTtXcfOlzGEee8O+c+MmUgGrNiBcXnuWxuFJHe6a5Hz7qwhwe5OgaSYI0IJvkLqWX1ASG+cJOkEiA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/emittery": {
      "version": "0.10.2",
      "resolved": "https://registry.npmjs.org/emittery/-/emittery-0.10.2.tgz",
      "integrity": "sha512-aITqOwnLanpHLNXZJENbOgjUBeHocD+xsSJmNrjovKBW5HbSpW3d1pEls7GFQPUWXiwG9+0P4GtHfEqC/4M0Iw==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sindresorhus/emittery?sponsor=1"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-message-util": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/jest-message-util/-/jest-message-util-28.1.3.tgz",
      "integrity": "sha512-PFdn9Iewbt575zKPf1286Ht9EPoJmYT7P0kY+RibeYZ2XtOr53pDLEFoTWXbd1h4JiGiWpTBC84fc8xMXQMb7g==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.12.13",
        "@jest/types": "^28.1.3",
        "@types/stack-utils": "^2.0.0",
        "chalk": "^4.0.0",
        "graceful-fs": "^4.2.9",
        "micromatch": "^4.0.4",
        "pretty-format": "^28.1.3",
        "slash": "^3.0.0",
        "stack-utils": "^2.0.3"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-message-util/node_modules/slash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-3.0.0.tgz",
      "integrity": "sha512-g9Q1haeby36OSStwb4ntCGGGaKsaVSjQ68fBxoQcutl5fS1vuY18H3wSt3jFyFtrkx+Kz0V1G85A4MyAdDMi2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-regex-util": {
      "version": "28.0.2",
      "resolved": "https://registry.npmjs.org/jest-regex-util/-/jest-regex-util-28.0.2.tgz",
      "integrity": "sha512-4s0IgyNIy0y9FK+cjoVYoxamT7Zeo7MhzqRGx7YDYmaQn1wucY9rotiGkBzzcMXTtjrCAP/f7f+E0F7+fxPNdw==",
      "license": "MIT",
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-util": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/jest-util/-/jest-util-28.1.3.tgz",
      "integrity": "sha512-XdqfpHwpcSRko/C35uLYFM2emRAltIIKZiJ9eAmhjsj0CqZMa0p1ib0R5fWIqGhn1a103DebTbpqIaP1qCQ6tQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^28.1.3",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "ci-info": "^3.2.0",
        "graceful-fs": "^4.2.9",
        "picomatch": "^2.2.3"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-watcher": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/jest-watcher/-/jest-watcher-28.1.3.tgz",
      "integrity": "sha512-t4qcqj9hze+jviFPUN3YAtAEeFnr/azITXQEMARf5cMwKY2SMBRnCQTXLixTl20OR6mLh9KLMrgVJgJISym+1g==",
      "license": "MIT",
      "dependencies": {
        "@jest/test-result": "^28.1.3",
        "@jest/types": "^28.1.3",
        "@types/node": "*",
        "ansi-escapes": "^4.2.1",
        "chalk": "^4.0.0",
        "emittery": "^0.10.2",
        "jest-util": "^28.1.3",
        "string-length": "^4.0.1"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-watcher/node_modules/string-length": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/string-length/-/string-length-4.0.2.tgz",
      "integrity": "sha512-+l6rNN5fYHNhZZy41RXsYptCjA2Igmq4EG7kZAYFQI1E1VTXarr6ZPXBg6eq7Y6eK4FEhY6AJlyuFIb/v/S0VQ==",
      "license": "MIT",
      "dependencies": {
        "char-regex": "^1.0.2",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-watcher/node_modules/strip-ansi": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/pretty-format": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/pretty-format/-/pretty-format-28.1.3.tgz",
      "integrity": "sha512-8gFb/To0OmxHR9+ZTb14Df2vNxdGCX8g1xWGUTqUw5TiZvcQf5sHKObd5UcPyLLyowNwDAMTF3XWOG1B6mxl1Q==",
      "license": "MIT",
      "dependencies": {
        "@jest/schemas": "^28.1.3",
        "ansi-regex": "^5.0.1",
        "ansi-styles": "^5.0.0",
        "react-is": "^18.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/react-is": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-18.3.1.tgz",
      "integrity": "sha512-/LLMVyas0ljjAtoYiPqYiL8VWXzUUdThrmU5+n20DZv+a+ClRoevUzw5JxU+Ieh5/c87ytoTBV9G1FiKfNJdmg==",
      "license": "MIT"
    },
    "node_modules/jest-watch-typeahead/node_modules/slash": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-4.0.0.tgz",
      "integrity": "sha512-3dOsAHXXUkQTpOYcoAxLIorMTp4gIQr5IW3iVb7A7lFIp0VHhnynm9izx6TssdrIcVIESAlVjtnO2K8bg+Coew==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/string-length": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/string-length/-/string-length-5.0.1.tgz",
      "integrity": "sha512-9Ep08KAMUn0OadnVaBuRdE2l615CQ508kr0XMadjClfYpdCyvrbFp6Taebo8yyxokQ4viUd/xPPUA4FGgUa0ow==",
      "license": "MIT",
      "dependencies": {
        "char-regex": "^2.0.0",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": ">=12.20"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/string-length/node_modules/char-regex": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/char-regex/-/char-regex-2.0.2.tgz",
      "integrity": "sha512-cbGOjAptfM2LVmWhwRFHEKTPkLwNddVmuqYZQt895yXwAsWsXObCG+YN4DGQ/JBtT4GP1a1lPPdio2z413LmTg==",
      "license": "MIT",
      "engines": {
        "node": ">=12.20"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/strip-ansi": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-7.2.0.tgz",
      "integrity": "sha512-yDPMNjp4WyfYBkHnjIRLfca1i6KMyGCtsVgoKe/z1+6vukgaENdgGBZt+ZmKPc4gavvEZ5OgHfHdrazhgNyG7w==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^6.2.2"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/strip-ansi?sponsor=1"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/strip-ansi/node_modules/ansi-regex": {
      "version": "6.2.2",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-6.2.2.tgz",
      "integrity": "sha512-Bq3SmSpyFHaWjPk8If9yc6svM8c56dB5BAtW4Qbw5jHTwwXXcTLoRMkpDJp6VL0XzlWaCHTXrkFURMYmD0sLqg==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-regex?sponsor=1"
      }
    },
    "node_modules/jest-watcher": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-watcher/-/jest-watcher-27.5.1.tgz",
      "integrity": "sha512-z676SuD6Z8o8qbmEGhoEUFOM1+jfEiL3DXHK/xgEiG2EyNYfFG60jluWcupY6dATjfEsKQuibReS1djInQnoVw==",
      "license": "MIT",
      "dependencies": {
        "@jest/test-result": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "ansi-escapes": "^4.2.1",
        "chalk": "^4.0.0",
        "jest-util": "^27.5.1",
        "string-length": "^4.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-worker": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-worker/-/jest-worker-27.5.1.tgz",
      "integrity": "sha512-7vuh85V5cdDofPyxn58nrPjBktZo0u9x1g8WtjQol+jZDaE+fhN+cIvTj11GndBnMnyfrUOG1sZQxCdjKh+DKg==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "merge-stream": "^2.0.0",
        "supports-color": "^8.0.0"
      },
      "engines": {
        "node": ">= 10.13.0"
      }
    },
    "node_modules/jest-worker/node_modules/supports-color": {
      "version": "8.1.1",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-8.1.1.tgz",
      "integrity": "sha512-MpUEN2OodtUzxvKQl72cUF7RQ5EiHsGvSsVG0ia9c5RbWGL2CI4C7EpPS8UTBIplnlzZiNuV56w+FuNxy3ty2Q==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/supports-color?sponsor=1"
      }
    },
    "node_modules/jiti": {
      "version": "1.21.7",
      "resolved": "https://registry.npmjs.org/jiti/-/jiti-1.21.7.tgz",
      "integrity": "sha512-/imKNG4EbWNrVjoNC/1H5/9GFy+tqjGBHCaSsN+P2RnPqjsLmv6UD3Ej+Kj8nBWaRAwyk7kK5ZUc+OEatnTR3A==",
      "license": "MIT",
      "bin": {
        "jiti": "bin/jiti.js"
      }
    },
    "node_modules/js-tokens": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/js-tokens/-/js-tokens-4.0.0.tgz",
      "integrity": "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==",
      "license": "MIT"
    },
    "node_modules/js-yaml": {
      "version": "3.14.2",
      "resolved": "https://registry.npmjs.org/js-yaml/-/js-yaml-3.14.2.tgz",
      "integrity": "sha512-PMSmkqxr106Xa156c2M265Z+FTrPl+oxd/rgOQy2tijQeK5TxQ43psO1ZCwhVOSdnn+RzkzlRz/eY4BgJBYVpg==",
      "license": "MIT",
      "dependencies": {
        "argparse": "^1.0.7",
        "esprima": "^4.0.0"
      },
      "bin": {
        "js-yaml": "bin/js-yaml.js"
      }
    },
    "node_modules/jsdom": {
      "version": "16.7.0",
      "resolved": "https://registry.npmjs.org/jsdom/-/jsdom-16.7.0.tgz",
      "integrity": "sha512-u9Smc2G1USStM+s/x1ru5Sxrl6mPYCbByG1U/hUmqaVsm4tbNyS7CicOSRyuGQYZhTu0h84qkZZQ/I+dzizSVw==",
      "license": "MIT",
      "dependencies": {
        "abab": "^2.0.5",
        "acorn": "^8.2.4",
        "acorn-globals": "^6.0.0",
        "cssom": "^0.4.4",
        "cssstyle": "^2.3.0",
        "data-urls": "^2.0.0",
        "decimal.js": "^10.2.1",
        "domexception": "^2.0.1",
        "escodegen": "^2.0.0",
        "form-data": "^3.0.0",
        "html-encoding-sniffer": "^2.0.1",
        "http-proxy-agent": "^4.0.1",
        "https-proxy-agent": "^5.0.0",
        "is-potential-custom-element-name": "^1.0.1",
        "nwsapi": "^2.2.0",
        "parse5": "6.0.1",
        "saxes": "^5.0.1",
        "symbol-tree": "^3.2.4",
        "tough-cookie": "^4.0.0",
        "w3c-hr-time": "^1.0.2",
        "w3c-xmlserializer": "^2.0.0",
        "webidl-conversions": "^6.1.0",
        "whatwg-encoding": "^1.0.5",
        "whatwg-mimetype": "^2.3.0",
        "whatwg-url": "^8.5.0",
        "ws": "^7.4.6",
        "xml-name-validator": "^3.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "canvas": "^2.5.0"
      },
      "peerDependenciesMeta": {
        "canvas": {
          "optional": true
        }
      }
    },
    "node_modules/jsesc": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/jsesc/-/jsesc-3.1.0.tgz",
      "integrity": "sha512-/sM3dO2FOzXjKQhJuo0Q173wf2KOo8t4I8vHy6lF9poUp7bKT0/NHE8fPX23PwfhnykfqnC2xRxOnVw5XuGIaA==",
      "license": "MIT",
      "bin": {
        "jsesc": "bin/jsesc"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/json-buffer": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/json-buffer/-/json-buffer-3.0.1.tgz",
      "integrity": "sha512-4bV5BfR2mqfQTJm+V5tPPdf+ZpuhiIvTuAB5g8kcrXOZpTT/QwwVRWBywX1ozr6lEuPdbHxwaJlm9G6mI2sfSQ==",
      "license": "MIT"
    },
    "node_modules/json-parse-even-better-errors": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/json-parse-even-better-errors/-/json-parse-even-better-errors-2.3.1.tgz",
      "integrity": "sha512-xyFwyhro/JEof6Ghe2iz2NcXoj2sloNsWr/XsERDK/oiPCfaNhl5ONfp+jQdAZRQQ0IJWNzH9zIZF7li91kh2w==",
      "license": "MIT"
    },
    "node_modules/json-schema": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/json-schema/-/json-schema-0.4.0.tgz",
      "integrity": "sha512-es94M3nTIfsEPisRafak+HDLfHXnKBhV3vU5eqPcS3flIWqcxJWgXHXiey3YrpaNsanY5ei1VoYEbOzijuq9BA==",
      "license": "(AFL-2.1 OR BSD-3-Clause)"
    },
    "node_modules/json-schema-traverse": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-0.4.1.tgz",
      "integrity": "sha512-xbbCH5dCYU5T8LcEhhuh7HJ88HXuW3qsI3Y0zOZFKfZEHcpWiHU/Jxzk629Brsab/mMiHQti9wMP+845RPe3Vg==",
      "license": "MIT"
    },
    "node_modules/json-stable-stringify-without-jsonify": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/json-stable-stringify-without-jsonify/-/json-stable-stringify-without-jsonify-1.0.1.tgz",
      "integrity": "sha512-Bdboy+l7tA3OGW6FjyFHWkP5LuByj1Tk33Ljyq0axyzdk9//JSi2u3fP1QSmd1KNwq6VOKYGlAu87CisVir6Pw==",
      "license": "MIT"
    },
    "node_modules/json5": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/json5/-/json5-2.2.3.tgz",
      "integrity": "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg==",
      "license": "MIT",
      "bin": {
        "json5": "lib/cli.js"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/jsonfile": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/jsonfile/-/jsonfile-6.2.0.tgz",
      "integrity": "sha512-FGuPw30AdOIUTRMC2OMRtQV+jkVj2cfPqSeWXv1NEAJ1qZ5zb1X6z1mFhbfOB/iy3ssJCD+3KuZ8r8C3uVFlAg==",
      "license": "MIT",
      "dependencies": {
        "universalify": "^2.0.0"
      },
      "optionalDependencies": {
        "graceful-fs": "^4.1.6"
      }
    },
    "node_modules/jsonpath": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/jsonpath/-/jsonpath-1.3.0.tgz",
      "integrity": "sha512-0kjkYHJBkAy50Z5QzArZ7udmvxrJzkpKYW27fiF//BrMY7TQibYLl+FYIXN2BiYmwMIVzSfD8aDRj6IzgBX2/w==",
      "license": "MIT",
      "dependencies": {
        "esprima": "1.2.5",
        "static-eval": "2.1.1",
        "underscore": "1.13.6"
      }
    },
    "node_modules/jsonpath/node_modules/esprima": {
      "version": "1.2.5",
      "resolved": "https://registry.npmjs.org/esprima/-/esprima-1.2.5.tgz",
      "integrity": "sha512-S9VbPDU0adFErpDai3qDkjq8+G05ONtKzcyNrPKg/ZKa+tf879nX2KexNU95b31UoTJjRLInNBHHHjFPoCd7lQ==",
      "bin": {
        "esparse": "bin/esparse.js",
        "esvalidate": "bin/esvalidate.js"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/jsonpointer": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/jsonpointer/-/jsonpointer-5.0.1.tgz",
      "integrity": "sha512-p/nXbhSEcu3pZRdkW1OfJhpsVtW1gd4Wa1fnQc9YLiTfAjn0312eMKimbdIQzuZl9aa9xUGaRlP9T/CJE/ditQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/jsx-ast-utils": {
      "version": "3.3.5",
      "resolved": "https://registry.npmjs.org/jsx-ast-utils/-/jsx-ast-utils-3.3.5.tgz",
      "integrity": "sha512-ZZow9HBI5O6EPgSJLUb8n2NKgmVWTwCvHGwFuJlMjvLFqlGG6pjirPhtdsseaLZjSibD8eegzmYpUZwoIlj2cQ==",
      "license": "MIT",
      "dependencies": {
        "array-includes": "^3.1.6",
        "array.prototype.flat": "^1.3.1",
        "object.assign": "^4.1.4",
        "object.values": "^1.1.6"
      },
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/keyv": {
      "version": "4.5.4",
      "resolved": "https://registry.npmjs.org/keyv/-/keyv-4.5.4.tgz",
      "integrity": "sha512-oxVHkHR/EJf2CNXnWxRLW6mg7JyCCUcG0DtEGmL2ctUo1PNTin1PUil+r/+4r5MpVgC/fn1kjsx7mjSujKqIpw==",
      "license": "MIT",
      "dependencies": {
        "json-buffer": "3.0.1"
      }
    },
    "node_modules/kind-of": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/kind-of/-/kind-of-6.0.3.tgz",
      "integrity": "sha512-dcS1ul+9tmeD95T+x28/ehLgd9mENa3LsvDTtzm3vyBEO7RPptvAD+t44WVXaUjTBRcrpFeFlC8WCruUR456hw==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/kleur": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/kleur/-/kleur-3.0.3.tgz",
      "integrity": "sha512-eTIzlVOSUR+JxdDFepEYcBMtZ9Qqdef+rnzWdRZuMbOywu5tO2w2N7rqjoANZ5k9vywhL6Br1VRjUIgTQx4E8w==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/klona": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/klona/-/klona-2.0.6.tgz",
      "integrity": "sha512-dhG34DXATL5hSxJbIexCft8FChFXtmskoZYnoPWjXQuebWYCNkVeV3KkGegCK9CP1oswI/vQibS2GY7Em/sJJA==",
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/language-subtag-registry": {
      "version": "0.3.23",
      "resolved": "https://registry.npmjs.org/language-subtag-registry/-/language-subtag-registry-0.3.23.tgz",
      "integrity": "sha512-0K65Lea881pHotoGEa5gDlMxt3pctLi2RplBb7Ezh4rRdLEOtgi7n4EwK9lamnUCkKBqaeKRVebTq6BAxSkpXQ==",
      "license": "CC0-1.0"
    },
    "node_modules/language-tags": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/language-tags/-/language-tags-1.0.9.tgz",
      "integrity": "sha512-MbjN408fEndfiQXbFQ1vnd+1NoLDsnQW41410oQBXiyXDMYH5z505juWa4KUE1LqxRC7DgOgZDbKLxHIwm27hA==",
      "license": "MIT",
      "dependencies": {
        "language-subtag-registry": "^0.3.20"
      },
      "engines": {
        "node": ">=0.10"
      }
    },
    "node_modules/launch-editor": {
      "version": "2.13.1",
      "resolved": "https://registry.npmjs.org/launch-editor/-/launch-editor-2.13.1.tgz",
      "integrity": "sha512-lPSddlAAluRKJ7/cjRFoXUFzaX7q/YKI7yPHuEvSJVqoXvFnJov1/Ud87Aa4zULIbA9Nja4mSPK8l0z/7eV2wA==",
      "license": "MIT",
      "dependencies": {
        "picocolors": "^1.1.1",
        "shell-quote": "^1.8.3"
      }
    },
    "node_modules/leven": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/leven/-/leven-3.1.0.tgz",
      "integrity": "sha512-qsda+H8jTaUaN/x5vzW2rzc+8Rw4TAQ/4KjB46IwK5VH+IlVeeeje/EoZRpiXvIqjFgK84QffqPztGI3VBLG1A==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/levn": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/levn/-/levn-0.4.1.tgz",
      "integrity": "sha512-+bT2uH4E5LGE7h/n3evcS/sQlJXCpIp6ym8OWJ5eV6+67Dsql/LaaT7qJBAt2rzfoa/5QBGBhxDix1dMt2kQKQ==",
      "license": "MIT",
      "dependencies": {
        "prelude-ls": "^1.2.1",
        "type-check": "~0.4.0"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/lilconfig": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/lilconfig/-/lilconfig-2.1.0.tgz",
      "integrity": "sha512-utWOt/GHzuUxnLKxB6dk81RoOeoNeHgbrXiuGk4yyF5qlRz+iIVWu56E2fqGHFrXz0QNUhLB/8nKqvRH66JKGQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/lines-and-columns": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/lines-and-columns/-/lines-and-columns-1.2.4.tgz",
      "integrity": "sha512-7ylylesZQ/PV29jhEDl3Ufjo6ZX7gCqJr5F7PKrqc93v7fzSymt1BpwEU8nAUXs8qzzvqhbjhK5QZg6Mt/HkBg==",
      "license": "MIT"
    },
    "node_modules/loader-runner": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/loader-runner/-/loader-runner-4.3.1.tgz",
      "integrity": "sha512-IWqP2SCPhyVFTBtRcgMHdzlf9ul25NwaFx4wCEH/KjAXuuHY4yNjvPXsBokp8jCB936PyWRaPKUNh8NvylLp2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=6.11.5"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/loader-utils": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/loader-utils/-/loader-utils-2.0.4.tgz",
      "integrity": "sha512-xXqpXoINfFhgua9xiqD8fPFHgkoq1mmmpE92WlDbm9rNRd/EbRb+Gqf908T2DMfuHjjJlksiK2RbHVOdD/MqSw==",
      "license": "MIT",
      "dependencies": {
        "big.js": "^5.2.2",
        "emojis-list": "^3.0.0",
        "json5": "^2.1.2"
      },
      "engines": {
        "node": ">=8.9.0"
      }
    },
    "node_modules/locate-path": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-5.0.0.tgz",
      "integrity": "sha512-t7hw9pI+WvuwNJXwk5zVHpyhIqzg2qTlklJOf0mVxGSbe3Fp2VieZcduNYjaLDoy6p9uGpQEGWG87WpMKlNq8g==",
      "license": "MIT",
      "dependencies": {
        "p-locate": "^4.1.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/lodash": {
      "version": "4.17.23",
      "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.17.23.tgz",
      "integrity": "sha512-LgVTMpQtIopCi79SJeDiP0TfWi5CNEc/L/aRdTh3yIvmZXTnheWpKjSZhnvMl8iXbC1tFg9gdHHDMLoV7CnG+w==",
      "license": "MIT"
    },
    "node_modules/lodash.debounce": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/lodash.debounce/-/lodash.debounce-4.0.8.tgz",
      "integrity": "sha512-FT1yDzDYEoYWhnSGnpE/4Kj1fLZkDFyqRb7fNt6FdYOSxlUWAtp42Eh6Wb0rGIv/m9Bgo7x4GhQbm5Ys4SG5ow==",
      "license": "MIT"
    },
    "node_modules/lodash.memoize": {
      "version": "4.1.2",
      "resolved": "https://registry.npmjs.org/lodash.memoize/-/lodash.memoize-4.1.2.tgz",
      "integrity": "sha512-t7j+NzmgnQzTAYXcsHYLgimltOV1MXHtlOWf6GjL9Kj8GK5FInw5JotxvbOs+IvV1/Dzo04/fCGfLVs7aXb4Ag==",
      "license": "MIT"
    },
    "node_modules/lodash.merge": {
      "version": "4.6.2",
      "resolved": "https://registry.npmjs.org/lodash.merge/-/lodash.merge-4.6.2.tgz",
      "integrity": "sha512-0KpjqXRVvrYyCsX1swR/XTK0va6VQkQM6MNo7PqW77ByjAhoARA8EfrP1N4+KlKj8YS0ZUCtRT/YUuhyYDujIQ==",
      "license": "MIT"
    },
    "node_modules/lodash.sortby": {
      "version": "4.7.0",
      "resolved": "https://registry.npmjs.org/lodash.sortby/-/lodash.sortby-4.7.0.tgz",
      "integrity": "sha512-HDWXG8isMntAyRF5vZ7xKuEvOhT4AhlRt/3czTSjvGUxjYCBVRQY48ViDHyfYz9VIoBkW4TMGQNapx+l3RUwdA==",
      "license": "MIT"
    },
    "node_modules/lodash.uniq": {
      "version": "4.5.0",
      "resolved": "https://registry.npmjs.org/lodash.uniq/-/lodash.uniq-4.5.0.tgz",
      "integrity": "sha512-xfBaXQd9ryd9dlSDvnvI0lvxfLJlYAZzXomUYzLKtUeOQvOP5piqAWuGtrhWeqaXK9hhoM/iyJc5AV+XfsX3HQ==",
      "license": "MIT"
    },
    "node_modules/loose-envify": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/loose-envify/-/loose-envify-1.4.0.tgz",
      "integrity": "sha512-lyuxPGr/Wfhrlem2CL/UcnUc1zcqKAImBDzukY7Y5F/yQiNdko6+fRLevlw1HgMySw7f611UIY408EtxRSoK3Q==",
      "license": "MIT",
      "dependencies": {
        "js-tokens": "^3.0.0 || ^4.0.0"
      },
      "bin": {
        "loose-envify": "cli.js"
      }
    },
    "node_modules/lower-case": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/lower-case/-/lower-case-2.0.2.tgz",
      "integrity": "sha512-7fm3l3NAF9WfN6W3JOmf5drwpVqX78JtoGJ3A6W0a6ZnldM41w2fV5D490psKFTpMds8TJse/eHLFFsNHHjHgg==",
      "license": "MIT",
      "dependencies": {
        "tslib": "^2.0.3"
      }
    },
    "node_modules/lru-cache": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-5.1.1.tgz",
      "integrity": "sha512-KpNARQA3Iwv+jTA0utUVVbrh+Jlrr1Fv0e56GGzAFOXN7dk/FviaDW8LHmK52DlcH4WP2n6gI8vN1aesBFgo9w==",
      "license": "ISC",
      "dependencies": {
        "yallist": "^3.0.2"
      }
    },
    "node_modules/magic-string": {
      "version": "0.25.9",
      "resolved": "https://registry.npmjs.org/magic-string/-/magic-string-0.25.9.tgz",
      "integrity": "sha512-RmF0AsMzgt25qzqqLc1+MbHmhdx0ojF2Fvs4XnOqz2ZOBXzzkEwc/dJQZCYHAn7v1jbVOjAZfK8msRn4BxO4VQ==",
      "license": "MIT",
      "dependencies": {
        "sourcemap-codec": "^1.4.8"
      }
    },
    "node_modules/make-dir": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/make-dir/-/make-dir-3.1.0.tgz",
      "integrity": "sha512-g3FeP20LNwhALb/6Cz6Dd4F2ngze0jz7tbzrD2wAV+o9FeNHe4rL+yK2md0J/fiSf1sa1ADhXqi5+oVwOM/eGw==",
      "license": "MIT",
      "dependencies": {
        "semver": "^6.0.0"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/make-dir/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/makeerror": {
      "version": "1.0.12",
      "resolved": "https://registry.npmjs.org/makeerror/-/makeerror-1.0.12.tgz",
      "integrity": "sha512-JmqCvUhmt43madlpFzG4BQzG2Z3m6tvQDNKdClZnO3VbIudJYmxsT0FNJMeiB2+JTSlTQTSbU8QdesVmwJcmLg==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "tmpl": "1.0.5"
      }
    },
    "node_modules/math-intrinsics": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/math-intrinsics/-/math-intrinsics-1.1.0.tgz",
      "integrity": "sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/mdn-data": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/mdn-data/-/mdn-data-2.0.4.tgz",
      "integrity": "sha512-iV3XNKw06j5Q7mi6h+9vbx23Tv7JkjEVgKHW4pimwyDGWm0OIQntJJ+u1C6mg6mK1EaTv42XQ7w76yuzH7M2cA==",
      "license": "CC0-1.0"
    },
    "node_modules/media-typer": {
      "version": "0.3.0",
      "resolved": "https://registry.npmjs.org/media-typer/-/media-typer-0.3.0.tgz",
      "integrity": "sha512-dq+qelQ9akHpcOl/gUVRTxVIOkAJ1wR3QAvb4RsVjS8oVoFjDGTc679wJYmUmknUF5HwMLOgb5O+a3KxfWapPQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/memfs": {
      "version": "3.5.3",
      "resolved": "https://registry.npmjs.org/memfs/-/memfs-3.5.3.tgz",
      "integrity": "sha512-UERzLsxzllchadvbPs5aolHh65ISpKpM+ccLbOJ8/vvpBKmAWf+la7dXFy7Mr0ySHbdHrFv5kGFCUHHe6GFEmw==",
      "license": "Unlicense",
      "dependencies": {
        "fs-monkey": "^1.0.4"
      },
      "engines": {
        "node": ">= 4.0.0"
      }
    },
    "node_modules/merge-descriptors": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/merge-descriptors/-/merge-descriptors-1.0.3.tgz",
      "integrity": "sha512-gaNvAS7TZ897/rVaZ0nMtAyxNyi/pdbjbAwUpFQpN70GqnVfOiXpeUUMKRBmzXaSQ8DdTX4/0ms62r2K+hE6mQ==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/merge-stream": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/merge-stream/-/merge-stream-2.0.0.tgz",
      "integrity": "sha512-abv/qOcuPfk3URPfDzmZU1LKmuw8kT+0nIHvKrKgFrwifol/doWcdA4ZqsWQ8ENrFKkd67Mfpo/LovbIUsbt3w==",
      "license": "MIT"
    },
    "node_modules/merge2": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/merge2/-/merge2-1.4.1.tgz",
      "integrity": "sha512-8q7VEgMJW4J8tcfVPy8g09NcQwZdbwFEqhe/WZkoIzjn/3TGDwtOCYtXGxA3O8tPzpczCCDgv+P2P5y00ZJOOg==",
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/methods": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/methods/-/methods-1.1.2.tgz",
      "integrity": "sha512-iclAHeNqNm68zFtnZ0e+1L2yUIdvzNoauKU4WBA3VvH/vPFieF7qfRlwUZU+DA9P9bPXIS90ulxoUoCH23sV2w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/micromatch": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/micromatch/-/micromatch-4.0.8.tgz",
      "integrity": "sha512-PXwfBhYu0hBCPw8Dn0E+WDYb7af3dSLVWKi3HGv84IdF4TyFoC0ysxFd0Goxw7nSv4T/PzEJQxsYsEiFCKo2BA==",
      "license": "MIT",
      "dependencies": {
        "braces": "^3.0.3",
        "picomatch": "^2.3.1"
      },
      "engines": {
        "node": ">=8.6"
      }
    },
    "node_modules/mime": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/mime/-/mime-1.6.0.tgz",
      "integrity": "sha512-x0Vn8spI+wuJ1O6S7gnbaQg8Pxh4NNHb7KSINmEWKiPE4RKOplvijn+NkmYmmRgP68mc70j2EbeTFRsrswaQeg==",
      "license": "MIT",
      "bin": {
        "mime": "cli.js"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/mime-db": {
      "version": "1.52.0",
      "resolved": "https://registry.npmjs.org/mime-db/-/mime-db-1.52.0.tgz",
      "integrity": "sha512-sPU4uV7dYlvtWJxwwxHD0PuihVNiE7TyAbQ5SWxDCB9mUYvOgroQOwYQQOKPJ8CIbE+1ETVlOoK1UC2nU3gYvg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/mime-types": {
      "version": "2.1.35",
      "resolved": "https://registry.npmjs.org/mime-types/-/mime-types-2.1.35.tgz",
      "integrity": "sha512-ZDY+bPm5zTTF+YpCrAU9nK0UgICYPT0QtT1NZWFv4s++TNkcgVaT0g6+4R2uI4MjQjzysHB1zxuWL50hzaeXiw==",
      "license": "MIT",
      "dependencies": {
        "mime-db": "1.52.0"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/mimic-fn": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/mimic-fn/-/mimic-fn-2.1.0.tgz",
      "integrity": "sha512-OqbOk5oEQeAZ8WXWydlu9HJjz9WVdEIvamMCcXmuqUYjTknH/sqsWvhQ3vgwKFRR1HpjvNBKQ37nbJgYzGqGcg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/mini-css-extract-plugin": {
      "version": "2.10.1",
      "resolved": "https://registry.npmjs.org/mini-css-extract-plugin/-/mini-css-extract-plugin-2.10.1.tgz",
      "integrity": "sha512-k7G3Y5QOegl380tXmZ68foBRRjE9Ljavx835ObdvmZjQ639izvZD8CS7BkWw1qKPPzHsGL/JDhl0uyU1zc2rJw==",
      "license": "MIT",
      "dependencies": {
        "schema-utils": "^4.0.0",
        "tapable": "^2.2.1"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.0.0"
      }
    },
    "node_modules/minimalistic-assert": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/minimalistic-assert/-/minimalistic-assert-1.0.1.tgz",
      "integrity": "sha512-UtJcAD4yEaGtjPezWuO9wC4nwUnVH/8/Im3yEHQP4b67cXlD/Qr9hdITCU1xDbSEXg2XKNaP8jsReV7vQd00/A==",
      "license": "ISC"
    },
    "node_modules/minimatch": {
      "version": "3.1.5",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-3.1.5.tgz",
      "integrity": "sha512-VgjWUsnnT6n+NUk6eZq77zeFdpW2LWDzP6zFGrCbHXiYNul5Dzqk2HHQ5uFH2DNW5Xbp8+jVzaeNt94ssEEl4w==",
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^1.1.7"
      },
      "engines": {
        "node": "*"
      }
    },
    "node_modules/minimist": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/minimist/-/minimist-1.2.8.tgz",
      "integrity": "sha512-2yyAR8qBkN3YuheJanUpWC5U3bb5osDywNB8RzDVlDwDHbocAJveqqj1u8+SVD7jkWT4yvsHCpWqqWqAxb0zCA==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/mkdirp": {
      "version": "0.5.6",
      "resolved": "https://registry.npmjs.org/mkdirp/-/mkdirp-0.5.6.tgz",
      "integrity": "sha512-FP+p8RB8OWpF3YZBCrP5gtADmtXApB5AMLn+vdyA+PyxCjrCs00mjyUozssO33cwDeT3wNGdLxJ5M//YqtHAJw==",
      "license": "MIT",
      "dependencies": {
        "minimist": "^1.2.6"
      },
      "bin": {
        "mkdirp": "bin/cmd.js"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "license": "MIT"
    },
    "node_modules/multicast-dns": {
      "version": "7.2.5",
      "resolved": "https://registry.npmjs.org/multicast-dns/-/multicast-dns-7.2.5.tgz",
      "integrity": "sha512-2eznPJP8z2BFLX50tf0LuODrpINqP1RVIm/CObbTcBRITQgmC/TjcREF1NeTBzIcR5XO/ukWo+YHOjBbFwIupg==",
      "license": "MIT",
      "dependencies": {
        "dns-packet": "^5.2.2",
        "thunky": "^1.0.2"
      },
      "bin": {
        "multicast-dns": "cli.js"
      }
    },
    "node_modules/mz": {
      "version": "2.7.0",
      "resolved": "https://registry.npmjs.org/mz/-/mz-2.7.0.tgz",
      "integrity": "sha512-z81GNO7nnYMEhrGh9LeymoE4+Yr0Wn5McHIZMK5cfQCl+NDX08sCZgUc9/6MHni9IWuFLm1Z3HTCXu2z9fN62Q==",
      "license": "MIT",
      "dependencies": {
        "any-promise": "^1.0.0",
        "object-assign": "^4.0.1",
        "thenify-all": "^1.0.0"
      }
    },
    "node_modules/nanoid": {
      "version": "3.3.11",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.11.tgz",
      "integrity": "sha512-N8SpfPUnUp1bK+PMYW8qSWdl9U+wwNWI4QKxOYDy9JAro3WMX7p2OeVRF9v+347pnakNevPmiHhNmZ2HbFA76w==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/natural-compare": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/natural-compare/-/natural-compare-1.4.0.tgz",
      "integrity": "sha512-OWND8ei3VtNC9h7V60qff3SVobHr996CTwgxubgyQYEpg290h9J0buyECNNJexkFm5sOajh5G116RYA1c8ZMSw==",
      "license": "MIT"
    },
    "node_modules/natural-compare-lite": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/natural-compare-lite/-/natural-compare-lite-1.4.0.tgz",
      "integrity": "sha512-Tj+HTDSJJKaZnfiuw+iaF9skdPpTo2GtEly5JHnWV/hfv2Qj/9RKsGISQtLh2ox3l5EAGw487hnBee0sIJ6v2g==",
      "license": "MIT"
    },
    "node_modules/negotiator": {
      "version": "0.6.4",
      "resolved": "https://registry.npmjs.org/negotiator/-/negotiator-0.6.4.tgz",
      "integrity": "sha512-myRT3DiWPHqho5PrJaIRyaMv2kgYf0mUVgBNOYMuCH5Ki1yEiQaf/ZJuQ62nvpc44wL5WDbTX7yGJi1Neevw8w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/neo-async": {
      "version": "2.6.2",
      "resolved": "https://registry.npmjs.org/neo-async/-/neo-async-2.6.2.tgz",
      "integrity": "sha512-Yd3UES5mWCSqR+qNT93S3UoYUkqAZ9lLg8a7g9rimsWmYGK8cVToA4/sF3RrshdyV3sAGMXVUmpMYOw+dLpOuw==",
      "license": "MIT"
    },
    "node_modules/no-case": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/no-case/-/no-case-3.0.4.tgz",
      "integrity": "sha512-fgAN3jGAh+RoxUGZHTSOLJIqUc2wmoBwGR4tbpNAKmmovFoWq0OdRkb0VkldReO2a2iBT/OEulG9XSUc10r3zg==",
      "license": "MIT",
      "dependencies": {
        "lower-case": "^2.0.2",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/node-exports-info": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/node-exports-info/-/node-exports-info-1.6.0.tgz",
      "integrity": "sha512-pyFS63ptit/P5WqUkt+UUfe+4oevH+bFeIiPPdfb0pFeYEu/1ELnJu5l+5EcTKYL5M7zaAa7S8ddywgXypqKCw==",
      "license": "MIT",
      "dependencies": {
        "array.prototype.flatmap": "^1.3.3",
        "es-errors": "^1.3.0",
        "object.entries": "^1.1.9",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/node-exports-info/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/node-forge": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/node-forge/-/node-forge-1.3.3.tgz",
      "integrity": "sha512-rLvcdSyRCyouf6jcOIPe/BgwG/d7hKjzMKOas33/pHEr6gbq18IK9zV7DiPvzsz0oBJPme6qr6H6kGZuI9/DZg==",
      "license": "(BSD-3-Clause OR GPL-2.0)",
      "engines": {
        "node": ">= 6.13.0"
      }
    },
    "node_modules/node-int64": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/node-int64/-/node-int64-0.4.0.tgz",
      "integrity": "sha512-O5lz91xSOeoXP6DulyHfllpq+Eg00MWitZIbtPfoSEvqIHdl5gfcY6hYzDWnj0qD5tz52PI08u9qUvSVeUBeHw==",
      "license": "MIT"
    },
    "node_modules/node-releases": {
      "version": "2.0.36",
      "resolved": "https://registry.npmjs.org/node-releases/-/node-releases-2.0.36.tgz",
      "integrity": "sha512-TdC8FSgHz8Mwtw9g5L4gR/Sh9XhSP/0DEkQxfEFXOpiul5IiHgHan2VhYYb6agDSfp4KuvltmGApc8HMgUrIkA==",
      "license": "MIT"
    },
    "node_modules/normalize-path": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/normalize-path/-/normalize-path-3.0.0.tgz",
      "integrity": "sha512-6eZs5Ls3WtCisHWp9S2GUy8dqkpGi4BVSz3GaqiE6ezub0512ESztXUwUB6C6IKbQkY2Pnb/mD4WYojCRwcwLA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/normalize-url": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/normalize-url/-/normalize-url-6.1.0.tgz",
      "integrity": "sha512-DlL+XwOy3NxAQ8xuC0okPgK46iuVNAK01YN7RueYBqqFeGsBjV9XmCAzAdgt+667bCl5kPh9EqKKDwnaPG1I7A==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/npm-run-path": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/npm-run-path/-/npm-run-path-4.0.1.tgz",
      "integrity": "sha512-S48WzZW777zhNIrn7gxOlISNAqi9ZC/uQFnRdbeIHhZhCA6UqpkOT8T1G7BvfdgP4Er8gF4sUbaS0i7QvIfCWw==",
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/nth-check": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/nth-check/-/nth-check-2.1.1.tgz",
      "integrity": "sha512-lqjrjmaOoAnWfMmBPL+XNnynZh2+swxiX3WUE0s4yEHI6m+AwrK2UZOimIRl3X/4QctVqS8AiZjFqyOGrMXb/w==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "boolbase": "^1.0.0"
      },
      "funding": {
        "url": "https://github.com/fb55/nth-check?sponsor=1"
      }
    },
    "node_modules/nwsapi": {
      "version": "2.2.23",
      "resolved": "https://registry.npmjs.org/nwsapi/-/nwsapi-2.2.23.tgz",
      "integrity": "sha512-7wfH4sLbt4M0gCDzGE6vzQBo0bfTKjU7Sfpqy/7gs1qBfYz2vEJH6vXcBKpO3+6Yu1telwd0t9HpyOoLEQQbIQ==",
      "license": "MIT"
    },
    "node_modules/object-assign": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz",
      "integrity": "sha512-rJgTQnkUnH1sFw8yT6VSU3zD3sWmu6sZhIseY8VX+GRu3P6F7Fu+JNDoXfklElbLJSnc3FUQHVe4cU5hj+BcUg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/object-hash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/object-hash/-/object-hash-3.0.0.tgz",
      "integrity": "sha512-RSn9F68PjH9HqtltsSnqYC1XXoWe9Bju5+213R98cNGttag9q9yAOTzdbsqvIa7aNm5WffBZFpWYr2aWrklWAw==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/object-inspect": {
      "version": "1.13.4",
      "resolved": "https://registry.npmjs.org/object-inspect/-/object-inspect-1.13.4.tgz",
      "integrity": "sha512-W67iLl4J2EXEGTbfeHCffrjDfitvLANg0UlX3wFUUSTx92KXRFegMHUVgSqE+wvhAbi4WqjGg9czysTV2Epbew==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object-keys": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/object-keys/-/object-keys-1.1.1.tgz",
      "integrity": "sha512-NuAESUOUMrlIXOfHKzD6bpPu3tYt3xvjNdRIQ+FeT0lNb4K8WR70CaDxhuNguS2XG+GjkyMwOzsN5ZktImfhLA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.assign": {
      "version": "4.1.7",
      "resolved": "https://registry.npmjs.org/object.assign/-/object.assign-4.1.7.tgz",
      "integrity": "sha512-nK28WOo+QIjBkDduTINE4JkF/UJJKyf2EJxvJKfblDpyg0Q+pkOHNTL0Qwy6NP6FhE/EnzV73BxxqcJaXY9anw==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0",
        "has-symbols": "^1.1.0",
        "object-keys": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object.entries": {
      "version": "1.1.9",
      "resolved": "https://registry.npmjs.org/object.entries/-/object.entries-1.1.9.tgz",
      "integrity": "sha512-8u/hfXFRBD1O0hPUjioLhoWFHRmt6tKA4/vZPyckBr18l1KE9uHrFaFaUi8MDRTpi4uak2goyPTSNJLXX2k2Hw==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.fromentries": {
      "version": "2.0.8",
      "resolved": "https://registry.npmjs.org/object.fromentries/-/object.fromentries-2.0.8.tgz",
      "integrity": "sha512-k6E21FzySsSK5a21KRADBd/NGneRegFO5pLHfdQLpRDETUNJueLXs3WCzyQ3tFRDYgbq3KHGXfTbi2bs8WQ6rQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object.getownpropertydescriptors": {
      "version": "2.1.9",
      "resolved": "https://registry.npmjs.org/object.getownpropertydescriptors/-/object.getownpropertydescriptors-2.1.9.tgz",
      "integrity": "sha512-mt8YM6XwsTTovI+kdZdHSxoyF2DI59up034orlC9NfweclcWOt7CVascNNLp6U+bjFVCVCIh9PwS76tDM/rH8g==",
      "license": "MIT",
      "dependencies": {
        "array.prototype.reduce": "^1.0.8",
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.24.0",
        "es-object-atoms": "^1.1.1",
        "gopd": "^1.2.0",
        "safe-array-concat": "^1.1.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object.groupby": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/object.groupby/-/object.groupby-1.0.3.tgz",
      "integrity": "sha512-+Lhy3TQTuzXI5hevh8sBGqbmurHbbIjAi0Z4S63nthVLmLxfbj4T54a4CfZrXIrt9iP4mVAPYMo/v99taj3wjQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.values": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/object.values/-/object.values-1.2.1.tgz",
      "integrity": "sha512-gXah6aZrcUxjWg2zR2MwouP2eHlCBzdV4pygudehaKXSGW4v2AsRQUK+lwwXhii6KFZcunEnmSUoYp5CXibxtA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/obuf": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/obuf/-/obuf-1.1.2.tgz",
      "integrity": "sha512-PX1wu0AmAdPqOL1mWhqmlOd8kOIZQwGZw6rh7uby9fTc5lhaOWFLX3I6R1hrF9k3zUY40e6igsLGkDXK92LJNg==",
      "license": "MIT"
    },
    "node_modules/on-finished": {
      "version": "2.4.1",
      "resolved": "https://registry.npmjs.org/on-finished/-/on-finished-2.4.1.tgz",
      "integrity": "sha512-oVlzkg3ENAhCk2zdv7IJwd/QUD4z2RxRwpkcGY8psCVcCYZNq4wYnVWALHM+brtuJjePWiYF/ClmuDr8Ch5+kg==",
      "license": "MIT",
      "dependencies": {
        "ee-first": "1.1.1"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/on-headers": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/on-headers/-/on-headers-1.1.0.tgz",
      "integrity": "sha512-737ZY3yNnXy37FHkQxPzt4UZ2UWPWiCZWLvFZ4fu5cueciegX0zGPnrlY6bwRg4FdQOe9YU8MkmJwGhoMybl8A==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/once": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/once/-/once-1.4.0.tgz",
      "integrity": "sha512-lNaJgI+2Q5URQBkccEKHTQOPaXdUxnZZElQTZY0MFUAuaEqe1E+Nyvgdz/aIyNi6Z9MzO5dv1H8n58/GELp3+w==",
      "license": "ISC",
      "dependencies": {
        "wrappy": "1"
      }
    },
    "node_modules/onetime": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/onetime/-/onetime-5.1.2.tgz",
      "integrity": "sha512-kbpaSSGJTWdAY5KPVeMOKXSrPtr8C8C7wodJbcsd51jRnmD+GZu8Y0VoU6Dm5Z4vWr0Ig/1NKuWRKf7j5aaYSg==",
      "license": "MIT",
      "dependencies": {
        "mimic-fn": "^2.1.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/open": {
      "version": "8.4.2",
      "resolved": "https://registry.npmjs.org/open/-/open-8.4.2.tgz",
      "integrity": "sha512-7x81NCL719oNbsq/3mh+hVrAWmFuEYUqrq/Iw3kUzH8ReypT9QQ0BLoJS7/G9k6N81XjW4qHWtjWwe/9eLy1EQ==",
      "license": "MIT",
      "dependencies": {
        "define-lazy-prop": "^2.0.0",
        "is-docker": "^2.1.1",
        "is-wsl": "^2.2.0"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/optionator": {
      "version": "0.9.4",
      "resolved": "https://registry.npmjs.org/optionator/-/optionator-0.9.4.tgz",
      "integrity": "sha512-6IpQ7mKUxRcZNLIObR0hz7lxsapSSIYNZJwXPGeF0mTVqGKFIXj1DQcMoT22S3ROcLyY/rz0PWaWZ9ayWmad9g==",
      "license": "MIT",
      "dependencies": {
        "deep-is": "^0.1.3",
        "fast-levenshtein": "^2.0.6",
        "levn": "^0.4.1",
        "prelude-ls": "^1.2.1",
        "type-check": "^0.4.0",
        "word-wrap": "^1.2.5"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/own-keys": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/own-keys/-/own-keys-1.0.1.tgz",
      "integrity": "sha512-qFOyK5PjiWZd+QQIh+1jhdb9LpxTF0qs7Pm8o5QHYZ0M3vKqSqzsZaEB6oWlxZ+q2sJBMI/Ktgd2N5ZwQoRHfg==",
      "license": "MIT",
      "dependencies": {
        "get-intrinsic": "^1.2.6",
        "object-keys": "^1.1.1",
        "safe-push-apply": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/p-limit": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-2.3.0.tgz",
      "integrity": "sha512-//88mFWSJx8lxCzwdAABTJL2MyWB12+eIY7MDL2SqLmAkeKU9qxRvWuSyTjm3FUmpBEMuFfckAIqEaVGUDxb6w==",
      "license": "MIT",
      "dependencies": {
        "p-try": "^2.0.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/p-locate": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-4.1.0.tgz",
      "integrity": "sha512-R79ZZ/0wAxKGu3oYMlz8jy/kbhsNrS7SKZ7PxEHBgJ5+F2mtFW2fK2cOtBh1cHYkQsbzFV7I+EoRKe6Yt0oK7A==",
      "license": "MIT",
      "dependencies": {
        "p-limit": "^2.2.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/p-retry": {
      "version": "4.6.2",
      "resolved": "https://registry.npmjs.org/p-retry/-/p-retry-4.6.2.tgz",
      "integrity": "sha512-312Id396EbJdvRONlngUx0NydfrIQ5lsYu0znKVUzVvArzEIt08V1qhtyESbGVd1FGX7UKtiFp5uwKZdM8wIuQ==",
      "license": "MIT",
      "dependencies": {
        "@types/retry": "0.12.0",
        "retry": "^0.13.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/p-try": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/p-try/-/p-try-2.2.0.tgz",
      "integrity": "sha512-R4nPAVTAU0B9D35/Gk3uJf/7XYbQcyohSKdvAxIRSNghFl4e71hVoGnBNQz9cWaXxO2I10KTC+3jMdvvoKw6dQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/param-case": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/param-case/-/param-case-3.0.4.tgz",
      "integrity": "sha512-RXlj7zCYokReqWpOPH9oYivUzLYZ5vAPIfEmCTNViosC78F8F0H9y7T7gG2M39ymgutxF5gcFEsyZQSph9Bp3A==",
      "license": "MIT",
      "dependencies": {
        "dot-case": "^3.0.4",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/parent-module": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/parent-module/-/parent-module-1.0.1.tgz",
      "integrity": "sha512-GQ2EWRpQV8/o+Aw8YqtfZZPfNRWZYkbidE9k5rpl/hC3vtHHBfGm2Ifi6qWV+coDGkrUKZAxE3Lot5kcsRlh+g==",
      "license": "MIT",
      "dependencies": {
        "callsites": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/parse-json": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/parse-json/-/parse-json-5.2.0.tgz",
      "integrity": "sha512-ayCKvm/phCGxOkYRSCM82iDwct8/EonSEgCSxWxD7ve6jHggsFl4fZVQBPRNgQoKiuV/odhFrGzQXZwbifC8Rg==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.0.0",
        "error-ex": "^1.3.1",
        "json-parse-even-better-errors": "^2.3.0",
        "lines-and-columns": "^1.1.6"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/parse5": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/parse5/-/parse5-6.0.1.tgz",
      "integrity": "sha512-Ofn/CTFzRGTTxwpNEs9PP93gXShHcTq255nzRYSKe8AkVpZY7e1fpmTfOyoIvjP5HG7Z2ZM7VS9PPhQGW2pOpw==",
      "license": "MIT"
    },
    "node_modules/parseurl": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/parseurl/-/parseurl-1.3.3.tgz",
      "integrity": "sha512-CiyeOxFT/JZyN5m0z9PfXw4SCBJ6Sygz1Dpl0wqjlhDEGGBP1GnsUVEL0p63hoG1fcj3fHynXi9NYO4nWOL+qQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/pascal-case": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/pascal-case/-/pascal-case-3.1.2.tgz",
      "integrity": "sha512-uWlGT3YSnK9x3BQJaOdcZwrnV6hPpd8jFH1/ucpiLRPh/2zCVJKS19E4GvYHvaCcACn3foXZ0cLB9Wrx1KGe5g==",
      "license": "MIT",
      "dependencies": {
        "no-case": "^3.0.4",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/path-exists": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-exists/-/path-exists-4.0.0.tgz",
      "integrity": "sha512-ak9Qy5Q7jYb2Wwcey5Fpvg2KoAc/ZIhLSLOSBmRmygPsGwkVVt0fZa0qrtMz+m6tJTAHfZQ8FnmB4MG4LWy7/w==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-is-absolute": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/path-is-absolute/-/path-is-absolute-1.0.1.tgz",
      "integrity": "sha512-AVbw3UJ2e9bq64vSaS9Am0fje1Pa8pbGqTTsmXfaIiMpnr5DlDhfJOuLj9Sf95ZPVDAUerDfEk88MPmPe7UCQg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/path-key": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-3.1.1.tgz",
      "integrity": "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-parse": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/path-parse/-/path-parse-1.0.7.tgz",
      "integrity": "sha512-LDJzPVEEEPR+y48z93A0Ed0yXb8pAByGWo/k5YYdYgpY2/2EsOsksJrq7lOHxryrVOn1ejG6oAp8ahvOIQD8sw==",
      "license": "MIT"
    },
    "node_modules/path-to-regexp": {
      "version": "0.1.12",
      "resolved": "https://registry.npmjs.org/path-to-regexp/-/path-to-regexp-0.1.12.tgz",
      "integrity": "sha512-RA1GjUVMnvYFxuqovrEqZoxxW5NUZqbwKtYz/Tt7nXerk0LbLblQmrsgdeOxV5SFHf0UDggjS/bSeOZwt1pmEQ==",
      "license": "MIT"
    },
    "node_modules/path-type": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-type/-/path-type-4.0.0.tgz",
      "integrity": "sha512-gDKb8aZMDeD/tZWs9P6+q0J9Mwkdl6xMV8TjnGP3qJVJ06bdMgkbBlLU8IdfOsIsFz2BW1rNVT3XuNEl8zPAvw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/performance-now": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/performance-now/-/performance-now-2.1.0.tgz",
      "integrity": "sha512-7EAHlyLHI56VEIdK57uwHdHKIaAGbnXPiw0yWbarQZOKaKpvUIgW0jWRVLiatnM+XXlSwsanIBH/hzGMJulMow==",
      "license": "MIT"
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-2.3.1.tgz",
      "integrity": "sha512-JU3teHTNjmE2VCGFzuY8EXzCDVwEqB2a8fsIvwaStHhAWJEeVd1o1QD80CU6+ZdEXXSLbSsuLwJjkCBWqRQUVA==",
      "license": "MIT",
      "engines": {
        "node": ">=8.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/pify": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/pify/-/pify-2.3.0.tgz",
      "integrity": "sha512-udgsAY+fTnvv7kI7aaxbqwWNb0AHiB0qBO89PZKPkoTmGOgdbrHDKD+0B2X4uTfJ/FT1R09r9gTsjUjNJotuog==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/pirates": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/pirates/-/pirates-4.0.7.tgz",
      "integrity": "sha512-TfySrs/5nm8fQJDcBDuUng3VOUKsd7S+zqvbOTiGXHfxX4wK31ard+hoNuvkicM/2YFzlpDgABOevKSsB4G/FA==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/pkg-dir": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/pkg-dir/-/pkg-dir-4.2.0.tgz",
      "integrity": "sha512-HRDzbaKjC+AOWVXxAU/x54COGeIv9eb+6CkDSQoNTt4XyWoIJvuPsXizxu/Fr23EiekbtZwmh1IcIG/l/a10GQ==",
      "license": "MIT",
      "dependencies": {
        "find-up": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/pkg-up": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/pkg-up/-/pkg-up-3.1.0.tgz",
      "integrity": "sha512-nDywThFk1i4BQK4twPQ6TA4RT8bDY96yeuCVBWL3ePARCiEKDRSrNGbFIgUJpLp+XeIR65v8ra7WuJOFUBtkMA==",
      "license": "MIT",
      "dependencies": {
        "find-up": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/pkg-up/node_modules/find-up": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-3.0.0.tgz",
      "integrity": "sha512-1yD6RmLI1XBfxugvORwlck6f75tYL+iR0jqwsOrOxMZyGYqUuDhJ0l4AXdO1iX/FTs9cBAMEk1gWSEx1kSbylg==",
      "license": "MIT",
      "dependencies": {
        "locate-path": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/pkg-up/node_modules/locate-path": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-3.0.0.tgz",
      "integrity": "sha512-7AO748wWnIhNqAuaty2ZWHkQHRSNfPVIsPIfwEOWO22AmaoVrWavlOcMR5nzTLNYvp36X220/maaRsrec1G65A==",
      "license": "MIT",
      "dependencies": {
        "p-locate": "^3.0.0",
        "path-exists": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/pkg-up/node_modules/p-locate": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-3.0.0.tgz",
      "integrity": "sha512-x+12w/To+4GFfgJhBEpiDcLozRJGegY+Ei7/z0tSLkMmxGZNybVMSfWj9aJn8Z5Fc7dBUNJOOVgPv2H7IwulSQ==",
      "license": "MIT",
      "dependencies": {
        "p-limit": "^2.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/pkg-up/node_modules/path-exists": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/path-exists/-/path-exists-3.0.0.tgz",
      "integrity": "sha512-bpC7GYwiDYQ4wYLe+FA8lhRjhQCMcQGuSgGGqDkg/QerRWw9CmGRT0iSOVRSZJ29NMLZgIzqaljJ63oaL4NIJQ==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/possible-typed-array-names": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/possible-typed-array-names/-/possible-typed-array-names-1.1.0.tgz",
      "integrity": "sha512-/+5VFTchJDoVj3bhoqi6UeymcD00DAwb1nJwamzPvHEszJ4FpF6SNNbUbOS8yI56qHzdV8eK0qEfOSiodkTdxg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.8",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.8.tgz",
      "integrity": "sha512-OW/rX8O/jXnm82Ey1k44pObPtdblfiuWnrd8X7GJ7emImCOstunGbXUpp7HdBrFQX6rJzn3sPT397Wp5aCwCHg==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.11",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/postcss-attribute-case-insensitive": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/postcss-attribute-case-insensitive/-/postcss-attribute-case-insensitive-5.0.2.tgz",
      "integrity": "sha512-XIidXV8fDr0kKt28vqki84fRK8VW8eTuIa4PChv2MqKuT6C9UjmSKzen6KaWhWEoYvwxFCa7n/tC1SZ3tyq4SQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-browser-comments": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/postcss-browser-comments/-/postcss-browser-comments-4.0.0.tgz",
      "integrity": "sha512-X9X9/WN3KIvY9+hNERUqX9gncsgBA25XaeR+jshHz2j8+sYyHktHw1JdKuMjeLpGktXidqDhA7b/qm1mrBDmgg==",
      "license": "CC0-1.0",
      "engines": {
        "node": ">=8"
      },
      "peerDependencies": {
        "browserslist": ">=4",
        "postcss": ">=8"
      }
    },
    "node_modules/postcss-calc": {
      "version": "8.2.4",
      "resolved": "https://registry.npmjs.org/postcss-calc/-/postcss-calc-8.2.4.tgz",
      "integrity": "sha512-SmWMSJmB8MRnnULldx0lQIyhSNvuDl9HfrZkaqqE/WHAhToYsAvDq+yAsA/kIyINDszOp3Rh0GFoNuH5Ypsm3Q==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9",
        "postcss-value-parser": "^4.2.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.2"
      }
    },
    "node_modules/postcss-clamp": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/postcss-clamp/-/postcss-clamp-4.1.0.tgz",
      "integrity": "sha512-ry4b1Llo/9zz+PKC+030KUnPITTJAHeOwjfAyyB60eT0AorGLdzp52s31OsPRHRf8NchkgFoG2y6fCfn1IV1Ow==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": ">=7.6.0"
      },
      "peerDependencies": {
        "postcss": "^8.4.6"
      }
    },
    "node_modules/postcss-color-functional-notation": {
      "version": "4.2.4",
      "resolved": "https://registry.npmjs.org/postcss-color-functional-notation/-/postcss-color-functional-notation-4.2.4.tgz",
      "integrity": "sha512-2yrTAUZUab9s6CpxkxC4rVgFEVaR6/2Pipvi6qcgvnYiVqZcbDHEoBDhrXzyb7Efh2CCfHQNtcqWcIruDTIUeg==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-color-hex-alpha": {
      "version": "8.0.4",
      "resolved": "https://registry.npmjs.org/postcss-color-hex-alpha/-/postcss-color-hex-alpha-8.0.4.tgz",
      "integrity": "sha512-nLo2DCRC9eE4w2JmuKgVA3fGL3d01kGq752pVALF68qpGLmx2Qrk91QTKkdUqqp45T1K1XV8IhQpcu1hoAQflQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-color-rebeccapurple": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/postcss-color-rebeccapurple/-/postcss-color-rebeccapurple-7.1.1.tgz",
      "integrity": "sha512-pGxkuVEInwLHgkNxUc4sdg4g3py7zUeCQ9sMfwyHAT+Ezk8a4OaaVZ8lIY5+oNqA/BXXgLyXv0+5wHP68R79hg==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-colormin": {
      "version": "5.3.1",
      "resolved": "https://registry.npmjs.org/postcss-colormin/-/postcss-colormin-5.3.1.tgz",
      "integrity": "sha512-UsWQG0AqTFQmpBegeLLc1+c3jIqBNB0zlDGRWR+dQ3pRKJL1oeMzyqmH3o2PIfn9MBdNrVPWhDbT769LxCTLJQ==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "caniuse-api": "^3.0.0",
        "colord": "^2.9.1",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-convert-values": {
      "version": "5.1.3",
      "resolved": "https://registry.npmjs.org/postcss-convert-values/-/postcss-convert-values-5.1.3.tgz",
      "integrity": "sha512-82pC1xkJZtcJEfiLw6UXnXVXScgtBrjlO5CBmuDQc+dlb88ZYheFsjTn40+zBVi3DkfF7iezO0nJUPLcJK3pvA==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-custom-media": {
      "version": "8.0.2",
      "resolved": "https://registry.npmjs.org/postcss-custom-media/-/postcss-custom-media-8.0.2.tgz",
      "integrity": "sha512-7yi25vDAoHAkbhAzX9dHx2yc6ntS4jQvejrNcC+csQJAXjj15e7VcWfMgLqBNAbOvqi5uIa9huOVwdHbf+sKqg==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.3"
      }
    },
    "node_modules/postcss-custom-properties": {
      "version": "12.1.11",
      "resolved": "https://registry.npmjs.org/postcss-custom-properties/-/postcss-custom-properties-12.1.11.tgz",
      "integrity": "sha512-0IDJYhgU8xDv1KY6+VgUwuQkVtmYzRwu+dMjnmdMafXYv86SWqfxkc7qdDvWS38vsjaEtv8e0vGOUQrAiMBLpQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-custom-selectors": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/postcss-custom-selectors/-/postcss-custom-selectors-6.0.3.tgz",
      "integrity": "sha512-fgVkmyiWDwmD3JbpCmB45SvvlCD6z9CG6Ie6Iere22W5aHea6oWa7EM2bpnv2Fj3I94L3VbtvX9KqwSi5aFzSg==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.4"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.3"
      }
    },
    "node_modules/postcss-dir-pseudo-class": {
      "version": "6.0.5",
      "resolved": "https://registry.npmjs.org/postcss-dir-pseudo-class/-/postcss-dir-pseudo-class-6.0.5.tgz",
      "integrity": "sha512-eqn4m70P031PF7ZQIvSgy9RSJ5uI2171O/OO/zcRNYpJbvaeKFUlar1aJ7rmgiQtbm0FSPsRewjpdS0Oew7MPA==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-discard-comments": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/postcss-discard-comments/-/postcss-discard-comments-5.1.2.tgz",
      "integrity": "sha512-+L8208OVbHVF2UQf1iDmRcbdjJkuBF6IS29yBDSiWUIzpYaAhtNl6JYnYm12FnkeCwQqF5LeklOu6rAqgfBZqQ==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-discard-duplicates": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-discard-duplicates/-/postcss-discard-duplicates-5.1.0.tgz",
      "integrity": "sha512-zmX3IoSI2aoenxHV6C7plngHWWhUOV3sP1T8y2ifzxzbtnuhk1EdPwm0S1bIUNaJ2eNbWeGLEwzw8huPD67aQw==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-discard-empty": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-discard-empty/-/postcss-discard-empty-5.1.1.tgz",
      "integrity": "sha512-zPz4WljiSuLWsI0ir4Mcnr4qQQ5e1Ukc3i7UfE2XcrwKK2LIPIqE5jxMRxO6GbI3cv//ztXDsXwEWT3BHOGh3A==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-discard-overridden": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-discard-overridden/-/postcss-discard-overridden-5.1.0.tgz",
      "integrity": "sha512-21nOL7RqWR1kasIVdKs8HNqQJhFxLsyRfAnUDm4Fe4t4mCWL9OJiHvlHPjcd8zc5Myu89b/7wZDnOSjFgeWRtw==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-double-position-gradients": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/postcss-double-position-gradients/-/postcss-double-position-gradients-3.1.2.tgz",
      "integrity": "sha512-GX+FuE/uBR6eskOK+4vkXgT6pDkexLokPaz/AbJna9s5Kzp/yl488pKPjhy0obB475ovfT1Wv8ho7U/cHNaRgQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-env-function": {
      "version": "4.0.6",
      "resolved": "https://registry.npmjs.org/postcss-env-function/-/postcss-env-function-4.0.6.tgz",
      "integrity": "sha512-kpA6FsLra+NqcFnL81TnsU+Z7orGtDTxcOhl6pwXeEq1yFPpRMkCDpHhrz8CFQDr/Wfm0jLiNQ1OsGGPjlqPwA==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-flexbugs-fixes": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/postcss-flexbugs-fixes/-/postcss-flexbugs-fixes-5.0.2.tgz",
      "integrity": "sha512-18f9voByak7bTktR2QgDveglpn9DTbBWPUzSOe9g0N4WR/2eSt6Vrcbf0hmspvMI6YWGywz6B9f7jzpFNJJgnQ==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8.1.4"
      }
    },
    "node_modules/postcss-focus-visible": {
      "version": "6.0.4",
      "resolved": "https://registry.npmjs.org/postcss-focus-visible/-/postcss-focus-visible-6.0.4.tgz",
      "integrity": "sha512-QcKuUU/dgNsstIK6HELFRT5Y3lbrMLEOwG+A4s5cA+fx3A3y/JTq3X9LaOj3OC3ALH0XqyrgQIgey/MIZ8Wczw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-focus-within": {
      "version": "5.0.4",
      "resolved": "https://registry.npmjs.org/postcss-focus-within/-/postcss-focus-within-5.0.4.tgz",
      "integrity": "sha512-vvjDN++C0mu8jz4af5d52CB184ogg/sSxAFS+oUJQq2SuCe7T5U2iIsVJtsCp2d6R4j0jr5+q3rPkBVZkXD9fQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-font-variant": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/postcss-font-variant/-/postcss-font-variant-5.0.0.tgz",
      "integrity": "sha512-1fmkBaCALD72CK2a9i468mA/+tr9/1cBxRRMXOUaZqO43oWPR5imcyPjXwuv7PXbCid4ndlP5zWhidQVVa3hmA==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-gap-properties": {
      "version": "3.0.5",
      "resolved": "https://registry.npmjs.org/postcss-gap-properties/-/postcss-gap-properties-3.0.5.tgz",
      "integrity": "sha512-IuE6gKSdoUNcvkGIqdtjtcMtZIFyXZhmFd5RUlg97iVEvp1BZKV5ngsAjCjrVy+14uhGBQl9tzmi1Qwq4kqVOg==",
      "license": "CC0-1.0",
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-image-set-function": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/postcss-image-set-function/-/postcss-image-set-function-4.0.7.tgz",
      "integrity": "sha512-9T2r9rsvYzm5ndsBE8WgtrMlIT7VbtTfE7b3BQnudUqnBcBo7L758oc+o+pdj/dUV0l5wjwSdjeOH2DZtfv8qw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-import": {
      "version": "15.1.0",
      "resolved": "https://registry.npmjs.org/postcss-import/-/postcss-import-15.1.0.tgz",
      "integrity": "sha512-hpr+J05B2FVYUAXHeK1YyI267J/dDDhMU6B6civm8hSY1jYJnBXxzKDKDswzJmtLHryrjhnDjqqp/49t8FALew==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.0.0",
        "read-cache": "^1.0.0",
        "resolve": "^1.1.7"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "postcss": "^8.0.0"
      }
    },
    "node_modules/postcss-initial": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/postcss-initial/-/postcss-initial-4.0.1.tgz",
      "integrity": "sha512-0ueD7rPqX8Pn1xJIjay0AZeIuDoF+V+VvMt/uOnn+4ezUKhZM/NokDeP6DwMNyIoYByuN/94IQnt5FEkaN59xQ==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8.0.0"
      }
    },
    "node_modules/postcss-js": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/postcss-js/-/postcss-js-4.1.0.tgz",
      "integrity": "sha512-oIAOTqgIo7q2EOwbhb8UalYePMvYoIeRY2YKntdpFQXNosSu3vLrniGgmH9OKs/qAkfoj5oB3le/7mINW1LCfw==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "camelcase-css": "^2.0.1"
      },
      "engines": {
        "node": "^12 || ^14 || >= 16"
      },
      "peerDependencies": {
        "postcss": "^8.4.21"
      }
    },
    "node_modules/postcss-lab-function": {
      "version": "4.2.1",
      "resolved": "https://registry.npmjs.org/postcss-lab-function/-/postcss-lab-function-4.2.1.tgz",
      "integrity": "sha512-xuXll4isR03CrQsmxyz92LJB2xX9n+pZJ5jE9JgcnmsCammLyKdlzrBin+25dy6wIjfhJpKBAN80gsTlCgRk2w==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-loader": {
      "version": "6.2.1",
      "resolved": "https://registry.npmjs.org/postcss-loader/-/postcss-loader-6.2.1.tgz",
      "integrity": "sha512-WbbYpmAaKcux/P66bZ40bpWsBucjx/TTgVVzRZ9yUO8yQfVBlameJ0ZGVaPfH64hNSBh63a+ICP5nqOpBA0w+Q==",
      "license": "MIT",
      "dependencies": {
        "cosmiconfig": "^7.0.0",
        "klona": "^2.0.5",
        "semver": "^7.3.5"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "postcss": "^7.0.0 || ^8.0.1",
        "webpack": "^5.0.0"
      }
    },
    "node_modules/postcss-logical": {
      "version": "5.0.4",
      "resolved": "https://registry.npmjs.org/postcss-logical/-/postcss-logical-5.0.4.tgz",
      "integrity": "sha512-RHXxplCeLh9VjinvMrZONq7im4wjWGlRJAqmAVLXyZaXwfDWP73/oq4NdIp+OZwhQUMj0zjqDfM5Fj7qby+B4g==",
      "license": "CC0-1.0",
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-media-minmax": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/postcss-media-minmax/-/postcss-media-minmax-5.0.0.tgz",
      "integrity": "sha512-yDUvFf9QdFZTuCUg0g0uNSHVlJ5X1lSzDZjPSFaiCWvjgsvu8vEVxtahPrLMinIDEEGnx6cBe6iqdx5YWz08wQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10.0.0"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-merge-longhand": {
      "version": "5.1.7",
      "resolved": "https://registry.npmjs.org/postcss-merge-longhand/-/postcss-merge-longhand-5.1.7.tgz",
      "integrity": "sha512-YCI9gZB+PLNskrK0BB3/2OzPnGhPkBEwmwhfYk1ilBHYVAZB7/tkTHFBAnCrvBBOmeYyMYw3DMjT55SyxMBzjQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0",
        "stylehacks": "^5.1.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-merge-rules": {
      "version": "5.1.4",
      "resolved": "https://registry.npmjs.org/postcss-merge-rules/-/postcss-merge-rules-5.1.4.tgz",
      "integrity": "sha512-0R2IuYpgU93y9lhVbO/OylTtKMVcHb67zjWIfCiKR9rWL3GUk1677LAqD/BcHizukdZEjT8Ru3oHRoAYoJy44g==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "caniuse-api": "^3.0.0",
        "cssnano-utils": "^3.1.0",
        "postcss-selector-parser": "^6.0.5"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-minify-font-values": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-minify-font-values/-/postcss-minify-font-values-5.1.0.tgz",
      "integrity": "sha512-el3mYTgx13ZAPPirSVsHqFzl+BBBDrXvbySvPGFnQcTI4iNslrPaFq4muTkLZmKlGk4gyFAYUBMH30+HurREyA==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-minify-gradients": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-minify-gradients/-/postcss-minify-gradients-5.1.1.tgz",
      "integrity": "sha512-VGvXMTpCEo4qHTNSa9A0a3D+dxGFZCYwR6Jokk+/3oB6flu2/PnPXAh2x7x52EkY5xlIHLm+Le8tJxe/7TNhzw==",
      "license": "MIT",
      "dependencies": {
        "colord": "^2.9.1",
        "cssnano-utils": "^3.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-minify-params": {
      "version": "5.1.4",
      "resolved": "https://registry.npmjs.org/postcss-minify-params/-/postcss-minify-params-5.1.4.tgz",
      "integrity": "sha512-+mePA3MgdmVmv6g+30rn57USjOGSAyuxUmkfiWpzalZ8aiBkdPYjXWtHuwJGm1v5Ojy0Z0LaSYhHaLJQB0P8Jw==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "cssnano-utils": "^3.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-minify-selectors": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/postcss-minify-selectors/-/postcss-minify-selectors-5.2.1.tgz",
      "integrity": "sha512-nPJu7OjZJTsVUmPdm2TcaiohIwxP+v8ha9NehQ2ye9szv4orirRU3SDdtUmKH+10nzn0bAyOXZ0UEr7OpvLehg==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.5"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-modules-extract-imports": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/postcss-modules-extract-imports/-/postcss-modules-extract-imports-3.1.0.tgz",
      "integrity": "sha512-k3kNe0aNFQDAZGbin48pL2VNidTF0w4/eASDsxlyspobzU3wZQLOGj7L9gfRe0Jo9/4uud09DsjFNH7winGv8Q==",
      "license": "ISC",
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-modules-local-by-default": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/postcss-modules-local-by-default/-/postcss-modules-local-by-default-4.2.0.tgz",
      "integrity": "sha512-5kcJm/zk+GJDSfw+V/42fJ5fhjL5YbFDl8nVdXkJPLLW+Vf9mTD5Xe0wqIaDnLuL2U6cDNpTr+UQ+v2HWIBhzw==",
      "license": "MIT",
      "dependencies": {
        "icss-utils": "^5.0.0",
        "postcss-selector-parser": "^7.0.0",
        "postcss-value-parser": "^4.1.0"
      },
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-modules-local-by-default/node_modules/postcss-selector-parser": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-7.1.1.tgz",
      "integrity": "sha512-orRsuYpJVw8LdAwqqLykBj9ecS5/cRHlI5+nvTo8LcCKmzDmqVORXtOIYEEQuL9D4BxtA1lm5isAqzQZCoQ6Eg==",
      "license": "MIT",
      "dependencies": {
        "cssesc": "^3.0.0",
        "util-deprecate": "^1.0.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/postcss-modules-scope": {
      "version": "3.2.1",
      "resolved": "https://registry.npmjs.org/postcss-modules-scope/-/postcss-modules-scope-3.2.1.tgz",
      "integrity": "sha512-m9jZstCVaqGjTAuny8MdgE88scJnCiQSlSrOWcTQgM2t32UBe+MUmFSO5t7VMSfAf/FJKImAxBav8ooCHJXCJA==",
      "license": "ISC",
      "dependencies": {
        "postcss-selector-parser": "^7.0.0"
      },
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-modules-scope/node_modules/postcss-selector-parser": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-7.1.1.tgz",
      "integrity": "sha512-orRsuYpJVw8LdAwqqLykBj9ecS5/cRHlI5+nvTo8LcCKmzDmqVORXtOIYEEQuL9D4BxtA1lm5isAqzQZCoQ6Eg==",
      "license": "MIT",
      "dependencies": {
        "cssesc": "^3.0.0",
        "util-deprecate": "^1.0.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/postcss-modules-values": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/postcss-modules-values/-/postcss-modules-values-4.0.0.tgz",
      "integrity": "sha512-RDxHkAiEGI78gS2ofyvCsu7iycRv7oqw5xMWn9iMoR0N/7mf9D50ecQqUo5BZ9Zh2vH4bCUR/ktCqbB9m8vJjQ==",
      "license": "ISC",
      "dependencies": {
        "icss-utils": "^5.0.0"
      },
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-nested": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/postcss-nested/-/postcss-nested-6.2.0.tgz",
      "integrity": "sha512-HQbt28KulC5AJzG+cZtj9kvKB93CFCdLvog1WFLf1D+xmMvPGlBstkpTEZfK5+AN9hfJocyBFCNiqyS48bpgzQ==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.1.1"
      },
      "engines": {
        "node": ">=12.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.14"
      }
    },
    "node_modules/postcss-nesting": {
      "version": "10.2.0",
      "resolved": "https://registry.npmjs.org/postcss-nesting/-/postcss-nesting-10.2.0.tgz",
      "integrity": "sha512-EwMkYchxiDiKUhlJGzWsD9b2zvq/r2SSubcRrgP+jujMXFzqvANLt16lJANC+5uZ6hjI7lpRmI6O8JIl+8l1KA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/selector-specificity": "^2.0.0",
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-normalize": {
      "version": "10.0.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize/-/postcss-normalize-10.0.1.tgz",
      "integrity": "sha512-+5w18/rDev5mqERcG3W5GZNMJa1eoYYNGo8gB7tEwaos0ajk3ZXAI4mHGcNT47NE+ZnZD1pEpUOFLvltIwmeJA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/normalize.css": "*",
        "postcss-browser-comments": "^4",
        "sanitize.css": "*"
      },
      "engines": {
        "node": ">= 12"
      },
      "peerDependencies": {
        "browserslist": ">= 4",
        "postcss": ">= 8"
      }
    },
    "node_modules/postcss-normalize-charset": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-charset/-/postcss-normalize-charset-5.1.0.tgz",
      "integrity": "sha512-mSgUJ+pd/ldRGVx26p2wz9dNZ7ji6Pn8VWBajMXFf8jk7vUoSrZ2lt/wZR7DtlZYKesmZI680qjr2CeFF2fbUg==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-display-values": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-display-values/-/postcss-normalize-display-values-5.1.0.tgz",
      "integrity": "sha512-WP4KIM4o2dazQXWmFaqMmcvsKmhdINFblgSeRgn8BJ6vxaMyaJkwAzpPpuvSIoG/rmX3M+IrRZEz2H0glrQNEA==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-positions": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize-positions/-/postcss-normalize-positions-5.1.1.tgz",
      "integrity": "sha512-6UpCb0G4eofTCQLFVuI3EVNZzBNPiIKcA1AKVka+31fTVySphr3VUgAIULBhxZkKgwLImhzMR2Bw1ORK+37INg==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-repeat-style": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize-repeat-style/-/postcss-normalize-repeat-style-5.1.1.tgz",
      "integrity": "sha512-mFpLspGWkQtBcWIRFLmewo8aC3ImN2i/J3v8YCFUwDnPu3Xz4rLohDO26lGjwNsQxB3YF0KKRwspGzE2JEuS0g==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-string": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-string/-/postcss-normalize-string-5.1.0.tgz",
      "integrity": "sha512-oYiIJOf4T9T1N4i+abeIc7Vgm/xPCGih4bZz5Nm0/ARVJ7K6xrDlLwvwqOydvyL3RHNf8qZk6vo3aatiw/go3w==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-timing-functions": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-timing-functions/-/postcss-normalize-timing-functions-5.1.0.tgz",
      "integrity": "sha512-DOEkzJ4SAXv5xkHl0Wa9cZLF3WCBhF3o1SKVxKQAa+0pYKlueTpCgvkFAHfk+Y64ezX9+nITGrDZeVGgITJXjg==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-unicode": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize-unicode/-/postcss-normalize-unicode-5.1.1.tgz",
      "integrity": "sha512-qnCL5jzkNUmKVhZoENp1mJiGNPcsJCs1aaRmURmeJGES23Z/ajaln+EPTD+rBeNkSryI+2WTdW+lwcVdOikrpA==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-url": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-url/-/postcss-normalize-url-5.1.0.tgz",
      "integrity": "sha512-5upGeDO+PVthOxSmds43ZeMeZfKH+/DKgGRD7TElkkyS46JXAUhMzIKiCa7BabPeIy3AQcTkXwVVN7DbqsiCew==",
      "license": "MIT",
      "dependencies": {
        "normalize-url": "^6.0.1",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-whitespace": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize-whitespace/-/postcss-normalize-whitespace-5.1.1.tgz",
      "integrity": "sha512-83ZJ4t3NUDETIHTa3uEg6asWjSBYL5EdkVB0sDncx9ERzOKBVJIUeDO9RyA9Zwtig8El1d79HBp0JEi8wvGQnA==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-opacity-percentage": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/postcss-opacity-percentage/-/postcss-opacity-percentage-1.1.3.tgz",
      "integrity": "sha512-An6Ba4pHBiDtyVpSLymUUERMo2cU7s+Obz6BTrS+gxkbnSBNKSuD0AVUc+CpBMrpVPKKfoVz0WQCX+Tnst0i4A==",
      "funding": [
        {
          "type": "kofi",
          "url": "https://ko-fi.com/mrcgrtz"
        },
        {
          "type": "liberapay",
          "url": "https://liberapay.com/mrcgrtz"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-ordered-values": {
      "version": "5.1.3",
      "resolved": "https://registry.npmjs.org/postcss-ordered-values/-/postcss-ordered-values-5.1.3.tgz",
      "integrity": "sha512-9UO79VUhPwEkzbb3RNpqqghc6lcYej1aveQteWY+4POIwlqkYE21HKWaLDF6lWNuqCobEAyTovVhtI32Rbv2RQ==",
      "license": "MIT",
      "dependencies": {
        "cssnano-utils": "^3.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-overflow-shorthand": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/postcss-overflow-shorthand/-/postcss-overflow-shorthand-3.0.4.tgz",
      "integrity": "sha512-otYl/ylHK8Y9bcBnPLo3foYFLL6a6Ak+3EQBPOTR7luMYCOsiVTUk1iLvNf6tVPNGXcoL9Hoz37kpfriRIFb4A==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-page-break": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/postcss-page-break/-/postcss-page-break-3.0.4.tgz",
      "integrity": "sha512-1JGu8oCjVXLa9q9rFTo4MbeeA5FMe00/9C7lN4va606Rdb+HkxXtXsmEDrIraQ11fGz/WvKWa8gMuCKkrXpTsQ==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8"
      }
    },
    "node_modules/postcss-place": {
      "version": "7.0.5",
      "resolved": "https://registry.npmjs.org/postcss-place/-/postcss-place-7.0.5.tgz",
      "integrity": "sha512-wR8igaZROA6Z4pv0d+bvVrvGY4GVHihBCBQieXFY3kuSuMyOmEnnfFzHl/tQuqHZkfkIVBEbDvYcFfHmpSet9g==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-preset-env": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/postcss-preset-env/-/postcss-preset-env-7.8.3.tgz",
      "integrity": "sha512-T1LgRm5uEVFSEF83vHZJV2z19lHg4yJuZ6gXZZkqVsqv63nlr6zabMH3l4Pc01FQCyfWVrh2GaUeCVy9Po+Aag==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-cascade-layers": "^1.1.1",
        "@csstools/postcss-color-function": "^1.1.1",
        "@csstools/postcss-font-format-keywords": "^1.0.1",
        "@csstools/postcss-hwb-function": "^1.0.2",
        "@csstools/postcss-ic-unit": "^1.0.1",
        "@csstools/postcss-is-pseudo-class": "^2.0.7",
        "@csstools/postcss-nested-calc": "^1.0.0",
        "@csstools/postcss-normalize-display-values": "^1.0.1",
        "@csstools/postcss-oklab-function": "^1.1.1",
        "@csstools/postcss-progressive-custom-properties": "^1.3.0",
        "@csstools/postcss-stepped-value-functions": "^1.0.1",
        "@csstools/postcss-text-decoration-shorthand": "^1.0.0",
        "@csstools/postcss-trigonometric-functions": "^1.0.2",
        "@csstools/postcss-unset-value": "^1.0.2",
        "autoprefixer": "^10.4.13",
        "browserslist": "^4.21.4",
        "css-blank-pseudo": "^3.0.3",
        "css-has-pseudo": "^3.0.4",
        "css-prefers-color-scheme": "^6.0.3",
        "cssdb": "^7.1.0",
        "postcss-attribute-case-insensitive": "^5.0.2",
        "postcss-clamp": "^4.1.0",
        "postcss-color-functional-notation": "^4.2.4",
        "postcss-color-hex-alpha": "^8.0.4",
        "postcss-color-rebeccapurple": "^7.1.1",
        "postcss-custom-media": "^8.0.2",
        "postcss-custom-properties": "^12.1.10",
        "postcss-custom-selectors": "^6.0.3",
        "postcss-dir-pseudo-class": "^6.0.5",
        "postcss-double-position-gradients": "^3.1.2",
        "postcss-env-function": "^4.0.6",
        "postcss-focus-visible": "^6.0.4",
        "postcss-focus-within": "^5.0.4",
        "postcss-font-variant": "^5.0.0",
        "postcss-gap-properties": "^3.0.5",
        "postcss-image-set-function": "^4.0.7",
        "postcss-initial": "^4.0.1",
        "postcss-lab-function": "^4.2.1",
        "postcss-logical": "^5.0.4",
        "postcss-media-minmax": "^5.0.0",
        "postcss-nesting": "^10.2.0",
        "postcss-opacity-percentage": "^1.1.2",
        "postcss-overflow-shorthand": "^3.0.4",
        "postcss-page-break": "^3.0.4",
        "postcss-place": "^7.0.5",
        "postcss-pseudo-class-any-link": "^7.1.6",
        "postcss-replace-overflow-wrap": "^4.0.0",
        "postcss-selector-not": "^6.0.1",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-pseudo-class-any-link": {
      "version": "7.1.6",
      "resolved": "https://registry.npmjs.org/postcss-pseudo-class-any-link/-/postcss-pseudo-class-any-link-7.1.6.tgz",
      "integrity": "sha512-9sCtZkO6f/5ML9WcTLcIyV1yz9D1rf0tWc+ulKcvV30s0iZKS/ONyETvoWsr6vnrmW+X+KmuK3gV/w5EWnT37w==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-reduce-initial": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/postcss-reduce-initial/-/postcss-reduce-initial-5.1.2.tgz",
      "integrity": "sha512-dE/y2XRaqAi6OvjzD22pjTUQ8eOfc6m/natGHgKFBK9DxFmIm69YmaRVQrGgFlEfc1HePIurY0TmDeROK05rIg==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "caniuse-api": "^3.0.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-reduce-transforms": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-reduce-transforms/-/postcss-reduce-transforms-5.1.0.tgz",
      "integrity": "sha512-2fbdbmgir5AvpW9RLtdONx1QoYG2/EtqpNQbFASDlixBbAYuTcJ0dECwlqNqH7VbaUnEnh8SrxOe2sRIn24XyQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-replace-overflow-wrap": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/postcss-replace-overflow-wrap/-/postcss-replace-overflow-wrap-4.0.0.tgz",
      "integrity": "sha512-KmF7SBPphT4gPPcKZc7aDkweHiKEEO8cla/GjcBK+ckKxiZslIu3C4GCRW3DNfL0o7yW7kMQu9xlZ1kXRXLXtw==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8.0.3"
      }
    },
    "node_modules/postcss-selector-not": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/postcss-selector-not/-/postcss-selector-not-6.0.1.tgz",
      "integrity": "sha512-1i9affjAe9xu/y9uqWH+tD4r6/hDaXJruk8xn2x1vzxC2U3J3LKO3zJW4CyxlNhA56pADJ/djpEwpH1RClI2rQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-selector-parser": {
      "version": "6.1.2",
      "resolved": "https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-6.1.2.tgz",
      "integrity": "sha512-Q8qQfPiZ+THO/3ZrOrO0cJJKfpYCagtMUkXbnEfmgUjwXg6z/WBeOyS9APBBPCTSiDV+s4SwQGu8yFsiMRIudg==",
      "license": "MIT",
      "dependencies": {
        "cssesc": "^3.0.0",
        "util-deprecate": "^1.0.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/postcss-svgo": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-svgo/-/postcss-svgo-5.1.0.tgz",
      "integrity": "sha512-D75KsH1zm5ZrHyxPakAxJWtkyXew5qwS70v56exwvw542d9CRtTo78K0WeFxZB4G7JXKKMbEZtZayTGdIky/eA==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0",
        "svgo": "^2.7.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-svgo/node_modules/commander": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/commander/-/commander-7.2.0.tgz",
      "integrity": "sha512-QrWXB+ZQSVPmIWIhtEO9H+gwHaMGYiF5ChvoJ+K9ZGHG/sVsa6yiesAD1GC/x46sET00Xlwo1u49RVVVzvcSkw==",
      "license": "MIT",
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/postcss-svgo/node_modules/css-tree": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/css-tree/-/css-tree-1.1.3.tgz",
      "integrity": "sha512-tRpdppF7TRazZrjJ6v3stzv93qxRcSsFmW6cX0Zm2NVKpxE1WV1HblnghVv9TreireHkqI/VDEsfolRF1p6y7Q==",
      "license": "MIT",
      "dependencies": {
        "mdn-data": "2.0.14",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/postcss-svgo/node_modules/mdn-data": {
      "version": "2.0.14",
      "resolved": "https://registry.npmjs.org/mdn-data/-/mdn-data-2.0.14.tgz",
      "integrity": "sha512-dn6wd0uw5GsdswPFfsgMp5NSB0/aDe6fK94YJV/AJDYXL6HVLWBsxeq7js7Ad+mU2K9LAlwpk6kN2D5mwCPVow==",
      "license": "CC0-1.0"
    },
    "node_modules/postcss-svgo/node_modules/sax": {
      "version": "1.5.0",
      "resolved": "https://registry.npmjs.org/sax/-/sax-1.5.0.tgz",
      "integrity": "sha512-21IYA3Q5cQf089Z6tgaUTr7lDAyzoTPx5HRtbhsME8Udispad8dC/+sziTNugOEx54ilvatQ9YCzl4KQLPcRHA==",
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": ">=11.0.0"
      }
    },
    "node_modules/postcss-svgo/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/postcss-svgo/node_modules/svgo": {
      "version": "2.8.2",
      "resolved": "https://registry.npmjs.org/svgo/-/svgo-2.8.2.tgz",
      "integrity": "sha512-TyzE4NVGLUFy+H/Uy4N6c3G0HEeprsVfge6Lmq+0FdQQ/zqoVYB62IsBZORsiL+o96s6ff/V6/3UQo/C0cgCAA==",
      "license": "MIT",
      "dependencies": {
        "commander": "^7.2.0",
        "css-select": "^4.1.3",
        "css-tree": "^1.1.3",
        "csso": "^4.2.0",
        "picocolors": "^1.0.0",
        "sax": "^1.5.0",
        "stable": "^0.1.8"
      },
      "bin": {
        "svgo": "bin/svgo"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/postcss-unique-selectors": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-unique-selectors/-/postcss-unique-selectors-5.1.1.tgz",
      "integrity": "sha512-5JiODlELrz8L2HwxfPnhOWZYWDxVHWL83ufOv84NrcgipI7TaeRsatAhK4Tr2/ZiYldpK/wBvw5BD3qfaK96GA==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.5"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-value-parser": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/postcss-value-parser/-/postcss-value-parser-4.2.0.tgz",
      "integrity": "sha512-1NNCs6uurfkVbeXG4S8JFT9t19m45ICnif8zWLd5oPSZ50QnwMfK+H3jv408d4jw/7Bttv5axS5IiHoLaVNHeQ==",
      "license": "MIT"
    },
    "node_modules/prelude-ls": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/prelude-ls/-/prelude-ls-1.2.1.tgz",
      "integrity": "sha512-vkcDPrRZo1QZLbn5RLGPpg/WmIQ65qoWWhcGKf/b5eplkkarX0m9z8ppCat4mlOqUsWpyNuYgO3VRyrYHSzX5g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/pretty-bytes": {
      "version": "5.6.0",
      "resolved": "https://registry.npmjs.org/pretty-bytes/-/pretty-bytes-5.6.0.tgz",
      "integrity": "sha512-FFw039TmrBqFK8ma/7OL3sDz/VytdtJr044/QUJtH0wK9lb9jLq9tJyIxUwtQJHwar2BqtiA4iCWSwo9JLkzFg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/pretty-error": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/pretty-error/-/pretty-error-4.0.0.tgz",
      "integrity": "sha512-AoJ5YMAcXKYxKhuJGdcvse+Voc6v1RgnsR3nWcYU7q4t6z0Q6T86sv5Zq8VIRbOWWFpvdGE83LtdSMNd+6Y0xw==",
      "license": "MIT",
      "dependencies": {
        "lodash": "^4.17.20",
        "renderkid": "^3.0.0"
      }
    },
    "node_modules/pretty-format": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/pretty-format/-/pretty-format-27.5.1.tgz",
      "integrity": "sha512-Qb1gy5OrP5+zDf2Bvnzdl3jsTf1qXVMazbvCoKhtKqVs4/YK4ozX4gKQJJVyNe+cajNPn0KoC0MC3FUmaHWEmQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1",
        "ansi-styles": "^5.0.0",
        "react-is": "^17.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/pretty-format/node_modules/ansi-styles": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-5.2.0.tgz",
      "integrity": "sha512-Cxwpt2SfTzTtXcfOlzGEee8O+c+MmUgGrNiBcXnuWxuFJHe6a5Hz7qwhwe5OgaSYI0IJvkLqWX1ASG+cJOkEiA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/process-nextick-args": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/process-nextick-args/-/process-nextick-args-2.0.1.tgz",
      "integrity": "sha512-3ouUOpQhtgrbOa17J7+uxOTpITYWaGP7/AhoR3+A+/1e9skrzelGi/dXzEYyvbxubEF6Wn2ypscTKiKJFFn1ag==",
      "license": "MIT"
    },
    "node_modules/promise": {
      "version": "8.3.0",
      "resolved": "https://registry.npmjs.org/promise/-/promise-8.3.0.tgz",
      "integrity": "sha512-rZPNPKTOYVNEEKFaq1HqTgOwZD+4/YHS5ukLzQCypkj+OkYx7iv0mA91lJlpPPZ8vMau3IIGj5Qlwrx+8iiSmg==",
      "license": "MIT",
      "dependencies": {
        "asap": "~2.0.6"
      }
    },
    "node_modules/prompts": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/prompts/-/prompts-2.4.2.tgz",
      "integrity": "sha512-NxNv/kLguCA7p3jE8oL2aEBsrJWgAakBpgmgK6lpPWV+WuOmY6r2/zbAVnP+T8bQlA0nzHXSJSJW0Hq7ylaD2Q==",
      "license": "MIT",
      "dependencies": {
        "kleur": "^3.0.3",
        "sisteransi": "^1.0.5"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/prop-types": {
      "version": "15.8.1",
      "resolved": "https://registry.npmjs.org/prop-types/-/prop-types-15.8.1.tgz",
      "integrity": "sha512-oj87CgZICdulUohogVAR7AjlC0327U4el4L6eAvOqCeudMDVU0NThNaV+b9Df4dXgSP1gXMTnPdhfe/2qDH5cg==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.4.0",
        "object-assign": "^4.1.1",
        "react-is": "^16.13.1"
      }
    },
    "node_modules/prop-types/node_modules/react-is": {
      "version": "16.13.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-16.13.1.tgz",
      "integrity": "sha512-24e6ynE2H+OKt4kqsOvNd8kBpV65zoxbA4BVsEOB3ARVWQki/DHzaUoC5KuON/BiccDaCCTZBuOcfZs70kR8bQ==",
      "license": "MIT"
    },
    "node_modules/proxy-addr": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/proxy-addr/-/proxy-addr-2.0.7.tgz",
      "integrity": "sha512-llQsMLSUDUPT44jdrU/O37qlnifitDP+ZwrmmZcoSKyLKvtZxpyV0n2/bD/N4tBAAZ/gJEdZU7KMraoK1+XYAg==",
      "license": "MIT",
      "dependencies": {
        "forwarded": "0.2.0",
        "ipaddr.js": "1.9.1"
      },
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/proxy-addr/node_modules/ipaddr.js": {
      "version": "1.9.1",
      "resolved": "https://registry.npmjs.org/ipaddr.js/-/ipaddr.js-1.9.1.tgz",
      "integrity": "sha512-0KI/607xoxSToH7GjN1FfSbLoU0+btTicjsQSWQlh/hZykN8KpmMf7uYwPW3R+akZ6R/w18ZlXSHBYXiYUPO3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/psl": {
      "version": "1.15.0",
      "resolved": "https://registry.npmjs.org/psl/-/psl-1.15.0.tgz",
      "integrity": "sha512-JZd3gMVBAVQkSs6HdNZo9Sdo0LNcQeMNP3CozBJb3JYC/QUYZTnKxP+f8oWRX4rHP5EurWxqAHTSwUCjlNKa1w==",
      "license": "MIT",
      "dependencies": {
        "punycode": "^2.3.1"
      },
      "funding": {
        "url": "https://github.com/sponsors/lupomontero"
      }
    },
    "node_modules/punycode": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/punycode/-/punycode-2.3.1.tgz",
      "integrity": "sha512-vYt7UD1U9Wg6138shLtLOvdAu+8DsC/ilFtEVHcH+wydcSpNE20AfSOduf6MkRFahL5FY7X1oU7nKVZFtfq8Fg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/q": {
      "version": "1.5.1",
      "resolved": "https://registry.npmjs.org/q/-/q-1.5.1.tgz",
      "integrity": "sha512-kV/CThkXo6xyFEZUugw/+pIOywXcDbFYgSct5cT3gqlbkBE1SJdwy6UQoZvodiWF/ckQLZyDE/Bu1M6gVu5lVw==",
      "deprecated": "You or someone you depend on is using Q, the JavaScript Promise library that gave JavaScript developers strong feelings about promises. They can almost certainly migrate to the native JavaScript promise now. Thank you literally everyone for joining me in this bet against the odds. Be excellent to each other.\n\n(For a CapTP with native promises, see @endo/eventual-send and @endo/captp)",
      "license": "MIT",
      "engines": {
        "node": ">=0.6.0",
        "teleport": ">=0.2.0"
      }
    },
    "node_modules/qs": {
      "version": "6.14.2",
      "resolved": "https://registry.npmjs.org/qs/-/qs-6.14.2.tgz",
      "integrity": "sha512-V/yCWTTF7VJ9hIh18Ugr2zhJMP01MY7c5kh4J870L7imm6/DIzBsNLTXzMwUA3yZ5b/KBqLx8Kp3uRvd7xSe3Q==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">=0.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/querystringify": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/querystringify/-/querystringify-2.2.0.tgz",
      "integrity": "sha512-FIqgj2EUvTa7R50u0rGsyTftzjYmv/a3hO345bZNrqabNqjtgiDMgmo4mkUjd+nzU5oF3dClKqFIPUKybUyqoQ==",
      "license": "MIT"
    },
    "node_modules/queue-microtask": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/queue-microtask/-/queue-microtask-1.2.3.tgz",
      "integrity": "sha512-NuaNSa6flKT5JaSYQzJok04JzTL1CA6aGhv5rfLW3PgqA+M2ChpZQnAC8h8i4ZFkBS8X5RqkDBHA7r4hej3K9A==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT"
    },
    "node_modules/raf": {
      "version": "3.4.1",
      "resolved": "https://registry.npmjs.org/raf/-/raf-3.4.1.tgz",
      "integrity": "sha512-Sq4CW4QhwOHE8ucn6J34MqtZCeWFP2aQSmrlroYgqAV1PjStIhJXxYuTgUIfkEk7zTLjmIjLmU5q+fbD1NnOJA==",
      "license": "MIT",
      "dependencies": {
        "performance-now": "^2.1.0"
      }
    },
    "node_modules/randombytes": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/randombytes/-/randombytes-2.1.0.tgz",
      "integrity": "sha512-vYl3iOX+4CKUWuxGi9Ukhie6fsqXqS9FE2Zaic4tNFD2N2QQaXOMFbuKK4QmDHC0JO6B1Zp41J0LpT0oR68amQ==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "^5.1.0"
      }
    },
    "node_modules/range-parser": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/range-parser/-/range-parser-1.2.1.tgz",
      "integrity": "sha512-Hrgsx+orqoygnmhFbKaHE6c296J+HTAQXoxEF6gNupROmmGJRoyzfG3ccAveqCBrwr/2yxQ5BVd/GTl5agOwSg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/raw-body": {
      "version": "2.5.3",
      "resolved": "https://registry.npmjs.org/raw-body/-/raw-body-2.5.3.tgz",
      "integrity": "sha512-s4VSOf6yN0rvbRZGxs8Om5CWj6seneMwK3oDb4lWDH0UPhWcxwOWw5+qk24bxq87szX1ydrwylIOp2uG1ojUpA==",
      "license": "MIT",
      "dependencies": {
        "bytes": "~3.1.2",
        "http-errors": "~2.0.1",
        "iconv-lite": "~0.4.24",
        "unpipe": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/raw-body/node_modules/iconv-lite": {
      "version": "0.4.24",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.4.24.tgz",
      "integrity": "sha512-v3MXnZAcvnywkTUEZomIActle7RXXeedOR31wwl7VlyoXO4Qi9arvSenNQWne1TcRwhCL1HwLI21bEqdpj8/rA==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react/-/react-18.3.1.tgz",
      "integrity": "sha512-wS+hAgJShR0KhEvPJArfuPVN1+Hz1t0Y6n5jLrGQbkb4urgPE/0Rve+1kMB1v/oWgHgm4WIcV+i7F2pTVj+2iQ==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-app-polyfill": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/react-app-polyfill/-/react-app-polyfill-3.0.0.tgz",
      "integrity": "sha512-sZ41cxiU5llIB003yxxQBYrARBqe0repqPTTYBTmMqTz9szeBbE37BehCE891NZsmdZqqP+xWKdT3eo3vOzN8w==",
      "license": "MIT",
      "dependencies": {
        "core-js": "^3.19.2",
        "object-assign": "^4.1.1",
        "promise": "^8.1.0",
        "raf": "^3.4.1",
        "regenerator-runtime": "^0.13.9",
        "whatwg-fetch": "^3.6.2"
      },
      "engines": {
        "node": ">=14"
      }
    },
    "node_modules/react-dev-utils": {
      "version": "12.0.1",
      "resolved": "https://registry.npmjs.org/react-dev-utils/-/react-dev-utils-12.0.1.tgz",
      "integrity": "sha512-84Ivxmr17KjUupyqzFode6xKhjwuEJDROWKJy/BthkL7Wn6NJ8h4WE6k/exAv6ImS+0oZLRRW5j/aINMHyeGeQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.16.0",
        "address": "^1.1.2",
        "browserslist": "^4.18.1",
        "chalk": "^4.1.2",
        "cross-spawn": "^7.0.3",
        "detect-port-alt": "^1.1.6",
        "escape-string-regexp": "^4.0.0",
        "filesize": "^8.0.6",
        "find-up": "^5.0.0",
        "fork-ts-checker-webpack-plugin": "^6.5.0",
        "global-modules": "^2.0.0",
        "globby": "^11.0.4",
        "gzip-size": "^6.0.0",
        "immer": "^9.0.7",
        "is-root": "^2.1.0",
        "loader-utils": "^3.2.0",
        "open": "^8.4.0",
        "pkg-up": "^3.1.0",
        "prompts": "^2.4.2",
        "react-error-overlay": "^6.0.11",
        "recursive-readdir": "^2.2.2",
        "shell-quote": "^1.7.3",
        "strip-ansi": "^6.0.1",
        "text-table": "^0.2.0"
      },
      "engines": {
        "node": ">=14"
      }
    },
    "node_modules/react-dev-utils/node_modules/find-up": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-5.0.0.tgz",
      "integrity": "sha512-78/PXT1wlLLDgTzDs7sjq9hzz0vXD+zn+7wypEe4fXQxCmdmqfGsEPQxmiCSQI3ajFV91bVSsvNtrJRiW6nGng==",
      "license": "MIT",
      "dependencies": {
        "locate-path": "^6.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/react-dev-utils/node_modules/loader-utils": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/loader-utils/-/loader-utils-3.3.1.tgz",
      "integrity": "sha512-FMJTLMXfCLMLfJxcX9PFqX5qD88Z5MRGaZCVzfuqeZSPsyiBzs+pahDQjbIWz2QIzPZz0NX9Zy4FX3lmK6YHIg==",
      "license": "MIT",
      "engines": {
        "node": ">= 12.13.0"
      }
    },
    "node_modules/react-dev-utils/node_modules/locate-path": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-6.0.0.tgz",
      "integrity": "sha512-iPZK6eYjbxRu3uB4/WZ3EsEIMJFMqAoopl3R+zuq0UjcAm/MO6KCweDgPfP3elTztoKP3KtnVHxTn2NHBSDVUw==",
      "license": "MIT",
      "dependencies": {
        "p-locate": "^5.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/react-dev-utils/node_modules/p-limit": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-3.1.0.tgz",
      "integrity": "sha512-TYOanM3wGwNGsZN2cVTYPArw454xnXj5qmWF1bEoAc4+cU/ol7GVh7odevjp1FNHduHc3KZMcFduxU5Xc6uJRQ==",
      "license": "MIT",
      "dependencies": {
        "yocto-queue": "^0.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/react-dev-utils/node_modules/p-locate": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-5.0.0.tgz",
      "integrity": "sha512-LaNjtRWUBY++zB5nE/NwcaoMylSPk+S+ZHNB1TzdbMJMny6dynpAGt7X/tl/QYq3TIeE6nxHppbo2LGymrG5Pw==",
      "license": "MIT",
      "dependencies": {
        "p-limit": "^3.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/react-dom": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-18.3.1.tgz",
      "integrity": "sha512-5m4nQKp+rZRb09LNH59GM4BxTh9251/ylbKIbpe7TpGxfJ+9kv6BLkLBXIjjspbgbnIBNqlI23tRnTWT0snUIw==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0",
        "scheduler": "^0.23.2"
      },
      "peerDependencies": {
        "react": "^18.3.1"
      }
    },
    "node_modules/react-error-overlay": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/react-error-overlay/-/react-error-overlay-6.1.0.tgz",
      "integrity": "sha512-SN/U6Ytxf1QGkw/9ve5Y+NxBbZM6Ht95tuXNMKs8EJyFa/Vy/+Co3stop3KBHARfn/giv+Lj1uUnTfOJ3moFEQ==",
      "license": "MIT"
    },
    "node_modules/react-is": {
      "version": "17.0.2",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-17.0.2.tgz",
      "integrity": "sha512-w2GsyukL62IJnlaff/nRegPQR94C/XXamvMWmSHRJ4y7Ts/4ocGRmTHvOs8PSE6pB3dWOrD/nueuU5sduBsQ4w==",
      "license": "MIT"
    },
    "node_modules/react-refresh": {
      "version": "0.11.0",
      "resolved": "https://registry.npmjs.org/react-refresh/-/react-refresh-0.11.0.tgz",
      "integrity": "sha512-F27qZr8uUqwhWZboondsPx8tnC3Ct3SxZA3V5WyEvujRyyNv0VYPhoBg1gZ8/MV5tubQp76Trw8lTv9hzRBa+A==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-scripts": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/react-scripts/-/react-scripts-5.0.1.tgz",
      "integrity": "sha512-8VAmEm/ZAwQzJ+GOMLbBsTdDKOpuZh7RPs0UymvBR2vRk4iZWCskjbFnxqjrzoIvlNNRZ3QJFx6/qDSi6zSnaQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.16.0",
        "@pmmmwh/react-refresh-webpack-plugin": "^0.5.3",
        "@svgr/webpack": "^5.5.0",
        "babel-jest": "^27.4.2",
        "babel-loader": "^8.2.3",
        "babel-plugin-named-asset-import": "^0.3.8",
        "babel-preset-react-app": "^10.0.1",
        "bfj": "^7.0.2",
        "browserslist": "^4.18.1",
        "camelcase": "^6.2.1",
        "case-sensitive-paths-webpack-plugin": "^2.4.0",
        "css-loader": "^6.5.1",
        "css-minimizer-webpack-plugin": "^3.2.0",
        "dotenv": "^10.0.0",
        "dotenv-expand": "^5.1.0",
        "eslint": "^8.3.0",
        "eslint-config-react-app": "^7.0.1",
        "eslint-webpack-plugin": "^3.1.1",
        "file-loader": "^6.2.0",
        "fs-extra": "^10.0.0",
        "html-webpack-plugin": "^5.5.0",
        "identity-obj-proxy": "^3.0.0",
        "jest": "^27.4.3",
        "jest-resolve": "^27.4.2",
        "jest-watch-typeahead": "^1.0.0",
        "mini-css-extract-plugin": "^2.4.5",
        "postcss": "^8.4.4",
        "postcss-flexbugs-fixes": "^5.0.2",
        "postcss-loader": "^6.2.1",
        "postcss-normalize": "^10.0.1",
        "postcss-preset-env": "^7.0.1",
        "prompts": "^2.4.2",
        "react-app-polyfill": "^3.0.0",
        "react-dev-utils": "^12.0.1",
        "react-refresh": "^0.11.0",
        "resolve": "^1.20.0",
        "resolve-url-loader": "^4.0.0",
        "sass-loader": "^12.3.0",
        "semver": "^7.3.5",
        "source-map-loader": "^3.0.0",
        "style-loader": "^3.3.1",
        "tailwindcss": "^3.0.2",
        "terser-webpack-plugin": "^5.2.5",
        "webpack": "^5.64.4",
        "webpack-dev-server": "^4.6.0",
        "webpack-manifest-plugin": "^4.0.2",
        "workbox-webpack-plugin": "^6.4.1"
      },
      "bin": {
        "react-scripts": "bin/react-scripts.js"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "optionalDependencies": {
        "fsevents": "^2.3.2"
      },
      "peerDependencies": {
        "react": ">= 16",
        "typescript": "^3.2.1 || ^4"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/read-cache": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/read-cache/-/read-cache-1.0.0.tgz",
      "integrity": "sha512-Owdv/Ft7IjOgm/i0xvNDZ1LrRANRfew4b2prF3OWMQLxLfu3bS8FVhCsrSCMK4lR56Y9ya+AThoTpDCTxCmpRA==",
      "license": "MIT",
      "dependencies": {
        "pify": "^2.3.0"
      }
    },
    "node_modules/readable-stream": {
      "version": "3.6.2",
      "resolved": "https://registry.npmjs.org/readable-stream/-/readable-stream-3.6.2.tgz",
      "integrity": "sha512-9u/sniCrY3D5WdsERHzHE4G2YCXqoG5FTHUiCC4SIbr6XcLZBY05ya9EKjYek9O5xOAwjGq+1JdGBAS7Q9ScoA==",
      "license": "MIT",
      "dependencies": {
        "inherits": "^2.0.3",
        "string_decoder": "^1.1.1",
        "util-deprecate": "^1.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/readdirp": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/readdirp/-/readdirp-3.6.0.tgz",
      "integrity": "sha512-hOS089on8RduqdbhvQ5Z37A0ESjsqz6qnRcffsMU3495FuTdqSm+7bhJ29JvIOsBDEEnan5DPu9t3To9VRlMzA==",
      "license": "MIT",
      "dependencies": {
        "picomatch": "^2.2.1"
      },
      "engines": {
        "node": ">=8.10.0"
      }
    },
    "node_modules/recursive-readdir": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/recursive-readdir/-/recursive-readdir-2.2.3.tgz",
      "integrity": "sha512-8HrF5ZsXk5FAH9dgsx3BlUer73nIhuj+9OrQwEbLTPOBzGkL1lsFCR01am+v+0m2Cmbs1nP12hLDl5FA7EszKA==",
      "license": "MIT",
      "dependencies": {
        "minimatch": "^3.0.5"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/reflect.getprototypeof": {
      "version": "1.0.10",
      "resolved": "https://registry.npmjs.org/reflect.getprototypeof/-/reflect.getprototypeof-1.0.10.tgz",
      "integrity": "sha512-00o4I+DVrefhv+nX0ulyi3biSHCPDe+yLv5o/p6d/UVlirijB8E16FtfwSAi4g3tcqrQ4lRAqQSoFEZJehYEcw==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.7",
        "get-proto": "^1.0.1",
        "which-builtin-type": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/regenerate": {
      "version": "1.4.2",
      "resolved": "https://registry.npmjs.org/regenerate/-/regenerate-1.4.2.tgz",
      "integrity": "sha512-zrceR/XhGYU/d/opr2EKO7aRHUeiBI8qjtfHqADTwZd6Szfy16la6kqD0MIUs5z5hx6AaKa+PixpPrR289+I0A==",
      "license": "MIT"
    },
    "node_modules/regenerate-unicode-properties": {
      "version": "10.2.2",
      "resolved": "https://registry.npmjs.org/regenerate-unicode-properties/-/regenerate-unicode-properties-10.2.2.tgz",
      "integrity": "sha512-m03P+zhBeQd1RGnYxrGyDAPpWX/epKirLrp8e3qevZdVkKtnCrjjWczIbYc8+xd6vcTStVlqfycTx1KR4LOr0g==",
      "license": "MIT",
      "dependencies": {
        "regenerate": "^1.4.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/regenerator-runtime": {
      "version": "0.13.11",
      "resolved": "https://registry.npmjs.org/regenerator-runtime/-/regenerator-runtime-0.13.11.tgz",
      "integrity": "sha512-kY1AZVr2Ra+t+piVaJ4gxaFaReZVH40AKNo7UCX6W+dEwBo/2oZJzqfuN1qLq1oL45o56cPaTXELwrTh8Fpggg==",
      "license": "MIT"
    },
    "node_modules/regex-parser": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/regex-parser/-/regex-parser-2.3.1.tgz",
      "integrity": "sha512-yXLRqatcCuKtVHsWrNg0JL3l1zGfdXeEvDa0bdu4tCDQw0RpMDZsqbkyRTUnKMR0tXF627V2oEWjBEaEdqTwtQ==",
      "license": "MIT"
    },
    "node_modules/regexp.prototype.flags": {
      "version": "1.5.4",
      "resolved": "https://registry.npmjs.org/regexp.prototype.flags/-/regexp.prototype.flags-1.5.4.tgz",
      "integrity": "sha512-dYqgNSZbDwkaJ2ceRd9ojCGjBq+mOm9LmtXnAnEGyHhN/5R7iDW2TRw3h+o/jCFxus3P2LfWIIiwowAjANm7IA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-errors": "^1.3.0",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "set-function-name": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/regexpu-core": {
      "version": "6.4.0",
      "resolved": "https://registry.npmjs.org/regexpu-core/-/regexpu-core-6.4.0.tgz",
      "integrity": "sha512-0ghuzq67LI9bLXpOX/ISfve/Mq33a4aFRzoQYhnnok1JOFpmE/A2TBGkNVenOGEeSBCjIiWcc6MVOG5HEQv0sA==",
      "license": "MIT",
      "dependencies": {
        "regenerate": "^1.4.2",
        "regenerate-unicode-properties": "^10.2.2",
        "regjsgen": "^0.8.0",
        "regjsparser": "^0.13.0",
        "unicode-match-property-ecmascript": "^2.0.0",
        "unicode-match-property-value-ecmascript": "^2.2.1"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/regjsgen": {
      "version": "0.8.0",
      "resolved": "https://registry.npmjs.org/regjsgen/-/regjsgen-0.8.0.tgz",
      "integrity": "sha512-RvwtGe3d7LvWiDQXeQw8p5asZUmfU1G/l6WbUXeHta7Y2PEIvBTwH6E2EfmYUK8pxcxEdEmaomqyp0vZZ7C+3Q==",
      "license": "MIT"
    },
    "node_modules/regjsparser": {
      "version": "0.13.0",
      "resolved": "https://registry.npmjs.org/regjsparser/-/regjsparser-0.13.0.tgz",
      "integrity": "sha512-NZQZdC5wOE/H3UT28fVGL+ikOZcEzfMGk/c3iN9UGxzWHMa1op7274oyiUVrAG4B2EuFhus8SvkaYnhvW92p9Q==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "jsesc": "~3.1.0"
      },
      "bin": {
        "regjsparser": "bin/parser"
      }
    },
    "node_modules/relateurl": {
      "version": "0.2.7",
      "resolved": "https://registry.npmjs.org/relateurl/-/relateurl-0.2.7.tgz",
      "integrity": "sha512-G08Dxvm4iDN3MLM0EsP62EDV9IuhXPR6blNz6Utcp7zyV3tr4HVNINt6MpaRWbxoOHT3Q7YN2P+jaHX8vUbgog==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/renderkid": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/renderkid/-/renderkid-3.0.0.tgz",
      "integrity": "sha512-q/7VIQA8lmM1hF+jn+sFSPWGlMkSAeNYcPLmDQx2zzuiDfaLrOmumR8iaUKlenFgh0XRPIUeSPlH3A+AW3Z5pg==",
      "license": "MIT",
      "dependencies": {
        "css-select": "^4.1.3",
        "dom-converter": "^0.2.0",
        "htmlparser2": "^6.1.0",
        "lodash": "^4.17.21",
        "strip-ansi": "^6.0.1"
      }
    },
    "node_modules/require-directory": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/require-directory/-/require-directory-2.1.1.tgz",
      "integrity": "sha512-fGxEI7+wsG9xrvdjsrlmL22OMTTiHRwAMroiEeMgq8gzoLC/PQr7RsRDSTLUg/bZAZtF+TVIkHc6/4RIKrui+Q==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/require-from-string": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/require-from-string/-/require-from-string-2.0.2.tgz",
      "integrity": "sha512-Xf0nWe6RseziFMu+Ap9biiUbmplq6S9/p+7w7YXP/JBHhrUDDUhwa+vANyubuqfZWTveU//DYVGsDG7RKL/vEw==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/requires-port": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/requires-port/-/requires-port-1.0.0.tgz",
      "integrity": "sha512-KigOCHcocU3XODJxsu8i/j8T9tzT4adHiecwORRQ0ZZFcp7ahwXuRU1m+yuO90C5ZUyGeGfocHDI14M3L3yDAQ==",
      "license": "MIT"
    },
    "node_modules/resolve": {
      "version": "1.22.11",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-1.22.11.tgz",
      "integrity": "sha512-RfqAvLnMl313r7c9oclB1HhUEAezcpLjz95wFH4LVuhk9JF/r22qmVP9AMmOU4vMX7Q8pN8jwNg/CSpdFnMjTQ==",
      "license": "MIT",
      "dependencies": {
        "is-core-module": "^2.16.1",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/resolve-cwd": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/resolve-cwd/-/resolve-cwd-3.0.0.tgz",
      "integrity": "sha512-OrZaX2Mb+rJCpH/6CpSqt9xFVpN++x01XnN2ie9g6P5/3xelLAkXWVADpdz1IHD/KFfEXyE6V0U01OQ3UO2rEg==",
      "license": "MIT",
      "dependencies": {
        "resolve-from": "^5.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/resolve-from": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/resolve-from/-/resolve-from-5.0.0.tgz",
      "integrity": "sha512-qYg9KP24dD5qka9J47d0aVky0N+b4fTU89LN9iDnjB5waksiC49rvMB0PrUJQGoTmH50XPiqOvAjDfaijGxYZw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/resolve-url-loader": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/resolve-url-loader/-/resolve-url-loader-4.0.0.tgz",
      "integrity": "sha512-05VEMczVREcbtT7Bz+C+96eUO5HDNvdthIiMB34t7FcF8ehcu4wC0sSgPUubs3XW2Q3CNLJk/BJrCU9wVRymiA==",
      "license": "MIT",
      "dependencies": {
        "adjust-sourcemap-loader": "^4.0.0",
        "convert-source-map": "^1.7.0",
        "loader-utils": "^2.0.0",
        "postcss": "^7.0.35",
        "source-map": "0.6.1"
      },
      "engines": {
        "node": ">=8.9"
      },
      "peerDependencies": {
        "rework": "1.0.1",
        "rework-visit": "1.0.0"
      },
      "peerDependenciesMeta": {
        "rework": {
          "optional": true
        },
        "rework-visit": {
          "optional": true
        }
      }
    },
    "node_modules/resolve-url-loader/node_modules/convert-source-map": {
      "version": "1.9.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-1.9.0.tgz",
      "integrity": "sha512-ASFBup0Mz1uyiIjANan1jzLQami9z1PoYSZCiiYW2FczPbenXc45FZdBZLzOT+r6+iciuEModtmCti+hjaAk0A==",
      "license": "MIT"
    },
    "node_modules/resolve-url-loader/node_modules/picocolors": {
      "version": "0.2.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-0.2.1.tgz",
      "integrity": "sha512-cMlDqaLEqfSaW8Z7N5Jw+lyIW869EzT73/F5lhtY9cLGoVxSXznfgfXMO0Z5K0o0Q2TkTXq+0KFsdnSe3jDViA==",
      "license": "ISC"
    },
    "node_modules/resolve-url-loader/node_modules/postcss": {
      "version": "7.0.39",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-7.0.39.tgz",
      "integrity": "sha512-yioayjNbHn6z1/Bywyb2Y4s3yvDAeXGOyxqD+LnVOinq6Mdmd++SW2wUNVzavyyHxd6+DxzWGIuosg6P1Rj8uA==",
      "license": "MIT",
      "dependencies": {
        "picocolors": "^0.2.1",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=6.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/postcss/"
      }
    },
    "node_modules/resolve-url-loader/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/resolve.exports": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/resolve.exports/-/resolve.exports-1.1.1.tgz",
      "integrity": "sha512-/NtpHNDN7jWhAaQ9BvBUYZ6YTXsRBgfqWFWP7BZBaoMJO/I3G5OFzvTuWNlZC3aPjins1F+TNrLKsGbH4rfsRQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/retry": {
      "version": "0.13.1",
      "resolved": "https://registry.npmjs.org/retry/-/retry-0.13.1.tgz",
      "integrity": "sha512-XQBQ3I8W1Cge0Seh+6gjj03LbmRFWuoszgK9ooCpwYIrhhoO80pfq4cUkU5DkknwfOfFteRwlZ56PYOGYyFWdg==",
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/reusify": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/reusify/-/reusify-1.1.0.tgz",
      "integrity": "sha512-g6QUff04oZpHs0eG5p83rFLhHeV00ug/Yf9nZM6fLeUrPguBTkTQOdpAWWspMh55TZfVQDPaN3NQJfbVRAxdIw==",
      "license": "MIT",
      "engines": {
        "iojs": ">=1.0.0",
        "node": ">=0.10.0"
      }
    },
    "node_modules/rimraf": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/rimraf/-/rimraf-3.0.2.tgz",
      "integrity": "sha512-JZkJMZkAGFFPP2YqXZXPbMlMBgsxzE8ILs4lMIX/2o0L9UBw9O/Y3o6wFw/i9YLapcUJWwqbi3kdxIPdC62TIA==",
      "deprecated": "Rimraf versions prior to v4 are no longer supported",
      "license": "ISC",
      "dependencies": {
        "glob": "^7.1.3"
      },
      "bin": {
        "rimraf": "bin.js"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/rollup": {
      "version": "2.80.0",
      "resolved": "https://registry.npmjs.org/rollup/-/rollup-2.80.0.tgz",
      "integrity": "sha512-cIFJOD1DESzpjOBl763Kp1AH7UE/0fcdHe6rZXUdQ9c50uvgigvW97u3IcSeBwOkgqL/PXPBktBCh0KEu5L8XQ==",
      "license": "MIT",
      "bin": {
        "rollup": "dist/bin/rollup"
      },
      "engines": {
        "node": ">=10.0.0"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/rollup-plugin-terser": {
      "version": "7.0.2",
      "resolved": "https://registry.npmjs.org/rollup-plugin-terser/-/rollup-plugin-terser-7.0.2.tgz",
      "integrity": "sha512-w3iIaU4OxcF52UUXiZNsNeuXIMDvFrr+ZXK6bFZ0Q60qyVfq4uLptoS4bbq3paG3x216eQllFZX7zt6TIImguQ==",
      "deprecated": "This package has been deprecated and is no longer maintained. Please use @rollup/plugin-terser",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.10.4",
        "jest-worker": "^26.2.1",
        "serialize-javascript": "^4.0.0",
        "terser": "^5.0.0"
      },
      "peerDependencies": {
        "rollup": "^2.0.0"
      }
    },
    "node_modules/rollup-plugin-terser/node_modules/jest-worker": {
      "version": "26.6.2",
      "resolved": "https://registry.npmjs.org/jest-worker/-/jest-worker-26.6.2.tgz",
      "integrity": "sha512-KWYVV1c4i+jbMpaBC+U++4Va0cp8OisU185o73T1vo99hqi7w8tSJfUXYswwqqrjzwxa6KpRK54WhPvwf5w6PQ==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "merge-stream": "^2.0.0",
        "supports-color": "^7.0.0"
      },
      "engines": {
        "node": ">= 10.13.0"
      }
    },
    "node_modules/rollup-plugin-terser/node_modules/serialize-javascript": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/serialize-javascript/-/serialize-javascript-4.0.0.tgz",
      "integrity": "sha512-GaNA54380uFefWghODBWEGisLZFj00nS5ACs6yHa9nLqlLpVLO8ChDGeKRjZnV4Nh4n0Qi7nhYZD/9fCPzEqkw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "randombytes": "^2.1.0"
      }
    },
    "node_modules/run-parallel": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/run-parallel/-/run-parallel-1.2.0.tgz",
      "integrity": "sha512-5l4VyZR86LZ/lDxZTR6jqL8AFE2S0IFLMP26AbjsLVADxHdhB/c0GUsH+y39UfCi3dzz8OlQuPmnaJOMoDHQBA==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "queue-microtask": "^1.2.2"
      }
    },
    "node_modules/safe-array-concat": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/safe-array-concat/-/safe-array-concat-1.1.3.tgz",
      "integrity": "sha512-AURm5f0jYEOydBj7VQlVvDrjeFgthDdEF5H1dP+6mNpoXOMo1quQqJ4wvJDyRZ9+pO3kGWoOdmV08cSv2aJV6Q==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "get-intrinsic": "^1.2.6",
        "has-symbols": "^1.1.0",
        "isarray": "^2.0.5"
      },
      "engines": {
        "node": ">=0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safe-buffer": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/safe-buffer/-/safe-buffer-5.2.1.tgz",
      "integrity": "sha512-rp3So07KcdmmKbGvgaNxQSJr7bGVSVk5S9Eq1F+ppbRo70+YeaDxkw5Dd8NPN+GD6bjnYm2VuPuCXmpuYvmCXQ==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT"
    },
    "node_modules/safe-push-apply": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/safe-push-apply/-/safe-push-apply-1.0.0.tgz",
      "integrity": "sha512-iKE9w/Z7xCzUMIZqdBsp6pEQvwuEebH4vdpjcDWnyzaI6yl6O9FHvVpmGelvEHNsoY6wGblkxR6Zty/h00WiSA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "isarray": "^2.0.5"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safe-regex-test": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/safe-regex-test/-/safe-regex-test-1.1.0.tgz",
      "integrity": "sha512-x/+Cz4YrimQxQccJf5mKEbIa1NzeCRNI5Ecl/ekmlYaampdNLPalVyIcCZNNH3MvmqBugV5TMYZXv0ljslUlaw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "is-regex": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safer-buffer": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/safer-buffer/-/safer-buffer-2.1.2.tgz",
      "integrity": "sha512-YZo3K82SD7Riyi0E1EQPojLz7kpepnSQI9IyPbHHg1XXXevb5dJI7tpyN2ADxGcQbHG7vcyRHk0cbwqcQriUtg==",
      "license": "MIT"
    },
    "node_modules/sanitize.css": {
      "version": "13.0.0",
      "resolved": "https://registry.npmjs.org/sanitize.css/-/sanitize.css-13.0.0.tgz",
      "integrity": "sha512-ZRwKbh/eQ6w9vmTjkuG0Ioi3HBwPFce0O+v//ve+aOq1oeCy7jMV2qzzAlpsNuqpqCBjjriM1lbtZbF/Q8jVyA==",
      "license": "CC0-1.0"
    },
    "node_modules/sass-loader": {
      "version": "12.6.0",
      "resolved": "https://registry.npmjs.org/sass-loader/-/sass-loader-12.6.0.tgz",
      "integrity": "sha512-oLTaH0YCtX4cfnJZxKSLAyglED0naiYfNG1iXfU5w1LNZ+ukoA5DtyDIN5zmKVZwYNJP4KRc5Y3hkWga+7tYfA==",
      "license": "MIT",
      "dependencies": {
        "klona": "^2.0.4",
        "neo-async": "^2.6.2"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "fibers": ">= 3.1.0",
        "node-sass": "^4.0.0 || ^5.0.0 || ^6.0.0 || ^7.0.0",
        "sass": "^1.3.0",
        "sass-embedded": "*",
        "webpack": "^5.0.0"
      },
      "peerDependenciesMeta": {
        "fibers": {
          "optional": true
        },
        "node-sass": {
          "optional": true
        },
        "sass": {
          "optional": true
        },
        "sass-embedded": {
          "optional": true
        }
      }
    },
    "node_modules/sax": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/sax/-/sax-1.2.4.tgz",
      "integrity": "sha512-NqVDv9TpANUjFm0N8uM5GxL36UgKi9/atZw+x7YFnQ8ckwFGKrl4xX4yWtrey3UJm5nP1kUbnYgLopqWNSRhWw==",
      "license": "ISC"
    },
    "node_modules/saxes": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/saxes/-/saxes-5.0.1.tgz",
      "integrity": "sha512-5LBh1Tls8c9xgGjw3QrMwETmTMVk0oFgvrFSvWx62llR2hcEInrKNZ2GZCCuuy2lvWrdl5jhbpeqc5hRYKFOcw==",
      "license": "ISC",
      "dependencies": {
        "xmlchars": "^2.2.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/scheduler": {
      "version": "0.23.2",
      "resolved": "https://registry.npmjs.org/scheduler/-/scheduler-0.23.2.tgz",
      "integrity": "sha512-UOShsPwz7NrMUqhR6t0hWjFduvOzbtv7toDH1/hIrfRNIDBnnBWd0CwJTGvTpngVlmwGCdP9/Zl/tVrDqcuYzQ==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0"
      }
    },
    "node_modules/schema-utils": {
      "version": "4.3.3",
      "resolved": "https://registry.npmjs.org/schema-utils/-/schema-utils-4.3.3.tgz",
      "integrity": "sha512-eflK8wEtyOE6+hsaRVPxvUKYCpRgzLqDTb8krvAsRIwOGlHoSgYLgBXoubGgLd2fT41/OUYdb48v4k4WWHQurA==",
      "license": "MIT",
      "dependencies": {
        "@types/json-schema": "^7.0.9",
        "ajv": "^8.9.0",
        "ajv-formats": "^2.1.1",
        "ajv-keywords": "^5.1.0"
      },
      "engines": {
        "node": ">= 10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/schema-utils/node_modules/ajv": {
      "version": "8.18.0",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-8.18.0.tgz",
      "integrity": "sha512-PlXPeEWMXMZ7sPYOHqmDyCJzcfNrUr3fGNKtezX14ykXOEIvyK81d+qydx89KY5O71FKMPaQ2vBfBFI5NHR63A==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "fast-uri": "^3.0.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/schema-utils/node_modules/ajv-keywords": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/ajv-keywords/-/ajv-keywords-5.1.0.tgz",
      "integrity": "sha512-YCS/JNFAUyr5vAuhk1DWm1CBxRHW9LbJ2ozWeemrIqpbsqKjHVxYPyi5GC0rjZIT5JxJ3virVTS8wk4i/Z+krw==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3"
      },
      "peerDependencies": {
        "ajv": "^8.8.2"
      }
    },
    "node_modules/schema-utils/node_modules/json-schema-traverse": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-1.0.0.tgz",
      "integrity": "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug==",
      "license": "MIT"
    },
    "node_modules/select-hose": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/select-hose/-/select-hose-2.0.0.tgz",
      "integrity": "sha512-mEugaLK+YfkijB4fx0e6kImuJdCIt2LxCRcbEYPqRGCs4F2ogyfZU5IAZRdjCP8JPq2AtdNoC/Dux63d9Kiryg==",
      "license": "MIT"
    },
    "node_modules/selfsigned": {
      "version": "2.4.1",
      "resolved": "https://registry.npmjs.org/selfsigned/-/selfsigned-2.4.1.tgz",
      "integrity": "sha512-th5B4L2U+eGLq1TVh7zNRGBapioSORUeymIydxgFpwww9d2qyKvtuPU2jJuHvYAwwqi2Y596QBL3eEqcPEYL8Q==",
      "license": "MIT",
      "dependencies": {
        "@types/node-forge": "^1.3.0",
        "node-forge": "^1"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/semver": {
      "version": "7.7.4",
      "resolved": "https://registry.npmjs.org/semver/-/semver-7.7.4.tgz",
      "integrity": "sha512-vFKC2IEtQnVhpT78h1Yp8wzwrf8CM+MzKMHGJZfBtzhZNycRFnXsHk6E5TxIkkMsgNS7mdX3AGB7x2QM2di4lA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/send": {
      "version": "0.19.2",
      "resolved": "https://registry.npmjs.org/send/-/send-0.19.2.tgz",
      "integrity": "sha512-VMbMxbDeehAxpOtWJXlcUS5E8iXh6QmN+BkRX1GARS3wRaXEEgzCcB10gTQazO42tpNIya8xIyNx8fll1OFPrg==",
      "license": "MIT",
      "dependencies": {
        "debug": "2.6.9",
        "depd": "2.0.0",
        "destroy": "1.2.0",
        "encodeurl": "~2.0.0",
        "escape-html": "~1.0.3",
        "etag": "~1.8.1",
        "fresh": "~0.5.2",
        "http-errors": "~2.0.1",
        "mime": "1.6.0",
        "ms": "2.1.3",
        "on-finished": "~2.4.1",
        "range-parser": "~1.2.1",
        "statuses": "~2.0.2"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/send/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/send/node_modules/debug/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/serialize-javascript": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/serialize-javascript/-/serialize-javascript-6.0.2.tgz",
      "integrity": "sha512-Saa1xPByTTq2gdeFZYLLo+RFE35NHZkAbqZeWNd3BpzppeVisAqpDjcp8dyf6uIvEqJRd46jemmyA4iFIeVk8g==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "randombytes": "^2.1.0"
      }
    },
    "node_modules/serve-index": {
      "version": "1.9.2",
      "resolved": "https://registry.npmjs.org/serve-index/-/serve-index-1.9.2.tgz",
      "integrity": "sha512-KDj11HScOaLmrPxl70KYNW1PksP4Nb/CLL2yvC+Qd2kHMPEEpfc4Re2e4FOay+bC/+XQl/7zAcWON3JVo5v3KQ==",
      "license": "MIT",
      "dependencies": {
        "accepts": "~1.3.8",
        "batch": "0.6.1",
        "debug": "2.6.9",
        "escape-html": "~1.0.3",
        "http-errors": "~1.8.0",
        "mime-types": "~2.1.35",
        "parseurl": "~1.3.3"
      },
      "engines": {
        "node": ">= 0.8.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/serve-index/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/serve-index/node_modules/depd": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/depd/-/depd-1.1.2.tgz",
      "integrity": "sha512-7emPTl6Dpo6JRXOXjLRxck+FlLRX5847cLKEn00PLAgc3g2hTZZgr+e4c2v6QpSmLeFP3n5yUo7ft6avBK/5jQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/serve-index/node_modules/http-errors": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/http-errors/-/http-errors-1.8.1.tgz",
      "integrity": "sha512-Kpk9Sm7NmI+RHhnj6OIWDI1d6fIoFAtFt9RLaTMRlg/8w49juAStsrBgp0Dp4OdxdVbRIeKhtCUvoi/RuAhO4g==",
      "license": "MIT",
      "dependencies": {
        "depd": "~1.1.2",
        "inherits": "2.0.4",
        "setprototypeof": "1.2.0",
        "statuses": ">= 1.5.0 < 2",
        "toidentifier": "1.0.1"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/serve-index/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/serve-index/node_modules/statuses": {
      "version": "1.5.0",
      "resolved": "https://registry.npmjs.org/statuses/-/statuses-1.5.0.tgz",
      "integrity": "sha512-OpZ3zP+jT1PI7I8nemJX4AKmAX070ZkYPVWV/AaKTJl+tXCTGyVdC1a4SL8RUQYEwk/f34ZX8UTykN68FwrqAA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/serve-static": {
      "version": "1.16.3",
      "resolved": "https://registry.npmjs.org/serve-static/-/serve-static-1.16.3.tgz",
      "integrity": "sha512-x0RTqQel6g5SY7Lg6ZreMmsOzncHFU7nhnRWkKgWuMTu5NN0DR5oruckMqRvacAN9d5w6ARnRBXl9xhDCgfMeA==",
      "license": "MIT",
      "dependencies": {
        "encodeurl": "~2.0.0",
        "escape-html": "~1.0.3",
        "parseurl": "~1.3.3",
        "send": "~0.19.1"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/set-function-length": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/set-function-length/-/set-function-length-1.2.2.tgz",
      "integrity": "sha512-pgRc4hJ4/sNjWCSS9AmnS40x3bNMDTknHgL5UaMBTMyJnU90EgWh1Rz+MC9eFu4BuN/UwZjKQuY/1v3rM7HMfg==",
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2",
        "get-intrinsic": "^1.2.4",
        "gopd": "^1.0.1",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/set-function-name": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/set-function-name/-/set-function-name-2.0.2.tgz",
      "integrity": "sha512-7PGFlmtwsEADb0WYyvCMa1t+yke6daIG4Wirafur5kcf+MhUnPms1UeR0CKQdTZD81yESwMHbtn+TR+dMviakQ==",
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-errors": "^1.3.0",
        "functions-have-names": "^1.2.3",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/set-proto": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/set-proto/-/set-proto-1.0.0.tgz",
      "integrity": "sha512-RJRdvCo6IAnPdsvP/7m6bsQqNnn1FCBX5ZNtFL98MmFF/4xAIJTIg1YbHW5DC2W5SKZanrC6i4HsJqlajw/dZw==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/setprototypeof": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/setprototypeof/-/setprototypeof-1.2.0.tgz",
      "integrity": "sha512-E5LDX7Wrp85Kil5bhZv46j8jOeboKq5JMmYM3gVGdGH8xFpPWXUMsNrlODCrkoxMEeNi/XZIwuRvY4XNwYMJpw==",
      "license": "ISC"
    },
    "node_modules/shebang-command": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-2.0.0.tgz",
      "integrity": "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA==",
      "license": "MIT",
      "dependencies": {
        "shebang-regex": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shebang-regex": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-3.0.0.tgz",
      "integrity": "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shell-quote": {
      "version": "1.8.3",
      "resolved": "https://registry.npmjs.org/shell-quote/-/shell-quote-1.8.3.tgz",
      "integrity": "sha512-ObmnIF4hXNg1BqhnHmgbDETF8dLPCggZWBjkQfhZpbszZnYur5DUljTcCHii5LC3J5E0yeO/1LIMyH+UvHQgyw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/side-channel/-/side-channel-1.1.0.tgz",
      "integrity": "sha512-ZX99e6tRweoUXqR+VBrslhda51Nh5MTQwou5tnUDgbtyM0dBgmhEDtWGP/xbKn6hqfPRHujUNwz5fy/wbbhnpw==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3",
        "side-channel-list": "^1.0.0",
        "side-channel-map": "^1.0.1",
        "side-channel-weakmap": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-list": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/side-channel-list/-/side-channel-list-1.0.0.tgz",
      "integrity": "sha512-FCLHtRD/gnpCiCHEiJLOwdmFP+wzCmDEkc9y7NsYxeF4u7Btsn1ZuwgwJGxImImHicJArLP4R0yX4c2KCrMrTA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-map": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/side-channel-map/-/side-channel-map-1.0.1.tgz",
      "integrity": "sha512-VCjCNfgMsby3tTdo02nbjtM/ewra6jPHmpThenkTYh8pG9ucZ/1P8So4u4FGBek/BjpOVsDCMoLA/iuBKIFXRA==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-weakmap": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/side-channel-weakmap/-/side-channel-weakmap-1.0.2.tgz",
      "integrity": "sha512-WPS/HvHQTYnHisLo9McqBHOJk2FkHO/tlpvldyrnem4aeQp4hai3gythswg6p01oSoTl58rcpiFAjF2br2Ak2A==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3",
        "side-channel-map": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/signal-exit": {
      "version": "3.0.7",
      "resolved": "https://registry.npmjs.org/signal-exit/-/signal-exit-3.0.7.tgz",
      "integrity": "sha512-wnD2ZE+l+SPC/uoS0vXeE9L1+0wuaMqKlfz9AMUo38JsyLSBWSFcHR1Rri62LZc12vLr1gb3jl7iwQhgwpAbGQ==",
      "license": "ISC"
    },
    "node_modules/sisteransi": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/sisteransi/-/sisteransi-1.0.5.tgz",
      "integrity": "sha512-bLGGlR1QxBcynn2d5YmDX4MGjlZvy2MRBDRNHLJ8VI6l6+9FUiyTFNJ0IveOSP0bcXgVDPRcfGqA0pjaqUpfVg==",
      "license": "MIT"
    },
    "node_modules/slash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-3.0.0.tgz",
      "integrity": "sha512-g9Q1haeby36OSStwb4ntCGGGaKsaVSjQ68fBxoQcutl5fS1vuY18H3wSt3jFyFtrkx+Kz0V1G85A4MyAdDMi2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/sockjs": {
      "version": "0.3.24",
      "resolved": "https://registry.npmjs.org/sockjs/-/sockjs-0.3.24.tgz",
      "integrity": "sha512-GJgLTZ7vYb/JtPSSZ10hsOYIvEYsjbNU+zPdIHcUaWVNUEPivzxku31865sSSud0Da0W4lEeOPlmw93zLQchuQ==",
      "license": "MIT",
      "dependencies": {
        "faye-websocket": "^0.11.3",
        "uuid": "^8.3.2",
        "websocket-driver": "^0.7.4"
      }
    },
    "node_modules/source-list-map": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/source-list-map/-/source-list-map-2.0.1.tgz",
      "integrity": "sha512-qnQ7gVMxGNxsiL4lEuJwe/To8UnK7fAnmbGEEH8RpLouuKbeEm0lhbQVFIrNSuB+G7tVrAlVsZgETT5nljf+Iw==",
      "license": "MIT"
    },
    "node_modules/source-map": {
      "version": "0.7.6",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.7.6.tgz",
      "integrity": "sha512-i5uvt8C3ikiWeNZSVZNWcfZPItFQOsYTUAOkcUPGd8DqDy1uOUikjt5dG+uRlwyvR108Fb9DOd4GvXfT0N2/uQ==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">= 12"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/source-map-loader": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/source-map-loader/-/source-map-loader-3.0.2.tgz",
      "integrity": "sha512-BokxPoLjyl3iOrgkWaakaxqnelAJSS+0V+De0kKIq6lyWrXuiPgYTGp6z3iHmqljKAaLXwZa+ctD8GccRJeVvg==",
      "license": "MIT",
      "dependencies": {
        "abab": "^2.0.5",
        "iconv-lite": "^0.6.3",
        "source-map-js": "^1.0.1"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.0.0"
      }
    },
    "node_modules/source-map-support": {
      "version": "0.5.21",
      "resolved": "https://registry.npmjs.org/source-map-support/-/source-map-support-0.5.21.tgz",
      "integrity": "sha512-uBHU3L3czsIyYXKX88fdrGovxdSCoTGDRZ6SYXtSRxLZUzHg5P/66Ht6uoUlHu9EZod+inXhKo3qQgwXUT/y1w==",
      "license": "MIT",
      "dependencies": {
        "buffer-from": "^1.0.0",
        "source-map": "^0.6.0"
      }
    },
    "node_modules/source-map-support/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/sourcemap-codec": {
      "version": "1.4.8",
      "resolved": "https://registry.npmjs.org/sourcemap-codec/-/sourcemap-codec-1.4.8.tgz",
      "integrity": "sha512-9NykojV5Uih4lgo5So5dtw+f0JgJX30KCNI8gwhz2J9A15wD0Ml6tjHKwf6fTSa6fAdVBdZeNOs9eJ71qCk8vA==",
      "deprecated": "Please use @jridgewell/sourcemap-codec instead",
      "license": "MIT"
    },
    "node_modules/spdy": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/spdy/-/spdy-4.0.2.tgz",
      "integrity": "sha512-r46gZQZQV+Kl9oItvl1JZZqJKGr+oEkB08A6BzkiR7593/7IbtuncXHd2YoYeTsG4157ZssMu9KYvUHLcjcDoA==",
      "license": "MIT",
      "dependencies": {
        "debug": "^4.1.0",
        "handle-thing": "^2.0.0",
        "http-deceiver": "^1.2.7",
        "select-hose": "^2.0.0",
        "spdy-transport": "^3.0.0"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/spdy-transport": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/spdy-transport/-/spdy-transport-3.0.0.tgz",
      "integrity": "sha512-hsLVFE5SjA6TCisWeJXFKniGGOpBgMLmerfO2aCyCU5s7nJ/rpAepqmFifv/GCbSbueEeAJJnmSQ2rKC/g8Fcw==",
      "license": "MIT",
      "dependencies": {
        "debug": "^4.1.0",
        "detect-node": "^2.0.4",
        "hpack.js": "^2.1.6",
        "obuf": "^1.1.2",
        "readable-stream": "^3.0.6",
        "wbuf": "^1.7.3"
      }
    },
    "node_modules/sprintf-js": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/sprintf-js/-/sprintf-js-1.0.3.tgz",
      "integrity": "sha512-D9cPgkvLlV3t3IzL0D0YLvGA9Ahk4PcvVwUbN0dSGr1aP0Nrt4AEnTUbuGvquEC0mA64Gqt1fzirlRs5ibXx8g==",
      "license": "BSD-3-Clause"
    },
    "node_modules/stable": {
      "version": "0.1.8",
      "resolved": "https://registry.npmjs.org/stable/-/stable-0.1.8.tgz",
      "integrity": "sha512-ji9qxRnOVfcuLDySj9qzhGSEFVobyt1kIOSkj1qZzYLzq7Tos/oUUWvotUPQLlrsidqsK6tBH89Bc9kL5zHA6w==",
      "deprecated": "Modern JS already guarantees Array#sort() is a stable sort, so this library is deprecated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort#browser_compatibility",
      "license": "MIT"
    },
    "node_modules/stack-utils": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/stack-utils/-/stack-utils-2.0.6.tgz",
      "integrity": "sha512-XlkWvfIm6RmsWtNJx+uqtKLS8eqFbxUg0ZzLXqY0caEy9l7hruX8IpiDnjsLavoBgqCCR71TqWO8MaXYheJ3RQ==",
      "license": "MIT",
      "dependencies": {
        "escape-string-regexp": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/stack-utils/node_modules/escape-string-regexp": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-2.0.0.tgz",
      "integrity": "sha512-UpzcLCXolUWcNu5HtVMHYdXJjArjsF9C0aNnquZYY4uW/Vu0miy5YoWvbV345HauVvcAUnpRuhMMcqTcGOY2+w==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/stackframe": {
      "version": "1.3.4",
      "resolved": "https://registry.npmjs.org/stackframe/-/stackframe-1.3.4.tgz",
      "integrity": "sha512-oeVtt7eWQS+Na6F//S4kJ2K2VbRlS9D43mAlMyVpVWovy9o+jfgH8O9agzANzaiLjclA0oYzUXEM4PurhSUChw==",
      "license": "MIT"
    },
    "node_modules/static-eval": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/static-eval/-/static-eval-2.1.1.tgz",
      "integrity": "sha512-MgWpQ/ZjGieSVB3eOJVs4OA2LT/q1vx98KPCTTQPzq/aLr0YUXTsgryTXr4SLfR0ZfUUCiedM9n/ABeDIyy4mA==",
      "license": "MIT",
      "dependencies": {
        "escodegen": "^2.1.0"
      }
    },
    "node_modules/statuses": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/statuses/-/statuses-2.0.2.tgz",
      "integrity": "sha512-DvEy55V3DB7uknRo+4iOGT5fP1slR8wQohVdknigZPMpMstaKJQWhwiYBACJE3Ul2pTnATihhBYnRhZQHGBiRw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/stop-iteration-iterator": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/stop-iteration-iterator/-/stop-iteration-iterator-1.1.0.tgz",
      "integrity": "sha512-eLoXW/DHyl62zxY4SCaIgnRhuMr6ri4juEYARS8E6sCEqzKpOiE521Ucofdx+KnDZl5xmvGYaaKCk5FEOxJCoQ==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "internal-slot": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/string_decoder": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/string_decoder/-/string_decoder-1.3.0.tgz",
      "integrity": "sha512-hkRX8U1WjJFd8LsDJ2yQ/wWWxaopEsABU1XfkM8A+j0+85JAGppt16cr1Whg6KIbb4okU6Mql6BOj+uup/wKeA==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "~5.2.0"
      }
    },
    "node_modules/string-length": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/string-length/-/string-length-4.0.2.tgz",
      "integrity": "sha512-+l6rNN5fYHNhZZy41RXsYptCjA2Igmq4EG7kZAYFQI1E1VTXarr6ZPXBg6eq7Y6eK4FEhY6AJlyuFIb/v/S0VQ==",
      "license": "MIT",
      "dependencies": {
        "char-regex": "^1.0.2",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/string-natural-compare": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/string-natural-compare/-/string-natural-compare-3.0.1.tgz",
      "integrity": "sha512-n3sPwynL1nwKi3WJ6AIsClwBMa0zTi54fn2oLU6ndfTSIO05xaznjSf15PcBZU6FNWbmN5Q6cxT4V5hGvB4taw==",
      "license": "MIT"
    },
    "node_modules/string-width": {
      "version": "4.2.3",
      "resolved": "https://registry.npmjs.org/string-width/-/string-width-4.2.3.tgz",
      "integrity": "sha512-wKyQRQpjJ0sIp62ErSZdGsjMJWsap5oRNihHhu6G7JVO/9jIB6UyevL+tXuOqrng8j/cxKTWyWUwvSTriiZz/g==",
      "license": "MIT",
      "dependencies": {
        "emoji-regex": "^8.0.0",
        "is-fullwidth-code-point": "^3.0.0",
        "strip-ansi": "^6.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/string-width/node_modules/emoji-regex": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-8.0.0.tgz",
      "integrity": "sha512-MSjYzcWNOA0ewAHpz0MxpYFvwg6yjy1NG3xteoqz644VCo/RPgnr1/GGt+ic3iJTzQ8Eu3TdM14SawnVUmGE6A==",
      "license": "MIT"
    },
    "node_modules/string.prototype.includes": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/string.prototype.includes/-/string.prototype.includes-2.0.1.tgz",
      "integrity": "sha512-o7+c9bW6zpAdJHTtujeePODAhkuicdAryFsfVKwA+wGw89wJ4GTY484WTucM9hLtDEOpOvI+aHnzqnC5lHp4Rg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.3"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/string.prototype.matchall": {
      "version": "4.0.12",
      "resolved": "https://registry.npmjs.org/string.prototype.matchall/-/string.prototype.matchall-4.0.12.tgz",
      "integrity": "sha512-6CC9uyBL+/48dYizRf7H7VAYCMCNTBeM78x/VTUe9bFEaxBepPJDa1Ow99LqI/1yF7kuy7Q3cQsYMrcjGUcskA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.6",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.6",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "internal-slot": "^1.1.0",
        "regexp.prototype.flags": "^1.5.3",
        "set-function-name": "^2.0.2",
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.repeat": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/string.prototype.repeat/-/string.prototype.repeat-1.0.0.tgz",
      "integrity": "sha512-0u/TldDbKD8bFCQ/4f5+mNRrXwZ8hg2w7ZR8wa16e8z9XpePWl3eGEcUD0OXpEH/VJH/2G3gjUtR3ZOiBe2S/w==",
      "license": "MIT",
      "dependencies": {
        "define-properties": "^1.1.3",
        "es-abstract": "^1.17.5"
      }
    },
    "node_modules/string.prototype.trim": {
      "version": "1.2.10",
      "resolved": "https://registry.npmjs.org/string.prototype.trim/-/string.prototype.trim-1.2.10.tgz",
      "integrity": "sha512-Rs66F0P/1kedk5lyYyH9uBzuiI/kNRmwJAR9quK6VOtIpZ2G+hMZd+HQbbv25MgCA6gEffoMZYxlTod4WcdrKA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "define-data-property": "^1.1.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-object-atoms": "^1.0.0",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trimend": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/string.prototype.trimend/-/string.prototype.trimend-1.0.9.tgz",
      "integrity": "sha512-G7Ok5C6E/j4SGfyLCloXTrngQIQU3PWtXGst3yM7Bea9FRURf1S42ZHlZZtsNque2FN2PoUhfZXYLNWwEr4dLQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trimstart": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/string.prototype.trimstart/-/string.prototype.trimstart-1.0.8.tgz",
      "integrity": "sha512-UXSH262CSZY1tfu3G3Secr6uGLCFVPMhIqHjlgCUtCCcgihYc/xKs9djMTMUOb2j1mVSeU8EU6NWc/iQKU6Gfg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/stringify-object": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/stringify-object/-/stringify-object-3.3.0.tgz",
      "integrity": "sha512-rHqiFh1elqCQ9WPLIC8I0Q/g/wj5J1eMkyoiD6eoQApWHP0FtlK7rqnhmabL5VUY9JQCcqwwvlOaSuutekgyrw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "get-own-enumerable-property-symbols": "^3.0.0",
        "is-obj": "^1.0.1",
        "is-regexp": "^1.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/strip-ansi": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-bom": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/strip-bom/-/strip-bom-4.0.0.tgz",
      "integrity": "sha512-3xurFv5tEgii33Zi8Jtp55wEIILR9eh34FAW00PZf+JnSsTmV/ioewSgQl97JHvgjoRGwPShsWm+IdrxB35d0w==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-comments": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/strip-comments/-/strip-comments-2.0.1.tgz",
      "integrity": "sha512-ZprKx+bBLXv067WTCALv8SSz5l2+XhpYCsVtSqlMnkAXMWDq+/ekVbl1ghqP9rUHTzv6sm/DwCOiYutU/yp1fw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/strip-final-newline": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/strip-final-newline/-/strip-final-newline-2.0.0.tgz",
      "integrity": "sha512-BrpvfNAE3dcvq7ll3xVumzjKjZQ5tI1sEUIKr3Uoks0XUl45St3FlatVqef9prk4jRDzhW6WZg+3bk93y6pLjA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/strip-json-comments": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/strip-json-comments/-/strip-json-comments-3.1.1.tgz",
      "integrity": "sha512-6fPc+R4ihwqP6N/aIv2f1gMH8lOVtWQHoqC4yK6oSDVVocumAsfCqjkXnqiYMhmMwS/mEHLp7Vehlt3ql6lEig==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/style-loader": {
      "version": "3.3.4",
      "resolved": "https://registry.npmjs.org/style-loader/-/style-loader-3.3.4.tgz",
      "integrity": "sha512-0WqXzrsMTyb8yjZJHDqwmnwRJvhALK9LfRtRc6B4UTWe8AijYLZYZ9thuJTZc2VfQWINADW/j+LiJnfy2RoC1w==",
      "license": "MIT",
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.0.0"
      }
    },
    "node_modules/stylehacks": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/stylehacks/-/stylehacks-5.1.1.tgz",
      "integrity": "sha512-sBpcd5Hx7G6seo7b1LkpttvTz7ikD0LlH5RmdcBNb6fFR0Fl7LQwHDFr300q4cwUqi+IYrFGmsIHieMBfnN/Bw==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "postcss-selector-parser": "^6.0.4"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/sucrase": {
      "version": "3.35.1",
      "resolved": "https://registry.npmjs.org/sucrase/-/sucrase-3.35.1.tgz",
      "integrity": "sha512-DhuTmvZWux4H1UOnWMB3sk0sbaCVOoQZjv8u1rDoTV0HTdGem9hkAZtl4JZy8P2z4Bg0nT+YMeOFyVr4zcG5Tw==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.2",
        "commander": "^4.0.0",
        "lines-and-columns": "^1.1.6",
        "mz": "^2.7.0",
        "pirates": "^4.0.1",
        "tinyglobby": "^0.2.11",
        "ts-interface-checker": "^0.1.9"
      },
      "bin": {
        "sucrase": "bin/sucrase",
        "sucrase-node": "bin/sucrase-node"
      },
      "engines": {
        "node": ">=16 || 14 >=14.17"
      }
    },
    "node_modules/sucrase/node_modules/commander": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/commander/-/commander-4.1.1.tgz",
      "integrity": "sha512-NOKm8xhkzAjzFx8B2v5OAHT+u5pRQc2UCa2Vq9jYL/31o2wi9mxBA7LIFs3sV5VSC49z6pEhfbMULvShKj26WA==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/supports-color": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-7.2.0.tgz",
      "integrity": "sha512-qpCAvRl9stuOHveKsn7HncJRvv501qIacKzQlO/+Lwxc9+0q2wLyv4Dfvt80/DPn2pqOBsJdDiogXGR9+OvwRw==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/supports-hyperlinks": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/supports-hyperlinks/-/supports-hyperlinks-2.3.0.tgz",
      "integrity": "sha512-RpsAZlpWcDwOPQA22aCH4J0t7L8JmAvsCxfOSEwm7cQs3LshN36QaTkwd70DnBOXDWGssw2eUoc8CaRWT0XunA==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^4.0.0",
        "supports-color": "^7.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/supports-preserve-symlinks-flag": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/supports-preserve-symlinks-flag/-/supports-preserve-symlinks-flag-1.0.0.tgz",
      "integrity": "sha512-ot0WnXS9fgdkgIcePe6RHNk1WA8+muPa6cSjeR3V8K27q9BB1rTE3R1p7Hv0z1ZyAc8s6Vvv8DIyWf681MAt0w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/svg-parser": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/svg-parser/-/svg-parser-2.0.4.tgz",
      "integrity": "sha512-e4hG1hRwoOdRb37cIMSgzNsxyzKfayW6VOflrwvR+/bzrkyxY/31WkbgnQpgtrNp1SdpJvpUAGTa/ZoiPNDuRQ==",
      "license": "MIT"
    },
    "node_modules/svgo": {
      "version": "1.3.2",
      "resolved": "https://registry.npmjs.org/svgo/-/svgo-1.3.2.tgz",
      "integrity": "sha512-yhy/sQYxR5BkC98CY7o31VGsg014AKLEPxdfhora76l36hD9Rdy5NZA/Ocn6yayNPgSamYdtX2rFJdcv07AYVw==",
      "deprecated": "This SVGO version is no longer supported. Upgrade to v2.x.x.",
      "license": "MIT",
      "dependencies": {
        "chalk": "^2.4.1",
        "coa": "^2.0.2",
        "css-select": "^2.0.0",
        "css-select-base-adapter": "^0.1.1",
        "css-tree": "1.0.0-alpha.37",
        "csso": "^4.0.2",
        "js-yaml": "^3.13.1",
        "mkdirp": "~0.5.1",
        "object.values": "^1.1.0",
        "sax": "~1.2.4",
        "stable": "^0.1.8",
        "unquote": "~1.1.1",
        "util.promisify": "~1.0.0"
      },
      "bin": {
        "svgo": "bin/svgo"
      },
      "engines": {
        "node": ">=4.0.0"
      }
    },
    "node_modules/svgo/node_modules/ansi-styles": {
      "version": "3.2.1",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-3.2.1.tgz",
      "integrity": "sha512-VT0ZI6kZRdTh8YyJw3SMbYm/u+NqfsAxEpWO0Pf9sq8/e94WxxOpPKx9FR1FlyCtOVDNOQ+8ntlqFxiRc+r5qA==",
      "license": "MIT",
      "dependencies": {
        "color-convert": "^1.9.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/svgo/node_modules/chalk": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/chalk/-/chalk-2.4.2.tgz",
      "integrity": "sha512-Mti+f9lpJNcwF4tWV8/OrTTtF1gZi+f8FqlyAdouralcFWFQWF2+NgCHShjkCb+IFBLq9buZwE1xckQU4peSuQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^3.2.1",
        "escape-string-regexp": "^1.0.5",
        "supports-color": "^5.3.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/svgo/node_modules/color-convert": {
      "version": "1.9.3",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-1.9.3.tgz",
      "integrity": "sha512-QfAUtd+vFdAtFQcC8CCyYt1fYWxSqAiK2cSD6zDB8N3cpsEBAvRxp9zOGg6G/SHHJYAT88/az/IuDGALsNVbGg==",
      "license": "MIT",
      "dependencies": {
        "color-name": "1.1.3"
      }
    },
    "node_modules/svgo/node_modules/color-name": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.3.tgz",
      "integrity": "sha512-72fSenhMw2HZMTVHeCA9KCmpEIbzWiQsjN+BHcBbS9vr1mtt+vJjPdksIBNUmKAW8TFUDPJK5SUU3QhE9NEXDw==",
      "license": "MIT"
    },
    "node_modules/svgo/node_modules/css-select": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/css-select/-/css-select-2.1.0.tgz",
      "integrity": "sha512-Dqk7LQKpwLoH3VovzZnkzegqNSuAziQyNZUcrdDM401iY+R5NkGBXGmtO05/yaXQziALuPogeG0b7UAgjnTJTQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "boolbase": "^1.0.0",
        "css-what": "^3.2.1",
        "domutils": "^1.7.0",
        "nth-check": "^1.0.2"
      }
    },
    "node_modules/svgo/node_modules/css-what": {
      "version": "3.4.2",
      "resolved": "https://registry.npmjs.org/css-what/-/css-what-3.4.2.tgz",
      "integrity": "sha512-ACUm3L0/jiZTqfzRM3Hi9Q8eZqd6IK37mMWPLz9PJxkLWllYeRf+EHUSHYEtFop2Eqytaq1FizFVh7XfBnXCDQ==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">= 6"
      },
      "funding": {
        "url": "https://github.com/sponsors/fb55"
      }
    },
    "node_modules/svgo/node_modules/dom-serializer": {
      "version": "0.2.2",
      "resolved": "https://registry.npmjs.org/dom-serializer/-/dom-serializer-0.2.2.tgz",
      "integrity": "sha512-2/xPb3ORsQ42nHYiSunXkDjPLBaEj/xTwUO4B7XCZQTRk7EBtTOPaygh10YAAh2OI1Qrp6NWfpAhzswj0ydt9g==",
      "license": "MIT",
      "dependencies": {
        "domelementtype": "^2.0.1",
        "entities": "^2.0.0"
      }
    },
    "node_modules/svgo/node_modules/domutils": {
      "version": "1.7.0",
      "resolved": "https://registry.npmjs.org/domutils/-/domutils-1.7.0.tgz",
      "integrity": "sha512-Lgd2XcJ/NjEw+7tFvfKxOzCYKZsdct5lczQ2ZaQY8Djz7pfAD3Gbp8ySJWtreII/vDlMVmxwa6pHmdxIYgttDg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "dom-serializer": "0",
        "domelementtype": "1"
      }
    },
    "node_modules/svgo/node_modules/domutils/node_modules/domelementtype": {
      "version": "1.3.1",
      "resolved": "https://registry.npmjs.org/domelementtype/-/domelementtype-1.3.1.tgz",
      "integrity": "sha512-BSKB+TSpMpFI/HOxCNr1O8aMOTZ8hT3pM3GQ0w/mWRmkhEDSFJkkyzz4XQsBV44BChwGkrDfMyjVD0eA2aFV3w==",
      "license": "BSD-2-Clause"
    },
    "node_modules/svgo/node_modules/escape-string-regexp": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-1.0.5.tgz",
      "integrity": "sha512-vbRorB5FUQWvla16U8R/qgaFIya2qGzwDrNmCZuYKrbdSUMG6I1ZCGQRefkRVhuOkIGVne7BQ35DSfo1qvJqFg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/svgo/node_modules/has-flag": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/has-flag/-/has-flag-3.0.0.tgz",
      "integrity": "sha512-sKJf1+ceQBr4SMkvQnBDNDtf4TXpVhVGateu0t918bl30FnbE2m4vNLX+VWe/dpjlb+HugGYzW7uQXH98HPEYw==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/svgo/node_modules/nth-check": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/nth-check/-/nth-check-1.0.2.tgz",
      "integrity": "sha512-WeBOdju8SnzPN5vTUJYxYUxLeXpCaVP5i5e0LF8fg7WORF2Wd7wFX/pk0tYZk7s8T+J7VLy0Da6J1+wCT0AtHg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "boolbase": "~1.0.0"
      }
    },
    "node_modules/svgo/node_modules/supports-color": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-5.5.0.tgz",
      "integrity": "sha512-QjVjwdXIt408MIiAqCX4oUKsgU2EqAGzs2Ppkm4aQYbjm+ZEWEcW4SfFNTr4uMNZma0ey4f5lgLrkB0aX0QMow==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^3.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/symbol-tree": {
      "version": "3.2.4",
      "resolved": "https://registry.npmjs.org/symbol-tree/-/symbol-tree-3.2.4.tgz",
      "integrity": "sha512-9QNk5KwDF+Bvz+PyObkmSYjI5ksVUYtjW7AU22r2NKcfLJcXp96hkDWU3+XndOsUb+AQ9QhfzfCT2O+CNWT5Tw==",
      "license": "MIT"
    },
    "node_modules/tailwindcss": {
      "version": "3.4.19",
      "resolved": "https://registry.npmjs.org/tailwindcss/-/tailwindcss-3.4.19.tgz",
      "integrity": "sha512-3ofp+LL8E+pK/JuPLPggVAIaEuhvIz4qNcf3nA1Xn2o/7fb7s/TYpHhwGDv1ZU3PkBluUVaF8PyCHcm48cKLWQ==",
      "license": "MIT",
      "dependencies": {
        "@alloc/quick-lru": "^5.2.0",
        "arg": "^5.0.2",
        "chokidar": "^3.6.0",
        "didyoumean": "^1.2.2",
        "dlv": "^1.1.3",
        "fast-glob": "^3.3.2",
        "glob-parent": "^6.0.2",
        "is-glob": "^4.0.3",
        "jiti": "^1.21.7",
        "lilconfig": "^3.1.3",
        "micromatch": "^4.0.8",
        "normalize-path": "^3.0.0",
        "object-hash": "^3.0.0",
        "picocolors": "^1.1.1",
        "postcss": "^8.4.47",
        "postcss-import": "^15.1.0",
        "postcss-js": "^4.0.1",
        "postcss-load-config": "^4.0.2 || ^5.0 || ^6.0",
        "postcss-nested": "^6.2.0",
        "postcss-selector-parser": "^6.1.2",
        "resolve": "^1.22.8",
        "sucrase": "^3.35.0"
      },
      "bin": {
        "tailwind": "lib/cli.js",
        "tailwindcss": "lib/cli.js"
      },
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/tailwindcss/node_modules/lilconfig": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/lilconfig/-/lilconfig-3.1.3.tgz",
      "integrity": "sha512-/vlFKAoH5Cgt3Ie+JLhRbwOsCQePABiU3tJ1egGvyQ+33R/vcwM2Zl2QR/LzjsBeItPt3oSVXapn+m4nQDvpzw==",
      "license": "MIT",
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/antonk52"
      }
    },
    "node_modules/tailwindcss/node_modules/postcss-load-config": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/postcss-load-config/-/postcss-load-config-6.0.1.tgz",
      "integrity": "sha512-oPtTM4oerL+UXmx+93ytZVN82RrlY/wPUV8IeDxFrzIjXOLF1pN+EmKPLbubvKHT2HC20xXsCAH2Z+CKV6Oz/g==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "lilconfig": "^3.1.1"
      },
      "engines": {
        "node": ">= 18"
      },
      "peerDependencies": {
        "jiti": ">=1.21.0",
        "postcss": ">=8.0.9",
        "tsx": "^4.8.1",
        "yaml": "^2.4.2"
      },
      "peerDependenciesMeta": {
        "jiti": {
          "optional": true
        },
        "postcss": {
          "optional": true
        },
        "tsx": {
          "optional": true
        },
        "yaml": {
          "optional": true
        }
      }
    },
    "node_modules/tailwindcss/node_modules/yaml": {
      "version": "2.8.2",
      "resolved": "https://registry.npmjs.org/yaml/-/yaml-2.8.2.tgz",
      "integrity": "sha512-mplynKqc1C2hTVYxd0PU2xQAc22TI1vShAYGksCCfxbn/dFwnHTNi1bvYsBTkhdUNtGIf5xNOg938rrSSYvS9A==",
      "extraneous": true,
      "license": "ISC",
      "bin": {
        "yaml": "bin.mjs"
      },
      "engines": {
        "node": ">= 14.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/eemeli"
      }
    },
    "node_modules/tapable": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/tapable/-/tapable-2.3.0.tgz",
      "integrity": "sha512-g9ljZiwki/LfxmQADO3dEY1CbpmXT5Hm2fJ+QaGKwSXUylMybePR7/67YW7jOrrvjEgL1Fmz5kzyAjWVWLlucg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/temp-dir": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/temp-dir/-/temp-dir-2.0.0.tgz",
      "integrity": "sha512-aoBAniQmmwtcKp/7BzsH8Cxzv8OL736p7v1ihGb5e9DJ9kTwGWHrQrVB5+lfVDzfGrdRzXch+ig7LHaY1JTOrg==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/tempy": {
      "version": "0.6.0",
      "resolved": "https://registry.npmjs.org/tempy/-/tempy-0.6.0.tgz",
      "integrity": "sha512-G13vtMYPT/J8A4X2SjdtBTphZlrp1gKv6hZiOjw14RCWg6GbHuQBGtjlx75xLbYV/wEc0D7G5K4rxKP/cXk8Bw==",
      "license": "MIT",
      "dependencies": {
        "is-stream": "^2.0.0",
        "temp-dir": "^2.0.0",
        "type-fest": "^0.16.0",
        "unique-string": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/tempy/node_modules/type-fest": {
      "version": "0.16.0",
      "resolved": "https://registry.npmjs.org/type-fest/-/type-fest-0.16.0.tgz",
      "integrity": "sha512-eaBzG6MxNzEn9kiwvtre90cXaNLkmadMWa1zQMs3XORCXNbsH/OewwbxC5ia9dCxIxnTAsSxXJaa/p5y8DlvJg==",
      "license": "(MIT OR CC0-1.0)",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/terminal-link": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/terminal-link/-/terminal-link-2.1.1.tgz",
      "integrity": "sha512-un0FmiRUQNr5PJqy9kP7c40F5BOfpGlYTrxonDChEZB7pzZxRNp/bt+ymiy9/npwXya9KH99nJ/GXFIiUkYGFQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-escapes": "^4.2.1",
        "supports-hyperlinks": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/terser": {
      "version": "5.46.0",
      "resolved": "https://registry.npmjs.org/terser/-/terser-5.46.0.tgz",
      "integrity": "sha512-jTwoImyr/QbOWFFso3YoU3ik0jBBDJ6JTOQiy/J2YxVJdZCc+5u7skhNwiOR3FQIygFqVUPHl7qbbxtjW2K3Qg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "@jridgewell/source-map": "^0.3.3",
        "acorn": "^8.15.0",
        "commander": "^2.20.0",
        "source-map-support": "~0.5.20"
      },
      "bin": {
        "terser": "bin/terser"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/terser-webpack-plugin": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/terser-webpack-plugin/-/terser-webpack-plugin-5.4.0.tgz",
      "integrity": "sha512-Bn5vxm48flOIfkdl5CaD2+1CiUVbonWQ3KQPyP7/EuIl9Gbzq/gQFOzaMFUEgVjB1396tcK0SG8XcNJ/2kDH8g==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/trace-mapping": "^0.3.25",
        "jest-worker": "^27.4.5",
        "schema-utils": "^4.3.0",
        "terser": "^5.31.1"
      },
      "engines": {
        "node": ">= 10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.1.0"
      },
      "peerDependenciesMeta": {
        "@swc/core": {
          "optional": true
        },
        "esbuild": {
          "optional": true
        },
        "uglify-js": {
          "optional": true
        }
      }
    },
    "node_modules/terser/node_modules/commander": {
      "version": "2.20.3",
      "resolved": "https://registry.npmjs.org/commander/-/commander-2.20.3.tgz",
      "integrity": "sha512-GpVkmM8vF2vQUkj2LvZmD35JxeJOLCwJ9cUkugyk2nuhbv3+mJvpLYYt+0+USMxE+oj+ey/lJEnhZw75x/OMcQ==",
      "license": "MIT"
    },
    "node_modules/test-exclude": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/test-exclude/-/test-exclude-6.0.0.tgz",
      "integrity": "sha512-cAGWPIyOHU6zlmg88jwm7VRyXnMN7iV68OGAbYDk/Mh/xC/pzVPlQtY6ngoIH/5/tciuhGfvESU8GrHrcxD56w==",
      "license": "ISC",
      "dependencies": {
        "@istanbuljs/schema": "^0.1.2",
        "glob": "^7.1.4",
        "minimatch": "^3.0.4"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/text-table": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/text-table/-/text-table-0.2.0.tgz",
      "integrity": "sha512-N+8UisAXDGk8PFXP4HAzVR9nbfmVJ3zYLAWiTIoqC5v5isinhr+r5uaO8+7r3BMfuNIufIsA7RdpVgacC2cSpw==",
      "license": "MIT"
    },
    "node_modules/thenify": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/thenify/-/thenify-3.3.1.tgz",
      "integrity": "sha512-RVZSIV5IG10Hk3enotrhvz0T9em6cyHBLkH/YAZuKqd8hRkKhSfCGIcP2KUY0EPxndzANBmNllzWPwak+bheSw==",
      "license": "MIT",
      "dependencies": {
        "any-promise": "^1.0.0"
      }
    },
    "node_modules/thenify-all": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/thenify-all/-/thenify-all-1.6.0.tgz",
      "integrity": "sha512-RNxQH/qI8/t3thXJDwcstUO4zeqo64+Uy/+sNVRBx4Xn2OX+OZ9oP+iJnNFqplFra2ZUVeKCSa2oVWi3T4uVmA==",
      "license": "MIT",
      "dependencies": {
        "thenify": ">= 3.1.0 < 4"
      },
      "engines": {
        "node": ">=0.8"
      }
    },
    "node_modules/throat": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/throat/-/throat-6.0.2.tgz",
      "integrity": "sha512-WKexMoJj3vEuK0yFEapj8y64V0A6xcuPuK9Gt1d0R+dzCSJc0lHqQytAbSB4cDAK0dWh4T0E2ETkoLE2WZ41OQ==",
      "license": "MIT"
    },
    "node_modules/thunky": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/thunky/-/thunky-1.1.0.tgz",
      "integrity": "sha512-eHY7nBftgThBqOyHGVN+l8gF0BucP09fMo0oO/Lb0w1OF80dJv+lDVpXG60WMQvkcxAkNybKsrEIE3ZtKGmPrA==",
      "license": "MIT"
    },
    "node_modules/tinyglobby": {
      "version": "0.2.15",
      "resolved": "https://registry.npmjs.org/tinyglobby/-/tinyglobby-0.2.15.tgz",
      "integrity": "sha512-j2Zq4NyQYG5XMST4cbs02Ak8iJUdxRM0XI5QyxXuZOzKOINmWurp3smXu3y5wDcJrptwpSjgXHzIQxR0omXljQ==",
      "license": "MIT",
      "dependencies": {
        "fdir": "^6.5.0",
        "picomatch": "^4.0.3"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/SuperchupuDev"
      }
    },
    "node_modules/tinyglobby/node_modules/fdir": {
      "version": "6.5.0",
      "resolved": "https://registry.npmjs.org/fdir/-/fdir-6.5.0.tgz",
      "integrity": "sha512-tIbYtZbucOs0BRGqPJkshJUYdL+SDH7dVM8gjy+ERp3WAUjLEFJE+02kanyHtwjWOnwrKYBiwAmM0p4kLJAnXg==",
      "license": "MIT",
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "picomatch": "^3 || ^4"
      },
      "peerDependenciesMeta": {
        "picomatch": {
          "optional": true
        }
      }
    },
    "node_modules/tinyglobby/node_modules/picomatch": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.3.tgz",
      "integrity": "sha512-5gTmgEY/sqK6gFXLIsQNH19lWb4ebPDLA4SdLP7dsWkIXHWlG66oPuVvXSGFPppYZz8ZDZq0dYYrbHfBCVUb1Q==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/tmpl": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/tmpl/-/tmpl-1.0.5.tgz",
      "integrity": "sha512-3f0uOEAQwIqGuWW2MVzYg8fV/QNnc/IpuJNG837rLuczAaLVHslWHZQj4IGiEl5Hs3kkbhwL9Ab7Hrsmuj+Smw==",
      "license": "BSD-3-Clause"
    },
    "node_modules/to-regex-range": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/to-regex-range/-/to-regex-range-5.0.1.tgz",
      "integrity": "sha512-65P7iz6X5yEr1cwcgvQxbbIw7Uk3gOy5dIdtZ4rDveLqhrdJP+Li/Hx6tyK0NEb+2GCyneCMJiGqrADCSNk8sQ==",
      "license": "MIT",
      "dependencies": {
        "is-number": "^7.0.0"
      },
      "engines": {
        "node": ">=8.0"
      }
    },
    "node_modules/toidentifier": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/toidentifier/-/toidentifier-1.0.1.tgz",
      "integrity": "sha512-o5sSPKEkg/DIQNmH43V0/uerLrpzVedkUh8tGNvaeXpfpuwjKenlSox/2O/BTlZUtEe+JG7s5YhEz608PlAHRA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.6"
      }
    },
    "node_modules/tough-cookie": {
      "version": "4.1.4",
      "resolved": "https://registry.npmjs.org/tough-cookie/-/tough-cookie-4.1.4.tgz",
      "integrity": "sha512-Loo5UUvLD9ScZ6jh8beX1T6sO1w2/MpCRpEP7V280GKMVUQ0Jzar2U3UJPsrdbziLEMMhu3Ujnq//rhiFuIeag==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "psl": "^1.1.33",
        "punycode": "^2.1.1",
        "universalify": "^0.2.0",
        "url-parse": "^1.5.3"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/tough-cookie/node_modules/universalify": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/universalify/-/universalify-0.2.0.tgz",
      "integrity": "sha512-CJ1QgKmNg3CwvAv/kOFmtnEN05f0D/cn9QntgNOQlQF9dgvVTHj3t+8JPdjqawCHk7V/KA+fbUqzZ9XWhcqPUg==",
      "license": "MIT",
      "engines": {
        "node": ">= 4.0.0"
      }
    },
    "node_modules/tr46": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/tr46/-/tr46-2.1.0.tgz",
      "integrity": "sha512-15Ih7phfcdP5YxqiB+iDtLoaTz4Nd35+IiAv0kQ5FNKHzXgdWqPoTIqEDDJmXceQt4JZk6lVPT8lnDlPpGDppw==",
      "license": "MIT",
      "dependencies": {
        "punycode": "^2.1.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/tryer": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/tryer/-/tryer-1.0.1.tgz",
      "integrity": "sha512-c3zayb8/kWWpycWYg87P71E1S1ZL6b6IJxfb5fvsUgsf0S2MVGaDhDXXjDMpdCpfWXqptc+4mXwmiy1ypXqRAA==",
      "license": "MIT"
    },
    "node_modules/ts-interface-checker": {
      "version": "0.1.13",
      "resolved": "https://registry.npmjs.org/ts-interface-checker/-/ts-interface-checker-0.1.13.tgz",
      "integrity": "sha512-Y/arvbn+rrz3JCKl9C4kVNfTfSm2/mEp5FSz5EsZSANGPSlQrpRI5M4PKF+mJnE52jOO90PnPSc3Ur3bTQw0gA==",
      "license": "Apache-2.0"
    },
    "node_modules/tsconfig-paths": {
      "version": "3.15.0",
      "resolved": "https://registry.npmjs.org/tsconfig-paths/-/tsconfig-paths-3.15.0.tgz",
      "integrity": "sha512-2Ac2RgzDe/cn48GvOe3M+o82pEFewD3UPbyoUHHdKasHwJKjds4fLXWf/Ux5kATBKN20oaFGu+jbElp1pos0mg==",
      "license": "MIT",
      "dependencies": {
        "@types/json5": "^0.0.29",
        "json5": "^1.0.2",
        "minimist": "^1.2.6",
        "strip-bom": "^3.0.0"
      }
    },
    "node_modules/tsconfig-paths/node_modules/json5": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/json5/-/json5-1.0.2.tgz",
      "integrity": "sha512-g1MWMLBiz8FKi1e4w0UyVL3w+iJceWAFBAaBnnGKOpNa5f8TLktkbre1+s6oICydWAm+HRUGTmI+//xv2hvXYA==",
      "license": "MIT",
      "dependencies": {
        "minimist": "^1.2.0"
      },
      "bin": {
        "json5": "lib/cli.js"
      }
    },
    "node_modules/tsconfig-paths/node_modules/strip-bom": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/strip-bom/-/strip-bom-3.0.0.tgz",
      "integrity": "sha512-vavAMRXOgBVNF6nyEEmL3DBK19iRpDcoIwW+swQ+CbGiu7lju6t+JklA1MHweoWtadgt4ISVUsXLyDq34ddcwA==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/tslib": {
      "version": "2.8.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-2.8.1.tgz",
      "integrity": "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w==",
      "license": "0BSD"
    },
    "node_modules/tsutils": {
      "version": "3.21.0",
      "resolved": "https://registry.npmjs.org/tsutils/-/tsutils-3.21.0.tgz",
      "integrity": "sha512-mHKK3iUXL+3UF6xL5k0PEhKRUBKPBCv/+RkEOpjRWxxx27KKRBmmA60A9pgOUvMi8GKhRMPEmjBRPzs2W7O1OA==",
      "license": "MIT",
      "dependencies": {
        "tslib": "^1.8.1"
      },
      "engines": {
        "node": ">= 6"
      },
      "peerDependencies": {
        "typescript": ">=2.8.0 || >= 3.2.0-dev || >= 3.3.0-dev || >= 3.4.0-dev || >= 3.5.0-dev || >= 3.6.0-dev || >= 3.6.0-beta || >= 3.7.0-dev || >= 3.7.0-beta"
      }
    },
    "node_modules/tsutils/node_modules/tslib": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-1.14.1.tgz",
      "integrity": "sha512-Xni35NKzjgMrwevysHTCArtLDpPvye8zV/0E4EyYn43P7/7qvQwPh9BGkHewbMulVntbigmcT7rdX3BNo9wRJg==",
      "license": "0BSD"
    },
    "node_modules/type-check": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/type-check/-/type-check-0.4.0.tgz",
      "integrity": "sha512-XleUoc9uwGXqjWwXaUTZAmzMcFZ5858QA2vvx1Ur5xIcixXIP+8LnFDgRplU30us6teqdlskFfu+ae4K79Ooew==",
      "license": "MIT",
      "dependencies": {
        "prelude-ls": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/type-detect": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/type-detect/-/type-detect-4.0.8.tgz",
      "integrity": "sha512-0fr/mIH1dlO+x7TlcMy+bIDqKPsw/70tVyeHW787goQjhmqaZe10uwLujubK9q9Lg6Fiho1KUKDYz0Z7k7g5/g==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/type-fest": {
      "version": "0.20.2",
      "resolved": "https://registry.npmjs.org/type-fest/-/type-fest-0.20.2.tgz",
      "integrity": "sha512-Ne+eE4r0/iWnpAxD852z3A+N0Bt5RN//NjJwRd2VFHEmrywxf5vsZlh4R6lixl6B+wz/8d+maTSAkN1FIkI3LQ==",
      "license": "(MIT OR CC0-1.0)",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/type-is": {
      "version": "1.6.18",
      "resolved": "https://registry.npmjs.org/type-is/-/type-is-1.6.18.tgz",
      "integrity": "sha512-TkRKr9sUTxEH8MdfuCSP7VizJyzRNMjj2J2do2Jr3Kym598JVdEksuzPQCnlFPW4ky9Q+iA+ma9BGm06XQBy8g==",
      "license": "MIT",
      "dependencies": {
        "media-typer": "0.3.0",
        "mime-types": "~2.1.24"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/typed-array-buffer": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/typed-array-buffer/-/typed-array-buffer-1.0.3.tgz",
      "integrity": "sha512-nAYYwfY3qnzX30IkA6AQZjVbtK6duGontcQm1WSG1MD94YLqK0515GNApXkoxKOWMusVssAHWLh9SeaoefYFGw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-typed-array": "^1.1.14"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/typed-array-byte-length": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/typed-array-byte-length/-/typed-array-byte-length-1.0.3.tgz",
      "integrity": "sha512-BaXgOuIxz8n8pIq3e7Atg/7s+DpiYrxn4vdot3w9KbnBhcRQq6o3xemQdIfynqSeXeDrF32x+WvfzmOjPiY9lg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "for-each": "^0.3.3",
        "gopd": "^1.2.0",
        "has-proto": "^1.2.0",
        "is-typed-array": "^1.1.14"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typed-array-byte-offset": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/typed-array-byte-offset/-/typed-array-byte-offset-1.0.4.tgz",
      "integrity": "sha512-bTlAFB/FBYMcuX81gbL4OcpH5PmlFHqlCCpAl8AlEzMz5k53oNDvN8p1PNOWLEmI2x4orp3raOFB51tv9X+MFQ==",
      "license": "MIT",
      "dependencies": {
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "for-each": "^0.3.3",
        "gopd": "^1.2.0",
        "has-proto": "^1.2.0",
        "is-typed-array": "^1.1.15",
        "reflect.getprototypeof": "^1.0.9"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typed-array-length": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/typed-array-length/-/typed-array-length-1.0.7.tgz",
      "integrity": "sha512-3KS2b+kL7fsuk/eJZ7EQdnEmQoaho/r6KUef7hxvltNA5DR8NAUM+8wJMbJyZ4G9/7i3v5zPBIMN5aybAh2/Jg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "for-each": "^0.3.3",
        "gopd": "^1.0.1",
        "is-typed-array": "^1.1.13",
        "possible-typed-array-names": "^1.0.0",
        "reflect.getprototypeof": "^1.0.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typedarray-to-buffer": {
      "version": "3.1.5",
      "resolved": "https://registry.npmjs.org/typedarray-to-buffer/-/typedarray-to-buffer-3.1.5.tgz",
      "integrity": "sha512-zdu8XMNEDepKKR+XYOXAVPtWui0ly0NtohUscw+UmaHiAWT8hrV1rr//H6V+0DvJ3OQ19S979M0laLfX8rm82Q==",
      "license": "MIT",
      "dependencies": {
        "is-typedarray": "^1.0.0"
      }
    },
    "node_modules/typescript": {
      "version": "5.9.3",
      "resolved": "https://registry.npmjs.org/typescript/-/typescript-5.9.3.tgz",
      "integrity": "sha512-jl1vZzPDinLr9eUt3J/t7V6FgNEw9QjvBPdysz9KfQDD41fQrC2Y4vKQdiaUpFT4bXlb1RHhLpp8wtm6M5TgSw==",
      "license": "Apache-2.0",
      "peer": true,
      "bin": {
        "tsc": "bin/tsc",
        "tsserver": "bin/tsserver"
      },
      "engines": {
        "node": ">=14.17"
      }
    },
    "node_modules/unbox-primitive": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/unbox-primitive/-/unbox-primitive-1.1.0.tgz",
      "integrity": "sha512-nWJ91DjeOkej/TA8pXQ3myruKpKEYgqvpw9lz4OPHj/NWFNluYrjbz9j01CJ8yKQd2g4jFoOkINCTW2I5LEEyw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-bigints": "^1.0.2",
        "has-symbols": "^1.1.0",
        "which-boxed-primitive": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/underscore": {
      "version": "1.13.6",
      "resolved": "https://registry.npmjs.org/underscore/-/underscore-1.13.6.tgz",
      "integrity": "sha512-+A5Sja4HP1M08MaXya7p5LvjuM7K6q/2EaC0+iovj/wOcMsTzMvDFbasi/oSapiwOlt252IqsKqPjCl7huKS0A==",
      "license": "MIT"
    },
    "node_modules/undici-types": {
      "version": "7.18.2",
      "resolved": "https://registry.npmjs.org/undici-types/-/undici-types-7.18.2.tgz",
      "integrity": "sha512-AsuCzffGHJybSaRrmr5eHr81mwJU3kjw6M+uprWvCXiNeN9SOGwQ3Jn8jb8m3Z6izVgknn1R0FTCEAP2QrLY/w==",
      "license": "MIT"
    },
    "node_modules/unicode-canonical-property-names-ecmascript": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/unicode-canonical-property-names-ecmascript/-/unicode-canonical-property-names-ecmascript-2.0.1.tgz",
      "integrity": "sha512-dA8WbNeb2a6oQzAQ55YlT5vQAWGV9WXOsi3SskE3bcCdM0P4SDd+24zS/OCacdRq5BkdsRj9q3Pg6YyQoxIGqg==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-match-property-ecmascript": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/unicode-match-property-ecmascript/-/unicode-match-property-ecmascript-2.0.0.tgz",
      "integrity": "sha512-5kaZCrbp5mmbz5ulBkDkbY0SsPOjKqVS35VpL9ulMPfSl0J0Xsm+9Evphv9CoIZFwre7aJoa94AY6seMKGVN5Q==",
      "license": "MIT",
      "dependencies": {
        "unicode-canonical-property-names-ecmascript": "^2.0.0",
        "unicode-property-aliases-ecmascript": "^2.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-match-property-value-ecmascript": {
      "version": "2.2.1",
      "resolved": "https://registry.npmjs.org/unicode-match-property-value-ecmascript/-/unicode-match-property-value-ecmascript-2.2.1.tgz",
      "integrity": "sha512-JQ84qTuMg4nVkx8ga4A16a1epI9H6uTXAknqxkGF/aFfRLw1xC/Bp24HNLaZhHSkWd3+84t8iXnp1J0kYcZHhg==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-property-aliases-ecmascript": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/unicode-property-aliases-ecmascript/-/unicode-property-aliases-ecmascript-2.2.0.tgz",
      "integrity": "sha512-hpbDzxUY9BFwX+UeBnxv3Sh1q7HFxj48DTmXchNgRa46lO8uj3/1iEn3MiNUYTg1g9ctIqXCCERn8gYZhHC5lQ==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unique-string": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/unique-string/-/unique-string-2.0.0.tgz",
      "integrity": "sha512-uNaeirEPvpZWSgzwsPGtU2zVSTrn/8L5q/IexZmH0eH6SA73CmAA5U4GwORTxQAZs95TAXLNqeLoPPNO5gZfWg==",
      "license": "MIT",
      "dependencies": {
        "crypto-random-string": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/universalify": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/universalify/-/universalify-2.0.1.tgz",
      "integrity": "sha512-gptHNQghINnc/vTGIk0SOFGFNXw7JVrlRUtConJRlvaw6DuX0wO5Jeko9sWrMBhh+PsYAZ7oXAiOnf/UKogyiw==",
      "license": "MIT",
      "engines": {
        "node": ">= 10.0.0"
      }
    },
    "node_modules/unpipe": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/unpipe/-/unpipe-1.0.0.tgz",
      "integrity": "sha512-pjy2bYhSsufwWlKwPc+l3cN7+wuJlK6uz0YdJEOlQDbl6jo/YlPi4mb8agUkVC8BF7V8NuzeyPNqRksA3hztKQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/unquote": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/unquote/-/unquote-1.1.1.tgz",
      "integrity": "sha512-vRCqFv6UhXpWxZPyGDh/F3ZpNv8/qo7w6iufLpQg9aKnQ71qM4B5KiI7Mia9COcjEhrO9LueHpMYjYzsWH3OIg==",
      "license": "MIT"
    },
    "node_modules/upath": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/upath/-/upath-1.2.0.tgz",
      "integrity": "sha512-aZwGpamFO61g3OlfT7OQCHqhGnW43ieH9WZeP7QxN/G/jS4jfqUkZxoryvJgVPEcrl5NL/ggHsSmLMHuH64Lhg==",
      "license": "MIT",
      "engines": {
        "node": ">=4",
        "yarn": "*"
      }
    },
    "node_modules/update-browserslist-db": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/update-browserslist-db/-/update-browserslist-db-1.2.3.tgz",
      "integrity": "sha512-Js0m9cx+qOgDxo0eMiFGEueWztz+d4+M3rGlmKPT+T4IS/jP4ylw3Nwpu6cpTTP8R1MAC1kF4VbdLt3ARf209w==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "escalade": "^3.2.0",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "update-browserslist-db": "cli.js"
      },
      "peerDependencies": {
        "browserslist": ">= 4.21.0"
      }
    },
    "node_modules/uri-js": {
      "version": "4.4.1",
      "resolved": "https://registry.npmjs.org/uri-js/-/uri-js-4.4.1.tgz",
      "integrity": "sha512-7rKUyy33Q1yc98pQ1DAmLtwX109F7TIfWlW1Ydo8Wl1ii1SeHieeh0HHfPeL2fMXK6z0s8ecKs9frCuLJvndBg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "punycode": "^2.1.0"
      }
    },
    "node_modules/url-parse": {
      "version": "1.5.10",
      "resolved": "https://registry.npmjs.org/url-parse/-/url-parse-1.5.10.tgz",
      "integrity": "sha512-WypcfiRhfeUP9vvF0j6rw0J3hrWrw6iZv3+22h6iRMJ/8z1Tj6XfLP4DsUix5MhMPnXpiHDoKyoZ/bdCkwBCiQ==",
      "license": "MIT",
      "dependencies": {
        "querystringify": "^2.1.1",
        "requires-port": "^1.0.0"
      }
    },
    "node_modules/util-deprecate": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/util-deprecate/-/util-deprecate-1.0.2.tgz",
      "integrity": "sha512-EPD5q1uXyFxJpCrLnCc1nHnq3gOa6DZBocAIiI2TaSCA7VCJ1UJDMagCzIkXNsUYfD1daK//LTEQ8xiIbrHtcw==",
      "license": "MIT"
    },
    "node_modules/util.promisify": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/util.promisify/-/util.promisify-1.0.1.tgz",
      "integrity": "sha512-g9JpC/3He3bm38zsLupWryXHoEcS22YHthuPQSJdMy6KNrzIRzWqcsHzD/WUnqe45whVou4VIsPew37DoXWNrA==",
      "license": "MIT",
      "dependencies": {
        "define-properties": "^1.1.3",
        "es-abstract": "^1.17.2",
        "has-symbols": "^1.0.1",
        "object.getownpropertydescriptors": "^2.1.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/utila": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/utila/-/utila-0.4.0.tgz",
      "integrity": "sha512-Z0DbgELS9/L/75wZbro8xAnT50pBVFQZ+hUEueGDU5FN51YSCYM+jdxsfCiHjwNP/4LCDD0i/graKpeBnOXKRA==",
      "license": "MIT"
    },
    "node_modules/utils-merge": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/utils-merge/-/utils-merge-1.0.1.tgz",
      "integrity": "sha512-pMZTvIkT1d+TFGvDOqodOclx0QWkkgi6Tdoa8gC8ffGAAqz9pzPTZWAybbsHHoED/ztMtkv/VoYTYyShUn81hA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4.0"
      }
    },
    "node_modules/uuid": {
      "version": "8.3.2",
      "resolved": "https://registry.npmjs.org/uuid/-/uuid-8.3.2.tgz",
      "integrity": "sha512-+NYs2QeMWy+GWFOEm9xnn6HCDp0l7QBD7ml8zLUmJ+93Q5NF0NocErnwkTkXVFNiX3/fpC6afS8Dhb/gz7R7eg==",
      "license": "MIT",
      "bin": {
        "uuid": "dist/bin/uuid"
      }
    },
    "node_modules/v8-to-istanbul": {
      "version": "8.1.1",
      "resolved": "https://registry.npmjs.org/v8-to-istanbul/-/v8-to-istanbul-8.1.1.tgz",
      "integrity": "sha512-FGtKtv3xIpR6BYhvgH8MI/y78oT7d8Au3ww4QIxymrCtZEh5b8gCw2siywE+puhEmuWKDtmfrvF5UlB298ut3w==",
      "license": "ISC",
      "dependencies": {
        "@types/istanbul-lib-coverage": "^2.0.1",
        "convert-source-map": "^1.6.0",
        "source-map": "^0.7.3"
      },
      "engines": {
        "node": ">=10.12.0"
      }
    },
    "node_modules/v8-to-istanbul/node_modules/convert-source-map": {
      "version": "1.9.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-1.9.0.tgz",
      "integrity": "sha512-ASFBup0Mz1uyiIjANan1jzLQami9z1PoYSZCiiYW2FczPbenXc45FZdBZLzOT+r6+iciuEModtmCti+hjaAk0A==",
      "license": "MIT"
    },
    "node_modules/vary": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/vary/-/vary-1.1.2.tgz",
      "integrity": "sha512-BNGbWLfd0eUPabhkXUVm0j8uuvREyTh5ovRa/dyow/BqAbZJyC+5fU+IzQOzmAKzYqYRAISoRhdQr3eIZ/PXqg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/w3c-hr-time": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/w3c-hr-time/-/w3c-hr-time-1.0.2.tgz",
      "integrity": "sha512-z8P5DvDNjKDoFIHK7q8r8lackT6l+jo/Ye3HOle7l9nICP9lf1Ci25fy9vHd0JOWewkIFzXIEig3TdKT7JQ5fQ==",
      "deprecated": "Use your platform's native performance.now() and performance.timeOrigin.",
      "license": "MIT",
      "dependencies": {
        "browser-process-hrtime": "^1.0.0"
      }
    },
    "node_modules/w3c-xmlserializer": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/w3c-xmlserializer/-/w3c-xmlserializer-2.0.0.tgz",
      "integrity": "sha512-4tzD0mF8iSiMiNs30BiLO3EpfGLZUT2MSX/G+o7ZywDzliWQ3OPtTZ0PTC3B3ca1UAf4cJMHB+2Bf56EriJuRA==",
      "license": "MIT",
      "dependencies": {
        "xml-name-validator": "^3.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/walker": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/walker/-/walker-1.0.8.tgz",
      "integrity": "sha512-ts/8E8l5b7kY0vlWLewOkDXMmPdLcVV4GmOQLyxuSswIJsweeFZtAsMF7k1Nszz+TYBQrlYRmzOnr398y1JemQ==",
      "license": "Apache-2.0",
      "dependencies": {
        "makeerror": "1.0.12"
      }
    },
    "node_modules/watchpack": {
      "version": "2.5.1",
      "resolved": "https://registry.npmjs.org/watchpack/-/watchpack-2.5.1.tgz",
      "integrity": "sha512-Zn5uXdcFNIA1+1Ei5McRd+iRzfhENPCe7LeABkJtNulSxjma+l7ltNx55BWZkRlwRnpOgHqxnjyaDgJnNXnqzg==",
      "license": "MIT",
      "dependencies": {
        "glob-to-regexp": "^0.4.1",
        "graceful-fs": "^4.1.2"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/wbuf": {
      "version": "1.7.3",
      "resolved": "https://registry.npmjs.org/wbuf/-/wbuf-1.7.3.tgz",
      "integrity": "sha512-O84QOnr0icsbFGLS0O3bI5FswxzRr8/gHwWkDlQFskhSPryQXvrTMxjxGP4+iWYoauLoBvfDpkrOauZ+0iZpDA==",
      "license": "MIT",
      "dependencies": {
        "minimalistic-assert": "^1.0.0"
      }
    },
    "node_modules/webidl-conversions": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/webidl-conversions/-/webidl-conversions-6.1.0.tgz",
      "integrity": "sha512-qBIvFLGiBpLjfwmYAaHPXsn+ho5xZnGvyGvsarywGNc8VyQJUMHJ8OBKGGrPER0okBeMDaan4mNBlgBROxuI8w==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=10.4"
      }
    },
    "node_modules/webpack": {
      "version": "5.105.4",
      "resolved": "https://registry.npmjs.org/webpack/-/webpack-5.105.4.tgz",
      "integrity": "sha512-jTywjboN9aHxFlToqb0K0Zs9SbBoW4zRUlGzI2tYNxVYcEi/IPpn+Xi4ye5jTLvX2YeLuic/IvxNot+Q1jMoOw==",
      "license": "MIT",
      "dependencies": {
        "@types/eslint-scope": "^3.7.7",
        "@types/estree": "^1.0.8",
        "@types/json-schema": "^7.0.15",
        "@webassemblyjs/ast": "^1.14.1",
        "@webassemblyjs/wasm-edit": "^1.14.1",
        "@webassemblyjs/wasm-parser": "^1.14.1",
        "acorn": "^8.16.0",
        "acorn-import-phases": "^1.0.3",
        "browserslist": "^4.28.1",
        "chrome-trace-event": "^1.0.2",
        "enhanced-resolve": "^5.20.0",
        "es-module-lexer": "^2.0.0",
        "eslint-scope": "5.1.1",
        "events": "^3.2.0",
        "glob-to-regexp": "^0.4.1",
        "graceful-fs": "^4.2.11",
        "json-parse-even-better-errors": "^2.3.1",
        "loader-runner": "^4.3.1",
        "mime-types": "^2.1.27",
        "neo-async": "^2.6.2",
        "schema-utils": "^4.3.3",
        "tapable": "^2.3.0",
        "terser-webpack-plugin": "^5.3.17",
        "watchpack": "^2.5.1",
        "webpack-sources": "^3.3.4"
      },
      "bin": {
        "webpack": "bin/webpack.js"
      },
      "engines": {
        "node": ">=10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependenciesMeta": {
        "webpack-cli": {
          "optional": true
        }
      }
    },
    "node_modules/webpack-dev-middleware": {
      "version": "5.3.4",
      "resolved": "https://registry.npmjs.org/webpack-dev-middleware/-/webpack-dev-middleware-5.3.4.tgz",
      "integrity": "sha512-BVdTqhhs+0IfoeAf7EoH5WE+exCmqGerHfDM0IL096Px60Tq2Mn9MAbnaGUe6HiMa41KMCYF19gyzZmBcq/o4Q==",
      "license": "MIT",
      "dependencies": {
        "colorette": "^2.0.10",
        "memfs": "^3.4.3",
        "mime-types": "^2.1.31",
        "range-parser": "^1.2.1",
        "schema-utils": "^4.0.0"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^4.0.0 || ^5.0.0"
      }
    },
    "node_modules/webpack-dev-server": {
      "version": "4.15.2",
      "resolved": "https://registry.npmjs.org/webpack-dev-server/-/webpack-dev-server-4.15.2.tgz",
      "integrity": "sha512-0XavAZbNJ5sDrCbkpWL8mia0o5WPOd2YGtxrEiZkBK9FjLppIUK2TgxK6qGD2P3hUXTJNNPVibrerKcx5WkR1g==",
      "license": "MIT",
      "dependencies": {
        "@types/bonjour": "^3.5.9",
        "@types/connect-history-api-fallback": "^1.3.5",
        "@types/express": "^4.17.13",
        "@types/serve-index": "^1.9.1",
        "@types/serve-static": "^1.13.10",
        "@types/sockjs": "^0.3.33",
        "@types/ws": "^8.5.5",
        "ansi-html-community": "^0.0.8",
        "bonjour-service": "^1.0.11",
        "chokidar": "^3.5.3",
        "colorette": "^2.0.10",
        "compression": "^1.7.4",
        "connect-history-api-fallback": "^2.0.0",
        "default-gateway": "^6.0.3",
        "express": "^4.17.3",
        "graceful-fs": "^4.2.6",
        "html-entities": "^2.3.2",
        "http-proxy-middleware": "^2.0.3",
        "ipaddr.js": "^2.0.1",
        "launch-editor": "^2.6.0",
        "open": "^8.0.9",
        "p-retry": "^4.5.0",
        "rimraf": "^3.0.2",
        "schema-utils": "^4.0.0",
        "selfsigned": "^2.1.1",
        "serve-index": "^1.9.1",
        "sockjs": "^0.3.24",
        "spdy": "^4.0.2",
        "webpack-dev-middleware": "^5.3.4",
        "ws": "^8.13.0"
      },
      "bin": {
        "webpack-dev-server": "bin/webpack-dev-server.js"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^4.37.0 || ^5.0.0"
      },
      "peerDependenciesMeta": {
        "webpack": {
          "optional": true
        },
        "webpack-cli": {
          "optional": true
        }
      }
    },
    "node_modules/webpack-dev-server/node_modules/ws": {
      "version": "8.19.0",
      "resolved": "https://registry.npmjs.org/ws/-/ws-8.19.0.tgz",
      "integrity": "sha512-blAT2mjOEIi0ZzruJfIhb3nps74PRWTCz1IjglWEEpQl5XS/UNama6u2/rjFkDDouqr4L67ry+1aGIALViWjDg==",
      "license": "MIT",
      "engines": {
        "node": ">=10.0.0"
      },
      "peerDependencies": {
        "bufferutil": "^4.0.1",
        "utf-8-validate": ">=5.0.2"
      },
      "peerDependenciesMeta": {
        "bufferutil": {
          "optional": true
        },
        "utf-8-validate": {
          "optional": true
        }
      }
    },
    "node_modules/webpack-manifest-plugin": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/webpack-manifest-plugin/-/webpack-manifest-plugin-4.1.1.tgz",
      "integrity": "sha512-YXUAwxtfKIJIKkhg03MKuiFAD72PlrqCiwdwO4VEXdRO5V0ORCNwaOwAZawPZalCbmH9kBDmXnNeQOw+BIEiow==",
      "license": "MIT",
      "dependencies": {
        "tapable": "^2.0.0",
        "webpack-sources": "^2.2.0"
      },
      "engines": {
        "node": ">=12.22.0"
      },
      "peerDependencies": {
        "webpack": "^4.44.2 || ^5.47.0"
      }
    },
    "node_modules/webpack-manifest-plugin/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/webpack-manifest-plugin/node_modules/webpack-sources": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/webpack-sources/-/webpack-sources-2.3.1.tgz",
      "integrity": "sha512-y9EI9AO42JjEcrTJFOYmVywVZdKVUfOvDUPsJea5GIr1JOEGFVqwlY2K098fFoIjOkDzHn2AjRvM8dsBZu+gCA==",
      "license": "MIT",
      "dependencies": {
        "source-list-map": "^2.0.1",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/webpack-sources": {
      "version": "3.3.4",
      "resolved": "https://registry.npmjs.org/webpack-sources/-/webpack-sources-3.3.4.tgz",
      "integrity": "sha512-7tP1PdV4vF+lYPnkMR0jMY5/la2ub5Fc/8VQrrU+lXkiM6C4TjVfGw7iKfyhnTQOsD+6Q/iKw0eFciziRgD58Q==",
      "license": "MIT",
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/webpack/node_modules/eslint-scope": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-5.1.1.tgz",
      "integrity": "sha512-2NxwbF/hZ0KpepYN0cNbo+FN6XoK7GaHlQhgx/hIZl6Va0bF45RQOOwhLIy8lQDbuCiadSLCBnH2CFYquit5bw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^4.1.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/webpack/node_modules/estraverse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-4.3.0.tgz",
      "integrity": "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/websocket-driver": {
      "version": "0.7.4",
      "resolved": "https://registry.npmjs.org/websocket-driver/-/websocket-driver-0.7.4.tgz",
      "integrity": "sha512-b17KeDIQVjvb0ssuSDF2cYXSg2iztliJ4B9WdsuB6J952qCPKmnVq4DyW5motImXHDC1cBT/1UezrJVsKw5zjg==",
      "license": "Apache-2.0",
      "dependencies": {
        "http-parser-js": ">=0.5.1",
        "safe-buffer": ">=5.1.0",
        "websocket-extensions": ">=0.1.1"
      },
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/websocket-extensions": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/websocket-extensions/-/websocket-extensions-0.1.4.tgz",
      "integrity": "sha512-OqedPIGOfsDlo31UNwYbCFMSaO9m9G/0faIHj5/dZFDMFqPTcx6UwqyOy3COEaEOg/9VsGIpdqn62W5KhoKSpg==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/whatwg-encoding": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/whatwg-encoding/-/whatwg-encoding-1.0.5.tgz",
      "integrity": "sha512-b5lim54JOPN9HtzvK9HFXvBma/rnfFeqsic0hSpjtDbVxR3dJKLc+KB4V6GgiGOvl7CY/KNh8rxSo9DKQrnUEw==",
      "deprecated": "Use @exodus/bytes instead for a more spec-conformant and faster implementation",
      "license": "MIT",
      "dependencies": {
        "iconv-lite": "0.4.24"
      }
    },
    "node_modules/whatwg-encoding/node_modules/iconv-lite": {
      "version": "0.4.24",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.4.24.tgz",
      "integrity": "sha512-v3MXnZAcvnywkTUEZomIActle7RXXeedOR31wwl7VlyoXO4Qi9arvSenNQWne1TcRwhCL1HwLI21bEqdpj8/rA==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/whatwg-fetch": {
      "version": "3.6.20",
      "resolved": "https://registry.npmjs.org/whatwg-fetch/-/whatwg-fetch-3.6.20.tgz",
      "integrity": "sha512-EqhiFU6daOA8kpjOWTL0olhVOF3i7OrFzSYiGsEMB8GcXS+RrzauAERX65xMeNWVqxA6HXH2m69Z9LaKKdisfg==",
      "license": "MIT"
    },
    "node_modules/whatwg-mimetype": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/whatwg-mimetype/-/whatwg-mimetype-2.3.0.tgz",
      "integrity": "sha512-M4yMwr6mAnQz76TbJm914+gPpB/nCwvZbJU28cUD6dR004SAxDLOOSUaB1JDRqLtaOV/vi0IC5lEAGFgrjGv/g==",
      "license": "MIT"
    },
    "node_modules/whatwg-url": {
      "version": "8.7.0",
      "resolved": "https://registry.npmjs.org/whatwg-url/-/whatwg-url-8.7.0.tgz",
      "integrity": "sha512-gAojqb/m9Q8a5IV96E3fHJM70AzCkgt4uXYX2O7EmuyOnLrViCQlsEBmF9UQIu3/aeAIp2U17rtbpZWNntQqdg==",
      "license": "MIT",
      "dependencies": {
        "lodash": "^4.7.0",
        "tr46": "^2.1.0",
        "webidl-conversions": "^6.1.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/which": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/which/-/which-2.0.2.tgz",
      "integrity": "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA==",
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "node-which": "bin/node-which"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/which-boxed-primitive": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/which-boxed-primitive/-/which-boxed-primitive-1.1.1.tgz",
      "integrity": "sha512-TbX3mj8n0odCBFVlY8AxkqcHASw3L60jIuF8jFP78az3C2YhmGvqbHBpAjTRH2/xqYunrJ9g1jSyjCjpoWzIAA==",
      "license": "MIT",
      "dependencies": {
        "is-bigint": "^1.1.0",
        "is-boolean-object": "^1.2.1",
        "is-number-object": "^1.1.1",
        "is-string": "^1.1.1",
        "is-symbol": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-builtin-type": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/which-builtin-type/-/which-builtin-type-1.2.1.tgz",
      "integrity": "sha512-6iBczoX+kDQ7a3+YJBnh3T+KZRxM/iYNPXicqk66/Qfm1b93iu+yOImkg0zHbj5LNOcNv1TEADiZ0xa34B4q6Q==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "function.prototype.name": "^1.1.6",
        "has-tostringtag": "^1.0.2",
        "is-async-function": "^2.0.0",
        "is-date-object": "^1.1.0",
        "is-finalizationregistry": "^1.1.0",
        "is-generator-function": "^1.0.10",
        "is-regex": "^1.2.1",
        "is-weakref": "^1.0.2",
        "isarray": "^2.0.5",
        "which-boxed-primitive": "^1.1.0",
        "which-collection": "^1.0.2",
        "which-typed-array": "^1.1.16"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-collection": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/which-collection/-/which-collection-1.0.2.tgz",
      "integrity": "sha512-K4jVyjnBdgvc86Y6BkaLZEN933SwYOuBFkdmBu9ZfkcAbdVbpITnDmjvZ/aQjRXQrv5EPkTnD1s39GiiqbngCw==",
      "license": "MIT",
      "dependencies": {
        "is-map": "^2.0.3",
        "is-set": "^2.0.3",
        "is-weakmap": "^2.0.2",
        "is-weakset": "^2.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-typed-array": {
      "version": "1.1.20",
      "resolved": "https://registry.npmjs.org/which-typed-array/-/which-typed-array-1.1.20.tgz",
      "integrity": "sha512-LYfpUkmqwl0h9A2HL09Mms427Q1RZWuOHsukfVcKRq9q95iQxdw0ix1JQrqbcDR9PH1QDwf5Qo8OZb5lksZ8Xg==",
      "license": "MIT",
      "dependencies": {
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "for-each": "^0.3.5",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/word-wrap": {
      "version": "1.2.5",
      "resolved": "https://registry.npmjs.org/word-wrap/-/word-wrap-1.2.5.tgz",
      "integrity": "sha512-BN22B5eaMMI9UMtjrGd5g5eCYPpCPDUy0FJXbYsaT5zYxjFOckS53SQDE3pWkVoWpHXVb3BrYcEN4Twa55B5cA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/workbox-background-sync": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-background-sync/-/workbox-background-sync-6.6.0.tgz",
      "integrity": "sha512-jkf4ZdgOJxC9u2vztxLuPT/UjlH7m/nWRQ/MgGL0v8BJHoZdVGJd18Kck+a0e55wGXdqyHO+4IQTk0685g4MUw==",
      "license": "MIT",
      "dependencies": {
        "idb": "^7.0.1",
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-broadcast-update": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-broadcast-update/-/workbox-broadcast-update-6.6.0.tgz",
      "integrity": "sha512-nm+v6QmrIFaB/yokJmQ/93qIJ7n72NICxIwQwe5xsZiV2aI93MGGyEyzOzDPVz5THEr5rC3FJSsO3346cId64Q==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-build": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-build/-/workbox-build-6.6.0.tgz",
      "integrity": "sha512-Tjf+gBwOTuGyZwMz2Nk/B13Fuyeo0Q84W++bebbVsfr9iLkDSo6j6PST8tET9HYA58mlRXwlMGpyWO8ETJiXdQ==",
      "license": "MIT",
      "dependencies": {
        "@apideck/better-ajv-errors": "^0.3.1",
        "@babel/core": "^7.11.1",
        "@babel/preset-env": "^7.11.0",
        "@babel/runtime": "^7.11.2",
        "@rollup/plugin-babel": "^5.2.0",
        "@rollup/plugin-node-resolve": "^11.2.1",
        "@rollup/plugin-replace": "^2.4.1",
        "@surma/rollup-plugin-off-main-thread": "^2.2.3",
        "ajv": "^8.6.0",
        "common-tags": "^1.8.0",
        "fast-json-stable-stringify": "^2.1.0",
        "fs-extra": "^9.0.1",
        "glob": "^7.1.6",
        "lodash": "^4.17.20",
        "pretty-bytes": "^5.3.0",
        "rollup": "^2.43.1",
        "rollup-plugin-terser": "^7.0.0",
        "source-map": "^0.8.0-beta.0",
        "stringify-object": "^3.3.0",
        "strip-comments": "^2.0.1",
        "tempy": "^0.6.0",
        "upath": "^1.2.0",
        "workbox-background-sync": "6.6.0",
        "workbox-broadcast-update": "6.6.0",
        "workbox-cacheable-response": "6.6.0",
        "workbox-core": "6.6.0",
        "workbox-expiration": "6.6.0",
        "workbox-google-analytics": "6.6.0",
        "workbox-navigation-preload": "6.6.0",
        "workbox-precaching": "6.6.0",
        "workbox-range-requests": "6.6.0",
        "workbox-recipes": "6.6.0",
        "workbox-routing": "6.6.0",
        "workbox-strategies": "6.6.0",
        "workbox-streams": "6.6.0",
        "workbox-sw": "6.6.0",
        "workbox-window": "6.6.0"
      },
      "engines": {
        "node": ">=10.0.0"
      }
    },
    "node_modules/workbox-build/node_modules/@apideck/better-ajv-errors": {
      "version": "0.3.6",
      "resolved": "https://registry.npmjs.org/@apideck/better-ajv-errors/-/better-ajv-errors-0.3.6.tgz",
      "integrity": "sha512-P+ZygBLZtkp0qqOAJJVX4oX/sFo5JR3eBWwwuqHHhK0GIgQOKWrAfiAaWX0aArHkRWHMuggFEgAZNxVPwPZYaA==",
      "license": "MIT",
      "dependencies": {
        "json-schema": "^0.4.0",
        "jsonpointer": "^5.0.0",
        "leven": "^3.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "ajv": ">=8"
      }
    },
    "node_modules/workbox-build/node_modules/ajv": {
      "version": "8.18.0",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-8.18.0.tgz",
      "integrity": "sha512-PlXPeEWMXMZ7sPYOHqmDyCJzcfNrUr3fGNKtezX14ykXOEIvyK81d+qydx89KY5O71FKMPaQ2vBfBFI5NHR63A==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "fast-uri": "^3.0.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/workbox-build/node_modules/fs-extra": {
      "version": "9.1.0",
      "resolved": "https://registry.npmjs.org/fs-extra/-/fs-extra-9.1.0.tgz",
      "integrity": "sha512-hcg3ZmepS30/7BSFqRvoo3DOMQu7IjqxO5nCDt+zM9XWjb33Wg7ziNT+Qvqbuc3+gWpzO02JubVyk2G4Zvo1OQ==",
      "license": "MIT",
      "dependencies": {
        "at-least-node": "^1.0.0",
        "graceful-fs": "^4.2.0",
        "jsonfile": "^6.0.1",
        "universalify": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/workbox-build/node_modules/json-schema-traverse": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-1.0.0.tgz",
      "integrity": "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug==",
      "license": "MIT"
    },
    "node_modules/workbox-build/node_modules/source-map": {
      "version": "0.8.0-beta.0",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.8.0-beta.0.tgz",
      "integrity": "sha512-2ymg6oRBpebeZi9UUNsgQ89bhx01TcTkmNTGnNO88imTmbSgy4nfujrgVEFKWpMTEGA11EDkTt7mqObTPdigIA==",
      "deprecated": "The work that was done in this beta branch won't be included in future versions",
      "license": "BSD-3-Clause",
      "dependencies": {
        "whatwg-url": "^7.0.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/workbox-build/node_modules/tr46": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/tr46/-/tr46-1.0.1.tgz",
      "integrity": "sha512-dTpowEjclQ7Kgx5SdBkqRzVhERQXov8/l9Ft9dVM9fmg0W0KQSVaXX9T4i6twCPNtYiZM53lpSSUAwJbFPOHxA==",
      "license": "MIT",
      "dependencies": {
        "punycode": "^2.1.0"
      }
    },
    "node_modules/workbox-build/node_modules/webidl-conversions": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/webidl-conversions/-/webidl-conversions-4.0.2.tgz",
      "integrity": "sha512-YQ+BmxuTgd6UXZW3+ICGfyqRyHXVlD5GtQr5+qjiNW7bF0cqrzX500HVXPBOvgXb5YnzDd+h0zqyv61KUD7+Sg==",
      "license": "BSD-2-Clause"
    },
    "node_modules/workbox-build/node_modules/whatwg-url": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/whatwg-url/-/whatwg-url-7.1.0.tgz",
      "integrity": "sha512-WUu7Rg1DroM7oQvGWfOiAK21n74Gg+T4elXEQYkOhtyLeWiJFoOGLXPKI/9gzIie9CtwVLm8wtw6YJdKyxSjeg==",
      "license": "MIT",
      "dependencies": {
        "lodash.sortby": "^4.7.0",
        "tr46": "^1.0.1",
        "webidl-conversions": "^4.0.2"
      }
    },
    "node_modules/workbox-cacheable-response": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-cacheable-response/-/workbox-cacheable-response-6.6.0.tgz",
      "integrity": "sha512-JfhJUSQDwsF1Xv3EV1vWzSsCOZn4mQ38bWEBR3LdvOxSPgB65gAM6cS2CX8rkkKHRgiLrN7Wxoyu+TuH67kHrw==",
      "deprecated": "workbox-background-sync@6.6.0",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-core": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-core/-/workbox-core-6.6.0.tgz",
      "integrity": "sha512-GDtFRF7Yg3DD859PMbPAYPeJyg5gJYXuBQAC+wyrWuuXgpfoOrIQIvFRZnQ7+czTIQjIr1DhLEGFzZanAT/3bQ==",
      "license": "MIT"
    },
    "node_modules/workbox-expiration": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-expiration/-/workbox-expiration-6.6.0.tgz",
      "integrity": "sha512-baplYXcDHbe8vAo7GYvyAmlS4f6998Jff513L4XvlzAOxcl8F620O91guoJ5EOf5qeXG4cGdNZHkkVAPouFCpw==",
      "license": "MIT",
      "dependencies": {
        "idb": "^7.0.1",
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-google-analytics": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-google-analytics/-/workbox-google-analytics-6.6.0.tgz",
      "integrity": "sha512-p4DJa6OldXWd6M9zRl0H6vB9lkrmqYFkRQ2xEiNdBFp9U0LhsGO7hsBscVEyH9H2/3eZZt8c97NB2FD9U2NJ+Q==",
      "deprecated": "It is not compatible with newer versions of GA starting with v4, as long as you are using GAv3 it should be ok, but the package is not longer being maintained",
      "license": "MIT",
      "dependencies": {
        "workbox-background-sync": "6.6.0",
        "workbox-core": "6.6.0",
        "workbox-routing": "6.6.0",
        "workbox-strategies": "6.6.0"
      }
    },
    "node_modules/workbox-navigation-preload": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-navigation-preload/-/workbox-navigation-preload-6.6.0.tgz",
      "integrity": "sha512-utNEWG+uOfXdaZmvhshrh7KzhDu/1iMHyQOV6Aqup8Mm78D286ugu5k9MFD9SzBT5TcwgwSORVvInaXWbvKz9Q==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-precaching": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-precaching/-/workbox-precaching-6.6.0.tgz",
      "integrity": "sha512-eYu/7MqtRZN1IDttl/UQcSZFkHP7dnvr/X3Vn6Iw6OsPMruQHiVjjomDFCNtd8k2RdjLs0xiz9nq+t3YVBcWPw==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0",
        "workbox-routing": "6.6.0",
        "workbox-strategies": "6.6.0"
      }
    },
    "node_modules/workbox-range-requests": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-range-requests/-/workbox-range-requests-6.6.0.tgz",
      "integrity": "sha512-V3aICz5fLGq5DpSYEU8LxeXvsT//mRWzKrfBOIxzIdQnV/Wj7R+LyJVTczi4CQ4NwKhAaBVaSujI1cEjXW+hTw==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-recipes": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-recipes/-/workbox-recipes-6.6.0.tgz",
      "integrity": "sha512-TFi3kTgYw73t5tg73yPVqQC8QQjxJSeqjXRO4ouE/CeypmP2O/xqmB/ZFBBQazLTPxILUQ0b8aeh0IuxVn9a6A==",
      "license": "MIT",
      "dependencies": {
        "workbox-cacheable-response": "6.6.0",
        "workbox-core": "6.6.0",
        "workbox-expiration": "6.6.0",
        "workbox-precaching": "6.6.0",
        "workbox-routing": "6.6.0",
        "workbox-strategies": "6.6.0"
      }
    },
    "node_modules/workbox-routing": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-routing/-/workbox-routing-6.6.0.tgz",
      "integrity": "sha512-x8gdN7VDBiLC03izAZRfU+WKUXJnbqt6PG9Uh0XuPRzJPpZGLKce/FkOX95dWHRpOHWLEq8RXzjW0O+POSkKvw==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-strategies": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-strategies/-/workbox-strategies-6.6.0.tgz",
      "integrity": "sha512-eC07XGuINAKUWDnZeIPdRdVja4JQtTuc35TZ8SwMb1ztjp7Ddq2CJ4yqLvWzFWGlYI7CG/YGqaETntTxBGdKgQ==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-streams": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-streams/-/workbox-streams-6.6.0.tgz",
      "integrity": "sha512-rfMJLVvwuED09CnH1RnIep7L9+mj4ufkTyDPVaXPKlhi9+0czCu+SJggWCIFbPpJaAZmp2iyVGLqS3RUmY3fxg==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0",
        "workbox-routing": "6.6.0"
      }
    },
    "node_modules/workbox-sw": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-sw/-/workbox-sw-6.6.0.tgz",
      "integrity": "sha512-R2IkwDokbtHUE4Kus8pKO5+VkPHD2oqTgl+XJwh4zbF1HyjAbgNmK/FneZHVU7p03XUt9ICfuGDYISWG9qV/CQ==",
      "license": "MIT"
    },
    "node_modules/workbox-webpack-plugin": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-webpack-plugin/-/workbox-webpack-plugin-6.6.0.tgz",
      "integrity": "sha512-xNZIZHalboZU66Wa7x1YkjIqEy1gTR+zPM+kjrYJzqN7iurYZBctBLISyScjhkJKYuRrZUP0iqViZTh8rS0+3A==",
      "license": "MIT",
      "dependencies": {
        "fast-json-stable-stringify": "^2.1.0",
        "pretty-bytes": "^5.4.1",
        "upath": "^1.2.0",
        "webpack-sources": "^1.4.3",
        "workbox-build": "6.6.0"
      },
      "engines": {
        "node": ">=10.0.0"
      },
      "peerDependencies": {
        "webpack": "^4.4.0 || ^5.9.0"
      }
    },
    "node_modules/workbox-webpack-plugin/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/workbox-webpack-plugin/node_modules/webpack-sources": {
      "version": "1.4.3",
      "resolved": "https://registry.npmjs.org/webpack-sources/-/webpack-sources-1.4.3.tgz",
      "integrity": "sha512-lgTS3Xhv1lCOKo7SA5TjKXMjpSM4sBjNV5+q2bqesbSPs5FjGmU6jjtBSkX9b4qW87vDIsCIlUPOEhbZrMdjeQ==",
      "license": "MIT",
      "dependencies": {
        "source-list-map": "^2.0.0",
        "source-map": "~0.6.1"
      }
    },
    "node_modules/workbox-window": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-window/-/workbox-window-6.6.0.tgz",
      "integrity": "sha512-L4N9+vka17d16geaJXXRjENLFldvkWy7JyGxElRD0JvBxvFEd8LOhr+uXCcar/NzAmIBRv9EZ+M+Qr4mOoBITw==",
      "license": "MIT",
      "dependencies": {
        "@types/trusted-types": "^2.0.2",
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/wrap-ansi": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/wrap-ansi/-/wrap-ansi-7.0.0.tgz",
      "integrity": "sha512-YVGIj2kamLSTxw6NsZjoBxfSwsn0ycdesmc4p+Q21c5zPuZ1pl+NfxVdxPtdHvmNVOQ6XSYG4AUtyt/Fi7D16Q==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^4.0.0",
        "string-width": "^4.1.0",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/wrap-ansi?sponsor=1"
      }
    },
    "node_modules/wrappy": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz",
      "integrity": "sha512-l4Sp/DRseor9wL6EvV2+TuQn63dMkPjZ/sp9XkghTEbV9KlPS1xUsZ3u7/IQO4wxtcFB4bgpQPRcR3QCvezPcQ==",
      "license": "ISC"
    },
    "node_modules/write-file-atomic": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/write-file-atomic/-/write-file-atomic-3.0.3.tgz",
      "integrity": "sha512-AvHcyZ5JnSfq3ioSyjrBkH9yW4m7Ayk8/9My/DD9onKeu/94fwrMocemO2QAJFAlnnDN+ZDS+ZjAR5ua1/PV/Q==",
      "license": "ISC",
      "dependencies": {
        "imurmurhash": "^0.1.4",
        "is-typedarray": "^1.0.0",
        "signal-exit": "^3.0.2",
        "typedarray-to-buffer": "^3.1.5"
      }
    },
    "node_modules/ws": {
      "version": "7.5.10",
      "resolved": "https://registry.npmjs.org/ws/-/ws-7.5.10.tgz",
      "integrity": "sha512-+dbF1tHwZpXcbOJdVOkzLDxZP1ailvSxM6ZweXTegylPny803bFhA+vqBYw4s31NSAk4S2Qz+AKXK9a4wkdjcQ==",
      "license": "MIT",
      "engines": {
        "node": ">=8.3.0"
      },
      "peerDependencies": {
        "bufferutil": "^4.0.1",
        "utf-8-validate": "^5.0.2"
      },
      "peerDependenciesMeta": {
        "bufferutil": {
          "optional": true
        },
        "utf-8-validate": {
          "optional": true
        }
      }
    },
    "node_modules/xml-name-validator": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/xml-name-validator/-/xml-name-validator-3.0.0.tgz",
      "integrity": "sha512-A5CUptxDsvxKJEU3yO6DuWBSJz/qizqzJKOMIfUJHETbBw/sFaDxgd6fxm1ewUaM0jZ444Fc5vC5ROYurg/4Pw==",
      "license": "Apache-2.0"
    },
    "node_modules/xmlchars": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/xmlchars/-/xmlchars-2.2.0.tgz",
      "integrity": "sha512-JZnDKK8B0RCDw84FNdDAIpZK+JuJw+s7Lz8nksI7SIuU3UXJJslUthsi+uWBUYOwPFwW7W7PRLRfUKpxjtjFCw==",
      "license": "MIT"
    },
    "node_modules/y18n": {
      "version": "5.0.8",
      "resolved": "https://registry.npmjs.org/y18n/-/y18n-5.0.8.tgz",
      "integrity": "sha512-0pfFzegeDWJHJIAmTLRP2DwHjdF5s7jo9tuztdQxAhINCdvS+3nGINqPd00AphqJR/0LhANUS6/+7SCb98YOfA==",
      "license": "ISC",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/yallist": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/yallist/-/yallist-3.1.1.tgz",
      "integrity": "sha512-a4UGQaWPH59mOXUYnAG2ewncQS4i4F43Tv3JoAM+s2VDAmS9NsK8GpDMLrCHPksFT7h3K6TOoUNn2pb7RoXx4g==",
      "license": "ISC"
    },
    "node_modules/yaml": {
      "version": "1.10.2",
      "resolved": "https://registry.npmjs.org/yaml/-/yaml-1.10.2.tgz",
      "integrity": "sha512-r3vXyErRCYJ7wg28yvBY5VSoAF8ZvlcW9/BwUzEtUsjvX/DKs24dIkuwjtuprwJJHsbyUbLApepYTR1BN4uHrg==",
      "license": "ISC",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/yargs": {
      "version": "16.2.0",
      "resolved": "https://registry.npmjs.org/yargs/-/yargs-16.2.0.tgz",
      "integrity": "sha512-D1mvvtDG0L5ft/jGWkLpG1+m0eQxOfaBvTNELraWj22wSVUMWxZUvYgJYcKh6jGGIkJFhH4IZPQhR4TKpc8mBw==",
      "license": "MIT",
      "dependencies": {
        "cliui": "^7.0.2",
        "escalade": "^3.1.1",
        "get-caller-file": "^2.0.5",
        "require-directory": "^2.1.1",
        "string-width": "^4.2.0",
        "y18n": "^5.0.5",
        "yargs-parser": "^20.2.2"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/yargs-parser": {
      "version": "20.2.9",
      "resolved": "https://registry.npmjs.org/yargs-parser/-/yargs-parser-20.2.9.tgz",
      "integrity": "sha512-y11nGElTIV+CT3Zv9t7VKl+Q3hTQoT9a1Qzezhhl6Rp21gJ/IVTW7Z3y9EWXhuUBC2Shnf+DX0antecpAwSP8w==",
      "license": "ISC",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/yocto-queue": {
      "version": "0.1.0",
      "resolved": "https://registry.npmjs.org/yocto-queue/-/yocto-queue-0.1.0.tgz",
      "integrity": "sha512-rVksvsnNCdJ/ohGc6xgPwyN8eheCxsiLM8mxuE/t/mOVqJewPuO1miLpTHQiRgTKCLexL4MeAFVagts7HmNZ2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    }
  }
}

```


## File: miniapp\frontend\package.json
```json
{
  "name": "auction-miniapp",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  },
  "proxy": "http://localhost:8000",
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version"]
  }
}

```


## File: miniapp\frontend\public\index.html
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <meta name="theme-color" content="#0c0c10" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <title>Аукционы</title>
  <!-- Telegram WebApp SDK -->
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
  window.Telegram = {
    WebApp: {
      initData: "",
      initDataUnsafe: { user: { id: 0, username: "dev_user", first_name: "Dev" } },
      ready: () => {},
      expand: () => {},
      close: () => {},
      setHeaderColor: () => {},
      setBackgroundColor: () => {},
      colorScheme: "dark",
      themeParams: {},
      MainButton: {
        text: "",
        show: () => {},
        hide: () => {},
        setText: () => {},
        onClick: () => {},
        offClick: () => {},
      },
      BackButton: {
        show: () => {},
        hide: () => {},
        onClick: () => {},
        offClick: () => {},
      },
      HapticFeedback: {
        impactOccurred: () => {},
        notificationOccurred: () => {},
      },
    }
  };
</script>
</head>
<body>
  <div id="root"></div>
</body>
</html>

```


## File: miniapp\frontend\src\index.css
```css
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;700;900&family=Golos+Text:wght@400;500;600;700&display=swap');

/* ── CSS Variables ── */
:root {
  --bg:      #0c0c10;
  --s1:      #14141a;
  --s2:      #1c1c24;
  --s3:      #22222c;
  --border:  rgba(255,255,255,0.07);
  --border2: rgba(255,255,255,0.13);
  --gold:    #e8b84b;
  --gold2:   #c97a20;
  --green:   #36cc7a;
  --red:     #ff4757;
  --blue:    #5b9cf6;
  --text:    #eeeef5;
  --text2:   #9090a8;
  --muted:   #55556a;
  --r:       14px;
  --r2:      10px;
}

/* ── Reset ── */
*, *::before, *::after {
  margin: 0; padding: 0; box-sizing: border-box;
  -webkit-tap-highlight-color: transparent;
}

html, body, #root {
  height: 100%; width: 100%;
  background: var(--bg);
  color: var(--text);
  font-family: 'Golos Text', sans-serif;
  font-size: 14px;
  overscroll-behavior: none;
}

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; }
input[type=number] { -moz-appearance: textfield; }

/* ── App shell ── */
.app {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--bg);
}

/* ── Status bar ── */
.status {
  height: 44px; padding: 0 20px 8px;
  display: flex; align-items: flex-end; justify-content: space-between;
  flex-shrink: 0;
}
.s-time { font-size: 15px; font-weight: 700; color: var(--text); }
.s-icons { display: flex; gap: 5px; align-items: center; color: var(--text2); }

/* ── TG header bar ── */
.tg-bar {
  background: var(--s1);
  border-bottom: 1px solid var(--border);
  padding: 8px 16px 12px;
  display: flex; align-items: center; gap: 12px;
  flex-shrink: 0;
}
.tg-back {
  width: 32px; height: 32px; border: none; background: none;
  color: var(--gold); font-size: 24px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%; transition: background 0.15s; flex-shrink: 0;
}
.tg-back:active { background: rgba(255,255,255,0.06); }
.tg-info { flex: 1; min-width: 0; }
.tg-title { font-size: 16px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tg-sub { font-size: 11px; font-weight: 500; }
.tg-sub.online { color: var(--green); }
.tg-sub.done   { color: var(--muted); }
.tg-ava {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, var(--gold), var(--gold2));
  display: flex; align-items: center; justify-content: center;
  font-size: 17px; flex-shrink: 0;
}

/* ── Screen sliding ── */
.screens {
  flex: 1; position: relative; overflow: hidden;
}
.screen-pane {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  transition: transform 0.3s cubic-bezier(.4,0,.2,1), opacity 0.3s;
  background: var(--bg);
  will-change: transform;
}
.screen-pane.slide-out {
  transform: translateX(-40px);
  opacity: 0.35;
  pointer-events: none;
}
.detail-pane {
  transform: translateX(100%);
  opacity: 0;
  pointer-events: none;
}
.detail-pane.slide-in {
  transform: translateX(0);
  opacity: 1;
  pointer-events: auto;
}

/* ── Segment control ── */
.seg-wrap { padding: 12px 16px 0; background: var(--bg); flex-shrink: 0; }
.seg {
  display: flex; background: var(--s2);
  border-radius: 12px; padding: 3px; position: relative;
}
.seg-pill {
  position: absolute; top: 3px; left: 3px;
  height: calc(100% - 6px);
  background: var(--gold); border-radius: 9px;
  transition: transform 0.25s cubic-bezier(.4,0,.2,1), width 0.25s;
  z-index: 0; pointer-events: none;
}
.seg-btn {
  flex: 1; padding: 9px 4px; text-align: center;
  font-size: 12px; font-weight: 700; letter-spacing: 0.3px;
  color: var(--text2); cursor: pointer; border-radius: 10px;
  transition: color 0.2s; position: relative; z-index: 1;
  border: none; background: none; font-family: 'Golos Text', sans-serif;
}
.seg-btn.active { color: #0c0c10; }

/* ── Scroll area ── */
.scroll {
  flex: 1; overflow-y: auto; overflow-x: hidden;
  padding: 14px 16px 24px;
  scroll-behavior: smooth;
}
.scroll::-webkit-scrollbar { display: none; }

/* ── Section header ── */
.sec-head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.sec-lbl {
  font-size: 11px; font-weight: 700;
  letter-spacing: 1.2px; text-transform: uppercase; color: var(--muted);
}
.live-pill {
  display: inline-flex; align-items: center; gap: 4px;
  background: rgba(255,71,87,0.13); border: 1px solid rgba(255,71,87,0.28);
  border-radius: 20px; padding: 2px 8px;
  font-size: 10px; font-weight: 800; color: var(--red); letter-spacing: 0.8px;
}
.live-dot {
  width: 5px; height: 5px; border-radius: 50%;
  background: var(--red); animation: blink 1.1s infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.2;} }

/* ── Lot card (compact) ── */
.lot-card {
  background: var(--s1); border: 1px solid var(--border);
  border-radius: var(--r);
  display: flex; gap: 12px; align-items: center;
  padding: 12px 14px; margin-bottom: 8px;
  cursor: pointer;
  transition: transform 0.15s, background 0.15s;
  position: relative; overflow: hidden;
}
.lot-card:active { transform: scale(0.983); background: var(--s2); }

.c-emoji { font-size: 30px; line-height: 1; width: 42px; text-align: center; flex-shrink: 0; }
.c-info  { flex: 1; min-width: 0; }
.c-code  {
  font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
  color: var(--muted); margin-bottom: 2px; font-family: 'Unbounded', sans-serif;
}
.c-title {
  font-size: 13px; font-weight: 600; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 5px;
}
.c-meta { display: flex; gap: 7px; align-items: center; flex-wrap: wrap; }
.meta-t { font-size: 11px; color: var(--text2); }
.c-right { text-align: right; flex-shrink: 0; }
.c-price {
  font-family: 'Unbounded', sans-serif;
  font-size: 14px; font-weight: 700;
  white-space: nowrap; margin-bottom: 4px;
}
.c-timer { font-size: 11px; font-weight: 700; color: var(--text2); }
.c-timer.end { color: var(--red); }

.chip {
  display: inline-block; padding: 2px 7px;
  border-radius: 20px; font-size: 10px; font-weight: 700;
}
.chip.leading { background: rgba(54,204,122,0.15); color: var(--green); }
.chip.outbid  { background: rgba(255,71,87,0.13);  color: var(--red);   }
.chip.won     { background: rgba(54,204,122,0.15); color: var(--green); }
.chip.lost    { background: rgba(255,71,87,0.1);   color: var(--red);   }

/* ── Empty state ── */
.empty {
  display: flex; flex-direction: column; align-items: center;
  padding: 60px 24px; gap: 12px; text-align: center;
}
.empty-ico { font-size: 44px; opacity: 0.4; }
.empty-ttl { font-family: 'Unbounded', sans-serif; font-size: 13px; font-weight: 700; color: var(--text2); }
.empty-sub { font-size: 12px; color: var(--muted); line-height: 1.5; }

/* ── Detail screen ── */
.detail-scroll {
  flex: 1; overflow-y: auto; overflow-x: hidden;
  padding-bottom: 24px; scroll-behavior: smooth;
}
.detail-scroll::-webkit-scrollbar { display: none; }

.hero {
  width: 100%; height: 220px; position: relative;
  background: linear-gradient(135deg, #18181f 0%, #24243a 50%, #18181f 100%);
  display: flex; align-items: center; justify-content: center;
  font-size: 86px; overflow: hidden; flex-shrink: 0;
}
.hero::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(to bottom, transparent 40%, rgba(12,12,16,0.97));
  z-index: 1;
}
.hero-badges { position: absolute; top: 14px; left: 14px; z-index: 3; display: flex; gap: 6px; }
.hero-timer  { position: absolute; bottom: 14px; right: 14px; z-index: 3; }
.hero-timer-val {
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(0,0,0,0.6); backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px; padding: 4px 12px;
  font-size: 13px; font-weight: 700; color: white;
}
.hero-timer-val.end { color: var(--red); border-color: rgba(255,71,87,0.4); }

.d-body { padding: 16px 16px 0; }
.d-code {
  font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
  color: var(--muted); margin-bottom: 5px; font-family: 'Unbounded', sans-serif;
}
.d-title {
  font-family: 'Unbounded', sans-serif;
  font-size: 17px; font-weight: 700; color: var(--text);
  line-height: 1.25; margin-bottom: 12px;
}
.d-desc {
  font-size: 13px; color: var(--text2); line-height: 1.65;
  margin-bottom: 16px; padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.stats3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 16px; }
.s3-box {
  background: var(--s2); border: 1px solid var(--border);
  border-radius: var(--r2); padding: 11px 8px; text-align: center;
}
.s3-val {
  font-family: 'Unbounded', sans-serif;
  font-size: 15px; font-weight: 700; color: var(--text);
  line-height: 1; margin-bottom: 4px;
}
.s3-val.gold { color: var(--gold); }
.s3-val.red  { color: var(--red);  }
.s3-lbl { font-size: 10px; color: var(--muted); font-weight: 600; letter-spacing: 0.3px; }

.my-bar {
  border-radius: var(--r2); padding: 11px 14px;
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 16px; border: 1px solid;
}
.my-bar.leading { background: rgba(54,204,122,0.07); border-color: rgba(54,204,122,0.22); }
.my-bar.outbid  { background: rgba(255,71,87,0.07);  border-color: rgba(255,71,87,0.22);  }
.my-bar.won     { background: rgba(54,204,122,0.07); border-color: rgba(54,204,122,0.22); }
.my-bar.lost    { background: rgba(255,71,87,0.07);  border-color: rgba(255,71,87,0.22);  }
.my-bar-icon { font-size: 18px; }
.my-bar-text { flex: 1; font-size: 12px; color: var(--text2); }
.my-bar-val  { font-family: 'Unbounded', sans-serif; font-size: 13px; font-weight: 700; }
.my-bar-val.green { color: var(--green); }
.my-bar-val.red   { color: var(--red);   }

.bid-cta-wrap { padding: 0 16px 20px; }
.bid-cta {
  width: 100%;
  background: linear-gradient(135deg, var(--gold), var(--gold2));
  border: none; border-radius: 14px; padding: 15px;
  font-family: 'Unbounded', sans-serif; font-size: 13px; font-weight: 700;
  color: #0c0c10; cursor: pointer; transition: opacity 0.15s;
}
.bid-cta:active { opacity: 0.82; }
.lot-closed {
  background: var(--s2); border-radius: 14px; padding: 14px;
  text-align: center; font-size: 13px; color: var(--muted); font-weight: 600;
}

/* ── Bid sheet ── */
.sheet-overlay {
  position: absolute; inset: 0;
  background: rgba(0,0,0,0.65); backdrop-filter: blur(6px);
  z-index: 50; display: flex; flex-direction: column; justify-content: flex-end;
  animation: fadeIn 0.2s;
}
@keyframes fadeIn { from{opacity:0;} to{opacity:1;} }

.sheet {
  background: var(--s1); border-radius: 22px 22px 0 0;
  border-top: 1px solid var(--border2);
  padding: 18px 18px 36px;
  animation: slideUp 0.28s cubic-bezier(.4,0,.2,1);
}
@keyframes slideUp { from{transform:translateY(100%);} to{transform:translateY(0);} }

.sheet-handle {
  width: 38px; height: 4px; background: var(--s3);
  border-radius: 2px; margin: 0 auto 18px;
}
.sheet-title {
  font-family: 'Unbounded', sans-serif;
  font-size: 15px; font-weight: 700; text-align: center;
  margin-bottom: 4px; color: var(--text);
}
.sheet-lot { text-align: center; color: var(--text2); font-size: 12px; margin-bottom: 18px; }

.bid-opts { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 14px; }
.bid-opt {
  background: var(--s2); border: 1.5px solid var(--border);
  border-radius: 12px; padding: 13px 10px; text-align: center;
  cursor: pointer; transition: all 0.15s; user-select: none;
}
.bid-opt.sel { border-color: var(--gold); background: rgba(232,184,75,0.07); }
.bid-opt:active { transform: scale(0.96); }
.opt-val { font-family: 'Unbounded', sans-serif; font-size: 14px; font-weight: 700; color: var(--gold); margin-bottom: 3px; }
.opt-lbl { font-size: 10px; color: var(--muted); font-weight: 600; }

/* Custom input */
.custom-wrap { margin-bottom: 14px; }
.custom-input {
  width: 100%; background: var(--s2);
  border: 1.5px solid var(--gold); border-radius: 12px;
  padding: 13px 48px 13px 16px;
  font-family: 'Unbounded', sans-serif; font-size: 15px; font-weight: 700;
  color: var(--text); outline: none;
}
.custom-rub {
  position: absolute; right: 14px; top: 50%; transform: translateY(-50%);
  font-size: 14px; font-weight: 700; color: var(--gold); pointer-events: none;
}
.custom-hint { font-size: 11px; margin-top: 6px; padding-left: 2px; }
.custom-hint.error { color: var(--red);   }
.custom-hint.ok    { color: var(--green); }

.sheet-confirm {
  width: 100%;
  background: linear-gradient(135deg, var(--gold), var(--gold2));
  border: none; border-radius: 14px; padding: 15px;
  font-family: 'Unbounded', sans-serif; font-size: 13px; font-weight: 700;
  color: #0c0c10; cursor: pointer; transition: all 0.2s;
}
.sheet-confirm:active { opacity: 0.82; }
.sheet-confirm.disabled { opacity: 0.4; cursor: not-allowed; }
.sheet-confirm.success  { background: linear-gradient(135deg, var(--green), #20a056); color: white; }
.sheet-confirm.error    { background: linear-gradient(135deg, var(--red), #c02030);   color: white; }
.sheet-note { text-align: center; font-size: 10px; color: var(--muted); margin-top: 10px; }

/* ── Spinner ── */
.spinner {
  width: 28px; height: 28px; border-radius: 50%;
  border: 3px solid var(--s3); border-top-color: var(--gold);
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

```


## File: miniapp\frontend\src\index.js
```javascript
import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<React.StrictMode><App /></React.StrictMode>);

```


## File: miniapp\frontend\src\hooks\useTelegram.js
```javascript
// src/hooks/useTelegram.js
import { useEffect, useState } from "react";

export function useTelegram() {
  const [tg, setTg] = useState(null);
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const webapp = window.Telegram?.WebApp;
    if (webapp) {
      webapp.ready();
      webapp.expand();
      webapp.setHeaderColor("#0c0c10");
      webapp.setBackgroundColor("#0c0c10");
      setTg(webapp);
      setUser(webapp.initDataUnsafe?.user || null);
    } else {
      // Dev fallback
      setUser({ id: 123456, first_name: "Dev", username: "devuser" });
    }
    setReady(true);
  }, []);

  const showBackButton = (onBack) => {
    if (tg?.BackButton) {
      tg.BackButton.show();
      tg.BackButton.onClick(onBack);
    }
  };

  const hideBackButton = () => {
    if (tg?.BackButton) {
      tg.BackButton.hide();
      tg.BackButton.offClick();
    }
  };

  const haptic = (type = "light") => {
    tg?.HapticFeedback?.impactOccurred(type);
  };

  const showMainButton = (text, onClick) => {
    if (tg?.MainButton) {
      tg.MainButton.setText(text);
      tg.MainButton.show();
      tg.MainButton.onClick(onClick);
    }
  };

  const hideMainButton = () => {
    if (tg?.MainButton) {
      tg.MainButton.hide();
      tg.MainButton.offClick();
    }
  };

  return { tg, user, ready, showBackButton, hideBackButton, haptic, showMainButton, hideMainButton };
}

```


## File: miniapp\frontend\src\hooks\useTimer.js
```javascript
// src/hooks/useTimer.js
import { useEffect, useState } from "react";
import { fmtTimer, isEndingSoon } from "../utils/format";

export function useTimer(endsAt) {
  const [display, setDisplay] = useState(fmtTimer(endsAt));
  const [ending, setEnding] = useState(isEndingSoon(endsAt));

  useEffect(() => {
    if (!endsAt) return;
    const tick = () => {
      setDisplay(fmtTimer(endsAt));
      setEnding(isEndingSoon(endsAt));
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [endsAt]);

  return { display, ending };
}

```


## File: miniapp\frontend\src\utils\api.js
```javascript
export const BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

function getInitData() {
  try {
    const data = window.Telegram?.WebApp?.initData || "";
    console.log("initData length:", data.length);
    return data;
  } catch {
    return "";
  }
}

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "x-tg-init-data": getInitData(),
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Ошибка запроса");
  }
  return res.json();
}

export const api = {
  getLots:    ()               => request("/api/lots"),
  getMyLots:  ()               => request("/api/lots/mine"),
  getLot:     (id)             => request(`/api/lots/${id}`),
  placeBid:   (lot_id, amount) =>
    request("/api/bids", {
      method: "POST",
      body: JSON.stringify({ lot_id, amount }),
    }),
};
```


## File: miniapp\frontend\src\utils\format.js
```javascript
// src/utils/format.js

export function fmtPrice(amount) {
  if (amount == null) return "—";
  return amount.toLocaleString("ru-RU") + " ₽";
}

export function fmtTimer(endsAt) {
  if (!endsAt) return null;
  const end = new Date(endsAt);
  const now = new Date();
  const diff = Math.max(0, Math.floor((end - now) / 1000));

  if (diff <= 0) return "завершён";

  const h = Math.floor(diff / 3600);
  const m = Math.floor((diff % 3600) / 60);
  const s = diff % 60;

  if (h > 0) return `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export function isEndingSoon(endsAt) {
  if (!endsAt) return false;
  const diff = new Date(endsAt) - new Date();
  return diff > 0 && diff < 10 * 60 * 1000; // < 10 min
}

export function getLotMyStatus(lot) {
  if (!lot.my_bid) return null;
  if (lot.status === "finished") {
    return lot.winner_user_id && lot.is_leading ? "won" : "lost";
  }
  return lot.is_leading ? "leading" : "outbid";
}

```