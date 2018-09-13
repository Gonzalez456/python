import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
# from config import *

browseer = webdriver.Chrome()
wait = WebDriverWait(browseer, 10)


def get_page():
    try:
        browseer.get('https://www.taobao.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        touch = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        input.send_keys('美食')
        touch.click()
        table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        get_item()
        return table.text
    except TimeoutException:
        get_page()


def next_page(smb_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        touch = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > '
                                                         'span.btn.J_Submit'))
        )
        input.clear()
        input.send_keys(smb_number)
        touch.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > '
                                                                      'li.item.active > span'), str(smb_number)))
        get_item()
    except TimeoutException:
        next_page(smb_number)


def get_item():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browseer.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'money': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[-4],
            'title': item.find('.title').text(),
            'dsrs': item.find('.dsrs').text(),
            'location': item.find('.location').text()
        }
        print(product)


def main():
    table = get_page()
    reuse = int(re.compile(r'(\d+)').search(table).group(1))
    for i in range(2, reuse + 1):
        next_page(i)


if __name__ == '__main__':
    main()