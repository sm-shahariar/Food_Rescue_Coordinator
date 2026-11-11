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
                self.update()
            elif choice == "4":
                self.delete()
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


    def update(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                print("\n================== Update Food =================")

                try:
                    food_id = int(input("\nEnter Food Id: "))
                except ValueError:
                    print("Please enter a valid Food Id!")
                    return

                query = """
                        SELECT id, food_name, quantity, remaining_qty, status FROM 
                        food_donations WHERE id = %s AND resturant_id = %s
                    """

                cursor.execute(query, (food_id, self.resturant_id))
                food = cursor.fetchone()

                if not food:
                    print("Food not found!")
                    return

                food_id, food_name, quantity, remaining_qty, status = food

                print("\n========== Current Food Information ==========")
                print(f"Food Name: {food_name}")
                print(f"Quantity: {quantity}")
                print(f"Remaining Quantity: {remaining_qty}")
                print(f"Status: {status}")

                print("\n========== Enter New Information ==========")

                new_name = input(f"Enter new name [{food_name}]: ")

                if new_name == "":
                    new_name = food_name

                new_qty = input(f"Enter new quantity [{quantity}]: ")

                if new_qty == "":
                    new_qty = quantity
                else:
                    try:
                        new_qty = int(new_qty)

                        if new_qty <= 0:
                            print("Quantity must be grather than 0")
                            return
                    except ValueError:
                        print("Please enter a valid quantity!")
                        return
                    

                new_remaining = input(f"Enter remaining quantity [{remaining_qty}]: ")

                if new_remaining == "":
                    new_remaining = remaining_qty

                try:
                    new_remaining = int(remaining_qty)

                    if new_remaining < 0:
                        print("Remaining quantity cannot be negative!")
                        return
                except ValueError:
                    print("Please enter a valid remaining quantity!")

                new_status = input(f"Enter status [{status}]: ")

                if new_status == "":
                    new_status = status

                if new_remaining > new_qty:
                    print("Reamining quantity cannot exceed total quantity!")
                    return

                update_query = """
                                UPDATE food_donations SET food_name = %s, quantity = %s, remaining_qty = %s,
                                status = %s WHERE id = %s AND resturant_id = %s
                            """

                values = (new_name, new_qty, new_remaining, new_status, food_id, self.resturant_id)

                cursor.execute(update_query, values)

                db.commit()

                print("Food Updated Successfully!")

        except mysql.connector.Error as err:
            print(err)

            if db:
                db.rollback()

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()

                
    # Food Delete Method

    def delete(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                print("\n================== Food Delete ===================")

                food_name = input("Enter Food Name: ")

                if not food_name:
                    print("Food name cannot be empty!")
                    return
                
                query = """
                        SELECT id, food_name, quantity, remaining_qty, status
                        FROM food_donations
                        WHERE food_name = %s AND resturant_id = %s
                    """

                cursor.execute(query, (food_name, self.resturant_id))
                foods = cursor.fetchall()

                if not foods:
                    print("Food not found!")
                    return

                print("\n========== Matching Food Information ==========")

                print("-" * 75)
                print(
                    f"{'ID':<8}"
                    f"{'Food Name':<20}"
                    f"{'Quantity':<12}"
                    f"{'Remaining':<15}"
                    f"{'Status':<15}"
                )
                print("-" * 75)

                for food in foods:
                    food_id, name, quantity, remaining_qty, status = food
                    print(
                    f"{food_id:<8}"
                    f"{name:<20}"
                    f"{quantity:<12}"
                    f"{remaining_qty:<15}"
                    f"{status:<15}")

                print("-" * 75)

                try:
                    food_id = int(input("\nEnter the ID of the food you want to delete: "))
                except ValueError:
                    print("\nPlease enter a valid Food ID!")
                    return
                
                selected_food = None

                for food in foods:
                    if food[0] == food_id:
                        selected_food = food
                        break

                if not selected_food:
                    print("Invalid Food Id!")
                    return

                food_id, food_name, quantity, remaining_qty, status = selected_food


                print("\n========== Food Information ==========")

                print(f"Food ID: {food_id}")
                print(f"Food Name: {food_name}")
                print(f"Quantity: {quantity}")
                print(f"Remaining Quantity: {remaining_qty}")
                print(f"Status: {status}")

                confirm = input("\nAre you sure you want to delete this food? (yes/no): ").strip().lower()

                if confirm == "yes":

                    delete_query = """
                        DELETE FROM food_donations
                        WHERE id = %s AND resturant_id = %s
                    """
                    cursor.execute(delete_query, (food_id, self.resturant_id))
                    db.commit()

                    print("Food deleted successfully!")

                else:
                    print("Food deletion cancelled")

        except mysql.connector.Error as err:
            print(err)

            if db:
                db.rollback()

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()



    # _
