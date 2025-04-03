import json
from sqlalchemy import create_engine, text
import pandas as pd
import local_settings, prompt
import deepseek

def result_data(data, result_type):
    key = f'```{result_type}'
    start = data.find(key)
    if start != -1:
        key = f'```'
        start = data.find(key)
    end = data.find('```', start + len(key))
    return data[start:end] if start != -1 and end != -1 else ""

def fetch_sql_answer(question):
    try:
        sql_answer = deepseek._ask(f'Question: {question} SQL Query:', prompt.sql)
        print(sql_answer)
        sql_data = result_data(sql_answer, 'sql')
        return sql_data
    except Exception as e:
        print(f"Error fetching SQL answer: {e}")
        return None

def fetch_protector_data(sql_data):
    try:
        protector_answer = deepseek._ask(sql_data, prompt.protector)
        print(protector_answer)
        protector_data = result_data(protector_answer, 'json')
        return json.loads(protector_data)
    except Exception as e:
        print(f"Error fetching protector data: {e}")
        return None

def get_data_from_db(engine,sql_data):
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(sql_data), conn)
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        print(sql_data)
        return None

def main():
    # Инициализация подключения к БД
    engine = create_engine(f'postgresql://{local_settings.POSTGRES_USER}:{local_settings.POSTGRES_PASSWORD}@{local_settings.POSTGRES_HOST}:{local_settings.POSTGRES_PORT}/{local_settings.POSTGRES_DB}')
    
    # Получаем вопрос от пользователя
    question = input("Введите вопрос: ")

    # Получаем SQL запрос
    sql_data = fetch_sql_answer(question)
    if not sql_data:
        print("Ошибка при получении SQL запроса.")
        return

    # Проверяем SQL запрос
    protector_data = fetch_protector_data(sql_data)
    if not protector_data or protector_data.get("answer") != 'safe':
        print("Ошибка данные небезопасны.")
        return

    # Выполняем запрос к базе данных
    df = get_data_from_db(engine,sql_data)
    if df is None:
        print("Ошибка при выполнении SQL запроса.")
        return

    # Формируем ответ
    user_text = {"question": question, "sql_data": sql_data, "protector_data": protector_data, "df": str(df)}
    text_answer = deepseek._ask(str(user_text), prompt.text)
    print(text_answer)

if __name__ == "__main__":
    main()
