import pandas as pd
import arrow
from motor import motor_asyncio as mt

async def main():
    client = mt.AsyncIOMotorClient('localhost', 27017)
    current_db = client['Wallet_db']
    collection = current_db['transaction_collection']

    # Извлечение данных из MongoDB
    cursor = collection.find()

    # Преобразование данных в список словарей
    data = [document async for document in cursor]

    print(data)
    # Преобразование списка в DataFrame
    df = pd.DataFrame(data)

    # Преобразование столбца 'date' в формат datetime
    df['date'] = pd.to_datetime(df['date'])

    # Фильтрация по месяцу
    start_date = arrow.get('2024-01-01')
    end_date = arrow.get('2024-01-31')
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Суммирование доходов и расходов
    total_income = df_filtered[df_filtered['input']]['amount'].sum()
    total_expense = df_filtered[~df_filtered['input']]['amount'].sum()

    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")

# Запуск асинхронной функции
import asyncio
asyncio.run(main())
