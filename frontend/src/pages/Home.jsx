import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaCrown } from 'react-icons/fa';

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24">
        <div className="flex flex-col items-center gap-6 w-full">
          <FaCrown className="text-primary text-6xl mb-2 drop-shadow-lg" />
          <h1 className="text-5xl md:text-7xl font-display font-extrabold text-primary mb-2 tracking-tight text-center">
            AIAgent Platform
          </h1>
          <p className="text-xl md:text-2xl text-accent/80 mb-4 text-center">
            Modular backend and web UI for intelligent, task-oriented agents powered
            by OpenAI and Django.
            <br />
            <span className="text-primary font-semibold">
              Fast. Modern. Extensible.
            </span>
          </p>
          <a
            href="/agent"
            className="inline-block px-8 py-3 rounded-lg bg-primary text-background font-bold text-lg shadow-lg hover:bg-primary-hover transition"
          >
            Explore Agents
          </a>
          <div className="mt-8 text-sm text-accent/60 text-center">
            Need help?{' '}
            <a
              href="mailto:contact@aiagent.com"
              className="text-primary underline hover:text-primary-hover"
            >
              Contact us
            </a>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}