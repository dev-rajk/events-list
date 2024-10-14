import streamlit as st
from db import add_event, get_events, approve_event, update_event, delete_event, decline_event
import pandas as pd
import json

st.set_page_config(
    page_title="Assam Quiz Calendar",
    layout="wide", 
    page_icon=":material/lightbulb:",
    menu_items={
        'about': '''**This was made with love in Assam**        
        The calendar attempts to help organisers and participants know more about the quizzing events across the state. 
        
        '''}
    )


st.title("Assam Quiz Calendar :calendar: ")
st.write('Select in sidebar to view quizzes or submit events')

BASIC_ADMIN_PASSWORD = st.secrets.user.pass1
FULL_ADMIN_PASSWORD = st.secrets.user.pass2
# Sidebar navigation
st.sidebar.title("Navigation")
options = ["View Events", "Submit Event", "Admin Panel"]
choice = st.sidebar.selectbox("Choose an action", options)

# FullCalendar HTML and JavaScript with custom modal including all event details
def fullcalendar(events, theme_mode):
    events_json = json.dumps(events)  # Convert events to JSON string
    
    # Styles for light and dark mode
    light_style = """
    body {
        background-color: white;
        color: black;
        font-family: Arial, sans-serif;
    }
    .modal-content {
        background-color: white;
        color: black;
        font-family: Arial, sans-serif;
    }
    .fc-event, .fc-daygrid-event, .fc-daygrid-event-dot {
        color: black;
        background-color: teal;
    }
    """
    
    dark_style = """
    body {
        background-color: black;
        color: black;
        font-family: Arial, sans-serif;
    }
    .modal-content {
        background-color: #2e2e2e;
        color: white;
        font-family: Arial, sans-serif;
    }
    .fc-event, .fc-daygrid-event, .fc-daygrid-event-dot {
        color: black;
        background-color: teal;
    }
    """

    # Determine the style based on the theme mode
    selected_style = dark_style if theme_mode == 'dark' else light_style

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

            /* Dynamic Style based on theme */
            {selected_style}
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
              initialView: 'dayGridMonth',  // Default to month view
              headerToolbar: {{
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek'  // Toggle between month and week views
              }},
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
                document.getElementById('modal-registration_link').innerHTML = info.event.extendedProps.registration_link || 'N/A';
                document.getElementById('modal-other_details').innerText = info.event.extendedProps.other_details || 'N/A';

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
            <p><strong>Registration Link (External link! Copy to another tab):</strong> <span id="modal-registration_link"></span></p>
            <p><strong>Other Details:</strong> <span id="modal-other_details"></span></p>
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
                        "contact_number": event['contact_number'],  # Contact Number
                        "registration_link": f'<a href="{event["registration_link"]}" target="_blank">Click here to register</a>',
                        "other_details": event['other_details']
                    }
                })
            
        # Retrieve current theme mode from Streamlit settings
        theme_mode = st.get_option('theme.base')  # 'light' or 'dark'

        # Display FullCalendar with modal functionality based on the global theme
        st.components.v1.html(fullcalendar(events, theme_mode=theme_mode), height=800)

        st.write('''
                :red[**This website is free of cost for all users.** ] \n
                :red[**The maintainers bear no responsibility for the accuracy of the event information, or any loss or damages resulting from the use of this site. The maintainer is not liable for any damages or misinformation.**] \n
                :red[**Users are encouraged to verify all event information.**] \n
                :red[**No personal infomation is tracked.**] \n
                :green[**Cheers to quizzing.** ] :partying_face::partying_face:\n
                  ''')

            
    else:
        st.write("No approved events to show.")
        st.write('''
                :red[ **This website is free of cost for all users.** ] \n
                :red[**The maintainers bear no responsibility for the accuracy of the event information, or any loss or damages resulting from the use of this site. The maintainer is not liable for any damages or misinformation.** ]  \n
                :red[**Users are encouraged to verify all event information.**] \n
                :red[**No personal infomation is tracked.** ] \n
                :green[**Cheers to quizzing.** ] :partying_face::partying_face:\n
                  ''')


# 2. Submitting Events
elif choice == "Submit Event":
    st.subheader("Submit a New Quiz Event")
    
    with st.form(key='event_form'):
        st.write(''':red[Please ensure that event details are accurate
                 Fields marked with * are necessary]''')
        Title = st.text_input("Quiz Name*")
        Date = st.date_input("Date*")
        Time = st.text_input("Time")
        Category = st.text_input("Category*")
        Venue = st.text_input("Venue")  # Changed from place to venue
        Location = st.text_input("Location*")
        Organizer = st.text_input("Organizer")
        Genre = st.text_input("Genre")
        QM = st.text_input("Quiz Master")
        Prize = st.text_input("Prize")
        Contact = st.text_input("Contact Number*")
        registration_link = st.text_input(" Registration Link")
        other_details = st.text_area("Other Details")
        
        submit_button = st.form_submit_button(label='Submit Event')
        
        if submit_button:
            if not Title or not Contact or not Location or not Date or not Category:
                st.error("Please fill all the fields marked with a *")
            else:
                add_event(Title, Date, Time, Category, Venue, Location, Organizer, Genre, QM, Prize, Contact, registration_link, other_details)
                st.success(f"Event '{Title}' submitted successfully! Awaiting admin approval.")
            

    st.markdown('''
                :red[ **This website is free of cost for all users.** ] \n
                :red[**The maintainers bear no responsibility for the accuracy of the event information, or any loss or damages resulting from the use of this site. The maintainer is not liable for any damages or misinformation.** ]  \n
                :red[**Users are encouraged to verify all event information.** ] \n
                :red[**No personal infomation is tracked.** ] \n
                :red[**Cheers to quizzing.** ] :partying_face::partying_face:\n
                  ''')


