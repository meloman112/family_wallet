import pytz
from motor import motor_asyncio as mt
from datetime import datetime
import asyncio
import time
from pprint import pprint
import pymongo
# clinet = mt.AsyncIOMotorClient('mongodb+srv://wallet_user:QGJ9aeA4zgVSxO5J@cluster0.eqlglqy.mongodb.net/FamilyWallet_db?retryWrites=true&w=majority')
# collection = clinet.FamilyWallet_db.Collection_wallet

from bson import ObjectId

client = mt.AsyncIOMotorClient('localhost', 27017)

current_db = client['Wallet_db']

collection = current_db['transaction_collection']


async def new_trans(wallet_id, user_id, amount: int, cаuse,  input: bool):
    print('------------------------success-----------------')
    date = datetime.now(pytz.UTC)
    trans_info = {
        'wallet_id': wallet_id,
        'user_id': user_id,
        'amount': amount,
        'cаuse': cаuse,
        'input': input,
        'date': date
    }
    await collection.insert_one(trans_info)
    return trans_info


async def get_user_id(user_id):
    trasac = collection.find({'user_id': user_id})
    results = await trasac.to_list(length=None)
    return results


async def get_id(user_id):
    trasac = await collection.find_one({'_id': user_id})
    return trasac


async def get_wallet_id(wallet_id):
    trasac = collection.find({'wallet_id': wallet_id})
    results = await trasac.to_list(length=None)
    return results


async def get_income_or_expense(wallet_id, input: bool):
    transactions_cursor = collection.find({'wallet_id': wallet_id, 'input': input})
    transactions = await transactions_cursor.to_list(length=None)
    all_income = 0
    for transaction in transactions:
        all_income += transaction['amount']
    return all_income


async def get_user_incexp(user_id, input: bool):
    transactions_cursor = collection.find({'input': input, 'user_id': user_id})
    transactions = await transactions_cursor.to_list(length=None)
    all_income = 0
    for transaction in transactions:
        all_income += transaction['amount']
    return all_income

async def get_income_of_date(wallet_id, year, month, input: bool):
    # Определяем начало и конец месяца для поиска
    start_date = datetime(year, month, 1, 0, 0, 0)
    end_date = datetime(year, month + 1, 1, 0, 0, 0) if month < 12 else datetime(year + 1, 1, 1, 0, 0, 0)

    # Формируем запрос и сортируем результаты по дате в порядке убывания
    transactions_cursor = collection.find({
        'wallet_id': wallet_id,
        'date': {'$gte': start_date, '$lt': end_date},
        'input': input  # Уточните это условие, если необходимо
    }).sort('date', pymongo.DESCENDING)
    # Получаем список транзакций и считаем сумму
    transactions = await transactions_cursor.to_list(length=None)
    pprint(transactions)
    total_income = sum(transaction['amount'] for transaction in transactions)

    return total_income
#
#
# async def main():
#     income = await get_income_of_date(ObjectId('65a2b6104216000d5c688cb5'), 2024, 1, True)
#     expanse = await get_income_of_date(ObjectId('65a2b6104216000d5c688cb5'), 2024, 1, False)
#
#     print(income - expanse)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
