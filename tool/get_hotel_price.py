from datetime import datetime,timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import logging
import time
from selenium.common.exceptions import NoSuchElementException


def open_driver(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.page_load_strategy = 'eager'
    options.add_argument("lang=en-US")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5)
    return driver


def modify_url_with_dates(base_url):
    # 获取当前日期和第二天的日期
    today = datetime.now()
    startDay = today + timedelta(days=7)
    endDay = today + timedelta(days=8)

    # 格式化日期为字符串
    checkin_date = startDay.strftime('%Y-%m-%d')
    checkout_date = endDay.strftime('%Y-%m-%d')

    # 插入日期参数到URL中
    modified_url = base_url.replace("&no", f"&checkin={checkin_date}&checkout={checkout_date}&no")
    return modified_url


def scrape_booking_details(link, driver):
    try:
        # 修改链接以包含日期参数
        link = modify_url_with_dates(link)
        print(link)

        # 打开URL
        driver.get(link)
        logging.info(f"访问链接: {link}")

        # 处理页面可能出现的弹窗和按钮
        selectAll = None
        try:
            selectAll = driver.find_element(By.NAME, 'selectAll')
        except Exception as e:
            print("no need select all")
        if selectAll is not None:
            selectAll.click()
            agreeButton = driver.find_element(By.TAG_NAME, 'button')
            agreeButton.click()
            time.sleep(15)

            cnSiteSelect = None
            closeButton = None
            try:
                cnSiteSelect = driver.find_element(By.ID, 'cnSiteSelect')
                closeButton = driver.find_element(By.CLASS_NAME, 'modal-mask-closeBtn')
            except Exception as e:
                print("no need cnSite")
            if closeButton is not None:
                closeButton.click()
            time.sleep(1)

            cookieAgree = None
            try:
                cookieAgree = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            except Exception as e:
                print("no need cookie")
            if cookieAgree is not None:
                cookieAgree.click()
            time.sleep(1)

        # 检查是否存在id = bodyconstraint-inner的元素
        try:
            body_constraint = driver.find_element(By.ID, "bodyconstraint-inner")
            logging.info("找到元素: id='bodyconstraint-inner'")
        except NoSuchElementException:
            logging.warning("未找到元素: id='bodyconstraint-inner'")
            return None

        # 获取房型和价格
        room_elements = driver.find_elements(By.CLASS_NAME, 'hprt-roomtype-link')
        price_elements = driver.find_elements(By.CLASS_NAME, 'prco-valign-middle-helper')

        room_price_list = []
        for room, price in zip(room_elements, price_elements):
            room_name = room.text.strip()
            room_price = price.text.strip()
            room_price_list.append({"name": room_name, "price": room_price})

        # 返回数据
        print(room_price_list)
        return room_price_list

    except Exception as e:
        logging.error(f"爬取过程中发生错误: {e}")
        return None


def scrape_all_hotel_details(hotel_table):
    driver = open_driver("https://www.booking.com/index.en-us.html")
    hotel_prices = []

    for index, hotel_row in hotel_table.iterrows():
        hotel = hotel_row["Hotel"]
        hotel_url = hotel_row["Details URL"]
        if len(str(hotel_url)) > 0:
            room_prices = scrape_booking_details(hotel_url, driver)
            if room_prices is not None:
                hotel_prices.append({"Hotel": hotel, "Prices": room_prices})

    # 将结果保存到Excel
    hotel_df = pd.DataFrame(hotel_prices)
    hotel_df.to_excel("hotel_details.xlsx", index=False)


if __name__ == "__main__":
    #hotel_table = pd.read_excel('./resources/hotelUrls.xlsx')
    #scrape_all_hotel_details(hotel_table)

    import pandas as pd

