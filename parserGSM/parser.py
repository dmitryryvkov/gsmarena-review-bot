import requests
import os.path
from bs4 import BeautifulSoup as beautifulsoup


class ParseGSM:
    max_page = 72
    pages = []
    host = "https://www.gsmarena.com"
    url = "https://www.gsmarena.com/reviews.php3"

    last_title = ""
    last_file_title = ""
    file_name = ""
    image_url = ""

    def __init__(self, file_name):
        self.image_name = 'last_review.jpg'
        self.file_name = file_name

        if os.path.exists(file_name):
            self.last_file_title = open(file_name, 'r').read()

        else:
            f = open(file_name, 'w')
            self.last_title = self.get_last_review_title()
            f.write(self.last_title)
            f.close()

    def get_last_review_title(self):
        page = requests.get(self.url)

        soup = beautifulsoup(page.content, 'html.parser')

        title = soup.select('.review-item-title > a')
        last_title = title[0].text

        return last_title

    def get_last_review_image(self):
        soup = beautifulsoup(requests.get(self.url).content, 'html.parser')
        image_urls = soup.select('.review-item-media-wrap > a > img')
        self.image_url = image_urls[0].attrs['src']

        return self.image_url

    def get_last_review_link(self):
        soup = beautifulsoup(requests.get(self.url).content, 'html.parser')

        review_links = soup.select('.review-item-media-wrap > a')
        review_link = self.host + review_links[0].attrs['href']

        return review_link

    def combine_review_info(self):

        return {
            "title": self.get_last_review_title(),
            "link": self.get_last_review_link(),
            "image": self.get_last_review_image()
        }

    def new_review_exists(self):
        self.last_title = self.get_last_review_title()
        return self.last_title != self.last_file_title

    def download_image(self):
        f = open(self.image_name, 'wb')
        f.write(requests.get(self.image_url).content)
        f.close()

        return self.image_name

    def update_last_title(self, file_name):
        f = open(file_name, 'w')
        f.write(self.last_title)
        f.close()
        self.last_file_title = self.last_title
