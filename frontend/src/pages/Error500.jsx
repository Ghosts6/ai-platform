import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaCrown } from 'react-icons/fa';

export default function Error500() {
  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex flex-1 flex-col items-center justify-center px-4 py-12 w-full">
        <FaCrown className="text-red-500 text-5xl mb-4 drop-shadow-lg" />
        <h1 className="text-6xl font-extrabold text-red-500 mb-2">500</h1>
        <h2 className="text-2xl font-semibold mb-4">Internal Server Error</h2>
        <p className="text-lg text-accent/80 mb-6 max-w-lg text-center">
          Sorry, something went wrong on our end.<br />
          If the problem persists, please <a href="mailto:contact@aiagent.com" className="text-primary underline hover:text-primary-hover">contact us</a>.
        </p>
        <a href="/" className="inline-block px-6 py-2 rounded-lg bg-primary text-background font-semibold shadow hover:bg-primary-hover transition">Go Home</a>
      </main>
      <Footer />
    </div>
  );
}