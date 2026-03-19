from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS


async def is_admin(user_id: int) -> bool:
    """Проверяет через БД. Fallback на .env если БД недоступна."""
    try:
        from db.queries import is_admin_in_db
        return await is_admin_in_db(user_id)
    except Exception:
        return user_id in ADMIN_IDS


async def is_super_admin(user_id: int) -> bool:
    """Суперадмин — из .env или помечен is_super=True в БД."""
    try:
        from db.queries import get_admin
        admin = await get_admin(user_id)
        return admin is not None and admin.is_super
    except Exception:
        return user_id in ADMIN_IDS


async def admin_only_message(message: Message) -> bool:
    if not await is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return False
    return True


async def admin_only_callback(callback: CallbackQuery) -> bool:
    if not await is_admin(callback.from_user.id):
        await callback.answer("⛔ Доступ запрещён.", show_alert=True)
        return False
    return True


async def super_admin_only_callback(callback: CallbackQuery) -> bool:
    """Только суперадмин — для управления другими админами."""
    if not await is_super_admin(callback.from_user.id):
        await callback.answer("⛔ Только суперадмин может это делать.", show_alert=True)
        return False
    return True
