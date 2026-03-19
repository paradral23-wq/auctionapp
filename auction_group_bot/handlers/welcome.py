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
