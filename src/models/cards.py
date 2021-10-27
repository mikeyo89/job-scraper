from bs4 import BeautifulSoup
from .metrics import CardMetrics
import multiprocessing
import requests
import copy

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

        self.details = CardDetails()
        self.details.link = link

class CardDetails(multiprocessing.Process):
    '''
    This class holds the search criterion that will be used against job-posting data.
    Seperating the criterion from the actual program because modularity is good.

    This class also inherits the Process class to ensure GET requests are not a bottleneck, because
    response time from GET request is longer than parsing of the model.
    '''
    # Global Variables.
    link = ''
    process_id = 1
    # We need a deep copy of these values so that metrics are unique to each job post.
    programming_languages = [
        ['python', False],
        ['c#', False],
        ['c', False],
        ['c++', False],
        ['ruby', False],
        ['java', False],
        [['javascript', 'js'], False],
        [['html', 'html5'], False],
        ['css', False],
        ['sql', False],
        ['r', False],
        ['assembly', False],
        ['swift', False],
        ['pascal', False],
        [['objective-c', 'objectivec'], False],
        ['php', False],
        [['go', 'golang'], False],
        ['perl', False],
        ['f#', False],
        ['scala', False],
        ['apex', False],
        ['kotlin', False],
        [['typescript', 'ts'], False]
    ]

    frameworks = [
        [['dotnet', '.net', 'asp.net', 'aspnet', 'net'], False],
        [['react', 'reactjs', 'react.js'], False],
        [['angular', 'angular.js', 'angularjs'], False],
        ['django', False],
        ['splunk', False],
        ['spring', False],
        ['rails', False],
        ['redux', False],
        [['express', 'expressjs', 'express.js'], False],
        [['vue', 'vuejs', 'vue.js'], False],
        ['flask', False],
        ['laravel', False],
        ['symfony', False],
        [['gatsby', 'gatsbyjs', 'gatsby.js'], False],
        ['sinatra', False],
        ['materialize', False],
        ['bootstrap', False],
        ['tailwind', False],
        ['ionic', False],
        ['xamarin', False],
        ['phonegap', False],
        ['native', False],
        ['corona', False],
        ['jquery', False],
        ['flutter', False],
        ['pytorch', False],
        ['pandas', False],
        [['sci-kit', 'scikit'], False],
        [['ml.net', 'mlnet'], False],
        ['chainer', False],
        ['pytest', False],
        ['jest', False],
        ['mocha', False],
        ['jasmine', False],
        ['cypress', False],
        ['scrapy', False],
        [['node', 'nodejs', 'npm'], False],
        [['git', 'github'], False],
        [['api', 'apis'], False],
        [['sdk', 'sdks'], False],
        [['postgres', 'postgresql', 'psql'], False],
        ['mysql', False],
        ['docker', False],
        ['jenkins', False],
        ['jira', False],
        [['rally','rallydev'], False],
        ['azure', False],
        ['kubernetes', False]
    ]

    def run(self):
        '''
        Multiprocessing method that will retrieve webpage HTML from the assigned url.
        '''
        # Do not run this process if self.link is None for some reason.
        if self.link is None or '':
            raise Exception(f'"Link" cannot be "None" when making a GET request.')
        
        # Make GET request and create BeautifulSoup object with returned data.
        response = requests.get(self.link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the job posting sections (i.e. "Job Summary", "Responsibilities", "Qualifications")
        raw_text = soup.find('div', attrs={'id': 'jobDescriptionText'})

        # If results found, split raw_text into individual word vectors.
        if raw_text is not None:
            split_text = raw_text.get_text(separator=' ').lower().replace('/', ' ').replace(',', ' ').split()
        else:
            print('raw_text was None. Retrying...')
            split_text = []
            response = requests.get(response.url)
            soup = BeautifulSoup(response.text, 'html.parser')

            raw_texts = soup.find_all(name='div', class_='iCIMS_Expandable_Text')

            for raw_text in raw_texts:
                split_text.extend(raw_text.text.lower().replace('/', ' ').replace('-', ' ').split())
            
            if raw_texts is None or len(raw_texts) == 0:
                print(f'Process {self.process_id} failed: raw_text is None or Empty. Cannot attempt to parse data.\nDetails: response_link = {response.url}')
                return

        # Clean (again) the job text into list of individual words (term vector).
        translation_table = dict.fromkeys(map(ord, ".,:;?|=~!@'(){}[]"), None) # Creates a set of chars which will be eliminated from each term.
        clean_text = [desc.translate(translation_table) for desc in split_text]

        # Run the job-data extraction model.
        self.update_criterion(clean_text)
    
    def update_criterion(self, words):
        # Iterate through each word in the job description.
        for word in words:
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

            # Else, proceed with checking if word is a framework using same process as above.
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
        
        self.report_criterion()
    
    def reset_criterion(self):
        '''
        Reset the boolean values of the programming_languages and frameworks lists to False.
        '''
        for pl in self.programming_languages:
            pl[1] = False
        
        for framework in self.frameworks:
            framework[1] = False
    
    def report_criterion(self):
        print(f'Process {self.process_id}: Success.')
        print(f'link = {self.link}')
        for pl in self.programming_languages:
            print(pl)
        
        for f in self.frameworks:
            print(f)
        print()