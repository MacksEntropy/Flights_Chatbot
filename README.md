## Using the Chatbot

First start up the virtual environment by running `pipenv shell` while in the main directory. Then start up the middleware server by running the `chatbot_api.py` file. Finally, boot up the UI by navigating to the `/webapp` directory and running `npm start`. An internet connection is required. 

## Improvements 

- Improve how nlp module identifies proper nouns (see propn_feature branch)
- Add return date feature
- Improve how UI handles when amadeus interface is called
    - Add loading spinner while API call completes
    - Look into how to improve preformace here
- Improve how flight recommendations are displayed in the UI
- Add feature for recommending flights based on sentiment / amenities (I want to go somewhere warm, go somewhere with a beach, etc...)