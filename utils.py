
import aiohttp
import asyncio
import logging

from pathlib import Path
from urllib import parse

logger = logging.getLogger(__name__)


class ImagesDownloader:
    BASE_DIR = Path(__file__).resolve().parent

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
        logger.info(f"\n\n Saving Images To : {save_path} \n\n")
        Path(save_path).mkdir(parents=True, exist_ok=True)
        tasks = [asyncio.create_task(self.async_download_image(
            image_url=image, save_path=save_path)) for image in self.images]
        await asyncio.gather(*tasks)

    def process(self):
        return asyncio.run(self.async_download_images)
