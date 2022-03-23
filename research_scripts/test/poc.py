from bs4 import BeautifulSoup
from bs4.element import Tag
'''
Simple Card Objects:
Card {
    title,
    company,
    location,
    rating,
    link,
    url
}
'''

# Open local text file of Indeed results HTML. 
with open('sample2.txt', 'rt') as file:
    # Create a BeautifulSoup object with sample.txt HTML.
    soup = BeautifulSoup(file, 'html.parser')

# Find all 'cards' (job postings) in HTML Document.
raw_cards = soup.select('a.tapItem.fs-unmask.result')

# Create a function that runs the above extractions and returns the 'card' object.
def get_card(raw_card: Tag):
    '''
    Takes an individual 'raw_card' and returns the processed 'card' object
    with a job title, company name, company rating, company location, and job link.
    '''

    # Job Link (href)
    link = 'https://www.indeed.com' + raw_card.get('href')

    # Extract high-level data from 'card'.
    card_content = raw_card.find('td')

    # Find all company data from 'card' (name, rating, location)
    company_content = card_content.find('div', class_='companyInfo')

    # Job Title
    title = card_content.find('span', title=True).get_text()

    # Company Name
    company = company_content.find('span', 'companyName').get_text()

    # Company Rating
    rating = company_content.find('span', 'ratingNumber')

    # Company Location
    location = company_content.find('div', 'companyLocation').get_text()

    # Posting Date
    date = raw_card.find('span', 'date').get_text()

    return {
        'title': title,
        'company': company,
        'rating': rating.text if rating is not None else 'None', # Company rating is not always provided in 'cards'.
        'location': location,
        'date': date,
        'link': link
    }

# Perform field extraction for an entire collection of raw cards.
cards = [get_card(raw_card) for raw_card in raw_cards]

with open('results.csv', 'w+') as f:
    f.write('JobTitle,CompanyName,CompanyRating,JobLocation,PostDate,JobUrl\n')
    lines = [(f'{card["title"]}, {card["company"]}, {card["rating"]}, {card["location"]}, {card["date"]}, {card["link"]}\n') for card in cards]
    f.writelines(lines)
