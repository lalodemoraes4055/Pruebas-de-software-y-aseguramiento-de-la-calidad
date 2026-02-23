"""
Unit tests for the Reservation System.
Includes positive and negative test cases.
"""

import unittest
import os
from reservation_system import Hotel, Customer, Reservation, DataManager


class BaseTest(unittest.TestCase):
    """Base test class to handle setup and teardown of files."""

    @classmethod
    def setUpClass(cls):
        """Set up dummy file names for testing to protect real data."""
        Hotel.FILE_NAME = 'test_hotels.json'
        Customer.FILE_NAME = 'test_customers.json'
        Reservation.FILE_NAME = 'test_reservations.json'

    def setUp(self):
        """Clean up files before each test."""
        for filename in [Hotel.FILE_NAME, Customer.FILE_NAME,
                         Reservation.FILE_NAME]:
            if os.path.exists(filename):
                os.remove(filename)

    def tearDown(self):
        """Clean up files after each test."""
        for filename in [Hotel.FILE_NAME, Customer.FILE_NAME,
                         Reservation.FILE_NAME]:
            if os.path.exists(filename):
                os.remove(filename)


class TestHotel(BaseTest):
    """Test suite for Hotel class."""

    def test_create_hotel_success(self):
        """Test successful hotel creation."""
        result = Hotel.create_hotel(1, "Plaza", "NYC", 100)
        self.assertTrue(result)

    def test_create_hotel_duplicate(self):
        """Negative 1: Create duplicate hotel."""
        Hotel.create_hotel(1, "Plaza", "NYC", 100)
        result = Hotel.create_hotel(1, "Plaza 2", "LA", 50)
        self.assertFalse(result)

    def test_delete_hotel(self):
        """Test deleting a hotel."""
        Hotel.create_hotel(1, "Plaza", "NYC", 100)
        result = Hotel.delete_hotel(1)
        self.assertTrue(result)

    def test_delete_hotel_not_found(self):
        """Negative 2: Delete non-existent hotel."""
        result = Hotel.delete_hotel(99)
        self.assertFalse(result)

    def test_modify_and_display(self):
        """Test modifying and displaying hotel."""
        Hotel.create_hotel(1, "Plaza", "NYC", 100)
        Hotel.modify_hotel(1, name="Grand Plaza", location="Boston")
        info = Hotel.display_hotel(1)
        self.assertEqual(info["name"], "Grand Plaza")
        self.assertEqual(info["location"], "Boston")


class TestCustomer(BaseTest):
    """Test suite for Customer class."""

    def test_create_customer_success(self):
        """Test successful customer creation."""
        result = Customer.create_customer(1, "John", "j@m.com")
        self.assertTrue(result)

    def test_create_customer_duplicate(self):
        """Negative 3: Create duplicate customer."""
        Customer.create_customer(1, "John", "j@m.com")
        result = Customer.create_customer(1, "Jane", "ja@m.com")
        self.assertFalse(result)

    def test_delete_customer(self):
        """Test deleting a customer."""
        Customer.create_customer(1, "John", "j@m.com")
        result = Customer.delete_customer(1)
        self.assertTrue(result)

    def test_delete_customer_not_found(self):
        """Negative 4: Delete non-existent customer."""
        result = Customer.delete_customer(99)
        self.assertFalse(result)

    def test_modify_and_display(self):
        """Test modifying and displaying customer."""
        Customer.create_customer(1, "John", "j@m.com")
        Customer.modify_customer(1, name="John Doe", email="jd@m.com")
        info = Customer.display_customer(1)
        self.assertEqual(info["name"], "John Doe")


class TestReservation(BaseTest):
    """Test suite for Reservation class."""

    def test_create_reservation_success(self):
        """Test successful reservation."""
        Hotel.create_hotel(1, "Plaza", "NYC", 10)
        Customer.create_customer(1, "John", "j@m.com")
        result = Reservation.create_reservation(1, 1, 1)
        self.assertTrue(result)

    def test_create_reservation_duplicate(self):
        """Negative 5: Duplicate reservation ID."""
        Hotel.create_hotel(1, "Plaza", "NYC", 10)
        Customer.create_customer(1, "John", "j@m.com")
        Reservation.create_reservation(1, 1, 1)
        result = Reservation.create_reservation(1, 1, 1)
        self.assertFalse(result)

    def test_create_reservation_no_hotel(self):
        """Negative 6: Reserve with non-existent hotel."""
        result = Reservation.create_reservation(1, 1, 99)
        self.assertFalse(result)

    def test_create_reservation_no_rooms(self):
        """Negative 7: Reserve when no rooms available."""
        Hotel.create_hotel(1, "Plaza", "NYC", 0)
        result = Reservation.create_reservation(1, 1, 1)
        self.assertFalse(result)

    def test_cancel_reservation(self):
        """Test successful reservation cancellation."""
        Hotel.create_hotel(1, "Plaza", "NYC", 10)
        Customer.create_customer(1, "John", "j@m.com")
        Reservation.create_reservation(1, 1, 1)
        result = Reservation.cancel_reservation(1)
        self.assertTrue(result)

    def test_cancel_reservation_not_found(self):
        """Negative 8: Cancel non-existent reservation."""
        result = Reservation.cancel_reservation(99)
        self.assertFalse(result)


class TestDataManager(BaseTest):
    """Test suite for DataManager class."""

    def test_invalid_json(self):
        """Negative 9: Handle invalid JSON."""
        with open(Hotel.FILE_NAME, 'w', encoding='utf-8') as f:
            f.write("INVALID JSON")
        data = DataManager.load_data(Hotel.FILE_NAME)
        self.assertEqual(data, {})


if __name__ == '__main__':
    unittest.main()
