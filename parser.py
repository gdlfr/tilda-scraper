import requests
from bs4 import BeautifulSoup
import csv
import os


URL = 'https://crm.tilda.cc/contacts/'
HEADERS = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
FILE = 'contacts.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='tcrm-list-item tcrm-clear js-contact-item')

    contacts = []

    contacts.append({
        'name': item.find('div', class_='tcrm-table-col tcrm-table-col-type-name js-table-cell js-lead-name').get_text(),
        'email': item.find('div', class_='tcrm-table-col tcrm-table-col-type-email js-table-cell js-lead-email').get_text(),
        'number': item.find('div', class_='tcrm-table-col tcrm-table-col-type-phone js-table-cell js-lead-phone').get_text(),
        'company': item.find('div', class_='tcrm-table-col tcrm-table-col-type-text js-table-cell js-lead-company').get_text(),
        # another item to parse add here
                    })
    return contacts

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'e-mail', 'Number', 'Company'])
        for item in items:
            writer.writerow([item['name'], item['email'], item['number'], item['company']])
            
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        contacts = []
        save_file(contacts, FILE)
        print(f'Recived: {len(contacts)} contact(s)')
        os.startfile(FILE)
    else:
        print('Error: no 200')

parse()
