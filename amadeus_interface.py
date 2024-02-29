import os
from dotenv import load_dotenv
from datetime import datetime

from amadeus import Client, ResponseError
from currency_converter import CurrencyConverter

load_dotenv()

class Amadeus():

    def __init__(self) -> None:
        self.amadeus = Client(
            client_id=os.getenv('AMADEUS_API_KEY'),
            client_secret=os.getenv("AMADEUS_PRIV_KEY")
        )

    def get_IATA_code(self, city : str) -> str:
        """
        Gets the IATA codes for the top airport in a given city
        """
        try:
            response = self.amadeus.reference_data.locations.get(
            keyword=city,
            subType=["AIRPORT"])
            return response.data[0]['iataCode']
        except ResponseError as error:
            print(error)

    def find_flights(self, origin : str, dest : str, departure_date: str, num_adults: int) -> list[str]:
        """
        :param origin: IATA Code for origin Airport. EX: 'IAH'
        :param dest:  IATA Code for desination Airport. EX: 'LGA'
        :param departure_date: Desired date of flight in YYYY-MM-DD format. EX:'2024-02-15'
        :param num_adults: The number of adult tickets

        :returns List of top 3 cheapest flights 
        """
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=dest,
                departureDate=departure_date,
                adults=num_adults)
            # Sort flight offers by grandTotal price (Price including fees)
            flight_list = sorted(response.data, key=lambda x: x['price']['grandTotal'])[:3]
            return self.format_flight_list(flight_list)
        except ResponseError as error:
            print(error)
            return f"Error in finding flights: {error}"

    def convert_departure_arrival(self, iso_datetime):

        parsed_datetime = datetime.fromisoformat(iso_datetime)
        month = parsed_datetime.strftime("%B")  # Full month name
        day = parsed_datetime.day
        year = parsed_datetime.year
        hour_minute = parsed_datetime.strftime("%I:%M %p")  # Hour:Minute AM/PM format
        formatted_datetime = f"{month} {day}, {year} {hour_minute}"
        return formatted_datetime

    def convert_last_day_to_book(self, date_str):

        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%B %d, %Y")
        return formatted_date

    def format_flight_list(self, flight_list):

        c = CurrencyConverter()
        formatted_response = []
        for flight in flight_list:
                formatted_response.append(
                {
                    "departure" : self.convert_departure_arrival(flight['itineraries'][0]['segments'][0]['departure']['at']),
                    "arrival" : self.convert_departure_arrival(flight['itineraries'][0]['segments'][0]['arrival']['at']),
                    "price" : f"${round(c.convert(flight['price']['grandTotal'], 'EUR', 'USD'), 2)} USD",
                    "numSeatsRemaining" : flight['numberOfBookableSeats'],
                })    
        return formatted_response

if __name__ == "__main__":

    flightAPI = Amadeus()
    print(flightAPI.find_flights('IAH', 'LGA', '2024-10-15', 1))
    # print(flightAPI.get_IATA_code("New York"))
