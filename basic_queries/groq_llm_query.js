/*
node groq_llm_query.js "Explain the importance of fast language models"
*/

import Groq from "groq-sdk";

// Initialize Groq client
const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

// Main function
async function main() {
  // Retrieve the prompt from the command-line arguments
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Please provide a prompt as a command-line argument.");
    process.exit(1);
  }
  const userPrompt = args.join(" ");

  try {
    // Send prompt to the Groq API
    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: "user",
          content: userPrompt,
        },
      ],
      model: "compound-beta-mini",
    });

    // Print the API response
    console.log("Response:");
    console.log(chatCompletion.choices[0]?.message?.content || "No response received.");
  } catch (error) {
    console.error("Error:", error.message || error);
  }
}

// Run the main function
main();
