import React, { useEffect, useState } from "react";
import './App.css';
import { Link } from 'react-router-dom';
import Form from './components/Form.js';
import UncontrolledForm from './components/UncontrolledForm.js';
import httpClient from "./httpClient";
import DoctorLogin from "./components/DoctorLogin.js";

function App() {
    // usestate for setting a javascript
    //  object for storing and using data
    const [data, setdata] = useState({
      name: "",
      age: 0,
      date: "",
      programming: "",
  });

    // Using useEffect for single rendering
    useEffect(() => {
        // Using fetch to fetch the api from 
        // flask server it will be redirected to proxy
        fetch("/data").then((res) =>
            res.json().then((data) => {
                // Setting a data from api
                setdata({
                    name: data.Name,
                    age: data.Age,
                    date: data.Date,
                    programming: data.programming,
                });
            })
        );
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>Welcome to Patient Tracker System</h1>
                <p>Please select your role</p>
                <div className='parent'>
                    <Link className='child' to="/PatientLogin">Patient Login</Link>
                    <Link className='child' to="/DoctorLogin">Doctor Login</Link>
                </div>
                <div className="temporary">
                    {/* Calling a data from setdata for showing */}
                    {/* TODO: delete after finishing */}
                    <p>Making sure the server is responding. DELETE before deployment</p>
                    <p>{data.name}</p>
                    <p>{data.age}</p>
                    <p>{data.date}</p>
                    <p>{data.programming}</p>
                </div>

            </header>
        </div>
    );
}

export default App;
