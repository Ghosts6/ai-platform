import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ScrollToTopButton from '../components/ScrollToTopButton';
import { FaBrain, FaCode, FaReact, FaServer, FaDatabase, FaEnvelope, FaFileExcel, FaCalendarAlt, FaTasks, FaUser, FaRobot, FaTools, FaLightbulb, FaCrown, FaCog, FaRocket, FaCogs } from 'react-icons/fa';

const HeroSection = () => {
  return (
    <section className="w-full flex flex-col items-center justify-center min-h-[60vh] bg-gradient-to-br from-secondary/80 via-background to-secondary/60 rounded-2xl shadow-xl mb-20 p-8 md:p-16 text-center relative overflow-hidden animate-fadeIn">
      <img src={process.env.PUBLIC_URL + '/img/hero2.png'} alt="AI Agents Collaboration" className="w-full max-w-3xl mx-auto mb-6 rounded-xl shadow-2xl object-cover animate-heroImageFade" loading="lazy" style={{maxHeight: '340px'}} />
      <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-4 tracking-tight leading-tight drop-shadow-lg animate-heroTextSlide">AI Agents</h1>
      <p className="text-1.5xl md:text-2xl text-accent/80 mb-8 max-w-2xl mx-auto leading-relaxed font-medium animate-heroTextFade">
        Unlock the full potential of Large Language Models. Seamlessly integrate, manage, and collaborate with digital agents designed for the future of productivity.
      </p>
    </section>
  );
};

const GoalSection = () => {
  return (
    <section className="w-full max-w-5xl mb-20">
      <h2 className="text-4xl font-bold text-primary mb-6 text-center">Our Goal</h2>
      <p className="text-xl text-accent/80 text-center">
        We aim to provide a robust and intuitive environment for developers and researchers to explore, create, and deploy sophisticated AI agents. Our platform is designed to demystify the complexities of LLM-powered workflows and enable the next generation of intelligent automation.
      </p>
    </section>
  );
};

