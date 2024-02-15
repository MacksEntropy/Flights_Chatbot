import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
origin_pattern = [{"LOWER": {"IN": ["from", "depart", "originating"]}}, {"POS": "PROPN", "OP": "+"}]
destination_pattern = [{"LOWER": {"IN": ["to", "destination", "arriving"]}}, {"POS": "PROPN", "OP": "+"}]
matcher.add("ORIGIN", [origin_pattern])
matcher.add("DESTINATION", [destination_pattern])

def extract_itinerary(text):
    doc = nlp(text)
    matches = matcher(doc)
    origin = None
    destination = None

    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "ORIGIN":
            origin = doc[start+1:end].text
        elif nlp.vocab.strings[match_id] == "DESTINATION":
            destination = doc[start+1:end].text
    return origin, destination

def confirm_itinerary(origin, dest):
    
    while not origin:
        print("Where are you leaving from?")
        o = input()
        origin_doc = nlp(o)
        origin = [ent for ent in origin_doc.ents if ent.label_ == "GPE"][0]

    while not dest:
        print("Where would you like to go?")
        d = input()
        dest_doc = nlp(d)
        dest = [ent for ent in dest_doc.ents if ent.label_ == "GPE"][0]

    print(f"Looking for flights from {origin} to {dest}")
    return origin, dest

def chatbot():

    print('Hello, how can I help you today?')
    user_input = input()
    origin, destination = extract_itinerary(user_input)
    confirm_itinerary(origin, destination)

if __name__ == "__main__":

    chatbot()