import requests
import re
from bs4 import BeautifulSoup

url = 'https://news.ycombinator.com/news'

response = requests.get(url)
content = BeautifulSoup(response.text, 'html.parser')

articles = []

for item in content.find_all('tr', class_='athing'):
    item_span = item.find('span', class_='titleline')
    item_a = item_span.find('a')
    item_link = item_a.get('href') if item_a else None
    item_text = item_a.get_text(strip=True) if item_a else None

    next_row = item.find_next_sibling('tr')

    item_points = next_row.find('span', class_='score')
    item_points = item_points.get_text(strip=True) if item_points else '0 point'

    item_comments = next_row.find('a', string=re.compile('\d+(&nbsp;|\s)comment(s?)'))
    item_comments = item_comments.get_text(strip=True).replace('\xa0', ' ') if item_comments else '0 comment'

    articles.append({'link': item_link, 'title': item_text, 'score': item_points, 'comment': item_comments})

for article in articles:
    print(article)
