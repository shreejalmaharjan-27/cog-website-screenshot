from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from cog import BasePredictor, Input, Path
import time


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        options = webdriver.ChromeOptions()
        options.binary_location = '/root/chrome-linux/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=options)

    def predict(
        self,
        url: str = Input(
            description="Link to the website"
        ),
        w: int = Input(
            description="Width of the screenshot",
            default=1920
        ),
        h: int = Input(
            description="Height of the screenshot",
            default=1080
        ),
        wait_until: int = Input(
            description="Time in seconds to wait before a screenshot is taken",
            default=0
        )
    ) -> Path:
        self.browser.set_window_size(w, h)
        self.browser.get(url)
        if wait_until > 0:
            for i in range(wait_until):
                print(f"Elapsed time: {i+1}/{wait_until} seconds")
                time.sleep(1)

        # debug details
        print(f"Page title: {self.browser.title}")
        print(f"Page URL: {self.browser.current_url}")
        

        self.browser.save_screenshot('screenshot.png')
        return Path('screenshot.png')
