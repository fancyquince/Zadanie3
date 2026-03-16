from pydantic import BaseModel
from typing import Dict, List

import json




    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Apartment']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of apartments"
        return {key: Apartment(**apartment) for key, apartment in data.items()}

    


    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Tenant']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of tenants"
        return {key: Tenant(**tenant) for key, tenant in data.items()}
    



    @staticmethod
    def from_json_file(file_path: str) -> List['Transfer']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of transfers"
        return [Transfer(**transfer) for transfer in data]




    @staticmethod
    def from_json_file(file_path: str) -> List['Bill']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of bills"
        return [Bill(**bill) for bill in data]




    @staticmethod
    def from_json_file(file_path: str) -> Dict[str, 'ApartmentSettlement']:
        with open(file_path, 'r') as file:
            data = json.load(file)

        assert isinstance(data, dict), "Expected a dictionary of apartment settlements"

        return {key: ApartmentSettlement(**settlement) for key, settlement in data.items()}




class TenantSettlement:
    def __init__(self, najemca, miesiac, rok, 
                 rozliczenie_mieszkania, kwota_czynszu, 
                 kwota_rachunki, suma_przelewow):
        self.najemca = najemca
        self.miesiac = miesiac
        self.rok = rok
        self.rozliczenie_mieszkania = rozliczenie_mieszkania
        self.kwota_czynszu = kwota_czynszu
        self.kwota_rachunki = kwota_rachunki
        self.suma_przelewow = suma_przelewow
        self.saldo = self.oblicz_saldo()

    def oblicz_saldo(self):
        koszty = self.kwota_czynszu + self.kwota_rachunki
        return self.suma_przelewow - koszty
