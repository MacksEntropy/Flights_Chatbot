from flask import Flask, request, jsonify
import requests
from flask_cors import CORS, cross_origin

from nlp import NLP, DateException
from amadeus_interface import Amadeus

app = Flask(__name__)
cors = CORS(app)
nlp = NLP()
amadeus = Amadeus()

@app.route("/chat", methods=["POST"])
def chat():

    flights = ['']
    error_text = ''
    try:
        input = request.json
        # For testing purposes
        # input = data.get('user_request')
        if nlp.is_complete():
            nlp.reset()

        try:
            if nlp.is_empty():
                nlp.extract_itinerary(input)
            elif not (nlp.origin and nlp.destination):
                try:
                    nlp.extract_location(input)
                except IndexError as e:
                    error_text = "Sorry I dont recognize that city, please choose another."
            elif not (nlp.date):
                nlp.extract_itinerary(input)
        except DateException as e:
            print(e)
            error_text = "Date is either incorrectly formatted or in the past. Please check your date and enter in as YYYY-MM-DD."
        
        check_text = nlp.confirm_itinerary()
        # For debugging purposes
        # response = {
        #         "origin" : nlp.origin,
        #         "destination" : nlp.destination,
        #         "date" : nlp.date,
        #         "numTickets" : nlp.numTickets
        #         }
        # print(response)
        
        if nlp.is_complete():
            orig_airport, dest_airport = amadeus.get_IATA_code(nlp.origin), amadeus.get_IATA_code(nlp.destination)
            flights = amadeus.find_flights(orig_airport, dest_airport, nlp.date, nlp.numTickets)

            if type(flights) == str:
                error_text = "Error in finding flights, please try again."



        origin = nlp.origin if nlp.origin else ''
        destination = nlp.destination if nlp.destination else ''
        date = nlp.date if nlp.date else ''

        if (origin and origin == destination):
            error_text = "Origin and destination cannot be the same, please try again."
            nlp.reset()

        text_response = error_text if error_text else check_text

        return jsonify({'text' : text_response, "origin" : origin, "destination" : destination, "date" : date, "flights" : flights})
    except Exception as e:
        return jsonify({'response' : e})

if __name__ == "__main__":
    app.run(debug=True)
