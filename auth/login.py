from connection.config import Database
from auth.password import Password
import mysql.connector

class Login:
    def login(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            print("\n========== USER LOGIN ==========")

            if db.is_connected():
                cursor = db.cursor()

                email = input("Enter email: ").strip()
                password = input("Enter password: ")

                query = """
                        SELECT id, name, email, phone, password, role
                        FROM users WHERE email = %s
                    """

                values = (email,)

                cursor.execute(query, values)

                user = cursor.fetchone()

                if user:
                    user_id, name, email,phone, stored_pass, role = user

                    if Password.verify_pass(password, stored_pass):
                        print("\nLogin Successful!")
                        print(f"Welcome, {name}")


                        return {
                            'id': user_id,
                            'name': name,
                            'email': email,
                            'phone': phone,
                            'role': role
                        }
                    else:
                        print("Invalid email or password")
                else:
                    print("Invalid email or password")

            return None

        except mysql.connector.Error as err:
            print(err)
            return None

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()