
import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Swal from 'sweetalert2';
import axios from '../api/axios';
import { useNavigate } from 'react-router-dom';

const ForgotPassword = () => {
    const [website, setWebsite] = useState('');
    const navigate = useNavigate();
    const handleSubmit = async (e) => {
        e.preventDefault();
        const email = e.target.email.value;
        const website = e.target.website.value;
        if (website) return;
        if (!email) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter your email address!',
            });
            return;
        }
        try {
            await axios.post('/profiles/password-reset/', { email, website });
            Swal.fire({
                icon: 'success',
                title: 'Reset link sent! Check your email.',
                showConfirmButton: false,
                timer: 1800
            });
            setTimeout(() => navigate('/login'), 1800);
        } catch (err) {
            Swal.fire({
                icon: 'error',
                title: 'Reset failed',
                text: err.response?.data?.error || 'Something went wrong',
            });
        }
    };

    return (
        <div className="login-container">
            <Header />
            <div className="login-box">
                <form className="login-form" onSubmit={handleSubmit}>
                    <h2 className="text-2xl font-bold mb-4 text-primary">Forgot Password</h2>
                    <p className="mb-4 text-[#111111]">Enter your email address and we will send you a link to reset your password.</p>
                    <input name="email" type="email" placeholder="Email" className="login-input" />
                    <input type="text" name="website" value={website} onChange={e => setWebsite(e.target.value)} className="hidden" autoComplete="off" tabIndex="-1" />
                    <button type="submit" className="login-button">Send Reset Link</button>
                </form>
            </div>
            <Footer />
        </div>
    );
};

export default ForgotPassword;
