import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Determine SQLite database path from environment variable or default
_db_env = os.getenv("DATABASE_PATH", "reservation.db")
if os.path.isabs(_db_env):
    DB_PATH = _db_env
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), _db_env)

TOTAL_SEATS = 10

# Realistic seat metadata
BUS_SEAT_METADATA = {
    1: {"label": "B1", "berth": "Window"},
    2: {"label": "B2", "berth": "Aisle"},
    3: {"label": "B3", "berth": "Aisle"},
    4: {"label": "B4", "berth": "Window"},
    5: {"label": "B5", "berth": "Window"},
    6: {"label": "B6", "berth": "Aisle"},
    7: {"label": "B7", "berth": "Aisle"},
    8: {"label": "B8", "berth": "Window"},
    9: {"label": "B9", "berth": "Window"},
    10: {"label": "B10", "berth": "Window"},
}

TRAIN_SEAT_METADATA = {
    1: {"label": "T1", "berth": "Lower Berth"},
    2: {"label": "T2", "berth": "Middle Berth"},
    3: {"label": "T3", "berth": "Upper Berth"},
    4: {"label": "T4", "berth": "Side Lower"},
    5: {"label": "T5", "berth": "Side Upper"},
    6: {"label": "T6", "berth": "Lower Berth"},
    7: {"label": "T7", "berth": "Middle Berth"},
    8: {"label": "T8", "berth": "Upper Berth"},
    9: {"label": "T9", "berth": "Side Lower"},
    10: {"label": "T10", "berth": "Side Upper"},
}

def get_db_connection():
    """Establish and return a SQLite database connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize or migrate the SQLite database with ticket_type and composite UNIQUE constraint."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check existing schema of bookings table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("PRAGMA table_info(bookings)")
        columns = [row["name"] for row in cursor.fetchall()]
        if "ticket_type" not in columns:
            # Migrate table to include ticket_type and composite unique constraint
            cursor.execute("""
                CREATE TABLE bookings_migrated (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_type TEXT NOT NULL DEFAULT 'Bus',
                    seat_number INTEGER NOT NULL,
                    passenger_name TEXT NOT NULL,
                    booking_status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(ticket_type, seat_number)
                )
            """)
            cursor.execute("""
                INSERT INTO bookings_migrated (id, ticket_type, seat_number, passenger_name, booking_status, created_at)
                SELECT id, 'Bus', seat_number, passenger_name, booking_status, created_at FROM bookings
            """)
            cursor.execute("DROP TABLE bookings")
            cursor.execute("ALTER TABLE bookings_migrated RENAME TO bookings")
            conn.commit()
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_type TEXT NOT NULL DEFAULT 'Bus',
                seat_number INTEGER NOT NULL,
                passenger_name TEXT NOT NULL,
                booking_status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(ticket_type, seat_number)
            )
        """)
        conn.commit()

    conn.close()

def get_seat_status(ticket_type="Bus"):
    """
    Returns the status of all 10 seats for the specified transport type ('Bus' or 'Train'),
    along with summary counts and realistic seat/berth labels.
    """
    ticket_type = "Train" if str(ticket_type).lower() == "train" else "Bus"
    meta_dict = TRAIN_SEAT_METADATA if ticket_type == "Train" else BUS_SEAT_METADATA

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT seat_number, passenger_name, booking_status FROM bookings WHERE ticket_type = ?",
        (ticket_type,)
    )
    rows = cursor.fetchall()
    conn.close()

    booked_map = {row["seat_number"]: row for row in rows}
    seats = []
    booked_count = 0

    for seat_num in range(1, TOTAL_SEATS + 1):
        meta = meta_dict.get(seat_num, {"label": f"#{seat_num}", "berth": ""})
        if seat_num in booked_map:
            seats.append({
                "seat_number": seat_num,
                "label": meta["label"],
                "berth": meta["berth"],
                "ticket_type": ticket_type,
                "is_booked": True,
                "passenger_name": booked_map[seat_num]["passenger_name"],
                "status": booked_map[seat_num]["booking_status"]
            })
            booked_count += 1
        else:
            seats.append({
                "seat_number": seat_num,
                "label": meta["label"],
                "berth": meta["berth"],
                "ticket_type": ticket_type,
                "is_booked": False,
                "passenger_name": None,
                "status": "AVAILABLE"
            })

    available_count = TOTAL_SEATS - booked_count

    return {
        "ticket_type": ticket_type,
        "total_seats": TOTAL_SEATS,
        "available_seats": available_count,
        "booked_seats": booked_count,
        "seats": seats
    }

def get_all_seats_status():
    """Returns combined seat status for both Bus and Train."""
    bus_status = get_seat_status("Bus")
    train_status = get_seat_status("Train")
    return {
        "Bus": bus_status,
        "Train": train_status,
        "total_seats": TOTAL_SEATS * 2,
        "available_seats": bus_status["available_seats"] + train_status["available_seats"],
        "booked_seats": bus_status["booked_seats"] + train_status["booked_seats"]
    }

def get_recent_bookings(limit=5):
    """Retrieve recent booking activity including ticket type."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, ticket_type, seat_number, passenger_name, booking_status, created_at "
        "FROM bookings ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        row_dict = dict(r)
        # Add label e.g. B1 or T1
        prefix = "T" if row_dict["ticket_type"] == "Train" else "B"
        row_dict["seat_label"] = f"{prefix}{row_dict['seat_number']}"
        results.append(row_dict)
    return results

def is_seat_available(ticket_type, seat_number):
    """Check if a seat is available for the given transport type (Bus or Train)."""
    ticket_type = "Train" if str(ticket_type).lower() == "train" else "Bus"
    if seat_number < 1 or seat_number > TOTAL_SEATS:
        return False
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM bookings WHERE ticket_type = ? AND seat_number = ?",
        (ticket_type, seat_number)
    )
    row = cursor.fetchone()
    conn.close()
    return row is None

def add_booking(ticket_type, seat_number, passenger_name):
    """
    Insert a booking for Bus or Train into SQLite database.
    Returns (True, message) on success, or (False, error_message) on failure.
    """
    ticket_type = "Train" if str(ticket_type).lower() == "train" else "Bus"
    prefix = "T" if ticket_type == "Train" else "B"
    seat_label = f"{prefix}{seat_number}"

    if seat_number < 1 or seat_number > TOTAL_SEATS:
        return False, f"Invalid seat number. Please choose between 1 and {TOTAL_SEATS}."

    if not passenger_name or not passenger_name.strip():
        return False, "Passenger name cannot be empty."

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO bookings (ticket_type, seat_number, passenger_name, booking_status) VALUES (?, ?, ?, ?)",
            (ticket_type, seat_number, passenger_name.strip(), "CONFIRMED")
        )
        conn.commit()
        success = True
        message = (
            f"Passenger: {passenger_name.strip()} | "
            f"Ticket Type: {ticket_type} | "
            f"Seat Number: {seat_label} | "
            f"Status: Booking Confirmed"
        )
    except sqlite3.IntegrityError:
        success = False
        message = f"{ticket_type} Seat {seat_label} is already booked! (Seat unavailable)"
    except Exception as e:
        success = False
        message = f"Error during booking: {str(e)}"
    finally:
        conn.close()

    return success, message

def reset_all_bookings():
    """Clear all bookings to reset the system."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='bookings'")
    conn.commit()
    conn.close()
