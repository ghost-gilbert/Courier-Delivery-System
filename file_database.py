import os

class FileHandling:
    def __init__(self, filepath):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as file:
                pass

        unq_path = "User_Details/unique_id.txt"
        if not os.path.exists(unq_path):
            with open(unq_path, "w") as file:
                file.write("CUST=0\nTRK=0\n")

    def generate_id(self, prefix="ID"):
        unq_path = "User_Details/unique_id.txt"
        counters = {}

        if os.path.exists(unq_path):
            with open(unq_path, "r") as file:
                for line in file:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        if v.isdigit():
                            counters[k.strip()] = int(v.strip())

        new_id = counters.get(prefix, 0) + 1
        counters[prefix] = new_id

        with open(unq_path, "w") as file:
            for k, v in counters.items():
                file.write(f"{k}={v}\n")

        return f"{prefix}{new_id:04d}"

    def _clean(self, value):
        return str(value).replace(",", ";").replace("=", "-").replace("\n", " ").strip()

    def _format_record(self, record_dict):
        pairs = ",".join(f"{k}={self._clean(v)}" for k, v in record_dict.items())
        return f"[{pairs}]"

    def _save_all(self, records):
        lines = [self._format_record(rec) for rec in records]
        self.write_file("\n".join(lines) + ("\n" if lines else ""))

    def read_file(self):
        with open(self.filepath, "r") as file:
            return file.read()

    def append_data(self, data):
        with open(self.filepath, "a+") as file:
            return file.write(data.strip() + "\n")

    def add_record(self, record_dict):
        return self.append_data(self._format_record(record_dict))

    def write_file(self, data):
        with open(self.filepath, "w") as file:
            return file.write(data)

    def parsed_dict(self):
        raw_data = self.read_file().strip()
        if not raw_data:
            return []

        main_list = []
        for data_tup in raw_data.split("\n"):
            line = data_tup.strip()
            if not line or not (line.startswith("[") and line.endswith("]")):
                continue

            dict_version = {}
            for raw_pair in line[1:-1].split(","):
                if "=" in raw_pair:
                    key, value = raw_pair.strip().split("=", 1)
                    dict_version[key.strip()] = value.strip()

            if dict_version:
                main_list.append(dict_version)

        return main_list

    def findOne(self, key, value):
        for record in self.parsed_dict():
            if record.get(key) == str(value):
                return record
        return None

    def deleteOne(self, key, value):
        records = self.parsed_dict()
        updated = [rec for rec in records if rec.get(key) != str(value)]
        if len(updated) == len(records):
            return False
        self._save_all(updated)
        return True

    def updateOne(self, key, value, new_data):
        records = self.parsed_dict()
        updated_flag = False
        for rec in records:
            if rec.get(key) == str(value):
                rec.update({k: self._clean(v) for k, v in new_data.items()})
                updated_flag = True
                break

        if updated_flag:
            self._save_all(records)
        return updated_flag