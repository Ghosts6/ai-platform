
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Swal from 'sweetalert2';
import axios from '../api/axios';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

const Login = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [website, setWebsite] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
    const [signupPasswordGuide, setSignupPasswordGuide] = useState(false);
    const navigate = useNavigate();
    const [showLoginPassword, setShowLoginPassword] = useState(false);
    const [showSignupPassword, setShowSignupPassword] = useState(false);
    const [showSignupConfirm, setShowSignupConfirm] = useState(false);
    const [loginPasswordValue, setLoginPasswordValue] = useState('');
    const [signupPasswordValue, setSignupPasswordValue] = useState('');
    const [signupConfirmValue, setSignupConfirmValue] = useState('');

    useEffect(() => {
        if (isLoggedIn) {
            navigate('/');
        }
    }, [isLoggedIn, navigate]);

    const handleLogin = async (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        const website = e.target.website.value;
        if (website) return;
        if (!username || !password) {
            Swal.fire({
                icon: 'error',
                title: 'Missing Fields',
                text: 'Please enter both username and password!',
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#007bff',
            });
            return;
        }
        try {
            const res = await axios.post('/profiles/login/', { username, password, website });
            localStorage.setItem('token', res.data.token);
            setIsLoggedIn(true);
            Swal.fire({
                icon: 'success',
                title: 'Welcome back!',
                text: 'Login successful.',
                background: '#222831',
                color: '#EEEEEE',
                showConfirmButton: false,
                timer: 1200
            });
            setTimeout(() => {
                if (res.data.is_admin || username.toLowerCase() === 'admin') {
                    window.location.href = '/admin/';
                } else {
                    navigate('/');
                }
            }, 1200);
        } catch (err) {
            Swal.fire({
                icon: 'error',
                title: 'Login failed',
                text: err.response?.data?.error || 'Something went wrong',
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#007bff',
            });
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const email = e.target.email.value;
        const password = e.target.password.value;
        const confirmPassword = e.target.confirmPassword.value;
        const website = e.target.website.value;
        if (website) return;
        if (!username || !email || !password || !confirmPassword) {
            Swal.fire({
                icon: 'error',
                title: 'Missing Fields',
                text: 'Please fill in all fields!',
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#007bff',
            });
            return;
        }
        if (password !== confirmPassword) {
            Swal.fire({
                icon: 'error',
                title: 'Password Mismatch',
                text: 'Passwords do not match!',
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#007bff',
            });
            return;
        }
        // Enhanced password validation: 8+ chars, uppercase, lowercase, digit, special char
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;
        if (!passwordRegex.test(password)) {
            Swal.fire({
                icon: 'error',
                title: 'Weak Password',
                text: 'Password must be 8+ characters with uppercase, lowercase, digit, and special character.',
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#007bff',
            });
            setSignupPasswordGuide(true);
            return;
        }
        try {
            const res = await axios.post('/profiles/register/', { 
                username, 
                email, 
                password, 
                confirm_password: confirmPassword,
                website 
            });
            // Auto-login after signup
            const loginRes = await axios.post('/profiles/login/', { username, password, website: '' });
            localStorage.setItem('token', loginRes.data.token);
            setIsLoggedIn(true);
            Swal.fire({
                icon: 'success',
                title: 'Welcome!',
                text: 'Signup successful. You are now logged in.',
                background: '#222831',
                color: '#EEEEEE',
                showConfirmButton: false,
                timer: 1500
            });
            setTimeout(() => navigate('/'), 1500);
        } catch (err) {
            let msg = 'Something went wrong';
            if (err.response?.data?.website) msg = err.response.data.website;
            else if (err.response?.data?.username) msg = err.response.data.username;
            else if (err.response?.data?.email) msg = err.response.data.email;
            else if (err.response?.data?.password) msg = err.response.data.password;
            else if (err.response?.data?.confirm_password) msg = err.response.data.confirm_password;
            else if (err.response?.data?.non_field_errors) msg = err.response.data.non_field_errors[0];
            Swal.fire({
                icon: 'error',
                title: 'Signup failed',
                text: msg,
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#007bff',
            });
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setIsLoggedIn(false);
        Swal.fire({
            icon: 'success',
            title: 'Logged out!',
            showConfirmButton: false,
            timer: 1000
        });
        setTimeout(() => navigate('/'), 1000);
    };

    return (
        <div className="login-container">
            <Header />
            <div className="login-box">
                <div className="login-toggle">
                    <button onClick={() => setIsLogin(true)} className={isLogin ? 'active' : ''}>Login</button>
                    <button onClick={() => setIsLogin(false)} className={!isLogin ? 'active' : ''}>Sign Up</button>
                </div>
                {isLoggedIn ? (
                    <button className="logout-button" onClick={handleLogout}>Logout</button>
                ) : isLogin ? (
                    <form className="login-form" onSubmit={handleLogin}>
                        <input name="username" type="text" placeholder="Username" className="login-input" />
                        <div className="password-input-wrapper mb-4">
                            <input
                                name="password"
                                type={showLoginPassword ? 'text' : 'password'}
                                placeholder="Password"
                                className="login-input pr-12"
                                value={loginPasswordValue}
                                onChange={e => setLoginPasswordValue(e.target.value)}
                                autoComplete="current-password"
                            />
                            <button
                                type="button"
                                tabIndex="-1"
                                className={`password-toggle-btn${loginPasswordValue ? '' : ' invisible'}`}
                                onClick={() => setShowLoginPassword(v => !v)}
                                aria-label={showLoginPassword ? 'Hide password' : 'Show password'}
                            >
                                {showLoginPassword ? <FaEyeSlash size={20} /> : <FaEye size={20} />}
                            </button>
                        </div>
                        <input type="text" name="website" value={website} onChange={e => setWebsite(e.target.value)} className="hidden" autoComplete="off" tabIndex="-1" />
                        <button type="submit" className="login-button">Login</button>
                        <Link to="/forgot-password" className="forgot-password">Forgot Password?</Link>
                    </form>
                ) : (
                    <form className="login-form" onSubmit={handleSignup}>
                        <input name="username" type="text" placeholder="Username" className="login-input" />
                        <input name="email" type="email" placeholder="Email" className="login-input" />
                        <div className="password-input-wrapper mb-4">
                            <input
                                name="password"
                                type={showSignupPassword ? 'text' : 'password'}
                                placeholder="Password"
                                className="login-input pr-12"
                                value={signupPasswordValue}
                                onChange={e => setSignupPasswordValue(e.target.value)}
                                autoComplete="new-password"
                            />
                            <button
                                type="button"
                                tabIndex="-1"
                                className={`password-toggle-btn${signupPasswordValue ? '' : ' invisible'}`}
                                onClick={() => setShowSignupPassword(v => !v)}
                                aria-label={showSignupPassword ? 'Hide password' : 'Show password'}
                            >
                                {showSignupPassword ? <FaEyeSlash size={20} /> : <FaEye size={20} />}
                            </button>
                        </div>
                        <div className="password-input-wrapper mb-4">
                            <input
                                name="confirmPassword"
                                type={showSignupConfirm ? 'text' : 'password'}
                                placeholder="Confirm Password"
                                className="login-input pr-12"
                                value={signupConfirmValue}
                                onChange={e => setSignupConfirmValue(e.target.value)}
                                autoComplete="new-password"
                            />
                            <button
                                type="button"
                                tabIndex="-1"
                                className={`password-toggle-btn${signupConfirmValue ? '' : ' invisible'}`}
                                onClick={() => setShowSignupConfirm(v => !v)}
                                aria-label={showSignupConfirm ? 'Hide password' : 'Show password'}
                            >
                                {showSignupConfirm ? <FaEyeSlash size={20} /> : <FaEye size={20} />}
                            </button>
                        </div>
                        <input type="text" name="website" value={website} onChange={e => setWebsite(e.target.value)} className="hidden" autoComplete="off" tabIndex="-1" />
                        <button type="submit" className="login-button">Sign Up</button>
                    </form>
                )}
            </div>
            <Footer />
        </div>
    );
};

export default Login;
