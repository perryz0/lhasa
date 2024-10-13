import streamlit as st
import requests
from backend.pplx_llm_handler import generate_itinerary_from_profile
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
    page_title="Lhasa",
    page_icon="🗺️",
    layout="centered",
    initial_sidebar_state="auto",
)

# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

# Sidebar for login/logout
with st.sidebar:
    st.title("User Login")

    # Initialize session state for login status
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    # Check login status
    if st.session_state['logged_in']:
        st.success(f"Logged in as {st.session_state['username']}")
        
        # Profile actions (can be extended with real functionality)
        st.button("Update Profile")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.rerun()  # Force rerun to immediately reflect the logged-out state
    else:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if username == "admin" and password == "password":  # Replace with real authentication
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.sidebar.success("Login successful!")
                st.rerun()  # Force rerun to immediately reflect the logged-in state
            else:
                st.sidebar.error("Invalid credentials")
    

# Title of the app
st.title(":mountain: :green[**Lhasa**] Smart Travel Hub")

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
# st.subheader("My Itineraries")
# st.write("List of saved and followed itineraries")

# Simulating saved and followed itineraries
saved_itineraries = [
    {
        'destination': 'Paris, France',
        'start_date': '2022-11-01',
        'end_date': '2022-11-07',
        'travel_type': 'Cultural',
        'budget': 3000,
        'activities': ['Visit Louvre', 'Eiffel Tower Sightseeing', 'Seine River Cruise']
    },
    {
        'destination': 'Tokyo, Japan',
        'start_date': '2023-12-10',
        'end_date': '2023-12-15',
        'travel_type': 'Adventure',
        'budget': 2000,
        'activities': ['Mount Fuji Hike', 'Visit Shibuya Crossing', 'Sushi Omakase Tasting']
    }
]

followed_itineraries = [
    {
        'destination': 'New York, USA',
        'start_date': '2024-10-19',
        'end_date': '2024-3-23',
        'travel_type': 'Business',
        'budget': 1500,
        'activities': ['Attend Business Conference', 'Central Park Walk', 'Attend Broadway Show']
    }
]

st.write("## My Itineraries")

# Section for Saved Itineraries
st.write("### Saved Itineraries")
if saved_itineraries:
    i = ""
    for idx, itinerary in enumerate(saved_itineraries):
        i += " "
        with st.expander(f"🗺️ {itinerary['destination']} ({itinerary['start_date']} - {itinerary['end_date']})"):
            st.markdown(f"**Travel Type**: {itinerary['travel_type']}")
            st.markdown(f"**Budget**: ${itinerary['budget']}")
            st.markdown("**Activities**:")
            for activity in itinerary['activities']:
                st.write(f"- {activity}")
            # Buttons for itinerary actions
            if st.button(f"View Details", key="details"+i):
                st.info(f"Viewing details of {itinerary['destination']}")
                # You can add more detailed views like maps, itineraries per day, etc.
            if st.button(f"Edit Itinerary", key="edit"+i):
                st.info(f"Editing {itinerary['destination']}")
                # You could redirect to an editing form (not implemented in this example)
            if st.button(f"Delete Itinerary", key="delete"+i):
                st.warning(f"{itinerary['destination']} deleted!")
                # Logic to delete the itinerary from the database/session state would go here.
else:
    st.write("You have no saved itineraries yet.")

# Section for Followed Itineraries
st.write("### Followed Itineraries")
if followed_itineraries:
    for idx, itinerary in enumerate(followed_itineraries):
        with st.expander(f"📍 {itinerary['destination']} ({itinerary['start_date']} - {itinerary['end_date']})"):
            st.markdown(f"**Travel Type**: {itinerary['travel_type']}")
            st.markdown(f"**Budget**: ${itinerary['budget']}")
            st.markdown("**Activities**:")
            for activity in itinerary['activities']:
                st.write(f"- {activity}")
            # Option to unfollow an itinerary
            if st.button(f"Unfollow Itinerary"):
                st.warning(f"You unfollowed {itinerary['destination']}.")
                # Logic to unfollow (e.g., remove from session or database) goes here.
else:
    st.write("You are not following any itineraries yet.")


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


if submit_profile_button:
    travel_data = {
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date,
        'interests': interests,
        'travel_type': travel_type,
        'budget': budget
    }
    
    # Display spinner while processing
    with st.spinner('Generating your personalized itinerary...'):
        # Call the Perplexity LLM handler here
        try:
            itinerary = generate_itinerary_from_profile(
                api_key="pplx-e0a9601780b78e0825c85b74f452b79dd794f43a5239a8130",  # Your actual API key
                destination=travel_data['destination'],
                start_date=travel_data['start_date'],
                end_date=travel_data['end_date'],
                interests=travel_data['interests'],
                travel_type=travel_data['travel_type'],
                budget=travel_data['budget']
            )

            # Display the generated itinerary
            if itinerary:
                st.success('Your itinerary has been generated successfully!')
                html_data = dict_to_html(itinerary)
                st.markdown(html_data, unsafe_allow_html=True)

                # Option to save itinerary to the community feed
                if share_itinerary:
                    st.success("Your itinerary has been shared with the community!")
                    
            else:
                st.error("Itinerary generation failed. Please try again.")

        except Exception as e:
            st.error(f"Error generating itinerary: {e}")