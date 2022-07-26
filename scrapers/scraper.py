"""
Scraping module
"""

import requests
from bs4 import BeautifulSoup
from aiogram.dispatcher import FSMContext


headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                  'Safari/537.36 '
}


async def fetch_data_dict_by_urls(urls_dict: dict):
    """
    Returns the dictionary with scraped data by given urls
            Parameters:
                    urls_dict (dict):
            Returns:
                    data_dict (dict):
    """

    data_dict = dict()

    for el in urls_dict.items():
        req = requests.get(el[1], headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        total_number = soup.find('div', class_='page-header').find('span').text
        data_dict.update({el[0].replace('url', 'number'): total_number})

    return data_dict


async def get_vacancies(state: FSMContext, param: str):
    """
    Returns the dictionary with scraped vacancies data by speciality and any search parameter
            Parameters:
                    state (FSMContext):
                    param (FSMContext):
            Returns:
                    results_dict (dict):
    """

    base_url = 'https://djinni.co/jobs/'

    async with state.proxy() as data:
        speciality = data['speciality']

    category = 'keyword-' + speciality.replace('/', '').lower()

    urls_dict = dict()
    urls_dict.update({'total_url': base_url + category})
    urls_dict.update({'junior_url': base_url + category + '/?keywords=junior'})
    urls_dict.update({'middle_url': base_url + category + '/?keywords=middle'})
    urls_dict.update({'senior_url': base_url + category + '/?keywords=senior'})
    if param != '/OK':
        urls_dict['total_url'] = urls_dict['total_url'] + '/?keywords=' + param
        urls_dict['junior_url'] = urls_dict['junior_url'] + '+' + param
        urls_dict['middle_url'] = urls_dict['middle_url'] + '+' + param
        urls_dict['senior_url'] = urls_dict['senior_url'] + '+' + param

    results_dict = await fetch_data_dict_by_urls(urls_dict)

    return results_dict


async def get_candidates(state: FSMContext, param: str):
    """
    Returns the dictionary with scraped candidates data by speciality and any search parameter
            Parameters:
                    state (FSMContext):
                    param (FSMContext):
            Returns:
                    results_dict (dict):
    """

    base_url = 'https://djinni.co/developers/'

    async with state.proxy() as data:
        speciality = data['speciality']

    category = '?exp_from=0&exp_to=1&title=' + speciality.replace('/', '') + '&sortby=date'

    urls_dict = dict()
    urls_dict.update({'total_url': base_url + category})
    urls_dict.update({'junior_url': base_url + category + '&keywords=junior'})
    urls_dict.update({'middle_url': base_url + category + '&keywords=middle'})
    urls_dict.update({'senior_url': base_url + category + '&keywords=senior'})
    if param != '/OK':
        urls_dict['total_url'] = urls_dict['total_url'] + '&keywords=' + param
        urls_dict['junior_url'] = urls_dict['junior_url'] + '+' + param
        urls_dict['middle_url'] = urls_dict['middle_url'] + '+' + param
        urls_dict['senior_url'] = urls_dict['senior_url'] + '+' + param

    results_dict = await fetch_data_dict_by_urls(urls_dict)

    return results_dict
