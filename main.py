from pydantic import BaseModel
from typing import Dict, List

import json


class Parameters(BaseModel):
    apartments_json_path: str = 'data/apartments.json'
    tenants_json_path: str = 'data/tenants.json'
    transfers_json_path: str = 'data/transfers.json'
    bills_json_path: str = 'data/bills.json'


class Room(BaseModel):
    name: str
    area_m2: float


class Apartment(BaseModel):
    key: str
    name: str
    location: str
    area_m2: float
    rooms: Dict[str, Room]

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Apartment']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of apartments"
        return {key: Apartment(**apartment) for key, apartment in data.items()}

    
class Tenant(BaseModel):
    name: str
    apartment: str
    room: str
    rent_pln: float
    deposit_pln: float
    date_agreement_from: str
    date_agreement_to: str

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Tenant']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of tenants"
        return {key: Tenant(**tenant) for key, tenant in data.items()}
    

class Transfer(BaseModel):
    amount_pln: float
    date: str
    settlement_year: int | None
    settlement_month: int | None
    tenant: str

    @staticmethod
    def from_json_file(file_path: str) -> List['Transfer']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of transfers"
        return [Transfer(**transfer) for transfer in data]


class Bill(BaseModel):
    amount_pln: float
    date_due: str
    apartment: str
    settlement_year: int
    settlement_month: int
    type: str

    @staticmethod
    def from_json_file(file_path: str) -> List['Bill']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of bills"
        return [Bill(**bill) for bill in data]


class ApartmentSettlement(BaseModel):
    apartment: str
    month: int
    year: int
    total_bills: float
    total_rent: float
    date_agreement_from: str
    amount_due: float

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str, 'ApartmentSettlement']:
        with open(file_path, 'r') as file:
            data = json.load(file)

        assert isinstance(data, dict), "Expected a dictionary of apartment settlements"

        return {key: ApartmentSettlement(**settlement) for key, settlement in data.items()}


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
                print(f"    - {transfer.amount_pln} PLN | {transfer.date} | settlement: {transfer.settlement_year}/{transfer.settlement_month}")