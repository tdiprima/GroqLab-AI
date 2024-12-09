import os

from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Define the team of agents
def agent_requirements_gatherer(prompt):
    """
    Agent responsible for gathering requirements from the user.
    """
    print("Agent 1: Gathering requirements...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.2-3b-preview",
    )
    requirements = chat_completion.choices[0].message.content
    print("Requirements gathered:", requirements)
    return requirements

def agent_designer(requirements):
    """
    Agent responsible for designing the application architecture.
    """
    print("Agent 2: Designing application architecture...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Design an application architecture based on the following requirements: {requirements}",
            }
        ],
        model="llama-3.2-3b-preview",
    )
    design = chat_completion.choices[0].message.content
    print("Application architecture designed:", design)
    return design

def agent_implementer(design):
    """
    Agent responsible for implementing the application code.
    """
    print("Agent 3: Implementing application code...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Write a Python script based on the following application architecture: {design}",
            }
        ],
        model="llama-3.2-3b-preview",
    )
    implementation = chat_completion.choices[0].message.content
    print("Application code implemented:", implementation)
    return implementation

# Define the main function that coordinates the team of agents
def develop_application(prompt):
    requirements = agent_requirements_gatherer(prompt)
    design = agent_designer(requirements)
    implementation = agent_implementer(design)
    return implementation

# Test the team of agents
# prompt = "Write a Python script that showcases a unique visual 2D game that's not snake."
prompt = "Write a Python script that shows balls moving around inside a 2D game."
implementation = develop_application(prompt)

# Save the implementation as a Python file
with open("application.py", "w") as f:
    f.write(implementation)

print("Application developed and saved to application.py")
