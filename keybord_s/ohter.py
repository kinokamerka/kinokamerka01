from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#Кнопки отмена и закрыть#
ikb_back_oikb=InlineKeyboardButton(text='Отмена❌', callback_data='cancellation_state')
ikb_back=InlineKeyboardMarkup().row(ikb_back_oikb)

ikb_close_oikb=InlineKeyboardButton(text='Закрыть❎', callback_data='close_text')
ikb_close=InlineKeyboardMarkup().row(ikb_close_oikb)
