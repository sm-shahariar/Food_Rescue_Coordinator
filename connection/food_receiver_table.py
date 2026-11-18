from config import Database
import mysql.connector

class FoodReceiverTable:

    def craete_table(self):
        db = None

        try:

            db = Database.connect()

            if db.is_connected():
                db.cmd_query("USE food_rescue")

                db.cmd_query("""
                        CREATE Table food_receiver(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            request_qty INT NOT NULL,
                            volunteer_id INT,
                            FOREIGN KEY(volunteer_id) REFERENCES users(id),
                            donation_id INT,
                            FOREIGN KEY(donation_id) REFERENCES food_donations(id),
                            status ENUM('pending', 'accepted', 'rejected', 'completed') DEFAULT 'pending',
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                """)

                print("Food Receiver Table Created Successfully!")

        except mysql.connector.Error as err:
            print(err)

        finally:
            db.close()

food_receiver_table = FoodReceiverTable()
food_receiver_table.craete_table()