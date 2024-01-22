from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bottons import wellcome, send_contact, walletf, wallet_new_old, cause_buttons
from wallet_func import *
from transactions import *
from users_func import *

Channel_id = -1002014290958

stroge = MemoryStorage()

API_TOKEN = '6872524495:AAFJJrdbgJUEoRBvDRg1oYgI6wosMDybV5U'  # BOT_FATHER
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=stroge)

# clinet = mt.AsyncIOMotorClient('mongodb+srv://wallet_user:QGJ9aeA4zgVSxO5J@cluster0.eqlglqy.mongodb.net/FamilyWallet_db?retryWrites=true&w=majority')
# collection = clinet.FamilyWallet_db.Collection_wallet


class User_data(StatesGroup):
    _id = State()
    name = State()
    phone = State()


class Operation(StatesGroup):
    plus = State()
    minus = State()
    plus_minus = State()


class WalletAdd(StatesGroup):
    add_wal = State()
    minus = State()

class CausesGroup(StatesGroup):
    user_id = State()
    Wallet_id = State()
    cause = State()




@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    name = message.from_user.first_name
    user_id = message.from_user.id
    user = await find_user(user_id)
    if not user:
        await message.reply(f"Ассалаума алейкум {name}")
        await message.answer('Как вас звать?')
        await User_data.name.set()
    else:
        await message.answer(f'Ассалаума алейкум, с возравщением {user["name"]}', reply_markup=wellcome)


@dp.message_handler(state=User_data.name)
async def ask_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['name'] = message.text
        await message.answer('Поделитесь своим контактом. Нажмите кнопку (Отправить контакт)',
                             reply_markup=send_contact)
        await User_data.phone.set()


@dp.message_handler(state=User_data.phone, content_types=types.ContentType.CONTACT)
async def ask_name(message: types.Message, state: FSMContext):
    contact = message.contact
    async with state.proxy() as data:
        data['phone'] = contact.phone_number
        new_user = await add_user(data)
        if new_user:
            await message.answer('Регистрация завершена', reply_markup=wallet_new_old)
        await state.finish()


@dp.message_handler(text='Создать кошелек')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    wallet_exists = await check_wallet_existence(user_id)
    # print(wallet_exists)
    if not wallet_exists:
        wallet = await new_wallet(user_id)
        await add_wallet(user_id, wallet['_id'])
        await message.answer(f'Ваш кошелек создан, ID - {wallet["_id"]}', reply_markup=wellcome)
    else:
        await message.answer(f'Вы уже имеете кошелек ID - {wallet_exists["_id"]}', reply_markup=wellcome)


@dp.message_handler(text='Присоединиться к кошелку')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    wallet_exists = await check_wallet_existence(user_id)
    if not wallet_exists:
        await message.answer(f'Введите ID кошелька')
        await WalletAdd.add_wal.set()
    else:
        await message.answer(f'У вас уже есть кошелек ID {wallet_exists["_id"]}', reply_markup=wellcome)


@dp.message_handler(state=WalletAdd.add_wal)
async def ask_name(message: types.Message, state: FSMContext):
    user_id = (message.from_user.id)
    wallet_id = message.text
    wallet = await new_user_wallet(wallet_id, user_id)
    if wallet:
        await message.answer(f'Вы добавлены к кошельку {wallet_id}', reply_markup=wellcome)
        await add_wallet(user_id, wallet_id)
        await state.finish()
    else:
        await message.answer(f'Кошелек {wallet_id} не найден.\nВведите корректное ID кошелька:')
        await WalletAdd.add_wal.set()


@dp.message_handler(text='Баланс')
async def get_balance_handler(message: types.Message):
    user_id = message.from_user.id
    user_document = await find_user(user_id)
    wallet_id = user_document.get('wallet_id')
    if not wallet_id:
        await message.answer("У вас нет кошелька. Пожалуйста, создайте его или присоединитесь к существующему.",
                             reply_markup=wallet_new_old)
    else:
        await bot.delete_message(message.chat.id, message_id=message.message_id)
        balance = await get_balance(wallet_id)
        await message.answer(f'Ваш баланс - {balance}', reply_markup=walletf)





