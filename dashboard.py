from Courier_Management_System import (
    CourierSystem,
    Package,
    generate_performance_report,
    show_charts,
)


class UserType:
    def __init__(self, role, current_user):
        self.role = role
        self.current_user = current_user
        self.system = CourierSystem()

    def _track_package(self):
        pending = [
            p for p in self.system.packages_db.parsed_dict()
        ]

        if not pending:
            print("\nNo pending packages available to assign.")
            return

        print("\n--- PACKAGES ---")
        for pkg in pending:
            print(
                f"Tracking ID: {pkg['tracking_id']} | Zone: {pkg['zone']} | Status: {pkg['status']} | Current Agent: {pkg['agent']}"
            )

        tid = input("Enter Tracking ID: ").strip().upper()
        pkg = self.system.packages_db.findOne("tracking_id", tid)
        if not pkg:
            print("Tracking ID not found.")
            return
        print("\n--- PACKAGE DETAILS ---")
        for k, v in pkg.items():
            print(f"{k.capitalize():<12}: {v}")
        print(f"Instructions: {Package.get_instructions(pkg['type'])}")

    def _create_shipment(self):
        if self.role == "Customer":
            cid = self.current_user["customer_id"]
            print(f"Booking shipment for Customer ID: {cid}")
        else:
            cid = input("Enter Customer ID: ").strip().upper()

        print("Types: [1] Standard  [2] Express  [3] Fragile")
        t_choice = {"1": "Standard", "2": "Express", "3": "Fragile"}.get(input("Choose (1-3): ").strip())
        if not t_choice:
            print("Invalid package type.")
            return
        weight = input("Weight (kg): ").strip()
        print("Zones:", ", ".join(self.system.VALID_ZONES))
        zone = input("Delivery Zone: ").strip().title()

        pkg = self.system.create_shipment(cid, t_choice, weight, zone)
        print(f"\nShipment created! Tracking ID: {pkg['tracking_id']} | Charge: Rs. {pkg['charge']}")

    def _assign_agent(self):
        pending = [
            p for p in self.system.packages_db.parsed_dict()
            if p.get("status") != "Delivered" and p.get("agent") == "None"
        ]

        if not pending:
            print("\nNo pending packages available to assign.")
            return

        print("\n--- UNASSIGNED PACKAGES ---")
        for pkg in pending:
            print(
                f"Tracking ID: {pkg['tracking_id']} | Zone: {pkg['zone']} | "
                f"Status: {pkg['status']} | Current Agent: {pkg['agent']}"
            )
        tid = input("Tracking ID: ").strip().upper()
        for i, agent in enumerate(self.system.AVAILABLE_AGENTS, 1):
            print(f"[{i}] {agent}")
        idx = input("Choose Agent (1-4): ").strip()
        if not idx.isdigit() or not (1 <= int(idx) <= len(self.system.AVAILABLE_AGENTS)):
            print("Invalid agent selection.")
            return
        agent = self.system.AVAILABLE_AGENTS[int(idx) - 1]
        self.system.assign_agent(tid, agent)
        print(f"{agent} assigned to {tid}.")

    def _update_location(self):
        pending = [
            p for p in self.system.packages_db.parsed_dict()
            if p.get("status") != "Delivered"
        ]

        if not pending:
            print("\nNo pending packages available to assign.")
            return

        print("\n--- UNDELIVERED PACKAGES ---")
        for pkg in pending:
            print(
                f"Tracking ID: {pkg['tracking_id']} | Zone: {pkg['zone']} | Current Agent: {pkg['agent']}"
            )


        tid = input("Tracking ID: ").strip().upper()
        loc = input("New Location: ").strip()
        self.system.update_location(tid, loc)
        print("Location updated.")

    def _record_attempt(self):
        pending = [
            p for p in self.system.packages_db.parsed_dict()
            if p.get("status") != "Delivered"
        ]

        if not pending:
            print("\nNo pending packages available to assign.")
            return

        print("\n--- UNDELIVERED PACKAGES ---")
        for pkg in pending:
            print(
                f"Tracking ID: {pkg['tracking_id']} | Zone: {pkg['zone']} | Status: {pkg['status']} | Current Agent: {pkg['agent']}"
            )

        tid = input("Tracking ID: ").strip().upper()
        res = input("Delivered successfully? (y/n): ").strip().lower()
        remarks = input("Remarks (optional): ").strip()
        log = self.system.record_delivery_attempt(tid, res == "y", remarks)
        print(f"Attempt #{log['attempt']} recorded ({log['result']}).")

    def _view_all(self):
        print("\n--- REGISTERED USERS ---")
        for c in self.system.customers_db.parsed_dict():
            print(f"ID: {c.get('customer_id')} | Name: {c.get('name')} | Phone: {c.get('phone')} | Email: {c.get('email')}")
        print("\n--- PACKAGES ---")
        for p in self.system.packages_db.parsed_dict():
            print(p)

    def _my_packages(self):
        cid = self.current_user["customer_id"]
        my_pkgs = [
            p for p in self.system.packages_db.parsed_dict()
            if p.get("customer_id") == cid
        ]

        if not my_pkgs:
            print("\nYou have no registered packages yet.")
            return

        print(f"\n--- MY PACKAGES ({cid}) ---")
        for pkg in my_pkgs:
            print(
                f"Tracking ID: {pkg['tracking_id']} | Type: {pkg['type']} | "
                f"Weight: {pkg['weight']} kg | Zone: {pkg['zone']} | "
                f"Status: {pkg['status']} | Location: {pkg['location']} | "
                f"Charge: Rs. {pkg['charge']}"
            )

        tid = input("Enter Tracking ID: ").strip().upper()
        pkg = self.system.packages_db.findOne("tracking_id", tid)
        if not pkg:
            print("Tracking ID not found.")
            return
        print("\n--- PACKAGE DETAILS ---")
        for k, v in pkg.items():
            print(f"{k.capitalize():<12}: {v}")
        print(f"Instructions: {Package.get_instructions(pkg['type'])}")

    def openFile(self):
        while True:
            print(f"\n===== {self.role.upper()} DASHBOARD ({self.current_user['name']}) =====")
            if self.role == "Customer":
                print("[1] Create Shipment\n[2] View My Packages\n[0] Logout")
            elif self.role == "Staff":
                print("[1] Assign Agent\n[2] Update Location\n[3] Record Delivery Attempt\n[4] Track Package\n[0] Logout")
            elif self.role == "Admin":
                print("[1] Track Package\n[2] View All Records\n[3] Delete Shipment\n[4] Performance Report\n[5] Show Charts\n[0] Logout")

            choice = input("Enter choice: ").strip()
            if choice == "0":
                print("Logged out.")
                break

            try:
                if self.role == "Customer":
                    if choice == "1":
                        self._create_shipment()
                    elif choice == "2":
                        self._my_packages()
                    else:
                        print("Invalid choice.")

                elif self.role == "Staff":
                    if choice == "1":
                        self._assign_agent()
                    elif choice == "2":
                        self._update_location()
                    elif choice == "3":
                        self._record_attempt()
                    elif choice == "4":
                        self._track_package()
                    else:
                        print("Invalid choice.")

                elif self.role == "Admin":
                    if choice == "1":
                        self._track_package()
                    elif choice == "2":
                        self._view_all()
                    elif choice == "3":
                        tid = input("Tracking ID to delete: ").strip()
                        self.system.delete_shipment(tid)
                        print("Shipment deleted.")
                    elif choice == "4":
                        generate_performance_report(self.system)
                    elif choice == "5":
                        show_charts(self.system)
                    else:
                        print("Invalid choice.")
            except ValueError as err:
                print(f"[Error] {err}")


def select_role(current_user):
    print("\n===== Pick Your Role =====")
    print("[1] Customer\n[2] Staff\n[3] Admin")
    choice = input("Select your role (1-3): ").strip()

    roles = {"1": "Customer", "2": "Staff", "3": "Admin"}
    if choice in roles:
        user = UserType(roles[choice], current_user)
        user.openFile()
        return user
    else:
        print("Invalid Input")
        return None