import json

from services.base import Base
from fastapi import APIRouter, HTTPException
from models.Models import Location
from fastapi.responses import JSONResponse

LOCATIONS = []


class Locations(Base):
    def __init__(self, root_path, is_debug=False):
        """Initialiseert de Locations-klasse met een pad naar het data-bestand.

        Args:
            root_path (str): Het basispad waar het JSON-data-bestand zich bevindt.
            is_debug (bool): Bepaalt of de klasse met debugdata moet worden geladen.
        """
        self.data_path = root_path + "locations.json"
        self.is_debug = is_debug
        self.load(is_debug)
        self.router = APIRouter()

        self.router.add_api_route(
            "/locations/", self.get_locations, methods=["GET"])
        self.router.add_api_route(
            "/locations/{location_id}", self.get_location, methods=["GET"])
        self.router.add_api_route(
            "/locations/", self.add_location, methods=["POST"])
        self.router.add_api_route(
            "/locations/{location_id}", self.update_location, methods=["PUT"])
        self.router.add_api_route(
            "/locations/{location_id}", self.remove_location, methods=["DELETE"])

    def get_locations(self):
        """Haalt alle locaties op uit de data.

        Returns:
            list: Een lijst met alle locaties.
        """
        return self.data

    def get_location(self, location_id: int):
        """Zoekt en retourneert een specifieke locatie op basis van het locatie-ID.

        Args:
            location_id (int): Het ID van de locatie om het op te halen.

        Returns:
            dict or None: De locatiegegevens als een dictionary als deze bestaat, anders None.
        """
        for location in self.data:
            if location["id"] == location_id:
                return location
        return None

    def get_locations_in_warehouse(self, warehouse_id: int):
        # Het haalt alle locaties op binnen een specifiek magazijn.
        # Args: warehouse_id (int): Het ID van het magazijn.
        # Returns: list: Een lijst met locaties binnen het opgegeven magazijn.
        # Deze methode wordt gebruikt door warehouses.py

        locations_in_warehouse = []
        # Doorloop alle locaties in de data
        for location in self.data:
            if location["warehouse_id"] == warehouse_id:
                locations_in_warehouse.append(location)
        if not locations_in_warehouse:
            raise HTTPException(status_code=400,
                                detail=f"No locations found with {warehouse_id} warehouse ID.")
        return locations_in_warehouse

    def add_location(self, location: Location):
        """Voegt een nieuwe locatie toe aan de data met tijdstempels voor aanmaak en update.

        Args:
            location (dict): De gegevens van de locatie om toe te voegen.
        """
        location_dictionary = location.model_dump()
        location_dictionary["created_at"] = self.get_timestamp()
        location_dictionary["updated_at"] = self.get_timestamp()
        self.data.append(location_dictionary)
        if not self.is_debug:
            self.save()
            raise HTTPException(status_code=200,
                                detail=f"Location has been added!")
        raise HTTPException(status_code=400,
                            detail=f"Location couldn't be added.")

    def update_location(self, location_id: int, location: Location):
        """Werk een bestaande locatie bij op basis van het locatie-ID.

        Args:
            location_id (int): Het ID van de locatie om bij te werken.
            location (dict): De bijgewerkte locatiegegevens.
        """
        location_dictionary = location.model_dump()
        location_dictionary["updated_at"] = self.get_timestamp()
        for index in range(len(self.data)):
            if self.data[index]["id"] == location_id:
                self.data[index] = location_dictionary
        if not self.is_debug:
            self.save()
            raise HTTPException(status_code=200,
                                detail=f"Location has been added!")

    def remove_location(self, location_id):
        """Verwijdert een locatie uit de data op basis van het locatie-ID.

        Args:
            location_id (int): Het ID van de locatie om te verwijderen.
        """
        try:
            for location in self.data:
                if location["id"] == location_id:
                    self.data.remove(location)
        except Exception as e:
            print(e)

    def load(self, is_debug):
        """Laadt de locatiegegevens uit een JSON-bestand of uit een debuglijst.

        Args:
            is_debug (bool): Bepaalt of debuggegevens moeten worden gebruikt.
        """
        if is_debug:
            self.data = LOCATIONS
        else:
            f = open(self.data_path, "r")
            self.data = json.load(f)
            f.close()

    def save(self):
        """Slaat de locatiegegevens op in een JSON-bestand."""
        f = open(self.data_path, "w")
        json.dump(self.data, f)
        f.close()
