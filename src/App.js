import './App.css';
import React, { useState, useEffect } from 'react';



function App() {
  
  const [comment, setComment] = useState([]);
  const 

  useEffect(() => {
    fetch("/comment_fetch", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(data);
      setComment(data.comment);
      

    })

  });

  
return (
  <div>

  <center>

  </center>
  </div>

  );
}

export default App;