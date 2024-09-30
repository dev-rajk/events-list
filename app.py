import streamlit as st
from db import init_db, add_event, get_events, approve_event
import pandas as pd

# Initialize the database (create the table if not exists)
init_db()

st.title("Community Quiz Event System")

# Sidebar navigation
st.sidebar.title("Navigation")
options = ["View Events", "Submit Event", "Admin Panel"]
choice = st.sidebar.selectbox("Choose an action", options)

# 1. Viewing Events
if choice == "View Events":
    st.subheader("Upcoming Quizzes")
    approved_events = get_events("Approved")
    if approved_events:
        df = pd.DataFrame(approved_events, columns=[
            "ID", "Quiz Name", "Date", "Time", "Category", "Place", "Location", "Organizer", 
            "Genre", "Quiz Master", "Prize", "Contact Number", "Status"
        ])
        st.dataframe(df.drop(columns=["ID", "Status"]))
    else:
        st.write("No approved events to show.")

# 2. Submitting Events
elif choice == "Submit Event":
    st.subheader("Submit a New Quiz Event")
    
    with st.form(key='event_form'):
        quiz_name = st.text_input("Quiz Name")
        date = st.date_input("Date")
        time = st.text_input("Time")
        category = st.text_input("Category")
        place = st.text_input("Place")
        location = st.text_input("Location")
        organizer = st.text_input("Organizer")
        genre = st.text_input("Genre")
        quiz_master = st.text_input("Quiz Master")
        prize = st.text_input("Prize")
        contact_number = st.text_input("Contact Number")
        
        submit_button = st.form_submit_button(label='Submit Event')
        
        if submit_button:
            add_event(quiz_name, date, time, category, place, location, organizer, genre, quiz_master, prize, contact_number)
            st.success(f"Event '{quiz_name}' submitted successfully! Awaiting admin approval.")

# 3. Admin Panel for Approving Events
elif choice == "Admin Panel":
    st.subheader("Admin: Approve Pending Events")
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
