from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

balance = KeyboardButton('Баланс')
# my_wallets = KeyboardButton('Мои транзакции')


wellcome = ReplyKeyboardMarkup(resize_keyboard=True).add(balance)


send_contact = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить контакт', request_contact=True))

add_to_balance = InlineKeyboardButton(text = '+', callback_data='plus')
subt = InlineKeyboardButton(text = '-', callback_data='minus')
add_and_sub = InlineKeyboardButton(text='±', callback_data="plus_minus")
mytrans = InlineKeyboardButton(text='История моих транзакции', callback_data='my_transactions')
transactions = InlineKeyboardButton(text='Общая история транзакции', callback_data='transactions')

walletf = InlineKeyboardMarkup().add(add_to_balance,add_and_sub, subt).add(mytrans, transactions)

new_wallet = KeyboardButton('Создать кошелек')
add_to_wallet = KeyboardButton('Присоединиться к кошелку')

wallet_new_old = ReplyKeyboardMarkup(resize_keyboard=True).add(new_wallet, add_to_wallet)


cause_auto = KeyboardButton(text='Авто')
util_bills = KeyboardButton(text='Ком. Услуги')
per_expenses = KeyboardButton(text='Лич. расходы')
products = KeyboardButton(text='Продукты')
credit = KeyboardButton(text='Кредиты')
other =KeyboardButton(text='Другое')

cause_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(cause_auto, util_bills).add(per_expenses, products).add(credit, other)