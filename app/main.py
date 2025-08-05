import requests

def chat_with_ollama(prompt):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={"model": "qwen2.5:3b", "prompt": prompt, "stream": False}
    )
    
    if response.status_code == 200:
        # Just return the 'response' text directly
        return response.json().get('response', 'No response field found')
    else:
        return f"Error: {response.status_code} - {response.text}"

print("💬 Hiro AI is ready. Type 'exit' to quit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    print("Hiro:", chat_with_ollama(user_input))