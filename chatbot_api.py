from flask import Flask, request, jsonify
import requests

from nlp import NLP

app = Flask(__name__)
nlp = NLP()

@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.json
        input = data.get('user_request')

        if nlp.is_empty():
            nlp.extract_itinerary(input)
        elif not (nlp.origin and nlp.destination):
            nlp.extract_location(input)     
        elif not (nlp.date):
            nlp.extract_itinerary(input)
        
        check_text = nlp.confirm_itinerary()
        response = {
                "origin" : nlp.origin,
                "destination" : nlp.destination,
                "date" : nlp.date,
                "numTickets" : nlp.numTickets
                }
        
        return jsonify({'text' : check_text, 'response' : response})
    except Exception as e:
        return jsonify({'response' : e})

if __name__ == "__main__":
    app.run(debug=True)
