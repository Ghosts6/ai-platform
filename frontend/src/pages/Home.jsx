import { useState, useEffect } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaCrown, FaCog, FaBrain, FaCode, FaArrowUp, FaReact, FaServer, FaDatabase } from 'react-icons/fa';

export default function Home() {
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => {
    if (window.pageYOffset > 300) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  };

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  useEffect(() => {
    window.addEventListener('scroll', toggleVisibility);
    return () => {
      window.removeEventListener('scroll', toggleVisibility);
    };
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center px-4 py-12 md:py-24">
        {/* Hero Section */}
        <div className="flex flex-col items-center gap-6 w-full mb-20 text-center">
          <img src="/img/Baner.png" alt="AIAgent Platform Banner" className="w-full max-w-4xl mx-auto mb-8 rounded-lg shadow-2xl" loading="lazy" />
          <h1 className="text-6xl md:text-8xl font-display font-extrabold text-primary mb-2 tracking-tight">
            AIAgent Platform
          </h1>
          <p className="text-2xl md:text-3xl text-accent/80 mb-6">
            A cutting-edge platform to harness the power of Large Language Models and build intelligent AI agents.
          </p>
        </div>

        {/* Goal of the Project */}
        <section className="w-full max-w-5xl mb-20">
          <h2 className="text-4xl font-bold text-primary mb-6 text-center">Our Goal</h2>
          <p className="text-xl text-accent/80 text-center">
            We aim to provide a robust and intuitive environment for developers and researchers to explore, create, and deploy sophisticated AI agents. Our platform is designed to demystify the complexities of LLM-powered workflows and enable the next generation of intelligent automation.
          </p>
        </section>

        {/* LLM Workflow */}
        <section className="w-full max-w-5xl mb-20">
          <div className="flex items-center justify-center mb-6">
            <FaBrain className="text-primary text-4xl mr-4" />
            <h2 className="text-4xl font-bold text-primary">LLM AI Workflow</h2>
          </div>
          <p className="text-xl text-accent/80 mb-8">
            The LLM AI workflow is a structured process that guides an AI agent from task conception to completion. It begins with interpreting a user's prompt, followed by a series of reasoning and action steps. This iterative process allows the agent to refine its understanding, correct its course, and ultimately generate a coherent and effective response. Our platform provides the tools to visualize and manage this entire workflow.
          </p>
          <div className="flex justify-center">
            <img src="/img/Llm.png" alt="LLM AI Workflow Diagram" className="w-full h-auto max-w-3xl rounded-lg shadow-lg" loading="lazy" />
          </div>
        </section>

        {/* Agent React */}
        <section className="w-full max-w-5xl mb-20">
          <div className="flex items-center justify-center mb-6">
            <FaCog className="text-primary text-4xl mr-4" />
            <h2 className="text-4xl font-bold text-primary">Agent React Framework</h2>
          </div>
          <p className="text-xl text-accent/80 mb-8">
            The "React" (Reasoning and Acting) framework empowers our AI agents to tackle complex, multi-step tasks. By interleaving thought and action, agents can dynamically reason about a problem, interact with external tools to gather information, and learn from their interactions. This enables a level of problem-solving that goes beyond simple prompt-response interactions, allowing for more sophisticated and autonomous behavior.
          </p>
          <div className="flex justify-center">
            <img src="/img/ReAct.png" alt="Agent React Framework" className="w-full h-auto max-w-3xl rounded-lg shadow-lg" loading="lazy" />
          </div>
        </section>

        {/* Chain of Thought */}
        <section className="w-full max-w-5xl mb-20">
          <div className="flex items-center justify-center mb-6">
            <FaBrain className="text-primary text-4xl mr-4" />
            <h2 className="text-4xl font-bold text-primary">Chain of Thought Reasoning</h2>
          </div>
          <p className="text-xl text-accent/80 mb-8">
            Chain of Thought (CoT) prompting is a powerful technique that enhances the reasoning capabilities of LLMs. By prompting the model to generate a step-by-step sequence of thoughts, we guide it toward a more logical and accurate conclusion. This is particularly effective for tasks requiring complex reasoning, such as arithmetic, commonsense, and symbolic problems. Our platform fully supports CoT to ensure high-quality outputs from your agents.
          </p>
          <div className="flex justify-center">
            <img src="/img/chain_of_thought.png" alt="Chain of Thought Reasoning" className="w-full h-auto max-w-3xl rounded-lg shadow-lg" loading="lazy" />
          </div>
        </section>

        {/* Technology Stack */}
        <section className="w-full max-w-5xl mb-20">
          <div className="flex items-center justify-center mb-6">
            <FaCode className="text-primary text-4xl mr-4" />
            <h2 className="text-4xl font-bold text-primary">Our Technology Stack</h2>
          </div>
          <p className="text-xl text-accent/80 mb-8 text-center">
            This platform is built on a modern, robust technology stack to ensure scalability, reliability, and a seamless user experience.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="bg-gray-800/50 p-6 rounded-lg flex flex-col items-center">
              <FaReact className="text-primary text-5xl mb-4" />
              <h3 className="text-2xl font-bold text-primary mb-2">Frontend</h3>
              <p className="text-lg text-accent/80">React, Tailwind CSS</p>
            </div>
            <div className="bg-gray-800/50 p-6 rounded-lg flex flex-col items-center">
              <FaServer className="text-primary text-5xl mb-4" />
              <h3 className="text-2xl font-bold text-primary mb-2">Backend</h3>
              <p className="text-lg text-accent/80">Django, Django REST Framework</p>
            </div>
            <div className="bg-gray-800/50 p-6 rounded-lg flex flex-col items-center">
              <FaDatabase className="text-primary text-5xl mb-4" />
              <h3 className="text-2xl font-bold text-primary mb-2">AI Integration</h3>
              <p className="text-lg text-accent/80">OpenAI API</p>
            </div>
          </div>
        </section>

        {/* Powered by OpenAI */}
        <section className="w-full max-w-5xl mb-20">
          <h2 className="text-4xl font-bold text-primary mb-6 text-center">Powered by OpenAI</h2>
          <p className="text-xl text-accent/80 text-center">
            Our platform leverages the state-of-the-art models from OpenAI via their API. This provides our agents with unparalleled natural language understanding and generation capabilities, allowing them to perform a wide range of tasks with remarkable accuracy and fluency.
          </p>
        </section>

        {/* Call to Action */}
        <div className="mt-12 text-center">
          <a
            href="/agent"
            className="inline-block px-10 py-4 rounded-lg bg-primary text-background font-bold text-xl shadow-lg hover:bg-primary-hover transition-transform transform hover:scale-105"
          >
            Explore the Agents
          </a>
        </div>
      </main>
      <Footer />
      {isVisible && (
        <button 
          onClick={scrollToTop}
          className="fixed bottom-8 right-8 bg-primary text-white p-4 rounded-full shadow-lg hover:bg-primary-hover active:bg-primary-dark transition-all duration-300 ease-in-out transform hover:scale-110 active:scale-100"
        >
          <FaArrowUp className="h-6 w-6" />
        </button>
      )}
    </div>
  );
}