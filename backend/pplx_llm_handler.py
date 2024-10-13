# Import necessary libraries
import requests

class PerplexityLLMHandler:
    def __init__(self, api_key):
        # Use the correct Perplexity API endpoint (replace with the actual endpoint when testing real calls)
        self.api_url = "https://api.perplexity.ai/v1/generate_itinerary"  # Hypothetical endpoint, adjust as needed
        self.api_key = api_key

    def get_itinerary(self, preferences):
        # Set up headers for API call
        headers = {
            'Authorization': f'Bearer {self.api_key}',  # Add your API key in the header
            'Content-Type': 'application/json',
        }
        
        # Real API call, commented out for now
        # response = requests.post(self.api_url, json=preferences, headers=headers)

        # Mock response to simulate an API call for testing purposes
        response = self.mock_response(preferences)
        
        if response['status_code'] == 200:
            # Return the generated itinerary from the response
            return response['data']
        else:
            # Raise an exception if the API call fails
            raise Exception(f"API call failed: {response['status_code']} - {response['message']}")

    def mock_response(self, preferences):
        """Mock function to simulate a successful API call."""
        mock_data = {
            'status_code': 200,
            'data': {
                'destination': preferences.get('destination', 'Unknown Destination'),
                'start_date': preferences.get('start_date', 'Unknown Start Date'),
                'end_date': preferences.get('end_date', 'Unknown End Date'),
                'itinerary': [
                    {
                        'day': 1,
                        'activities': ['Visit museum', 'Walk around old town', 'Dinner at local restaurant']
                    },
                    {
                        'day': 2,
                        'activities': ['Hiking', 'Explore the park', 'Visit a gallery']
                    }
                ],
                'budget': preferences.get('budget', 'Unknown Budget'),
                'interests': preferences.get('interests', 'Unknown Interests'),
            },
            'message': 'Mock response successful!'
        }
        return mock_data

# Example of using the handler in a Streamlit app or test case

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

    # Call the function to get the itinerary from Perplexity API (mocked in this case)
    itinerary = handler.get_itinerary(preferences)
    return itinerary
