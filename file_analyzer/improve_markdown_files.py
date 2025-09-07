"""
Read markdown files and make improvements

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = "tdiprima"
__version__ = "1.0"
__license__ = "MIT"

import os
from pathlib import Path

from groq import Groq

# Set your Groq API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Directory containing Markdown files
home_directory = os.environ["HOME"]
MARKDOWN_DIR = home_directory + "/path/to/markdown/files"
OUTPUT_DIR = home_directory + "/path/to/output/files"


def improve_markdown(file_path, output_path):
    """
    Read a Markdown file, send its content to compound-beta-mini for improvement, and save the response.
    """
    content = Path(file_path).read_text()
    print(f"Processing: {file_path}")

    # Construct the OpenAI prompt
    prompt = f"""You are a helpful assistant. Here is some Markdown content. Can you rewrite it to make it better while keeping the meaning the same?

Content:
{content}
"""

    try:
        # Call compound-beta-mini (or mixtral-8x7b-32768)
        response = client.chat.completions.create(
            model="compound-beta-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in writing and improving markdown content.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Extract improved content
        improved_content = response.choices[0].message.content

        # Save the improved content to the output file
        Path(output_path).write_text(improved_content)
        print(f"Improved content saved to: {output_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def process_markdown_files(input_dir, output_dir):
    """
    Process all Markdown files in the input directory.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Iterate through all markdown files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".md"):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            improve_markdown(input_path, output_path)


if __name__ == "__main__":
    process_markdown_files(MARKDOWN_DIR, OUTPUT_DIR)
