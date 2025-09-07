import os

from groq import Groq

# Initialize the client with your API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# List all available models
models = client.models.list()
for model in models.data:
    print(model.id)
