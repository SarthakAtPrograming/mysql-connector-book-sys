import mysql.connector
def connect_to_server():
    return mysql.connector.connect(
        user="root",
        password="9693",
        host="localhost")
def create_database():
    conn = connect_to_server()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS spotsplus")
    print("Database 'spotsplus' created or already exists.")
    cursor.close()
    conn.close()
def connect_to_database():
    return mysql.connector.connect(
        user="root",  
        password="9693",
        host="localhost",
        database="spotsplus")
def create_tables():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password1 VARCHAR(100) NOT NULL
        )
        """
        )
    print("Table 'Users' created or already exists.")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Shows (
            show_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
        """
    )
    print("Table 'Shows' created or already exists.")

    # Create Bookings table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            ticket_id INT NOT NULL,
            num_tickets INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (ticket_id) REFERENCES Shows(show_id) ON DELETE CASCADE
        )
        """
    )
    print("Table 'Bookings' created or already exists.")
    conn.commit()
    cursor.close()
    conn.close()
if __name__ == "__main__":
    print("Setting up the database...")
    create_database()
    create_tables()
    print("Database and tables are set up successfully!")
