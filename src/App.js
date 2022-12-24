import './App.css';
import React from "react";
import { useState } from 'react';
import ReactDOM from 'react-dom/client';

let eq = "(A|B)";

function makeData() {
  console.log(window.truthTable(eq))
  return JSON.parse(window.truthTable(eq));
}

function MyForm(props) {
  const [str, setName] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    eq = `${str}`
    console.log(eq)
   props.setData(makeData())
    //alert(`The str you entered was: ${str}`)
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>Enter an equation: 
        <input 
          type="text" 
          value={str}
          onChange={(e) => setName(e.target.value)}
        />
      </label>
      <input type="submit" />
    </form>
  )
}
  
function App() {
  
  const [data, setData] = React.useState([])
  React.useEffect(function() {
    window.brythonReady = function () {
      setData(makeData())
    }
  }, [])
  console.log(data)
  let numRows = 0
  if (Object.keys(data).length > 0) {
    numRows = data[Object.keys(data)[0]].length
  }
  const rows = []
  for (var i = 0; i < numRows; i++) {
    rows.push(Object.keys(data).map((key) => data[key][i]))
  }
  return (
    
    <div className="App">
      <div className="align">
      <MyForm setData={setData} />
      <table>
        <tr>
          {Object.keys(data).map((key) => <td>{key}</td>)}
        </tr>
        {
          rows.map((row) => <tr>{row.map((cell) => <td>{cell + ""}</td>)}</tr>)
        }
      </table>
      </div>
    </div>
  );
}

export default App;