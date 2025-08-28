import requests

GEMINI_API_KEY = "AIzaSyD_mglywUAV374j_s5wJa9mF1NWW8GoATY"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def count_tokens(text):
    # Simple token estimation: split by whitespace and punctuation
    import re
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    return len(tokens)

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
        ],
        "generationConfig": {
            "topP": 0.7,        # Nucleus sampling
            "temperature": 0.8  # Updated temperature for more creative responses
        }
    }
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    prompt_tokens = count_tokens(prompt)
    if response.status_code == 200:
        result = response.json()
        try:
            reply = result['candidates'][0]['content']['parts'][0]['text'].strip()
            reply_tokens = count_tokens(reply)
            total_tokens = prompt_tokens + reply_tokens
            print(f"[Token Usage] Prompt: {prompt_tokens}, Response: {reply_tokens}, Total: {total_tokens}")
            return reply
        except (KeyError, IndexError):
            print(f"[Token Usage] Prompt: {prompt_tokens}, Response: 0, Total: {prompt_tokens}")
            return "Sorry, I couldn't understand the response."
    else:
        print(f"[Token Usage] Prompt: {prompt_tokens}, Response: 0, Total: {prompt_tokens}")
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