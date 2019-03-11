import base64
import json
import re
from os import makedirs
from os.path import isfile

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm.autonotebook import tqdm

RESULT_PATH = '../result/acm.json'
PAGE_DIR = '../data/ACM/pages/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 ' \
             'YaBrowser/19.3.0.2489 Yowser/2.5 Safari/537.36'


def init():
    for path in (PAGE_DIR, '../result/'):
        try:
            makedirs(PAGE_DIR)
        except FileExistsError:
            pass


def parse_index_page():
    url = 'https://dl.acm.org/events.cfm'

    page = requests.get(url, headers={'user-agent': USER_AGENT}).text
    soup = bs(page, 'html.parser')

    result = []
    for link in tqdm(soup.find_all(href=re.compile(r'event\.cfm\?id'))):
        result.append('https://dl.acm.org/' + link.get('href'))

    return result


def download_pages(conferences, force_reload=False):
    result = {}
    driver = webdriver.Firefox()

    try:
        for link in tqdm(conferences):
            if not force_reload and isfile(PAGE_DIR + format_filename(link)):
                with open(PAGE_DIR + format_filename(link)) as file:
                    result[link] = file.read()
            else:
                driver.get(link)

                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "TopChoices"))
                )
                result[link] = driver.page_source
                with open(PAGE_DIR + format_filename(link), mode='w') as file:
                    file.write(result[link])
    finally:
        driver.quit()

    return result


def parse_pages(sources):
    result = []
    for url, page in tqdm(sources.items()):
        soup = bs(page, 'html.parser')

        short_title = soup.find('strong', style='padding-right:10px')
        short_id = short_title.text
        title = short_title.nextSibling.text

        table = soup.find('td', style='padding:10px;  border:thin #000 solid')
        parsed_table = [x.text for x in table.children if x != '\n']

        description = soup.find(id='toShow1')
        description = description.text.strip()

        result.append(dict(
            url=url,
            id=short_id,
            title=title,
            categories=parsed_table,
            description=description
        ))

    return result


def format_filename(name):
    return base64.urlsafe_b64encode(
        name.encode('utf-8')
    ).decode('ascii') + '.html'


def main():
    init()

    print('Parsing index page')
    conferences = parse_index_page()

    print('Downloading conference pages')
    sources = download_pages(conferences)

    print('Parsing conference pages')
    result = parse_pages(sources)

    print(f'Dumping results to {RESULT_PATH}')
    print(f'Total: {len(result)} conferences')
    with open(RESULT_PATH, mode='w') as file:
        json.dump(result, file, indent=2)


if __name__ == '__main__':
    main()
