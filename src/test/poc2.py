from bs4 import BeautifulSoup
import sys

# Adding models to the system path.
sys.path.insert(0, '/Users/michaelbonilla/Documents/0 Eastern Connecticut State University/2 2021FA/0 CSC-450 Senior Research/0 Assignments/Research Project/job-scraper/src')

from models.cards import CardDetails
card_details = CardDetails()

with open('src/test/sample3.txt', 'r') as file:
    text = file.read()
    file.close()

# Get the job posting sections (i.e. "Job Summary", "Responsibilities", "Qualifications")
soup = BeautifulSoup(text, 'html.parser')
raw_description = soup.find('div', attrs={'id': 'jobDescriptionText'})
split_description = raw_description.text.lower().replace('/', ' ').replace('-', ' ').split()

# Clean-up the description words.
translation_table = dict.fromkeys(map(ord, ",.:;?|=`~!@*'()<>{}[]"), None)
clean_description = [desc.translate(translation_table) for desc in split_description]

# Run the CardDetails model that checks individual job postings.
card_details.update_criterion(clean_description)

for pl in card_details.programming_languages:
    if pl[1]:
        print(pl[0])

for framework in card_details.frameworks:
    if framework[1]:
        print(framework[0])
