import os
import requests
import csv
import sys

# Adding models to the system path.
sys.path.insert(0, '/Users/michaelbonilla/Documents/0 Eastern Connecticut State University/2 2021FA/0 CSC-450 Senior Research/0 Assignments/Research Project/job-scraper/src')

from bs4 import BeautifulSoup
from models.cards import BasicCard, CardDetails

card_id = 1
success = 0
failure = 0

def get_url(position):
    ''' Builds and returns query url based on provided position (what). '''
    template_url = 'https://www.indeed.com/jobs?q={}&l'
    return template_url.format(position)

def get_raw_cards(soup):
    ''' Returns a collection of 'raw_cards' to be parsed. '''
    return soup.select('a.tapItem.fs-unmask.result')

def get_card(raw_card):
    '''
    Takes an individual 'raw_card' and returns a processed 'card' object
    with a job title, company name, company rating, company location, and job link.
    '''
    # Get unique id from global id count.
    global card_id
    id = card_id
    card_id += 1 # Incremend global_id so it is different for next card.

    # Extract high-level data from 'card'.
    card_content = raw_card.find('td')

    # Find all company data from 'card' (name, rating, location).
    company_content = card_content.pre

    # Job Title.
    title = card_content.div.h2.find('span', title=True).text

    # Company Name.
    company = company_content.find('span', 'companyName').text

    # Company Rating.
    raw_rating = company_content.find('span', 'ratingsDisplay')
    rating = raw_rating.text if raw_rating is not None else 'None'

    # Company Location.
    location = company_content.find('div', 'companyLocation').contents[0].text

    # Posting Date.
    date = raw_card.find('span', 'date').text

    # Job Link (href).
    link = 'https://www.indeed.com' + raw_card.get('href')

    return BasicCard(id, title, company, rating, location, date, link)

if __name__ == '__main__':
    # Make an HTTP GET Request and save HTML text if request is successful.
    url = get_url('software engineer')
    print('Parsing results: 1 - 15')
    response = requests.get(url)

    # Create a BeautifulSoup object from HTTP response and extract all 'cards' (job postings).
    soup = BeautifulSoup(response.text, 'html.parser')
    raw_cards = get_raw_cards(soup)

    # Perform field extraction for an entire collection of 'raw cards'.
    records = [get_card(raw_card) for raw_card in raw_cards]
    
    # Iterate through the pagination to collect all cards from the search query.
    for count in range(1, 2):
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')

            print(f'Parsing results: {(count * 15) + 1} - {(count + 1) * 15}')
            response = requests.get(url)

            soup = BeautifulSoup(response.text, 'html.parser')
            raw_cards = get_raw_cards(soup)

            records += [get_card(raw_card) for raw_card in raw_cards]
        except AttributeError:
            break
    
    file_path = '/Users/michaelbonilla/Documents/0 Eastern Connecticut State University/2 2021FA/0 CSC-450 Senior Research/0 Assignments/Research Project/job-scraper/src/test/results.csv'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobID', 'JobTitle', 'CompanyName', 'CompanyRating', 'JobLocation', 'PostDate', 'JobUrl'])
        writer.writerows([(record.card_id, record.title, record.company, record.rating, record.location, record.date, record.link) for record in records])
    
    # Make GET requests for each job posting, in individual threads.
    count = 1
    for record in records:
        record.details.process_id = count
        record.details.start()
        count += 1