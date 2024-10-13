import requests
import re

class PerplexityLLMHandler:
    def __init__(self, api_key, use_mock=False):
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.api_key = api_key
        self.use_mock = use_mock

    def get_itinerary(self, preferences):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "Generate three different travel itinerary options based on the user preferences."
                },
                {
                    "role": "user",
                    "content": (
                        f"Generate three travel itinerary options for {preferences.get('destination')} from "
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
            response = self.mock_response(preferences)
        else:
            response = requests.post(self.api_url, json=payload, headers=headers)

            if response.status_code == 200:
                response = response.json()
                print(f"Full API response: {response}")  # Debugging

                if 'choices' in response:
                    return self.parse_response(response['choices'])
                else:
                    raise KeyError("'choices' key not found in API response")
            else:
                raise Exception(f"API call failed: {response.status_code} - {response.text}")

    def parse_response(self, choices):
        itineraries = []

        for choice in choices:
            content = choice['message']['content']  # Large block of text
            sections = re.split(r'### Itinerary Option', content)  # Split by itinerary options

            for section in sections:
                if section.strip():  # Skip empty sections
                    # Extract itinerary option number
                    option_match = re.search(r'Option (\d+)', section)
                    option = f"Itinerary Option {option_match.group(1)}" if option_match else "Unknown Option"
                    
                    # Extract destination (if possible)
                    destination_match = re.search(r"for ([A-Za-z\s]+)", section)
                    destination = destination_match.group(1).strip() if destination_match else "Unknown Destination"
                    
                    # Extract itinerary details by 'Day' delimiters
                    itinerary = []
                    day_matches = re.findall(r'(Day \d+):\s*(.*?)(?=Day \d+|$)', section, re.DOTALL)
                    for day, activities in day_matches:
                        itinerary.append({
                            'day': day,
                            'activities': [activity.strip() for activity in activities.split('\n') if activity.strip()]
                        })

                    # Only add if itinerary is valid
                    if itinerary:
                        itineraries.append({
                            'option': option,
                            'destination': destination,
                            'itinerary': itinerary
                        })

        return itineraries if itineraries else None

    def mock_response(self, preferences):
        """Mock function to simulate a successful API call returning three itinerary options."""
        mock_data = [
            {
                'destination': preferences.get('destination', 'Unknown Destination'),
                'start_date': preferences.get('start_date', 'Unknown Start Date'),
                'end_date': preferences.get('end_date', 'Unknown End Date'),
                'itinerary': [
                    {'day': 1, 'activities': ['Visit museum', 'Walk around old town', 'Dinner at local restaurant']},
                    {'day': 2, 'activities': ['Hiking', 'Explore the park', 'Visit a gallery']}
                ],
                'budget': preferences.get('budget', 'Unknown Budget'),
                'interests': preferences.get('interests', 'Unknown Interests'),
                'option': 'Itinerary Option 1'
            },
            {
                'destination': preferences.get('destination', 'Unknown Destination'),
                'start_date': preferences.get('start_date', 'Unknown Start Date'),
                'end_date': preferences.get('end_date', 'Unknown End Date'),
                'itinerary': [
                    {'day': 1, 'activities': ['City tour', 'Lunch at cafe', 'Visit local market']},
                    {'day': 2, 'activities': ['Beach day', 'Boat tour']}
                ],
                'budget': preferences.get('budget', 'Unknown Budget'),
                'interests': preferences.get('interests', 'Unknown Interests'),
                'option': 'Itinerary Option 2'
            },
            {
                'destination': preferences.get('destination', 'Unknown Destination'),
                'start_date': preferences.get('start_date', 'Unknown Start Date'),
                'end_date': preferences.get('end_date', 'Unknown End Date'),
                'itinerary': [
                    {'day': 1, 'activities': ['Museum tour', 'Lunch at a riverside restaurant']},
                    {'day': 2, 'activities': ['Hiking in nearby hills', 'Dinner at a fancy restaurant']}
                ],
                'budget': preferences.get('budget', 'Unknown Budget'),
                'interests': preferences.get('interests', 'Unknown Interests'),
                'option': 'Itinerary Option 3'
            }
        ]
        return mock_data

# Example usage
def generate_itinerary_from_profile(destination, start_date, end_date, interests, travel_type, budget,
                                    api_key="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", use_mock=False):
    handler = PerplexityLLMHandler(api_key=api_key, use_mock=use_mock)

    preferences = {
        'destination': destination,
        'start_date': str(start_date),
        'end_date': str(end_date),
        'interests': interests.split(','),  # Split interests into a list
        'travel_type': travel_type,
        'budget': budget
    }

    itineraries = handler.get_itinerary(preferences)
    return itineraries
