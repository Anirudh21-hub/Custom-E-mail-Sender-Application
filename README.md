
Overview
This application enables users to send customized emails via an intuitive Streamlit-based dashboard. It integrates with email services, supports scheduling and tracking, and provides real-time analytics using Python.

Features

Data Integration

Upload data from Google Sheets or CSV files.
Auto-detect columns for dynamic placeholders.
Email Integration

Connect email accounts via OAuth2 (e.g., Gmail, Outlook).
SMTP/ESP (SendGrid, Amazon SES, Mailgun) integration.
Customizable Content

Accept customizable email prompts with placeholders.
Scheduling and Throttling

Schedule email batches.
Throttle email sending to comply with limits.
Real-Time Analytics

View sent, pending, and failed emails.
Track delivery status: Delivered, Opened, Bounced.
Setup and Installation
Prerequisites
Python 3.8+
API keys for the selected ESP (SendGrid, Amazon SES, Mailgun).
SMTP account credentials for custom email services.


Usage

Upload Data
Launch the Streamlit dashboard.
Upload a CSV or connect a Google Sheet via its URL.
Customize Email Content
Enter a prompt with placeholders (e.g., {Name}, {Location}).
Placeholders are automatically mapped to CSV/Sheet columns.
Schedule Emails
Set a specific time or batch interval for emails.
Configure throttling limits (e.g., X emails per hour).
Track Progress
Monitor the email dashboard for real-time updates on:
Total Sent
Pending
Failed
Opened/Delivered/Bounced statuses.


Project Structure

custom-email-sender/
├── app.py                # Main Streamlit application
├── email_service.py      # Email sending logic (SMTP/ESP integration)
├── utils.py              # Utility functions for data processing
├── templates/            # Email templates
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation


Technology Stack

Frontend: Streamlit
Backend: Python
Email Services: SMTP, SendGrid, Mailgun, Amazon SES
Database: SQLite for storing analytics and scheduling data
LLM API: OpenAI/Groq API for content generation
Key Features Implementation
Frontend: Streamlit
File Upload: Use st.file_uploader to upload CSV.
Input Prompt: Text area for email templates with placeholders.
Progress Tracking: Display analytics using st.metric and st.progress.
Backend: Python
Email Sending: Use smtplib for SMTP or API clients for ESPs.
Scheduling: Use schedule or APScheduler.
Data Processing: Use pandas for CSV/Google Sheet pars