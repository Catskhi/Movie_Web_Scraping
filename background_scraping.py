import requests 

movie_list = ['Fight Club']
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

response = requests.get('https://www.imdb.com/', headers=headers)
print(response)