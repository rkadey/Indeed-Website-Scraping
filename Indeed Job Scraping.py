from bs4 import BeautifulSoup
import pandas as pd
import csv
import requests
from datetime import datetime
from time import sleep
from random import randint
from selenium import webdriver

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}


def get_url(position, location):
    template = "https://www.indeed.com/jobs?q={}&l={}"
    url = template.format(position, location)
    return url


def get_record(card):
    a_tag = card.h2.a
    job_title = card.h2.a.span.text
    job_title = a_tag.get('jobTitle')
    job_url = 'https://www.indeed.com' + str(a_tag.get('href'))
    job_company = card.find('span', 'companyName').text
    post_date = card.find('span', 'date').text

    record = (job_title, job_url, job_company, post_date)

    return record


def main(position, location):

    records = []
    url = get_url(position, location)
    print(url)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe", chrome_options=options)

    while True:
        response = requests.get(url, headers=header)
        driver.get(url)
        elem = driver.find_element_by_xpath("//*")
        source_code = elem.get_attribute("outerHTML")
        soup = BeautifulSoup(source_code, 'html.parser')
        cards = soup.find_all('div', 'job_seen_beacon')

        for card in cards:
            record = get_record(card)
            print(record)
            records.append(record)

        try:
            soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
    return records


job_roles = main('software developer', 'remote')
df = pd.DataFrame(job_roles)
df.columns = ['Position', 'URL', 'Comapny', 'Date Posted']
df.to_csv('Software Developer.csv')
