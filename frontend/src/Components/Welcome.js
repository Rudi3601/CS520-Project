import React from 'react'
import { Link } from 'react-router-dom';

function Welcome(){
    return (
        <div>
            <h1>
                Patient Tracker System
            </h1>
            <div>
                <h2>Login</h2>
                <Link to='/login'>login as</Link>
            </div>
        </div>
    )
}

export default Welcome;