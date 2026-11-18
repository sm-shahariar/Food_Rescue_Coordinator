from config import Database
import mysql.connector

class FoodRatingTable:

    def create_table(self):
        db = None

        try:

            db = Database.connect()

            if db.is_connected():
                db.cmd_query("USE food_rescue")

                db.cmd_query("""
                        CREATE Table volunteer_request_collections(
                            id INT AUTO_INCREMENT PRIMARY KEY ,
                            request_id INT NOT NULL UNIQUE,
                            volunteer_id INT NOT NULL,
                            donor_id INT NOT NULL,
                            rating TINYINT NOT NULL,
                            feedback TEXT,
                            
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (volunteer_id)
                                REFERENCES users(id),

                            FOREIGN KEY (donor_id)
                                REFERENCES users(id),

                            FOREIGN KEY (donation_id)
                                REFERENCES food_donations(id),

                            CHECK (rating BETWEEN 1 AND 5)
                        )
                    """)
                                
                print("Volunteer Request Collection Table Create Successfully!")
                
        except mysql.connector.Error as err:
                    print(err)
        
        finally:
            db.close()

volunteer_request_collection_table = VolunteerRequestCollectionTable()
volunteer_request_collection_table.create_table()