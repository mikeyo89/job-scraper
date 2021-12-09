# Create your models here.
class JobCardModel:
    '''
    Model of data to be extracted from initial results web scraping.
    '''
    def __init__(self, card_id, title, company, rating, location, date, url):
        self.card_id = card_id
        self.title = title
        self.company = company
        self.rating = rating
        self.location = location
        self.date = date
        self.url = url

        # Setup Job post Details
        self.details = JobDetailsModel()

class JobDetailsModel:
    '''
    This class holds the search criterion that will be used against job-posting data.
    Seperating the criterion from the actual program because modularity is good.

    This class also inherits the Thread class to ensure GET requests are not a bottleneck, because
    response time from GET request is longer than parsing of the model.
    '''
    # Global Variables.
    programming_languages = []
    frameworks = []
    thread_suceeded = False

class HttpHeadersModel:
    ''' This class holds headers information that the web scraper will use, at random. '''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
    }

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    ]

class JobMetricsModel:
    ''' Defines the set of metrics that will be measured for each job post. '''
    pl = [
        ['python', False],
        ['c#', False],
        [['c++', 'c'], False],
        ['ruby', False],
        ['java', False],
        [['javascript', 'js'], False],
        [['html', 'html5'], False],
        [['css', 'css3'], False],
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

    f = [
        [['dotnet', '.net', 'asp.net', 'aspnet', 'net'], False],
        [['react', 'reactjs', 'react.js'], False],
        [['angular', 'angular.js', 'angularjs', 'angular2+', 'angular3+'], False],
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
        [['api', 'apis', 'rest', 'restful'], False],
        [['sdk', 'sdks'], False],
        [['postgres', 'postgresql', 'psql'], False],
        ['mysql', False],
        [['mongo', 'mongodb'], False],
        ['docker', False],
        ['jenkins', False],
        ['jira', False],
        [['rally','rallydev'], False],
        ['azure', False],
        ['kubernetes', False],
        ['swagger', False],
        [['scrum', 'agile'], False]
    ]

class JobDataModel:
    ''' Defines the count of appearances for each metric in all job posts. '''
    pl = [
        ['Python', 0],
        ['C#', 0],
        ['C/C++', 0],
        ['Ruby', 0],
        ['Java', 0],
        ['Javascript', 0],
        ['HTML5', 0],
        ['CSS', 0],
        ['SQL', 0],
        ['R', 0],
        ['Assembly', 0],
        ['Swift', 0],
        ['Pascal', 0],
        ['Objective-C', 0],
        ['PHP', 0],
        ['GoLang', 0],
        ['Perl', 0],
        ['F#', 0],
        ['Scala', 0],
        ['Apex', 0],
        ['Kotlin', 0],
        ['Typescript', 0]
    ]

    f = [
        ['.NET', 0],
        ['ReactJS', 0],
        ['AngularJS', 0],
        ['Django', 0],
        ['Splunk', 0],
        ['Spring', 0],
        ['Ruby on Rails', 0],
        ['Redux', 0],
        ['ExpressJS', 0],
        ['VueJS', 0],
        ['Flask', 0],
        ['Laravel', 0],
        ['Symfony', 0],
        ['GatsbyJS', 0],
        ['Sinatra', 0],
        ['Materialize', 0],
        ['Bootstrap', 0],
        ['Tailwind CSS', 0],
        ['Ionic', 0],
        ['Xamarin', 0],
        ['Phonegap', 0],
        ['Native', 0],
        ['Corona', 0],
        ['jQuery', 0],
        ['Flutter', 0],
        ['PyTorch', 0],
        ['Pandas', 0],
        ['Sci-kit', 0],
        ['ML.net', 0],
        ['Chainer', 0],
        ['PyTest', 0],
        ['Jest', 0],
        ['Mocha', 0],
        ['Jasmine', 0],
        ['Cypress', 0],
        ['Scrapy', 0],
        ['NodeJS', 0],
        ['Git/Github', 0],
        ['APIs', 0],
        ['SDKs', 0],
        ['PostgreSQL', 0],
        ['MySQL', 0],
        ['MongoDB', 0],
        ['Docker', 0],
        ['Jenkins', 0],
        ['Jira', 0],
        ['RallyDev', 0],
        ['MS Azure', 0],
        ['Kubernetes', 0],
        ['Swagger', 0],
        ['Scrum/Agile', 0]
    ]