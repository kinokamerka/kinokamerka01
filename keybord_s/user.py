from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.db import get_AllChennel, get_Allplayer
from misc.plugin.KinoPoiskFree import get_FilmsMe


async def sub_list():
    data_chennel=await get_AllChennel()
    sub_list=InlineKeyboardMarkup(row_width=1)
    for i in data_chennel:
        sub_list.add(InlineKeyboardButton(text=i[1], url=i[2]))
    sub_list.add(InlineKeyboardButton(text='Одна из сыллок не работает❓', callback_data='link_no_work'))
    return sub_list

#
async def kb_films(name_films):
    ikb=InlineKeyboardMarkup(row_width=1)
    for i in await get_Allplayer():
        if i[2]:
            url=await get_FilmsMe(name=name_films, web=i[0])
            ikb.row(InlineKeyboardButton(text=i[3], url=url))
    return ikb
