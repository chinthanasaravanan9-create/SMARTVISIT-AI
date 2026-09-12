from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)


# =========================
# SERVICE INFORMATION
# =========================

services = {

    "KYC Update": {
        "employee": "KYC Officer",
        "duration": "15–25 minutes",
        "availability": "Available",
        "workload": "Low",
        "documents": [
            "Aadhaar Card / Valid ID Proof",
            "PAN Card",
            "Address Proof",
            "Passport-size Photo"
        ]
    },

    "Account Opening": {
        "employee": "Account Opening Officer",
        "duration": "20–30 minutes",
        "availability": "Available",
        "workload": "Medium",
        "documents": [
            "Aadhaar Card / Valid ID Proof",
            "PAN Card",
            "Address Proof",
            "Passport-size Photo"
        ]
    },

    "Loan Enquiry": {
        "employee": "Loan Officer",
        "duration": "30–45 minutes",
        "availability": "Available",
        "workload": "High",
        "documents": [
            "Aadhaar Card",
            "PAN Card",
            "Income Proof",
            "Bank Statement"
        ]
    },

    "Address Change": {
        "employee": "Customer Service Officer",
        "duration": "10–20 minutes",
        "availability": "Available",
        "workload": "Low",
        "documents": [
            "Aadhaar Card / Valid ID Proof",
            "New Address Proof"
        ]
    },

    "General Enquiry": {
        "employee": "Customer Service Officer",
        "duration": "5–15 minutes",
        "availability": "Available",
        "workload": "Low",
        "documents": [
            "Valid ID Proof"
        ]
    }
}


# =========================
# GOVERNMENT HOLIDAYS 2026
# =========================

holidays = {

    "2026-01-01": "New Year's Day",
    "2026-01-15": "Pongal",
    "2026-01-16": "Thiruvalluvar Day",
    "2026-01-17": "Uzhavar Thirunal",
    "2026-01-26": "Republic Day",

    "2026-02-01": "Thai Poosam",

    "2026-03-19": "Telugu New Year's Day",
    "2026-03-21": "Ramzan",
    "2026-03-31": "Mahaveer Jayanthi",

    "2026-04-01": "Annual Bank Closing",
    "2026-04-03": "Good Friday",
    "2026-04-14": "Tamil New Year",

    "2026-05-01": "May Day",

    "2026-05-28": "Bakrid",

    "2026-06-26": "Muharram",

    "2026-08-15": "Independence Day",
    "2026-08-26": "Milad-un-Nabi",

    "2026-09-04": "Krishna Jayanthi",
    "2026-09-14": "Vinayagar Chathurthi",

    "2026-10-02": "Gandhi Jayanthi",
    "2026-10-19": "Ayutha Pooja",
    "2026-10-20": "Vijaya Dasami",

    "2026-11-08": "Deepavali",

    "2026-12-25": "Christmas"
}


# =========================
# CHECK WEEKLY HOLIDAY
# =========================

def check_weekly_holiday(date):

    # Sunday
    if date.weekday() == 6:
        return "Sunday"

    # Saturday
    if date.weekday() == 5:

        saturday_number = (date.day - 1) // 7 + 1

        if saturday_number == 2:
            return "2nd Saturday"

        if saturday_number == 4:
            return "4th Saturday"

    return None


# =========================
# LOGIN
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        if username and password:

            if role == "customer":

                return render_template(
                    "customer.html",
                    username=username
                )

            elif role == "admin":

                return """
                <h1>Organization / Admin</h1>
                <p>Admin dashboard will be added next.</p>
                """

        return "Please enter username and password."

    return render_template("login.html")


# =========================
# CUSTOMER PAGE
# =========================

@app.route("/customer")
def customer():

    username = request.args.get(
        "username",
        "Customer"
    )

    return render_template(
        "customer.html",
        username=username
    )


# =========================
# RECOMMENDATION
# =========================

@app.route("/recommend", methods=["POST"])
def recommend():

    service = request.form.get("service")
    preferred_date = request.form.get("preferred_date")
    preferred_time = request.form.get("preferred_time")
    distance = request.form.get(
        "distance",
        "0"
    )

    # Check service
    if service not in services:

        return "Invalid service selected."

    service_info = services[service]

    employee = service_info["employee"]
    availability = service_info["availability"]
    workload = service_info["workload"]
    duration = service_info["duration"]
    documents = service_info["documents"]


    # =========================
    # CHECK DATE
    # =========================

    if not preferred_date:

        return "Please select a date."


    date = datetime.strptime(
        preferred_date,
        "%Y-%m-%d"
    ).date()


    # =========================
    # GOVERNMENT HOLIDAY
    # =========================

    if preferred_date in holidays:

        holiday_name = holidays[preferred_date]

        return render_template(
            "result.html",

            service=service,
            preferred_time=preferred_time,
            distance=distance,

            recommended_time="Branch Closed",

            documents=documents,

            employee="Not Available",

            availability="Closed",

            workload="N/A",

            duration="N/A",

            suitability="Government Holiday - " + holiday_name
        )


    # =========================
    # SUNDAY / SATURDAY
    # =========================

    weekly_holiday = check_weekly_holiday(date)

    if weekly_holiday:

        return render_template(
            "result.html",

            service=service,
            preferred_time=preferred_time,
            distance=distance,

            recommended_time="Branch Closed",

            documents=documents,

            employee="Not Available",

            availability="Closed",

            workload="N/A",

            duration="N/A",

            suitability=weekly_holiday + " Holiday"
        )


    # =========================
    # WORKING HOURS
    # =========================

    if preferred_time == "9:30 AM - 10:30 AM":

        recommended_time = "10:00 AM - 11:00 AM"

        suitability = "TIME ADJUSTED - BEFORE WORKING HOURS"


    # =========================
    # LUNCH BREAK
    # =========================

    elif preferred_time == "12:30 PM - 1:30 PM":

        recommended_time = "2:00 PM - 3:00 PM"

        suitability = "TIME ADJUSTED - LUNCH BREAK"


    elif preferred_time == "1:30 PM - 2:30 PM":

        recommended_time = "2:00 PM - 3:00 PM"

        suitability = "TIME ADJUSTED - LUNCH BREAK"


    # =========================
    # EMPLOYEE + WORKLOAD
    # =========================

    else:

        if availability == "Available":

            if workload == "Low":

                recommended_time = preferred_time

                suitability = "HIGH SUITABILITY"


            elif workload == "Medium":

                recommended_time = preferred_time

                suitability = "MEDIUM SUITABILITY"


            else:

                recommended_time = "2:00 PM - 3:00 PM"

                suitability = "LOW SUITABILITY"


        else:

            recommended_time = "Next Available Working Slot"

            suitability = "EMPLOYEE CURRENTLY BUSY"


    # =========================
    # RESULT
    # =========================

    return render_template(

        "result.html",

        service=service,

        preferred_time=preferred_time,

        distance=distance,

        recommended_time=recommended_time,

        documents=documents,

        employee=employee,

        availability=availability,

        workload=workload,

        duration=duration,

        suitability=suitability
    )


# =========================
# START APPLICATION
# =========================

if __name__ == "__main__":

    app.run(debug=True)