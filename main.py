import authentication as auth
from dashboard import select_role

class Dashboard:
    def __init__(self):
        pass

    def LoginMenu(self):
        while True:
            print("\n==== [Login Menu] ====")
            email = input("Enter your Email (or type 'exit' to quit): ").strip()
            if email.lower() == "exit":
                print("Goodbye!")
                break
            password = input("Enter your Password: ").strip()

            user = auth.UserAuthentication("User_Details/credentials.txt", email, password)
            login = user.sign_in()

            if login["status"] == True:
                current_user = login["result"]
                print(f"\nWelcome back, {current_user['name']} ({current_user['customer_id']})!")
                select_role(current_user)

            elif login["status"] == ValueError:
                print(f"\nLogin Failed! {login['result']}")
                choice = input("Do you want to sign up with a new account? (y/n): ").strip().lower()
                if choice == "y":
                    print("\n[Sign Up]")
                    new_email = input("Enter a new Email: ").strip()
                    new_password = input("Enter a Password: ").strip()
                    name = input("Enter your Name: ").strip()
                    phone = input("Enter your Phone No.: ").strip()

                    new_user = auth.UserAuthentication("User_Details/credentials.txt", new_email, new_password)
                    if new_user.findOne("email", new_email):
                        print("That email is already registered! Returning to Login Menu...")
                        continue

                    signup = new_user.sign_up(name, phone)
                    if signup["status"]:
                        current_user = signup["result"]
                        print(f"Account created! Your Customer ID is: {current_user['customer_id']}")
                        select_role(current_user)
                    else:
                        print(f"Sign Up Failed! {signup['result']}")
                else:
                    print("Returning to Login Menu...")

            elif login["status"] == IndexError:
                print("\n[User not found]")
                choice = input("Do you want to sign up with this email? (y/n): ").strip().lower()
                if choice == "y":
                    print("\n[Sign Up]")
                    name = input("Enter your Name: ").strip()
                    phone = input("Enter your Phone No.: ").strip()

                    signup = user.sign_up(name, phone)
                    if signup["status"]:
                        current_user = signup["result"]
                        print(f"Account created! Your Customer ID is: {current_user['customer_id']}")
                        select_role(current_user)
                    else:
                        print(f"Sign Up Failed! {signup['result']}")
                else:
                    print("Returning to Login Menu...")


if __name__ == "__main__":
    d1 = Dashboard()
    d1.LoginMenu()