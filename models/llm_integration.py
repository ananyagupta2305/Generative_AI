# # # models/llm_integration.py
# # import requests

# # def get_llm_response(prompt):
# #     # Assuming you have the API endpoint and necessary headers
# #     url = "https://api.groq.com/openai/v1/chat/completions"  # Replace with your actual endpoint
# #     headers = {
# #         "Authorization": "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",  # Replace with your actual API key
# #         "Content-Type": "application/json"
# #     }
# #     data = {
# #         "prompt": prompt,
# #         "max_tokens": 1500  # Adjust as needed
# #     }
    
# #     response = requests.post(url, headers=headers, json=data)
# #     if response.status_code == 200:
# #         return response.json().get('response', 'No response found.')
# #     else:
# #         return "Error: Unable to get response from LLM."



# models/llm_integration.py
import requests
import os

def get_llm_response(prompt):
    # Endpoint URL (verify that this is the correct URL for Groq's API)
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Retrieve API key from environment variable
    api_key = os.getenv("GROQ_API_KEY", "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")
    headers = {
        "Authorization": f"Bearer {api_key}",  # Make sure the token format matches Groq's requirements
        "Content-Type": "application/json"
    }
    
    # Payload according to expected API structure
    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "llama3-8b-8192",
        "max_tokens": 1500,  # Adjust token limit as needed
        "temperature" : 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        # Check if the response is successful
        if response.status_code == 200:
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', 'No response content found.')
        else:
            # Detailed error message for troubleshooting
            return f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}"
    
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        return f"Request error: {str(e)}"






# import requests
# import os

# def get_llm_response(prompt, context):
#     # Combine the context and the prompt if needed
#     combined_prompt = f"{context}\n{prompt}"
    
#     # Endpoint URL
#     url = "https://api.groq.com/openai/v1/chat/completions"
    
#     # Retrieve API key from environment variable
#     api_key = os.getenv("GROQ_API_KEY", "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")
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
    
#     # Payload according to expected API structure
#     data = {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": combined_prompt  # Use the combined prompt
#             }
#         ],
#         "model": "llama3-8b-8192",
#         "max_tokens": 1500,
#         "temperature": 0.9
#     }
    
#     try:
#         response = requests.post(url, headers=headers, json=data)
        
#         # Check if the response is successful
#         if response.status_code == 200:
#             result = response.json()
#             return result.get('choices', [{}])[0].get('message', {}).get('content', 'No response content found.')
#         else:
#             return f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}"
    
#     except requests.exceptions.RequestException as e:
#         return f"Request error: {str(e)}"
