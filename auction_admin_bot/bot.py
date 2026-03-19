import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from config import BOT_TOKEN, GROUP_BOT_TOKEN, TELEGRAM_API_SERVER
from db.database import init_db
from handlers import main_menu, create_lot, monitor, manage, finish, admins, edit_lot
from utils.scheduler import (
    setup_scheduler,
    restore_scheduled_jobs,
    sync_finish_jobs,
    sync_overbid_notifications,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    # Использовать локальный Bot API сервер если настроен
    if TELEGRAM_API_SERVER:
        session = AiohttpSession(
            api=TelegramAPIServer.from_base(TELEGRAM_API_SERVER, is_local=True)
        )
        bot = Bot(token=BOT_TOKEN, session=session)
        winner_bot = Bot(token=GROUP_BOT_TOKEN, session=session) if GROUP_BOT_TOKEN else None
        logger.info(f"Using local Bot API server: {TELEGRAM_API_SERVER}")
    else:
        bot = Bot(token=BOT_TOKEN)
        winner_bot = Bot(token=GROUP_BOT_TOKEN) if GROUP_BOT_TOKEN else None

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    await init_db()

    # Загрузить суперадминов из .env в БД
    from config import ADMIN_IDS
    from db.queries import seed_super_admins
    await seed_super_admins(ADMIN_IDS)

    scheduler = setup_scheduler(bot)
    scheduler.start()

    await restore_scheduled_jobs(bot, winner_bot)

    asyncio.create_task(sync_finish_jobs(bot, winner_bot))
    asyncio.create_task(sync_overbid_notifications(bot, winner_bot))

    dp.include_router(main_menu.router)
    dp.include_router(create_lot.router)
    dp.include_router(monitor.router)
    dp.include_router(manage.router)
    dp.include_router(finish.router)
    dp.include_router(admins.router)
    dp.include_router(edit_lot.router)

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
