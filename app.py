import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import (
    init_db,
    get_seat_status,
    get_all_seats_status,
    get_recent_bookings,
    reset_all_bookings
)
from mutex import (
    book_seat_with_mutex,
    run_race_condition_test,
    run_mutex_test,
    run_simultaneous_passenger_test
)

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "reservation_com_bus_train_mutex_demo_key")

# Initialize database table and composite constraints on startup
init_db()

@app.route("/")
def dashboard():
    """Main Dashboard: Displays Bus & Train seat layouts, summary cards, and Simultaneous Demo."""
    bus_data = get_seat_status("Bus")
    train_data = get_seat_status("Train")
    recent_bookings = get_recent_bookings(limit=6)

    return render_template(
        "dashboard.html",
        bus_data=bus_data,
        train_data=train_data,
        recent_bookings=recent_bookings
    )

@app.route("/book", methods=["GET", "POST"])
def booking():
    """Page 2: Seat Booking Page for Bus or Train, protected with Mutex Lock."""
    if request.method == "POST":
        ticket_type = request.form.get("ticket_type", "Bus").strip()
        seat_number_raw = request.form.get("seat_number")
        passenger_name = request.form.get("passenger_name", "").strip()

        if not seat_number_raw or not passenger_name:
            flash("Please choose a seat and enter a passenger name.", "danger")
            return redirect(url_for("booking"))

        try:
            seat_number = int(seat_number_raw)
        except ValueError:
            flash("Invalid seat number specified.", "danger")
            return redirect(url_for("booking"))

        # Execute safe booking operation protected by Mutex Lock in critical section
        success, message = book_seat_with_mutex(ticket_type, seat_number, passenger_name)

        if success:
            flash(message, "success")
            return redirect(url_for("dashboard"))
        else:
            flash(f"Booking Failed: {message}", "danger")
            return redirect(url_for("booking", type=ticket_type))

    # GET request: render the booking page with both Bus & Train seat status
    selected_type = request.args.get("type", "Bus")
    if selected_type.lower() == "train":
        selected_type = "Train"
    else:
        selected_type = "Bus"

    bus_data = get_seat_status("Bus")
    train_data = get_seat_status("Train")

    return render_template(
        "booking.html",
        selected_type=selected_type,
        bus_data=bus_data,
        train_data=train_data
    )

@app.route("/api/simultaneous-booking", methods=["POST"])
def api_simultaneous_booking():
    """API endpoint for Two-Passenger Simultaneous Booking with Bus & Train support."""
    data = request.get_json() or {}

    p1_type = data.get("passenger1_type", "Bus")
    p1_name = data.get("passenger1_name", "Alice")
    p2_type = data.get("passenger2_type", "Bus")
    p2_name = data.get("passenger2_name", "Bob")

    try:
        seat1 = int(data.get("seat1", 1))
        seat2 = int(data.get("seat2", 1))
    except (ValueError, TypeError):
        seat1, seat2 = 1, 1

    with_mutex = bool(data.get("with_mutex", True))

    result = run_simultaneous_passenger_test(
        passenger1_type=p1_type,
        passenger1_name=p1_name,
        seat1=seat1,
        passenger2_type=p2_type,
        passenger2_name=p2_name,
        seat2=seat2,
        with_mutex=with_mutex
    )
    return jsonify(result)

@app.route("/api/reset-bookings", methods=["POST"])
def api_reset_bookings():
    """Reset all real bookings for a fresh demonstration."""
    reset_all_bookings()
    flash("All seat reservations have been reset successfully.", "info")
    return redirect(url_for("dashboard"))

@app.route("/api/seats", methods=["GET"])
def api_seats():
    """Return JSON status of all seats for Bus and Train."""
    return jsonify(get_all_seats_status())

# Retain legacy routes for testing / compatibility
@app.route("/api/test-race-condition", methods=["POST"])
def api_test_race_condition():
    return jsonify(run_race_condition_test())

@app.route("/api/test-mutex", methods=["POST"])
def api_test_mutex():
    return jsonify(run_mutex_test())

if __name__ == "__main__":
    # Support dynamic PORT environment variable (standard for cloud platforms like Render)
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
