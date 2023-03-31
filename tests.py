import requests
import string
import random
import json

url = 'http://localhost:5000//user/api/v1/'
headers = {"Content-Type": "application/json; charset=utf-8"}


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# create_Account
user_name = random_string(10)
password = random_string(10)
email = f'{random_string(10)}@gmail.com'

data = {'username': user_name, 'password': password, 'email': email}
print("sign_up", data)

r = requests.post(f'{url}sign_up', json=data, headers=headers)
print(r.json())


# log_in
data = {'username': user_name, 'password': password}
print("log_in", data)
r = requests.post(f'{url}log_in', json=data, headers=headers)
print(r.json())