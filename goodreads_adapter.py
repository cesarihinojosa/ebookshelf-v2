from bs4 import BeautifulSoup
import requests
import re
from dataclasses import dataclass


class ApiError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 500):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

GOODREADS_UNAVAILABLE = ApiError(
    code="GOODREADS_UNAVAILABLE",
    message="Unable to fetch books at this time.",
    status_code=502
)

@dataclass
class Book:
    image_url: str

#TODO: add logging
class GoodreadsAdapter:
    """
    Scapes Goodreads to retrive data.
    """

    # TODO: Clean up
    # TODO: Add data caching/backup
    def get_books(self):

        start = 1
        current = start
        end = 5000
        books = []
        small_images = []

        while current < end:

            link = f"https://www.goodreads.com/review/list/144045223?page={current}&ref=nav_mybooks"
            current += 1
            headers = { # necessary to imitate a human
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.4'
            }
            response = requests.get(link, headers=headers) # sending off request

            if response.status_code == 200: # catching an error if bad request
                webpage = response.text
                webpage = BeautifulSoup(webpage, "html.parser")
                table = webpage.find("table", id="books")

                if not table:
                    raise GOODREADS_UNAVAILABLE

                rows = table.find_all('tr')
                rows = rows[1:]
                for row in rows:

                    cover = row.find('td', class_='field cover')
                    if not cover:
                        raise GOODREADS_UNAVAILABLE

                    img_tag = cover.find("img")
                    if not img_tag and not img_tag.has_attr('src'):
                        raise GOODREADS_UNAVAILABLE

                    img_src = img_tag['src']
                    small_images.append(img_src)
            else:
                print(f"Failed to retrieve page {current-1}. Status code: {response.status_code}")
            if len(rows) < 2: # if there are no books on page
                break

        pattern = r"/books/(\d+[a-zA-Z]/\d+)" 
        large_image_codes = []
        for image in small_images: # getting the ID from small image url
            match = re.search(pattern, image)
            if match:
                result = match.group(1)
                large_image_codes.append(result)
            else:
                print("No match found during regex")

        # creating the new url for larger images and wrap them as Book instances
        books = [Book(image_url="https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/" + code + ".jpg")
                 for code in large_image_codes]

        print(books)
        return books