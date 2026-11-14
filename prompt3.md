Modify the existing Reservation.com project. Do not rebuild the application.

### 1. Remove Duplicate Mutex Demonstration Panel

The dashboard currently contains two Mutex demonstration sections:

- Simultaneous Passenger Booking Demo (upper section)
- Concurrency Demonstration (lower section)

Keep **Simultaneous Passenger Booking Demo**.

Completely remove the lower **Concurrency Demonstration** panel, including:
- Test Without Mutex button
- Test With Mutex button
- Threads Started counter
- Successful Bookings counter
- Failed Bookings counter
- Final Seat Status
- Thread Execution Trace
- Related result messages

The upper Simultaneous Passenger Booking Demo already provides these demonstrations, so the lower panel is unnecessary.

IMPORTANT: Remove only the duplicate UI section. Preserve the underlying Mutex implementation and testing logic used by the upper demonstration.

### 2. Add Bus and Train Options to Seat Layout

The project is a **Train/Bus Ticket Reservation System**, so the seat layout should support both transport types.

Add two options above the seat layout:

- Bus
- Train

When the user selects Bus:
- Display a bus-style seat layout.
- Show seats arranged in rows with a realistic bus configuration.
- Include seat numbers.
- Use green for available seats and red for booked seats.

When the user selects Train:
- Display a train-style seat layout.
- Show a realistic train seating arrangement.
- Include seat numbers and appropriate berth/seat labels where practical.
- Use green for available seats and red for booked seats.

Switching between Bus and Train should update the seat layout dynamically.

Keep the layouts simple and suitable for a college project demonstration. Do not create overly complicated seating arrangements.

### 3. Update Booking Details and Status

Make sure every booking is associated with its transport type.

Display the following in booking status and booking confirmation:

- Passenger Name
- Ticket Type (Bus or Train)
- Seat Number
- Booking Status
- Booking Result

Example:

Passenger: Alice  
Ticket Type: Bus  
Seat Number: B3  
Status: Booking Confirmed

Passenger: Bob  
Ticket Type: Train  
Seat Number: T5  
Status: Booking Confirmed

Also show the ticket type in the recent booking activity section.

### 4. Update Simultaneous Passenger Booking Demo

The existing two-passenger demonstration should support both Bus and Train tickets.

Add a transport type selection for each passenger:
- Bus
- Train

Allow passengers to select their seat according to the selected transport type.

Preserve the existing demonstration scenarios:

**Same Seat + Same Transport Type**
- Without Mutex: demonstrate a race condition.
- With Mutex: only one passenger gets confirmation.

**Different Seats + Same Transport Type**
- Both passengers can book successfully.

**Different Transport Types**
- Both passengers can book successfully, even if the seat numbers are identical, because bus and train seats are separate resources.

Ensure the lock protects the correct shared resource. Use a resource key that includes both transport type and seat number, such as `(ticket_type, seat_number)`.

### 5. Database Updates

Keep SQLite and the existing database structure as simple as possible.

If necessary, add a `ticket_type` column to the existing bookings table.

Allowed values:
- Bus
- Train

Ensure duplicate seat prevention applies to the combination of ticket type and seat number, not seat number alone.

Avoid creating unnecessary tables.

### 6. UI Requirements

- Maintain the existing Reservation.com branding.
- Keep the subtitle "Confirm Booking Assured".
- Maintain the current dashboard design and color scheme.
- Make Bus/Train selection clear and easy to use.
- Keep the dashboard clean and responsive.
- Do not add unnecessary pages, animations, or features.

### 7. Important Instructions

- Inspect the existing code before making changes.
- Modify existing files instead of generating a new project.
- Preserve working Flask routes and database functionality.
- Do not break the existing Mutex demonstration.
- Do not remove the upper Simultaneous Passenger Booking Demo.
- Remove only the lower duplicate Concurrency Demonstration panel.
- Test Bus and Train seat selection.
- Test booking confirmation and booking status.
- Test same-seat and different-seat simultaneous bookings.
- Ensure all changes work with the existing application.

**Final Objective:** A simple Train/Bus Reservation.com prototype with separate bus and train seat layouts, clear ticket-type information, and one complete two-passenger Mutex demonstration.