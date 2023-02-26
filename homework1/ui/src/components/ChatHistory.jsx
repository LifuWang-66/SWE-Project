import React from "react";

var history_resumed = false
const ChatHistory = ({ history }) => {
  const username = localStorage.getItem('username')
  const handleClick = () => {
    console.log(history_resumed)
    if (!history_resumed) {
      fetch(`http://flask-api/chat_history`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          username: username,
        })
      })
      .then(res => {
        if (!res.ok) {
          console.error('Response not OK:', res.status, res.statusText);
          throw new Error(res.statusText);
        }
        return res.json();
      })
      .then(data => {
        if (!data.chat_history) {
          console.log(data)
        } else {
          for (var i = 0; i < data.chat_history.length; i++) {
            history.push(data.chat_history[i]);
          }   
          history_resumed = true    
        }
      });
    }
  }
  // TODO: make the history clickable, and can resume history chat
  return (
    <div>
      <button onClick={handleClick}>Resume History</button>
      <ul className="history-list">
        {history.map((item, index) => (
          <li key={index}>
            <div className="history-item">
              <div className="history-input">{item.input}</div>
              <div className="history-output">{item.output}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatHistory;
