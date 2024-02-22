import torch
from huggingface_hub import login
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class GemmaFraudDetector:
    def __init__(self, hf_token="REPLACEWITHYOURHFTOKEN", temperature=1, top_p=1):
        login(hf_token)
        self.prompt = (
            'Based only on the context:\n'
            '{context}'
            'Tell me if this statement is a fact: {query}\n'
            'You must reply in this format:\n'
            'Answer: <Your answer>\n'
            'Evidence: <evidence in simple words with source>'
        )
        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
        self.model = AutoModelForCausalLM.from_pretrained(
            "google/gemma-2b-it", 
            device_map="auto", 
            torch_dtype=torch.bfloat16)
        
    def __call__(self, query, context, max_length=500):
        input_text = self.prompt.format(query=query, context=context)
        input_ids = self.tokenizer(
            input_text, 
            return_tensors="pt").to("cuda")
            
        outputs = self.model.generate(max_length=max_length, **input_ids)
        response = self.tokenizer.decode(outputs[0])[len(input_text)+5:-5].strip()
        return response