from loader import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from myFilters.admin import IsAdminC
from myFilters.admin import IsAdminCAndChenneger_swich_player, IsAdminCAndChenneger_kbname_player_admin
from fsm_state_ import admin as astate
from data.db import get_AllFilms, only_list, get_AllChennel, delete_Chennel, update_nameChennel, swich_player
from random import randint
from keybord_s.ohter import ikb_back_oikb, ikb_back, ikb_close
from keybord_s.admin import admin_menu_list, admin_menu_main, get_Player_menu, admin_menu_text

#
@dp.callback_query_handler(IsAdminC(), text='back_main_menu_admin')
async def list_data_check(call: types.Message):
    await call.message.edit_reply_markup(admin_menu_main)
    

#обработка запроса на рассылку#
@dp.callback_query_handler(IsAdminC(), text='myling_list_start_admin')
async def myling_list_start_admin(call: types.Message, state: FSMContext):
    message_data=await bot.send_message(chat_id=call.from_user.id, text='Хорошо отправь текст для рассылки✒️\nМожно использовать стандартную разметку✂️', reply_markup=ikb_back)
    async with state.proxy() as data:
        data['message_id']=message_data.message_id
    await astate.Admin_State.myling_list.text.set()

#списки#
@dp.callback_query_handler(IsAdminC(), text='list_data_admin')
async def list_data_check(call: types.Message):
    await call.message.edit_reply_markup(admin_menu_list)

@dp.callback_query_handler(IsAdminC(), text='list_films_admin')
async def list_data_films(call: types.Message):
    file_films=open(file='data//films_data.txt', mode='w+', encoding='UTF-8')
    for i in await get_AllFilms():
        file_films.write(f'Код: {i[0]}, название: {i[1]}\n')
    file_films.close()
    try:
        await bot.send_document(chat_id=call.from_user.id, document=open(file='data//films_data.txt', mode='rb'), reply_markup=ikb_close)
    except:
        await call.answer('У вас нет фильмов❌')
    
@dp.callback_query_handler(IsAdminC(), text='list_chennel_admin')
async def list_data_films(call: types.Message):
    file_films=open(file='data//chennal_data.txt', mode='w+', encoding='UTF-8')
    for i in await get_AllChennel():
        file_films.write(f'Индификатор(вводить при удалении): {i[0]}, Отображение: {i[1]}, Сыллка: {i[2]}\n')
    file_films.close()
    try:
        await bot.send_document(chat_id=call.from_user.id, document=open(file='data//chennal_data.txt', mode='rb'), reply_markup=ikb_close)
    except:
        await call.answer('У вас нет каналов❌')

#Принятие каллбека о добавления фильма в базу данных#
@dp.callback_query_handler(IsAdminC(), text='add_film_admin')
async def add_film_admin(call: types.Message, state: FSMContext):
    message_data=await bot.send_message(chat_id=call.from_user.id, text='Хорошо отправь мне код🔑', reply_markup=types.InlineKeyboardMarkup(row_width=1).\
        add(types.InlineKeyboardButton(text='Сгенирировать♻️', callback_data='generetion_fims_code_admin'), ikb_back_oikb))
    async with state.proxy() as data:
        data['message_id']=message_data.message_id
    await astate.Admin_State.add_film.code.set()

#обработка кнопки сгенирировать#
@dp.callback_query_handler(IsAdminC(), text='generetion_fims_code_admin', state=astate.Admin_State.add_film.code)
async def add_film_generetion_fims_code(call: types.Message, state: FSMContext):
    list_id=await only_list(kortage=await get_AllFilms(type='films_code'))
    while True:
        code=randint(0, 999)
        if code not in list_id:
            break
    async with state.proxy() as data:
        data['code']=code
    await call.message.edit_text('Хорошо теперь отправь мне название🎫')
    await call.message.edit_reply_markup(ikb_back)
    await astate.Admin_State.add_film.name.set()

#удаления канала#
@dp.callback_query_handler(IsAdminC(), text='delete_film_admin')
async def delete_film_admin(message: types.Message, state: FSMContext):
    message_data=await bot.send_message(chat_id=message.from_user.id, text='Хорошо отправь мне код фильма которго хочешь удалить🗑', reply_markup=ikb_back)
    async with state.proxy() as data:
        data['message_id']=message_data.message_id
    await astate.Admin_State.delete_film.code.set()

#добавления канала#
@dp.callback_query_handler(IsAdminC(), text='add_chennel_admin')
async def add_chennel_admin(message: types.Message, state: FSMContext):
    message_data=await bot.send_message(chat_id=message.from_user.id, text='Хорошо дайте в канале права мне "просматривать участников" и "пригласительные сыллками", после отправь мне @username или id канала которго хотите добавить➕', reply_markup=ikb_back)
    async with state.proxy() as data:
        data['message_id']=message_data.message_id
    await astate.Admin_State.add_chennel.username.set()

