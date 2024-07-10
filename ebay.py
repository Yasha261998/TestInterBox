from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import json


TEST_URL = "https://www.ebay.com/itm/404265004322"


class EBay:
    """Scraping page of the product, output result to console or file.

    :param path_file:
        Path to file for output
    """

    path_file = "temp.json"

    def __init__(self, headless: bool = True):
        """Create Chrome driver and set options.

        :param headless:
            Enable or disable headless mode for browser (default=True).
        """
        
        # Chrome options
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if headless:
            options.add_argument("--headless=new")

        # chrome driver
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                   options=options)
        self.browser.implicitly_wait(2)
    

    def write_to_file(self, data: dict):
        """Write JSON to file.

        :param data:
            Output data.
        """
        
        with open(self.path_file, "w") as f:
            try:
                f.write(json.dumps(data, indent=4))
            except json.JSONDecodeError as ex:
                print(f"JSONDecodeError {ex}")

    def write_to_console(self, data: dict):
        """Output JSON to console

        :param data:
            Output data
        """
        
        try:
            print(json.dumps(data, indent=4))
        except json.JSONDecodeError as ex:
            print(f"JSONDecodeError {ex}")

    def scrapper(self, url: str) -> dict:
        """Scraping info for product.

        :param url:
            Url to page.
        :returns:
            Info for product.
        """

        self.browser.get(url)
        result = {}
        try:
            try:
                name_ele = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "x-item-title__mainTitle")))
            except TimeoutException:
                print("TimeoutException for page")
                raise NoSuchElementException
            name = name_ele.text
            img_ele = self.browser.find_element(By.CSS_SELECTOR, "#PicturePanel .ux-image-carousel-container .zoom")
            path_img = []
            for img in img_ele.find_elements(By.CSS_SELECTOR, ".ux-image-carousel-item.image-treatment.image img"):
                path_img.append(img.get_attribute("data-zoom-src"))
                
            price = self.browser.find_element(By.CSS_SELECTOR, ".x-price-section .x-bin-price__content .x-price-primary .ux-textspans").text
            seller = self.browser.find_element(By.CLASS_NAME, "x-sellercard-atf__info__about-seller").get_attribute("title")
            shipping_cost = self.browser.find_element(By.CSS_SELECTOR, f".ux-layout-section--shipping .ux-labels-values--shipping "
                                                                       f".ux-labels-values__values .ux-textspans--BOLD").text
            data = {"name": name,
                    "path_img": path_img,
                    "current_url": url,
                    "price": price,
                    "seller": seller,
                    "shipping_cost": shipping_cost}
        except NoSuchElementException as ex:
            print(f"NoSuchElementException: {ex}")
            return None
        else:
            return data
        finally:
            self.browser.quit()


if __name__ == "__main__":
    ebay = EBay()
    result = ebay.scrapper(TEST_URL)
    if result:
        ebay.write_to_console(result)
        ebay.write_to_file(result)
