Modify the existing project. Do not rebuild the application or change its existing architecture unnecessarily.

The project should look like a simple, professional reservation website with a clear Operating Systems Mutex demonstration.

## 1. Change Project Branding
- Replace "OS Seat Mutex" with **"Reservation.com"** everywhere it appears as the project name.
- Replace "College OS Project" with **"Confirm Booking Assured"**.
- Keep the branding clean and professional.

## 2. Dashboard Cleanup
Remove unnecessary information from the existing dashboard:

- Remove the "OS Concept Demo" badge.
- Remove lengthy explanations below headings.
- Remove the large race-condition explanation box.
- Remove the bottom "Threading Mutex Demo" label and "Python threading.Lock()" badge if decorative.
- Remove repeated technical explanations and unnecessary labels.

Keep the dashboard simple and focused.

## 3. Existing Concurrency Demonstration

Keep the two existing buttons:

1. Test Without Mutex
2. Test With Mutex

Display these results:
- Threads Started
- Successful Bookings
- Failed Bookings
- Final Seat Status

Use short result messages:

**Without Mutex:** "Race Condition Detected – Both threads booked the same seat."

**With Mutex:** "Mutex Applied – Only one thread successfully booked the seat."

Keep the thread execution trace, but make it compact and readable.

## 4. Add a Two-Passenger Booking Demonstration (IMPORTANT)

Add a separate section titled:

**"Simultaneous Passenger Booking Demo"**

This section should visually demonstrate two passengers trying to book tickets at the same time.

### Passenger Details

Provide two separate passenger detail forms:

**Passenger 1**
- Passenger Name
- Seat Number

**Passenger 2**
- Passenger Name
- Seat Number

Add a scenario selector:

- Same Seat – Both passengers attempt to book the same seat.
- Different Seats – Each passenger attempts to book a different seat.

Add a button:

**"Start Simultaneous Booking"**

When clicked:
- Create two Python threads.
- Start both booking attempts at nearly the same time.
- Use the selected passenger details and seat numbers.
- Display the booking result for each passenger separately.

### Expected Results

**Scenario A: Both passengers select the SAME seat**

With Mutex:
- Passenger 1: Booking Confirmed.
- Passenger 2: Booking Failed – Seat Already Booked.
- Only one booking should be stored.

Without Mutex:
- Simulate a race condition in an isolated test.
- Both threads may read the seat as available before either updates it.
- Demonstrate how both may report successful booking, causing overbooking.

**Scenario B: Both passengers select DIFFERENT seats**

With Mutex:
- Passenger 1: Booking Confirmed.
- Passenger 2: Booking Confirmed.
- Both bookings should succeed because the passengers selected different seats.

Without Mutex:
- Both passengers should also be able to book their different available seats.

### Demonstration Controls

Allow the user to select:
- With Mutex
- Without Mutex

Then click "Start Simultaneous Booking".

Display the results in two separate passenger result cards.

Each card should show:
- Passenger Name
- Selected Seat
- Booking Status
- Short result message

Also show a small summary:
- Total Attempts: 2
- Successful Bookings
- Failed Bookings

Reset the isolated test seats before each new demonstration so previous tests do not affect the results.

## 5. Important Mutex Logic

Implement actual Python threading.

- Use `threading.Lock()` to protect the critical section.
- The critical section must include checking seat availability and confirming the booking.
- Use `with lock:` for safe lock handling.
- Ensure two threads trying to book the same seat cannot both succeed when Mutex is enabled.
- Different seats must both be bookable.
- Use a synchronization mechanism such as `threading.Barrier` or `threading.Event` to coordinate simultaneous test starts.

The unsafe demonstration must use isolated in-memory test data. Never expose actual booking records to the unsafe race-condition test.

## 6. Database
Keep the existing SQLite database simple.

Use only the existing bookings table with:
- id
- seat_number
- passenger_name
- booking_status

Use a unique constraint on seat_number to prevent duplicate real bookings.

Do not add unnecessary tables or relationships.

## 7. UI Design
- Professional reservation website appearance.
- Clean dashboard with summary cards.
- Clear passenger booking forms.
- Green for successful bookings.
- Red for failed bookings.
- Yellow/orange for warnings.
- Compact thread execution logs.
- Responsive layout.
- Avoid unnecessary animations and decorative sections.

## 8. Important Instructions
- Modify the existing project instead of generating a new one.
- Preserve all working Flask routes and database functionality.
- Do not break the existing Mutex and race-condition tests.
- Do not remove the original "Test Without Mutex" and "Test With Mutex" buttons.
- Do not add login, payment, registration, email, external APIs, or deployment.
- Do not generate lengthy documentation or step-by-step explanations.
- Keep the implementation beginner-friendly and easy to explain during a college viva.
- Test all four combinations: same seat/different seats and with/without Mutex.

### Final Objective

The final application should clearly demonstrate:

1. Two passengers trying to book the same seat simultaneously.
2. Mutex allowing only one passenger to get confirmation.
3. Two passengers booking different seats successfully.
4. The difference between race conditions and mutual exclusion.

The main priority is a correct and understandable Mutex demonstration, not a complex reservation website.