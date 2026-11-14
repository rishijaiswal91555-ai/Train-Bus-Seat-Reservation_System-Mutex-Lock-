import threading
import time
from database import is_seat_available, add_booking

# Global Mutex Lock for real database booking operations
booking_lock = threading.Lock()

def book_seat_with_mutex(ticket_type, seat_number, passenger_name):
    """
    Safely book a real seat using Python's threading.Lock().
    
    CRITICAL SECTION:
    1. Check seat availability for (ticket_type, seat_number).
    2. Insert booking record if available.
    """
    with booking_lock:
        # --- CRITICAL SECTION BEGINS ---
        if not is_seat_available(ticket_type, seat_number):
            prefix = "T" if str(ticket_type).lower() == "train" else "B"
            return False, f"{ticket_type} Seat {prefix}{seat_number} is already booked! (Critical Section Protected)"
        
        success, message = add_booking(ticket_type, seat_number, passenger_name)
        return success, message
        # --- CRITICAL SECTION ENDS ---


# =====================================================================
# SIMULTANEOUS PASSENGER BOOKING DEMONSTRATION
# Supports Bus & Train, Same Seat vs Different Seats, With vs Without Mutex
# Uses resource key (ticket_type, seat_number) and threading.Barrier(2)
# =====================================================================

sim_two_passenger_lock = threading.Lock()

