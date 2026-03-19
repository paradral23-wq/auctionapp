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

