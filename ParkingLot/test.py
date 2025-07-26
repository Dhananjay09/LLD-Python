import unittest
from parking_lot import *

class TestParkingLot(unittest.TestCase):

    def setUp(self):
        self.parking_lot = ParkingLot(HourlyRateCalculator())
        self.parking_lot.add_slot(CarSlot("C1"))
        self.parking_lot.add_slot(BikeSlot("B1"))

    def test_park_and_unpark_car(self):
        car = Car("MH12XY1234")
        ticket = self.parking_lot.park_vehicle(car)
        self.assertTrue(ticket.slot.occupied)
        fee = self.parking_lot.unpark_vehicle(ticket.id)
        self.assertEqual(ticket.slot.occupied, False)
        self.assertGreaterEqual(fee, 10)

    def test_no_available_slot(self):
        self.parking_lot.park_vehicle(Car("C123"))
        with self.assertRaises(Exception):
            self.parking_lot.park_vehicle(Car("C124"))

    def test_fee_calculation(self):
        calculator = HourlyRateCalculator()
        start = datetime.now()
        end = start.replace(hour=start.hour + 1)
        fee = calculator.calculate(start, end)
        self.assertEqual(fee, 20)

    def test_ticket_uniqueness(self):
        car = Car("MH01AA1111")
        ticket1 = self.parking_lot.park_vehicle(car)
        self.parking_lot.unpark_vehicle(ticket1.id)
        car2 = Car("MH01AA2222")
        ticket2 = self.parking_lot.park_vehicle(car2)
        self.assertNotEqual(ticket1.id, ticket2.id)

if __name__ == '__main__':
    unittest.main()
