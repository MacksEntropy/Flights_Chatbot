import spacy

nlp = spacy.load("en_core_web_sm")

def extract_destination(text):

    doc = nlp(text)
    # for ent in doc.ents:
    #     print(ent)
    return [ent for ent in doc.ents if ent.label_ == "GPE"]

if __name__ == "__main__":

    user_input = "I want to fight into Houston to turn off Google"
    print(extract_destination(user_input))