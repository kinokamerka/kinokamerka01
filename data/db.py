import sqlite3
from time import time

#connect к db#
sql=sqlite3.connect('data/DataBase.db')
cs=sql.cursor()

#создания таблицы юзеров#
cs.execute("""CREATE TABLE IF NOT EXISTS user_data(
    user_id INTEGER PRIMARY KEY,
    user_menotion TEXT,
    user_error_link_complaint_unix INTEGER,
    user_unix INTEGER
)""")

#создания таблицы с данными о кино#
cs.execute("""CREATE TABLE IF NOT EXISTS films_data(
    films_code TEXT PRIMARY KEY,
    films_name TEXT,
    films_priv TEXT
)""")

#создания таблицы с данными о каналов#
cs.execute("""CREATE TABLE IF NOT EXISTS chennel_data(
    chennel_identifier TEXT PRIMARY KEY,
    chennel_name TEXT,
    chennel_link TEXT
)""")

cs.execute("""CREATE TABLE IF NOT EXISTS player_data(
    player_web TEXT,
    player_name TEXT PRIMARY KEY,
    switch BOOL,
    kb_name TEXT
)""")

cs.execute("""CREATE TABLE IF NOT EXISTS text_data(
    text_type TEXT PRIMARY KEY,
    text_text TEXT
)""")

sql.commit()

try:
    data=['https://ww5.frkp.lol', 'frkp', True, 'Смотреть #1▶️']
    cs.execute("INSERT INTO player_data VALUES(?, ?, ?, ?)", data)
    sql.commit()
except:
    pass
try:
    data=['www.ggkinopoisk.ru', 'vavada', False, 'Смотреть #2▶️']
    cs.execute("INSERT INTO player_data VALUES(?, ?, ?, ?)", data)
    sql.commit()
except:
    pass

try:
    data=['wellcome', '*Привет* [{full_name}](tg://user?id={user_id}) *ты в {username_bot} это самый лучший бот по фильмом веди код фильма и можешь даже посмотреть его бесплатно😉*']
    cs.execute("INSERT INTO text_data VALUES(?, ?)", data)
    sql.commit()
except:
    pass

try:
    data=['film', '👤От: {username_bot}\n🎥Название: {film_name}']
    cs.execute("INSERT INTO text_data VALUES(?, ?)", data)
    sql.commit()
except:
    pass

async def only_list(kortage):
    lists=list()
    for i in kortage:
        lists.append(i[0])
    return lists

async def add_user(user_id, user_menotion):
    data=[user_id, user_menotion, None, time()]
    cs.execute("INSERT INTO user_data VALUES(?, ?, ?, ?)", data)
    sql.commit()

async def get_AllUser(type='*'):
    cs.execute(f"SELECT {type} FROM user_data")
    return cs.fetchall()


async def add_film(code, name, priv):
    data=[code, name, priv]
    cs.execute("INSERT INTO films_data VALUES(?, ?, ?)", data)
    sql.commit()

async def get_AllFilms(type='*'):
    cs.execute(f"SELECT {type} FROM films_data")
    return cs.fetchall()

async def get_films(code):
    cs.execute(f"SELECT * FROM films_data WHERE films_code = '{code}'")
    return cs.fetchall()

async def delete_Film(code):
    cs.execute(f"SELECT films_code FROM films_data WHERE films_code  = '{code}'")
    if cs.fetchall() == []:
        return False 
    cs.execute(f"DELETE FROM films_data WHERE films_code = '{code}'")
    sql.commit()
    return True
    #cs.execute(f'DELETE FROM bank_data WHERE invest_id = {id_invest}')

async def get_error_link_complaint_unix(user_id):
    cs.execute(f"SELECT user_error_link_complaint_unix FROM user_data")
    return cs.fetchall()[0][0]

async def update_error_link_complaint_unix(user_id, time_ub):
    cs.execute(f"UPDATE user_data SET user_error_link_complaint_unix = {time_ub} WHERE user_id = {user_id}")
    sql.commit()

async def add_Chennel(chennel_identifier, name, link):
    data=[chennel_identifier, name, link]
    cs.execute("INSERT INTO chennel_data VALUES(?, ?, ?)", data)
    sql.commit()

async def get_AllChennel(type='*'):
    cs.execute(f"SELECT {type} FROM chennel_data")
    return cs.fetchall()

async def update_nameChennel(chennel_identifier, name):
    cs.execute(f"UPDATE chennel_data SET chennel_name = '{name}' WHERE chennel_identifier = '{chennel_identifier}'")
    sql.commit()

async def delete_Chennel(chennel_identifier):
    cs.execute(f"SELECT * FROM chennel_data WHERE chennel_identifier = '{chennel_identifier}'")
    if cs.fetchall() == []:
        return False 
    cs.execute(f"DELETE FROM chennel_data WHERE chennel_identifier = '{chennel_identifier}'")
    sql.commit()
    return True

async def get_Allplayer(type='*'):
    cs.execute(f"SELECT {type} FROM player_data")
    return cs.fetchall()

async def swich_player(player_name):
    cs.execute(f"SELECT switch FROM player_data WHERE player_name = '{player_name}'")
    data_swich=cs.fetchall()[0][0]
    if data_swich == 1:
        edit=0
    elif data_swich == 0:
        edit=1
    cs.execute(f"UPDATE player_data SET switch = {edit} WHERE player_name = '{player_name}'")
    sql.commit()


async def update_kbname_player(player_name, kb):
    cs.execute(f"UPDATE player_data SET kb_name = '{kb}' WHERE player_name = '{player_name}'")
    sql.commit()

async def get_text(type, text_type):
    cs.execute(f"SELECT {type} FROM text_data WHERE text_type = '{text_type}'")
    return cs.fetchall()

async def update_wellcome_text(text, text_type):
    cs.execute(f"UPDATE text_data SET text_text = '{text}' WHERE text_type = '{text_type}'")
    sql.commit()
