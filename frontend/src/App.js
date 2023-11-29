import React, { useEffect, useState } from "react";
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Welcome from './Components/Welcome';
import Login from './Components/Login';
import LoginForm from './Components/LoginForm';
import "bootstrap/dist/css/bootstrap.min.css"

function App() {
  // usestate for setting a javascript
    // object for storing and using data
    const [data, setdata] = useState({
      name: "",
      age: 0,
      date: "",
      programming: "",
  });

  const [loggedIn, setLoggedIn] = useState(false)
  const [email, setEmail] = useState("")

  // Using useEffect for single rendering
//   useEffect(() => {
//       // Using fetch to fetch the api from 
//       // flask server it will be redirected to proxy
//       fetch("/data").then((res) =>
//           res.json().then((data) => {
//               // Setting a data from api
//               setdata({
//                   name: data.Name,
//                   age: data.Age,
//                   date: data.Date,
//                   programming: data.programming,
//               });
//           })
//       );
//   }, []);

  return (
    //   <div className="App">
    //       <header className="App-header">
    //           <h1>React and flask</h1>
    //           {/* Calling a data from setdata for showing */}
    //           <p>{data.name}</p>
    //           <p>{data.age}</p>
    //           <p>{data.date}</p>
    //           <p>{data.programming}</p>

    //       </header>
    //   </div>
    // <Router>
    //     <Routes>
    //         <Route exaxt path="/" element={<Welcome email={email} loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>} />
    //         <Route exaxt path="/login" element={<Login/>} />
    //     </Routes>
    // </Router>

    <div className="App">
    <Router>
    <Routes>
        <Route path="/" element={<Welcome email={email} loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>} />
        <Route path="/login" element={<Login />} />
        <Route path="/loginform" element={<LoginForm />}/>
    </Routes>
    </Router>
    </div>

  );
}

export default App;
