class FileHandling:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_file(self):
        with open(self.filepath, "r") as file:
            return file.read()

    def append_data(self, data):
        with open(self.filepath, "a+") as file:
            return file.write(data)

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

    def find_user_detail(self, key, value):
        for user in self.parsed_dict():
            if (user[key]==str(value)):
                return user