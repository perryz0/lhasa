import unittest
from pplx_llm_handler import PerplexityLLMHandler, generate_itinerary_from_profile

class TestPerplexityLLMHandler(unittest.TestCase):

    def setUp(self):
        # Set your API key here (use your actual key for real tests)
        self.api_key = "pplx-your-api-key-here"
        
        # Initialize the Perplexity handler with the API key (use_mock=True for testing)
        self.handler = PerplexityLLMHandler(api_key=self.api_key, use_mock=True)
        
        # Example travel preferences
        self.preferences = {
            'destination': 'Paris',
            'start_date': '2024-10-15',
            'end_date': '2024-10-25',
            'interests': ['hiking', 'art'],
            'travel_type': 'Leisure',
            'budget': 1500
        }

    def test_mock_response(self):
        # Test the mock response to make sure the mock function returns expected results
        mock_itinerary = self.handler.get_itinerary(self.preferences)
        self.assertEqual(mock_itinerary['destination'], 'Paris')
        self.assertIn('itinerary', mock_itinerary)

    def test_real_api_response(self):
        # Test the real API response (for this, set use_mock=False and ensure API key is correct)
        self.handler.use_mock = False
        real_itinerary = self.handler.get_itinerary(self.preferences)

        # Since the output from the real API can vary, just check for required fields
        self.assertIn('destination', real_itinerary)
        self.assertIn('itinerary', real_itinerary)

    def test_generate_itinerary_from_profile_mock(self):
        # Test using the generate_itinerary_from_profile with mock
        itinerary = generate_itinerary_from_profile(
            api_key=self.api_key,
            destination="Paris",
            start_date="2024-10-15",
            end_date="2024-10-25",
            interests="hiking,art",
            travel_type="Leisure",
            budget=1500,
            use_mock=True
        )
        self.assertEqual(itinerary['destination'], 'Paris')
        self.assertIn('itinerary', itinerary)

    def test_generate_itinerary_from_profile_real(self):
        # Test using the generate_itinerary_from_profile with the real API
        itinerary = generate_itinerary_from_profile(
            api_key=self.api_key,
            destination="Paris",
            start_date="2024-10-15",
            end_date="2024-10-25",
            interests="hiking,art",
            travel_type="Leisure",
            budget=1500,
            use_mock=False
        )
        self.assertIn('destination', itinerary)
        self.assertIn('itinerary', itinerary)

if __name__ == '__main__':
    unittest.main()
