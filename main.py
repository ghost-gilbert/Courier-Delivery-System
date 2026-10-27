import authentication as auth

class Dashboard:
    def __init__(self):
        pass

    def LoginMenu(self):
        print("[Login Menu]")
        print("New user will be redirected for sign up")
        email = input("Enter your Email: ")
        password = input("Enter you Password: ")

        user = auth.UserAuthentication("User_Details/credentials.txt", email, password)
        login = user.sign_in()
        if(login["status"]==ValueError):
            print(f"Login Failed! {user["result"]}")
        elif(login["status"]==IndexError):
            print("[User not found]")
            print("[Sign Up]")
            name = input("Enter your Name: ")
            phone = input("Enter your Phone No.: ")

# Only for testing purpose
d1 = Dashboard()
d1.LoginMenu()