from config import Database
import mysql.connector

class FoodDonationTable:
    def create_table(self):
        db = None

        try:
            db = Database.connect()

            if db.is_connected():
                db.cmd_query("USE food_rescue")

                db.cmd_query("""
                        CREATE Table food_dinations(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            resturant_id INT,
                            FOREIGN KEY (resturant_id) REFERENCES users(id),
                            food_name VARCHAR(80) NOT NULL,
                            quantity INT(3) NOT NULL,
                            remaining_qty INT(3) NOT NULL,
                            status TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )   
                    """)

                print("Food Donations Table Create Successfully!")

        except mysql.connector.Error as err:
            print(err)

        finally:
            db.close()

food_donations_table = FoodDonationTable()
food_donations_table.create_table()