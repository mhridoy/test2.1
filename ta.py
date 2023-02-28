# import streamlit as st
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from datetime import datetime, timedelta
# from tabulate import tabulate


# Define Streamlit app
st.set_page_config(page_title="FMC Teacher Attendance System", page_icon=":clipboard:")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# # Define Google Sheets credentials
# SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# SERVICE_ACCOUNT_FILE = 'service_account_file02.json'

# # Define Google Forms and Sheets IDs
# FORM_ID = '1FAIpQLScO_Dfe0t_f2O2opEsAkSMLvjvSbaLMMhtvL8wEf_1ZTsBUsA'
# SHEET_ID = '1ERX4yJmT-w26imY2tbB3CnKGVjCvBTYT2hLAx-4dUBc'

# # Connect to Google Sheets API
# creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
# client = gspread.authorize(creds)
# sheet = client.open_by_key(SHEET_ID).sheet1

# # Define Streamlit app
# st.set_page_config(page_title="Teacher Attendance System", page_icon=":clipboard:")
# st.title('Teacher Attendance System')
# st.markdown('Please enter your information below:')

# # Get the list of teacher names from the Google Sheet
# teacher_names = sheet.col_values(1)[1:]

# # Create a form to input teacher information
# with st.form(key='teacher_info_form'):
#     teacher_name = st.text_input(label='Name')
#     today = datetime.now().strftime('%Y-%m-%d')
#     num_classes = st.number_input(label='Number of Classes Taught', min_value=0, value=0)
#     submit_button = st.form_submit_button(label='Submit')

# # Check if the form was submitted
# if submit_button:
#     # Add the attendance record to the Google Sheet
#     sheet.append_row([teacher_name, today, num_classes, '', '', ''])
#     st.success('Teacher information submitted!')

# # Display the teacher information records in a table
# st.markdown('## Teacher Information Records')
# rows = sheet.get_all_values()
# if len(rows) == 1:
#     st.warning('No teacher information records yet.')
# else:
#     header = rows[0]
#     data = rows[1:]
#     st.write(tabulate(data, headers=header, tablefmt='pipe'))

#     # Count the number of classes taught by each teacher
#     class_counts = {}
#     for row in data:
#         teacher = row[0]
#         num_classes = int(row[2])
#         if teacher in class_counts:
#             class_counts[teacher] += num_classes
#         else:
#             class_counts[teacher] = num_classes

#     # Display the class counts in a separate table
#     st.markdown('## Number of Classes Taught by Each Teacher')
#     headers = ['Teacher Name', 'Number of Classes']
#     data = [[teacher, class_counts[teacher]] for teacher in class_counts]
#     st.write(tabulate(data, headers=headers, tablefmt='pipe'))
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from tabulate import tabulate

# Define Google Sheets credentials
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account_file02.json'

# Define Google Forms and Sheets IDs
FORM_ID = '1FAIpQLScO_Dfe0t_f2O2opEsAkSMLvjvSbaLMMhtvL8wEf_1ZTsBUsA'
SHEET_ID = '1ERX4yJmT-w26imY2tbB3CnKGVjCvBTYT2hLAx-4dUBc'

# Connect to Google Sheets API
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# Define Streamlit app

st.title('Feni Model Teacher Attendance System')
st.markdown('Please enter your information below:')

# Get the list of teacher names from the Google Sheet
teacher_names = sheet.col_values(1)[1:]


# Create a form to input teacher information
with st.form(key='teacher_info_form'):
    teacher_name = st.text_input(label='Name')
    today = datetime.now().strftime('%Y-%m-%d')
    num_classes = st.number_input(label='Number of Classes Taught', min_value=0, value=0)
    submit_button = st.form_submit_button(label='Submit')



# Check if the form was submitted
if submit_button:
    # Add the attendance record to the Google Sheet
    sheet.append_row([teacher_name, today, num_classes, '', '', ''])
    st.success('Teacher information submitted!')


# Display the teacher information records in a table
with st.expander('Teacher Attandance Records Approved or Declined by Admin'):

    #st.markdown('## Teacher Attandance Records')
    rows = sheet.get_all_values()
    if len(rows) == 1:
        st.warning('No teacher information records yet.')
    else:
        header = rows[0]
        data = rows[1:]
        st.write(tabulate(data, headers=header, tablefmt='pipe'))

# Create a date range selector
st.header('Generate montly report:')
with st.form(key='date_range_selector'):
    start_date = st.date_input('Start date')
    end_date = st.date_input('End date')
    submit_button = st.form_submit_button(label='Select')

# Check if the form was submitted
if submit_button:
    # Count the number of classes taught by each teacher within the selected date range
    class_counts = {}
    rows = sheet.get_all_values()[1:]
    for row in rows:
        teacher_name = row[0]
        row_date = datetime.strptime(row[1], '%Y-%m-%d')
        if row_date.date() >= start_date and row_date.date() <= end_date:
            approval = row[3]
            if approval == 'Yes':
                if teacher_name in class_counts:
                    class_counts[teacher_name] += 1
                else:
                    class_counts[teacher_name] = 1

    # Display the class counts in a table
    st.markdown(f'## Classes Taught ({start_date} - {end_date})')
    if not class_counts:
        st.warning('No classes taught within the selected date range.')
    else:
        table_data = []
        for teacher_name, count in class_counts.items():
            table_data.append([teacher_name, count])
        st.write(tabulate(table_data, headers=['Teacher Name', 'Number of Classes Taught'], tablefmt='pipe'))
