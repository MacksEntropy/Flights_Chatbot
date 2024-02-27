import React, { useState, useEffect, createContext, useContext } from 'react';
import './App.css';

const ChatContext = createContext();

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    const storedMessages = JSON.parse(localStorage.getItem('chatMessages')) || [];
    setMessages(storedMessages);
  }, []);

  useEffect(() => {
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  const handleMessageSubmit = () => {
    if (input.trim() !== '') {
      const userMessage = { text: input, sender: 'user' };
      const botResponse = { text: 'This is a response from the chatbot.', sender: 'bot' };
  
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
