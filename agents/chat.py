# https://youtu.be/32k6DRcX4pA?si=d36N8CigNngiso7i
import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="compound-beta-mini",
)

print(chat_completion.choices[0].message.content)
