from connection.config import Database
from auth.password import Password
import mysql.connector

class Registration:

    def register(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                print("\n========== USER REGISTRATION ==========")
                name = input("Enter Name: ")
                email = input("Enter Email: ").strip()
                password = input("Enter Password: ")
                phone = input("Enter phone: ")
                address = input("Enter address: ")

                print("\n1. Admin")
                print("2. Donor")
                print("3. Receiver")

                choice = input("Select role: ")

                if choice == "1":
                    role = "admin"
                elif choice == "2":
                    role = "donor"
                elif choice == "3":
                    role = "receiver"
                else:
                    print("This type role not exists")

                if len(password) < 8:
                    print("Password must be at least 8 characters")
                    return

                hash_pass = Password.hash_password(password)

                query = """
                            INSERT INTO users(name, email, phone, password, address, role) VALUES 
                            (%s, %s, %s, %s, %s, %s)
                        """

                values = (name, email, phone, hash_pass, address, role)

                cursor.execute(query, values)
                db.commit()

                print("\n Registration Successful!")

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()