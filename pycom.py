import streamlit as st
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from flask import request
import os

# Define Streamlit app
st.set_page_config(page_title='Python Assignment Submission', page_icon=':pencil2:')
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Define Google Sheets credentials
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account_file02.json'

SHEET_ID = '1dmXjXLxbeGNAJB-7AFHvoEFZzgDbIlaypmFe4b1g574'

# Connect to Google Sheets API
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# Get existing data from Google Sheet
# data = sheet.get_all_records()

# # Display data in tabulation format
# if data:
#     df = pd.DataFrame(data)
#     st.write(df)

st.title('Assignment Submission |  Made With Love 💌 💌 🤟')

# Get student name and marks
name = st.text_input('Enter your name:')
code = st.text_area('Enter your code here:')
input_data = st.text_input('Enter input data (optional):')
marks = "Not Evaluated"
opinion = "Not Checked"

# Get client IP address

ip_address = os.environ.get('HTTP_X_FORWARDED_FOR', '')

if st.button('Submit your Assignment'):
    # Check if the IP address has already submitted an assignment
    st.write(ip_address)
    existing_data = sheet.get_all_records()
    existing_ips = [row['IP Address'] for row in existing_data]
    if ip_address in existing_ips:
        st.error('You have already submitted an assignment.')
    else:
        # Set up API credentials
        CLIENT_ID = '3b35002899d368ba013f18d76b1b838a'
        CLIENT_SECRET = '7ac2b8e3fe5d92d04aa75db9a678158df17d0d8cbc01c7862de4d5340d0a2540'

        # Set up API request data
        data = {
            'clientId': CLIENT_ID,
            'clientSecret': CLIENT_SECRET,
            'script': code,
            'stdin': input_data,
            'language': 'python3',
            'versionIndex': 3
        }

        # Send code and input data to JDoodle API for execution
        response = requests.post('https://api.jdoodle.com/v1/execute', json=data)
        result = response.json()

        # Display result
        output = result['output']
        #st.write(output)
        st.balloons()

        # Add data to Google Sheet
        if output:
            row = [name, code, input_data, output.strip(), marks, opinion, ip_address]
            sheet.append_row(row)

with st.expander('View Assignment Submission History with Results'):
    existing_data = sheet.get_all_records()

            # Display updated data in tabulation format
    if existing_data:
                df = pd.DataFrame(existing_data)
                st.write(df)
            # Refresh data
            # existing_data = sheet.get_all_records()

            # # Display updated data in tabulation format
            # if existing_data:
            #     df = pd.DataFrame(existing_data)
            #     st.write(df)


# import streamlit as st
# import requests


# # Define Streamlit app
# st.set_page_config(page_title='Python Programming Q&A', page_icon=':pencil2:')
# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         </style>
#         """
# st.markdown(hide_menu_style, unsafe_allow_html=True)

# st.title('Python Compiler Made With Love 💌 💌 🤟')

# code = st.text_area('Enter your code here:')
# input_data = st.text_input('Enter input data (optional):')

# if st.button('Run'):
#     # Set up API credentials
#     CLIENT_ID = '3b35002899d368ba013f18d76b1b838a'
#     CLIENT_SECRET = '7ac2b8e3fe5d92d04aa75db9a678158df17d0d8cbc01c7862de4d5340d0a2540'
    
#     # Set up API request data
#     data = {
#         'clientId': CLIENT_ID,
#         'clientSecret': CLIENT_SECRET,
#         'script': code,
#         'stdin': input_data,
#         'language': 'python3',
#         'versionIndex': 3
#     }
    
#     # Send code and input data to JDoodle API for execution
#     response = requests.post('https://api.jdoodle.com/v1/execute', json=data)
#     result = response.json()

#     # Display result
#     st.write(result['output'])