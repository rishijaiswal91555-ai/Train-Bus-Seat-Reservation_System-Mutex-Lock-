document.addEventListener("DOMContentLoaded", function () {
    // =============================================================
    // 1. Dashboard: Dynamic Bus vs Train View Toggle
    // =============================================================
    const toggleBusView = document.getElementById("toggle-bus-view");
    const toggleTrainView = document.getElementById("toggle-train-view");
    const layoutBus = document.getElementById("layout-bus-container");
    const layoutTrain = document.getElementById("layout-train-container");
    const statTotal = document.getElementById("stat-total-seats");
    const statAvailable = document.getElementById("stat-available-seats");
    const statBooked = document.getElementById("stat-booked-seats");
    const activeTransportLabels = document.querySelectorAll(".active-transport-label");
    const btnOpenBookingPage = document.getElementById("btn-open-booking-page");

    function switchDashboardTransport(type) {
        if (!window.SEAT_DATA) return;
        const data = window.SEAT_DATA[type];
        if (!data) return;

        // Update Toggle Buttons
        if (type === "Bus") {
            if (toggleBusView) {
                toggleBusView.className = "btn btn-primary fw-semibold";
            }
            if (toggleTrainView) {
                toggleTrainView.className = "btn btn-outline-secondary fw-semibold";
            }
            if (layoutBus) layoutBus.classList.remove("d-none");
            if (layoutTrain) layoutTrain.classList.add("d-none");
            if (btnOpenBookingPage) btnOpenBookingPage.href = "/book?type=Bus";
        } else {
            if (toggleTrainView) {
                toggleTrainView.className = "btn btn-primary fw-semibold";
            }
            if (toggleBusView) {
                toggleBusView.className = "btn btn-outline-secondary fw-semibold";
            }
            if (layoutTrain) layoutTrain.classList.remove("d-none");
            if (layoutBus) layoutBus.classList.add("d-none");
            if (btnOpenBookingPage) btnOpenBookingPage.href = "/book?type=Train";
        }

        // Update Labels and Summary Cards
        activeTransportLabels.forEach(el => el.textContent = type);
        if (statTotal) statTotal.textContent = data.total_seats;
        if (statAvailable) statAvailable.textContent = data.available_seats;
        if (statBooked) statBooked.textContent = data.booked_seats;
    }

    if (toggleBusView && toggleTrainView) {
        toggleBusView.addEventListener("click", () => switchDashboardTransport("Bus"));
        toggleTrainView.addEventListener("click", () => switchDashboardTransport("Train"));
    }

    // =============================================================
    // 2. Booking Page: Bus & Train Selection and Dynamic Dropdown
    // =============================================================
    const bookingTabBus = document.getElementById("booking-tab-bus");
    const bookingTabTrain = document.getElementById("booking-tab-train");
    const bookingBusLayout = document.getElementById("booking-bus-layout");
    const bookingTrainLayout = document.getElementById("booking-train-layout");
    const formTicketType = document.getElementById("form_ticket_type");
    const seatNumberDropdown = document.getElementById("seat_number");

    function populateBookingSeatDropdown(type) {
        if (!seatNumberDropdown || !window.BOOKING_SEAT_DATA) return;
        const data = window.BOOKING_SEAT_DATA[type];
        if (!data) return;

        seatNumberDropdown.innerHTML = '<option value="" disabled selected>-- Select a Seat --</option>';
        data.seats.forEach(seat => {
            const opt = document.createElement("option");
            opt.value = seat.seat_number;
            if (seat.is_booked) {
                opt.disabled = true;
                opt.textContent = `${seat.label} - ${seat.berth} (Booked - ${seat.passenger_name})`;
            } else {
                opt.textContent = `${seat.label} - ${seat.berth} (Available)`;
            }
            seatNumberDropdown.appendChild(opt);
        });
    }

    function switchBookingTransport(type) {
        if (formTicketType) formTicketType.value = type;

        if (type === "Bus") {
            if (bookingTabBus) bookingTabBus.className = "btn btn-primary fw-semibold";
            if (bookingTabTrain) bookingTabTrain.className = "btn btn-outline-secondary fw-semibold";
            if (bookingBusLayout) bookingBusLayout.classList.remove("d-none");
            if (bookingTrainLayout) bookingTrainLayout.classList.add("d-none");
        } else {
            if (bookingTabTrain) bookingTabTrain.className = "btn btn-primary fw-semibold";
            if (bookingTabBus) bookingTabBus.className = "btn btn-outline-secondary fw-semibold";
            if (bookingTrainLayout) bookingTrainLayout.classList.remove("d-none");
            if (bookingBusLayout) bookingBusLayout.classList.add("d-none");
        }

        // Clear previous seat selection highlight
        document.querySelectorAll(".clickable-seat").forEach(s => s.classList.remove("seat-selected"));
        populateBookingSeatDropdown(type);
    }

    if (bookingTabBus && bookingTabTrain) {
        bookingTabBus.addEventListener("click", () => switchBookingTransport("Bus"));
        bookingTabTrain.addEventListener("click", () => switchBookingTransport("Train"));
    }

    if (formTicketType) {
        formTicketType.addEventListener("change", function () {
            switchBookingTransport(this.value);
        });
        // Initial population
        populateBookingSeatDropdown(formTicketType.value || "Bus");
    }

    // Clickable seats on Booking Page
    const clickableSeats = document.querySelectorAll(".clickable-seat");
    clickableSeats.forEach(seat => {
        seat.addEventListener("click", function () {
            const transport = this.getAttribute("data-transport");
            const seatNumber = this.getAttribute("data-seat-number");

            if (formTicketType && formTicketType.value !== transport) {
                switchBookingTransport(transport);
            }

            clickableSeats.forEach(s => s.classList.remove("seat-selected"));
            this.classList.add("seat-selected");

            if (seatNumberDropdown) {
                seatNumberDropdown.value = seatNumber;
            }
        });
    });

    if (seatNumberDropdown) {
        seatNumberDropdown.addEventListener("change", function () {
            const currentTransport = formTicketType ? formTicketType.value : "Bus";
            const currentVal = this.value;

            clickableSeats.forEach(seat => {
                const sType = seat.getAttribute("data-transport");
                const sNum = seat.getAttribute("data-seat-number");
                if (sType === currentTransport && sNum === currentVal) {
                    seat.classList.add("seat-selected");
                } else {
                    seat.classList.remove("seat-selected");
                }
            });
        });
    }

    // =============================================================
    // 3. Simultaneous Passenger Booking Demo (Bus & Train)
    // =============================================================
    const scenarioSameSeat = document.getElementById("scenario-same-seat");
    const scenarioDiffSeat = document.getElementById("scenario-diff-seat");
    const scenarioDiffType = document.getElementById("scenario-diff-type");

    const p1Type = document.getElementById("p1-type");
    const p1Seat = document.getElementById("p1-seat");
    const p1Name = document.getElementById("p1-name");
    const p1Badge = document.getElementById("p1-type-badge");

    const p2Type = document.getElementById("p2-type");
    const p2Seat = document.getElementById("p2-seat");
    const p2Name = document.getElementById("p2-name");
    const p2Badge = document.getElementById("p2-type-badge");

    const modeMutex = document.getElementById("mode-mutex");
    const btnStartSimultaneous = document.getElementById("btn-start-simultaneous");

    const simResultsPanel = document.getElementById("sim-results-panel");
    const simSummaryBanner = document.getElementById("sim-summary-banner");
    const simSummaryText = document.getElementById("sim-summary-text");
    const simTotalAttempts = document.getElementById("sim-total-attempts");
    const simSuccessful = document.getElementById("sim-successful");
    const simFailed = document.getElementById("sim-failed");

    const resP1Name = document.getElementById("res-p1-name");
    const resP1Type = document.getElementById("res-p1-type");
    const resP1Seat = document.getElementById("res-p1-seat");
    const resP1Status = document.getElementById("res-p1-status");
    const resP1Message = document.getElementById("res-p1-message");
    const resP1Badge = document.getElementById("res-p1-badge");
    const cardP1Result = document.getElementById("card-p1-result");

    const resP2Name = document.getElementById("res-p2-name");
    const resP2Type = document.getElementById("res-p2-type");
    const resP2Seat = document.getElementById("res-p2-seat");
    const resP2Status = document.getElementById("res-p2-status");
    const resP2Message = document.getElementById("res-p2-message");
    const resP2Badge = document.getElementById("res-p2-badge");
    const cardP2Result = document.getElementById("card-p2-result");

    const simExecutionLogs = document.getElementById("sim-execution-logs");

    function updateSeatOptions(selectElement, transportType) {
        if (!selectElement) return;
        const currentVal = selectElement.value || "1";
        const prefix = transportType === "Train" ? "T" : "B";
        selectElement.innerHTML = "";
        for (let i = 1; i <= 10; i++) {
            const opt = document.createElement("option");
            opt.value = i;
            opt.textContent = `${prefix}${i} (Seat #${i})`;
            if (i.toString() === currentVal.toString()) {
                opt.selected = true;
            }
            selectElement.appendChild(opt);
        }
    }

    if (p1Type && p1Seat && p1Badge) {
        p1Type.addEventListener("change", function () {
            p1Badge.textContent = this.value;
            updateSeatOptions(p1Seat, this.value);
            if (scenarioSameSeat && scenarioSameSeat.checked) {
                p2Type.value = this.value;
                p2Badge.textContent = this.value;
                updateSeatOptions(p2Seat, this.value);
                p2Seat.value = p1Seat.value;
            }
        });
    }

    if (p2Type && p2Seat && p2Badge) {
        p2Type.addEventListener("change", function () {
            p2Badge.textContent = this.value;
            updateSeatOptions(p2Seat, this.value);
        });
    }

    // Scenarios Setup
    function applySimScenario() {
        if (scenarioSameSeat && scenarioSameSeat.checked) {
            // Same Seat + Same Type
            p1Type.value = "Bus";
            p2Type.value = "Bus";
            p1Badge.textContent = "Bus";
            p2Badge.textContent = "Bus";
            updateSeatOptions(p1Seat, "Bus");
            updateSeatOptions(p2Seat, "Bus");
            p1Seat.value = "1";
            p2Seat.value = "1";
            p2Type.disabled = true;
            p2Seat.disabled = true;
        } else if (scenarioDiffSeat && scenarioDiffSeat.checked) {
            // Different Seats + Same Type
            p1Type.value = "Bus";
            p2Type.value = "Bus";
            p1Badge.textContent = "Bus";
            p2Badge.textContent = "Bus";
            updateSeatOptions(p1Seat, "Bus");
            updateSeatOptions(p2Seat, "Bus");
            p1Seat.value = "1";
            p2Seat.value = "2";
            p2Type.disabled = false;
            p2Seat.disabled = false;
        } else if (scenarioDiffType && scenarioDiffType.checked) {
            // Different Types (Bus vs Train, same seat number 1)
            p1Type.value = "Bus";
            p2Type.value = "Train";
            p1Badge.textContent = "Bus";
            p2Badge.textContent = "Train";
            updateSeatOptions(p1Seat, "Bus");
            updateSeatOptions(p2Seat, "Train");
            p1Seat.value = "1";
            p2Seat.value = "1";
            p2Type.disabled = false;
            p2Seat.disabled = false;
        }
    }

    if (scenarioSameSeat) scenarioSameSeat.addEventListener("change", applySimScenario);
    if (scenarioDiffSeat) scenarioDiffSeat.addEventListener("change", applySimScenario);
    if (scenarioDiffType) scenarioDiffType.addEventListener("change", applySimScenario);

    if (p1Seat && p2Seat) {
        p1Seat.addEventListener("change", function () {
            if (scenarioSameSeat && scenarioSameSeat.checked) {
                p2Seat.value = this.value;
            }
        });
    }

    // Start Simultaneous Booking Button Handler
    if (btnStartSimultaneous) {
        btnStartSimultaneous.addEventListener("click", function () {
            btnStartSimultaneous.disabled = true;
            btnStartSimultaneous.innerHTML = "<span class='spinner-border spinner-border-sm me-2'></span>Simulating concurrent booking...";

            const payload = {
                passenger1_type: p1Type.value,
                passenger1_name: (p1Name ? p1Name.value.trim() : "") || "Alice",
                seat1: parseInt(p1Seat.value),
                passenger2_type: p2Type.value,
                passenger2_name: (p2Name ? p2Name.value.trim() : "") || "Bob",
                seat2: parseInt(p2Seat.value),
                with_mutex: modeMutex ? modeMutex.checked : true
            };

            fetch("/api/simultaneous-booking", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            })
            .then(res => {
                if (!res.ok) throw new Error("Server error during simulation");
                return res.json();
            })
            .then(data => {
                if (simResultsPanel) simResultsPanel.classList.remove("d-none");

                // Summary Banner
                if (simSummaryText) simSummaryText.textContent = data.summary_message;
                if (simSummaryBanner) {
                    if (data.summary_message.includes("Race Condition")) {
                        simSummaryBanner.className = "alert alert-danger mb-4 text-center fw-semibold py-3 shadow-sm";
                    } else if (data.summary_message.includes("Mutex Applied")) {
                        simSummaryBanner.className = "alert alert-success mb-4 text-center fw-semibold py-3 shadow-sm";
                    } else {
                        simSummaryBanner.className = "alert alert-info mb-4 text-center fw-semibold py-3 shadow-sm";
                    }
                }

                // Summary Metrics
                if (simTotalAttempts) simTotalAttempts.textContent = data.total_attempts;
                if (simSuccessful) simSuccessful.textContent = data.successful_bookings;
                if (simFailed) simFailed.textContent = data.failed_bookings;

                // Passenger 1 Result Card
                if (resP1Name) resP1Name.textContent = data.passenger1.name;
                if (resP1Type) resP1Type.textContent = data.passenger1.ticket_type;
                if (resP1Seat) resP1Seat.textContent = data.passenger1.seat_number;
                if (resP1Status) resP1Status.textContent = data.passenger1.status;
                if (resP1Message) resP1Message.textContent = data.passenger1.message;
                if (resP1Badge) {
                    resP1Badge.className = data.passenger1.success ? "badge bg-success" : "badge bg-danger";
                    resP1Badge.textContent = data.passenger1.success ? "CONFIRMED" : "FAILED";
                }
                if (cardP1Result) {
                    cardP1Result.className = data.passenger1.success
                        ? "card h-100 shadow-sm border border-success"
                        : "card h-100 shadow-sm border border-danger";
                }

                // Passenger 2 Result Card
                if (resP2Name) resP2Name.textContent = data.passenger2.name;
                if (resP2Type) resP2Type.textContent = data.passenger2.ticket_type;
                if (resP2Seat) resP2Seat.textContent = data.passenger2.seat_number;
                if (resP2Status) resP2Status.textContent = data.passenger2.status;
                if (resP2Message) resP2Message.textContent = data.passenger2.message;
                if (resP2Badge) {
                    resP2Badge.className = data.passenger2.success ? "badge bg-success" : "badge bg-danger";
                    resP2Badge.textContent = data.passenger2.success ? "CONFIRMED" : "FAILED";
                }
                if (cardP2Result) {
                    cardP2Result.className = data.passenger2.success
                        ? "card h-100 shadow-sm border border-success"
                        : "card h-100 shadow-sm border border-danger";
                }

                // Render Logs
                if (simExecutionLogs) {
                    simExecutionLogs.innerHTML = "";
                    data.logs.forEach(log => {
                        const line = document.createElement("div");
                        line.className = "log-line";
                        if (log.includes("[Thread-1]")) line.classList.add("log-t1");
                        if (log.includes("[Thread-2]")) line.classList.add("log-t2");
                        if (log.includes("Confirmed") || log.includes("AVAILABLE")) line.classList.add("log-success");
                        if (log.includes("Failed") || log.includes("Already Booked") || log.includes("already booked")) line.classList.add("log-fail");
                        if (log.includes("Lock")) line.classList.add("log-mutex");
                        line.textContent = log;
                        simExecutionLogs.appendChild(line);
                    });
                }
            })
            .catch(err => {
                console.error("Simulation error:", err);
                if (simSummaryBanner) {
                    simSummaryBanner.className = "alert alert-warning mb-4 text-center py-2";
                    simSummaryText.textContent = "Simulation failed: " + err.message;
                }
            })
            .finally(() => {
                btnStartSimultaneous.disabled = false;
                btnStartSimultaneous.innerHTML = "<i class='bi bi-play-fill me-1'></i> Start Simultaneous Booking";
            });
        });
    }
});
