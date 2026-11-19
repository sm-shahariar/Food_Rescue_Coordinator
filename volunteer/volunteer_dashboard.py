from connection.config import Database
import mysql.connector

class VolunteerDashboard:

    def __init__(self, volunteer_id):
        self.volunteer_id = volunteer_id

    def index(self):
        while True:
            print("\n ======================== Volunteer Dashboard =======================")
            print("\n1. View Nearby Donor Resturants")
            print("2. View Available Foods")
            print("3. Send Food Collection Request")
            print("4. View My Requests")
            print("5. Update Collection Status")
            print("6. Give Rating & Feedback")
            print("7. Back to Main Menu")

            choice = int(input("\n Select Options: "))

            if choice == 1:
                self.nearbyResturant()

            elif choice == 2:
                self.viewFoods()

            elif choice == 3:
                self.sendRequest()
                # print("Coming soon")

            elif choice == 4:
                # self.viewRequest()
                print("Coming soon")

            elif choice == 5:
                # self.updateStatus()
                print("Coming soon")

            elif choice == 6:
                # self.rating()
                print("Coming soon")

            elif choice == 7:
                break

            else:
                print("Invalid Option! Try Again")


    # Nearby Resturant

    def nearbyResturant(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                # location query
                location_query = """ 
                        SELECT latitude, longitude FROM users
                        WHERE id = %s AND role = 'volunteer'
                """

                cursor.execute(location_query, (self.volunteer_id,))
                location = cursor.fetchone()

                if not location or location[0] is None or location[1] is None:
                    print(
                        "\nYour location coordinates are not available. "
                        "Please update your address location first.")
                    return

                latitude, longitude = location

                # Find nearby donor returant
                query = """
                    SELECT u.id, u.name, u.address,
                    (
                        6371 * ACOS(
                            LEAST(1, GREATEST(-1,
                                COS(RADIANS(%s))
                                * COS(RADIANS(u.latitude))
                                * COS(RADIANS(u.longitude) - RADIANS(%s))
                                + SIN(RADIANS(%s))
                                * SIN(RADIANS(u.latitude))))
                            )
                    ) AS distance

                    FROM users AS u WHERE u.role = 'donor' AND u.latitude IS NOT NULL
                    AND u.longitude IS NOT NULL HAVING distance <= 5 ORDER BY distance ASC
                """

                cursor.execute(query, (latitude, longitude, latitude))

                resturants = cursor.fetchall()


                print("\n ========================= Nearby Resturant (5 KM) =========================")

                if not resturants:
                    print("No nearby resturant found!")
                    return

                print("-" * 80)

                for resturant in resturants:
                    donor_id, name, address, distance = resturant

                    print(f"\nRestaurant ID: {donor_id}")
                    print(f"Restaurant Name: {name}")
                    print(f"Address: {address}")
                    print(f"Distance: {distance:.2f} KM")

                    print("-" * 80)

                input("\nPress Enter to continue....")

        except mysql.connector.Error as err:
            print("Database error:", err)

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()


    # View Available Food

    def viewFoods(self):
        db = None
        cursor = None

        try:
            db = Database.connect()
            cursor = db.cursor()

            if db.is_connected():

                location_query = """
                    SELECT latitude, longitude
                    FROM users
                    WHERE id = %s
                """

                cursor.execute(location_query, (self.volunteer_id,))
                location = cursor.fetchone()

                if not location or location[0] is None or location[1] is None:
                    print("\nYour location is not available!")
                    return

                latitude, longitude = location

                query = """
                    SELECT f.id, u.name, u.address, f.food_name, f.remaining_qty,
                    (
                        6371 * ACOS(
                            LEAST(1, GREATEST(-1,
                                COS(RADIANS(%s))
                                * COS(RADIANS(u.latitude))
                                * COS(RADIANS(u.longitude) - RADIANS(%s))
                                + SIN(RADIANS(%s))
                                * SIN(RADIANS(u.latitude))))
                            )
                    ) AS distance

                    FROM food_donations AS f JOIN users u ON f.resturant_id = u.id
                    WHERE f.status = 'available' AND f.remaining_qty > 0 AND 
                    u.latitude IS NOT NULL AND u.longitude IS NOT NULL HAVING
                    distance <= 5 ORDER BY distance ASC
                """

                cursor.execute(query,(latitude, longitude, latitude))
                foods = cursor.fetchall()

                print("\n================ Nearby Available Foods ================")

                if not foods:
                    print("\nNo available foods found nearby!")
                    return

                for food in foods:

                    food_id, donor, address, name, quantity, distance = food

                    print(f"\nFood ID: {food_id}")
                    print(f"Restaurant: {donor}")
                    print(f"Address: {address}")
                    print(f"Food Name: {name}")
                    print(f"Available Quantity: {quantity}")
                    print(f"Distance: {distance:.2f} KM")

                    print("-" * 60)


                input("\n Press Enter to continue....")

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()


    # Send Collection Request

    def sendRequest(self):
        db = None
        cursor = None

        try:
            # Nearby Available Food
            self.viewFoods()

            db = Database.connect()

            print("\n========================== Send Food Request =======================")

            if db.is_connected():
                cursor = db.cursor()

                try:
                    donation_id = int(input("\nEnter Food ID: "))

                    if donation_id <= 0:
                        print("Invalid Food ID!")
                        return

                except ValueError:
                    print("Please enter a valid food ID!")
                    return


                query = """
                        SELECT id, resturant_id, food_name, quantity FROM food_donations WHERE id = %s AND
                        status = 'available' AND remaining_qty > 0
                    """

                cursor.execute(query, (donation_id,))
                food = cursor.fetchone()

                if not food:
                    print("\nFood not available!")
                    return

                food_id, donor_id, food_name, remaining_qty = food

                print(f"Food name: {food_name}")
                print(f"Available quantity: {remaining_qty}")

                try:
                    request_qty = int(input("\nEnter Request Quantity: "))

                    if remaining_qty <= 0 or request_qty > remaining_qty:
                        print("Invalid request quantity!")
                        return
                except ValueError:
                    print("Please enter a valid quantity!")
                    return

                # Confirm the donor is within 5 KM
                location_query = """SELECT latitude, longitude FROM users WHERE id = %s"""
                cursor.execute(location_query, (self.volunteer_id,))
                volunteer_location = cursor.fetchone()

                donor_location_query = """SELECT latitude, longitude FROM users WHERE id = %s AND role = 'donor' """
                cursor.execute(donor_location_query, (donor_id,))
                donor_location = cursor.fetchone()

                if not volunteer_location or not donor_location or None in volunteer_location or None in donor_location:
                    print("Location information is incomplete!")
                    return

                lat1, lon1 = volunteer_location
                lat2, lon2 = donor_location

                distance_query = """
                    SELECT
                        6371 * ACOS(
                            LEAST(1, GREATEST(-1,
                                COS(RADIANS(%s))
                                * COS(RADIANS(%s))
                                * COS(RADIANS(%s) - RADIANS(%s))
                                + SIN(RADIANS(%s))
                                * SIN(RADIANS(%s))
                            ))
                        )"""

                cursor.execute(distance_query, (lat1, lat2, lon2, lon1, lat1, lat2))
                distance = cursor.fetchone()[0]

                if distance > 5:
                    print("This rasturant is outside your 5 KM radius!")
                    return

                insert_query = """INSERT INTO volunteer_request_collections 
                    (volunteer_id, donor_id, donation_id, request_qty) VALUES(%s, %s, %s, %s)"""

                values = (self.volunteer_id, donor_id, donation_id, request_qty)
                cursor.execute(insert_query, values)
                db.commit()

                print("\nFood Collection Request Sent Successfully!")
                print("Waiting for Donor Approval....")

        except mysql.connector.Error as err:
            print("Database error:", err)

            if db:
                db.rollback()

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()

    #   _ 