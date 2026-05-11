import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==============================
# TRAIN TICKET & REVENUE SYSTEM
# ==============================
# Language : Python
# Database : MySQL
# Visualization : Matplotlib

print("=" * 60)
print("        TRAIN TICKET & REVENUE SYSTEM")
print("=" * 60)

# ------------------------------
# MYSQL DATABASE CONNECTION
# ------------------------------
# Change username and password according to your MySQL setup

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Suraj@0987*#",
        database="railwaydb"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        passenger_name VARCHAR(100),
        age INT,
        class_type VARCHAR(20),
        route_name VARCHAR(100),
        seat_no INT,
        fare INT,
        booking_date VARCHAR(50)
    )
    """)

    conn.commit()

except Exception as e:
    print("Database Connection Error:", e)

# ------------------------------
# ROUTE INFORMATION
# ------------------------------

routes = {
    1: {"route": "SEC to Rayalaseema", "distance": 731},
    2: {"route": "SEC to Mumbai", "distance": 879},
    3: {"route": "SEC to Chennai", "distance": 784}
}

print("\nAvailable Routes")
print("1. SEC to Rayalaseema")
print("2. SEC to Mumbai")
print("3. SEC to Chennai")

route_choice = int(input("\nSelect Route: "))

route_name = routes[route_choice]["route"]
distance = routes[route_choice]["distance"]

print("Selected Route:", route_name)
print("Distance:", distance, "KM")

# ------------------------------
# PASSENGER DETAILS
# ------------------------------

num_passengers = int(input("\nEnter Number of Passengers: "))

passenger_data = []
total_fare = 0

for i in range(num_passengers):
    print(f"\nPassenger {i + 1} Details")

    name = input("Enter Passenger Name: ")
    age = int(input("Enter Age: "))

    print("\nClass Types")
    print("1. General")
    print("2. Sleeper")
    print("3. AC")

    class_choice = int(input("Select Class Type: "))

    if class_choice == 1:
        class_type = "General"
        base_fare = 150

    elif class_choice == 2:
        class_type = "Sleeper"
        base_fare = 400

    else:
        class_type = "AC"
        base_fare = 900

    # Dynamic Fare Calculation
    dynamic_charge = int(distance * 0.5)
    fare = base_fare + dynamic_charge

    # Child Discount
    if age < 12:
        fare = int(fare * 0.5)

    seat_no = 100 + i

    print("Seat Allocated:", seat_no)
    print("Ticket Fare:", fare)

    total_fare += fare

    booking_date = str(datetime.now())

    passenger_data.append([
        name,
        age,
        class_type,
        route_name,
        seat_no,
        fare,
        booking_date
    ])

    # Insert into Database
    try:
        sql = """
        INSERT INTO bookings
        (passenger_name, age, class_type, route_name, seat_no, fare, booking_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            age,
            class_type,
            route_name,
            seat_no,
            fare,
            booking_date
        )

        cursor.execute(sql, values)
        conn.commit()

    except Exception as e:
        print("Database Insert Error:", e)

# ------------------------------
# DISPLAY TICKET DETAILS
# ------------------------------

columns = [
    "Passenger Name",
    "Age",
    "Class",
    "Route",
    "Seat No",
    "Fare",
    "Booking Date"
]


df = pd.DataFrame(passenger_data, columns=columns)

print("\n================ TICKET DETAILS ================")
print(df.to_string(index=False))

print("\nTotal Ticket Revenue:", total_fare)

# ------------------------------
# TRAIN TIME CALCULATION
# ------------------------------

average_speed = int(input("\nEnter Average Train Speed (KM/H): "))

time_taken = distance / average_speed

print("Estimated Time to Reach Destination:")
print(round(time_taken, 2), "Hours")

# ------------------------------
# LIVE SEAT AVAILABILITY
# ------------------------------

print("\n================ SEAT AVAILABILITY ================")

TOTAL_GENERAL = 100
TOTAL_SLEEPER = 120
TOTAL_AC = 60

booked_general = 0
booked_sleeper = 0
booked_ac = 0

for row in passenger_data:
    if row[2] == "General":
        booked_general += 1

    elif row[2] == "Sleeper":
        booked_sleeper += 1

    else:
        booked_ac += 1

print("General Available Seats:", TOTAL_GENERAL - booked_general)
print("Sleeper Available Seats:", TOTAL_SLEEPER - booked_sleeper)
print("AC Available Seats:", TOTAL_AC - booked_ac)

# ------------------------------
# CANCELLATION & REFUND LOGIC
# ------------------------------

cancel = input("\nDo you want to cancel any ticket? (yes/no): ")

refund_amount = 0

if cancel.lower() == "yes":
    cancel_name = input("Enter Passenger Name for Cancellation: ")

    for row in passenger_data:
        if row[0].lower() == cancel_name.lower():
            refund_amount = int(row[5] * 0.8)
            total_fare -= refund_amount

            print("Ticket Cancelled Successfully")
            print("Refund Amount:", refund_amount)
            break

# ------------------------------
# REVENUE ANALYTICS
# ------------------------------

print("\n================ REVENUE ANALYTICS ================")

revenue_general = 0
revenue_sleeper = 0
revenue_ac = 0

for row in passenger_data:
    if row[2] == "General":
        revenue_general += row[5]

    elif row[2] == "Sleeper":
        revenue_sleeper += row[5]

    else:
        revenue_ac += row[5]

print("General Revenue:", revenue_general)
print("Sleeper Revenue:", revenue_sleeper)
print("AC Revenue:", revenue_ac)
print("Final Revenue:", total_fare)

# ------------------------------
# BAR CHART
# ------------------------------

classes = ["General", "Sleeper", "AC"]
revenues = [revenue_general, revenue_sleeper, revenue_ac]

plt.figure(figsize=(8, 5))
plt.bar(classes, revenues)
plt.xlabel("Class Type")
plt.ylabel("Revenue")
plt.title("Revenue Generated by Train Classes")
plt.show()

# ------------------------------
# PIE CHART
# ------------------------------

plt.figure(figsize=(6, 6))
plt.pie(
    revenues,
    labels=classes,
    autopct='%1.1f%%',
    shadow=True
)

plt.title("Revenue Distribution")
plt.legend()
plt.show()

# ------------------------------
# MONTHLY REVENUE ANALYSIS
# ------------------------------

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
monthly_revenue = [15000, 20000, 18000, 25000, 30000, total_fare]

plt.figure(figsize=(8, 5))
plt.plot(months, monthly_revenue, marker='o')
plt.xlabel("Months")
plt.ylabel("Revenue")
plt.title("Monthly Revenue Analysis")
plt.grid(True)
plt.show()

# ------------------------------
# DATABASE RECORDS DISPLAY
# ------------------------------

print("\n================ DATABASE RECORDS ================")

try:
    cursor.execute("SELECT * FROM bookings")
    records = cursor.fetchall()

    for record in records:
        print(record)

except Exception as e:
    print("Fetch Error:", e)

# ------------------------------
# PROJECT SUMMARY
# ------------------------------

print("\n===================================================")
print("TRAIN TICKET & REVENUE SYSTEM COMPLETED SUCCESSFULLY")
print("===================================================")

print("\nProject Features:")
print("1. Ticket Booking System")
print("2. Dynamic Fare Calculation")
print("3. Live Seat Availability")
print("4. Cancellation & Refund Logic")
print("5. Revenue Analytics")
print("6. MySQL Database Integration")
print("7. Matplotlib Visualizations")

# ------------------------------
# CLOSE DATABASE CONNECTION
# ------------------------------

try:
    cursor.close()
    conn.close()

except:
    pass
