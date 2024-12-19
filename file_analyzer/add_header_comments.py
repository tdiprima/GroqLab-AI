import os

from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Folder to process
INPUT_FOLDER = "/path/to/your/scripts"

# File types to process
SUPPORTED_FILE_TYPES = [".js", ".py"]


def process_file(file_path):
    """Analyze the file and add a header comment summarizing its functionality."""
    with open(file_path, "r") as file:
        content = file.read()

    # Construct Groq prompt
    prompt = f"""You are a code analysis assistant. Please read the following code and summarize its functionality in one sentence. 
    Add the summary as a comment at the top of the file  Don't say "Here is the summary" or things of that nature.  Just write the script.

    Code:
    {content}
    """

    try:
        # Get response from Groq
        response = client.chat.completions.create(model="llama3-8b-8192",
            messages=[{"role": "system", "content": "You are an expert in analyzing code."},
                      {"role": "user", "content": prompt}])

        # Extract the summary from the response
        summary = response.choices[0].message.content.strip()

        # Add header comment
        if file_path.endswith(".js"):
            header_comment = f"// {summary}\n"
        elif file_path.endswith(".py"):
            header_comment = f"# {summary}\n"
        else:
            print(f"Unsupported file type for {file_path}. Skipping.")
            return

        # Write the updated file
        with open(file_path, "w") as file:
            file.write(header_comment + content)

        print(f"Updated file: {file_path}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def process_folder(folder_path):
    """Process all supported files in the folder."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_FILE_TYPES):
                process_file(os.path.join(root, file))


# Run the script
if __name__ == "__main__":
    process_folder(INPUT_FOLDER)
