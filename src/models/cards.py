from bs4 import BeautifulSoup
from threading import Thread
import requests

class BasicCard:
    '''
    Model of data to be extracted from initial results web scraping.
    '''
    def __init__(self, card_id, title, company, rating, location, date, link):
        self.card_id = card_id
        self.title = title
        self.company = company
        self.rating = rating
        self.location = location
        self.date = date
        self.link = link

        # Setup Job post Details
        self.details = CardDetails()
        self.details.link = link
        self.details.thread_id = self.card_id

class CardDetails(Thread):
    '''
    This class holds the search criterion that will be used against job-posting data.
    Seperating the criterion from the actual program because modularity is good.

    This class also inherits the Thread class to ensure GET requests are not a bottleneck, because
    response time from GET request is longer than parsing of the model.
    '''
    # Global Variables.
    thread_id = 1
    link = ''
    thread_suceeded = False
    response = ''
    programming_languages = []
    frameworks = []
    api_key = 'df88ce6bdd893bacffe698b9b2d525bd'

    def run(self):
        '''
        Multithreading method that will retrieve webpage HTML from the assigned url.
        '''
        # Do not run this thread if self.link is None for some reason.
        if self.link is None or '':
            raise Exception(f'"Link" cannot be "None" when making a GET request.')
        
        '''
        client = ScraperAPIClient(self.api_key)
        self.response = client.get(url=self.link, render=True)
        '''
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.response = requests.get(self.link, headers=headers)
    
    def update_criterion(self):
        # Create a BeautifulSoup object based on GET response.
        soup = BeautifulSoup(self.response.text, 'html.parser')

        # Get the job posting sections (i.e. "Job Summary", "Responsibilities", "Qualifications")
        raw_text = soup.find('div', attrs={'id': 'jobDescriptionText'})

        # If results found, split raw_text into individual word vectors.
        if raw_text is not None:
            split_text = raw_text.get_text(separator=' ').lower().replace('/', ' ').replace(',', ' ').split()
        else:
            print(f'Thread {self.thread_id} failed: raw_text is None. Cannot attempt to parse data.\nDetails: response_link = {self.response.url}')
            return

        # Clean (again) the job text into list of individual words (term vector).
        translation_table = dict.fromkeys(map(ord, ".,:;?|=~!@'(){}[]"), None) # Creates a set of chars which will be eliminated from each term.
        clean_words = [desc.translate(translation_table) for desc in split_text]

        # Iterate through each word in the job description.
        for word in clean_words:
            flagged = False
            # Iterate through each programming language in self.programming_languages.
            for pl in self.programming_languages:
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
            for framework in self.frameworks:
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
        
        self.thread_suceeded = True
    
    def reset_criterion(self):
        '''
        Reset the boolean values of the programming_languages and frameworks lists to False.
        '''
        for pl in self.programming_languages:
            pl[1] = False
        
        for framework in self.frameworks:
            framework[1] = False
    
    def report_criterion(self):
        if self.thread_suceeded:
            print(f'Thread {self.thread_id}: Succeed.\nLink = {self.link}')
            for pl in self.programming_languages:
                print(pl)
            
            for f in self.frameworks:
                print(f)
            print()
        else:
            print(f'Thread {self.thread_id} failed.')