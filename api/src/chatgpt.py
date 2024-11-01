from .settings import app_settings as settings
import requests

def get_chatgpt_response(prompt, message):
    # Define the request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.OPENAI_API_KEY}'
    }

    # Build the messages list
    messages = []
    if prompt:
        # Include the prompt as a system message
        messages.append({"role": "system", "content": prompt})
    # Add the user message
    messages.append({"role": "user", "content": message})

    # Define the payload without the prompt parameter
    data = {
        "model": settings.OPENAI_API_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 150
    }

    # Send a request to the OpenAI API
    response = requests.post(settings.OPENAI_API_URL, headers=headers, json=data)

    # Check the response status and return the generated response
    if response.status_code == 200:
        return response.json().get("choices")[0].get("message").get("content")
    else:
        # Handle any errors in response
        raise Exception(f"Error: {response.status_code} - {response.text}")
