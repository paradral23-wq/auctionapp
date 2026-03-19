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

