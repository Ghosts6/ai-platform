
import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Swal from 'sweetalert2';

const ResetPassword = () => {
    const handleSubmit = (e) => {
        e.preventDefault();
        const password = e.target.password.value;
        const confirmPassword = e.target.confirmPassword.value;

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

        // Handle password reset logic here
    };

    return (
        <div className="login-container">
            <Header />
            <div className="login-box">
                <form className="login-form" onSubmit={handleSubmit}>
                    <h2 className="text-2xl font-bold mb-4">Reset Password</h2>
                    <input name="password" type="password" placeholder="New Password" className="login-input" />
                    <input name="confirmPassword" type="password" placeholder="Confirm New Password" className="login-input" />
                    <button type="submit" className="login-button">Reset Password</button>
                </form>
            </div>
            <Footer />
        </div>
    );
};

export default ResetPassword;
