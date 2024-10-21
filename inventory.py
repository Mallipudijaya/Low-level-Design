from enum import Enum
from typing import Dict, List, Set

class LocationType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Location:
    location_count = 0

    def __init__(self, location_type: LocationType):
        Location.location_count += 1
        self.location_id = Location.location_count
        self.is_available = True
        self.location_type = location_type

    def set_is_available(self, is_available: bool):
        self.is_available = is_available

    def get_is_available(self) -> bool:
        return self.is_available

class Unit:
    unit_count = 0

    def __init__(self, product_id: int, location: Location):
        Unit.unit_count += 1
        self.unit_id = Unit.unit_count
        self.product_id = product_id
        self.location = location
        self.location.set_is_available(False)

    def free_location(self):
        self.location.set_is_available(True)

class Product:
    product_count = 0

    def __init__(self, name: str, price: float):
        Product.product_count += 1
        self.product_id = Product.product_count
        self.product_name = name
        self.units: Set[Unit] = set()
        self.price = price

    def add_unit(self, location: Location):
        new_unit = Unit(self.product_id, location)
        self.units.add(new_unit)

    def remove_unit(self, unit: Unit):
        unit.free_location()
        self.units.remove(unit)

    def set_price(self, price: float):
        self.price = price

    def get_product_id(self) -> int:
        return self.product_id

class Order:
    def __init__(self, products: Dict[int, List[Unit]]):
        self.products = products

class InventorySystem:
    def __init__(self):
        self.all_products: Dict[int, Product] = {}
        self.all_locations: Dict[LocationType, List[Location]] = {}
        self.all_orders: List[Order] = []

    def get_location_availability(self, location_type: LocationType) -> Location:
        locations = self.all_locations.get(location_type, [])
        for location in locations:
            if location.get_is_available():
                return location
        return None

    def create_new_product(self, product_name: str, n_units: int, price: float):
        new_product = Product(product_name, price)
        product_id = new_product.get_product_id()
        for _ in range(n_units):
            new_product.add_unit(None)  # Assuming no location is needed initially
        self.all_products[product_id] = new_product

    def create_order(self, products: Dict[int, List[Unit]]):
        for product_id, units in products.items():
            product = self.all_products[product_id]
            for unit in units:
                product.remove_unit(unit)
        order = Order(products)
        self.all_orders.append(order)

    def update_product(self, price: float, product_id: int) -> Product:
        product = self.all_products[product_id]
        product.set_price(price)
        return product

    def update_product(self, n_units: int, product_id: int, location_type: LocationType) -> Product:
        product = self.all_products[product_id]
        for _ in range(n_units):
            location = self.get_location_availability(location_type)
            if location:
                product.add_unit(location)
        return product

    def create_locations(self):
        # Implementation not provided in the original code
        pass