import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)
user_input = input("Enter your prompt: ")
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_input,
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)