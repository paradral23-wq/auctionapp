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
