import React, { useState, useEffect } from 'react';

function App() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetch('/api/messages')
      .then(response => response.json())
      .then(data => setMessages(data))
      .catch(error => console.error('Error fetching messages:', error));
  }, []);

  return (
    <div>
      <h1>Slack Message Dashboard</h1>
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>User</th>
            <th>Message</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {messages.map(message => (
            <tr key={message.ts}>
              <td>{message.ts}</td>
              <td>{message.user}</td>
              <td>{message.text}</td>
              <td>{message.category}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
