import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleMessageSubmit = () => {
    if (input.trim() !== '') {
      setMessages([...messages, { text: input, sender: 'user' }]);
      // Here you would typically call your chatbot API to get a response
      // For simplicity, let's just mimic a bot response here
      setTimeout(() => {
        setMessages([...messages, { text: 'This is a response from the chatbot.', sender: 'bot' }]);
      }, 500);
      setInput('');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Find a Flight Chatbot</h1>
      </header>
      <div className="Chat-container">
        <div className="Messages">
          {messages.map((message, index) => (
            <div key={index} className={`Message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </div>
        <div className="Input-container">
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleMessageSubmit();
              }
            }}
          />
          <button onClick={handleMessageSubmit}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
