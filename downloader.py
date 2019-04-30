import time
import re

import requests
from selenium import webdriver
import chromedriver_binary
from typing import List

from tqdm import tqdm

from keys import username, password


SRC_PATTERN = re.compile("<img src=\"(.+)\" alt")


def login_twitter(driver):
    # login on twitter
    # send username
    driver.find_element_by_id('username_or_email').send_keys(username)

    # send password
    driver.find_element_by_id('password').send_keys(password)

    # send submit
    driver.find_element_by_class_name('buttons').submit()


def login(driver):
    # click login button
    driver.find_element_by_class_name('Header__login').click()

    # select tewitter button
    driver.find_element_by_class_name('LoginModalDialog__twitter').click()

    # login by twitter
    login_twitter(driver)


def get_dl_list(driver) -> List[str]:
    # return list
    ret = []

    # get PhotoListItem list
    photo_list = driver.find_element_by_class_name("PhotoList__container").find_elements_by_class_name("PhotoListItem")
    for i, div in enumerate(tqdm(photo_list)):
        # page scroll
        driver.execute_script("window.scrollTo(0, {});".format(i * 60))
        # page load
        time.sleep(1)
        # add to list
        ret.append(get_url_from_tag(div.get_attribute('innerHTML')))
    return ret


def get_url_from_tag(text: str) -> str:
    return thumbnail_to_large_img(SRC_PATTERN.search(text).group(1))


def thumbnail_to_large_img(url_text: str) -> str:
    return url_text.replace("files", "uploads")[:-14]+".png"


def download_img(url: str):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open("img/"+url.split('/')[-1], 'wb') as f:
            f.write(r.content)


def main(driver):
    # go cluster
    driver.get('https://cluster.mu/')

    # login
    login(driver)

    # login後は待った方が良さげ
    time.sleep(10)

    # photo list
    driver.get('https://cluster.mu/account/photos')

    # DL list
    dl_list = get_dl_list(driver)

    for url in tqdm(dl_list):
        download_img(url)
        time.sleep(1)


if __name__ == '__main__':
    chromedriver_binary.add_chromedriver_to_path()
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    main(driver)

    driver.quit()
