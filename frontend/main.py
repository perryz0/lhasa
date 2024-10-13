import streamlit as st
import requests
import sys
import os
import pymongo  # MongoDB

# Add the 'backend' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

# Import the handler
from pplx_llm_handler import generate_itinerary_from_profile
import Itineraries as it
import json

# MongoDB connection setup
client = pymongo.MongoClient("mongodb+srv://perryz0:peiru123@cluster0.402ih.mongodb.net/?retryWrites=true&w=majority")
db = client["lhasa_travel_db"]
collection = db["itineraries"]

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

if 'selected_itinerary' not in st.session_state:
    st.session_state['selected_itinerary'] = None

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

# Step 3: When an itinerary is shared, show a success message
def store_itinerary(itinerary_data):
    try:
        result = collection.insert_one(itinerary_data)
        st.session_state['selected_itinerary'] = itinerary_data  # Save to session state
        st.success(f"Your selected itinerary has been successfully shared! Document ID: {result.inserted_id}")
    except Exception as e:
        st.error(f"Failed to store itinerary: {e}")

# Helper function to render and handle example itineraries
def render_example_itineraries(example_itineraries):
    col1, col2, col3 = st.columns(3)

    for col, itinerary in zip([col1, col2, col3], example_itineraries):
        with col:
            st.subheader(f"{itinerary['destination']}")
            st.write(f"**Dates**: {itinerary['dates']}")
            st.write(f"**Budget**: ${itinerary['budget']}")
            st.write(f"**Type**: {itinerary['travel_type']}")
            st.write("**Activities**:")
            for activity in itinerary['activities']:
                st.write(f"- {activity}")
            if st.button(f"Choose {itinerary['destination']} Itinerary"):
                st.session_state['selected_itinerary'] = itinerary
                store_itinerary(itinerary)
                st.success(f"Selected itinerary for {itinerary['destination']} has been shared successfully!")
                st.experimental_rerun()  # Rerun to hide options after selection

# Select between modes of itinerary planning
st.subheader("How would you like to start?")
mode = st.radio("", ['Start from scratch', 'Upload preferences file', 'Community Itineraries'])

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

                # Main logic for itinerary selection
                if itinerary:
                    st.success('Your itinerary has been generated successfully!')
                    html_data = dict_to_html(itinerary)
                    st.markdown(html_data, unsafe_allow_html=True)

                    if st.session_state['selected_itinerary'] is None:
                        st.markdown("### Example Itineraries You May Like")
                        example_itineraries = [
                            {'username': 'dubai_explorer', 'destination': 'Dubai, UAE', 'dates': '2024-05-10 to 2024-05-15', 'budget': 2500,
                            'travel_type': 'Adventure', 'activities': ['Visit Burj Khalifa', 'Desert Safari', 'Dhow Cruise']},
                            {'username': 'parisian_lover', 'destination': 'Paris, France', 'dates': '2024-06-01 to 2024-06-07', 'budget': 4000,
                            'travel_type': 'Romantic', 'activities': ['Visit Eiffel Tower', 'Louvre Museum', 'Seine River Cruise']},
                            {'username': 'tokyo_adventurer', 'destination': 'Tokyo, Japan', 'dates': '2024-07-15 to 2024-07-22', 'budget': 3000,
                            'travel_type': 'Cultural', 'activities': ['Visit Shibuya Crossing', 'Explore Meiji Shrine', 'Mount Fuji Day Trip']}
                        ]
                        render_example_itineraries(example_itineraries)
                    else:
                        st.success(f"Selected itinerary for {st.session_state['selected_itinerary']['destination']} has been shared successfully!")

            except Exception as e:
                st.error(f"Error generating itinerary: {e}")

# Explore shared itineraries (community feed)
elif mode == 'Upload preferences file':
    st.subheader("Upload a preferences file for faster itinerary generation")

    # Upload preferences JSON file
    uploaded_file = st.file_uploader("Upload your preferences (JSON format)...", type=["json"], key='preferences_file_uploader')

    if st.button('Generate Itinerary from Preferences'):
        if uploaded_file is not None:
            with st.spinner('Generating itinerary from preferences...'):
                files = {'file': uploaded_file.getvalue()}
                response = requests.post('http://127.0.0.1:5000/submit_preferences', files=files)
                if response.status_code == 200:
                    generated_itinerary = response.json()
                    st.success('Itinerary generated successfully!')
                    markdown_data = dict_to_markdown(generated_itinerary)
                    html_data = dict_to_html(generated_itinerary)
                    st.markdown(html_data, unsafe_allow_html=True)
                else:
                    st.error('Error generating itinerary from preferences.')
        else:
            st.warning('Please upload a valid preferences file.')

elif mode == 'Community Itineraries':
    st.subheader("Explore Community Itineraries")

    # Add filters and search functionality for the community feed
    destination_filter = st.text_input("Search by Destination")
    travel_type_filter = st.selectbox("Filter by Travel Type", options=["All", "Cultural", "Adventure", "Luxury", "Romantic", "Business"])

    # Filter the community itineraries based on user input
    filtered_itineraries = [
        itinerary for itinerary in it.community_itineraries
        if (destination_filter.lower() in itinerary['destination'].lower()) and
        (travel_type_filter == "All" or itinerary['travel_type'] == travel_type_filter)
    ]

    # Display the filtered itineraries
    top = min(len(filtered_itineraries), 5)
    st.write(f"Showing {top} out of {len(filtered_itineraries)} itineraries:")
    i = 0
    for itinerary in filtered_itineraries:
        if (i < top):
            with st.expander(f"🌍 {itinerary['destination']} ({itinerary['dates']}) by {itinerary['username']}"):
                st.write(f"**Travel Type**: {itinerary['travel_type']}")
                st.write(f"**Budget**: ${itinerary['budget']}")
                st.write("**Activities**:")
                for activity in itinerary['activities']:
                    st.write(f"- {activity}")
            i += 1

# Simple dashboard for saved itineraries
st.divider()
st.write("## My Itineraries")

# Section for Saved Itineraries
st.write("### Saved Itineraries")
if it.saved_itineraries:
    i = ""
    for idx, itinerary in enumerate(it.saved_itineraries):
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
if it.followed_itineraries:
    for idx, itinerary in enumerate(it.followed_itineraries):
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