@dp.message_handler(state=Operation.minus)
async def minus_to_balance(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_document = await find_user(user_id)
    wallet_id = user_document.get('wallet_id')
    if not wallet_id:
        await message.answer("У вас нет кошелька. Пожалуйста, создайте его.")
        await state.finish()
        return

    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Введите корректную сумму.")
        await Operation.minus.set()
        return

    balance = await subtract_from_balance(wallet_id, amount)

    if balance == 'недостаточно средств на балансе':
        await message.answer('недостаточно средств на балансе')
        await Operation.minus.set()
    else:
        async with state.proxy() as data:
            data['amount'] = amount
            data['user_id'] = user_id
            data['wallet_id'] = wallet_id
        await message.answer(f'Выберите, причину расхода', reply_markup=cause_buttons)
        await CausesGroup.cause.set()





@dp.message_handler(state=Operation.plus_minus)
async def plus_to_balance(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_document = await find_user(user_id)
    wallet_id = user_document.get('wallet_id')
    if not wallet_id:
        await message.answer("У вас нет кошелька. Пожалуйста, создайте его.")
        await state.finish()
        return
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Введите корректную сумму.")
        await Operation.plus_minus.set()
        return

    balance = await add_to_wallet(wallet_id, amount)
    transaction = await new_trans(wallet_id, user_id, amount, None, True)
    name = await get_name(transaction["user_id"])
    await bot.send_message(chat_id=Channel_id, text=f'🟢🟢🟢ПРИХОД🟢🟢🟢\n'
                                                    f'Автор - {name}\n'
                                                    f'Cумма - {transaction["amount"]}\n'
                                                    f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}')

    balance_minus = await subtract_from_balance(wallet_id, amount)
    async with state.proxy() as data:
        data['amount'] = amount
        data['user_id'] = user_id
        data['wallet_id'] = wallet_id
    await message.answer(f'Выберите, причину расхода', reply_markup=cause_buttons)
    await CausesGroup.cause.set()




@dp.message_handler(state=Operation.plus)
async def plus_to_balance(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    user_document = await find_user(user_id)

    wallet_id = user_document.get('wallet_id')
    if not wallet_id:
        await message.answer("У вас нет кошелька. Пожалуйста, создайте его.")
        await state.finish()
        return

    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Введите корректную сумму.")
        await Operation.plus.set()

        return

    balance = await add_to_wallet(wallet_id, amount)
    await message.answer(f'Ваш баланс - {balance}', reply_markup=walletf)
    transaction = await new_trans(wallet_id, user_id, amount, None, True)
    name = await get_name(transaction["user_id"])
    await bot.send_message(chat_id=Channel_id, text=f'ПРИХОД\n'
                                                    f'Автор - {name}\n'
                                                    f'Cумма - {transaction["amount"]}\n'
                                                    f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}')

    await state.finish()


@dp.message_handler(state=CausesGroup.cause)
async def select_casuses(message: types.Message, state: FSMContext):
    cause = message.text
    async with state.proxy() as data:
        print(data)

        transaction = await new_trans(wallet_id=data['wallet_id'], user_id=data['user_id'], amount=data['amount'], cаuse=cause, input=False)
        name = await get_name(transaction["user_id"])
        await bot.send_message(chat_id=Channel_id, text=f'*🔴🔴🔴РАСХОД🔴🔴🔴*\n'
                                                        f'Автор - {name}\n'
                                                        f'Cумма - {transaction["amount"]}\n'
                                                        f'Причина - {cause}\n'
                                                        f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}',
                               parse_mode="Markdown")
        balance = await get_balance(data['wallet_id'])
        await message.answer('Расход успешно внесен', reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Ваш баланс - {balance}', reply_markup=walletf)

        await state.finish()


@dp.callback_query_handler(lambda callback_query: True)
async def handle_callback_query(callback_query: types.CallbackQuery, state:FSMContext):
    # Обработка нажатия на кнопку
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.message.chat.id
    user_document = await find_user(user_id)
    wallet_id = user_document.get('wallet_id')

    # В зависимости от того, какая кнопка была нажата, выполняется соответствующее действие
    if callback_query.data == 'plus':
        await bot.send_message(callback_query.message.chat.id, 'Введите сумму пополнения')
        await Operation.plus.set()
    elif callback_query.data == 'plus_minus':
        await bot.send_message(callback_query.message.chat.id, f'Введите сумму расхода')
        await Operation.plus_minus.set()
    elif callback_query.data == 'minus':
        await bot.send_message(callback_query.message.chat.id, f'Введите сумму расхода')
        await Operation.minus.set()
    elif callback_query.data == 'transactions':
        user_document = await find_user(user_id)
        wallet_id = user_document['wallet_id'] if user_document else None

        if wallet_id:
            transactions = await (get_wallet_id(wallet_id) if callback_query.data == 'transactions' else get_user_id(user_id=user_id))

            for trans in transactions:
                name = await get_name(trans["user_id"])
                operation_type = "ПРИХОД" if trans["input"] else "РАСХОД"
                await callback_query.message.answer(
                    f'{operation_type}\n'
                    f'Автор - {name}\n'
                    f'Cумма - {trans["amount"]}\n'
                    f'Дата - {trans["date"].strftime("%Y-%m-%d %H:%M:%S")}'
                )

            income = await get_income_or_expense(wallet_id, True)
            expense = await get_income_or_expense(wallet_id, False)
            await callback_query.message.answer(f'ПРИХОД  - {income}\nРАСХОД - {expense}')
        else:
            await callback_query.message.answer("У вас нет кошелька. Пожалуйста, создайте его.")
    elif callback_query.data == 'my_transactions':
        transactions = await get_user_id(user_id=user_id)
        for trans in transactions:
            name = await get_name(trans["user_id"])
            await callback_query.message.answer(f'{"ПРИХОД" if trans["input"] else "РАСХОД"}\n'
                                                f'Автор - {name}\n'
                                                f'Cумма - {trans["amount"]}\n'
                                                f'Дата - {trans["date"].strftime("%Y-%m-%d %H:%M:%S")}')
        income = await get_user_incexp(user_id, True)
        expense = await get_user_incexp(user_id, False)
        await callback_query.message.answer(f'ПРИХОД  - {income}\nРАСХОД - {expense}')

    #
    # elif callback_query.data == 'auto':
    #     async with state.proxy() as data:
    #         print(data)
    #
    #
    #         transaction = await new_trans(wallet_id=wallet_id, user_id=user_id, amount=data['amount'],cаuse='auto', input=False)
    #         name = await get_name(transaction["user_id"])
    #         await bot.send_message(chat_id=Channel_id, text=f'*🔴🔴🔴РАСХОД🔴🔴🔴*\n'
    #                                                         f'Автор - {name}\n'
    #                                                         f'Cумма - {transaction["amount"]}\n'
    #                                                         f'Причина - Для авто\n'
    #                                                         f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}',
    #                                parse_mode="Markdown")
    #
    #         await state.finish()
    # elif callback_query.data == 'products':
    #     async with state.proxy() as data:
    #
    #
    #         transaction = await new_trans(wallet_id=wallet_id, user_id=user_id, amount=data['amount'],cаuse='products', input=False)
    #         name = await get_name(transaction["user_id"])
    #         await bot.send_message(chat_id=Channel_id, text=f'*🔴🔴🔴РАСХОД🔴🔴🔴*\n'
    #                                                         f'Автор - {name}\n'
    #                                                         f'Cумма - {transaction["amount"]}\n'
    #                                                         f'Причина - Продукты\n'
    #                                                         f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}',
    #                                parse_mode="Markdown")
    #
    #         await state.finish()
    # elif callback_query.data == 'pers_expenses':
    #     async with state.proxy() as data:
    #
    #
    #         transaction = await new_trans(wallet_id=wallet_id, user_id=user_id, amount=data['amount'],cаuse='pers_expnsees', input=False)
    #         name = await get_name(transaction["user_id"])
    #         await bot.send_message(chat_id=Channel_id, text=f'*🔴🔴🔴РАСХОД🔴🔴🔴*\n'
    #                                                         f'Автор - {name}\n'
    #                                                         f'Cумма - {transaction["amount"]}\n'
    #                                                         f'Причина - Личные расходы\n'
    #                                                         f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}',
    #                                parse_mode="Markdown")
    #
    #         await state.finish()
    # elif callback_query.data == 'utility_bills':
    #     async with state.proxy() as data:
    #
    #
    #         transaction = await new_trans(wallet_id=wallet_id, user_id=user_id, amount=data['amount'],cаuse='utility_bills', input=False)
    #         name = await get_name(transaction["user_id"])
    #         await bot.send_message(chat_id=Channel_id, text=f'*🔴🔴🔴РАСХОД🔴🔴🔴*\n'
    #                                                         f'Автор - {name}\n'
    #                                                         f'Cумма - {transaction["amount"]}\n'
    #                                                         f'Причина - Коммунальные услуги\n'
    #                                                         f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}',
    #                                parse_mode="Markdown")
    #
    #         await state.finish()
    # elif callback_query.data == 'credits':
    #     async with state.proxy() as data:
    #
    #
    #         transaction = await new_trans(wallet_id=wallet_id, user_id=user_id, amount=data['amount'],cаuse='credits', input=False)
    #         name = await get_name(transaction["user_id"])
    #         await bot.send_message(chat_id=Channel_id, text=f'*🔴🔴🔴РАСХОД🔴🔴🔴*\n'
    #                                                         f'Автор - {name}\n'
    #                                                         f'Cумма - {transaction["amount"]}\n'
    #                                                         f'Причина - Кредит\n'
    #                                                         f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}',
    #                                parse_mode="Markdown")
    #
    #         await state.finish()
    # elif callback_query.data == 'others':
    #     print('----1212----')
    #     async with state.proxy() as data:
    #         print(data)
    #
    #
    #         transaction = await new_trans(wallet_id=wallet_id, user_id=user_id, amount=data['amount'],cаuse='others', input=False)
    #         name = await get_name(transaction["user_id"])
    #         await bot.send_message(chat_id=Channel_id, text=f'*🔴🔴🔴РАСХОД🔴🔴🔴*\n'
    #                                                         f'Автор - {name}\n'
    #                                                         f'Cумма - {transaction["amount"]}\n'
    #                                                         f'Причина - Другое\n'
    #                                                         f'Дата - {transaction["date"].strftime("%Y-%m-%d %H:%M:%S")}',
    #                                parse_mode="Markdown")
    #
    #         await state.finish()


async def send_message(user_id, text: str):
    await bot.send_message(user_id, text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
