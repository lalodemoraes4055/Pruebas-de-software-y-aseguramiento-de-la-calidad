"""
Reservation System Module.
Handles Hotels, Customers, and Reservations with JSON persistence.
"""

import json
import os


class DataManager:
    """Helper class to handle JSON file operations."""

    @staticmethod
    def load_data(filename):
        """Loads data from a JSON file."""
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Invalid JSON in {filename}. Returning empty.")
            return {}
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Unexpected error loading {filename}: {e}")
            return {}

    @staticmethod
    def save_data(filename, data):
        """Saves data to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Unexpected error saving to {filename}: {e}")


class Hotel:
    """Class representing a Hotel."""
    FILE_NAME = 'hotels.json'

    def __init__(self, hotel_id, name, location, total_rooms):
        self.hotel_id = str(hotel_id)
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms

    def to_dict(self):
        """Converts hotel object to dictionary."""
        return {
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms
        }

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms):
        """Creates a new hotel and saves it to the file."""
        data = DataManager.load_data(cls.FILE_NAME)
        if str(hotel_id) in data:
            print(f"Error: Hotel ID {hotel_id} already exists.")
            return False
        new_hotel = cls(hotel_id, name, location, rooms)
        data[str(hotel_id)] = new_hotel.to_dict()
        DataManager.save_data(cls.FILE_NAME, data)
        return True

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Deletes a hotel by ID."""
        data = DataManager.load_data(cls.FILE_NAME)
        if str(hotel_id) in data:
            del data[str(hotel_id)]
            DataManager.save_data(cls.FILE_NAME, data)
            return True
        print(f"Error: Hotel ID {hotel_id} not found.")
        return False

    @classmethod
    def display_hotel(cls, hotel_id):
        """Displays hotel information."""
        data = DataManager.load_data(cls.FILE_NAME)
        return data.get(str(hotel_id), "Hotel not found.")

    @classmethod
    def modify_hotel(cls, hotel_id, name=None, location=None):
        """Modifies hotel attributes."""
        data = DataManager.load_data(cls.FILE_NAME)
        hid = str(hotel_id)
        if hid in data:
            if name:
                data[hid]["name"] = name
            if location:
                data[hid]["location"] = location
            DataManager.save_data(cls.FILE_NAME, data)
            return True
        return False


class Customer:
    """Class representing a Customer."""
    FILE_NAME = 'customers.json'

    def __init__(self, customer_id, name, email):
        self.customer_id = str(customer_id)
        self.name = name
        self.email = email

    def to_dict(self):
        """Converts customer object to dictionary."""
        return {"name": self.name, "email": self.email}

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Creates a new customer."""
        data = DataManager.load_data(cls.FILE_NAME)
        if str(customer_id) in data:
            print(f"Error: Customer ID {customer_id} already exists.")
            return False
        new_customer = cls(customer_id, name, email)
        data[str(customer_id)] = new_customer.to_dict()
        DataManager.save_data(cls.FILE_NAME, data)
        return True

    @classmethod
    def delete_customer(cls, customer_id):
        """Deletes a customer by ID."""
        data = DataManager.load_data(cls.FILE_NAME)
        if str(customer_id) in data:
            del data[str(customer_id)]
            DataManager.save_data(cls.FILE_NAME, data)
            return True
        return False

    @classmethod
    def display_customer(cls, customer_id):
        """Displays customer information."""
        data = DataManager.load_data(cls.FILE_NAME)
        return data.get(str(customer_id), "Customer not found.")

    @classmethod
    def modify_customer(cls, customer_id, name=None, email=None):
        """Modifies customer attributes."""
        data = DataManager.load_data(cls.FILE_NAME)
        cid = str(customer_id)
        if cid in data:
            if name:
                data[cid]["name"] = name
            if email:
                data[cid]["email"] = email
            DataManager.save_data(cls.FILE_NAME, data)
            return True
        return False


class Reservation:
    """Class representing a Reservation."""
    FILE_NAME = 'reservations.json'

    @classmethod
    def create_reservation(cls, res_id, customer_id, hotel_id):
        """Creates a reservation if the hotel has available rooms."""
        res_data = DataManager.load_data(cls.FILE_NAME)
        if str(res_id) in res_data:
            print("Error: Reservation ID already exists.")
            return False

        hotel_data = DataManager.load_data(Hotel.FILE_NAME)
        if str(hotel_id) not in hotel_data:
            print("Error: Hotel does not exist.")
            return False

        if hotel_data[str(hotel_id)]["available_rooms"] > 0:
            hotel_data[str(hotel_id)]["available_rooms"] -= 1
            DataManager.save_data(Hotel.FILE_NAME, hotel_data)

            res_data[str(res_id)] = {
                "customer_id": str(customer_id),
                "hotel_id": str(hotel_id)
            }
            DataManager.save_data(cls.FILE_NAME, res_data)
            return True
        print("Error: No rooms available.")
        return False

    @classmethod
    def cancel_reservation(cls, res_id):
        """Cancels a reservation and frees up the room."""
        res_data = DataManager.load_data(cls.FILE_NAME)
        if str(res_id) not in res_data:
            print("Error: Reservation not found.")
            return False

        hotel_id = res_data[str(res_id)]["hotel_id"]
        hotel_data = DataManager.load_data(Hotel.FILE_NAME)

        if hotel_id in hotel_data:
            hotel_data[hotel_id]["available_rooms"] += 1
            DataManager.save_data(Hotel.FILE_NAME, hotel_data)

        del res_data[str(res_id)]
        DataManager.save_data(cls.FILE_NAME, res_data)
        return True
