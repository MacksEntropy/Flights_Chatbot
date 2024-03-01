from flask import Flask, request, jsonify
import requests
from flask_cors import CORS, cross_origin

from nlp import NLP
from amadeus_interface import Amadeus

app = Flask(__name__)
cors = CORS(app)
nlp = NLP()
amadeus = Amadeus()

@app.route("/chat", methods=["POST"])
def chat():

    flights = ['']
    try:
        input = request.json
        # For testing purposes
        # input = data.get('user_request')
        if nlp.is_complete():
            nlp.reset()
            
        if nlp.is_empty():
            nlp.extract_itinerary(input)
        elif not (nlp.origin and nlp.destination):
            nlp.extract_location(input)     
        elif not (nlp.date):
            nlp.extract_itinerary(input)
        
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
                check_text = "Error in finding flights, please try again."

        origin = nlp.origin if nlp.origin else ''
        destination = nlp.destination if nlp.destination else ''
        date = nlp.date if nlp.date else ''

        return jsonify({'text' : check_text, "origin" : origin, "destination" : destination, "date" : date, "flights" : flights})
    except Exception as e:
        return jsonify({'response' : e})

if __name__ == "__main__":
    app.run(debug=True)
