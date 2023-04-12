
import json
import logging

from datetime import datetime
from dotenv import dotenv_values
from twitter_scraper_selenium.profile import Profile as BaseProfile
from twitter_scraper_selenium.driver_utils import Utilities

from utils import Login, ImagesDownloader, VideosDownloader, TwiterStatusesVideosUrlRetriever

logging.basicConfig(level=logging.WARNING)

environ = dotenv_values('.env.master')

masterUsername = environ['USERNAME']
masterPassword = environ['PASSWORD']

modelUsername = environ['MODEL']


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
            # self.__close_driver()
            data = dict(list(self.posts_data.items())
                        [0:int(self.tweets_count)])
            return data
        except Exception as ex:
            self.__close_driver()
            logging.exception(
                "Error at method scrap : {} ".format(ex))
        
    def get_driver(self):
        return self.__driver
    
    def close_driver(self):
        return self.__close_driver()


class TwitterScrapper():
    def __init__(self, username: str) -> None:
        self.profile_bot = None
        self.username = username
        self.videos = []
        self.images = []
        self.tweet_urls = []
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
                if len(data[key]['videos']):
                    self.tweet_urls.append(data[key]['tweet_url'])
        except Exception as exc:
            print(exc)
            pass
        self.profile_bot = profile_bot
        return {'videos': self.videos, 'images': self.images, 'tweet_urls': self.tweet_urls}
    
    def save_scrapping_results(self):

        data = {'videos': self.videos, 'images': self.images,
                'tweet_urls': self.tweet_urls}

        file = open(f"{self.save_dir}/data.json", 'w', encoding='utf-8')
        json.dump(data, file, ensure_ascii=False)
        file.close()


    def save_videos(self):
        video_urls = self.get_videos_urls()
        downloader = VideosDownloader(videos=video_urls, save_dir=f"{self.save_dir}/Videos")
        downloader.process()
        return True

    def save_images(self):
        downloader = ImagesDownloader(
            images=self.images, save_dir=f"{self.save_dir}/Images")
        downloader.process()
        return True
    
    def get_videos_urls(self):
        retriever = TwiterStatusesVideosUrlRetriever(self.profile_bot.get_driver(), self.tweet_urls)
        results = retriever.process()
        self.profile_bot.close_driver()
        return results

    def generate_save_dir(self):
        return f'Records/{str(self.username).upper()}/Twitter/{datetime.now().timestamp()}'


if __name__ == '__main__':
    scrapper = TwitterScrapper(username=modelUsername)

    scrapper_data = scrapper.process(limit=323)

    print(scrapper_data)
    print(scrapper.save_dir)

    scrapper.save_scrapping_results()
    scrapper.save_images()
    scrapper.save_videos()
