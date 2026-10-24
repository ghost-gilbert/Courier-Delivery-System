class Utility:
    def required_input(self, input_dict):
        for i in input_dict:
            print(i)
            if(input_dict[i].strip()=="" or input_dict[i]==None):
                return {"status": False, "result": f"Empty Value at {i}"}

        return {"status": True, "result": input_dict}


# u1 = Utility()
# print(u1.required_input({"name": "Kumar", "email": ""}))