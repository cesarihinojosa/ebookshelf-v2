from bs4 import BeautifulSoup
import requests
import re
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

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
    goodreads_uri = "https://www.goodreads.com"
    headers = { # necessary to imitate a human
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.4'
    }

    def _optimize_images(self, images: list[str]) -> list[str]:
        """
        Optimize images by converting them to a larger size.
        Args:
            images (list[str]): list of image urls
        Returns:
            list[str]: list of optimized image urls
        """
        pattern = r"/books/(\d+[a-zA-Z]/\d+)" 
        large_image_codes = []
        for image in images:
            match = re.search(pattern, image)
            if match:
                result = match.group(1)
                large_image_codes.append(result)
            else:
                print("No match found during regex") # Hanlde this better
        return large_image_codes

    def get_books_read(self, user_id: str) -> list[Book]:
        """
        Fetches the books read by a user from Goodreads.
        Args:
            user_id (str): the user's ID on Goodreads
        Returns:
            list[Book]: a list of Book instances with optimized image URLs
        """
        logging.info(f"Fetching books read by user {user_id} from Goodreads")
        start = 1
        end = 5000 # Arbitrary large number to prevent infinite loop
        images = []
        for i in range(start, end):

            url = f"{self.goodreads_uri}/review/list/{user_id}?page={i}&ref=nav_mybooks&shelf=read"
            response = requests.get(url, headers=self.headers) # sending off request
            response.raise_for_status()

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
                images.append(img_src)
                
            if len(rows) < 2: # break when there are no books left to scrape
                break

        optimized_images = self._optimize_images(images)
        # creating the new url for larger images and wrap them as Book instances
        books = [Book(image_url="https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/" + code + ".jpg")
                 for code in optimized_images] #TODO: fix me
        return books