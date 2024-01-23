import bson
from collections import defaultdict

import pytz
from motor import motor_asyncio as mt
from datetime import datetime
import asyncio
import time
from pprint import pprint
import pymongo
import matplotlib.pyplot as plt
from users_func import get_name

client = mt.AsyncIOMotorClient('localhost', 27017)

current_db = client['Wallet_db']

collection = current_db['transaction_collection']


async def get_expenses(wallet_id):
    transactions_cursor = collection.find({'input': False, 'wallet_id': wallet_id})
    transactions = await transactions_cursor.to_list(length=None)
    return transactions


async def get_income(wallet_id):
    transactions_cursor = collection.find({'input': True, 'wallet_id': wallet_id})
    transactions = await transactions_cursor.to_list(length=None)
    return transactions

async def create_circle(target_month, wallet_id):
    transactions = await get_expenses(wallet_id)
    filter_transactions = [record for record in transactions if record['date'].month == target_month]
    causes, amounts = create_lists(filter_transactions)

    # Суммирование расходов по причинам
    result = sum_by_cause(causes, amounts)

    plt.pie(list(result.values()), labels=list(result.keys()), autopct='%1.1f%%')
    plt.savefig('circle_diogram.png')

    return result

async def plot(target_month, wallet_id):
    transactions = await get_income(wallet_id)

    filter_transactions = [record for record in transactions if record['date'].month == target_month]



    causes, amounts = create_list_imcome(filter_transactions)
    names = []
    for name in causes:
        names.append(await get_name(name))
    print(names)
    # Суммирование расходов по причинам
    result = sum_by_cause(names, amounts)

    plt.pie(list(result.values()), labels=list(result.keys()), autopct='%1.1f%%')
    plt.savefig('circle_diogram_income.png')

    return result




# Функция для создания списков причин и сумм расходов
def create_lists(records):
    causes = []
    amounts = []

    for record in records:
        causes.append(record['cаuse'])
        amounts.append(record['amount'])

    return causes, amounts
def create_list_imcome(records):
    causes = []
    amounts = []

    for record in records:
        causes.append(record['user_id'])
        amounts.append(record['amount'])

    return causes, amounts

# Функция для суммирования расходов по причинам
def sum_by_cause(causes, amounts):
    cause_amount_dict = defaultdict(int)

    for cause, amount in zip(causes, amounts):
        cause_amount_dict[cause] += amount

    return cause_amount_dict
#
#
# async def main():
#     print(await plot(target_month=1, wallet_id=bson.ObjectId('65a2b6104216000d5c688cb5')))
# if __name__ == '__main__':
#     asyncio.run(main())