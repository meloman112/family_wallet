import pytz
from motor import motor_asyncio as mt
from datetime import datetime
import asyncio
import time
import pymongo
# clinet = mt.AsyncIOMotorClient('mongodb+srv://wallet_user:QGJ9aeA4zgVSxO5J@cluster0.eqlglqy.mongodb.net/FamilyWallet_db?retryWrites=true&w=majority')
# collection = clinet.FamilyWallet_db.Collection_wallet
#

client = mt.AsyncIOMotorClient('localhost', 27017)

current_db = client['Wallet_db']

collection = current_db['wallets']


async def new_wallet(user_id, balance: int):
    date = datetime.now(pytz.UTC)
    trans_info = {
        'users_id': [user_id],
        'balance': balance,
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




async def main():
   aa = await new_trans(123456, 321, False)
   print(aa['_id'])

if __name__ == '__main__':
    asyncio.run(main())