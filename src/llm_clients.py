
"""
llm_client.py

This module provides utility functions to interact with different LLM APIs, 
such as OpenAI's GPT-4 and Meta's LLaMA. It includes functions to generate 
responses using various models, handling system prompts and formatting.

API clients for OpenAI and LLaMA are initialized at the beginning.
"""
from openai import OpenAI
from data.key import get_key_openai, get_key_llama

# Set your GPT-4 API key
client = OpenAI(
    api_key= get_key_openai()
)

# Set your llama API key, still using the OpenAI client API
llama = OpenAI(
    api_key=get_key_llama(),
    base_url = "https://api.llama-api.com"
)

def generate_response(prompt, sys_prompt, response_format):
    response = client.beta.chat.completions.parse(
        messages=[
            { "role": "system", "content":  sys_prompt},
            { "role": "user", "content": prompt }
        ],
        #model="gpt-4o",
        model="gpt-4o-mini",
        max_tokens=2000,
        response_format=response_format
    )
    return response.choices[0].message.parsed

def generate_response_llama(prompt, sys_prompt):
    response = llama.beta.chat.completions.parse(
        messages=[
            { "role": "system", "content":  sys_prompt},
            { "role": "user", "content": prompt }
        ],
        model="llama3.3-70b",
        #model="llama3.1-8b",
        max_tokens=2000,
    )
    
    return response.choices[0].message.content
    """
    response = client.beta.chat.completions.parse(
        messages=[
            { "role": "system", "content":  sys_prompt},
            { "role": "user", "content": prompt }
        ],
        #model="gpt-4o",
        model="gpt-4o-mini",
        max_tokens=2000,
    )
    return response.choices[0].message.content
    """