# 3. Admin Panel for Approving, Editing, Deleting, and Exporting Events
elif choice == "Admin Panel":
    st.subheader("Admin: Manage Events")
    password = st.text_input("Enter Admin Password", type="password")

    if password == BASIC_ADMIN_PASSWORD:
        # Fetch events based on status
        approved_events = get_events("Approved")
        pending_events = get_events("Pending")
        declined_events = get_events("Declined")
    
        # Tab to switch between managing approved and pending events
        tab1, tab2, tab3 = st.tabs(["Manage Approved Events", "Approve Pending Events", "Declined Events"])
    
        with tab1:  # Manage Approved Events Tab
            st.write("Manage Approved Events")
            
            if  approved_events:
                
                df = pd.DataFrame(approved_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"], key =1)
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form_accepted_1'):
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
                    registration_link = st.text_input(" Registration Link", value=selected_event["registration_link"])
                    other_details = st.text_area("Other Details", value=selected_event["other_details"])
        
    
                    submit_button = st.form_submit_button(label='Update Event')
                    st.write('Updated events need to be approved again')
                   
    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, QM, Prize, Contact, registration_link, other_details)
                        st.success(f"Event ID {selected_event_id} updated successfully!")
    
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
                st.markdown("No approved events to manage. :smiley: :smiley: :smiley:")
    
        with tab2:  # Approve Pending Events Tab
            st.write("Approve Pending Events")
    
            if  pending_events:
                
                df_pending = pd.DataFrame(pending_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
                
                st.dataframe(df_pending.drop(columns=["status"]))
    
                selected_event_id_pending = st.selectbox("Select an Event to Approve", df_pending["id"], key =2)
                if st.button("Approve Event"):
                    approve_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} approved!")
                elif st.button("Decline Event"):
                    decline_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} Declined!")
            else:
                st.markdown("No pending events to approve. :smiley: :smiley: :smiley:")
        with tab3:  # Manage Approved Events Tab
            st.write("Manage Declined Events")
            
            if  declined_events:
                
                df = pd.DataFrame(declined_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"], key =3)
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form_declined_1'):
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
                    registration_link = st.text_input(" Registration Link", value=selected_event["registration_link"])
                    other_details = st.text_area("Other Details", value=selected_event["other_details"])
        
    
                    submit_button = st.form_submit_button(label='Update Event')
                    st.write('Updated events need to be approved again')
                    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, QM, Prize, Contact, registration_link, other_details)
                        st.success(f"Event ID {selected_event_id} updated successfully!")
    
            else:
                st.write("No Declined events.")
    elif password == FULL_ADMIN_PASSWORD:
        # Fetch events based on status
        approved_events = get_events("Approved")
        pending_events = get_events("Pending")
        declined_events = get_events("Declined")
        # Tab to switch between managing approved and pending events
        tab1, tab2, tab3 = st.tabs(["Manage Approved Events", "Approve Pending Events", "Declined Events"])
    
        with tab1:  # Manage Approved Events Tab
            st.write("Manage Approved Events")
            
            if  approved_events:
                
                df = pd.DataFrame(approved_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"], key =4)
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form_accepted_2'):
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
                    registration_link = st.text_input(" Registration Link", value=selected_event["registration_link"])
                    other_details = st.text_area("Other Details", value=selected_event["other_details"])
        
    
                    submit_button = st.form_submit_button(label='Update Event')
                    st.write('Updated events need to be approved again')
                    delete_button = st.form_submit_button(label='Delete Event')
    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, QM, Prize, Contact, registration_link, other_details)
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
                
                df_pending = pd.DataFrame(pending_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
                
                st.dataframe(df_pending.drop(columns=["status"]))
    
                selected_event_id_pending = st.selectbox("Select an Event to Approve", df_pending["id"], key = 5)
                if st.button("Approve Event"):
                    approve_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} approved!")
                elif st.button("Decline Event"):
                    decline_event(selected_event_id_pending)
                    st.success(f"Event ID {selected_event_id_pending} Declined!")
            else:
                st.write("No pending events to approve.")
        with tab3:  # Manage Approved Events Tab
            st.write("Manage Declined Events")
            
            if  declined_events:
                
                df = pd.DataFrame(declined_events, columns= ['id', 'quiz_name', 'date', 'time', 'category', 'venue', 'location', 'organizer', 'genre', 'quiz_master', 'prize', 'contact_number', 'registration_link', 'other_details', 'status' ])
    
                # Display approved events
                st.dataframe(df.drop(columns=["status"]))
    
                # Select event for editing or deleting
                selected_event_id = st.selectbox("Select an Event to Edit or Delete", df["id"], key =6)
                selected_event = df[df["id"] == selected_event_id].iloc[0]  # Get selected event details
    
                # Editing form with existing values pre-filled
                with st.form(key='edit_event_form_declined_2'):
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
                    registration_link = st.text_input(" Registration Link", value=selected_event["registration_link"])
                    other_details = st.text_area("Other Details", value=selected_event["other_details"])
        
    
                    submit_button = st.form_submit_button(label='Update Event')
                    st.write('Updated events need to be approved again')
                    delete_button = st.form_submit_button(label='Delete Event')
    
                    if submit_button:
                        # Update event in the database
                        update_event(selected_event_id, Title, Date, Time, Category, Venue, Location, Organizer, Genre, QM, Prize, Contact, registration_link, other_details)
                        st.success(f"Event ID {selected_event_id} updated successfully!")
    
                    if delete_button:
                        # Delete event from the database
                        delete_event(selected_event_id)
                        st.success(f"Event ID {selected_event_id} deleted successfully!")
            else:
                st.write("No Declined events.")
    
     
    elif password:
        st.error("Incorrect Admin Password")
    
