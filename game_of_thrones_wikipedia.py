import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_episodes'

response = requests.get(url)
content = BeautifulSoup(response.text, 'html.parser')

episodes = []

for table in content.find_all('table', class_="wikitable plainrowheaders wikiepisodetable"):

    headers = []

    for header in table.find('tr').find_all('th'):
        headers.append(header.text)

    for row in table.find_all('tr')[1:]:
        values = []
        for value in row.find_all(['td', 'th']):
            values.append(value.text)

        if values:
            temp_dict = {headers[i]: values[i] for i in range(len(values))}
            episodes.append(temp_dict)


for ep in episodes:
    print(ep)
