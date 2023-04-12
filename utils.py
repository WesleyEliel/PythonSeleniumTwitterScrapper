
import aiohttp
import asyncio
import logging
import time

from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions

from urllib import parse

logging.basicConfig(level=logging.WARNING)

class Downloader:
    BASE_DIR = Path(__file__).resolve().parent


class ImagesDownloader(Downloader):

    def __init__(self, images: list, save_dir: str) -> None:
        """
        Initiliaze the downloader

        Args:
            images: a list of image url that should be downloaded ['https://pbs.twimg.com/media/EaXxY09XsAAYi9J?format=jpg&name=small', 'https://pbs.twimg.com/media/EaXxY09XsAAYi9J.jpg']
            save_dir: relative directory where images should be saved
        """
        self.images = images
        self.save_dir = save_dir

    async def async_download_image(self, image_url: str, save_path: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as res:
                query = dict(parse.parse_qsl(parse.urlsplit(image_url).query))
                if 'format' in query.keys():
                    file = f"{image_url.split('?')[0].split('/')[-1]}.{query['format']}"
                else:
                    file = image_url.split("/")[-1]
                with open(f"{save_path}/{file}", "wb") as f:
                    print(f"Downloaded {file}")
                    f.write(await res.read())

    async def async_download_images(self):
        save_path = f"{self.BASE_DIR}/{self.save_dir}"
        logging.warning(f"\n\n Saving Images To : {save_path} \n\n")
        Path(save_path).mkdir(parents=True, exist_ok=True)
        tasks = [asyncio.create_task(self.async_download_image(
            image_url=image, save_path=save_path)) for image in self.images]
        await asyncio.gather(*tasks)

    def process(self):
        return asyncio.run(self.async_download_images())


class VideosDownloader(Downloader):

    def __init__(self, videos: list, save_dir: str) -> None:
        """
        Initiliaze the downloader

        Args:
            videos: a list of image url that should be downloaded ['https://twitter.com/dickhddaily/status/1387565986501513216']
            save_dir: relative directory where images should be saved
        """
        self.videos = videos
        self.save_dir = save_dir

    async def async_download_video(self, video_url: str, save_path: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as res:
                file = f"{video_url.split('?')[0].split('/')[-1]}"
                with open(f"{save_path}/{file}", "wb") as f:
                    print(f"Downloaded {file}")
                    f.write(await res.read())

    async def async_download_videos(self):
        save_path = f"{self.BASE_DIR}/{self.save_dir}"
        logging.warning(f"\n\n Saving Videos To : {save_path} \n\n")
        Path(save_path).mkdir(parents=True, exist_ok=True)
        tasks = [asyncio.create_task(self.async_download_video(
            video_url=video, save_path=save_path)) for video in self.videos]
        await asyncio.gather(*tasks)

    def process(self):
        return asyncio.run(self.async_download_videos())


class Login:
    def __init__(self, browser, username: str, password: str) -> None:
        self.browser = browser
        self.username = username
        self.password = password
        self._baseUrl = 'https://www.twitter.com/login'

    def log_message(self, message):
        logging.warning(f'\n\n { message } \n\n')

    def login(self):
        self.log_message("Waiting for Browser")
        wait = WebDriverWait(self.browser, 40)
        self.browser.get(self._baseUrl)
        self.log_message("Loking for Username Input")
        username_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "text")))
        self.log_message("Sending Keys to Username Input")
        username_input.send_keys(self.username)
        self.log_message("Found Username Input")
        time.sleep(3)
        username_input.send_keys(Keys.ENTER)
        self.log_message("Waiting for Browser")
        time.sleep(10)
        self.log_message("Loking for Password Input")
        password_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "password")))
        self.log_message("Sending Keys to Password Input")
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(7)
        return self.browser


class TwiterStatusesVideosUrlRetriever:
    def __init__(self, browser, statuses: list,  quality: str = '576x1024') -> None:
        self.browser = browser
        self.quality = quality
        self.statuses = statuses
        self.download_endpoint = "https://twittervideodownloader.com"

    def video_quality(self):
        if self.quality == "480x652":
            xpath_element = "/html/body/div[2]/div/center/div[7]/div[1]/a"
        elif self.quality == "576x1024":
            xpath_element = "/html/body/div[2]/div/center/div[6]/div[1]/a"
        else:
            xpath_element = "/html/body/div[2]/div/center/div[5]/div[1]/a"
        return xpath_element

    def log_message(self, message):
        logging.warning(f'\n\n { message } \n\n')

    def download_video(self, url):
        self.log_message(f"Started retrieval at {url}")
        self.browser.get(self.download_endpoint)
        url_entry_field = self.browser.find_element(By.NAME, "tweet")
        url_entry_field.send_keys(url)
        url_entry_field.send_keys(Keys.ENTER)
        self.log_message("Loading web resource, please wait..")
        try:
            download_btn = WebDriverWait(self.browser, 20).until(
                expected_conditions.presence_of_element_located((By.XPATH, self.video_quality())))
            video_url = download_btn.get_attribute('href')
            time.sleep(3)
            return video_url
        except Exception as exc:
            self.log_message(exc.__str__())

    def process(self):
        result = [x for x in map(
            self.download_video, self.statuses) if x is not None]
        return result
