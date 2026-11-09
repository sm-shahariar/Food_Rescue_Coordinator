import mysql.connector

class Database:

    @staticmethod
    def connect():   
        return mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "food_rescue"
        )