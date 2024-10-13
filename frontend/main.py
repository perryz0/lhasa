import streamlit as st
import requests
import json

# Helper function to format itinerary data in markdown
def dict_to_markdown(d, level=0):
    md_content = ""
    indent = "  " * level
    for key, value in d.items():
        if isinstance(value, dict):
            md_content += f"{indent}- **{key}**:\n"
            md_content += dict_to_markdown(value, level + 1)
        elif isinstance(value, list):
            md_content += f"{indent}- **{key}**:\n"
            for item in value:
                md_content += f"{indent}  - {item}\n"
        else:
            md_content += f"{indent}- **{key}**:\n {value}\n"
    return md_content

# Helper function to format itinerary data in HTML
def dict_to_html(d, level=0):
    html_content = ""
    indent = "  " * level * 2  # Increase indentation for nested levels
    header_size = min(level+3, 6)  # Decrease header size as depth increases (from h3 to h6)
    margin = f"margin-left: {level * 30}px;" 
    for key, value in d.items():
        if isinstance(value, dict):
            html_content += f"<h{header_size} style='color:#FFA500; {margin}'>{indent}{key}</h{header_size}>\n"
            html_content += dict_to_html(value, level + 1)
        else:
            html_content += f"<h{header_size} style='color:#FFA500; {margin}'>{indent}{key}</h{header_size}>\n"
            html_content += f"<p style = '{margin}'>{indent}{value}<br><br></p>"
    return html_content

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

    # Image uploader
    uploaded_file = st.file_uploader("Upload a reference image (optional, e.g., destination photo)...", type=["jpg", "jpeg", "png"], key='itinerary_image_uploader')

    # Manage uploaded_file in session state
    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file
        # Display uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    else:
        uploaded_file = st.session_state.get('uploaded_file', None)
        if uploaded_file is not None:
            # Display uploaded image from session state
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

    # Auto-fill button (optional for future AI analysis from image)
    # In this version, this feature could be expanded to recommend destinations based on the image
    if st.button('Generate Itinerary'):
        if uploaded_file is not None:
            with st.spinner('Analyzing image and generating itinerary...'):
                files = {'image': uploaded_file.getvalue()}
                response = requests.post('http://127.0.0.1:5000/generate', files=files)
                if response.status_code == 200:
                    generated_itinerary = response.json()
                    st.success('Itinerary generated successfully!')
                    markdown_data = dict_to_markdown(generated_itinerary)
                    html_data = dict_to_html(generated_itinerary)
                    st.markdown(html_data, unsafe_allow_html=True)
                else:
                    st.error('Error generating itinerary.')
        else:
            st.warning('You can generate an itinerary based on your input below.')

    # Form to fill out travel details
    with st.form(key='itinerary_form', clear_on_submit=False):
        st.info("Fill out the form below with your travel details and preferences.")

        destination = st.text_input(
            "Destination",
            help="Enter the name of your destination (e.g., 'Paris, France')"
        )

        start_date = st.date_input(
            "Start Date",
            help="Select the start date of your trip."
        )

        end_date = st.date_input(
            "End Date",
            help="Select the end date of your trip."
        )

        interests = st.text_area(
            "Your Interests",
            help="List your interests or preferred activities (e.g., 'museums, beaches, hiking')."
        )

        travel_type = st.selectbox(
            "Travel Type",
            options=["Leisure", "Adventure", "Cultural", "Romantic", "Business"]
        )

        budget = st.slider(
            "Budget (USD)",
            min_value=100, max_value=10000, value=1500, step=100
        )

        submit_button = st.form_submit_button(label='Submit for Itinerary Generation')

    if submit_button:
        # Collect form data
        travel_data = {
            'destination': destination,
            'start_date': str(start_date),
            'end_date': str(end_date),
            'interests': interests,
            'travel_type': travel_type,
            'budget': budget
        }

        with st.spinner('Generating your personalized itinerary...'):
            response = requests.post('http://127.0.0.1:5000/submit_itinerary', data=travel_data)
            if response.status_code == 200:
                st.success('Your itinerary has been generated successfully!')
                itinerary = response.json()
                html_data = dict_to_html(itinerary)
                st.markdown(html_data, unsafe_allow_html=True)
            else:
                st.error('Error generating the itinerary.')

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
