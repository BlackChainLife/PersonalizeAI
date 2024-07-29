import os, sys
from openai import OpenAI
from openai.types.model import Model
from dotenv import load_dotenv
from openai_usage.schema import openAIModel  # 修正了拼写错误
from typing import List

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")

client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)

model_list : List[Model] = client.models.list().data

for k in model_list:
    print(k.to_dict())

