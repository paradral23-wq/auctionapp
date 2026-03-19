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

