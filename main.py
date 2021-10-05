import requests
import os
from bs4 import BeautifulSoup

def find_name(url):
    '''this function find name in url'''

    name = url.split('?')[0]
    name = name.split('/')[-1]
    return name

def get_categories_url(url):
    '''
    This function find all url categories companies

    return: dict with list url categories
    '''
    headers = {
        'Accept': '*/*',
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }

    reg = requests.get(url, headers=headers)

    with open('obraz/categories.html', 'w') as file:
        file.write(reg.text)

    with open('obraz/categories.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    articles = soup.find_all("a", class_='employers-company__item')

    category_companyes_urls = []
    for article in articles:
        project_url = "https://rabota.by" + article.get('href') + '&vacanciesRequired=true'
        category_companyes_urls.append(project_url)

    return category_companyes_urls

get_categories_url("https://rabota.by/employers_company?area=16")
