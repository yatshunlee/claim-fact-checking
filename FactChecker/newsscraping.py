from pandas import DataFrame
from googlesearch import search
from newsplease import NewsPlease

class NewsScraper:
    def __init__(self):
        self.google_search_query = (
            'site:nytimes.com OR '
            'site:bbc.com OR '
            'site:cnn.com OR '
            'site:washingtonpost.com'
            '{query} '
            '2023..2024')
            
    def get_relevant_urls(self, query, num_results, tbs):
        gsq = self.google_search_query.format(query=query)
        
        urls = []
        for url in search(gsq, stop=num_results): # , tbs='qdr:m'
            urls.append(url)
        
        return urls
    
    def __call__(self, query, num_results=10, tbs=''):
        urls = self.get_relevant_urls(query, num_results, tbs)
        
        context = {
            'url': [], 'title': [],
            'description': [], 'maintext': [], 'date_publish': []}
            
        
        context['url'] = urls
        for i in range(len(urls)):
            article = NewsPlease.from_url(urls[i])
            try:
                context['title'].append(article.title)
                context['description'].append(article.description)
                context['maintext'].append(article.maintext)
                context['date_publish'].append(article.date_publish)
            except:
                for key in ['title', 'description', 'maintext', 'date_publish']:
                    context[key].append('')
                    
        return DataFrame(context)
     
     

if __name__ == "__main__":
    print('Hello')