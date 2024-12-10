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
Машина состояний и таблица Users в Telegram-bot:
.'''



from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import asyncio
import crud_functions
from module14.crud_functions import get_all_products, is_included, add_user

api="7706788533:"
bot=Bot(token=api)
dp=Dispatcher(bot,storage=MemoryStorage())
kb_menu=ReplyKeyboardMarkup(              #главное меню
    keyboard=[
        [
            KeyboardButton(text="Расчитать"),
            KeyboardButton(text="info"),
            KeyboardButton(text="Купить")
        ],
        [KeyboardButton(text="Регистрация")]
    ], resize_keyboard=True
)

kb2=InlineKeyboardMarkup(   #выбор расчет калорий или вывод формулы
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

kb_product=InlineKeyboardMarkup(   #выбор товара
    inline_keyboard=[
        [InlineKeyboardButton(text='Product_A', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_B', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_C', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_D', callback_data='product_buying')]
    ]
)




class RegistrationState(StatesGroup):
    username=State()
    email=State()
    age=State()
    balance=State()



class UserState(StatesGroup):
    growth=State()
    weight=State()
    age=State()

    #блок главного меню

@dp.message_handler(commands= ["start"])
async def main_start(message):
    await message.answer('Привет! \nВыберите опцию:', reply_markup=kb_menu)

@dp.message_handler(text="Расчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.message_handler(text= "info")
async def get_info(message):
    await message.answer('Этот бот считает каллории для мужчин, со средней физической активностью')
###
@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()



#Блок покупки товаров
@dp.message_handler(text="Купить")
async def get_buying_list(message):
    await message.answer('У вас есть возможность приобрести следующие товары:')
    all_product = get_all_products()
    for i in range(len(all_product)):    #Вынимаем из BD характеристики товаров, и соответствующие "фото"
        with open(f'{all_product[i][4]}', "rb") as img:
            await message.answer_photo(img, f'Название: {all_product[i][1]} | Описание: {all_product[i][2]} | Цена:{all_product[i][3]}')

    await message.answer('Для покупки товара нажмите на соответствующую кнопку',reply_markup=kb_product)

@dp.callback_query_handler(text= 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Продукт заказан')
    await call.answer()

#Блок расчета калорий с машинным состоянием
@dp.callback_query_handler(text= "calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()     #ждем передачи сообщения от пользователя -> Состояние age


@dp.message_handler(state=UserState.age) #как только прило сообщение, происходит событие  UserState.age
async def set_growth(message,state):

        try:
            a=float(message.text)
            await state.update_data(age=message.text)   #записываем в дата с ключом age значение age

            await message.answer('Введите свой рост:')
            await UserState.growth.set()
        except Exception:
            await message.answer('неверный формат возраста')
            await message.answer('Введите свой возраст еще раз:')
            await UserState.age.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    try:
        a = float(message.text)
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес')
        await UserState.weight.set()
    except Exception:
        await message.answer('неверный формат роста')
        await message.answer('Введите свой рост еще раз:')
        await UserState.growth.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        a = float(message.text)
        await state.update_data(weight=message.text)
        data = await state.get_data()   # получаем dat'у из записанных значений
        k_call=(10*float(data['weight'])+6.25*float(data['growth'])-5*float(data['age'])+5)*1.55
        await message.answer(f'Ваша норма каллорий: {k_call}')
        await state.finish()  #завершаем состояние
    except Exception:
        await message.answer('неверный формат веса')
        await message.answer('Введите свой вес еще раз:')
        await UserState.weight.set()



#подблок вывода формулы рачсета каллорий
@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('call=10*weight(kg)+6.25*growth(cm)-5*age(y)+5)*1.55')
    await call.answer()


###Регистрация пользователя

@dp.message_handler(state=RegistrationState.username) #как только прилшло сообщение о "username", происходит событие  RegistrationState.username
async def set_username(message,state):
    if is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email')
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)  # как только прилшло сообщение о "email", происходит событие  RegistrationState.email
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)  # как только прилшло сообщение о "age", происходит событие  RegistrationState.age
async def set_user(message, state):
    try:
        a = float(message.text)
        await state.update_data(age=message.text)
        data = await state.get_data()  # получаем dat'у из записанных значений
        print(data)
        us_name=data['username']
        add_user(us_name,data['email'],int(data['age']))
        await message.answer(f'Пользователь {us_name} зарегистрирован')
        await state.finish()  # завершаем состояние
    except Exception:
        await message.answer('неверный формат Возраста')
        await message.answer('Введите свой возраст еще раз:')
        await RegistrationState.age.set()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)