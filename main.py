from auth.register import Registration
from auth.login import Login

class FoodRescueCoordinator:

    def __init__(self):
        self.registration = Registration()
        self.login = Login()

    def main(self):

        while True:
            print("\n============================= FOOD RESCUE COORDINATOR ===========================")
            print("")
            print("1. Registration")
            print("2. Login")
            print("3. Exit")

            choice = input("\nSelect Option: ")

            if choice == "1":
                self.registration.register()
            elif choice == "2":
                user = self.login.login()

                if user:
                    if user["role"] == "receiver":
                        print("\nWelcome to Receiver Dashboard!")
                    elif user["role"] == "doner":
                        print("\nWelcome to Doner Dashboard!")
            elif choice == "3":
                print("\nThank you for using Food Rescue Coordinator!")
                break
            else:
                print("Invalid Option! Try Again.")

if __name__ == "__main__":
    app = FoodRescueCoordinator()
    app.main()