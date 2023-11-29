import React from 'react'
import { Link } from 'react-router-dom';

// function Welcome(){
//     return (
//         <div>
//             <h1>
//                 Patient Tracker System
//             </h1>
//             <div>
//                 <h2>Login</h2>
//                 <Link to='/login'>login as</Link>
//             </div>
//         </div>
//     )
// }
  

const Welcome = () => {
    return (
        <div>
            <h1> Welcome to the Patient Tracker System</h1>
            <Link to="/login">Login</Link>
            <Link to="/loginform">LoginForm</Link>
        </div>
    )
}


export default Welcome;