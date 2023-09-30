from loader import dp, bot, admin_id
from aiogram import types
from myFilters.user import IsCode
from data.db import get_films, get_AllChennel, get_error_link_complaint_unix, update_error_link_complaint_unix, get_text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from time import time
from keybord_s.ohter import ikb_close, ikb_close_oikb
from keybord_s.user import sub_list, kb_films
from datetime import datetime, timedelta

#получение фильма по коду#
@dp.message_handler(IsCode())
async def get_FimsWithCode(message: types.Message):
    await message.delete()
    data_chennel=await get_AllChennel()
    for i in data_chennel:
        try:
            status=await bot.get_chat_member(chat_id=i[0], user_id=message.from_user.id)
            if status.status == 'left':
                await message.answer('Вы не подписаны на канал(ы)❌\nПосле подписки повторите попытку👌', reply_markup=await sub_list())
                return
        except:
            await bot.send_message(chat_id=admin_id, text=f'Похоже этот канал удалил нас запустите "Проверку каналов"\nЧто бы проверить меня на наличие прав\nИндификатор: {i[0]}\nНазвание: {i[1]}\nСыллка: {i[2]}', reply_markup=ikb_close.row(InlineKeyboardButton(text='Проверить каналы⚛️', callback_data='check_chennel_admin')))

    film_data=await get_films(code=message.text)
    text_film=await get_text(type='text_text', text_type='film')
    text_film=text_film[0][0]
    me=await bot.get_me()
    text_film=str(text_film).replace('{username_bot}', me.mention)
    text_film=str(text_film).replace('{bot_id}', str(me.id))
    text_film=str(text_film).replace('{username}', message.from_user.mention)
    text_film=str(text_film).replace('{full_name}', message.from_user.full_name)
    text_film=str(text_film).replace('{user_id}', str(message.from_user.id)) 
    text_film=str(text_film).replace('{film_name}', film_data[0][1]) 
    text_film=str(text_film).replace('{film_code}', message.text) 
    
    ikb_films=await kb_films(name_films=film_data[0][1])
    await bot.send_photo(chat_id=message.from_user.id, photo=film_data[0][2], caption=text_film, reply_markup=ikb_films.row(ikb_close_oikb), parse_mode=types.ParseMode.HTML)

#Обработка кнопки "Одна из сыллок не работает❓"#
@dp.callback_query_handler(text='link_no_work')
async def Link_complaint(call: types.CallbackQuery):
    if await get_error_link_complaint_unix(user_id=call.from_user.id) == None or await get_error_link_complaint_unix(user_id=call.from_user.id) <= time():
        await call.message.answer('Мы отправили администратуру ошибку☑️', reply_markup=ikb_close)
        await bot.send_message(chat_id=admin_id, text=f'Пользователь [{call.from_user.full_name}](tg://user?id={call.from_user.id}) пожаловался то что одна из сыллок не работает❗️', parse_mode=types.ParseMode.MARKDOWN, reply_markup=ikb_close.row(InlineKeyboardButton(text='Проверить каналы⚛️', callback_data='check_chennel_admin')))
        timeub=datetime.now()+timedelta(hours=3)
        await update_error_link_complaint_unix(user_id=call.from_user.id, time_ub=timeub.timestamp())
    else:
        await call.answer('Вы уже жаловались❌')
