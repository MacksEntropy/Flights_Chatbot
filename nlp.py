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
        origin = None
        destination = None
        date = None

        for match_id, start, end in matches:
            if self.nlp.vocab.strings[match_id] == "ORIGIN":
                origin = doc[start+1:end].text
            elif self.nlp.vocab.strings[match_id] == "DESTINATION":
                destination = doc[start+1:end].text
            elif self.nlp.vocab.strings[match_id] == "DATE":
                date = doc[start:end].text
        return origin, destination, date
    
    def extract_location(self, text):
        """
        Helper function for extracting a location from a input sentence
        """
        doc = self.nlp(text)
        return [ent for ent in doc.ents if ent.label_ == "GPE"][0]

    def confirm_itinerary(self, origin, dest, date):
        
        while not origin:
            print("What city are you leaving from?")
            o = input()
            origin_doc = self.nlp(o)
            origin = [ent for ent in origin_doc.ents if ent.label_ == "GPE"][0]

        while not dest:
            print("What city would you like to visit?")
            d = input()
            dest_doc = self.nlp(d)
            dest = [ent for ent in dest_doc.ents if ent.label_ == "GPE"][0]
        
        # Maybe replace with date picker in webapp
        while not date:
            print("What date are you looking to fly? (Please enter in YYYY-MM-DD format)")
            date_str = input()
            date_doc = self.nlp(date_str)
            for match_id, start, end in self.matcher(date_doc):
                matched_span = date_doc[start:end]
                if self.validate_date(matched_span.text):
                    date = matched_span.text
                else:
                    print("Invalid date")

        # Maybe replace with dropdown in webapp
        numTickets = None
        while not numTickets:
            print("How many tickets should I look for? (Must be greater than zero)")
            tickets = int(input())
            if tickets > 0: 
                numTickets = tickets
        return origin, dest, date, numTickets 

if __name__ == "__main__":

    nlp = NLP()
    print('Hello, how can I help you today?')
    user_input = input()
    origin, destination, date = nlp.extract_itinerary(user_input)
    orig, dest, date, numTickets = nlp.confirm_itinerary(origin, destination, date)
    print(f"Looking for {numTickets} ticket(s) from {orig} to {dest} on {date}")