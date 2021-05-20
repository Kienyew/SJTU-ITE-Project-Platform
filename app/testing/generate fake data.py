from faker import Faker
from local_function import random_date_between
import datetime
import secrets
import string
import random
import pandas as pd
import os

# Configuration
NUMS_ACCOUNT = 20
EMAIL_DOMAIN = ["gmail", "yahoo", "hotmail"]

# Preparation --------------------------------------------------------------------------------------------------------
with open('random name.txt') as f:
    chinese_names = f.read().splitlines()
with open('random project name.txt') as f:
    project_names = f.read().splitlines()
with open('random team name.txt') as f:
    team_names = f.read().splitlines()
with open('random paragraph.txt') as f:
    random_paragraph = f.read().splitlines()

testing_pictures = [i for i in os.listdir("../static/user resources/testing") if not i.startswith('.')]
print(f'Generating random pictures from: {testing_pictures}')
faker = Faker()
ALPHABET = string.ascii_letters + string.digits  # for random password

output_usernames = []
output_user_avatar = []
output_emails = []
output_passwords = []

output_team_names = []
output_team_description = []
output_teammates = []
output_project_name = []
output_project_pictures = []
output_project_description = []
output_project_date = []

# Main algorithm ------------------------------------------------------------------------------------------------
for _ in range(NUMS_ACCOUNT):
    username = random.choice(chinese_names)
    if username in output_usernames:
        continue  # for UNIQUENESS
    user_avatar = f'avatar {random.randint(1, 99):03}.png'
    email = faker.name().replace(" ", "") + "@" + random.choice(EMAIL_DOMAIN) + ".com"
    if email in output_emails:
        continue
    password = "".join(secrets.choice(ALPHABET) for i in range(10))

    teammates = []
    for _ in range(random.randint(2, 3)):
        teammates.append(random.choice(chinese_names))
    
    project_pictures = []
    for _ in range(random.randint(1, 4)):
        project_pictures.append("testing/" + random.choice(testing_pictures))

    project_description = []
    for _ in range(random.randint(3, 6)):
        project_description.append(random.choice(random_paragraph))
    
    output_usernames.append(username)
    output_user_avatar.append(user_avatar)
    output_emails.append(email)
    output_passwords.append(password)
    output_team_names.append(random.choice(team_names))
    output_team_description.append(random.choice(random_paragraph))
    output_teammates.append(teammates)
    output_project_name.append(random.choice(project_names))
    output_project_pictures.append(project_pictures)
    output_project_description.append(project_description)
    output_project_date.append(random_date_between(datetime.date(2018, 1, 2), datetime.date(2021, 12, 24)))

# Output configuration -------------------------------------------------------------------------------------------------
fake_data = {
    "username": output_usernames,
    "user_avatar": output_user_avatar,
    "email": output_emails,
    "password": output_passwords,
    
    "team_name": output_team_names,
    "team_description": output_team_description,
    "teammates": output_teammates,
    "project_name": output_project_name,
    "project_pictures": output_project_pictures,
    "project_description": output_project_description,
    "project_date": output_project_date,
}

data = pd.DataFrame(fake_data)
data.to_csv("fake_data.csv", index=False)

