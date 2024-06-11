#!/usr/bin/env python3
#coding: utf-8
from openai import OpenAI
from os import getenv

def generate(user_prompt,
                 system_prompt="",
                 model="gpt-4",
                 temperature_value=0.7,
                 max_tokens_value=64,
                 top_p_value=1
                ):

    client = OpenAI(api_key=getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model=f"{model}",
        messages=[
            {
                "role": "system",
                "content": f"{system_prompt}"
            },
            {
                "role": "user",
                "content": f"{user_prompt}"
            }
        ],
        temperature=temperature_value,
        max_tokens=max_tokens_value,
        top_p=top_p_value
    )

    return response.choices[0].message.content

