
import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Swal from 'sweetalert2';

const ForgotPassword = () => {
    const handleSubmit = (e) => {
        e.preventDefault();
        const email = e.target.email.value;

        if (!email) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please enter your email address!',
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
                    <h2 className="text-2xl font-bold mb-4">Forgot Password</h2>
                    <p className="mb-4">Enter your email address and we will send you a link to reset your password.</p>
                    <input name="email" type="email" placeholder="Email" className="login-input" />
                    <button type="submit" className="login-button">Send Reset Link</button>
                </form>
            </div>
            <Footer />
        </div>
    );
};

export default ForgotPassword;
