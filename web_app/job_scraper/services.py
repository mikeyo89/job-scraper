import requests
import copy

from .models import JobCardModel, JobMetricsModel, HttpHeadersModel, JobDataModel
from bs4 import BeautifulSoup
from threading import Thread

# Write your model services here.
class JobCardService:
    ''' Handles the retrieval and storage of JobCardModel objects. '''

    # Global variables.
    card_id = 0
    max_results = 0
    success_count = 0
    failure_count = 0

    cards = []
    http_headers = HttpHeadersModel.headers
    user_agents = HttpHeadersModel.user_agents
    user_agents_count = len(user_agents) - 1
    url: str

    def __init__(self):
        ''' Default constructor. '''
        self.url = ''
    
    def __init__(self, position: str, *args):
        ''' Default constructor, with a job position specified. '''
        pos = position.replace(' ', '+')
        if len(args) == 0:
            self.url = self.get_url(pos)
        else:
            location = args[0].replace(' ', '+')
            self.url = self.get_url(pos, location)
    
    def parse_page_results(self) -> None:
        ''' Makes a GET request to Indeed based on defined url, parses results page. '''
        headers = copy.deepcopy(self.http_headers)
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' #self.user_agents[random.randint(0, self.user_agents_count)]
        response = requests.get(self.url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        if soup is None:
            print(f'Error: GET request to Indeed using {response.url} returned status code {response.status_code}.')
            return

        raw_cards = soup.select('a.tapItem.fs-unmask.result')
        if raw_cards is None:
            print(f'Error: raw_cards is none.\nCheck the url: {response.url}')
            return
        
        # Perform field extraction for an entire collection of 'raw cards'.
        print(f'Parsing results 1 - 15: url = {response.url}')
        parsed_cards = self.parse_card_details(cards = [self.get_card(raw_card) for raw_card in raw_cards])
        self.cards.extend(parsed_cards)

        # Iterate through the pagination to collect all cards from the search query.
        for count in range(15, self.max_results, 15):
            try:
                url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')

                print(f'Parsing results {count + 1} - {count + 15}: url = {url}')
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser') if response.status_code == 200 else None
                if soup is None:
                    return f'Error: GET request to Indeed using {url} returned status code {response.status_code}.'

                raw_cards = soup.select('a.tapItem.fs-unmask.result')
                if raw_cards is None:
                    return f'Error: raw_cards is none.\nCheck the url: {response.url}'

                parsed_cards = self.parse_card_details(cards = [self.get_card(raw_card) for raw_card in raw_cards])
                self.cards.extend(parsed_cards)
            except AttributeError:
                print('There is an attribute error!!')
                continue
        
        '''
        # Multithreaded approach of retrieving all cards.
        thread_url_template = self.url + '&start={}'
        result_count = 10

        for count in range(15, self.max_results, 15):
            url = thread_url_template.format(result_count)
            print(f'Attempting to GET results {count + 1} - {count + 15}. url = {url}')
            
            thread = Thread(target=self.get_raw_cards, args=(url,))
            thread.start()
            thread.join() # Removed concurrent execution to reduce CAPTCHA likelihood because this is too fast for Indeed.

            result_count += 10
        '''

    def get_raw_cards(self, url: str) -> None:
        '''
        This method will make a thread-safe GET request to Indeed.
        The thread executing this function will append the found cards into self.cards.
        '''
        response = requests.get(url, headers=self.http_headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup is None:
            return f'Error: GET request to Indeed using {response.url} returned status code {response.status_code}.'

        raw_cards = soup.select('a.tapItem.fs-unmask.result')
        if raw_cards is None:
            return f'Error: raw_cards is none.\nCheck the url: {response.url}'

        self.cards.extend([self.get_card(raw_card) for raw_card in raw_cards])

    def get_card(self, raw_card) -> JobCardModel:
        '''
        Takes an individual 'raw_card' and returns a processed 'card' object
        with a card id, job title, company name, company rating, company location, and job link.
        '''
        card_content = raw_card.find('td')
        company_content = card_content.find('div', class_='companyInfo')

        self.card_id += 1
        try:
            # Job Link (href)
            url = 'https://www.indeed.com' + raw_card.get('href')

            # Job Title
            title = card_content.find('span', title=True).get_text()

            # Company Name
            company = company_content.find('span', 'companyName').get_text()

            # Company Rating
            raw_rating = company_content.find('span', 'ratingNumber')
            rating = raw_rating.get_text() if raw_rating else 'None'

            # Company Location
            raw_location = company_content.find('div', 'companyLocation')
            location = raw_location.get_text() if raw_location else 'None Found'

            # Posting Date
            date = raw_card.find('span', 'date').get_text()

            return JobCardModel(self.card_id, title, company, rating, location, date, url)
        except AttributeError:
            print(f'Missing field in card {self.card_id}.')
            return

    def get_url(self, position, *args) -> str:
        ''' Builds and returns query url based on position (what) and location (where). '''
        if len(args) == 0:
            template_url = 'https://www.indeed.com/jobs?q={}&l'
            return template_url.format(position)
        else:
            template_url = 'https://www.indeed.com/jobs?q={}&l={}'
            return template_url.format(position, args[0])
    
    def parse_card_details(self, cards):
        ''' Parses through all individual job posts, updates the metrics data, and returns parsed cards. '''
        count = 0
        for card in cards:
            if card:
                count += 1

                card.details.programming_languages = copy.deepcopy(JobMetricsModel.pl)
                card.details.frameworks = copy.deepcopy(JobMetricsModel.f)

                thread = Thread(target=self.update_card_metrics, args=(card,))
                thread.start()
                thread.join()
            else:
                print(f'Card is None. card.url = {card}')

        for card in cards:
            if card.details.thread_suceeded:
                self.success_count += 1
            else:
                self.failure_count += 1
        
        return cards
    
    def update_card_metrics(self, card: JobCardModel) -> None:
        ''' Makes a GET request to an individual job post and updates the associated cards' metrics. '''
        if card is None:
            print(f'Card is {card}. Cannot attempt to update_card_metrics.')
            return

        if card.url is None or '':
            print(f'Thread {card.card_id} failed: Could not make GET request to the specified url. Url = {card.url}')
            return
        
        # Make GET request and retrieve raw_text.
        response = requests.get(card.url, headers=self.http_headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        if soup is None:
            print(f'Error: GET request to Indeed using {self.url} returned status code {response.status_code}.')
            return

        # Find the job description's (raw) text.
        raw_text = soup.find('div', attrs={'id': 'jobDescriptionText'})
        if raw_text is not None:
            split_text = raw_text.get_text(separator=' ').lower().replace('/', ' ').replace(',', ' ').replace('-', ' ').split()
        else:
            print(f'Thread {card.card_id} failed: raw_text is None.\nDetails: response_link = {response.url}')
            return

        # Clean (again) the job text into list of individual words (word vector).
        translation_table = dict.fromkeys(map(ord, ".:;?|=~!@'(){}[]"), None)  # List of chars to remove.
        clean_words = [word.translate(translation_table).strip() for word in split_text]

        # Iterate through each word in the job description.
        for word in clean_words:
            flagged = False
            # Iterate through each programming language in self.programming_languages.
            for pl in card.details.programming_languages:
                if type(pl[0]) == list:
                    # Iterate through all pneumonics of this programming language and check if any matches with the word.
                    for p in pl[0]:
                        if p == word:
                            pl[1] = True
                            flagged = True
                            break
                        else:
                            continue
                else:
                    # Check if the word is a programming language.
                    if pl[0] == word:
                        pl[1] = True
                        flagged = True
                # If this word turned out to be a programming language, break from checking other
                # programming languages and flag to self.frameworks that they need not be checked either.
                if flagged:
                    break
                else:
                    continue
            
            # If the word was a programming language, continue to the next word.
            if flagged:
                continue

            # Else, proceed with checking if word is a framework using same thread as above.
            for framework in card.details.frameworks:
                if type(framework[0]) == list:
                    for f in framework[0]:
                        if f == word:
                            framework[1] = True
                            flagged = True
                            break
                        else:
                            continue
                else:
                    if framework[0] == word:
                        framework[1] = True
                        flagged = True
                
                if flagged:
                    break
                else:
                    continue
        
        card.details.thread_suceeded = True

class JobDataService:
    ''' This class serves as a data analysis engine for a list of JobDetailsModel. '''
    cards = []
    pl_counts = copy.deepcopy(JobDataModel.pl)
    f_counts = copy.deepcopy(JobDataModel.f)

    def __init__(self, cards) -> None:
        ''' Default constructor with cards object.'''
        self.cards = []
        for card in cards:
            self.cards += card

    def reset_counts(self):
        ''' Reset count of the counts. '''
        for pl in self.pl_counts:
            pl[1] = 0
        
        for f in self.f_counts:
            f[1] = 0
    
    def get_counts(self):
        ''' Parses through cards and sets the count of every pl. '''
        if not any(self.cards):
            print('Cards is empty. Returning None for now.')
            return
        
        for card in self.cards:
            index = 0
            for pl in card.details.programming_languages:
                if pl[1]:
                    self.pl_counts[index][1] += 1
                index += 1
            
            index = 0
            for f in card.details.frameworks:
                if f[1]:
                    self.f_counts[index][1] += 1
                index += 1
    
    def filter_counts(self):
        ''' Sorts the counts lists in descending order and returns the top 10 items. '''
        self.pl_counts = sorted(self.pl_counts, key=lambda pl: pl[1], reverse=True)[:10]
        self.f_counts = sorted(self.f_counts, key=lambda f: f[1], reverse=True)[:10]
