import os, sys
from openai import OpenAI
from openai.types.model import Model
from dotenv import load_dotenv
from typing import List


openai_api_base = "https://chatgptproxyapi-5uc.pages.dev/v1"
openai_api_key = "sk-proj-47lXqDtlw7AHKd3jZv8nT3BlbkFJs7xLLXX4NmTzQSVsJVCm"



client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)

model_list : List[Model] = client.models.list().data

for k in model_list:
    print(k.to_dict())

