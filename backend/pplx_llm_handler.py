import requests

class PerplexityLLMHandler:
    def __init__(self, api_key):
        # Use the correct Perplexity API endpoint (replace with the actual endpoint)
        self.api_url = "https://api.perplexity.ai/v1/generate_itinerary"  # Hypothetical endpoint, adjust as needed
        self.api_key = api_key

    def get_itinerary(self, preferences):
        # Set up headers for API call
        headers = {
            'Authorization': f'Bearer {self.api_key}',  # Add your API key in the header
            'Content-Type': 'application/json',
        }
        
        # Make the POST request to the Perplexity API with user preferences as the payload
        response = requests.post(self.api_url, json=preferences, headers=headers)
        
        if response.status_code == 200:
            # Return the generated itinerary from the response
            return response.json()
        else:
            # Raise an exception if the API call fails
            raise Exception(f"API call failed: {response.status_code} - {response.text}")

# Example of using the handler
# Initialize the handler with your actual API key
handler = PerplexityLLMHandler(api_key="pplx-e0a9601780b78e0825c85b74f452b79dd794f43a5239a8130")

# User travel preferences
preferences = {
    'destination': 'Paris',
    'budget': 1500,
    'interests': ['hiking', 'art'],
    'start_date': '2024-10-15',
    'end_date': '2024-10-25'
}

# Call the function to get the itinerary
itinerary = handler.get_itinerary(preferences)
print(itinerary)
