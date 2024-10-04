import streamlit as st
from db import init_db, add_event, get_events, approve_event
import pandas as pd
import json

st.set_page_config(
    page_title="Assam Quiz Calendar")
# Initialize the database
init_db()

st.title("Assam Quiz Calendar")

# Sidebar navigation
st.sidebar.title("Navigation")
options = ["View Events", "Submit Event", "Admin Panel"]
choice = st.sidebar.selectbox("Choose an action", options)

# FullCalendar HTML and JavaScript with custom modal including all event details
def fullcalendar(events):
    events_json = json.dumps(events)  # Convert events to JSON string
    calendar_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.css' rel='stylesheet' />
        <script src='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js'></script>
        <style>
            /* The Modal (background) */
            .modal {{
                display: none; /* Hidden by default */
                position: fixed; /* Stay in place */
                z-index: 1; /* Sit on top */
                left: 0;
                top: 0;
                width: 100%; /* Full width */
                height: 100%; /* Full height */
                overflow: auto; /* Enable scroll if needed */
                background-color: rgb(0,0,0); /* Fallback color */
                background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
                padding-top: 60px;
            }}

            /* Modal Content */
            .modal-content {{
                background-color: #fefefe;
                margin: 5% auto; /* 15% from the top and centered */
                padding: 20px;
                border: 1px solid #888;
                width: 80%; /* Could be more or less, depending on screen size */
            }}

            /* The Close Button */
            .close {{
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }}

            .close:hover,
            .close:focus {{
                color: black;
                text-decoration: none;
                cursor: pointer;
            }}
        </style>
        <script>
          document.addEventListener('DOMContentLoaded', function() {{
            var calendarEl = document.getElementById('calendar');
            var modal = document.getElementById('myModal');
            var closeModal = document.getElementsByClassName('close')[0];

            // Close the modal when the user clicks on <span> (x)
            closeModal.onclick = function() {{
                modal.style.display = "none";
            }}

            // Close the modal when the user clicks outside of it
            window.onclick = function(event) {{
                if (event.target == modal) {{
                    modal.style.display = "none";
                }}
            }}

            var calendar = new FullCalendar.Calendar(calendarEl, {{
              initialView: 'dayGridMonth',
              events: {events_json},
              eventClick: function(info) {{
                // Populate modal with all event details
                document.getElementById('modal-title').innerText = info.event.title;
                document.getElementById('modal-date').innerText = info.event.start.toLocaleDateString();
                document.getElementById('modal-time').innerText = info.event.extendedProps.time || 'N/A';
                document.getElementById('modal-venue').innerText = info.event.extendedProps.venue || 'N/A';
                document.getElementById('modal-location').innerText = info.event.extendedProps.location || 'N/A';
                document.getElementById('modal-organizer').innerText = info.event.extendedProps.organizer || 'N/A';
                document.getElementById('modal-category').innerText = info.event.extendedProps.category || 'N/A';
                document.getElementById('modal-quiz-master').innerText = info.event.extendedProps.quiz_master || 'N/A';
                document.getElementById('modal-genre').innerText = info.event.extendedProps.genre || 'N/A';
                document.getElementById('modal-prize').innerText = info.event.extendedProps.prize || 'N/A';
                document.getElementById('modal-contact').innerText = info.event.extendedProps.contact_number || 'N/A';

                // Display the modal
                modal.style.display = "block";
              }}
            }});
            calendar.render();
          }});
        </script>
    </head>
    <body>

        <!-- FullCalendar -->
        <div id='calendar'></div>

        <!-- The Modal -->
        <div id="myModal" class="modal">
          <div class="modal-content">
            <span class="close">&times;</span>
            <h2 id="modal-title"></h2>
            <p><strong>Date:</strong> <span id="modal-date"></span></p>
            <p><strong>Time:</strong> <span id="modal-time"></span></p>
            <p><strong>Venue:</strong> <span id="modal-venue"></span></p>
            <p><strong>Location:</strong> <span id="modal-location"></span></p>
            <p><strong>Organizer:</strong> <span id="modal-organizer"></span></p>
            <p><strong>Category:</strong> <span id="modal-category"></span></p>
            <p><strong>Quiz Master:</strong> <span id="modal-quiz-master"></span></p>
            <p><strong>Genre:</strong> <span id="modal-genre"></span></p>
            <p><strong>Prize:</strong> <span id="modal-prize"></span></p>
            <p><strong>Contact Number:</strong> <span id="modal-contact"></span></p>
          </div>
        </div>

    </body>
    </html>
    """
    return calendar_code


# 1. Viewing Events
if choice == "View Events":
    st.subheader("Upcoming Quizzes")
    approved_events = get_events("Approved")
    
    if approved_events:
        # Prepare events for FullCalendar
        events = []
        for event in approved_events:
            events.append({
                "title": event[1],  # Quiz Name
                "start": event[2],  # Date
                "extendedProps": {  # Additional event details
                    "time": event[3], 
                    "Category": event[4],  # Venue (renamed from place)
                    "venue": event[5],
                    "location":   event[6], # Location
                    "organizer": event[7],                    
                    "genre": event[8],
                    "quiz_master": event[9],  # Quiz Master
                    "prize": event[10],
                    "contact_number": event[11]  # Contact Number
                }
            })
        
        # Display FullCalendar with modal functionality
        st.components.v1.html(fullcalendar(events), height=600)
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
        venue = st.text_input("Venue")  # Changed from place to venue
        location = st.text_input("Location")
        organizer = st.text_input("Organizer")
        genre = st.text_input("Genre")
        quiz_master = st.text_input("Quiz Master")
        prize = st.text_input("Prize")
        contact_number = st.text_input("Contact Number")
        
        submit_button = st.form_submit_button(label='Submit Event')
        
        if submit_button:
            add_event(quiz_name, date, time, category, venue, location, organizer, genre, quiz_master, prize, contact_number)
            st.success(f"Event '{quiz_name}' submitted successfully! Awaiting admin approval.")


# 3. Admin Panel for Approving Events
elif choice == "Admin Panel":
    st.subheader("Admin: Approve Pending Events")
    pending_events = get_events("Pending")
    
    if pending_events:
        df = pd.DataFrame(pending_events, columns=[
            "ID", "Quiz Name", "Date", "Time", "Category", "Venue", "Location", "Organizer", 
            "Genre", "Quiz Master", "Prize", "Contact Number", "Status"
        ])  # Changed from place to venue
        st.dataframe(df.drop(columns=["Status"]))
        
        selected_event_id = st.selectbox("Select an Event to Approve", df["ID"])
        if st.button("Approve Event"):
            approve_event(selected_event_id)
            st.success(f"Event ID {selected_event_id} approved!")
    else:
        st.write("No pending events to approve.")
