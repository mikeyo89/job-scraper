import sys

# Adding models to the system path.
sys.path.insert(0, '/Users/michaelbonilla/Documents/0 Eastern Connecticut State University/2 2021FA/0 CSC-450 Senior Research/0 Assignments/Research Project/job-scraper/src')

from models.cards import CardDetails

if __name__ == '__main__':
    '''
    record = CardDetails()
    record.link = 'https://www.indeed.com/rc/clk?jk=24e2911d8256b2b4&fccid=a5b4499d9e91a5c6&vjs=3'
    record.start()
    '''
    record2 = CardDetails()
    record2.link = 'https://www.indeed.com/company/Spatial-Networks/jobs/Software-Engineer-6eaf69f74b8752a2?fccid=6410610dd779bf9a&vjs=3'
    record2.start()
