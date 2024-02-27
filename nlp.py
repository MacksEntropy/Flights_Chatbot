import spacy
from spacy.matcher import Matcher
from datetime import datetime

class NLP():

    def __init__(self) -> None:
        
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)
        origin_pattern = [{"LOWER": {"IN": ["from", "leave"]}}, {"POS": "PROPN", "OP": "+", "ENT_TYPE": "GPE"}]
        destination_pattern = [{"LOWER": {"IN": ["to", "tour", "visit"]}}, {"POS": "PROPN", "OP": "+", "ENT_TYPE": "GPE"}]
        date_pattern = [
            {"IS_DIGIT": True, "LENGTH": 4},  # Year
            {"TEXT": "-", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": 2},   # Month
            {"TEXT": "-", "OP": "?"},
            {"IS_DIGIT": True, "LENGTH": 2},   # Day
        ]
        self.matcher.add("ORIGIN", [origin_pattern])
        self.matcher.add("DESTINATION", [destination_pattern])
        self.matcher.add("DATE", [date_pattern])

        self.origin = None
        self.destination = None
        self.date = None
        self.numTickets = None

    def validate_date(self, date_str):
        try:
            # Parse the string into a datetime object
            date_object = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Get today's date
            today = datetime.now().date()
            
            # Check if the parsed date is not in the past
            if date_object.date() >= today:
                return True
            else:
                return False
        except ValueError:
            return False

    def extract_itinerary(self, text):

        doc = self.nlp(text)
        matches = self.matcher(doc)

        for match_id, start, end in matches:

            if self.nlp.vocab.strings[match_id] == "ORIGIN":
                self.origin = doc[start+1:end].text

            elif self.nlp.vocab.strings[match_id] == "DESTINATION":
                self.destination = doc[start+1:end].text

            elif self.nlp.vocab.strings[match_id] == "DATE":
                if self.validate_date(doc[start:end].text):
                    self.date = doc[start:end].text


    def confirm_itinerary(self):
        
        if not self.origin:
            return "What city are you leaving from?"

        if not self.destination:
            return "What city would you like to visit?"
        
        # Maybe replace with date picker in webapp
        if not self.date:
            return "What date are you looking to fly? (Please enter in YYYY-MM-DD format)"

# if __name__ == "__main__":

    # nlp = NLP()
    # print('Hello, how can I help you today?')
    # user_input = input()
    # nlp.extract_itinerary(user_input)
    # orig, dest, date, numTickets = nlp.confirm_itinerary(origin, destination, date)
    # print(f"Looking for {numTickets} ticket(s) from {orig} to {dest} on {date}")