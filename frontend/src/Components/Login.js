import React from 'react'
//onSubmit={this.handleSubmit}>
function Login(){
    return (
        <div>
            <h2>Login Form</h2>
            <form>
            <div>
                <label htmlFor="username">Username:</label>
                <input
                type="text"
                id="username"
                //value={this.state.username}
                //onChange={this.handleUsernameChange}
                />
            </div>
            <div>
                <label htmlFor="password">Password:</label>
                <input
                type="password"
                id="password"
                //value={this.state.password}
                //onChange={this.handlePasswordChange}
                />
            </div>
            <div>
                <button type="submit">Submit</button>
            </div>
            </form>
        </div>
    )
}

export default Login;