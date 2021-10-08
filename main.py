import requests
import os
from bs4 import BeautifulSoup

def find_name(url):
    '''this function find name in url'''

    name = url.split('?')[0]
    name = name.split('/')[-1]
    return name

HEADERS = {
        'Accept': '*/*',
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
}

def get_categories_url(url):
    '''
    This function find all url categories companies

    :return: dict with list url categories
    '''

    # reg = requests.get(url, headers=HEADERS)
    #
    # with open('obraz/categories.html', 'w') as file:
    #     file.write(reg.text)

    with open('obraz/categories.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    articles = soup.find_all("a", class_='employers-company__item')

    category_companyes_urls = []
    for article in articles:
        project_url = "https://rabota.by" + article.get('href').split('?')[0] + '?page=0&vacanciesRequired=true&area=16'
        category_companyes_urls.append(project_url)

    return category_companyes_urls

def get_urls_each_category():
    """
    This function save links companies for each category
    :return: files with links companies
    """

    for cat_company_url in get_categories_url("https://rabota.by/employers_company"):
        print(f"{cat_company_url} ####### successful")
        reg = requests.get(cat_company_url, headers=HEADERS)
        project_name = find_name(cat_company_url)

        with open(f"obraz/{project_name}.html", 'w') as file:
            file.write(reg.text)

        with open(f'obraz/{project_name}.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        articles = soup.find_all("span", class_='employers-company__description')

        companyes_urls = []
        for article in articles:
            company_url = "https://rabota.by" + article.find('a').get("href")
            companyes_urls.append(company_url)

        with open(f'data/{project_name}.txt', 'a') as file: # save links on companies in files
            for line in companyes_urls:
                file.write(f'{line}\n')


get_urls_each_category()

