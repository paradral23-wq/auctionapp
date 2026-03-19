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
    "DATABASE_URL", "sqlite+aiosqlite:///./auction.db"
)

# ── Auction defaults ─────────────────────────────────────────
ANTISNIPE_MINUTES: int = int(os.getenv("ANTISNIPE_MINUTES", "2"))
MIN_BID_STEP: int = int(os.getenv("MIN_BID_STEP", "500"))

# Mini App URL (используется в group bot)
MINIAPP_URL: str = os.getenv("MINIAPP_URL", "")

# Локальный Telegram Bot API сервер (для загрузки файлов > 20MB)
TELEGRAM_API_SERVER: str = os.getenv("TELEGRAM_API_SERVER", "")
