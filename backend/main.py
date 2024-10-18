import sqlite3
from datetime import datetime

class RoleSystem:
    def __init__(self):
        self.conn = sqlite3.connect('role_system.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.current_user_id = None
        self.current_user_role = None

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                added_by INTEGER,
                added_on DATETIME,
                FOREIGN KEY (added_by) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password, role):
        try:
            self.cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                                (username, password, role))
            self.conn.commit()
            print(f"User {username} added successfully as {role}")
        except sqlite3.IntegrityError:
            print(f"User {username} already exists")

    def add_faculty(self, username, password):
        if self.current_user_role == 'admin':
            self.add_user(username, password, 'faculty')
        else:
            print("Only administrators can add faculty members")

    def add_client(self, name, email):
        if self.current_user_role == 'faculty':
            self.cursor.execute('''
                INSERT INTO clients (name, email, added_by, added_on)
                VALUES (?, ?, ?, ?)
            ''', (name, email, self.current_user_id, datetime.now()))
            self.conn.commit()
            print(f"Client {name} added successfully")
        else:
            print("Only faculty members can add clients")

    def login(self, username, password):
        self.cursor.execute('SELECT id, role FROM users WHERE username = ? AND password = ?',
                            (username, password))
        user = self.cursor.fetchone()
        if user:
            self.current_user_id, self.current_user_role = user
            print(f"Logged in as {username} ({self.current_user_role})")
            return True
        else:
            print("Invalid username or password")
            return False

    def logout(self):
        self.current_user_id = None
        self.current_user_role = None
        print("Logged out successfully")

    def view_clients(self):
        if self.current_user_role in ['admin', 'faculty']:
            self.cursor.execute('''
                SELECT c.name, c.email, u.username, c.added_on
                FROM clients c
                JOIN users u ON c.added_by = u.id
            ''')
            clients = self.cursor.fetchall()
            if clients:
                print("Client List:")
                for client in clients:
                    print(f"Name: {client[0]}, Email: {client[1]}, Added by: {client[2]}, Added on: {client[3]}")
            else:
                print("No clients found")
        else:
            print("You don't have permission to view clients")

    def close(self):
        self.conn.close()

def main():
    system = RoleSystem()

    # Add initial admin user if not exists
    system.add_user('admin', 'adminpass', 'admin')

    while True:
        print("\n--- Role System Menu ---")
        print("1. Login")
        print("2. Logout")
        print("3. Add Faculty (Admin only)")
        print("4. Add Client (Faculty only)")
        print("5. View Clients")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            system.login(username, password)
        elif choice == '2':
            system.logout()
        elif choice == '3':
            if system.current_user_role == 'admin':
                username = input("Enter new faculty username: ")
                password = input("Enter new faculty password: ")
                system.add_faculty(username, password)
            else:
                print("You must be logged in as an admin to add faculty.")
        elif choice == '4':
            if system.current_user_role == 'faculty':
                name = input("Enter client name: ")
                email = input("Enter client email: ")
                system.add_client(name, email)
            else:
                print("You must be logged in as faculty to add clients.")
        elif choice == '5':
            system.view_clients()
        elif choice == '6':
            print("Exiting the system. Goodbye!")
            system.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()