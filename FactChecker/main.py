from newsscraping import NewsScraper
from frauddetection import FraudDetector
from similarity import RelevantContextRetriever

if __name__ == "__main__":
    print("I am a Fact Checking Robot.")
    
    news_scraper = NewsScraper()   
    fraud_detector = FraudDetector()
    relevant_context_retriever = RelevantContextRetriever()
    
    while True:
        query = input("Do you fact-check any statement? You can exit by type q.\n")
        if query == "q":
            print("Goodbye!")
            break
            
        print('News Scraping...')
        context_df = news_scraper(query)
        print('Done news scraping.')
        print('Building relevant prompt...')
        relevant_context_df = relevant_context_retriever(query, context_df)
        print('Built relevant prompt.')
        
        context = []
        for i in range(relevant_context_df.shape[0]):
            title = relevant_context_df.at[i, 'title']
            sen = relevant_context_df.at[i, 'sentence']
            context.append(f'source: {title}\n{sen}')
        
        context = '\n'.join(context)
        
        print('Prompt for GPT3.5:')
        
        response = fraud_detector(query, context)
        print(response)