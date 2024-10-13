# WORKING VER OF PPLX LLM HANDLER. ARCHIVED HERE FOR TESTING REASONS (NEED TO ADD MOCK API CALLS IN REAL VERSION RIGHT NOW)

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

# Example of using the handler in a Streamlit app

def generate_itinerary_from_profile(api_key, destination, start_date, end_date, interests, travel_type, budget):
    # Initialize the handler with your actual API key
    handler = PerplexityLLMHandler(api_key=api_key)

    # User travel preferences - these will be passed as a JSON object to the Perplexity API
    preferences = {
        'destination': destination,
        'start_date': str(start_date),
        'end_date': str(end_date),
        'interests': interests.split(','),  # Split interests into a list
        'travel_type': travel_type,
        'budget': budget
    }

    # Call the function to get the itinerary from Perplexity API
    itinerary = handler.get_itinerary(preferences)
    return itinerary

