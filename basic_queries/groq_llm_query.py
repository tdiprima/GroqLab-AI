"""
python groq_llm_query.py "Hello! Who are you?"

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = "tdiprima"
__version__ = "1.0"
__license__ = "MIT"

import argparse
import os

from groq import Groq


def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description="Send a prompt to the Groq API and get a response."
    )
    parser.add_argument("prompt", type=str, help="The prompt to send to the Groq API.")
    args = parser.parse_args()

    # Initialize Groq client
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    # Send chat completion request
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": args.prompt,
            }
        ],
        model="compound-beta-mini",
        stream=False,
    )

    # Print the response
    print("\nResponse:")
    print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    main()
