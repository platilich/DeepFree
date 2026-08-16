import asyncio
from aiogram import Bot, Dispatcher


from bot_tools.handlers import router


from aiogram.fsm.storage.memory import MemoryStorage

from config import TG_TOKEN



bot = Bot(token=TG_TOKEN)
storage = MemoryStorage()


dp = Dispatcher(storage=storage)






async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())