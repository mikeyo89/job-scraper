from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.core.cache import caches

from job_scraper.models import JobDataModel
from .services import JobCardService, JobDataService

# Create your views here.
class HomeView(generic.TemplateView):
    ''' Index/Landing view of the job_scraper app. '''
    template_name = 'scraper/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        self.what = self.request.GET.get('what')
        self.where = self.request.GET.get('where')
        self.amount = self.request.GET.get('amount')
        
        context.update({'range': range(1*15, 11*15, 15)})

        return context
    
    def get_success_url(self):
        return reverse('job_scraper:search') + str(f'?what={self.what}&where={self.where}&amount={self.amount}')

class SearchView(generic.TemplateView):
    ''' View of the search results from user search input. '''
    template_name = 'scraper/search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        amount = self.request.GET.get('amount')
        self.what = self.request.GET.get('what')
        self.where = self.request.GET.get('where')
        self.amount = int(amount) if amount != 'default' else 15

        cache = caches['default']
        search_query = f'?what={self.what}&where={self.where}&amount={self.amount}'
        self.parser = cache.get(search_query)

        if not self.parser:
            print(f'Search query "{search_query}" was not in the cache. Making GET request to Indeed...')
            self.parser = self.start_service()
            self.slice_cards()
            if self.parser:
                cache.set(search_query, self.parser)
        
        self.extracter = JobDataService(self.parser.cards)
        programming_language = [[],[]]  # [ [labels], [data] ]
        frameworks = [[],[]]            # [ [labels], [data] ]

        if self.extracter:
            self.extracter.reset_counts()
            self.extracter.get_counts()
            self.extracter.filter_counts()

            for pl_count in self.extracter.pl_counts:
                programming_language[0].append(pl_count[0]) # Appends labels for data.
                programming_language[1].append(pl_count[1]) # Appends data for graphs.

            for f_count in self.extracter.f_counts:
                frameworks[0].append(f_count[0]) # Appends labels for data.
                frameworks[1].append(f_count[1]) # Appends data for graphs.

        # Raw Card text optimizations.
        for card in self.extracter.cards:
            labeled_pl = JobDataModel.pl
            labeled_f = JobDataModel.f

            # Fix 'Date Posted' Text.
            card.date = 'Posted: ' + card.date[6:]

            # Show -.- if the Card has no rating.
            if card.rating == 'None' or None:
                card.rating = '--'
            
            # Neater text of technologies found in Cards.
            index = 0
            for pl in card.details.programming_languages:
                pl[0] = labeled_pl[index][0]
                index += 1
            
            index = 0
            for f in card.details.frameworks:
                f[0] = labeled_f[index][0]
                index += 1

        context.update(
            {
                'what': self.what,
                'where': self.where,
                'amount': self.amount,
                'range': range(1*15, 11*15, 15),
                'max_range': range(1*15, self.amount, 15),
                'parser': self.parser if self.parser else None,
                'pl': programming_language if any(programming_language) else None,
                'f': frameworks if any(frameworks) else None
            }
        )

        return context
    
    def start_service(self) -> JobCardService:
        """
        Starts JobCardService to query and parse Indeed based on user input.
        Returns: List of JobCardModels; Individual job posts and their parsed metrics.
        """
        if self.what and not self.where:
            parser = JobCardService(self.what)
        elif self.what and self.where:
            parser = JobCardService(self.what, self.where)
        else:
            print(f'start_service() could not be started.')
            return None
        
        parser.max_results = self.amount
        parser.parse_page_results()

        return parser
    
    def slice_cards(self):
        ''' Slices cards into even chunks of 15. '''
        print('Splitting', len(self.parser.cards), 'into even cuts of 15 each.')
        self.parser.cards = [self.parser.cards[x:x+15] for x in range(0, len(self.parser.cards), 15)]
    
    def get_success_url(self):
        return reverse('job_scraper:search') + str(f'?what={self.what}&where={self.where}&amount={self.amount}')
