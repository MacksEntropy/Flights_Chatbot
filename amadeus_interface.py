import os
from dotenv import load_dotenv
from datetime import datetime

from amadeus import Client, ResponseError
from currency_converter import CurrencyConverter

load_dotenv()

amadeus = Client(
    client_id=os.getenv('AMADEUS_API_KEY'),
    client_secret=os.getenv("AMADEUS_PRIV_KEY")
)

def find_flights(origin : str, dest : str, departure_date: str, num_adults: int) -> list[str]:
    """
    :param origin: IATA Code for origin Airport. EX: 'IAH'
    :param dest:  IATA Code for desination Airport. EX: 'LGA'
    :param departure_date: Desired date of flight in YYYY-MM-DD format. EX:'2024-02-15'
    :param num_adults: The number of adult tickets

    :returns List of top 3 cheapest flights 
    """
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=dest,
            departureDate=departure_date,
            adults=num_adults)
        # Sort flight offers by grandTotal price (Price including fees)
        return sorted(response.data, key=lambda x: x['price']['grandTotal'])[:3]
    except ResponseError as error:
        print(error)

def convert_departure_arrival(iso_datetime):

    parsed_datetime = datetime.fromisoformat(iso_datetime)
    month = parsed_datetime.strftime("%B")  # Full month name
    day = parsed_datetime.day
    year = parsed_datetime.year
    hour_minute = parsed_datetime.strftime("%I:%M %p")  # Hour:Minute AM/PM format
    formatted_datetime = f"{month} {day}, {year} {hour_minute}"
    return formatted_datetime

def convert_last_day_to_book(date_str):

    parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = parsed_date.strftime("%B %d, %Y")
    return formatted_date

def format_response(flight_list):

    c = CurrencyConverter()
    formatted_response = []
    for flight in flight_list:
            formatted_response.append(
            {
                "departure" : convert_departure_arrival(flight['itineraries'][0]['segments'][0]['departure']['at']),
                "arrival" : convert_departure_arrival(flight['itineraries'][0]['segments'][0]['arrival']['at']),
                "price" : f"${round(c.convert(flight['price']['grandTotal'], 'EUR', 'USD'), 2)} USD",
                "lastDayToBook" : convert_last_day_to_book(flight['lastTicketingDate']),
                "numSeatsRemaining" : flight['numberOfBookableSeats'],
            })    
    return formatted_response

if __name__ == "__main__":
    flight_list = find_flights('IAH', 'LGA', '2024-02-15', 1)
    print(format_response(flight_list))