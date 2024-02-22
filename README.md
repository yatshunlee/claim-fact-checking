# claim-fact-checking
A cli, python based application to fact check a statement by comparing to relevant and recent news.
## Installation
```
git clone https://github.com/yatshunlee/claim-fact-checking.git
conda env create -f env/environment.yml
conda activate claim-fact-check
```
## Usage
1. replace with your valid openai api key in `frauddetection.py`
2. run `python main.py`
## Architecture
[more about the architecture](https://yatshunlee.super.site/projects/llm-for-fact-checking)
![image](https://github.com/yatshunlee/claim-fact-checking/assets/69416199/2c6a94ca-9c95-4f64-9cee-346e188f337d)
## Fact Checker
### Check statement: Joe Biden told people not to vote
![image](https://github.com/yatshunlee/claim-fact-checking/assets/69416199/87ceed02-dafc-4d07-bec7-bb404efc0a3d)
![image](https://github.com/yatshunlee/claim-fact-checking/assets/69416199/ae35abcf-0955-4743-b743-753ec157887a)

### Check statement: Taylor Swift Promoting Le Creuset Cookware
![image](https://github.com/yatshunlee/claim-fact-checking/assets/69416199/b1cd6117-3410-4fd8-8f5a-2af6e04bed98)
![image](https://github.com/yatshunlee/claim-fact-checking/assets/69416199/78646f09-0061-41ea-84bc-b45eb7bc1aaf)