const HowItWorksSection = () => {
  return (
    <section className="w-full max-w-5xl mb-20">
      <h2 className="text-4xl font-bold text-primary mb-12 text-center">How It Works</h2>
      <div className="flex justify-center items-center">
        {/* Replace this with the diagram image you will provide */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
          <div className="flex flex-col items-center">
            <FaUser className="text-primary text-5xl mb-4" />
            <h3 className="text-2xl font-bold text-primary mb-2">1. Send a Prompt</h3>
            <p className="text-lg text-accent/80">The user sends a request to the platform.</p>
          </div>
          <div className="flex flex-col items-center">
            <FaRobot className="text-primary text-5xl mb-4" />
            <h3 className="text-2xl font-bold text-primary mb-2">2. Select an Agent</h3>
            <p className="text-lg text-accent/80">The platform selects the most appropriate agent for the task.</p>
          </div>
          <div className="flex flex-col items-center">
            <FaTools className="text-primary text-5xl mb-4" />
            <h3 className="text-2xl font-bold text-primary mb-2">3. Process the Prompt</h3>
            <p className="text-lg text-accent/80">The agent processes the prompt, interacting with tools and knowledge bases.</p>
          </div>
          <div className="flex flex-col items-center">
            <FaLightbulb className="text-primary text-5xl mb-4" />
            <h3 className="text-2xl font-bold text-primary mb-2">4. Get a Response</h3>
            <p className="text-lg text-accent/80">The agent returns a response to the user.</p>
          </div>
        </div>
      </div>
    </section>
  );
};

const UseCasesSection = () => {
  return (
    <section className="w-full max-w-5xl mb-20">
      <h2 className="text-4xl font-bold text-primary mb-12 text-center">Use Cases</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 text-center">
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaEnvelope className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">Email Automation</h3>
          <p className="text-lg text-accent/80">Summarize, draft, and send emails automatically.</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaFileExcel className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">Data Analysis</h3>
          <p className="text-lg text-accent/80">Analyze data from Excel files and generate insights.</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaCalendarAlt className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">Calendar Management</h3>
          <p className="text-lg text-accent/80">Create and manage calendar events and meetings.</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaTasks className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">Task Automation</h3>
          <p className="text-lg text-accent/80">Automate repetitive tasks and workflows.</p>
        </div>
      </div>
    </section>
  );
};

const FeaturesSection = () => {
  return (
    <section
      className="w-full max-w-5xl mb-20 p-8 rounded-2xl"
      style={{
        backgroundImage: `url(${process.env.PUBLIC_URL + '/img/FeaturesSection.jpg'})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }}
    >
      <div className="flex items-center justify-center mb-6">
        <FaCrown className="text-primary text-4xl mr-4" />
        <h2 className="text-4xl font-bold text-primary">Features</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 text-center">
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaServer className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">Modular Backend</h3>
          <p className="text-lg text-accent/80">Reusable Django apps for core services, agents, and scheduling.</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaReact className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">React Frontend</h3>
          <p className="text-lg text-accent/80">A dynamic and responsive user interface for interacting with the AI agents.</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaBrain className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">LLM Integration</h3>
          <p className="text-lg text-accent/80">Seamlessly connect with OpenAI for dynamic prompt handling.</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaCode className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">REST APIs</h3>
          <p className="text-lg text-accent/80">Communicate between the frontend and backend using Django REST Framework.</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaRobot className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">Pre-built Agents</h3>
          <p className="text-lg text-accent/80">Includes agents for summarization, Q&A, email, Excel, and Teams calendar integration.</p>
        </div>
        <div className="bg-gray-800/50 p-6 rounded-lg">
          <FaRocket className="text-primary text-5xl mb-4 mx-auto" />
          <h3 className="text-2xl font-bold text-primary mb-2">CI/CD Pipeline</h3>
          <p className="text-lg text-accent/80">Automated testing and deployment with GitHub Actions.</p>
        </div>
      </div>
    </section>
  );
};

const TechStackSection = () => {
  return (
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
  );
};

const OpenAISection = () => {
  return (
    <section className="w-full max-w-5xl mb-20">
      <h2 className="text-4xl font-bold text-primary mb-6 text-center">Powered by OpenAI</h2>
      <p className="text-xl text-accent/80 text-center">
        Our platform leverages the state-of-the-art models from OpenAI via their API. This provides our agents with unparalleled natural language understanding and generation capabilities, allowing them to perform a wide range of tasks with remarkable accuracy and fluency.
      </p>
    </section>
  );
};

const ChainOfThoughtSection = () => {
  return (
    <section className="w-full max-w-5xl mb-20">
      <div className="flex items-center justify-center mb-6">
        <FaBrain className="text-primary text-4xl mr-4" />
        <h2 className="text-4xl font-bold text-primary">Chain of Thought Reasoning</h2>
      </div>
      <p className="text-xl text-accent/80 mb-8 text-center">
        Chain of Thought (CoT) prompting is a powerful technique that enhances the reasoning capabilities of LLMs. By prompting the model to generate a step-by-step sequence of thoughts, we guide it toward a more logical and accurate conclusion. This is particularly effective for tasks requiring complex reasoning, such as arithmetic, commonsense, and symbolic problems. Our platform fully supports CoT to ensure high-quality outputs from your agents.
      </p>
      <div className="flex justify-center">
        <img src={process.env.PUBLIC_URL + '/img/chain_of_thought.png'} alt="Chain of Thought Reasoning" className="w-full max-h-[27.5rem] max-w-3xl rounded-lg shadow-lg" loading="lazy" />
      </div>
    </section>
  );
};

const ReactFrameworkSection = () => {
  return (
    <section className="w-full max-w-5xl mb-20">
      <div className="flex items-center justify-center mb-6">
        <FaCog className="text-primary text-4xl mr-4" />
        <h2 className="text-4xl font-bold text-primary">Agent React Framework</h2>
      </div>
      <p className="text-xl text-accent/80 mb-8 text-center">
        The "React" (Reasoning and Acting) framework empowers our AI agents to tackle complex, multi-step tasks. By interleaving thought and action, agents can dynamically reason about a problem, interact with external tools to gather information, and learn from their interactions. This enables a level of problem-solving that goes beyond simple prompt-response interactions, allowing for more sophisticated and autonomous behavior.
      </p>
      <div className="flex justify-center">
        <img src={process.env.PUBLIC_URL + '/img/ReAct.png'} alt="Agent React Framework" className="w-full h-auto max-w-3xl rounded-lg shadow-lg" loading="lazy" />
      </div>
    </section>
  );
};

const WorkflowSection = () => {
  return (
    <section className="w-full max-w-5xl mb-20">
      <div className="flex items-center justify-center mb-6">
        <FaBrain className="text-primary text-4xl mr-4" />
        <h2 className="text-4xl font-bold text-primary">LLM AI Workflow</h2>
      </div>
      <p className="text-xl text-accent/80 mb-8 text-center">
        The LLM AI workflow is a structured process that guides an AI agent from task conception to completion. It begins with interpreting a user's prompt, followed by a series of reasoning and action steps. This iterative process allows the agent to refine its understanding, correct its course, and ultimately generate a coherent and effective response. Our platform provides the tools to visualize and manage this entire workflow.
      </p>
      <div className="flex justify-center">
        <img src={process.env.PUBLIC_URL + '/img/Llm.png'} alt="LLM AI Workflow Diagram" className="w-full h-auto max-w-3xl rounded-lg shadow-lg" loading="lazy" />
      </div>
    </section>
  );
};

const CoreConceptsSection = () => {
  return (
    <section className="w-full max-w-5xl mb-20">
      <div className="flex items-center justify-center mb-12">
        <FaCogs className="text-primary text-4xl mr-4" />
        <h2 className="text-4xl font-bold text-primary">Core Concepts</h2>
      </div>
      <div className="flex flex-col items-center">
        <ChainOfThoughtSection />
        <ReactFrameworkSection />
        <WorkflowSection />
      </div>
    </section>
  );
};

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
      <main className="flex-1 flex flex-col items-center px-4 py-4 md:py-12">
        <HeroSection />
        <GoalSection />
        <HowItWorksSection />
        <UseCasesSection />
        <FeaturesSection />
        <TechStackSection />
        <OpenAISection />
        <CoreConceptsSection />
      </main>
      <Footer />
      <ScrollToTopButton visible={isVisible} onClick={scrollToTop} />
    </div>
  );
}
