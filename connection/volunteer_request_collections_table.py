from config import Database
import mysql.connector

class VolunteerRequestCollectionTable:

    def create_table(self):
        db = None

        try:

            db = Database.connect()

            if db.is_connected():
                db.cmd_query("USE food_rescue")

                db.cmd_query("""
                        CREATE Table volunteer_request_collections(
                            id INT AUTO_INCREMENT PRIMARY KEY ,
                            volunteer_id INT NOT NULL,
                            donor_id INT NOT NULL,
                            request_qty INT NOT NULL, 
                            status ENUM(
                                'pending',
                                'accepted',
                                'rejected',
                                'picked_up',
                                'completed',
                                'cancelled'
                            ) DEFAULT 'pending',

                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                            FOREIGN KEY (volunteer_id) REFERENCES users(id),

                            FOREIGN KEY (donor_id) REFERENCES users(id))

                    """)
                                
                print("Volunteer Request Collection Table Create Successfully!")
        except mysql.connector.Error as err:
                    print(err)
        
        finally:
            db.close()

volunteer_request_collection_table = VolunteerRequestCollectionTable()
volunteer_request_collection_table.create_table()