#удаления канала#
@dp.callback_query_handler(IsAdminC(), text='delete_chennel_admin')
async def add_chennel_admin(message: types.Message, state: FSMContext):
    message_data=await bot.send_message(chat_id=message.from_user.id, text='Хорошо дайте канал который удалить➖', reply_markup=ikb_back)
    async with state.proxy() as data:
        data['message_id']=message_data.message_id
    await astate.Admin_State.delete_chennel.username.set()

@dp.callback_query_handler(IsAdminC(), text='check_chennel_admin')
async def check_chennel_admin(message: types.Message, state: FSMContext):
    text=''
    message_data=await bot.send_message(chat_id=message.from_user.id, text='Хорошо я проверяю подождите♻️')
    me=await bot.get_me()
    me_username=me.username
    for i in await get_AllChennel():
        try:
            me_chat_status=await bot.get_chat_administrators(chat_id=i[0])
            chat_status=await bot.get_chat(chat_id=i[0])
            await bot.get_chat_member(chat_id=i[0], user_id=message.from_user.id)
            await update_nameChennel(chennel_identifier=i[0], name=chat_status.full_name)
            for e in me_chat_status:
                if e['user']['username'] == me_username:
                    if e['can_invite_users']:
                        text+=f'Канал: {i[1]} прошел проверку✅\n\n'
                    else:
                        text+=f'Канал: {i[1]} не имею доступ к сыллкам❗️\n\n'
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_data.message_id, text=f'Хорошо я проверяю подождите♻️\n\n{text}')
                    break
        except:
            await delete_Chennel(chennel_identifier=i[0])
            text+=f'Был удален {i[1]}🗑\n\n'
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_data.message_id, text=f'Хорошо я проверяю подождите♻️\n\n{text}')
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_data.message_id, text=f'Проверка закончена❇️\n\n{text}\n\nТак же если изменились название каналов то в кнопке они тоже поменяются🔰', reply_markup=ikb_close)

@dp.callback_query_handler(IsAdminC(), text='player_settings_admin')
async def settings_player(call: types.CallbackQuery):
    await call.message.edit_reply_markup(await get_Player_menu())

#вкл./выкл. плееров#
@dp.callback_query_handler(IsAdminCAndChenneger_kbname_player_admin())
async def chennger_kbname_player_admin(call: types.CallbackQuery, state: FSMContext):
    message_data1=await bot.send_message(chat_id=call.from_user.id, text='Хорошо отправь мне новое название кнопки📌', reply_markup=ikb_back)
    message_data2=call.message
    async with state.proxy() as data:
        data['message_id1']=message_data1.message_id
        data['message_id2']=message_data2.message_id
        data['name_kb']=call.data[29:]
    await astate.Admin_State.chennger_kbname_player.text.set()

@dp.callback_query_handler(IsAdminCAndChenneger_swich_player())
async def swich_player_admin(call: types.CallbackQuery):
    await swich_player(player_name=call.data[28:])
    await call.message.edit_reply_markup(await get_Player_menu())
    
@dp.callback_query_handler(IsAdminC(), text='text_settings_admin')
async def text_settings_admin(call: types.CallbackQuery):
    await call.message.edit_reply_markup(admin_menu_text)

@dp.callback_query_handler(IsAdminC(), text='chenneger_wellcome_text_settings_admin')
async def chennger_wellcome_text_settings_admin(call: types.CallbackQuery, state: FSMContext):
    message_data=await bot.send_message(chat_id=call.from_user.id, text='{username_bot}-username бота\n{bot_id}-id бота\n{username}-username пользователя\n{full_name}-полное имя пользователя\n{user_id}-id пользователя\n\nМожно ипользовать разметку MARKDOWN✂️\n\nХорошо отправь мне новое приветствие🖊', reply_markup=ikb_back)
    async with state.proxy() as data:
        data['message_id']=message_data.message_id
    await astate.Admin_State.chennger_wellcome_text.text.set()

@dp.callback_query_handler(IsAdminC(), text='chenneger_film_text_settings_admin')
async def chennger_wellcome_text_settings_admin(call: types.CallbackQuery, state: FSMContext):
    message_data=await bot.send_message(chat_id=call.from_user.id, text='{username_bot}-username бота\n{bot_id}-id бота\n{username}-username пользователя\n{full_name}-полное имя пользователя\n{user_id}-id пользователя\n{film_name}-название фильма\n{film_code}-код от фильма\n\nМожно ипользовать разметку HTML✂️\n\nХорошо отправь мне новый текст для фильмов🖊', reply_markup=ikb_back)
    async with state.proxy() as data:
        data['message_id']=message_data.message_id
    await astate.Admin_State.chennger_film_text.text.set()

