import local_settings
import pandas as pd
from sqlalchemy import create_engine

if __name__ == '__main__':
    engine = create_engine(f'postgresql://{local_settings.POSTGRES_USER}:{local_settings.POSTGRES_PASSWORD}@{local_settings.POSTGRES_HOST}:{local_settings.POSTGRES_PORT}/{local_settings.POSTGRES_DB}')
    df = pd.read_csv('freelancer_earnings_bd.csv')
    # Загрузка данных в PostgreSQL
    df.to_sql('freelancers', engine, if_exists='replace', index=False)