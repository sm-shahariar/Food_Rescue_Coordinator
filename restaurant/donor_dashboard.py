from connection.config import Database
import mysql.connector

class DonorDashboard:

    def  __init__(self, resturant_id):
        self.resturant_id = resturant_id

    def index(self):

        while True:

            print("\n================ Restaurant Dashboard ================")
            print("\n1. View All Food")
            print("2. Add Food")
            print("3. Update Food")
            print("4. Delete Food")
            print("5. Back to main menu")

            choice = input("\nSelect option: ")

            if choice == "1":
                self.view()
            elif choice == "2":
                self.store()
            elif choice == "3":
                print("Update Food - Coming Up Soon")
            elif choice == "4":
                print("Delete Food - Coming Up Soon")
            elif choice == "5":
                print("\nBack to main menu...")
                break
            else:
                print("Invalid option! Try again.")


    def view(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                query = """
                        SELECT id, food_name, quantity, remaining_qty, status 
                        FROM food_donations WHERE resturant_id = %s ORDER BY id DESC
                    """

                cursor.execute(query, (self.resturant_id,))
                foods = cursor.fetchall()

                print("\n================== My Food Donations =================")

                if foods:
                    print("-" * 85)

                    print(
                        f"{'ID':<6}"
                        f"{'Food Name':<22}"
                        f"{'Quantity':<12}"
                        f"{'Remaining':<15}"
                        f"{'Status':<15}"
                    )

                    print("-" * 85)   #  _

                    for food in foods:
                        food_id, food_name, qty, remaining_qty, status = food
                        print(
                            f"{food_id:<6}"
                            f"{food_name:<22}"
                            f"{qty:<12}"
                            f"{remaining_qty:<15}"
                            f"{status:<15}"
                        )

                    print("-" * 85)

                else:
                    print("\nNo Food Donation Found!")
                    
                input("\nPress Enter to continue...")

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()

    def store(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                print("============== Add Food =============")
                food_name = input("Enter food name: ")

                try:
                    quantity = int(input("Enter quantity: "))

                    if quantity <= 0:
                        print("Quantity must be grather than 0")
                        return

                except ValueError:
                    print("Please enter a valid quantity!")
                    return

                status = input("Enter status: ")

                query = """
                        INSERT INTO food_donations(resturant_id, food_name, quantity, remaining_qty, status) VALUES
                        (%s, %s, %s, %s, %s)
                    """
                
                values = (self.resturant_id, food_name, quantity, quantity, status)

                cursor.execute(query, values)
                db.commit()

                print("\nFood added successfully!")
                

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()
        

# _
