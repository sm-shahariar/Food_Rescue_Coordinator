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

            elif choice == 4:
                self.viewRequest()

            elif choice == 5:
                self.updateStatus()

            elif choice == 6:
                self.rating()

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



    # View My Request
    def viewRequest(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                query = """
                        SELECT r.id, u.name, f.food_name, r.request_qty, r.status
                        FROM volunteer_request_collections r JOIN users u ON r.donor_id = u.id
                        JOIN food_donations f ON r.donation_id = f.id WHERE r.volunteer_id = %s
                        ORDER BY r.id DESC
                """

                cursor.execute(query,(self.volunteer_id,))
                requests = cursor.fetchall()

                print("\n======================= My Collection Requests =======================")

                if not requests:
                    print("No Request Found!")
                    return

                for request in requests:
                    request_id, donor, food, qty,status = request
                    print(f"\nRequest ID: {request_id}")
                    print(f"Restaurant: {donor}")
                    print(f"Food Name: {food}")
                    print(f"Requested Quantity: {qty}")
                    print(f"Status: {status}")

                    print("-" * 55)

                input("\nPress enter to be continue....")

        except mysql.connector.Error as err:
            print("Database error:", err)   

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected:
                db.close()


    # Update Collection Status

    def updateStatus(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            print("\n========================= Update Collection Status =======================")

            if db.is_connected:
                cursor = db.cursor()

                query = """
                    SELECT r.id, f.food_name, u.name, r.request_qty, r.status
                    FROM volunteer_request_collections r JOIN food_donations f ON r.donation_id = f.id
                    JOIN users u ON r.donor_id = u.id WHERE volunteer_id = %s AND r.status IN 
                    ('accepted', 'picked_up') ORDER BY r.id DESC
                """

                cursor.execute(query, (self.volunteer_id,))
                requests = cursor.fetchall()

                if not requests:
                    print("\nNo collection request available!")
                    return

                # Display request
                print("\n======================== My Collection Requests ========================")

                print("-" * 85)
                print(
                    f"{'No.':<6}"
                    f"{'Food Name':<22}"
                    f"{'Restaurant':<22}"
                    f"{'Quantity':<12}"
                    f"{'Status':<15}"
                )
                print("-" * 85)

                for index, request in enumerate(requests, start=1):
                    req_id, food_name, resturant, req_qty, status = request
                    print(
                        f"{index:<6}"
                        f"{food_name:<22}"
                        f"{resturant:<22}"
                        f"{req_qty:<12}"
                        f"{status:<15}"
                    )

                print("-" * 85)

                food_name = input("\nSelect Food Name: ")

                if not food_name:
                    print("\nFood name cannot be empty!")
                    return

                matched_requests = [
                    request for request in requests
                    if request[1].lower() == food_name.lower()
                ]

                if not matched_requests:
                    print("\nFood cannot found in your collection requests!")
                    return

                if len(matched_requests) == 1:
                    select_req = matched_requests[0]
                    req_id = select_req[0]
                    curr_status = select_req[4]
                else:

                    print("\nMultiple request found for this food!")

                    print("-" * 75)
                    print(
                        f"{'No.':<6}"
                        f"{'Food Name':<20}"
                        f"{'Restaurant':<22}"
                        f"{'Quantity':<12}"
                        f"{'Status':<15}"
                    )
                    print("-" * 75)

                    for index, request in enumerate(requests, start=1):
                        print(
                            f"{index:<6}"
                            f"{request[1]:<20}"
                            f"{request[2]:<22}"
                            f"{request[3]:<12}"
                            f"{request[4]:<15}"
                        )

                    print("-" * 75)

                    try:
                        choice = int(input("\nSelect Request: "))

                        if choice < 1 or choice > len(matched_requests):
                            print("\nInvalid Option!")
                            return
                    except ValueError:
                        print("Please input a valid option!")
                        return

                    select_req = matched_requests[choice - 1]
                    req_id = select_req[0]
                    curr_status = select_req[4]


                # Determine new status
                if curr_status == 'accepted':
                    new_status = 'picked_up'

                elif curr_status == 'picked_up':
                    new_status = 'completed'

                else:
                    print("\nInvalid request status!")
                    return

                # Confirm Status Update
                print("\nSelected Food:", select_req[1])
                print("Restaurant:", select_req[2])
                print("Current Status:", curr_status)
                print("New Status:", new_status)


                confirm = input("\nConfirm status update? (y/n): ").strip().lower()

                if confirm != 'y':
                    print("\nStatus update cancelled!")
                    return

                # Update collection request status query

                update_query = """
                        UPDATE volunteer_request_collections SET status = %s WHERE id = %s
                        AND volunteer_id = %s AND status = %s
                """

                values = (new_status, req_id, self.volunteer_id, curr_status)

                cursor.execute(update_query, values)

                if cursor.rowcount == 0:
                    print("\nRequest status could not be updated!")
                    db.rollback()
                    return

                db.commit()

                print("\nCollection Status Updated Successfully!")
                print("Food Name:", select_req[1])
                print("New Status:", new_status)


                if new_status == 'picked_up':
                    print("\nYou can now collect the food from the resturant!")

                elif new_status == 'completed':
                    print("\nFood collection process completed successfully!")

        except mysql.connector.Error as err:
            print("Database error:", err)

            if db:
                db.rollback()

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected:
                db.close()


    # Rating and Feedback

    def rating(self):
        db = None
        cursor = None

        try:
            db = Database.connect()

            if db.is_connected():
                cursor = db.cursor()

                print("\n====================== Resturant Rating =========================")

                query = """
                    SELECT DISTINCT u.id, u.name FROM volunteer_request_collections r JOIN users u
                    ON r.donor_id = u.id WHERE r.volunteer_id = %s AND r.status = 'completed'
                    AND NOT EXISTS (SELECT 1 FROM resturant_ratings rr WHERE rr.request_id = r.id)
                """

                cursor.execute(query, (self.volunteer_id,))
                resturants = cursor.fetchall()

                if not resturants:
                    print("\nNo unrated completed resturant found!")
                    return

                # Check available resturan
                check_available_resturant = resturants


                # Display resturants
                print("\n============================= Restuarnts Available for Rating ============================")

                print("-" * 55)
                print(f"{'No.':<8}{'Resturant Name':<30}")
                print("-" * 55)

                for index, resturant in enumerate(check_available_resturant, start=1):
                    print(
                        f"{index:<8}"
                        f"{resturant[1]:<30}"
                    )

                print("-" * 55)


                resturant_name = input("\nEnter Resturant Name: ")

                matched_resturants = [
                    resturant for resturant in check_available_resturant
                    if resturant[1].lower() == resturant_name.lower()]

                if not matched_resturants:
                    print("\nResturant not found!")
                    return

                if len(matched_resturants) > 1:
                    print("\nMultiple resturant found with same name.")

                    for index, resturant in enumerate(matched_resturants, start=1):
                        print(f"{index}. {resturant[1]} (ID: {resturant[0]})")

                    choice = int(input("\nSelect Resturant: "))

                    if choice < 1 or choice > len(matched_resturants):
                        print("\nInvalid option!")
                        return

                    selected_resturant = matched_resturants[choice - 1]

                else:
                    selected_resturant = matched_resturants[0]


                donor_id = selected_resturant[0]

                # Find unrated completed requests qeury
                request_query = """
                        SELECT r.id, u.name, r.request_qty FROM volunteer_request_collections r JOIN food_donations f ON r.donor_id = f.id 
                        JOIN users u ON r.donor_id = u.id WHERE r.volunteer_id = %s AND r.donor_id = %s AND r.status = 'completed' 
                        AND NOT EXISTS (SELECT 1 FROM resturant_ratings rr WHERE rr.request_id = r.id)
                """

                cursor.execute(request_query, (self.volunteer_id, donor_id))
                available_requests = cursor.fetchall()

                if not available_requests:
                    print("\nNo unrated completed request found!")
                    return

                if len(available_requests) > 1:
                    print("\n=========================== Completed Requests ===============================")

                    for index, request in enumerate(available_requests, start=1):
                        print(
                            f"{index}. Food: {request[1]} "
                            f"| Quantity: {request[2]}"
                        )
                        if choice < 1 or choice > len(available_requests):
                            print("\nInvalid option!")
                            return

                        selected_request = available_requests[choice - 1]
                else:
                    selected_request = available_requests[0]

                request_id = selected_request[0]


                # Take Rating

                rating = int(input("\nGive Rating (1-5): "))

                if rating < 1 or rating > 5:
                    print("\nRating must be between 1 to 5!")
                    return

                feedback = input("\nWrite feedback: ")

                # Insert Rating and Feedback

                insert_query = """
                        INSERT INTO resturant_ratings (request_id, volunteer_id, donor_id, rating, feedback)
                        VALUES (%s, %s, %s, %s, %s)
                """

                values = (request_id, self.volunteer_id, donor_id,rating, feedback)

                cursor.execute(insert_query, values)
                db.commit()

                print("\nRestaurant Rating Submitted Successfully!")
                print("Thank you for your feedback!")

        except mysql.connector.Error as err:
            print("Database Error:", err)

            if db:
                db.rollback()

        finally:
            if cursor:
                cursor.close()

            if db and db.is_connected():
                db.close()


    #   _ 