import os
from file_database import FileHandling
from utility import Utility

os.makedirs("User_Details", exist_ok=True)

class UserAuthentication(FileHandling):
    def __init__(self, filepath, email, password):
        super().__init__(filepath)
        self.email = email
        self.password = password
        self.util = Utility()

    def sign_up(self, name, phone):
        check = self.util.required_input({
            "name": name,
            "phone": phone,
            "email": self.email,
            "password": self.password
        })
        if not check["status"]:
            return check

        customer_id = self.generate_id("CUST")
        user_record = {
            "customer_id": customer_id,
            "name": name,
            "phone": phone,
            "email": self.email,
            "password": self.password
        }
        self.add_record(user_record)
        return {"status": True, "result": user_record}

    def sign_in(self):
        result = self.findOne("email", self.email)
        if result:
            if result["password"] == self.password:
                return {"status": True, "result": result}
            else:
                return {"status": ValueError, "result": "Invalid Credentials! Please check your password."}
        else:
            return {"status": IndexError, "result": "Invalid Credentials! Please check your email address."}