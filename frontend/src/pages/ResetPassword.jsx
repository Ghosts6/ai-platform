
import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Swal from 'sweetalert2';
import axios from '../api/axios';
import { useNavigate, useLocation } from 'react-router-dom';

const ResetPassword = () => {
    const [website, setWebsite] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    // Extract token from query string
    const params = new URLSearchParams(location.search);
    const token = params.get('token');
    const handleSubmit = async (e) => {
        e.preventDefault();
        const password = e.target.password.value;
        const confirmPassword = e.target.confirmPassword.value;
        const website = e.target.website.value;
        if (website) return;
        if (!password || !confirmPassword) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter and confirm your new password!',
            });
            return;
        }
        if (password !== confirmPassword) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Passwords do not match!',
            });
            return;
        }
        if (!token) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid link',
                text: 'No reset token found.',
            });
            return;
        }
        try {
            await axios.post('/profiles/password-reset/confirm/', { token, password, website });
            Swal.fire({
                icon: 'success',
                title: 'Password reset successful! Please log in.',
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
                    <h2 className="text-2xl font-bold mb-4">Reset Password</h2>
                    <input name="password" type="password" placeholder="New Password" className="login-input" />
                    <input name="confirmPassword" type="password" placeholder="Confirm New Password" className="login-input" />
                    <input type="text" name="website" value={website} onChange={e => setWebsite(e.target.value)} className="hidden" autoComplete="off" tabIndex="-1" />
                    <button type="submit" className="login-button">Reset Password</button>
                </form>
            </div>
            <Footer />
        </div>
    );
};

export default ResetPassword;
