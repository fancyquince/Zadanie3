class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)


if __name__ == '__main__':
    parameters = Parameters()
    manager = Manager(parameters)

    print("\n=== Apartments ===")
    for apartment in manager.apartments.values():
        print(f"\nApartment: {apartment.name}")
        print(f"  Key: {apartment.key}")
        print(f"  Location: {apartment.location}")
        print(f"  Area: {apartment.area_m2} m2")
        print("  Rooms:")
        for room in apartment.rooms.values():
            print(f"    - {room.name} ({room.area_m2} m2)")

        print("  Bills:")
        for bill in manager.bills:
            if bill.apartment == apartment.key:
                print(f"    - {bill.type}: {bill.amount_pln} PLN | due: {bill.date_due}")

    print("\n=== Tenants ===")
    for tenant in manager.tenants.values():
        print(f"\nTenant: {tenant.name}")
        print(f"  Apartment: {tenant.apartment}")
        print(f"  Room: {tenant.room}")
        print(f"  Rent: {tenant.rent_pln} PLN")
        print(f"  Deposit: {tenant.deposit_pln} PLN")
        print(f"  Agreement: {tenant.date_agreement_from} → {tenant.date_agreement_to}")

        print("  Transfers:")
        for transfer in manager.transfers:
            if transfer.tenant == tenant.name:
                print('  ', transfer.amount_pln, transfer.date, transfer.settlement_year, transfer.settlement_month)