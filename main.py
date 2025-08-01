# import requests
#
#
# def time_split(seconds):
#     hours = seconds // 3600
#     minute = (seconds % 3600) // 60
#     second = seconds % 60
#     return f"{hours}:{minute}:{second}"
#
#
# def define_genere(ids):
#     url2 = "http://localhost:8000"
#     response = requests.get(url2).json()
#     genres = []
#     for datas in response:
#         if datas['id'] in ids:
#             genres.append(datas['name'])
#     return genres
#
#
# url = "http://localhost:8000/contents/"
#
# response = requests.get(url).json()
# for datas in response:
#     print(f'FILM: {datas.get("title")}')
#     for key, value in datas.items():
#         if key == 'duration':
#             print(f"{key}: {time_split(value)}")
#         elif key == 'genre':
#             print(f"{key}: {define_genere(value)}")
#         else:

# print(f"{key}: {value}")

# print(response.json())


import requests

url = "http://localhost:8000/1/"

response = requests.delete(url)

print(response.status_code)