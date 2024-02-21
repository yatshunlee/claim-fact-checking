import os
import openai
from openai import OpenAI

class FraudDetector:
    def __init__(self, openai_api_key="REPLACEWITHYOUROPENAIAPIKEY"):
        if openai_api_key == "REPLACEWITHYOUROPENAIAPIKEY":
            raise ValueError("Replace with your openai api key.")
        self.client = OpenAI(api_key=openai_api_key)
        self.prompt = (
            'Based only on the context:\n'
            '{context}'
            'Tell me if this statement is a fact: {query}'
            'Your replying format: <Your answer> <evidence in simple words with source>'
        )
        
    def __call__(self, query, context, temperature=.5):
        session = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": self.prompt.format(query=query, context=context)
            }],
            temperature=temperature
        )

        response = session.choices[0].message.content
        return response
