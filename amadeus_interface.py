import os
from dotenv import load_dotenv

from amadeus import Client, ResponseError

load_dotenv()

amadeus = Client(
    client_id=os.getenv('AMADEUS_API_KEY'),
    client_secret=os.getenv("AMADEUS_PRIV_KEY")
)
try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='IAH',
        destinationLocationCode='LGA',
        departureDate='2024-02-15',
        adults=1)
    # Sort flight offers by grandTotal price (Price including fees)
    sorted_response = sorted(response.data, key=lambda x: x['price']['grandTotal'])[:6]
    print([x['price']['grandTotal'] for x in sorted_response])
except ResponseError as error:
    print(error)