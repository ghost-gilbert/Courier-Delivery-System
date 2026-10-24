import os
from file_database import FileHandling
from utility import Utility

try:
    os.makedirs("User_Details")
except:
    pass

class UserAuthentication(FileHandling):
    def __init__(self, filepath, email, password):
        super().__init__(filepath)
        self.email = email
        self.password = password

    def sign_up(self, name, phone):
        self.append_data(f"[name={name},phone={phone},email={self.email},password={self.password}]")
        # with open("User_Details/user_data.txt", "a") as file:
        #     file.write()

    def sign_in(self):
        result = self.find_user_detail("email", self.email)
        if(result):
            if(result["password"]==self.password):
                return {"status": True, "result": result}
            else:
                return {"status": ValueError, "result": "Invalid Credentails! Please Check your password"}
        else:
            return {"status": IndexError, "result": "Invalid Credentails! Please Check you email address"}

# u1 = UserAuthentication("User_Details/credentials.txt", "0001.gilbert@gmail.com", "Kum@rH@r&h!001")
# print(u1.sign_in())


# v1 = Utility()
# v1.required_input()