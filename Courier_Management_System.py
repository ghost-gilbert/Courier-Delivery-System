from datetime import datetime
import matplotlib.pyplot as plt
from file_database import FileHandling


class Package:
    EXTRA_CHARGES = {"Standard": 0.0, "Express": 150.0, "Fragile": 80.0}
    INSTRUCTIONS = {
        "Standard": "Standard ground delivery.",
        "Express": "Priority Express: handle carefully and prioritize delivery.",
        "Fragile": "Fragile: do not stack; handle with extreme caution.",
    }

    @staticmethod
    def calculate_charge(pkg_type, weight):
        base = 50.0 + (float(weight) * 10.0)
        return base + Package.EXTRA_CHARGES.get(pkg_type, 0.0)

    @staticmethod
    def get_instructions(pkg_type):
        return Package.INSTRUCTIONS.get(pkg_type, "Standard handling.")


class CourierSystem:
    VALID_ZONES = ["North", "South", "East", "West", "Central"]
    AVAILABLE_AGENTS = ["Agent_John", "Agent_Sarah", "Agent_Mike", "Agent_Emma"]

    def __init__(self):
        self.customers_db = FileHandling("User_Details/credentials.txt")
        self.packages_db = FileHandling("User_Details/packages.txt")
        self.logs_db = FileHandling("User_Details/delivery_logs.txt")

    def register_customer(self, name, phone):
        customer_id = self.customers_db.generate_id("CUST")
        self.customers_db.add_record({
            "customer_id": customer_id,
            "name": name,
            "phone": phone,
        })
        return customer_id

    def create_shipment(self, customer_id, pkg_type, weight, zone):
        if not self.customers_db.findOne("customer_id", customer_id):
            raise ValueError(f"Customer ID '{customer_id}' is not registered.")
        if zone not in self.VALID_ZONES:
            raise ValueError(f"Invalid zone. Choose from: {', '.join(self.VALID_ZONES)}")

        weight = float(weight)
        if weight <= 0:
            raise ValueError("Weight must be greater than zero.")

        tracking_id = self.packages_db.generate_id("TRK")
        charge = Package.calculate_charge(pkg_type, weight)
        record = {
            "tracking_id": tracking_id,
            "customer_id": customer_id,
            "type": pkg_type,
            "weight": weight,
            "zone": zone,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "Registered",
            "agent": "None",
            "attempts": 0,
            "location": "Warehouse",
            "charge": f"{charge:.2f}",
        }
        self.packages_db.add_record(record)
        return record

    def assign_agent(self, tracking_id, agent_name):
        pkg = self.packages_db.findOne("tracking_id", tracking_id)
        if not pkg:
            raise ValueError(f"Tracking ID '{tracking_id}' not found.")
        if pkg["status"] == "Delivered":
            raise ValueError("Cannot assign an agent to a delivered package.")
        if agent_name not in self.AVAILABLE_AGENTS:
            raise ValueError(f"Agent '{agent_name}' is not available.")

        self.packages_db.updateOne("tracking_id", tracking_id, {
            "agent": agent_name,
            "status": "In Transit",
            "location": f"With {agent_name}",
        })

    def update_location(self, tracking_id, new_location):
        pkg = self.packages_db.findOne("tracking_id", tracking_id)
        if not pkg:
            raise ValueError(f"Tracking ID '{tracking_id}' not found.")
        if pkg["status"] == "Delivered":
            raise ValueError("Cannot update location of a delivered package.")

        self.packages_db.updateOne("tracking_id", tracking_id, {"location": new_location})

    def record_delivery_attempt(self, tracking_id, success, remarks=""):
        pkg = self.packages_db.findOne("tracking_id", tracking_id)
        if not pkg:
            raise ValueError(f"Tracking ID '{tracking_id}' not found.")
        if pkg["status"] == "Delivered":
            raise ValueError("Package has already been delivered.")
        if pkg["agent"] == "None":
            raise ValueError("Assign a delivery agent first.")

        attempts = int(pkg["attempts"]) + 1
        if success:
            status, location, result = "Delivered", "Delivered to customer", "SUCCESS"
        else:
            status = "Failed" if attempts >= 3 else "Attempt Failed"
            location, result = pkg["location"], "FAILED"

        self.packages_db.updateOne("tracking_id", tracking_id, {
            "attempts": attempts,
            "status": status,
            "location": location,
        })

        log = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tracking_id": tracking_id,
            "attempt": attempts,
            "result": result,
            "agent": pkg["agent"],
            "remarks": remarks or "None",
        }
        self.logs_db.add_record(log)
        return log

    def delete_shipment(self, tracking_id):
        if not self.packages_db.deleteOne("tracking_id", tracking_id):
            raise ValueError(f"Tracking ID '{tracking_id}' not found.")


# ============================================================
# REPORTS & MATPLOTLIB CHARTS
# ============================================================

def generate_performance_report(system):
    packages = system.packages_db.parsed_dict()
    if not packages:
        print("\nNo packages to analyze.")
        return

    total = len(packages)
    delivered = sum(1 for p in packages if p["status"] == "Delivered")
    zone_counts = {}
    for p in packages:
        zone_counts[p["zone"]] = zone_counts.get(p["zone"], 0) + 1

    print("\n" + "=" * 50)
    print("           COURIER PERFORMANCE REPORT")
    print("=" * 50)
    print(f"Total Packages       : {total}")
    print(f"Delivered Packages   : {delivered}")
    print(f"Undelivered Packages : {total - delivered}")
    print(f"Success Rate         : {(delivered / total) * 100:.1f}%")
    print(f"Zone Volumes         : {zone_counts}")
    print("=" * 50)


def show_charts(system):
    packages = system.packages_db.parsed_dict()
    if not packages:
        print("No package data available for plotting.")
        return

    # Chart 1: Packages by Status
    status_counts = {}
    for p in packages:
        status_counts[p["status"]] = status_counts.get(p["status"], 0) + 1

    plt.figure(figsize=(8, 4))
    plt.bar(status_counts.keys(), status_counts.values())
    plt.title("Packages by Delivery Status")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

    # Chart 2: Delivery Performance by Zone
    zones = system.VALID_ZONES
    total = [sum(1 for p in packages if p["zone"] == z) for z in zones]
    delivered = [sum(1 for p in packages if p["zone"] == z and p["status"] == "Delivered") for z in zones]

    pos = list(range(len(zones)))
    plt.figure(figsize=(8, 4))
    plt.bar([i - 0.2 for i in pos], total, width=0.4, label="Total")
    plt.bar([i + 0.2 for i in pos], delivered, width=0.4, label="Delivered")
    plt.xticks(pos, zones)
    plt.title("Delivery Performance by Zone")
    plt.xlabel("Zone")
    plt.ylabel("Packages")
    plt.legend()
    plt.tight_layout()
    plt.show()