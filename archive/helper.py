class GoogleSearchQueryOptimizer:
    def __init__(self):
        self.reliable_sources = (
            "site:nytimes.com",
            "site:bbc.com",
            "site:cnn.com",
            "site:theguardian.com",
            "site:washingtonpost.com") # site:yahoo.com
    
    def __call__(self, query, today, need_optimize=False):
        if not need_optimize:
            return ["{query} {reliable_source}".format(
                query=query,
                reliable_source=reliable_source) for reliable_source in self.reliable_sources]
        
        prompt_google_search_query = self.get_prompt(query, today)
        google_search_queries = self.get_queries(prompt_google_search_query)
        return google_search_queries

    def get_prompt(self, query, today):
        """few shot prompting"""
        prompt_google_search_query = (
            "You are a helpful assistant that give a google search query for getting "
            "an accurate and relevant information about a statement.\n"
            "Input: Joe Biden told people not to vote\n"
            "Output: Joe Biden voting statement fact check {reliable_source}\n"
            "Input: Is there a war between China and Taiwan?\n"
            "Output: China Taiwan conflict {reliable_source}\n"
            f"Input: {query}\n"
            "Output: <your keywords> <must keep {reliable_source}>")
        return prompt_google_search_query
    
    def get_queries(self, prompt_google_search_query):
        """using an LLM to generate"""
        return ["Joe Biden vote {reliable_source}".format(
            reliable_source=reliable_source) for reliable_source in self.reliable_sources]
    
    
class FraudDetector:
    def __init__(self, temperature=1):
        self.temperature = temperature
    
    def __call__(self, query, context, today):
        prompt = self.get_prompt(query, context, today)
        return self.llm(prompt)
        
    def llm(self, prompt):
        return prompt
    
    def get_prompt(self, query, context, today):
        prompt = (
            f"Based only on the following context:\n{context}\n"
            f"Given that today is {today}, using the format, which is <TRUE/FALSE/NOT SURE> <your evidence>, "
            f"to answer the question: {query}")
        return prompt