from loader import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from myFilters.admin import IsAdminM
from fsm_state_ import admin as astate
from data.db import add_film, only_list, get_AllUser, delete_Film, add_Chennel, delete_Chennel, update_kbname_player, update_wellcome_text
from keybord_s.admin import get_Player_menu
from keybord_s.ohter import ikb_back, ikb_close



@dp.channel_post_handler()
async def get_id(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=message.chat.id)

#рассылка#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.myling_list.text, content_types=types.ContentTypes.ANY)
async def myling_list(message: types.Message, state: FSMContext):
    msg_myling=message.message_id
    async with state.proxy() as data:
        data_user=await only_list(await get_AllUser(type='user_id'))
        count_accept=0
        count_error=0
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=f'*Данные о рассылки\nТекст: "{message.text}"\n✅Успешно: {count_accept}\n❌Ошибки: {count_error}*', parse_mode=types.ParseMode.MARKDOWN)
        for i in data_user:
            try:
                await bot.copy_message(chat_id=message.from_user.id, from_chat_id=i, message_id=msg_myling, parse_mode=types.ParseMode.MARKDOWN)
                count_accept+=1
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=f'*Данные о рассылки\nТекст: "{message.text}"\n✅Успешно: {count_accept}\n❌Ошибки: {count_error}*', parse_mode=types.ParseMode.MARKDOWN)
            except:
                count_error+=1
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=f'*Данные о рассылки\nТекст: "{message.text}"\n✅Успешно: {count_accept}\n❌Ошибки: {count_error}*', parse_mode=types.ParseMode.MARKDOWN)
        await message.delete()
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=f'*Данные о рассылки\nТекст: "{message.text}"\n✅Успешно: {count_accept}\n❌Ошибки: {count_error}\nРассылка завершенна🔔*', parse_mode=types.ParseMode.MARKDOWN, reply_markup=ikb_close)
    await state.finish()

#получения кода от фильма#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_film.code)
async def state_add_film_code(message: types.Message, state: FSMContext):
    
    async with state.proxy() as data:
        data['code']=message.text
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Хорошо теперь отправь мне название🎫', reply_markup=ikb_back)
    await astate.Admin_State.add_film.name.set()

#получение название от фильма#
@dp.message_handler(IsAdminM(),state=astate.Admin_State.add_film.name)
async def state_add_film_name(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['name']=message.text
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Отлично теперь отправь мне фотографии для обложки📌')
    await astate.Admin_State.add_film.priew.set()

#палучение обложки и сохранение данных#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_film.priew, content_types=types.ContentTypes.PHOTO)
async def state_add_film_priew(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.chat.id, message_id=data['message_id'])
        try:
            await add_film(code=data['code'], name=data['name'], priv=message.photo[-1].file_id)
            await message.answer_photo(photo=message.photo[-1].file_id, caption=f'📌Фильм добавлен\n🔑Код: {data["code"]}\n🎫Название: {data["name"]}', reply_markup=ikb_close)
        except:
            await message.answer('Скорее всего этот код уже добавлен')
    await state.finish()

#если не фотография#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_film.priew)
async def state_add_film_priew_no_photo(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Жду фотографию😡\nОтлично теперь отправь мне фотографии для обложки📌', reply_markup=ikb_back)
        except:
            pass

#удаления фильма#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.delete_film.code)
async def delete_film(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            chennel_identifier=int(message.text)
        except:
            chennel_identifier=message.text
        if await delete_Film(code=chennel_identifier):
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Успешно удалено❎', reply_markup=ikb_close)
            await state.finish()
        else:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Нет токого кода❌', reply_markup=ikb_back)
            except:
                pass

@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_chennel.username)
async def add_chennel(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            chennel_identifier=int(message.text)
        except:
            chennel_identifier=message.text
        try:
            await bot.get_chat_member(chat_id=chennel_identifier, user_id=message.from_user.id)
            chat=await bot.get_chat(chat_id=chennel_identifier)
            me=await bot.get_me()
            link_chat=await bot.create_chat_invite_link(chat_id=chennel_identifier, name=f'Вход от {me.mention}')
            try:
                await add_Chennel(chennel_identifier=chennel_identifier, name=chat.full_name, link=link_chat.invite_link)
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Канал успешно добавлен✅', reply_markup=ikb_close)
                await state.finish()
            except:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Этот канал уже был добавлен🫤', reply_markup=ikb_back)
        except:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Извините у меня там нет прав "просматривать участников" и "управления сыллками"❌', reply_markup=ikb_back)
            except:
                pass

@dp.message_handler(IsAdminM(), state=astate.Admin_State.delete_chennel.username)
async def delete_chennel(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        if await delete_Chennel(chennel_identifier=message.text):
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Канал удален успешно✅', reply_markup=ikb_close)
            await state.finish()
        else:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Извините вы не добавляли такого канал❌', reply_markup=ikb_back)
    
@dp.message_handler(IsAdminM(), state=astate.Admin_State.chennger_kbname_player.text)
async def chennger_kbname_player(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await update_kbname_player(player_name=data['name_kb'], kb=message.text)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id1'], text='Кнопка изменена успешно✅', reply_markup=ikb_close)
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=data['message_id2'], reply_markup=await get_Player_menu())
        await state.finish()

@dp.message_handler(IsAdminM(), state=astate.Admin_State.chennger_wellcome_text.text)
async def chennger_wellcome_text(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=message.text, parse_mode=types.ParseMode.MARKDOWN)
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Успешно изминил текст приветствия✅', reply_markup=ikb_close)
            await state.finish()
            await update_wellcome_text(text_type='wellcome', text=message.text)
        except:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Не правильная разметка MARKDOWN✂️', reply_markup=ikb_back)
            except:
                pass

@dp.message_handler(IsAdminM(), state=astate.Admin_State.chennger_film_text.text)
async def chennger_wellcome_text(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=message.text, parse_mode=types.ParseMode.MARKDOWN)
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Успешно изминил текст фильма✅', reply_markup=ikb_close)
            await update_wellcome_text(text_type='film', text=message.text)
            await state.finish()
        except:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Не правильная разметка MARKDOWN✂️', reply_markup=ikb_back)
            except:
                pass
