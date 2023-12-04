// DoctorSchedule.js

import React, { useState, useEffect } from 'react';
import { Navigate } from "react-router-dom";
import DoctorScheduleView from './DoctorScheduleView';

const DoctorPortal = () => {
    // Protect this page
    const [authenticated, setauthenticated] = useState(localStorage.getItem("authenticated"));
    useEffect(() => {
        const loggedInUser = localStorage.getItem("authenticated");
        if (loggedInUser) {
          setauthenticated(loggedInUser);
        }
      }, []);
    
    if (!authenticated) {
        return <Navigate replace to="/" />;
    }
    // Hardcoded events data for each hour
    const events = [
        { hour: '9 AM', event: 'Meeting with Patient A' },
        { hour: '10 AM', event: 'Checkup for Patient B' },
        { hour: '11 AM', event: 'Lunch break' },
        { hour: '12 PM', event: 'Surgery for Patient C' },
        { hour: '1 PM', event: 'Phone consultation' },
        // Add more events as needed
    ];

    return (
        <div>
            <h1>Doctor's Name</h1>
            <DoctorScheduleView />
        </div>
    );
};

export default DoctorPortal;