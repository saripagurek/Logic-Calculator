import './App.css';
import React from "react";
import { useState } from 'react';

let eq = "(A|B)";

function makeData() {
  try {
    console.log(window.truthTable(eq))
  }
  catch(err) {
    alert("Error: Invalid Input \nCheck for correct brackets and invalid characters")
  }
  return JSON.parse(window.truthTable(eq));
}

function MyForm(props) {
  const [str, setName] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    eq = `${str}`
    console.log(eq)
    props.setData(makeData())
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
      <div className="title">
        <h1>Predicate Logic Calculator</h1>
        <h2>Input a logical equation to evaluate a truth table. 
          Ensure your equation is surrounded with brackets: "(A|B)".</h2>
          <h2>Use the symbols: & , | , ! . </h2>
      </div>
      <MyForm setData={setData} />
      <table>
        <tr class="header">
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