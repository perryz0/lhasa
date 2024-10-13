import unittest
from pplx_llm_handler import PerplexityLLMHandler, generate_itinerary_from_profile

class TestPerplexityLLMHandler(unittest.TestCase):

    def setUp(self):
        # Set actual API key here
        self.api_key = "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"
        
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
        mock_itineraries = self.handler.get_itinerary(self.preferences)
        self.assertEqual(len(mock_itineraries), 3)  # Check that three itinerary options are returned
        self.assertEqual(mock_itineraries[0]['destination'], 'Paris')
        self.assertIn('itinerary', mock_itineraries[0])

    def test_real_api_response(self):
        # Test the real API response (for this, set use_mock=False and ensure API key is correct)
        self.handler.use_mock = False
        real_itineraries = self.handler.get_itinerary(self.preferences)

        # Since the output from the real API can vary, just check for required fields
        self.assertEqual(len(real_itineraries), 3)
        self.assertIn('destination', real_itineraries[0])
        self.assertIn('itinerary', real_itineraries[0])

    def test_generate_itinerary_from_profile_mock(self):
        # Test using the generate_itinerary_from_profile with mock
        itineraries = generate_itinerary_from_profile(
            api_key=self.api_key,
            destination="Paris",
            start_date="2024-10-15",
            end_date="2024-10-25",
            interests="hiking,art",
            travel_type="Leisure",
            budget=1500,
            use_mock=True
        )
        self.assertEqual(len(itineraries), 3)
        self.assertEqual(itineraries[0]['destination'], 'Paris')
        self.assertIn('itinerary', itineraries[0])

    def test_generate_itinerary_from_profile_real(self):
        # Test using the generate_itinerary_from_profile with the real API
        itineraries = generate_itinerary_from_profile(
            api_key=self.api_key,
            destination="Paris",
            start_date="2024-10-15",
            end_date="2024-10-25",
            interests="hiking,art",
            travel_type="Leisure",
            budget=1500,
            use_mock=False
        )
        self.assertEqual(len(itineraries), 3)
        self.assertIn('destination', itineraries[0])
        self.assertIn('itinerary', itineraries[0])

if __name__ == '__main__':
    unittest.main()
