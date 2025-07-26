from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# ----------------- VEHICLES -----------------
class Vehicle(ABC):
    def __init__(self, number: str):
        self.number = number
        self.entry_time = datetime.now()

class Car(Vehicle):
    pass

class Bike(Vehicle):
    pass

class Truck(Vehicle):
    pass

# ----------------- PARKING SLOT -----------------
class ParkingSlot(ABC):
    def __init__(self, slot_id: str):
        self.slot_id = slot_id
        self.occupied = False
        self.vehicle = None

    def park(self, vehicle: Vehicle):
        self.occupied = True
        self.vehicle = vehicle

    def unpark(self):
        self.occupied = False
        self.vehicle = None

class CarSlot(ParkingSlot): pass
class BikeSlot(ParkingSlot): pass
class TruckSlot(ParkingSlot): pass

# ----------------- TICKET -----------------
class Ticket:
    def __init__(self, vehicle: Vehicle, slot: ParkingSlot):
        self.id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.slot = slot
        self.issued_at = datetime.now()

# ----------------- FEE STRATEGY -----------------
class FeeCalculator(ABC):
    @abstractmethod
    def calculate(self, entry_time: datetime, exit_time: datetime) -> float:
        pass

class FlatRateCalculator(FeeCalculator):
    def calculate(self, entry_time, exit_time):
        return 20  # flat rate

class HourlyRateCalculator(FeeCalculator):
    def calculate(self, entry_time, exit_time):
        hours = (exit_time - entry_time).seconds // 3600 + 1
        return hours * 10

# ----------------- TICKET MANAGER -----------------
class TicketManager:
    def __init__(self):
        self.active_tickets = {}

    def issue_ticket(self, vehicle: Vehicle, slot: ParkingSlot) -> Ticket:
        ticket = Ticket(vehicle, slot)
        self.active_tickets[ticket.id] = ticket
        return ticket

    def close_ticket(self, ticket_id: str):
        if ticket_id in self.active_tickets:
            return self.active_tickets.pop(ticket_id)
        return None

# ----------------- PARKING LOT -----------------
class ParkingLot:
    def __init__(self, fee_strategy: FeeCalculator):
        self.slots = []
        self.ticket_manager = TicketManager()
        self.fee_strategy = fee_strategy

    def add_slot(self, slot: ParkingSlot):
        self.slots.append(slot)

    def find_available_slot(self, vehicle: Vehicle) -> ParkingSlot:
        for slot in self.slots:
            if not slot.occupied and isinstance(slot, self._get_slot_type(vehicle)):
                return slot
        return None

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        slot = self.find_available_slot(vehicle)
        if not slot:
            raise Exception("No available slot")
        slot.park(vehicle)
        ticket = self.ticket_manager.issue_ticket(vehicle, slot)
        print(f"Ticket Issued: {ticket.id}")
        return ticket

    def unpark_vehicle(self, ticket_id: str):
        ticket = self.ticket_manager.close_ticket(ticket_id)
        if not ticket:
            raise Exception("Invalid ticket")
        exit_time = datetime.now()
        fee = self.fee_strategy.calculate(ticket.vehicle.entry_time, exit_time)
        ticket.slot.unpark()
        print(f"Vehicle {ticket.vehicle.number} exited. Fee: ₹{fee}")
        return fee

    def _get_slot_type(self, vehicle: Vehicle):
        if isinstance(vehicle, Car):
            return CarSlot
        elif isinstance(vehicle, Bike):
            return BikeSlot
        elif isinstance(vehicle, Truck):
            return TruckSlot
        else:
            raise Exception("Unsupported vehicle type")

# ----------------- Example Usage -----------------
if __name__ == "__main__":
    parking_lot = ParkingLot(fee_strategy=HourlyRateCalculator())

    # Setup slots
    parking_lot.add_slot(CarSlot("C1"))
    parking_lot.add_slot(BikeSlot("B1"))
    parking_lot.add_slot(TruckSlot("T1"))

    # Park vehicles
    car = Car("MH-12-XY-1234")
    ticket1 = parking_lot.park_vehicle(car)

    bike = Bike("MH-31-ZZ-1111")
    ticket2 = parking_lot.park_vehicle(bike)
    ticket3 = parking_lot.park_vehicle(bike)
    ticket4 = parking_lot.park_vehicle(car)
    ticket5 = parking_lot.park_vehicle(Truck("MH-31-ZZ-1111"))

    # Unpark vehicles
    parking_lot.unpark_vehicle(ticket1.id)
    parking_lot.unpark_vehicle(ticket2.id)
