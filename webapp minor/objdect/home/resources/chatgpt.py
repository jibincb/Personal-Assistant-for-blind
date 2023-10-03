import openai

# Set up your OpenAI API credentials
openai.api_key = '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'

# Define a function to send a message and receive a response from ChatGPT
def send_message(message):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the GPT model to use
        prompt=message,
        max_tokens=50,  # Adjust the response length as per your requirement
        temperature=0.7,  # Controls the randomness of the output
        n = 1,  # Number of responses to generate
        stop=None,  # Stop generating further tokens at a specific sequence (optional)
        timeout=30,  # Timeout limit for the API request (optional)
    )
    
    # Extract and return the reply from the API response
    reply = response.choices[0].text.strip()
    return reply


# Continue the conversation
# while True:
#     user_message = input("User: ")
#     bot_message = send_message(user_message)
#     print("Bot:", bot_message)
