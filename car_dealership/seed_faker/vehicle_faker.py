#from pathlib import Path
#print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

#import faker
import datetime
from random import choice, randint
from faker.providers import BaseProvider
#from vehicle_dict import vehicles, PETROL_CHOICES, CAR_TYPE_CHOICES, GEAR_CHOICES

PETROL_CHOICES = ['Petrol', 'Diesel', 'Electric', 'Hybrid'
]

CAR_TYPE_CHOICES = [
        'Sedan', 'SUV', 'Truck', 'Coupe', 'Convertible', 'Hatchback', 'Van', 'Wagon'
]

GEAR_CHOICES = [
        'Manual', 'Automatic'
]
class VehicleProvider(BaseProvider):

    """
    A Provider for vehicle related test data.

    >>> from faker import Faker
    >>> from vehicle_faker import VehicleProvider
    >>> fake = Faker()
    >>> fake.add_provider(VehicleProvider)

    vehicle_object(self):        
        Returns a random vehicle dict example:
        {"Year": 2008, "Make": "Jeep", "Model": "Wrangler", "Category": "SUV"}

    vehicle_year_make_model(self):
        Returns str: Year Make Model 
        example: 1997 Nissan 240SX

    vehicle_year_make_model_cat_vin(self):
        Returns str: Year Make Model Cat 
        example:
        2017 GMC Sierra 1500 Double Cab (Pickup)

    vehicle_make_model(self):
        Returns str: Make Model 
        example: Audi Q7

    vehicle_make(self):
        Returns str: Make 
        example: Lincoln

    vehicle_year(self):
        Returns str: Year 
        example: 1999

    def vehicle_model(self):
        Returns str: Model 
        example: Prius

    def vehicle_category(self):
        Returns str: Category 
        example: SUV

    def vehicle_generated_vin(self):
        Returns str: VIN
        example: 'RT3GZYSKXXNDZ9J97'
    """

    def vehicle_object_dict(self) -> dict:
        """
        Returns a random vehicle dict example:
        {'year': 2010, 'manufacturer_name': 'Dodge', 'model_name': 'Ram 1500 Regular Cab', 'car_type': 'Sedan', 'VIN': 'VK1GR2EU7BA555CTA', 'manufacturer_country': 'default country', 'manufacturer_established_date': datetime.date(1999, 10, 10), 'price': 123456, 'vehicle_description': 'Super-duper description', 'petrol_type': 'Hybrid', 'gear_type': 'Manual'}
        """
        
        
        veh = {
            #'VIN': fake.vin(),
            'year': randint(1992, 2024),
            'car_type': VehicleProvider.vehicle_car_type(self),
            #'manufacturer_country': VehicleProvider.vehicle_manufacturer_country(self),
            #'manufacturer_established_date': VehicleProvider.vehicle_manufacturer_established_date(self),
            'price': VehicleProvider.vehicle_price(),
            'description': VehicleProvider.vehicle_description(),
            'petrol_type': VehicleProvider.vehicle_petrol_type(),
            'gear_type': VehicleProvider.vehicle_gear_type(),
            'milage': VehicleProvider.vehicle_milige(),
        }

        return veh


# Manufacturer


    def vehicle_manufacturer_name(self) -> str:
        """Returns Make example: Lincoln"""
        veh = self.vehicle_object_dict()
        return veh.get('manufacturer_name')

    def vehicle_manufacturer_country(self) -> str:
        return 'default country'

    def vehicle_manufacturer_established_date(self) -> datetime:
        return datetime.date(1999, 10, 10)

# Brandmodel
    def vehicle_model(self) -> str:
        """Returns Model example: Frontier King Cab"""
        veh = self.vehicle_object_dict()
        return veh.get('model_name')

    def vehicle_year(self) -> int:
        """Returns Year example: 1999"""
        veh = self.vehicle_object_dict()
        return int(veh.get('year'))

# Car

    def vehicle_car_type(self) -> str:
        """Returns Category example: SUV"""
        return choice(CAR_TYPE_CHOICES)

    def vehicle_price() -> int:
        return randint(30000, 40000)

    def vehicle_description() -> str:
        return "Super-duper description"

    def vehicle_generated_vin(self) -> str:
        """Returns VIN example: 'RT3GZYSKXXNDZ9J97'"""
        veh = self.vehicle_object_dict()
        return veh.get('VIN')

    def vehicle_petrol_type() -> str:
        return choice(PETROL_CHOICES)

    def vehicle_gear_type() -> str:
        return choice(GEAR_CHOICES)
    
    def vehicle_milige() -> int:
        return randint(0, 1000000)
