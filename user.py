import streamlit as st
import pandas as pd
import requests

# Backend API endpoints
UPLOAD_API = "http://localhost:5000/upload"
STATUS_API = "http://localhost:5000/status"
SCHEDULE_API = "http://localhost:5000/schedule"

# Page layout
st.title("Email Sender Dashboard")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Menu", ["Upload CSV", "View Email Status", "Schedule Emails"]
)

# Upload CSV Section
if menu == "Upload CSV":
    st.header("Upload CSV File")
    uploaded_file = st.file_uploader("Book1.csv", type="csv")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of the uploaded file:")
            st.dataframe(df)

            # Upload to backend
            if st.button("Upload to Server"):
                files = {"file": uploaded_file.getvalue()}
                response = requests.post(UPLOAD_API, files=files)
                if response.status_code == 200:
                    st.success("File uploaded successfully!")
                else:
                    st.error("Failed to upload the file. Please try again.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# View Email Status Section
elif menu == "View Email Status":
    st.header("Email Status")
    response = requests.get(STATUS_API)

    if response.status_code == 200:
        email_status = response.json()
        df_status = pd.DataFrame(email_status)
        st.dataframe(df_status)
    else:
        st.error("Failed to fetch email status. Please check the server.")

# Schedule Emails Section
elif menu == "Schedule Emails":
    st.header("Schedule Emails")

    # Input time for scheduling
    schedule_time = st.time_input("Select Time to Schedule Emails")
    if st.button("Schedule"):
        data = {"time": str(schedule_time)}
        response = requests.post(SCHEDULE_API, json=data)
        if response.status_code == 200:
            st.success("Emails scheduled successfully!")
        else:
            st.error("Failed to schedule emails. Please try again.")
