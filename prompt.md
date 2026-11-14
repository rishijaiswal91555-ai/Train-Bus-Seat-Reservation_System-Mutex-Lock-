Build a simple, functional **Seat Reservation System – Mutex Lock Demonstration** for a college Operating Systems project.

IMPORTANT: This is a small demonstration/prototype project, NOT a full commercial reservation application. Keep the code, architecture, database, and features simple. Do not over-engineer or generate lengthy explanations. Focus on implementing and demonstrating Mutex Lock.

### 1. Technology Stack
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Backend: Python Flask
- Database: SQLite (avoid MySQL to reduce setup complexity)
- Synchronization: Python threading.Lock()
- Use only free tools and libraries.

### 2. Application Pages

Create only two connected pages:

**Page 1: Main Dashboard**
- Project title: Seat Reservation System – Mutex Demonstration
- Display total seats (10).
- Display available seats.
- Display booked seats.
- Show a visual seat layout with 10 seats.
- Green = Available.
- Red = Booked.
- Display recent booking activity.
- Add a button to open the booking page.
- Add a button to run a concurrency demonstration.

**Page 2: Seat Booking Page**
- Display all 10 seats.
- Allow the user to select an available seat.
- Ask for a passenger name.
- Provide a Book Seat button.
- Show booking success or failure.
- Prevent users from booking an already booked seat.
- Add a button to return to the dashboard.

### 3. Operating System Concepts (MOST IMPORTANT)

Implement the following:

**A. Critical Section**
The critical section should contain the seat availability check and booking operation.

**B. Mutex Lock**
Use Python's threading.Lock() to protect the booking operation.

Example:
- Acquire the lock before checking seat availability.
- Check whether the seat is available.
- If available, mark it as booked.
- Release the lock after the operation.
- Use a `with lock:` block for safe lock handling.

**C. Race Condition Demonstration**
Create a separate demonstration function that simulates two threads trying to book the same seat simultaneously WITHOUT a mutex lock.

Show how both threads can read the seat as available before either updates it.

**D. Mutex Demonstration**
Run the same test WITH a mutex lock.

Show that only one thread successfully books the seat while the other receives a booking failure.

### 4. Database

Use SQLite with only one table:

`bookings`
- id
- seat_number
- passenger_name
- booking_status

Use a unique constraint on seat_number to prevent duplicate bookings.

Keep the database simple. Do not create unnecessary tables, relationships, authentication systems, or complex queries.

### 5. Dashboard Demonstration

Add a concurrency testing section to the dashboard.

Include two buttons:

1. Test Without Mutex
2. Test With Mutex

Display:
- Number of threads started.
- Number of successful bookings.
- Number of failed bookings.
- Final seat status.
- A clear message explaining whether a race condition or mutual exclusion occurred.

Reset the test seat between demonstrations so the results can be compared.

Keep the unsafe race-condition test isolated from actual booking records. Never leave the real booking functionality unprotected.

### 6. UI Design

Create a clean, modern college-project dashboard:
- Professional dashboard layout.
- Sidebar navigation.
- Summary cards.
- Seat status indicators.
- Simple tables.
- Clear success/error messages.
- Responsive design.
- Avoid unnecessary animations and complicated graphics.

### 7. Code Structure

Keep the folder structure simple:

seat_mutex_project/
│
├── app.py
├── database.py
├── mutex.py
├── requirements.txt
│
├── templates/
│   ├── dashboard.html
│   └── booking.html
│
└── static/
    ├── style.css
    └── script.js

### 8. Important Instructions

- Generate a working application, not just static UI.
- Connect the frontend to Flask routes.
- Ensure SQLite database operations work.
- Implement actual Python threads and Mutex Lock.
- Make both concurrency tests functional.
- Keep the code beginner-friendly and easy to explain in a college viva.
- Avoid unnecessary features such as login, payment, user registration, email, external APIs, and deployment.
- Do not install paid tools or use paid APIs.
- Do not generate lengthy documentation or explain every step.
- First inspect the existing project folder. Reuse useful files and modify only what is necessary.
- Run the application and fix errors before declaring it complete.

Priority: Correct Mutex implementation and a clear demonstration of race condition versus mutual exclusion are more important than UI complexity.