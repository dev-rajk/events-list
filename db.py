import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Initialize Firestore using secrets
if not firebase_admin._apps:  # Check if the app is already initialized
    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Firestore operations
def add_event(quiz_name, date, time, category, venue, location, organizer, genre, quiz_master, prize, contact_number):
    doc_ref = db.collection('events').document()
    doc_ref.set({
        'quiz_name': quiz_name,
        'date': str(date),
        'time': time,
        'category': category,
        'venue': venue,
        'location': location,
        'organizer': organizer,
        'genre': genre,
        'quiz_master': quiz_master,
        'prize': prize,
        'contact_number': contact_number,
        'status': 'Pending'
    })

def get_events(status):
    events_ref = db.collection('events').where('status', '==', status)
    events = events_ref.stream()
    events_list = []
    for event in events:
        event_data = event.to_dict()
        event_data['id'] = event.id
        events_list.append(event_data)
    return events_list

def approve_event(event_id):
    doc_ref = db.collection('events').document(event_id)
    doc_ref.update({'status': 'Approved'})

def update_event(event_id, quiz_name, date, time, category, venue, location, organizer, genre, quiz_master, prize, contact_number):
    doc_ref = db.collection('events').document(event_id)
    doc_ref.update({
        'quiz_name': quiz_name,
        'date': str(date),
        'time': time,
        'category': category,
        'venue': venue,
        'location': location,
        'organizer': organizer,
        'genre': genre,
        'quiz_master': quiz_master,
        'prize': prize,
        'contact_number': contact_number
    })

def delete_event(event_id):
    db.collection('events').document(event_id).delete()
