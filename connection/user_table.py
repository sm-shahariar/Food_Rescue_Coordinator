from config import Database
import mysql.connector

class CreateUserTable:

    def create_table(self):
        db = None

        try:
            db = Database.connect()

            if db.is_connected():
                db.cmd_query("USE food_rescue")

                db.cmd_query("""
                    CREATE Table users(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        email VARCHAR(50) NOT NULL UNIQUE,
                        phone VARCHAR(15) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        role ENUM('super_admin', 'donor', 'volunteer') NOT NULL DEFAULT 'volunteer',
                        address TEXT NOT NULL,
                        latitude DECIMAL(10, 8) DEFAULT NULL,
                        longitude DECIMAL(11, 8) DEFAULT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                print("User Table Created Successfully")

        except mysql.connector.Error as err:
            print(err)

        finally:
            db.close()

user_table = CreateUserTable()
user_table.create_table()