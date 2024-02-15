import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
origin_pattern = [{"LOWER": {"IN": ["from", "leave"]}}, {"POS": "PROPN", "OP": "+", "ENT_TYPE": "GPE"}]
destination_pattern = [{"LOWER": {"IN": ["to", "tour", "visit"]}}, {"POS": "PROPN", "OP": "+", "ENT_TYPE": "GPE"}]
date_pattern = [
    {"IS_DIGIT": True, "LENGTH": 4},  # Year
    {"TEXT": "-", "OP": "?"},
    {"IS_DIGIT": True, "LENGTH": 2},   # Month
    {"TEXT": "-", "OP": "?"},
    {"IS_DIGIT": True, "LENGTH": 2},   # Day
]
matcher.add("ORIGIN", [origin_pattern])
matcher.add("DESTINATION", [destination_pattern])
matcher.add("DATE", [date_pattern])

def extract_itinerary(text):

    doc = nlp(text)
    matches = matcher(doc)
    origin = None
    destination = None
    date = None

    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "ORIGIN":
            origin = doc[start+1:end].text
        elif nlp.vocab.strings[match_id] == "DESTINATION":
            destination = doc[start+1:end].text
        elif nlp.vocab.strings[match_id] == "DATE":
            date = doc[start:end].text
    return origin, destination, date

def confirm_itinerary(origin, dest, date):
    
    while not origin:
        print("What city are you leaving from?")
        o = input()
        origin_doc = nlp(o)
        origin = [ent for ent in origin_doc.ents if ent.label_ == "GPE"][0]

    while not dest:
        print("What city would you like to visit?")
        d = input()
        dest_doc = nlp(d)
        dest = [ent for ent in dest_doc.ents if ent.label_ == "GPE"][0]
    
    # Maybe replace with date picker in webapp
    while not date:
        print("What date are you looking to fly? (Please enter in YYYY-MM-DD format)")
        date_str = input()
        date_doc = nlp(date_str)
        for match_id, start, end in matcher(date_doc):
            matched_span = date_doc[start:end]
            date = matched_span.text

    # # Maybe replace with dropdown in webapp
    numTickets = None
    while not numTickets:
        print("How many tickets should I look for? (Must be greater than zero)")
        tickets = int(input())
        if tickets > 0: 
            numTickets = tickets

    print(f"Looking for {numTickets} ticket(s) from {origin} to {dest} on {date}")
    return origin, dest, date, numTickets

def chatbot():

    print('Hello, how can I help you today?')
    user_input = input()
    origin, destination, date = extract_itinerary(user_input)
    confirm_itinerary(origin, destination, date)

if __name__ == "__main__":

    chatbot()