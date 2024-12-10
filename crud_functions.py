'''Задача "Регистрация покупателей":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.

Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
username - текст (не пустой)
email - текст (не пустой)
age - целое число (не пустой)
balance - целое число (не пустой)
add_user(username, email, age), которая принимает: имя пользователя, почту и возраст. Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными. Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.

Изменения в Telegram-бот:
Кнопки главного меню дополните кнопкой "Регистрация".
Напишите новый класс состояний RegistrationState с следующими объектами класса State: username, email, age, balance(по умолчанию 1000).
Создайте цепочку изменений состояний RegistrationState.
Фукнции цепочки состояний RegistrationState:
sing_up(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text. Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и запрашивать новое состояние для RegistrationState.username.
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
В конце завершать приём состояний при помощи метода finish().
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.

Пример результата выполнения программы:
Машина состояний и таблица Users в Telegram-bot:'''
import sqlite3


def initiate_db():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    img_name TEXT
    )    
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )    
    ''')
    connection.commit()
    connection.close()


def set_product(title,description,price,img_name):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Product (title,description,price, img_name) VALUES (?,?,?,?)",
                   (f'{title}', f'{description}', f'{price}',f'{img_name}'))
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Product")
    total = cursor.fetchall()
    connection.commit()
    connection.close()
    return total


def add_user(username, email, age):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username,email,age,balance) VALUES (?,?,?,?)",
                   (f'{username}', f'{email}', f'{age}',1000))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    check_user=cursor.execute("SELECT * FROM Users WHERE username=?",(f'{username}',))
    if check_user.fetchone() is None:
        connection.commit()
        connection.close()
        return True
    connection.commit()
    connection.close()
    return False



# Инициализация базы данных, и наполнение продуктами

#initiate_db()
#set_product("Product_A",'Самый лучший комплекс_A',100, "A.jpg")
#set_product("Product_B",'Самый лучший комплекс_B',200, "B.jpg")
#set_product("Product_C",'Самый лучший комплекс_C',300, "C.jpg")
#set_product("Product_D",'Самый лучший комплекс_D',400, "D.jpg")

#


