from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data.db import only_list, get_AllFilms

class IsCode(BoundFilter):
    async def check(self, message: types.Message):
        data_code=await only_list(await get_AllFilms(type='films_code'))
        for i in data_code:
            if i == message.text:
                return True
        return False

