# Basically i was trying to create CRUD operation for a txt file
class FileHandling:
    def __init__(self, filepath):
        self.filepath = filepath
        unq_id = 0
        with open('User_Details/unique_id.txt', 'r') as file:
            unq_id = file.read().split("=")[1].strip()
        self.unq_id = unq_id


    # Reading txt file data
    def read_file(self):
        with open(self.filepath, "r") as file:
            return file.read()

    def read_lines(self):
        fileData = ""
        with open(self.filepath, 'r') as file:
            while True:
                data = file.readline()
                if(not data):
                    break
                fileData = fileData + data.strip() +"\n"
        return fileData

    # Appending raw data to file
    def append_data(self, data):
        with open(self.filepath, "a+") as file:
            return file.write(data)

    def write_file(self, data):
        with open(self.filepath, "w") as file:
            return file.write(data)
        
    # Read
    # Converting the data of txt file into a dictionary
    def parsed_dict(self):
        rawData = self.read_file()
        user_capsule = rawData.strip()

        main_list = []

        for data_tup in user_capsule.split("\n"):
            dict_version = {}
            for raw_pairs_list in data_tup[1:-1].split(","):
                (key, value) = raw_pairs_list.strip().split("=")
                dict_version.update({key: value})

            main_list.append(dict_version)

        return main_list

    # Fetch data related to a particular Users from the txt file 
    def findOne(self, key, value):
        for user in self.parsed_dict():
            if (user[key]==str(value)):
                return user

    # Delete
    def deleteOne(self, key, value):
        combo = f"[{key}={value}"
        data = self.read_lines()
        start = data.find(combo)
        newData = data[start:]
        end = newData.find("\n")
        newStr = data[0:start]+newData[end:].strip()
        self.write_file(newStr)

    # Update
    def updateOne(self, key, value):
        for user in self.parsed_dict():
            pass
