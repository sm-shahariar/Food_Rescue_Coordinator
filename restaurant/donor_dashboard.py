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
            print("5. View Collecton Request")
            print("6. Back to main menu")

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
                self.view_requests()
            elif choice == "6":
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

                new_status = input(f"Enter status [{status}] (available/unavailable): ")

                if new_status in ('available/unavailable') or new_status == "":
                    new_status = status
                else:
                    print("\nInvalid status!")
                    return

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

    
    def view_requests(self):

        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                query = """
                        SELECT r.id, u.name, f.food_name, r.request_qty, r.status
                        FROM volunteer_request_collections r 
                        JOIN users u ON r.volunteer_id = u.id
                        JOIN food_donations f ON r.donaton_id = f.id
                        WHERE r.donor_id = %s ORDER BY r.id DESC
                    """ 

                cursor.execute(query, (self.resturant_id))
                requests = cursor.fetchall()

                print("\n=========================== Collection Requests ========================")

                if not requests:
                    print("\nNo Collection Request Found!")
                    return

                for request in requests:
                    print(
                        f"\nRequest ID: {request[0]}"
                        f"\nVolunteer: {request[1]}"
                        f"\nFood: {request[2]}"
                        f"\nRequested Quantity: {request[3]}"
                        f"\nStatus: {request[4]}"
                    )
                    print("-" * 55)

                try:
                    request_id = int(input("\n Enter Request ID to respond(0 to back): "))
                except ValueError:
                    print("\nInvalid Request ID!")
                    return

                if request_id == 0:
                    return

                self.repond_request(request_id)

        except mysql.connector.Error as err:
           print("Database err:", err)

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()


    # Accept Or Reject Request

    def respond_request(self, request_id):
        db = None
        cursor = None

        try:
            db = Database.connect()
            db.start_transaction()
            cursor = db.cursor()

            query = """
                SELECT id, donation_id, request_qty, status
                FROM volunteer_collection_requests
                WHERE id = %s AND donor_id = %s
                FOR UPDATE
            """

            cursor.execute(query, (request_id, self.resturant_id))
            request = cursor.fetchone()

            if not request:
                print("Request not found!")
                db.rollback()
                return

            req_id, donation_id, request_qty, status = request

            if status != "pending":
                print("This request has already been processed!")
                db.rollback()
                return

            print("\n1. Accept")
            print("2. Reject")

            choice = input("Select option: ")

            if choice == "1":

                food_query = """
                    SELECT remaining_qty
                    FROM food_donations
                    WHERE id = %s AND resturant_id = %s
                    FOR UPDATE
                """

                cursor.execute(
                    food_query,
                    (donation_id, self.resturant_id))

                food = cursor.fetchone()

                if not food or food[0] < request_qty:
                    print("Not enough food available!")
                    db.rollback()
                    return

                remaining = food[0] - request_qty

                food_update = """
                    UPDATE food_donations
                    SET remaining_qty = %s,
                        status = %s
                    WHERE id = %s AND resturant_id = %s
                """

                if remaining > 0:
                    food_status = 'available'
                else:
                    food_status = 'unavailable'

                cursor.execute(
                    food_update,
                    (remaining, food_status, donation_id, self.resturant_id))

                new_status = 'accepted'

            elif choice == "2":
                new_status = 'rejected'

            else:
                print("\n Invalid option!")
                db.rollback()
                return

            
            update_query = """
                UPDATE volunteer_collection_requests
                SET status = %s
                WHERE id = %s AND donor_id = %s
            """

            cursor.execute(
                update_query,
                (new_status, request_id, self.resturant_id))

            db.commit()

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
