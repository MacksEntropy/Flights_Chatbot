import spacy

nlp = spacy.load("en_core_web_sm")

def extract_destination(text):
    doc = nlp(text)
    # TODO Figure out case where user specifies destination and location of departure. 
    return [ent for ent in doc.ents if ent.label_ == "GPE"]

def confirm_desination(dest):
    
    while not dest:
        print("Sorry, where would you like to go?")
        user_input = input()
        dest = extract_destination(user_input)
    print("Looking for flights to", dest[0])

def chatbot():

    print('Hello, how can I help you today?')
    user_input = input()
    destination = extract_destination(user_input)
    confirm_desination(destination)

if __name__ == "__main__":

    chatbot()