import os
import streamlit as st
from groq import Groq

# Read API key from Streamlit Secrets if available, otherwise from .env
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Groq API Key not found.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="AI FAQ Generator", page_icon="❓")

st.title("❓ AI FAQ Generator")
st.write("Generate Frequently Asked Questions and Answers using AI.")

topic = st.text_input("Enter a Topic")

num_questions = st.selectbox(
    "Number of FAQs",
    [3, 5, 7, 10],
    index=1
)

if st.button("Generate FAQs"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:

        prompt = f"""
Generate {num_questions} Frequently Asked Questions (FAQs) about {topic}.

For each FAQ use this format:

Q1:
Answer:

Q2:
Answer:

Keep the answers simple, clear, and beginner-friendly.
"""

        with st.spinner("Generating FAQs..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
            )

        output = response.choices[0].message.content

        st.success("FAQs Generated Successfully!")
        st.markdown(output)