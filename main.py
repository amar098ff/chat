
import requests

GEMINI_API_KEY = "AIzaSyD_mglywUAV374j_s5wJa9mF1NWW8GoATY"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def get_gemini_response(user_input):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    # Zero-shot prompt
    prompt = f"You are a helpful assistant. Answer the user's question as accurately as possible.\nUser: {user_input}\nAssistant:"
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
    print("AI Chatbot (Gemini API, Zero-Shot Prompting). Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = get_gemini_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()
```