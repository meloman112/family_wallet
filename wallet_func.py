from motor import motor_asyncio as mt
from datetime import datetime
from pprint import pprint
import asyncio
import pymongo
from users_func import add_wallet
# clinet = mt.AsyncIOMotorClient('mongodb+srv://wallet_user:QGJ9aeA4zgVSxO5J@cluster0.eqlglqy.mongodb.net/FamilyWallet_db?retryWrites=true&w=majority')
# collection = clinet.FamilyWallet_db.Collection_wallet

from bson import ObjectId


client = mt.AsyncIOMotorClient('localhost', 27017)

current_db = client['Wallet_db']

collection = current_db['wallets']


async def new_wallet(user_id):
    date = datetime.now()
    trans_info = {
        'users_id': [user_id],
        'balance': 0,
        'date': date
    }
    await collection.insert_one(trans_info)
    return trans_info


async def new_user_wallet(wallet_id, user_id):
    if ObjectId.is_valid(wallet_id):
        wallet_id_ObjectId = ObjectId(wallet_id)
        find_and_update = await collection.update_one({'_id': wallet_id_ObjectId}, {"$push": {"users_id": user_id}})
        print(find_and_update.matched_count, find_and_update.modified_count)
        return True
    else:
        return False




async def check_wallet_existence(user_id):
    wallet = await collection.find_one({'users_id': {'$in': [user_id]}})
    return wallet if False else wallet


async def add_to_wallet(wallet_id, amount: int):
    wallet = await collection.find_one({'_id': wallet_id})

    if wallet:
        await collection.update_one({'_id': wallet_id}, {'$inc': {'balance': amount}})
        return wallet.get('balance') + amount


async def subtract_from_balance(wallet_id, amount: int):
    wallet = await collection.find_one({'_id': wallet_id})

    if wallet.get('balance') >= amount:
        await collection.update_one({'_id': wallet_id}, {'$inc': {'balance': -amount}})
        return wallet.get('balance') - amount
    else:
        return 'недостаточно средств на балансе'


async def get_balance(wallet_id):
    wallet = await collection.find_one({'_id': wallet_id})
    return wallet['balance']

# async def main():
#     ea = collection.find_one({'_id': '502419529_10_48_33'})
#     print(ea)

# if __name__ == '__main__':
#     asyncio.run(main())
