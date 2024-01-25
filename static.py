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


clinet = mt.AsyncIOMotorClient('mongodb+srv://wallet_user:QGJ9aeA4zgVSxO5J@cluster0.eqlglqy.mongodb.net/FamilyWallet_db?retryWrites=true&w=majority')
collection = clinet.FamilyWallet_db.Collection_Transactions



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
    causes, amounts = await create_lists(filter_transactions)

    # Суммирование расходов по причинам
    result = await sum_by_cause(causes, amounts)

    plt.pie(list(result.values()), labels=list(result.keys()), autopct='%1.1f%%')
    plt.savefig('circle_diogram.png')

    return result

async def plot(target_month, wallet_id):
    transactions = await get_income(wallet_id)

    filter_transactions = [record for record in transactions if record['date'].month == target_month]



    causes, amounts = await create_list_imcome(filter_transactions)
    names = []
    for name in causes:
        names.append(await get_name(name))

    # Суммирование расходов по причинам
    result = await sum_by_cause(names, amounts)

    plt.pie(list(result.values()), labels=list(result.keys()), autopct='%1.1f%%')
    plt.savefig('circle_diogram_income.png')
    #pprint(result)
    return result




# Функция для создания списков причин и сумм расходов
async def create_lists(records):
    causes = []
    amounts = []

    for record in records:
        causes.append(record['cause'])
        amounts.append(record['amount'])

    return causes, amounts
async def create_list_imcome(records):
    causes = []
    amounts = []

    for record in records:
        causes.append(record['user_id'])
        amounts.append(record['amount'])

    return causes, amounts

# Функция для суммирования расходов по причинам
async def sum_by_cause(causes, amounts):
    cause_amount_dict = defaultdict(int)

    for cause, amount in zip(causes, amounts):
        cause_amount_dict[cause] += amount

    return cause_amount_dict


async def main():
    pprint(await plot(target_month=1, wallet_id=bson.ObjectId('65b215d16b50ac628335fbec')))
if __name__ == '__main__':
    asyncio.run(main())