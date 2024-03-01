import React, { useState, useEffect, createContext, useContext } from 'react';
import './App.css'; 

const ChatContext = createContext();

const test_json = {
  "origin": "Houston",
  "destination": "New York",
  "date": "2024-05-05",
  "flights": [
      {
          "arrival": "March 28, 2024 09:47 AM",
          "departure": "March 28, 2024 07:30 AM",
          "numSeatsRemaining": 7,
          "price": "$1290.24 USD"
      },
      {
          "arrival": "March 28, 2024 12:33 PM",
          "departure": "March 28, 2024 09:30 AM",
          "numSeatsRemaining": 7,
          "price": "$1609.25 USD"
      },
      {
          "arrival": "March 28, 2024 03:35 PM",
          "departure": "March 28, 2024 12:30 PM",
          "numSeatsRemaining": 7,
          "price": "$1609.25 USD"
      }
  ]
}

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading ] = useState(false);

  useEffect(() => {
    const storedMessages = JSON.parse(localStorage.getItem('chatMessages')) || [];
    setMessages(storedMessages);
  }, []);

  useEffect(() => {
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  // TODO Finish formatting of final response
  
  // function formatDictList(dictList) {
  //   let result = "";
  //   dictList.forEach((dictionary, index) => {
  //       Object.entries(dictionary).forEach(([key, value]) => {
  //           result += `${key}: ${value}\n`;
  //       });
  //       result += "\n"; // Add a new line between dictionaries
  //       if (index !== dictList.length - 1) {
  //           result += "\n"; // Add an additional new line if it's not the last dictionary
  //       }
  //   });
  //   return result;
  // }

  // function formatData(flights_json) {
  //   const {origin, destination, date, flights} = flights_json

  //   return (`I found ${flights.length} flights from ${origin} to ${destination} on ${date}: \n ${formatDictList(flights)}`
  //   );
  // }

  async function postData(data) {
    const url = "http://127.0.0.1:5000/chat"
    setLoading(true);
    try {
        return await fetch(url, {
        method: 'POST',
        headers: {
          "access-control-allow-origin" : "*",
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      }).then(response => response.json())
      .then(data => {
        console.log("data.text is ",data.text)
        setLoading(false)
        return data.text
      });
    } catch (error) { 
      setLoading(false)
      console.log("Error!!!!!!")
      console.log(error);
    }
  }

  const handleMessageSubmit = async () => {
    if (input.trim() !== '') {
      const userMessage = { text: input, sender: 'user' };
      const botText = await postData(input)
      // const formatted_data = formatData(test_json)
      const botResponse = { text: botText, sender: 'bot' };
      setMessages([...messages, userMessage, botResponse]);
      setInput('');
    }
  };

  return (
    <ChatContext.Provider value={{ messages, setMessages }}>
      <div className="App">
        <header className="App-header">
          <h1>Flights Chatbot</h1>
        </header>
        <p>
          Hello, I am a chatbot made to find flights for you! From where to where would you like to fly?
        </p>
        <div className="Chat-container">
          <ChatMessages />
          <div className="Input-container">
            <input
              type="text"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleMessageSubmit();
                }
              }}
            />
            <button onClick={handleMessageSubmit}>Send</button>
          </div>
        </div>
      </div>
    </ChatContext.Provider>
  );
}

function ChatMessages() {
  const { messages } = useContext(ChatContext);

  return (
    <div className="Messages">
      {messages.map((message, index) => (
        <div key={index} className={`Message ${message.sender}`}>
          {message.text}
        </div>
      ))}
    </div>
  );
}

export default App;
