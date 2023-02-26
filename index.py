import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate


# Define Streamlit app
st.set_page_config(page_title='Python Programming Q&A', page_icon=':pencil2:')
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Define Google Sheets credentials
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account_file.json'

# Define Google Forms and Sheets IDs
FORM_ID = '1FAIpQLSeL7WofQO_Me3jzkXJbpxOul6lu_l4V0pd3muJvLcpNAg5sFw'
SHEET_ID = '1jM0rNZ51-MjWaiDxt6LUvEJpMbHSguAy6undyWjLV9E'

# Connect to Google Sheets API
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# Define Streamlit app
st.title('Python Programming Q&A')
st.markdown('Use this form to submit your questions:')
with st.form(key='question_form'):
    question = st.text_input(label='Questions')
    submit_button = st.form_submit_button(label='Submit')

# Check if the form was submitted
if submit_button:
    # Add the question to the Google Sheet
    sheet.append_row([question])
    st.success('Question submitted!')

# Display the questions and answers in a table
st.markdown('## Questions and Answers')
rows = sheet.get_all_values()
if len(rows) == 1:
    st.warning('No questions submitted yet.')
else:
    headers = rows[0]
    data = rows[1:]
    table = tabulate(data, headers=headers, tablefmt="pipe")
    st.markdown(table)
