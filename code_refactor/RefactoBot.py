"""
This script analyzes Python code files using Groq AI to detect inefficiencies, suggest improvements,
refactor the code, and save the optimized versions with a prefixed filename while providing performance metrics.

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = 'tdiprima'
__version__ = '1.0'
__license__ = 'MIT'

import os
import timeit

from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def load_code_from_project_directory(directory_path):
    """Load all Python files from the given directory."""
    code_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    code_files.append((file, f.read()))
    return code_files


def analyze_code_with_groq(system_prompt, user_prompt):
    """Send code to Groq AI model for analysis and suggestions."""
    try:
        response = client.chat.completions.create(model="llama3-8b-8192",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}])
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return str(e)


def profile_runtime(original_code, refactored_code):
    """Compare execution time of original and refactored code."""

    def execute_code(code):
        try:
            exec(code, {})
        except Exception as e:
            return str(e)

    original_time = timeit.timeit(lambda: execute_code(original_code), number=10)
    refactored_time = timeit.timeit(lambda: execute_code(refactored_code), number=10)
    return {"original_time": original_time, "refactored_time": refactored_time}


def display_results(issues, refactorings, performance_metrics):
    """Present analysis and suggestions in a developer-friendly format."""
    print("\nStatic Code Issues:")
    for issue in issues:
        print("-", issue)

    print("\nSuggested Refactorings:")
    print(refactorings)

    print("\nPerformance Metrics:")
    print("Original Time:", performance_metrics["original_time"], "seconds")
    print("Refactored Time:", performance_metrics["refactored_time"], "seconds")


def save_refactored_code(refactored_code, original_filename):
    """Save refactored code to a file named based on the original file."""
    refactored_filename = f"refactored_{original_filename}"
    with open(refactored_filename, "w") as file:
        file.write(refactored_code)
    print(f"Refactored code saved as: {refactored_filename}")


def main():
    directory_path = "./example_project"  # TODO: Replace with your directory
    system_prompt = "You are an expert code analyzer and refactorer. Detect inefficiencies and suggest improvements."

    code_files = load_code_from_project_directory(directory_path)

    for original_filename, input_code in code_files:
        print(f"\nProcessing file: {original_filename}...")

        user_prompt = f"Analyze and refactor the following code:\n{input_code}"
        groq_response = analyze_code_with_groq(system_prompt, user_prompt)

        refactored_code = groq_response
        performance_metrics = profile_runtime(input_code, refactored_code)

        display_results([], refactored_code, performance_metrics)
        save_refactored_code(refactored_code, original_filename)


if __name__ == "__main__":
    main()
