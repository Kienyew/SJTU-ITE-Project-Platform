import datetime
import random

# sd = datetime.date(2020, 1, 2)
# ed = datetime.date(2020, 12, 1)


def random_date_between(d1, d2):
    time_difference = d2 - d1
    new_time = d1 + datetime.timedelta(seconds=int(time_difference.total_seconds() * random.random()))
    return new_time


