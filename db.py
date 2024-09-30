import sqlite3
import pandas as pd

# Connect to the database (or create it if it doesn't exist)
def connect_db():
    conn = sqlite3.connect('events.db')
    return conn

# Example function to fetch all events
def get_events(status):
    conn = connect_db()
    query = "SELECT * FROM events WHERE Status = ?"
    result = conn.execute(query, (status,))
    events = result.fetchall()
    conn.close()
    return events

# Example function to insert an event
def insert_event(event):
    conn = connect_db()
    query = '''
    INSERT INTO events 
    (QuizName, Date, Time, Category, Place, Location, Organizer, Genre, QuizMaster, Prize, ContactNumber, Status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    conn.execute(query, event)
    conn.commit()
    conn.close()


def init_db():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_name TEXT,
            date TEXT,
            time TEXT,
            category TEXT,
            place TEXT,
            location TEXT,
            organizer TEXT,
            genre TEXT,
            quiz_master TEXT,
            prize TEXT,
            contact_number TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_event(quiz_name, date, time, category, place, location, organizer, genre, quiz_master, prize, contact_number):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (quiz_name, date, time, category, place, location, organizer, genre, quiz_master, prize, contact_number, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
    ''', (quiz_name, date, time, category, place, location, organizer, genre, quiz_master, prize, contact_number))
    conn.commit()
    conn.close()

def get_events(status):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE status=?', (status,))
    events = c.fetchall()
    conn.close()
    return events

def approve_event(event_id):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('UPDATE events SET status="Approved" WHERE id=?', (event_id,))
    conn.commit()
    conn.close()

# Edit an event
def edit_event(event_id, quiz_name, date, time, prize):
    conn = connect_db()
    query = """
        UPDATE events 
        SET QuizName = ?, Date = ?, Time = ?, Prize = ?
        WHERE ID = ?
    """
    conn.execute(query, (quiz_name, date, time, prize, event_id))
    conn.commit()
    conn.close()

# Delete an event
def delete_event(event_id):
    conn = connect_db()
    query = "DELETE FROM events WHERE ID = ?"
    conn.execute(query, (event_id,))
    conn.commit()
    conn.close()

# Export events to a CSV file
def export_events():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM events", conn)
    df.to_csv("exported_events.csv", index=False)
    conn.close()
