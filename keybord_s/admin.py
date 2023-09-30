from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .ohter import ikb_close_oikb
from data.db import get_Allplayer

async def get_Player_menu():
    ikb=InlineKeyboardMarkup(row_width=4)
    ikb.insert(InlineKeyboardButton(text='Название', callback_data='player_exemple'))
    ikb.insert(InlineKeyboardButton(text='Сайт', callback_data='player_exemple'))
    ikb.insert(InlineKeyboardButton(text='Вкл./Выкл.', callback_data='player_exemple'))
    ikb.insert(InlineKeyboardButton(text='Название на кнопки', callback_data='player_exemple'))
    for i in await get_Allplayer():
        if i[2] == 1:
            swich=str(i[2]).replace('1', '✅')
        elif i[2] == 0:
            swich=str(i[2]).replace('0', '❌')
        ikb.insert(InlineKeyboardButton(text=i[1], callback_data='chenneger_name_player_admin'))
        ikb.insert(InlineKeyboardButton(text=i[0], callback_data='chenneger_web_player_admin'))
        ikb.insert(InlineKeyboardButton(text=swich, callback_data='chenneger_swich_player_admin'+i[1]))
        ikb.insert(InlineKeyboardButton(text=i[3], callback_data='chenneger_kbname_player_admin'+i[1]))
    ikb.row(InlineKeyboardButton(text='Назад⬅️', callback_data='back_main_menu_admin'))
    return ikb

#админ меню#
admin_menu_main=InlineKeyboardMarkup(row_width=2)
admin_menu_main.row(InlineKeyboardButton(text='Сделать рассылку📬', callback_data='myling_list_start_admin'))
admin_menu_main.row(InlineKeyboardButton(text='Списки🗒', callback_data='list_data_admin'))
admin_menu_main.row(InlineKeyboardButton(text='Добавить фильм📌', callback_data='add_film_admin'))
admin_menu_main.insert(InlineKeyboardButton(text='Удалить фильм🗑', callback_data='delete_film_admin'))
admin_menu_main.row(InlineKeyboardButton(text='Добавить канал➕', callback_data='add_chennel_admin'))
admin_menu_main.insert(InlineKeyboardButton(text='Удалить канал➖', callback_data='delete_chennel_admin'))
admin_menu_main.row(InlineKeyboardButton(text='Проверка каналов⚛️', callback_data='check_chennel_admin'))
admin_menu_main.row(InlineKeyboardButton(text='Плаеры▶️', callback_data='player_settings_admin'))
admin_menu_main.row(InlineKeyboardButton(text='Текста📝', callback_data='text_settings_admin'))
admin_menu_main.row(ikb_close_oikb)

#меню списков#
admin_menu_list=InlineKeyboardMarkup(row_width=1)
admin_menu_list.row(InlineKeyboardButton(text='Фильмы🎥', callback_data='list_films_admin'))
admin_menu_list.row(InlineKeyboardButton(text='Каналы📢', callback_data='list_chennel_admin'))
admin_menu_list.row(InlineKeyboardButton(text='Назад⬅️', callback_data='back_main_menu_admin'))

admin_menu_text=InlineKeyboardMarkup(row_width=1)
admin_menu_text.row(InlineKeyboardButton(text='Приветствие', callback_data='chenneger_wellcome_text_settings_admin'))
admin_menu_text.row(InlineKeyboardButton(text='Фильм', callback_data='chenneger_film_text_settings_admin'))
admin_menu_text.row(InlineKeyboardButton(text='Назад⬅️', callback_data='back_main_menu_admin'))

