import csv
import os
import logging
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

file_path = Path.cwd().joinpath('uszips.csv')

con_postgres = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    host=os.getenv('POSTGRES_HOST'),
    password=os.getenv('POSTGRES_PASSWORD'),
    port=os.getenv('POSTGRES_PORT'),
)


def load_data_postgres(file_path):

    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cursor = con_postgres.cursor()
            cursor.execute(
                'INSERT INTO location_location (city, state, zip, lat, lng) VALUES (%s, %s, %s, %s, %s)',
                (row['city'], row['state_name'], row['zip'], row['lat'], row['lng'])
            )
        logger.info('Data has been loaded to postgres')
        con_postgres.commit()
        cursor.close()


load_data_postgres(file_path)