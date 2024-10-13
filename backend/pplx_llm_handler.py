import requests

class PerplexityLLMHandler:
    def __init__(self, api_key):
        self.api_url = "https://api.perplexity.ai/generate_itinerary"  # Replace with actual API endpoint
        self.api_key = api_key

    def get_itinerary(self, preferences):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        response = requests.post(self.api_url, json=preferences, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API call failed: {response.status_code} - {response.text}")

# Example of using the handler
# handler = PerplexityLLMHandler(api_key="your_api_key")
# preferences = {'destination': 'Paris', 'budget': 1500, 'interests': ['hiking', 'art']}
# itinerary = handler.get_itinerary(preferences)
# print(itinerary)
