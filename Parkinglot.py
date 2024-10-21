# Enum for Vehicle Size
from enum import Enum

class VehicleSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

# Class representing a vehicle
class Vehicle:
    def __init__(self, license_plate, size):
        self.license_plate = license_plate
        self.size = size  # This should be a VehicleSize Enum value

# Class representing a parking spot
class ParkingSpot:
    def __init__(self, spot_id, size, floor, distances):
        self.spot_id = spot_id
        self.size = size  # VehicleSize Enum
        self.floor = floor  # The floor this spot belongs to
        self.is_occupied = False
        self.vehicle = None
        self.distances = distances  # Dictionary of distances to each entrance

    def can_fit_vehicle(self, vehicle):
        return not self.is_occupied and vehicle.size.value <= self.size.value

    def park_vehicle(self, vehicle):
        if self.can_fit_vehicle(vehicle):
            self.vehicle = vehicle
            self.is_occupied = True
            return True
        return False

    def remove_vehicle(self):
        if self.is_occupied:
            self.vehicle = None
            self.is_occupied = False
            return True
        return False

# Class representing the parking lot with multiple floors
class ParkingLot:
    def __init__(self, num_floors, spots_distances):
        """
        spots_distances: A dictionary where each key is a tuple (floor, spot_size), 
                         and value is a list of dictionaries representing spots' distances to each entrance.
                         Example: 
                         {
                            (1, VehicleSize.SMALL): [
                                {"spot_id": "S1_0", "distances": {"Entrance1": 10, "Entrance2": 15}},
                                {"spot_id": "S1_1", "distances": {"Entrance1": 12, "Entrance2": 17}}
                            ],
                            (2, VehicleSize.LARGE): [
                                {"spot_id": "B2_0", "distances": {"Entrance1": 30, "Entrance2": 40}},
                                ...
                            ]
                         }
        """
        self.spots = {}
        for (floor, size), spot_list in spots_distances.items():
            if floor not in self.spots:
                self.spots[floor] = {}
            self.spots[floor][size] = [ParkingSpot(spot["spot_id"], size, floor, spot["distances"]) for spot in spot_list]

    def find_closest_available_spot(self, vehicle, entrance):
        """
        Finds the closest available parking spot for a vehicle of a particular size
        based on the entrance used. It checks across all floors.
        """
        for floor in self.spots:
            # Create a list of spots based on vehicle size (smaller vehicles can park in larger spots)
            if vehicle.size == VehicleSize.SMALL:
                spot_list = self.spots[floor].get(VehicleSize.SMALL, []) + self.spots[floor].get(VehicleSize.MEDIUM, []) + self.spots[floor].get(VehicleSize.LARGE, [])
            elif vehicle.size == VehicleSize.MEDIUM:
                spot_list = self.spots[floor].get(VehicleSize.MEDIUM, []) + self.spots[floor].get(VehicleSize.LARGE, [])
            else:  # LARGE
                spot_list = self.spots[floor].get(VehicleSize.LARGE, [])

            # Filter available spots
            available_spots = [spot for spot in spot_list if not spot.is_occupied]

            # Sort available spots by distance to the specified entrance and return the closest one
            if available_spots:
                closest_spot = sorted(available_spots, key=lambda spot: spot.distances[entrance])[0]
                return closest_spot
        
        return None

    def park_vehicle(self, vehicle, entrance):
        spot = self.find_closest_available_spot(vehicle, entrance)
        if spot:
            spot.park_vehicle(vehicle)
            print(f'Vehicle {vehicle.license_plate} parked at spot {spot.spot_id}, floor {spot.floor}, distance to {entrance}: {spot.distances[entrance]}')
        else:
            print(f'No available spots for vehicle {vehicle.license_plate}')

    def leave_spot(self, vehicle_license_plate):
        for floor in self.spots:
            for size in self.spots[floor]:
                for spot in self.spots[floor][size]:
                    if spot.is_occupied and spot.vehicle.license_plate == vehicle_license_plate:
                        spot.remove_vehicle()
                        print(f'Vehicle {vehicle_license_plate} has left spot {spot.spot_id} on floor {spot.floor}')
                        return
        print(f'Vehicle {vehicle_license_plate} not found in the parking lot.')

    def display_available_spots(self):
        for floor in self.spots:
            print(f"Floor {floor}:")
            for size, spots in self.spots[floor].items():
                available = sum(1 for spot in spots if not spot.is_occupied)
                print(f"  Available {size.name} spots: {available}")

# Example usage
if __name__ == "__main__":
    # Define parking spots and distances
    spots_distances = {
        (1, VehicleSize.SMALL): [
            {"spot_id": "S1_0", "distances": {"Entrance1": 5, "Entrance2": 10}},
            {"spot_id": "S1_1", "distances": {"Entrance1": 6, "Entrance2": 11}}
        ],
        (1, VehicleSize.MEDIUM): [
            {"spot_id": "M1_0", "distances": {"Entrance1": 4, "Entrance2": 9}},
            {"spot_id": "M1_1", "distances": {"Entrance1": 7, "Entrance2": 8}}
        ],
        (2, VehicleSize.LARGE): [
            {"spot_id": "B2_0", "distances": {"Entrance1": 12, "Entrance2": 20}},
            {"spot_id": "B2_1", "distances": {"Entrance1": 15, "Entrance2": 18}}
        ]
    }

    # Create the parking lot with the given distances
    parking_lot = ParkingLot(num_floors=2, spots_distances=spots_distances)

    # Create some vehicles
    car1 = Vehicle("ABC123", VehicleSize.SMALL)
    car2 = Vehicle("XYZ987", VehicleSize.LARGE)
    car3 = Vehicle("LMN456", VehicleSize.MEDIUM)

    # Park vehicles
    parking_lot.park_vehicle(car1, "Entrance1")  # Parks at the closest spot based on Entrance1
    parking_lot.park_vehicle(car2, "Entrance2")  # Parks at the closest spot based on Entrance2
    parking_lot.park_vehicle(car3, "Entrance1")  # Parks at the closest spot based on Entrance1

    # Display available spots
    parking_lot.display_available_spots()

    # Car leaves the lot
    parking_lot.leave_spot("ABC123")

    # Display available spots again
    parking_lot.display_available_spots()
