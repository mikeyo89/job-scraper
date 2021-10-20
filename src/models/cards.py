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
        self.card_details

class CardDetails:
    '''
    Model of data to be extracted from following a job posting.
    '''
    def __init__(self, basic_card):
        self.basic_card = basic_card
        
