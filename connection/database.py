from config import Database
import mysql.connector

class CreateDatabase:    
    def create_database(self):
        db = None

        try:
            db = Database.connect()

            if db.is_connected():
                db.cmd_query("CREATE DATABASE food_rescue")
                print("Database Created Successfully")

        except mysql.connector.Error as err:
            print(err)

        finally:
            db.close()

database = CreateDatabase()
database.create_database()