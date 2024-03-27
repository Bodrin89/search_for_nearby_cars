import os

import psycopg2
from dotenv import load_dotenv

from config.celery import app

load_dotenv()


@app.task
def refresh_location_cars():
    con_postgres = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        host=os.getenv('POSTGRES_HOST'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('POSTGRES_PORT'),
    )
    cursor = con_postgres.cursor()

    cursor.execute("""SELECT id FROM car_car""")
    ids_cars = cursor.fetchall()

    cursor.execute("""SELECT id FROM location_location ORDER BY RANDOM() LIMIT %s""", (len(ids_cars),))
    ids_location = cursor.fetchall()

    data = zip(ids_cars, ids_location)

    for id_car, id_location in data:
        cursor.execute(
            """UPDATE car_car SET now_location_id = %s WHERE id = %s""", (id_location[0], id_car[0])
        )
    con_postgres.commit()
    cursor.close()
