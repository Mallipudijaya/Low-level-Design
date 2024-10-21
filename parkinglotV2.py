from enum import Enum
from typing import Dict, List, Set
from datetime import datetime

class VehicleType(Enum):
    BIKE = 1
    SEDAN = 2
    SUV = 3
    TRUCK = 4

class ParkingSlotType(Enum):
    TWOWHEELER = 1
    SMALL = 2
    MEDIUM = 3
    LARGE = 4

class Vehicle:
    def __init__(self, vehicle_id: int, vehicle_type: VehicleType):
        self.vehicle_id = vehicle_id
        self.type = vehicle_type

class ParkingSlot:
    def __init__(self, name: str):
        self.name = name
        self.parking_slot_type = None
        self.vehicle = None
        self.is_available = True

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.is_available = False

    def remove_vehicle(self):
        self.vehicle = None
        self.is_available = True

    def get_parking_slot_type(self) -> ParkingSlotType:
        return self.parking_slot_type

class ParkingFloor:
    def __init__(self, name: str):
        self.parking_floor_name = name
        self.parking_slots: Dict[ParkingSlotType, List[ParkingSlot]] = {}

    def get_parking_slot_type(self, vehicle: Vehicle) -> ParkingSlotType:
        if vehicle.type == VehicleType.BIKE:
            return ParkingSlotType.TWOWHEELER
        elif vehicle.type == VehicleType.SEDAN:
            return ParkingSlotType.SMALL
        elif vehicle.type == VehicleType.SUV:
            return ParkingSlotType.MEDIUM
        else:
            return ParkingSlotType.LARGE

    def add_parking_slots(self, parking_slot: ParkingSlot, parking_slot_type: ParkingSlotType):
        if parking_slot_type not in self.parking_slots:
            self.parking_slots[parking_slot_type] = []
        self.parking_slots[parking_slot_type].append(parking_slot)

    def assign_slot(self, vehicle: Vehicle) -> ParkingSlot:
        parking_slot_type = self.get_parking_slot_type(vehicle)
        for parking_slot in self.parking_slots.get(parking_slot_type, []):
            if parking_slot.is_available:
                parking_slot.add_vehicle(vehicle)
                return parking_slot
        return None

    def remove_slot(self, vehicle: Vehicle):
        for slots in self.parking_slots.values():
            for slot in slots:
                if slot.vehicle == vehicle:
                    slot.remove_vehicle()
                    return

class Ticket:
    def __init__(self, ticket_id: int, vehicle: Vehicle, parking_slot: ParkingSlot):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.parking_slot = parking_slot
        self.start_time = datetime.now()
        self.end_time = None

    def calculate_duration(self) -> float:
        if self.end_time is None:
            self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds() / 3600  # in hours
        return duration

    def calculate_price(self) -> float:
        duration = self.calculate_duration()
        price_per_hour = 0.01
        if self.parking_slot.get_parking_slot_type() == ParkingSlotType.TWOWHEELER:
            price_per_hour += 0.01
        elif self.parking_slot.get_parking_slot_type() == ParkingSlotType.SMALL:
            price_per_hour += 0.02
        elif self.parking_slot.get_parking_slot_type() == ParkingSlotType.MEDIUM:
            price_per_hour += 0.03
        elif self.parking_slot.get_parking_slot_type() == ParkingSlotType.LARGE:
            price_per_hour += 0.04
        return duration * price_per_hour

    def get_ticket_parking_slot(self) -> ParkingSlot:
        return self.parking_slot

class ParkingLot:
    _instance = None

    def __init__(self, name: str):
        if ParkingLot._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.parking_lot_name = name
            self.parking_floors: Set[ParkingFloor] = set()
            ParkingLot._instance = self

    @staticmethod
    def create_parking_lot(name: str) -> 'ParkingLot':
        if ParkingLot._instance is None:
            ParkingLot._instance = ParkingLot(name)
        return ParkingLot._instance

    def add_floor(self, floor: ParkingFloor):
        self.parking_floors.add(floor)

    def remove_floor(self, floor: ParkingFloor):
        self.parking_floors.remove(floor)

    def get_parking_slot(self, vehicle: Vehicle) -> Ticket:
        for parking_floor in self.parking_floors:
            parking_slot = parking_floor.assign_slot(vehicle)
            if parking_slot is not None:
                return Ticket(len(self.parking_floors), vehicle, parking_slot)
        return None

    def remove_parking_slot(self, ticket: Ticket) -> float:
        price = ticket.calculate_price()
        vehicle = ticket.vehicle
        parking_slot = ticket.get_ticket_parking_slot()
        parking_slot.remove_vehicle()
        return price