import mysql.connector

def connect_db():
    return mysql.connector.connect(
        user="root",
        password="9693",
        host="localhost",
        database="spotsplus"
    )

def execute_query(query, values=None, fetch=False):
    conn = connect_db()
    cursor = conn.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    if fetch:
        result = cursor.fetchall()
    else:
        conn.commit()
        result = None
    cursor.close()
    conn.close()
    return result

def user_login():
    email = input("Enter your email: ")
    password1 = input("Enter your password: ")
    query = "SELECT * FROM Users WHERE email=%s AND password1=%s"
    user = execute_query(query, (email, password1), fetch=True)
    if user:
        print("Login successful!")
        user_dashboard(user[0][0])
    else:
        print("Invalid credentials.")

def user_signup():
    print("\nSign Up")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password1 = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")
    if password1 != confirm_password:
        print("Passwords do not match. Please try again.")
        return
    else:
        query = "INSERT INTO Users (name, email, password1) VALUES (%s, %s, %s)"
        try:
            execute_query(query, (name, email, password1))
            print("Sign-up successful! You can now log in.")
        except Exception as e:
            print(f"Error: {e}. Email might already be registered.")

def user_dashboard(user_id):
    while True:
        print("\nUser Dashboard")
        print("1. View Ticket Options")
        print("2. Book a Ticket")
        print("3. View My Bookings")
        print("4. Cancel a Booking")
        print("5. Logout")
        choice = input("Choose an option: ")
        if choice == "1":
            view_ticket_options()
        elif choice == "2":
            book_ticket(user_id)
        elif choice == "3":
            view_bookings(user_id)
        elif choice == "4":
            cancel_booking(user_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def view_ticket_options():
    print("\nAvailable Ticket Options:")
    query = "SELECT * FROM Shows"
    shows = execute_query(query, fetch=True)
    for show in shows:
        print(f"Show ID: {show[0]}, Name: {show[1]}, Date: {show[2]}, Time: {show[3]}, Price: {show[4]}")

def book_ticket(user_id):
    ticket_id = int(input("Enter show ID: "))
    num_tickets = int(input("Enter number of tickets: "))
    query = "INSERT INTO Bookings (user_id, ticket_id, num_tickets) VALUES (%s, %s, %s)"
    execute_query(query, (user_id, ticket_id, num_tickets))
    print("Booking successful!")

def view_bookings(user_id):
    query = "SELECT * FROM Bookings WHERE user_id=%s"
    bookings = execute_query(query, (user_id,), fetch=True)
    for booking in bookings:
        print(f"Booking ID: {booking[0]}, Ticket ID: {booking[1]}, Number of Tickets: {booking[3]}")

def cancel_booking(user_id):
    booking_id = int(input("Enter booking ID to cancel: "))
    query = "DELETE FROM Bookings WHERE booking_id=%s AND user_id=%s"
    execute_query(query, (booking_id, user_id))
    print("Booking canceled!")

def operator_dashboard():
    while True:
        print("\nOperator Dashboard")
        print("1. Add Ticket Option")
        print("2. View All Bookings")
        print("3. Edit or Delete Booking")
        print("4. Logout")
        choice = input("Choose an option: ")
        if choice == "1":
            add_ticket_option()
        elif choice == "2":
            view_all_bookings()
        elif choice == "3":
            manage_booking()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def add_ticket_option():
    name = input("Enter show name: ")
    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM:SS): ")
    price = float(input("Enter price: "))
    query = "INSERT INTO Shows (name, date, time, price) VALUES (%s, %s, %s, %s)"
    execute_query(query, (name, date, time, price))
    print("Show added successfully!")

def view_all_bookings():
    query = "SELECT * FROM Bookings"
    bookings = execute_query(query, fetch=True)
    for booking in bookings:
        print(booking)

def manage_booking():
    booking_id = int(input("Enter booking ID to manage: "))
    action = input("Enter action (Edit/Delete): ").capitalize()
    if action == "Edit":
        num_tickets = int(input("Enter new number of tickets: "))
        query = "UPDATE Bookings SET num_tickets=%s WHERE booking_id=%s"
        execute_query(query, (num_tickets, booking_id))
        print("Booking updated successfully!")
    elif action == "Delete":
        query = "DELETE FROM Bookings WHERE booking_id=%s"
        execute_query(query, (booking_id,))
        print("Booking deleted successfully!")
    else:
        print("Invalid action.")

print("Welcome to Ticket Booking System")
while True:
    print("\n1. User Login")
    print("2. Sign Up")
    print("3. Operator Dashboard")
    print("4. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        user_login()
    elif choice == '2':
        user_signup()
    elif choice == "3":
        operator_dashboard()
    elif choice == "4":
        print("Thank you for using SPOTsPLUS!")
        break
    else:
        print("Invalid choice. Try again.")