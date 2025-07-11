"""
Instead of re-writing the file, just print the file name and give a brief summary.

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = 'tdiprima'
__version__ = '1.0'
__license__ = 'MIT'

import os

from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

INPUT_FOLDER = "/path/to/your/scripts"

SUPPORTED_FILE_TYPES = [".js", ".py", ".java"]


def process_file(file_path):
    """Analyze the file and print its name and a summary of its functionality."""
    with open(file_path, "r") as file:
        content = file.read()

    prompt = f"""You are a code analysis assistant. Please read the following code and summarize its functionality in one sentence. 
    Just write the summary in plain text.

Code:
{content}
"""

    try:
        response = client.chat.completions.create(
            model="compound-beta-mini",
            messages=[{"role": "system", "content": "You are an expert in analyzing code"},
                      {"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content.strip()
        # Print the file name and summary
        print(f"File: {file_path}")
        print(f"Summary: {summary}\n")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def process_folder(folder_path):
    """Process all supported files in the folder."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_FILE_TYPES):
                process_file(os.path.join(root, file))


process_folder(INPUT_FOLDER)
