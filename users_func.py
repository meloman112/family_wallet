from datetime import datetime
from pymongo import errors
from bson import ObjectId
from motor import motor_asyncio as mt




#
#
# client = mt.AsyncIOMotorClient('localhost', 27017)
#
# current_db = client['Wallet_db']
#
# collection = current_db['col_userswalet']
#

clinet = mt.AsyncIOMotorClient('mongodb+srv://wallet_user:QGJ9aeA4zgVSxO5J@cluster0.eqlglqy.mongodb.net/FamilyWallet_db?retryWrites=true&w=majority')
collection = clinet.FamilyWallet_db.Collection_users



async def add_user(data):
    date = datetime.now().date()
    info = {
        '_id': data['user_id'],
        'name': data['name'],
        'phone': data['phone'],
        'wallet_id': None,
        'date': str(date)
    }
    try:
        await collection.insert_one(info)
        return True
    except errors.DuplicateKeyError:
        return False


async def add_wallet(user_id, wallet_id):
    wallet_id_ObjectId = ObjectId(wallet_id)
    collection.update_one({'_id': user_id}, {'$set': {'wallet_id': wallet_id_ObjectId}})

async def find_user(user_id):
    user = await collection.find_one({'_id': user_id})
    return user

async def get_name(user_id):
    user = await find_user(user_id)
    name = user.get('name')
    return name
