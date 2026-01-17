from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as sr

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

sr.title("👽 ASSKMEEE AI")
sr.markdown("My bot with langchain and gemini")

if "messages" not in sr.session_state:
    sr.session_state.messages = []

for messages in sr.session_state.messages:
    role = messages["role"]
    content = messages["content"]
    sr.chat_message(role).markdown(content)

query = sr.chat_input("Ask Any Thing... ")
if query:
    sr.session_state.messages.append({"role":"user", "content":query})
    sr.chat_message("user").markdown(query)
    res = llm.invoke(query)
    sr.chat_message("ai").markdown(res.content)
    sr.session_state.messages.append({"role":"ai", "content":res.content})
