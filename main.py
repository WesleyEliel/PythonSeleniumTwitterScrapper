
import json
import logging

from datetime import datetime
from dotenv import dotenv_values
from twitter_scraper_selenium.profile import Profile as BaseProfile
from twitter_scraper_selenium.driver_utils import Utilities

from login import Login
from utils import ImagesDownloader

logger = logging.getLogger(__name__)
environ = dotenv_values('.env.master')

masterUsername = environ['USERNAME']
masterPassword = environ['PASSWORD']


class Profile(BaseProfile):

    def scrap(self):
        try:
            self.__start_driver()
            self.__driver = Login(
                self.__driver, masterUsername, masterPassword).login()
            self.__driver.get(self.URL)
            Utilities.wait_until_completion(self.__driver)
            Utilities.wait_until_tweets_appear(self.__driver)
            self.__fetch_and_store_data()
            self.__close_driver()
            data = dict(list(self.posts_data.items())
                        [0:int(self.tweets_count)])
            return data
        except Exception as ex:
            self.__close_driver()
            logger.exception(
                "Error at method scrap : {} ".format(ex))


class TwitterScrapper():
    def __init__(self, username: str) -> None:
        self.username = username
        self.videos = []
        self.images = []
        self.save_dir = self.generate_save_dir()

    def process(self, limit: int = 10):
        profile_bot = Profile(twitter_username=self.username, browser="chrome",
                              proxy=None, tweets_count=limit, headless=False, browser_profile=None)
        Chocolateplayg1 = json.dumps(profile_bot.scrap())

        try:
            data = json.loads(Chocolateplayg1)
            for key in data.keys():
                self.images.extend(data[key]['images'])
                self.videos.extend(data[key]['videos'])
        except Exception as exc:
            print(exc)
            pass
        return {'videos': self.videos, 'images': self.images}

    def save_videos(self):
        return self.videos

    async def save_images(self):
        downloader = ImagesDownloader(
            images=self.images, save_dir=f"{self.save_dir}/Images")
        downloader.process()
        return True

    def generate_save_dir(self):
        return f'Records/{str(self.username).upper()}-{datetime.now().timestamp()}'


if __name__ == '__main__':
    scrapper = TwitterScrapper(username='Chocolateplayg1')

    scrapper_data = scrapper.process(limit=5)

    print(scrapper_data)
    print(scrapper.save_dir)

    scrapper.save_images()
