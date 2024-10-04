import sqlite3
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
            venue TEXT,  -- Changed from place to venue
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
    
def add_event(quiz_name, date, time, category, venue, location, organizer, genre, quiz_master, prize, contact_number):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (quiz_name, date, time, category, venue, location, organizer, genre, quiz_master, prize, contact_number, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
    ''', (quiz_name, date, time, category, venue, location, organizer, genre, quiz_master, prize, contact_number))
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
