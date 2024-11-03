import requests
import re
from bs4 import BeautifulSoup

qualities = {
    '144': 0,
    '240': 1,
    '360': 2,
    '480': 3,
    '720': 4,
    '1080': 5
}


class VideoDownloadException(Exception):
    pass


class QualityError(VideoDownloadException):
    pass


class Scraper:
    def __init__(self, url, quality):
        self.url = url
        self.quality = quality

    def get_all_links(self):
        response = requests.get(self.url)
        content = BeautifulSoup(response.text, 'html.parser')
        tag_a = []
        for link in content.find_all('a', attrs={'href': re.compile(r'.mp4')}):
            tag_a.append(link)

        video_links = [li['href'] for li in tag_a]
        video_links.reverse()
        return video_links

    def get_link(self):
        links = self.get_all_links()
        legal_qualities = self.get_qualities()
        if self.quality not in legal_qualities:
            raise QualityError(f'This quality in not available \n available qualities are {legal_qualities}')
        else:
            return links[qualities[self.quality]]

    def get_qualities(self):
        links = self.get_all_links()
        qua = list(qualities.keys())
        available_qualities = []
        for i in range(len(links)):
            available_qualities.append(qua[i])

        return available_qualities


class Download:
    def __init__(self, url, quality):
        self.url = url
        self.quality = quality
        self.scraper = Scraper(self.url, self.quality)

    def download(self):
        video_link = self.scraper.get_link()
        with open('video.mp4', mode='wb') as f:
            print('Downloading')
            response = requests.get(video_link, stream=True)
            total = response.headers.get('content-length')
            if total is None:
                f.write(response.text)
            else:
                download = 0
                total = int(total)
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    download += len(data)
                    done = int(50 * download / total)
                    print('\r[{}{}]'.format('=' * done, ' ' * (50 - done)), end='')

        print('\nVideo downloaded')

a = Download(url='https://www.namasha.com/v/Ozrw1mCa', quality='144')
a.download()
