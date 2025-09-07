import os

from groq import Groq

# Initialize the client with your API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello! Who are you?"}],
    # model="llama3-70b-8192"
    model="meta-llama/llama-4-scout-17b-16e-instruct",
)
print(response.choices[0].message.content)
