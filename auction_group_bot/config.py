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
