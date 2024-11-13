import asyncio
import json
import time
from urllib.parse import urlencode
from httpx import AsyncClient
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def open_driver(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # for ignore warning and error
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5) # set a waiting time limit for the browser driver
    return driver

# initialize an async httpx client
client = AsyncClient(
    # enable http2
    http2=True,
    # add basic browser like headers to prevent getting blocked
    headers={
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
    },
    follow_redirects=True
)


async def search_page(
    query,
    checkin: str = "",
    checkout: str = "",
    number_of_rooms=1,
    offset: int = 0,):
    """scrapes a single hotel search page of booking.com"""
    checkin_year, checking_month, checking_day = checkin.split("-") if checkin else ("", "", "")
    checkout_year, checkout_month, checkout_day = checkout.split("-") if checkout else ("", "", "")

    url = "https://www.booking.com/searchresults.html"
    url_param = "?" + urlencode(
        {
            "ss": query,
            "lang":"en-gb",
            "checkin_year": checkin_year,
            "checkin_month": checking_month,
            "checkin_monthday": checking_day,
            "checkout_year": checkout_year,
            "checkout_month": checkout_month,
            "checkout_monthday": checkout_day,
            "no_rooms": number_of_rooms,
            "offset": offset,
        }
    )
    print(url + url_param)
    first_page = await client.get(url + url_param)
    print(first_page.text)
    return first_page

async def run():
    await search_page("Macau YOHO TREASURE ISLAND RESORTS WORLD HOTEL")


def getSearchPageUrl(query,
    checkin: str = "",
    checkout: str = "",
    number_of_rooms=1,
    offset: int = 0,):
    """scrapes a single hotel search page of booking.com"""
    checkin_year, checking_month, checking_day = checkin.split("-") if checkin else ("", "", "")
    checkout_year, checkout_month, checkout_day = checkout.split("-") if checkout else ("", "", "")

    url = "https://www.booking.com/searchresults.html"
    url_param = "?" + urlencode(
        {
            "ss": query,
            "lang":"en-gb",
            "checkin_year": checkin_year,
            "checkin_month": checking_month,
            "checkin_monthday": checking_day,
            "checkout_year": checkout_year,
            "checkout_month": checkout_month,
            "checkout_monthday": checkout_day,
            "no_rooms": number_of_rooms,
            "offset": offset,
        }
    )
    print(url + url_param)
    return url + url_param

hotel_list = ["WYNN PALACE"]
def getHotelUrl():
    driver = open_driver("https://www.booking.cn/")
    for hotel in hotel_list:
        hotel_search_url = getSearchPageUrl(hotel)
        driver.get(hotel_search_url)

        wait = WebDriverWait(driver, 20)
        time.sleep(1)
        selectAll = None
        try:
            selectAll = driver.find_element(By.NAME, 'selectAll')
        except Exception as e:
            print(e)
        if selectAll != None:
            selectAll.click()
            agreeButton = driver.find_element(By.TAG_NAME, 'button')
            agreeButton.click()
        time.sleep(300)





if __name__ == "__main__":
    #asyncio.run(run())
    getHotelUrl()

