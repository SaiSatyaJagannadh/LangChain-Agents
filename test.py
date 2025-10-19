# from dotenv import load_dotenv
# import os
# load_dotenv()
# print(os.getenv("OPENAI_API_KEY"))


from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(client.models.list())
