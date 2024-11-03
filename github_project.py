import requests
from bs4 import BeautifulSoup

url = 'https://github.com/{}'
username = 'ALI-Hash1'

response = requests.get(url.format(username), params={'tab': 'repositories'})
content = BeautifulSoup(response.text, 'html.parser')

items = content.find(id='user-repositories-list')

for item in items.find_all('li'):
    title = item.find('a').get_text(strip=True)
    description = item.find('p', itemprop='description').get_text(strip=True)
    language = item.find('span', itemprop='programmingLanguage').get_text(strip=True)

    print(title, description, language, sep='\n', end='\n' + '*' * 50 + '\n')
