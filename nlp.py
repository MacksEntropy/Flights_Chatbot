import spacy
from spacy.matcher import Matcher
from datetime import datetime
from geonamescache import GeonamesCache

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
        gc = GeonamesCache()
        cities_dict = gc.get_cities()
        self.cities = [*self.gen_dict_extract(cities_dict, 'name')]

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
        
    def gen_dict_extract(self, var, key):
        if isinstance(var, dict):
            for k, v in var.items():
                if k == key:
                    yield v
                if isinstance(v, (dict, list)):
                    yield from self.gen_dict_extract(v, key)
        elif isinstance(var, list):
            for d in var:
                yield from self.gen_dict_extract(d, key)
        
    def validate_location(self, text):
        if text in self.cities:
            return True
        else:
            raise CityException(text)


    def extract_itinerary(self, text):

        doc = self.nlp(text)
        matches = self.matcher(doc)

        for match_id, start, end in matches:

            if self.nlp.vocab.strings[match_id] == "ORIGIN":
                location = doc[start+1:end].text
                if location in self.cities:
                    self.origin = location
                else:
                    raise CityException(location)

            elif self.nlp.vocab.strings[match_id] == "DESTINATION":
                location = doc[start+1:end].text
                if location in self.cities:
                    self.destination = location
                else:
                    raise CityException(location)

            elif self.nlp.vocab.strings[match_id] == "DATE":
                if self.validate_date(doc[start:end].text):
                    self.date = doc[start:end].text
                else:
                    raise DateException()

    def extract_location(self, text):
        """
        Helper function for extracting a location from an input
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
        
    # TODO Add self.numTickets here for variable ticket functionallity
    def is_empty(self):
        return True if not (self.origin or self.destination or self.date) else False
    
    # TODO Add self.numTickets here for variable ticket functionallity
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
    
class DateException(Exception):
    def __init__(self, message="Date is incorrectly formatted."):
        self.message = message
        super().__init__(self.message)

class CityException(Exception):
    def __init__(self, city):
        self.message = f"{city} not a city"
        self.city = city
        super().__init__(self.message)