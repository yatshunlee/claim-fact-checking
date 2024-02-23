import torch
import numpy as np
from pandas import DataFrame
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class RelevantContextRetriever:
    def __init__(self, num_results=5):
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
            'date_publish': context_df.date_publish.iloc[list(news_indices[0])].to_list(),
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
        
class RelevantContextRetriever2:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.nli_model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli').to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')
        
    def __call__(self, query, context_df):
        relevant_scores = []
        
        for i in range(context_df.shape[0]):
            x = self.tokenizer.encode(
                context_df.title[i], query, return_tensors='pt',
                truncation_strategy='only_first').to(self.device)
            
            logits = self.nli_model(x)[0]
      
            entail_contradiction_logits = logits[:,[0,2]]
            probs = entail_contradiction_logits.softmax(dim=1)
            prob_label_is_true = probs[:,1]
            relevant_scores.append(prob_label_is_true[0].cpu().detach().numpy())

            torch.cuda.empty_cache()
        
        context_df['relevant_score'] = relevant_scores
        context_df = context_df.sort_values(by='relevant_score', ascending=False)
        
        return context_df.iloc[:3]
        
        # return DataFrame({
        #     'date_publish': [context_df['date_publish'].iloc[0]],
        #     'title': [context_df['title'].iloc[0]],
        #     'sentence': [context_df['maintext'].iloc[0]]
        # })
