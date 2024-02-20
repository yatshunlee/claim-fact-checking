import numpy as np
from pandas import DataFrame
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer

class RelevantContextRetriever:
    def __init__(self, num_results=3):
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.knn = NearestNeighbors(n_neighbors=num_results)
        
    def __call__(self, query, context_df):
        sentences, sentence_to_id = self.get_sentences_and_title_ids(context_df)
        self.fit(sentences)
        
        # get nearest sentences and titles
        target = self.embedding_model.encode(query)
        coontent_indices = self.knn.kneighbors(target[np.newaxis, :], return_distance=False)
        news_indices = np.array(sentence_to_id)[coontent_indices]
        
        # return searching result
        relevant = np.array(sentences)[coontent_indices][0] # index 0 is to turn into 1D
        return DataFrame({
            'title': context_df.title.iloc[list(news_indices[0])].to_list(),
            'sentence': relevant
        })
    
    def fit(self, sentences):
        embeddings = self.embedding_model.encode(sentences)
        self.knn.fit(embeddings)
    
    def split_into_sentences(self, text):
        # # Define the regex pattern for sentence splitting
        # sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'

        # # Split the text into sentences using the pattern
        # sentences = re.split(sentence_pattern, text)

        # return sentences
        return text.split('\n')
        
    def get_sentences_and_title_ids(self, context_df):
        # get list of sentences
        sentences = context_df.maintext.apply(self.split_into_sentences)
        # get corresponding title indices
        numbers_of_sentences = sentences.apply(len)
        sentence_to_id = []
        for i, num in enumerate(numbers_of_sentences):
            sentence_to_id += [i] * num
        return [sentence for lst in sentences for sentence in lst], sentence_to_id