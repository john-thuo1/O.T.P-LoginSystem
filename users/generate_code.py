import string as s
import random as r


def get_code():
    length_of_string= 6
    random_code = "".join(r.choices(s.digits + s.ascii_uppercase, k = length_of_string))
    return random_code