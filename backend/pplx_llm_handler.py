# Import necessary libraries
import requests

class PerplexityLLMHandler:
    def __init__(self, api_key, use_mock=False):
        # Use the correct Perplexity API endpoint
        self.api_url = "https://api.perplexity.ai/chat/completions"  # Correct endpoint from the API docs
        self.api_key = api_key
        self.use_mock = use_mock  # Control whether to use mock responses or real API calls

    def get_itinerary(self, preferences):
        # Set up headers for API call
        headers = {
            'Authorization': f'Bearer {self.api_key}',  # Add your API key in the header
            'Content-Type': 'application/json',
        }
        
        # Prepare the payload based on the API specifications
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",  # Replace with actual model, if needed
            "messages": [
                {
                    "role": "system",
                    "content": "Generate an optimal travel itinerary based on the user preferences."
                },
                {
                    "role": "user",
                    "content": (
                        f"Generate a travel itinerary for {preferences.get('destination')} from "
                        f"{preferences.get('start_date')} to {preferences.get('end_date')} with interests "
                        f"in {', '.join(preferences.get('interests', []))} and a budget of {preferences.get('budget')}."
                    )
                }
            ],
            "temperature": 0.2,
            "top_p": 0.9,
            "return_citations": False,
            "return_images": False,
            "return_related_questions": False,
        }

        if self.use_mock:
            # Mock response to simulate an API call for testing purposes
            response = self.mock_response(preferences)
        else:
            # Make the real API call
            response = requests.post(self.api_url, json=payload, headers=headers)

            # Check if the response is valid
            if response.status_code == 200:
                response = response.json()
            else:
                raise Exception(f"API call failed: {response.status_code} - {response.text}")
        
        # Return the generated itinerary from the response
        return response['data']

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
def generate_itinerary_from_profile(api_key, destination, start_date, end_date, interests, travel_type, budget, use_mock=False):
    # Initialize the handler with your actual API key
    handler = PerplexityLLMHandler(api_key=api_key, use_mock=use_mock)

    # User travel preferences - these will be passed as a JSON object to the Perplexity API
    preferences = {
        'destination': destination,
        'start_date': str(start_date),
        'end_date': str(end_date),
        'interests': interests.split(','),  # Split interests into a list
        'travel_type': travel_type,
        'budget': budget
    }

    # Call the function to get the itinerary from Perplexity API (mocked or real based on `use_mock`)
    itinerary = handler.get_itinerary(preferences)
    return itinerary
