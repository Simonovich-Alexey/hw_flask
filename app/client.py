import requests

response = requests.post('http://127.0.0.1:5000/user',
                         json={"name": "user_6",
                               "email": "email6@mail.ru",
                               "password": "123"})
# response = requests.post('http://127.0.0.1:5000/login',
#                          json={"name": "user_6",
#                                "password": "123"})

# response = requests.get('http://127.0.0.1:5000/user',
#                         headers={'Authorization': 'f39fcaca-443c-4222-ad95-d84b563da34f'})
# response = requests.patch('http://127.0.0.1:5000/user',
#                         headers={'Authorization': 'f39fcaca-443c-4222-ad95-d84b563da34f'},
#                         json={'password': '321'})
# response = requests.delete('http://127.0.0.1:5000/user',
#                            headers={'Authorization': 'f39fcaca-443c-4222-ad95-d84b563da34f'})

# response = requests.post('http://127.0.0.1:5000/ads',
#                          params={'id': '1', 'password': '12345611'},
#                          json={"title": "Объявление №1",
#                                "description": "Тут может быть ваше объявление"})
#
# response = requests.get('http://localhost:5000/ads')
#
# response = requests.patch('http://127.0.0.1:5000/ads/1',
#                          params={'name': 'user_1', 'password': '12345611'},
#                          json={"title": "Продам Объявление",
#                                "description": "Тут НЕ может быть вашего объявления"})
#
# response = requests.delete('http://localhost:5000/ads/1',
#                            params={'name': 'user_1', 'password': '12345611'})
#
print(response.text)
print(response.status_code)
