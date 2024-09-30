import streamlit as st
import pandas as pd
import sqlite3
from db import get_events, approve_event, delete_event, edit_event, export_events, create_table

# Create the table when the app starts
create_table()

# Function to sort events by date (closest upcoming first)
def get_sorted_events():
    approved_events = get_events("Approved")
    df = pd.DataFrame(approved_events, columns=[
        "ID", "Quiz Name", "Date", "Time", "Category", "Place", "Location", "Organizer", 
        "Genre", "Quiz Master", "Prize", "Contact Number", "Status"
    ])
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.sort_values(by='Date')
    return df.drop(columns=["ID", "Status"])

st.title("Community Quiz Event System")

# Display upcoming quizzes
st.subheader("Upcoming Quizzes")
sorted_events = get_sorted_events()

# Add custom CSS for sleek capsule design
st.markdown("""
    <style>
    .event-capsule {
        background-color: #f0f8ff;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .event-date {
        font-size: 24px;
        font-weight: bold;
        color: #ff4500;
    }
    .event-name {
        font-size: 20px;
        font-weight: bold;
        color: #1e90ff;
    }
    .event-prize {
        font-size: 18px;
        font-weight: bold;
        color: #228b22;
    }
    .event-details {
        font-size: 14px;
        color: #555555;
    }
    </style>
""", unsafe_allow_html=True)

if not sorted_events.empty:
    for idx, event in sorted_events.iterrows():
        st.markdown(f"""
            <div class="event-capsule">
                <div class="event-date">{event['Date'].strftime('%d %b, %A')}</div>
                <div class="event-name">{event['Quiz Name']}</div>
                <div class="event-prize">Prize: {event['Prize']}</div>
                <div class="event-details">
                    Time: {event['Time']}<br>
                    Location: {event['Place']}, {event['Location']}<br>
                    Organizer: {event['Organizer']}<br>
                    Genre: {event['Genre']}<br>
                    Quiz Master: {event['Quiz Master']}<br>
                    Contact: {event['Contact Number']}
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.write("No approved events to display.")

# Admin Panel
st.sidebar.title("Admin Panel")

basic_password = st.sidebar.text_input("Enter Basic Admin Password", type="password")
full_password = st.sidebar.text_input("Enter Full Admin Password", type="password")

BASIC_ADMIN_PASSWORD = st.secrets.user.pass1
FULL_ADMIN_PASSWORD = st.secrets.user.pass2

# Basic Admin Panel (Approve/Decline Events)
if basic_password == BASIC_ADMIN_PASSWORD:
    st.subheader("Basic Admin: Approve/Decline Events")
    pending_events = get_events("Pending")
    
    if pending_events:
        df = pd.DataFrame(pending_events, columns=[
            "ID", "Quiz Name", "Date", "Time", "Category", "Place", "Location", "Organizer", 
            "Genre", "Quiz Master", "Prize", "Contact Number", "Status"
        ])
        st.dataframe(df.drop(columns=["Status"]))
        
        selected_event_id = st.selectbox("Select an Event to Approve", df["ID"])
        if st.button("Approve Event"):
            approve_event(selected_event_id)
            st.success(f"Event ID {selected_event_id} approved!")
    else:
        st.write("No pending events to approve.")
        
elif basic_password and basic_password != BASIC_ADMIN_PASSWORD:
    st.error("Incorrect Basic Admin Password.")

# Full Admin Panel (Edit, Delete, Export)
if full_password == FULL_ADMIN_PASSWORD:
    st.subheader("Full Admin Control Panel")
    
    # Edit Events
    st.write("Edit Events")
    approved_events = get_events("Approved")
    df = pd.DataFrame(approved_events, columns=[
        "ID", "Quiz Name", "Date", "Time", "Category", "Place", "Location", "Organizer", 
        "Genre", "Quiz Master", "Prize", "Contact Number", "Status"
    ])
    
    selected_event_id = st.selectbox("Select an Event to Edit", df["ID"])
    if selected_event_id:
        event = df[df["ID"] == selected_event_id].iloc[0]
        new_name = st.text_input("Edit Quiz Name", event["Quiz Name"])
        new_date = st.date_input("Edit Date", pd.to_datetime(event["Date"]))
        new_time = st.text_input("Edit Time", event["Time"])
        new_prize = st.text_input("Edit Prize", event["Prize"])

        if st.button("Save Changes"):
            edit_event(selected_event_id, new_name, new_date, new_time, new_prize)
            st.success(f"Event ID {selected_event_id} edited successfully!")

    # Delete Events
    st.write("Delete Events")
    del_event_id = st.selectbox("Select an Event to Delete", df["ID"])
    if st.button("Delete Event"):
        delete_event(del_event_id)
        st.success(f"Event ID {del_event_id} deleted successfully!")

    # Export Events
    st.write("Export Events")
    if st.button("Export to CSV"):
        export_events()
        st.success("Events exported successfully!")
        
elif full_password and full_password != FULL_ADMIN_PASSWORD:
    st.error("Incorrect Full Admin Password.")
