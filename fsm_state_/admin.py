from aiogram.dispatcher.filters.state import State, StatesGroup

#состояние админа#
class Admin_State(StatesGroup):
    class add_film(StatesGroup):
        code=State()
        name=State()
        priew=State()
    class myling_list(StatesGroup):
        text=State()
    class delete_film(StatesGroup):
        code=State()
    class add_chennel(StatesGroup):
        username=State()
        link=State()
    class delete_chennel(StatesGroup):
        username=State()
    class chennger_kbname_player(StatesGroup):
        text=State()
    class chennger_wellcome_text(StatesGroup):
        text=State()
    class chennger_wellcome_text(StatesGroup):
        text=State()
    class chennger_film_text(StatesGroup):
        text=State()
