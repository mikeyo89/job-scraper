from bs4 import BeautifulSoup

'''
Simple Card Objects:
Card {
    title,
    company,
    location,
    rating,
    link
}
'''

# Open local text file of Indeed results HTML. 
with open('src/test/sample.txt', 'r') as file:
    text = file.read()
    file.close()

# Create a BeautifulSoup object with sample.txt HTML.
soup = BeautifulSoup(text, 'html.parser')

# Find all 'cards' (job postings) in HTML Document.
raw_cards = soup.select('a.tapItem.fs-unmask.result')

# Create a function that runs the above extractions and returns the 'card' object.
def get_card(raw_card):
    '''
    Takes an individual 'raw_card' and returns the processed 'card' object
    with a job title, company name, company rating, company location, and job link.
    '''

    # Extract high-level data from 'card'.
    card_content = raw_card.find('td')

    # Find all company data from 'card' (name, rating, location)
    company_content = card_content.pre

    # Job Title
    title = card_content.div.h2.find('span', title=True).text

    # Company Name
    company = company_content.find('span', 'companyName').text

    # Company Rating
    rating = company_content.find('span', 'ratingsDisplay')

    # Company Location
    location = company_content.find('div', 'companyLocation').contents[0].text

    # Posting Date
    date = raw_card.find('span', 'date').text

    # Job Link (href)
    link = 'https://www.indeed.com' + raw_card.get('href')

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
print(cards)
