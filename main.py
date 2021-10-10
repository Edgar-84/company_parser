import re
import requests
import os
from bs4 import BeautifulSoup
import json


def find_name(url):
    '''this function find name in url'''

    name = url.split('?')[0]
    return name.split('/')[-1]

def correct_text(text):
    return ''.join(re.sub(r'( )', ' ', text))

HEADERS = {
        'Accept': '*/*',
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
}

def get_categories_url(url):
    '''
    This function find all url categories companies
    :return: dict with list url categories
    '''

    reg = requests.get(url, headers=HEADERS)

    with open('obraz/categories.html', 'w') as file:
        file.write(reg.text)

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
        print(f"{cat_company_url} ####### success")
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

def get_info_company():
    """
    This function take all information about company
    :return: json files with all information
    """
    name_category = (lambda name: name.split('.')[0])
    for root, dirs, files in os.walk("data"):
        for company in files:
            with open(f'data/{company}') as file:
                lines = [line.strip() for line in file.readlines()]

                all_about_company = []
                count = 0
                for line in lines:
                    q = requests.get(line, headers=HEADERS)
                    result = q.content
                    soup = BeautifulSoup(result, 'lxml')

                    try:
                        name_company = soup.find(class_="company-header-title-name").text
                    except Exception:
                        name_company = 'No name company'
                    name_company = correct_text(name_company)
                    try:
                        link_on_site = soup.find(class_="g-user-content").get('href')
                    except Exception:
                        link_on_site = 'No link on site'

                    try:
                        main_info = soup.find('div', class_='g-user-content').text
                    except Exception:
                        main_info = "No information"

                    main_info = correct_text(main_info)
                    try:
                        project_logo = soup.find('img', class_='employer-sidebar__logo').get('src')
                    except Exception:
                        project_logo = 'No logo'

                    data = {
                        'name_company': name_company,
                        'link_on_site': link_on_site,
                        'project_logo': project_logo,
                        'main_info': main_info.strip()
                    }

                    count += 1
                    all_about_company.append(data)
                    print(f"#{count}: {line} is success!")

            with open(f'all_info/{name_category(company)}.json', 'a', encoding='utf-8') as file:
                json.dump(all_about_company, file, indent=4, ensure_ascii=False)

def main():

    get_urls_each_category()
    get_info_company()

if __name__== "__main__":
    main()


