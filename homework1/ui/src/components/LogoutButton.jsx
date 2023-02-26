import React, { useState } from "react";

const LogoutButton = () => {
  const [username, setUsername] = useState("");
  const handleClick = () => {
    // TODO: Perform logout action here, removing the username from local storage
    // Redirect the user to the login page
    setUsername(localStorage.getItem('username'))
    fetch(`http://flask-api/logout`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        username,
      })
    })
      .then((res) => {
        console.log(res)
        if (!res.ok) {
          console.error('Response not OK:', res.status, res.statusText);
          throw new Error(res.statusText);
        }
        return res.json();
      })
      .then((data) => {
        console.log(data)
        if (data.error) {
          console.log(data.error)
          localStorage.setItem('username', null);
          window.location.href = '/';
        } else {
          localStorage.setItem('username', null);
          window.location.href = '/';
        }
      })
      .catch((err) => {
        console.error(err);
      });  
  };


  return (
    <button onClick={handleClick}>Logout</button>
  );
};

export default LogoutButton;