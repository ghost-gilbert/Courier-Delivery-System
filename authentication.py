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


    def sign_in(self):
        result = self.findOne("email", self.email)
        if(result):
            if(result["password"]==self.password):
                return {"status": True, "result": result}
            else:
                return {"status": ValueError, "result": "Invalid Credentails! Please Check your password"}
        else:
            return {"status": IndexError, "result": "Invalid Credentails! Please Check you email address"}
