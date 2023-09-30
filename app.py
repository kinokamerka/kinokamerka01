from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from loader import dp, bot, admin_id
from heandlers import dp
from keybord_s.ohter import ikb_close

#отмена любого состаяния#
@dp.callback_query_handler(text='cancellation_state', state='*')
async def cancellation_state(call: types.Message, state: FSMContext):
    await state.finish()
    await call.answer('Отмена❌')
    await call.message.delete()

#закрыть#
@dp.callback_query_handler(text='close_text')
async def cancellation_state(call: types.Message):
    await call.message.delete()

#уведомления о запуске#
async def satrt_nofication(self):
    try:
        me=await bot.get_me()
        print(f'Твой бот {me.mention} работает.')
    except:
        print(f'Твой бот {me.mention} работает.')
        print('Вы не нажали /start в сеом боте!')

executor.start_polling(dp, on_startup=satrt_nofication)
