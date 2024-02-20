from flask import Flask, request, jsonify
import requests

from nlp import NLP

app = Flask(__name__)

# Define a route to handle incoming chatbot requests
@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.json
        words = data.get('user_request')
        nlp = NLP()
        origin, destination, date = nlp.extract_itinerary(words)
        response = {
            "origin" : origin,
            "destination" : destination,
            "date" : date
            }
        return jsonify({'response' : response})
    except Exception as e:
        return jsonify({'response' : e})

if __name__ == "__main__":
    app.run(debug=True)
