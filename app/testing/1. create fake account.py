from faker import Faker
import secrets
import string
import random
import pandas as pd

GENERATE_NEW_LIST = False  # CHANGE THIS ONLY IF YOU WANT TO CREATE A NEW LIST OF ACCOUNT !!!!
NUMS_ACCOUNT = 20
EMAIL_DOMAIN = ["gmail", "yahoo", "hotmail"]

faker = Faker()
ALPHABET = string.ascii_letters + string.digits  # for random password

if GENERATE_NEW_LIST:
    name_list = []
    email_list = []
    password_list = []
    
    for _ in range(NUMS_ACCOUNT):
        name = faker.name()  # we could use loop because it's a generator
        email = name.replace(" ", "") + "@" + random.choice(EMAIL_DOMAIN) + ".com"
        password = "".join(secrets.choice(ALPHABET) for i in range(10))
        name_list.append(name)
        email_list.append(email)
        password_list.append(password)
    
    fake_users = {
        "name": name_list,
        "email": email_list,
        "password": password_list
    }
    
    data = pd.DataFrame(fake_users)
    data.to_csv("fake_users.csv", index=False)
