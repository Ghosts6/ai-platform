
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Swal from 'sweetalert2';

const Login = () => {
    const [isLogin, setIsLogin] = useState(true);

    const handleLogin = (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;

        if (!username || !password) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter both username and password!',
            });
            return;
        }

        // Handle login logic here
    };

    const handleSignup = (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const email = e.target.email.value;
        const password = e.target.password.value;

        if (!username || !email || !password) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please fill in all fields!',
            });
            return;
        }

        // Handle signup logic here
    };

    return (
        <div className="login-container">
            <Header />
            <div className="login-box">
                <div className="login-toggle">
                    <button onClick={() => setIsLogin(true)} className={isLogin ? 'active' : ''}>Login</button>
                    <button onClick={() => setIsLogin(false)} className={!isLogin ? 'active' : ''}>Sign Up</button>
                </div>
                {isLogin ? (
                    <form className="login-form" onSubmit={handleLogin}>
                        <input name="username" type="text" placeholder="Username" className="login-input" />
                        <input name="password" type="password" placeholder="Password" className="login-input" />
                        <button type="submit" className="login-button">Login</button>
                        <Link to="/forgot-password" className="forgot-password">Forgot Password?</Link>
                    </form>
                ) : (
                    <form className="login-form" onSubmit={handleSignup}>
                        <input name="username" type="text" placeholder="Username" className="login-input" />
                        <input name="email" type="email" placeholder="Email" className="login-input" />
                        <input name="password" type="password" placeholder="Password" className="login-input" />
                        <button type="submit" className="login-button">Sign Up</button>
                    </form>
                )}
            </div>
            <Footer />
        </div>
    );
};

export default Login;
