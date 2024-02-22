from tabulate import tabulate
from newsscraping import NewsScraper
from fraud_detection_gemma import GemmaFraudDetector
from similarity import RelevantContextRetriever, RelevantContextRetriever2

import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    print("\n\nI am a Fact Checking Robot.")
    
    news_scraper = NewsScraper()   
    fraud_detector = GemmaFraudDetector()
    relevant_context_retriever = RelevantContextRetriever()
    relevant_context_retriever2 = RelevantContextRetriever2()
    
    while True:
        query = input("You can type q to exit, or input the statement you want to fact-check: ")
        if query == "q":
            print("Goodbye!")
            break
            
        print('News Scraping...')
        context_df = news_scraper(query)
        print('Done news scraping.')
        print('Building relevant prompt...')
        relevant_context_df = relevant_context_retriever2(query, context_df)
        relevant_context_df = relevant_context_retriever(query, relevant_context_df)
        print('Built relevant prompt.')
        
        print('Show relevant content:')
        print(tabulate(relevant_context_df, headers='keys', tablefmt='psql'))
        context = []
        for i in range(relevant_context_df.shape[0]):
            title = relevant_context_df.at[i, 'title']
            sen = relevant_context_df.at[i, 'sentence']
            context.append(f'source: {title}\n{sen}')
        
        context = '\n'.join(context)
        
        response = fraud_detector(query, context)
        print(response)
        print('\n')