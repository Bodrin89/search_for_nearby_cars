import csv
import logging
import os
import random
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

from utils.gen_number_car import generate_custom_code

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
    """Загрузка локаций из csv в postgres."""

    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cursor = con_postgres.cursor()
            cursor.execute(
                'INSERT INTO location_location (city, state, zip, lat, lng) VALUES (%s, %s, %s, %s, %s)',
                (row['city'], row['state_name'], row['zip'], row['lat'], row['lng'])
            )
        logger.info('Данные локации загружены в postgres')
        con_postgres.commit()
        cursor.close()


def added_cars_postgres():
    """Добавление машин в postgres."""

    cursor = con_postgres.cursor()
    cursor.execute(
        """SELECT id FROM location_location ORDER BY RANDOM() LIMIT 20"""
    )
    id_locations = cursor.fetchall()

    numbers = [generate_custom_code() for _ in range(20)]

    lifting_capacities = [random.randint(1, 1000) for _ in range(20)]

    for i in range(20):
        cursor.execute(
            'INSERT INTO car_car (number, now_location_id, lifting_capacity) VALUES (%s, %s, %s)',
            (numbers[i], id_locations[i][0], lifting_capacities[i])
        )
    logger.info('Данные по машинам загружены в postgres')
    con_postgres.commit()
    cursor.close()


added_cars_postgres()
load_data_postgres(file_path)
