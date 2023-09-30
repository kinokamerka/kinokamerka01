from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loader import admin_id

#фильтр на дамина в сообщения#
class IsAdminM(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.id == admin_id

#фильтр на дамина в callback#
class IsAdminC(BoundFilter):
    async def check(self, message: types.CallbackQuery):
        return message.from_user.id == admin_id

class IsAdminCAndChenneger_swich_player(BoundFilter):
    async def check(self, message: types.CallbackQuery):
        return message.from_user.id == admin_id and message.data[0:28] == 'chenneger_swich_player_admin'

class IsAdminCAndChenneger_kbname_player_admin(BoundFilter):
    async def check(self, message: types.CallbackQuery):
        return message.from_user.id == admin_id and message.data[0:29] == 'chenneger_kbname_player_admin'