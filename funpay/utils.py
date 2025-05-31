import string
import random


def random_tag() -> str:
    return "".join(random.choice(string.digits + string.ascii_lowercase) for _ in range(10))