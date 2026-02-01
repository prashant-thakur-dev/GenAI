import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model="arcee-ai/trinity-large-preview:free",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    streaming=True
)

question = "explain gen ai in detail"

res = llm.stream(question)
for chunk in res:
    print(chunk.content, end="")