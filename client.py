import requests


response = requests.post('http://127.0.0.1:5000/api/user',
                         json={"name": "user_2",
                               "email": "emaaaaail@mail.ru",
                               "password": "12345611"})

# response = requests.post('http://localhost:5000/api/ads/',
#                          json={"title": "Объявление",
#                                "description": "Тут может быть ваше объявление",
#                                "owner": "1"})
#
# response = requests.get('http://localhost:5000/api/ads/1')

# response = requests.patch('http://localhost:5000/api/ads/1',
#                          json={"description": "Тут НЕ может быть ваше объявление"})

# response = requests.delete('http://localhost:5000/api/ads/1')

print(response.text)
print(response.status_code)
