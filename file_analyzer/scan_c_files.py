"""
Extracts names and URLs from C/C++ source and header files.
"""

import os

from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_c_files(directory):
    c_files = []
    for root, dirs, files in os.walk(directory):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith((".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".hxx")):
                c_files.append(os.path.join(root, file))
    return c_files


def read_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""


def extract_possible_names_or_urls(content):
    prompt = (
        "Extract any names or URLs that appear to be identifiers, authors, or references in the given C/C++ file. "
        "Do not include any preamble or extra text, just list the extracted names or URLs."
    )

    # Get response from Groq
    response = client.chat.completions.create(
        model="compound-beta-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content[:4000]},
        ],
    )  # Limit to 4000 characters

    return response.choices[0].message.content.strip()


def main(directory):
    c_files = get_c_files(directory)

    for file in c_files:
        content = read_file_content(file)
        if content:
            extracted_info = extract_possible_names_or_urls(content)
            if extracted_info:
                print(f"File: {file}")
                print(extracted_info)
                print("-" * 40)


if __name__ == "__main__":
    target_directory = "."  # Change this to the directory you want to scan
    main(target_directory)
