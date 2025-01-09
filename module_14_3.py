from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

kl = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
kl.add(button)
kl.add(button2)

kb = InlineKeyboardMarkup(resize_keyboard=True)
button_ = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button_2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button_3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button_4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb.insert(button_)
kb.insert(button_2)
kb.insert(button_3)
kb.insert(button_4)

kp = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kp.insert(button)
kp.insert(button2)
kp.insert(button3)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('files/Product1.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product1 | Описание: описание 1 | Цена: 100p')
    with open('files/Product2.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product2 | Описание: описание 2 | Цена: 200p')
    with open('files/Product3.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product3 | Описание: описание 3 | Цена: 300p')
    with open('files/Product4.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product4 | Описание: описание 4 | Цена: 400p')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb,)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kl)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('calories = 10 * weight + 6.25 * growth - 5 * age - 161')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer('Введите свой рост:')

@dp.message_handler(state=UserState.growth)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer('Введите свой вес:')

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f'Ваша норма калорий: {calories:.2f}')
    await state.finish()

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup= kp)

@dp.message_handler()
async def all_message(message):
    await message.answer('Ввeдите команду /start,что бы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
