import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Rocket, Target, Users, TrendingUp, Star, Lightbulb, Trophy } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="container mx-auto px-4 py-12"
    >
      {/* Hero Section */}
      <div className="relative text-center mb-16">
        <div 
          className="absolute inset-0 bg-cover bg-center opacity-5 dark:opacity-5"
          style={{ 
            backgroundImage: 'url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=2000")',
            backgroundBlendMode: 'overlay',
          }}
        />
        <div className="relative">
          <motion.h1 
            initial={{ y: -20 }}
            animate={{ y: 0 }}
            className="text-4xl md:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600"
          >
            Turn Your Vision Into Reality
          </motion.h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
            Join the next generation of innovators. Use AI-powered insights to transform your idea into a successful startup.
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/assessment')}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-lg"
          >
            Start Free Assessment
          </motion.button>
        </div>
      </div>

      {/* Stats Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16 bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg">
        <div className="text-center">
          <h3 className="text-3xl font-bold text-blue-600 dark:text-blue-400">500+</h3>
          <p className="text-gray-600 dark:text-gray-400">Startups Launched</p>
        </div>
        <div className="text-center">
          <h3 className="text-3xl font-bold text-purple-600 dark:text-purple-400">$10M+</h3>
          <p className="text-gray-600 dark:text-gray-400">Funding Raised</p>
        </div>
        <div className="text-center">
          <h3 className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">95%</h3>
          <p className="text-gray-600 dark:text-gray-400">Success Rate</p>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-8 mb-16">
        <motion.div
          whileHover={{ y: -5 }}
          className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <Target className="h-12 w-12 text-blue-600 mb-4" />
          <h3 className="text-xl font-semibold mb-2 dark:text-white">Smart Analysis</h3>
          <p className="text-gray-600 dark:text-gray-400">AI-powered insights to validate your idea with real market needs</p>
        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <Users className="h-12 w-12 text-purple-600 mb-4" />
          <h3 className="text-xl font-semibold mb-2 dark:text-white">Market Fit</h3>
          <p className="text-gray-600 dark:text-gray-400">Deep understanding of your target audience and market opportunity</p>
        </motion.div>

        <motion.div
          whileHover={{ y: -5 }}
          className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <TrendingUp className="h-12 w-12 text-indigo-600 mb-4" />
          <h3 className="text-xl font-semibold mb-2 dark:text-white">Growth Strategy</h3>
          <p className="text-gray-600 dark:text-gray-400">Clear roadmap for scaling your startup to success</p>
        </motion.div>
      </div>

      {/* Testimonials */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-8 dark:text-white">Success Stories</h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
            <div className="flex items-center mb-4">
              <img
                src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=100"
                alt="Sarah Chen"
                className="w-12 h-12 rounded-full mr-4"
              />
              <div>
                <h4 className="font-semibold dark:text-white">Sarah Chen</h4>
                <p className="text-gray-600 dark:text-gray-400">TechStart Founder</p>
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-400 italic">
              "HustleBot helped me validate my SaaS idea and secure seed funding within 3 months. The insights were invaluable!"
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
            <div className="flex items-center mb-4">
              <img
                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=100"
                alt="Mark Thompson"
                className="w-12 h-12 rounded-full mr-4"
              />
              <div>
                <h4 className="font-semibold dark:text-white">Mark Thompson</h4>
                <p className="text-gray-600 dark:text-gray-400">HealthTech Innovator</p>
              </div>
            </div>
            <p className="text-gray-600 dark:text-gray-400 italic">
              "The structured assessment helped us identify critical gaps in our business model before launch."
            </p>
          </div>
        </div>
      </div>

      {/* Inspirational Quotes */}
      <div className="grid md:grid-cols-2 gap-8 mb-16">
        <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-8 rounded-2xl text-white">
          <Lightbulb className="h-8 w-8 mb-4" />
          <blockquote className="text-xl font-light mb-4">
            "Innovation distinguishes between a leader and a follower."
          </blockquote>
          <cite className="text-sm">- Steve Jobs</cite>
        </div>
        <div className="bg-gradient-to-br from-purple-500 to-indigo-600 p-8 rounded-2xl text-white">
          <Star className="h-8 w-8 mb-4" />
          <blockquote className="text-xl font-light mb-4">
            "The biggest risk is not taking any risk."
          </blockquote>
          <cite className="text-sm">- Mark Zuckerberg</cite>
        </div>
      </div>

      {/* Final CTA Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-white text-center relative overflow-hidden">
        <div className="absolute inset-0 bg-cover bg-center opacity-10"
             style={{ 
               backgroundImage: 'url("https://images.unsplash.com/photo-1581090700227-2730d8d3e2da?auto=format&fit=crop&q=80&w=2000")',
               backgroundBlendMode: 'overlay',
             }} />
        <div className="relative">
          <Trophy className="h-16 w-16 mx-auto mb-6 text-yellow-300" />
          <h2 className="text-4xl font-bold mb-4">Ready to Transform Your Idea?</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Join thousands of successful founders who turned their innovative ideas into thriving businesses
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/assessment')}
            className="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg"
          >
            Start Your Journey Now
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};

export default LandingPage;