import os
import streamlit as st
from openai import OpenAI


def get_client():
    api_key = st.secrets.get(
        "GROQ_API_KEY",
        os.getenv("GROQ_API_KEY")
    )

    if not api_key:
        raise ValueError("Groq API key is missing!")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )


def ask_ai(prompt, system_message):
    client = get_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def ask_ai_stream(messages):
    client = get_client()

    return client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        stream=True
    )