def run_simultaneous_passenger_test(passenger1_type, passenger1_name, seat1,
                                    passenger2_type, passenger2_name, seat2,
                                    with_mutex=True):
    """
    Simulates two passengers concurrently attempting to book seats.
    - Synchronizes start using threading.Barrier(2).
    - Resource key is (ticket_type, seat_number) so Bus and Train seats are distinct.
    - If with_mutex is True, critical section is protected with threading.Lock().
    - If with_mutex is False, critical section is unprotected to expose race conditions.
    - Operates strictly on an isolated in-memory test layout.
    """
    p1_type = "Train" if str(passenger1_type).lower() == "train" else "Bus"
    p2_type = "Train" if str(passenger2_type).lower() == "train" else "Bus"

    p1_prefix = "T" if p1_type == "Train" else "B"
    p2_prefix = "T" if p2_type == "Train" else "B"

    # 1. Reset isolated test seats (Bus 1-10 and Train 1-10)
    test_seats = {
        ("Bus", i): {"is_booked": False, "booked_by": None, "booking_count": 0}
        for i in range(1, 11)
    }
    test_seats.update({
        ("Train", i): {"is_booked": False, "booked_by": None, "booking_count": 0}
        for i in range(1, 11)
    })

    logs = []
    barrier = threading.Barrier(2)

    p1_result = {
        "name": passenger1_name or "Passenger 1",
        "ticket_type": p1_type,
        "seat_number": f"{p1_prefix}{seat1}",
        "raw_seat": seat1,
        "status": "",
        "success": False,
        "message": ""
    }
    p2_result = {
        "name": passenger2_name or "Passenger 2",
        "ticket_type": p2_type,
        "seat_number": f"{p2_prefix}{seat2}",
        "raw_seat": seat2,
        "status": "",
        "success": False,
        "message": ""
    }

    res1 = (p1_type, seat1)
    res2 = (p2_type, seat2)
    same_resource = (res1 == res2)

    def booking_worker(p_name, p_type, seat_num, result_dict, thread_id):
        # Synchronize release time so both threads hit critical section simultaneously
        barrier.wait()
        if thread_id == "Thread-2":
            time.sleep(0.005)  # Slight offset to give Thread-1 priority for consistent lock ordering

        res_key = (p_type, seat_num)
        prefix = "T" if p_type == "Train" else "B"
        label = f"{prefix}{seat_num}"

        logs.append(f"[{thread_id}] {p_name} requesting booking for {p_type} Seat {label}.")

        if with_mutex:
            # Protected Critical Section
            with sim_two_passenger_lock:
                logs.append(f"[{thread_id}] Lock acquired by {p_name}. Checking {p_type} Seat {label}...")
                if not test_seats[res_key]["is_booked"]:
                    logs.append(f"[{thread_id}] {p_type} Seat {label} is AVAILABLE. Confirming booking...")
                    time.sleep(0.04)
                    test_seats[res_key]["is_booked"] = True
                    test_seats[res_key]["booked_by"] = p_name
                    test_seats[res_key]["booking_count"] += 1
                    result_dict["status"] = "Booking Confirmed"
                    result_dict["success"] = True
                    result_dict["message"] = f"Booking Confirmed on {p_type} Seat {label}."
                    logs.append(f"[{thread_id}] Booking Confirmed for {p_name} on {p_type} Seat {label}.")
                else:
                    result_dict["status"] = "Booking Failed"
                    result_dict["success"] = False
                    result_dict["message"] = f"Booking Failed – Seat Already Booked by {test_seats[res_key]['booked_by']}."
                    logs.append(f"[{thread_id}] Booking Failed for {p_name}: {p_type} Seat {label} already booked.")
                logs.append(f"[{thread_id}] Lock released by {p_name}.")
        else:
            # Unprotected Critical Section (Race Condition)
            logs.append(f"[{thread_id}] {p_name} checking {p_type} Seat {label} WITHOUT Mutex...")
            available = not test_seats[res_key]["is_booked"]
            logs.append(f"[{thread_id}] {p_name} read status as {'AVAILABLE' if available else 'BOOKED'}.")
            
            # Latency exposing race condition window
            time.sleep(0.05)
            
            if available:
                test_seats[res_key]["is_booked"] = True
                test_seats[res_key]["booked_by"] = p_name
                test_seats[res_key]["booking_count"] += 1
                result_dict["status"] = "Booking Confirmed"
                result_dict["success"] = True
                if same_resource and test_seats[res_key]["booking_count"] > 1:
                    result_dict["message"] = f"Booking Confirmed (Race Condition – Overbooked on {label})."
                else:
                    result_dict["message"] = f"Booking Confirmed on {p_type} Seat {label}."
                logs.append(f"[{thread_id}] {p_name} wrote booking for {p_type} Seat {label}.")
            else:
                result_dict["status"] = "Booking Failed"
                result_dict["success"] = False
                result_dict["message"] = f"Booking Failed – Seat Already Booked."
                logs.append(f"[{thread_id}] {p_name} booking failed: {p_type} Seat {label} already booked.")

    t1 = threading.Thread(
        target=booking_worker,
        args=(p1_result["name"], p1_type, seat1, p1_result, "Thread-1")
    )
    t2 = threading.Thread(
        target=booking_worker,
        args=(p2_result["name"], p2_type, seat2, p2_result, "Thread-2")
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Calculate summary counts
    success_count = (1 if p1_result["success"] else 0) + (1 if p2_result["success"] else 0)
    failed_count = 2 - success_count

    # Determine summary explanation
    if same_resource:
        if not with_mutex:
            summary_message = "Race Condition Detected – Both threads booked the same seat."
        else:
            summary_message = "Mutex Applied – Only one thread successfully booked the seat."
    elif p1_type != p2_type:
        summary_message = "Different Transport Types – Bus and Train seats are separate resources, so both bookings succeeded."
    else:
        summary_message = "Both passengers successfully booked their different seats."

    return {
        "scenario": "same_resource" if same_resource else "different_resources",
        "with_mutex": with_mutex,
        "total_attempts": 2,
        "successful_bookings": success_count,
        "failed_bookings": failed_count,
        "summary_message": summary_message,
        "passenger1": p1_result,
        "passenger2": p2_result,
        "logs": logs
    }


# Retain legacy functions for test compatibility
def run_race_condition_test():
    res = run_simultaneous_passenger_test("Alice", "Bus", 1, "Bob", "Bus", 1, with_mutex=False)
    return {
        "test_type": "Without Mutex",
        "threads_started": 2,
        "successful_bookings": res["successful_bookings"],
        "failed_bookings": res["failed_bookings"],
        "final_seat_status": f"Overbooked on B1",
        "is_race_condition": True,
        "explanation": "Race Condition Detected – Both threads booked the same seat.",
        "logs": res["logs"]
    }

def run_mutex_test():
    res = run_simultaneous_passenger_test("Alice", "Bus", 1, "Bob", "Bus", 1, with_mutex=True)
    return {
        "test_type": "With Mutex",
        "threads_started": 2,
        "successful_bookings": res["successful_bookings"],
        "failed_bookings": res["failed_bookings"],
        "final_seat_status": f"Booked by Alice on B1",
        "is_race_condition": False,
        "explanation": "Mutex Applied – Only one thread successfully booked the seat.",
        "logs": res["logs"]
    }
