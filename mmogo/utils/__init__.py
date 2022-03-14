import string
import random
from mmogo.utils.upload import upload


def format_mobile_number(number):
    if number.startswith('0027'):
        return '+27'+number[4:]
    elif number.startswith('0'):
        return '+27'+number[1:]
    else:
        return number


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def genrate_id():
    ALPHABET = "abcdfghjklmnpqrstvwxyz0123456789ABCDFGHJKLMNPQRSTVWXYZ"
    MAXLEN = 8
    result = ''
    for i in range(0, MAXLEN):
        result += random.choice(ALPHABET)
    return result