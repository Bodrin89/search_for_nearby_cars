import random


def generate_custom_code():
    random_number = random.randint(1000, 9999)
    random_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return f'{random_number}{random_letter}'
