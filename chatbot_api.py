from flask import Flask, request, jsonify
import requests

from nlp import NLP

app = Flask(__name__)
nlp = NLP()

# Define a route to handle incoming chatbot requests
@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.json
        words = data.get('user_request')
        nlp.extract_itinerary(words)
        confirmation_text = nlp.confirm_itinerary()
        response = {
            "origin" : nlp.origin,
            "destination" : nlp.destination,
            "date" : nlp.date
            }
        return jsonify({'text' : confirmation_text, 'response' : response})
    except Exception as e:
        return jsonify({'response' : e})

if __name__ == "__main__":
    app.run(debug=True)
