import requests

GEMINI_API_KEY = "AIzaSyD_mglywUAV374j_s5wJa9mF1NWW8GoATY"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def get_gemini_response(conversation_history):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    # Dynamic prompt: include conversation history
    prompt = "You are a helpful assistant. Continue the conversation based on the following history:\n"
    for turn in conversation_history:
        prompt += f"{turn['role']}: {turn['content']}\n"
    prompt += "Assistant:"
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        except (KeyError, IndexError):
            return "Sorry, I couldn't understand the response."
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    print("AI Chatbot (Gemini API, Dynamic Prompting). Type 'exit' to quit.")
    conversation_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        conversation_history.append({"role": "User", "content": user_input})
        response = get_gemini_response(conversation_history)
        print("Bot:", response)
        conversation_history.append({"role": "Assistant", "content": response})

if __name__ == "__main__":
    main()