import streamlit as st
import requests
import json

# Helper function to format itinerary data in markdown
def dict_to_markdown(d, level=0):
    # Same function for markdown rendering
    ...

def dict_to_html(d, level=0):
    # Same function for HTML rendering
    ...

# Set page configuration
st.set_page_config(
    page_title="Lhasa Itinerary Planner",
    page_icon="🗺️",
    layout="centered",
    initial_sidebar_state="auto",
)

# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

# Title of the app
st.title(":mountain: :green[**Lhasa**] AI-Powered Travel Itinerary Planner")

st.markdown("""
**Plan your perfect trip** with Lhasa's AI-driven itinerary generator. Whether you're planning a weekend getaway or a multi-country adventure, Lhasa helps you create a customized and memorable travel experience.
""")

# Select between modes of itinerary planning
st.subheader("How would you like to start?")
mode = st.radio("", ['Start from scratch', 'Upload preferences file'])

if mode == 'Start from scratch':
    st.subheader("Enter Your Travel Information")

    # New section for user profile creation (added profile completion indicator)
    with st.form(key='user_profile_form', clear_on_submit=False):
        st.info("Fill out your travel preferences to generate an itinerary.")
        
        destination = st.text_input("Destination", help="Enter your destination")
        start_date = st.date_input("Start Date", help="Select your trip start date")
        end_date = st.date_input("End Date", min_value=start_date, help="Select your trip end date")
        interests = st.text_area("Interests", help="List your interests (e.g., hiking, museums)")
        travel_type = st.selectbox("Travel Type", ["Leisure", "Adventure", "Cultural", "Romantic", "Business"])
        budget = st.slider("Budget (USD)", min_value=100, max_value=10000, value=1500, step=100)
        
        # Opt-in checkbox for sharing itinerary
        share_itinerary = st.checkbox("Share my itinerary with the community")
        
        # Submit button for itinerary generation
        submit_profile_button = st.form_submit_button(label='Submit Profile & Generate Itinerary')

    # If the form is submitted, generate the itinerary
    if submit_profile_button:
        travel_data = {
            'destination': destination,
            'start_date': str(start_date),
            'end_date': str(end_date),
            'interests': interests,
            'travel_type': travel_type,
            'budget': budget,
            'share_itinerary': share_itinerary
        }
        
        # Display spinner while processing
        with st.spinner('Generating your personalized itinerary...'):
            response = requests.post('http://127.0.0.1:5000/submit_itinerary', data=travel_data)
            if response.status_code == 200:
                st.success('Your itinerary has been generated successfully!')
                itinerary = response.json()
                html_data = dict_to_html(itinerary)
                st.markdown(html_data, unsafe_allow_html=True)
                
                # Option to save itinerary to the community feed
                if share_itinerary:
                    st.success("Your itinerary has been shared with the community!")
            else:
                st.error('Error generating the itinerary.')

# Explore shared itineraries (community feed)
elif mode == 'Upload preferences file':
    st.subheader("Explore Community Itineraries")

    # Search bar for destinations or activities
    search_query = st.text_input("Search for itineraries by destination or activity:")
    
    # Example of filter options for the community feed
    filters = st.multiselect(
        "Filter by Travel Type", ["Leisure", "Adventure", "Cultural", "Romantic", "Business"]
    )

    if st.button('Search'):
        # Dummy search action (could be replaced with real search logic)
        st.success(f"Showing itineraries matching '{search_query}' with filters {filters}")
        # Example rendering of community itineraries
        for i in range(3):  # Assume 3 itineraries are returned
            st.markdown(f"**Itinerary {i + 1}:** Destination Example")
            st.markdown("Activities: Museum, Hiking")
            st.markdown("Budget: $1500")
            st.button(f"Follow Itinerary {i + 1}")

# Simple dashboard for saved itineraries
st.subheader("My Itineraries")
st.write("List of saved and followed itineraries")

# Future feature: Notifications section for when users interact with your itinerary
if 'notifications' not in st.session_state:
    st.session_state['notifications'] = []

notifications = st.session_state['notifications']
if notifications:
    st.markdown("**Notifications**:")
    for notification in notifications:
        st.write(notification)
else:
    st.write("No new notifications.")
