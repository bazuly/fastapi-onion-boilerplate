import random
import string

kafka_error_detail = "Failed to send message, break..."


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=16))
