import requests

def chat_with_llama(prompt):
    """
    Since the native Llama-2-7b model format requires complex setup,
    let's use Ollama to serve it instead. First, we need to import the model into Ollama.
    """
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={"model": "llama2:7b", "prompt": prompt, "stream": False}
        )
        
        if response.status_code == 200:
            return response.json().get('response', 'No response field found')
        else:
            return f"Error: {response.status_code} - {response.text}. Make sure Ollama is running and has llama2:7b model."
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Please start Ollama and run 'ollama pull llama2:7b' first."
    except Exception as e:
        return f"Error: {str(e)}"

print("💬 Hiro AI is ready. Type 'exit' to quit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    print("Hiro:", chat_with_llama(user_input))