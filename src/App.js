import './App.css';
import React, { useState, useEffect } from 'react';


//Creates a map and form for the passed data from the bp.route for Comment fetch.
function App() {
  const [revised, setRevised] = useState([]);
  const listRevised = revised.map((x, index) => {
    return (
      <ul>
        <form id={index}>
          <label for="movieid">Movie ID:</label>
          <input type="text" id="movieID" name="movieID" value={x[0]} readonly></input>
          <input type="number" id="rating" name="rating" min="0" max="10" placeholder={x[1]} defaultValue={x[1]} required></input>
          <input type="text" placeholder={x[2]} defaultValue={x[2]} name="comments" required></input>
          <input type="button" id="change" onClick={() => handleClick(index)} value="Delete Comment"></input>
        </form>
      </ul>
    )
  });

  //Finds comment position and deletes comment on click. Wires up save and delete button.
  const pass = [];
  function handleClick(index) {
    const revisedForm = document.getElementById(index);
    pass.push(index);
    pass.sort(function (a, b) { return b - a; })
    revisedForm.remove();
    console.log(revised);
    console.log(pass);
  };

  //UseEffect fetches the bp route comment_fetch and reads the array
  useEffect(() => {
    fetch('/fetch_comment', {
      method: 'POST', headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => { return response.json() })
      .then(data => {
        setRevised(data.revised)
        console.log(data)
      })
  }, []);


  //Post the editied data to the saveComment bpRoute
  function saveRevised() {
    alert("Your changes have been successfully saved")
    fetch('/save_comment', {
      method: 'POST', headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(pass)
    })
  };



  return (
    <div className="App">
      {listRevised}
      <a href="/"><input type="submit" id="change" value="Save your opinion" onClick={() => saveRevised()}></input></a>
    </div>
  );
};

export default App;