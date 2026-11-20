class Utility:
    def required_input(self, input_dict):
        for key, value in input_dict.items():
            if value is None or str(value).strip() == "":
                return {"status": False, "result": f"Empty value at {key}"}

        return {"status": True, "result": input_dict}