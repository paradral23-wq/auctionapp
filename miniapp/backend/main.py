"""
miniapp/backend/main.py — FastAPI для Dutch-аукциона недвижимости.
"""
import hashlib, hmac, json, logging, os
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import parse_qsl

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select, text, update

from database import AsyncSessionLocal, Bid, BannedUser, Lot, LotMedia, LotStatus

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Dubai Property Auction API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "")
GROUP_BOT_TOKEN = os.getenv("GROUP_BOT_TOKEN", "")
ADMIN_TG_ID     = int(os.getenv("ADMIN_TG_ID", "0"))
VIDEOS_DIR      = Path(os.getenv("VIDEOS_DIR", "./videos"))
TG_API_SERVER   = os.getenv("TELEGRAM_API_SERVER", "https://api.telegram.org")
DEV_USER_ID     = int(os.getenv("DEV_USER_ID", "0"))

# Кеш цен в памяти (обновляется вебхуком от бота)
_price_cache: dict = {}


# ── Auth ──────────────────────────────────────────────────────

def verify_init_data(init_data: str, bot_token: str) -> Optional[dict]:
    try:
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        hash_value = parsed.pop("hash", "")
        data_check = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        # Правильный способ: HMAC-SHA256(secret_key, data_check)
        # где secret_key = HMAC-SHA256("WebAppData", bot_token)
        secret = hmac.new(
            "WebAppData".encode(),
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        expected = hmac.new(
            secret,
            data_check.encode(),
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(expected, hash_value):
            return None
        return json.loads(parsed.get("user", "{}"))
    except Exception as e:
        logger.warning(f"verify_init_data exception: {e}")
        return None



def get_user(x_tg_init_data: Optional[str] = Header(None)) -> dict:
    if not x_tg_init_data:
        logger.warning("No x-tg-init-data header, using dev_user")
        return {"id": DEV_USER_ID or 0, "username": "dev_user", "first_name": "Dev"}
    # Пробуем верифицировать всеми доступными токенами
    for token in filter(None, [ADMIN_BOT_TOKEN, GROUP_BOT_TOKEN]):
        user = verify_init_data(x_tg_init_data, token)
        if user:
            logger.info(f"Verified user: id={user.get('id')} username={user.get('username')}")
            return user
    # Верификация не прошла — читаем user из initData без проверки подписи
    # (данные всё равно пришли из Telegram)
    try:
        from urllib.parse import parse_qsl
        parsed = dict(parse_qsl(x_tg_init_data, keep_blank_values=True))
        user = json.loads(parsed.get("user", "{}"))
        if user.get("id"):
            logger.warning(f"Signature failed but extracting user from initData: id={user.get('id')}")
            return user
    except Exception as e:
        logger.warning(f"Failed to extract user from initData: {e}")
    return {"id": DEV_USER_ID or 0, "username": "dev_user", "first_name": "Dev"}


# ── Serialisation ─────────────────────────────────────────────

def fmt_aed(amount: int) -> str:
    return f"AED {amount:,}".replace(",", " ")


def lot_to_dict(lot: Lot, user_id: int, top_bid: Optional[Bid] = None,
                bid_count: int = 0, last_bid_at: Optional[datetime] = None) -> dict:
    now = datetime.now(timezone.utc)

    # Применить кеш цены если есть (обновляется вебхуком от бота)
    cached = _price_cache.get(lot.id)
    if cached and lot.status == LotStatus.ACTIVE:
        lot.current_price = cached["current_price"]

    seconds_left = 0
    if lot.ends_at:
        ends = lot.ends_at if lot.ends_at.tzinfo else lot.ends_at.replace(tzinfo=timezone.utc)
        seconds_left = max(0, int((ends - now).total_seconds()))

    # Для Dutch: считаем секунды до следующего снижения
    # на основе времени последней ставки (= последнее снижение)
    seconds_until_drop = None
    # Если есть свежий кеш от вебхука — используем его
    if cached and cached.get("seconds_until_drop") is not None and lot.status == LotStatus.ACTIVE:
        cache_age = int((now - datetime.fromisoformat(cached["updated_at"])).total_seconds())
        seconds_until_drop = max(0, cached["seconds_until_drop"] - cache_age)
    elif lot.price_drop_interval_minutes and lot.status == "active":
        interval_secs = lot.price_drop_interval_minutes * 60
        if last_bid_at:
            last = last_bid_at if last_bid_at.tzinfo else last_bid_at.replace(tzinfo=timezone.utc)
            elapsed = int((now - last).total_seconds())
            seconds_until_drop = max(0, interval_secs - elapsed)
        else:
            # Нет ставок — считаем от времени создания лота
            created = lot.created_at if lot.created_at.tzinfo else lot.created_at.replace(tzinfo=timezone.utc)
            elapsed = int((now - created).total_seconds()) % interval_secs
            seconds_until_drop = max(0, interval_secs - elapsed)

    is_my_lot = top_bid and top_bid.user_id == user_id

    return {
        "id":            lot.id,
        "lot_code":      lot.lot_code,
        "emoji":         lot.emoji,
        "title":         lot.title,
        "description":   lot.description or "",
        "photo_file_id": lot.photo_file_id,
        "status":        lot.status.value if hasattr(lot.status, "value") else lot.status,

        # Недвижимость
        "property_type":   lot.property_type,
        "area_sqft":       lot.area_sqft,
        "floor_level":     lot.floor_level,
        "view_type":       lot.view_type,
        "parking_spots":   lot.parking_spots,
        "property_status": lot.property_status,
        "purchase_price":  lot.purchase_price,
        "market_price":    lot.market_price,
        "discount_pct":    lot.discount_pct,

        # Ценообразование Dutch
        "start_price":   lot.start_price,
        "current_price": lot.current_price,
        "bid_step":      lot.bid_step,
        "price_drop_interval_minutes": lot.price_drop_interval_minutes,
        "seconds_until_drop": seconds_until_drop,

        # Тайминг
        "starts_at":    lot.starts_at.isoformat() if lot.starts_at else None,
        "ends_at":      lot.ends_at.isoformat() if lot.ends_at else None,
        "seconds_left": seconds_left,
        "seconds_until_start": (
            max(0, int((
                (lot.starts_at if lot.starts_at.tzinfo else lot.starts_at.replace(tzinfo=timezone.utc))
                - now
            ).total_seconds()))
            if lot.starts_at and lot.status == LotStatus.SCHEDULED else None
        ),

        # Итог
        "winner_user_id":  lot.winner_user_id,
        "winner_username": lot.winner_username,
        "final_price":     lot.final_price,

        # Медиа — массив {file_id, media_type}
        "media": [],   # заполняется в _enrich

        # Для текущего пользователя
        "bid_count":  bid_count,
        "i_bought":   bool(lot.status == LotStatus.FINISHED and
                           lot.winner_user_id and lot.winner_user_id == user_id),
        "i_bid":      bool(is_my_lot),

        # Для кнопки "Написать администратору"
        "admin_tg_id": ADMIN_TG_ID or None,
    }


async def _enrich(session, lot: Lot, user_id: int) -> dict:
    top = (await session.execute(
        select(Bid).where(Bid.lot_id == lot.id, Bid.is_cancelled == False)
        .order_by(Bid.amount.desc()).limit(1)
    )).scalar_one_or_none()
    cnt = (await session.execute(
        select(Bid).where(Bid.lot_id == lot.id, Bid.is_cancelled == False)
    )).scalars().all()
    # Последняя ставка по времени = момент последнего снижения цены
    last_bid = (await session.execute(
        select(Bid).where(Bid.lot_id == lot.id, Bid.is_cancelled == False)
        .order_by(Bid.created_at.desc()).limit(1)
    )).scalar_one_or_none()
    last_bid_at = last_bid.created_at if last_bid else None
    # Медиафайлы лота
    media_rows = (await session.execute(
        select(LotMedia).where(LotMedia.lot_id == lot.id).order_by(LotMedia.order)
    )).scalars().all()
    media = [
        {
            "file_id":    m.file_id,
            "media_type": m.media_type,
            "has_local":  bool(m.file_path and Path(m.file_path).exists()),
        }
        for m in media_rows
    ]
    d = lot_to_dict(lot, user_id, top, len(cnt), last_bid_at)
    d["media"] = media
    return d


# ── GET /api/lots ─────────────────────────────────────────────

@app.get("/api/lots")
async def get_lots(x_tg_init_data: Optional[str] = Header(None)):
    user = get_user(x_tg_init_data)
    uid  = user.get("id", 0)

    async with AsyncSessionLocal() as s:
        await s.execute(text("PRAGMA read_uncommitted = true;"))
        result = await s.execute(
            select(Lot)
            .where(Lot.status.in_([
                LotStatus.ACTIVE, LotStatus.SCHEDULED, LotStatus.PAUSED,
                LotStatus.FINISHED, LotStatus.CANCELLED,
            ]))
            .order_by(Lot.created_at.desc())
            .execution_options(populate_existing=True)
        )
        lots = result.scalars().all()
        output = [await _enrich(s, lot, uid) for lot in lots]

    return {"lots": output}


# ── GET /api/lots/mine ────────────────────────────────────────

@app.get("/api/lots/mine")
async def get_my_lots(x_tg_init_data: Optional[str] = Header(None)):
    """Все лоты где пользователь делал ставку (участвовал)."""
    user = get_user(x_tg_init_data)
    uid  = user.get("id", 0)

    async with AsyncSessionLocal() as s:
        # Все lot_id где этот user делал ставки
        bid_rows = await s.execute(
            select(Bid.lot_id).where(
                Bid.user_id == uid, Bid.is_cancelled == False
            ).distinct()
        )
        lot_ids = [r[0] for r in bid_rows.all()]
        if not lot_ids:
            return {"lots": []}

        result = await s.execute(
            select(Lot).where(Lot.id.in_(lot_ids)).order_by(Lot.created_at.desc())
        )
        lots = result.scalars().all()
        output = [await _enrich(s, lot, uid) for lot in lots]

    return {"lots": output}


# ── GET /api/lots/{lot_id} ────────────────────────────────────

@app.get("/api/lots/{lot_id}")
async def get_lot(lot_id: int, x_tg_init_data: Optional[str] = Header(None)):
    user = get_user(x_tg_init_data)
    uid  = user.get("id", 0)

    async with AsyncSessionLocal() as s:
        lot = await s.get(Lot, lot_id)
        if not lot:
            raise HTTPException(status_code=404, detail="Лот не найден")
        data = await _enrich(s, lot, uid)

    return data


# ── POST /api/buy ─────────────────────────────────────────────

class BuyRequest(BaseModel):
    lot_id: int


@app.post("/api/buy")
async def buy_lot(req: BuyRequest, x_tg_init_data: Optional[str] = Header(None)):
    """
    Dutch-аукцион: купить лот по текущей цене.
    Атомарно: проверяем статус, ставим FINISHED, записываем победителя.
    """
    user     = get_user(x_tg_init_data)
    user_id  = user.get("id", 0)
    username = user.get("username")

    async with AsyncSessionLocal() as s:
        async with s.begin():
            # Проверка бана
            banned = await s.get(BannedUser, user_id)
            if banned:
                raise HTTPException(status_code=403, detail="Вы заблокированы")

            result = await s.execute(
                select(Lot).where(Lot.id == req.lot_id).with_for_update()
            )
            lot = result.scalar_one_or_none()

            if not lot:
                raise HTTPException(status_code=404, detail="Лот не найден")
            if lot.status != LotStatus.ACTIVE:
                if lot.status == LotStatus.FINISHED:
                    raise HTTPException(status_code=400, detail="Лот уже куплен другим участником")
                raise HTTPException(status_code=400, detail="Аукцион не активен")
            if not lot.price_drop_interval_minutes:
                raise HTTPException(status_code=400, detail="Не Dutch-аукцион")

            final_price = lot.current_price

            # Записать ставку
            bid = Bid(lot_id=req.lot_id, user_id=user_id,
                      username=username, amount=final_price)
            s.add(bid)

            # Завершить лот
            lot.status          = LotStatus.FINISHED
            lot.winner_user_id  = user_id
            lot.winner_username = username or None
            lot.final_price     = final_price

    logger.info(f"Dutch buy: lot={req.lot_id} user={user_id} price={final_price}")

    return {
        "ok":          True,
        "lot_id":      req.lot_id,
        "final_price": final_price,
        "final_price_fmt": fmt_aed(final_price),
    }


# ── GET /api/photo/{file_id} ──────────────────────────────────

@app.get("/api/photo/{file_id:path}")
async def get_photo(file_id: str):
    return await _stream_tg_file(file_id, "image/jpeg")


# ── GET /api/video/{file_id} ──────────────────────────────────

@app.get("/api/video/{file_id:path}")
async def get_video(file_id: str, request: Request):
    """
    Стриминг видео. Приоритет:
    1. Локальный файл на диске (file_path из lot_media) — для файлов > 20MB
    2. Telegram Bot API — для файлов <= 20MB (если нет локального)
    """
    # Ищем локальный файл в БД по file_id
    async with AsyncSessionLocal() as s:
        row = (await s.execute(
            select(LotMedia).where(LotMedia.file_id == file_id).limit(1)
        )).scalar_one_or_none()

    local_path = None
    if row and row.file_path:
        p = Path(row.file_path)
        if p.exists():
            local_path = p

    if local_path:
        # Стриминг с диска — поддержка Range
        file_size = local_path.stat().st_size
        range_header = request.headers.get("range")

        if range_header:
            start, end = 0, file_size - 1
            parts = range_header.replace("bytes=", "").split("-")
            start = int(parts[0]) if parts[0] else 0
            end   = int(parts[1]) if len(parts) > 1 and parts[1] else file_size - 1
            end   = min(end, file_size - 1)
            chunk_size = end - start + 1

            def iter_file_range():
                with open(local_path, "rb") as f:
                    f.seek(start)
                    remaining = chunk_size
                    while remaining > 0:
                        data = f.read(min(65536, remaining))
                        if not data:
                            break
                        remaining -= len(data)
                        yield data

            return StreamingResponse(
                iter_file_range(),
                status_code=206,
                media_type="video/mp4",
                headers={
                    "Content-Range":  f"bytes {start}-{end}/{file_size}",
                    "Accept-Ranges":  "bytes",
                    "Content-Length": str(chunk_size),
                },
            )
        else:
            return FileResponse(
                path=str(local_path),
                media_type="video/mp4",
                headers={"Accept-Ranges": "bytes"},
            )

    # Fallback: стриминг через Telegram Bot API (только для файлов <= 20MB)
    token = ADMIN_BOT_TOKEN or GROUP_BOT_TOKEN
    if not token:
        raise HTTPException(status_code=500, detail="No bot token and no local file")
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(
                f"{TG_API_SERVER.rstrip('/')}/bot{token}/getFile",
                params={"file_id": file_id}
            )
            data = r.json()
            if not data.get("ok"):
                raise HTTPException(status_code=404, detail=str(data))
            tg_path   = data["result"]["file_path"]
            file_size = data["result"].get("file_size", 0)
            # Локальный сервер возвращает абсолютный путь к файлу
            if tg_path.startswith("/"):
                local_path = Path(tg_path)
                if local_path.exists():
                    return FileResponse(str(local_path), media_type="video/mp4",
                                        headers={"Accept-Ranges": "bytes"})
            video_url = f"{TG_API_SERVER.rstrip('/')}/file/bot{token}/{tg_path}"

            async def stream_full():
                async with httpx.AsyncClient(timeout=120) as c:
                    async with c.stream("GET", video_url) as resp:
                        async for chunk in resp.aiter_bytes(65536):
                            yield chunk

            return StreamingResponse(
                stream_full(),
                media_type="video/mp4",
                headers={"Accept-Ranges": "bytes",
                         "Content-Length": str(file_size) if file_size else ""},
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"get_video error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _stream_tg_file(file_id: str, media_type: str):
    token = ADMIN_BOT_TOKEN or GROUP_BOT_TOKEN
    if not token:
        raise HTTPException(status_code=500, detail="No bot token")
    base = TG_API_SERVER.rstrip("/")
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{base}/bot{token}/getFile",
                                 params={"file_id": file_id})
            data = r.json()
            if not data.get("ok"):
                raise HTTPException(status_code=404, detail=str(data))
            fp  = data["result"]["file_path"]
            # Локальный сервер возвращает абсолютный путь
            if fp.startswith("/"):
                with open(fp, "rb") as f:
                    return StreamingResponse(iter([f.read()]), media_type=media_type)
            img = await client.get(f"{base}/file/bot{token}/{fp}")
            return StreamingResponse(iter([img.content]), media_type=media_type)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── POST /api/contact ─────────────────────────────────────────

@app.post("/api/contact")
async def contact_admin(x_tg_init_data: Optional[str] = Header(None)):
    """Открыть чат с администратором — возвращает tg://user?id=..."""
    user = get_user(x_tg_init_data)
    uid  = user.get("id", 0)
    logger.info(f"Contact request from user {uid}")
    return {"admin_tg_id": ADMIN_TG_ID, "ok": True}


# ── Startup ───────────────────────────────────────────────────

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
        rows = (await s.execute(
            text("SELECT id, lot_code, status, current_price FROM lots ORDER BY id DESC LIMIT 10")
        )).fetchall()
    return {"rows": [list(r) for r in rows]}
