import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

# ---------------- ENV ----------------
load_dotenv()

# ---------------- LLM ----------------
openrouter_llm = ChatOpenAI(
    model="xiaomi/mimo-v2-flash:free",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

# ---------------- Schema ----------------
class Movie(BaseModel):
    title: str = Field(description="Movie Title")
    year: int = Field(description="Movie Release Year")

class AllMovies(BaseModel):
    movies: List[Movie]

movie_llm = openrouter_llm.with_structured_output(AllMovies)

# ---------------- UI ----------------
st.set_page_config(page_title="AI Movie Generator", page_icon="🎬")
st.title("🎬 AI Movie Generator")
st.write("Generate recent movies using OpenRouter AI + Structured Output")

num_movies = st.slider("Number of movies", 5, 20, 10)

if st.button("Generate Movies"):
    with st.spinner("Generating..."):
        prompt = f"""
        Give me a list of {num_movies} recent movies.
        Return the result strictly in JSON format following this schema:
        {{
          "movies": [
            {{
              "title": "string",
              "year": number
            }}
          ]
        }}
        """

        try:
            res = movie_llm.invoke(prompt)
            st.success("Movies generated successfully!")

            for i, m in enumerate(res.movies, 1):
                st.markdown(f"**{i}. {m.title} ({m.year})**")

        except Exception as e:
            st.error("AI Output Parsing Failed")
            st.code(str(e))

st.markdown("---")
st.caption("Powered by LangChain + OpenRouter + Structured AI")