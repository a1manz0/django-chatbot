from langchain import HuggingFaceHub
from dotenv import load_dotenv
import os


load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
llm=HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
                   huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
                   model_kwargs={"max_new_tokens":1200})
print(llm("Tell me one joke about data scientist"))
