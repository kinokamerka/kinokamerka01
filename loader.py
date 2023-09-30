from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token, admin_id

#Connect к боту#
storage=MemoryStorage()
bot=Bot(token)
dp=Dispatcher(bot, storage=storage)
admin_id=admin_id