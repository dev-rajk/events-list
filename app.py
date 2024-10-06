import streamlit as st
from db import add_event, get_events, approve_event, update_event, delete_event
import pandas as pd
import json

st.set_page_config(
    page_title="Assam Quiz Calendar",
    layout="wide", 
    page_icon=":material/lightbulb:",
    menu_items={
        'about': '''**This was made with love in Assam**        
        The calendar attempts to help organisers and participants know more about the quizzing events across the state. 
        For feature requests or bug reports contact @dev_rajk on Instagram
        '''}
    )


st.title("Assam Quiz Calendar")

BASIC_ADMIN_PASSWORD = st.secrets.user.pass1
FULL_ADMIN_PASSWORD = st.secrets.user.pass2
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
            "title": event['quiz_name'],  # Quiz Name
            "start": event['date'],  # Date
            "extendedProps": {  # Additional event details
            "time": event['time'], 
                        "category": event['category'],  # Venue (renamed from place)
                        "venue": event['venue'],
                        "location":   event['location'], # Location
                        "organizer": event['organizer'],                    
                        "genre": event['genre'],
                        "quiz_master": event['quiz_master'],  # Quiz Master
                        "prize": event['prize'],
                        "contact_number": event['contact_number']  # Contact Number
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
        Title = st.text_input("Quiz Name")
        Date = st.date_input("Date")
        Time = st.text_input("Time")
        Category = st.text_input("Category")
        Venue = st.text_input("Venue")  # Changed from place to venue
        Location = st.text_input("Location")
        Organizer = st.text_input("Organizer")
        Genre = st.text_input("Genre")
        QM = st.text_input("Quiz Master")
        Prize = st.text_input("Prize")
        Contact = st.text_input("Contact Number")
        
        submit_button = st.form_submit_button(label='Submit Event')
        
        if submit_button:
            add_event(Title, Date, Time, Category, Venue, Location, Organizer, Genre, QM, Prize, Contact)
            st.success(f"Event '{Title}' submitted successfully! Awaiting admin approval.")


# 3. Admin Panel for Approving, Editing, Deleting, and Exporting Events
elif choice == "Admin Panel":
    st.subheader("Admin: Manage Events")
    password = st.text_input("Enter Admin Password", type="password")

    if password == BASIC_ADMIN_PASSWORD:
        pending_events = get_events("Pending")
        
        if  pending_events:
            columns = list(pending_events[0].keys())
            df = pd.DataFrame(pending_events, columns= columns)
            st.dataframe(df.drop(columns=["status"]))
                
            selected_event_id = st.selectbox("Select an Event to Approve", df["id"])
            if st.button("Approve Event"):
                approve_event(selected_event_id)
                st.success(f"Event ID {selected_event_id} approved!")

           
        else:
            st.write("No pending events to approve.")
    elif password == FULL_ADMIN_PASSWORD:
        # Fetch events based on status
        approved_events = get_events("Approved")
        pending_events = get_events("Pending")
    
        # Tab to switch between managing approved and pending events
        tab1, tab2 = st.tabs(["Manage Approved Events", "Approve Pending Events"])
    
        with tab1:  # Manage Approved Events Tab
            st.write("Manage Approved Events")
            
            if  approved_events:
                columns = list(approved_events[0].keys())
                df = pd.DataFrame(approved_events, columns=columns)
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"])
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form'):
                    Title = st.text_input("Quiz Name", value=selected_event["quiz_name"])
                    Date = st.date_input("Date", value=pd.to_datetime(selected_event["date"]))
                    Time = st.text_input("Time", value=selected_event["time"])
                    Category = st.text_input("Category", value=selected_event["category"])
                    Venue = st.text_input("Venue", value=selected_event["venue"])
                    Location = st.text_input("Location", value=selected_event["location"])
                    Organizer = st.text_input("Organizer", value=selected_event["organizer"])
                    Genre = st.text_input("Genre", value=selected_event["genre"])
                    QM = st.text_input("Quiz Master", value=selected_event["quiz_master"])
                    Prize = st.text_input("Prize", value=selected_event["prize"])
                    Contact = st.text_input("Contact Number", value=selected_event["contact_number"])
    
                    submit_button = st.form_submit_button(label='Update Event')
                    delete_button = st.form_submit_button(label='Delete Event')
    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, QM, Prize, Contact)
                        st.success(f"Event ID {selected_event_id} updated successfully!")
    
                    if delete_button:
                        # Delete event from the database
                        delete_event(selected_event_id)
                        st.success(f"Event ID {selected_event_id} deleted successfully!")
    
                # Button to export approved events as a CSV file
                if st.button('Export Approved Events as CSV'):
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name='approved_events.csv',
                        mime='text/csv',
                    )
    
            else:
                st.write("No approved events to manage.")
    
        with tab2:  # Approve Pending Events Tab
            st.write("Approve Pending Events")
    
            if  pending_events:
                columns = list(pending_events[0].keys())
                df_pending = pd.DataFrame(pending_events, columns=columns)
                
                st.dataframe(df_pending.drop(columns=["status"]))
    
                selected_event_id_pending = st.selectbox("Select an Event to Approve", df_pending["id"])
                if st.button("Approve Event"):
                    approve_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} approved!")
            else:
                st.write("No pending events to approve.")
    
     
    elif password:
        st.error("Incorrect Admin Password")
    
