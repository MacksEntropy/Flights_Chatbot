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
        # TODO Add ability to specify number of tickets
        self.numTickets = 1

    def validate_date(self, date_str):
        """
        Checks if the given date is not in the past. Must be in YYYY-MM-DD format
        """
        try:
            date_object = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now().date()
            return True if (date_object.date() >= today) else False
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

    def extract_location(self, text):
        """
        Helper function for extracting a location from a input sentence
        """
        doc = self.nlp(text)
        if not self.origin:
            orig = [ent for ent in doc.ents if ent.label_ == "GPE"][0]
            self.origin = orig.text

        if not self.destination:
            dest = [ent for ent in doc.ents if ent.label_ == "GPE"][0]
            self.destination = dest.text

    def is_complete(self):
        return True if (self.origin and self.destination and self.date and self.numTickets) else False
        
    def is_empty(self):
        return True if not (self.origin or self.destination or self.date) else False
    
    def reset(self):
        self.origin = None
        self.destination = None
        self.date = None

    def confirm_itinerary(self):
        
        if not self.origin:
            return "What city are you leaving from?"

        if not self.destination:
            return "What city would you like to visit?"
        
        # Maybe replace with date picker in webapp
        if not self.date:
            return "What date are you looking to fly? (Please enter in YYYY-MM-DD format)"
        
        return f"Looking for {self.numTickets} ticket(s) from {self.origin} to {self.destination} on {self.date}"