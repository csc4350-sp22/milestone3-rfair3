import {useState, useEffect} from 'react';



function App() {
  
  const [comment, setComment] = useState([]);

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
      <h2>Your reviews:</h2>
      <table>
        {comment && comment.map((c) =>
          <tr>
            <tb><b>Movie ID: {c.movieid}</b></tb>&nbsp;
            <tb><input type="text" value={c.rating} size="3"></input></tb>&nbsp;
            <tb><input type="text" value={c.comments}></input></tb>&nbsp;
            <button>Delete</button>
          </tr>
        )}
      </table>
      <button>Save Changes</button>
  </center>
  </div>

  );
}

export default App;