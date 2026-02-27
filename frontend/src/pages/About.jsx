import React from 'react';
import { Shield, Users, Award, Target } from 'lucide-react';
import { motion } from 'framer-motion';

const About = () => {
    return (
        <div className="min-h-screen p-6">
            <div className="max-w-4xl mx-auto">
                {/* Hero Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-12"
                >
                    <div className="bg-gradient-to-br from-primary-500 to-purple-600 p-6 rounded-2xl inline-block mb-6 glow">
                        <Shield className="w-16 h-16 text-white" />
                    </div>
                    <h1 className="text-5xl font-bold text-gradient mb-4">ScamShield AI</h1>
                    <p className="text-xl text-slate-300 mb-2">Agentic Honey-Pot Intelligence Platform</p>
                    <p className="text-slate-400">India AI Impact Buildathon 2026</p>
                </motion.div>

                {/* Mission */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="card mb-8"
                >
                    <h2 className="text-2xl font-bold text-white mb-4">Our Mission</h2>
                    <p className="text-slate-300 leading-relaxed">
                        ScamShield AI is an advanced agentic honey-pot system designed to detect, engage, and extract intelligence from scammers.
                        Using state-of-the-art AI and NLP technologies, we create believable personas that interact with scammers to gather
                        critical information while protecting potential victims.
                    </p>
                </motion.div>

                {/* Features */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="card mb-8"
                >
                    <h2 className="text-2xl font-bold text-white mb-6">Key Features</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {[
                            { icon: '🤖', title: 'AI-Powered Detection', desc: 'Advanced NLP for scam classification' },
                            { icon: '🕵️', title: 'Multi-Persona Agents', desc: '5+ believable personas for engagement' },
                            { icon: '📊', title: 'Real-Time Analytics', desc: 'Comprehensive intelligence dashboard' },
                            { icon: '🕸️', title: 'Network Graphs', desc: 'Entity relationship visualization' },
                            { icon: '⚡', title: 'Auto-Mode', desc: 'Automated multi-turn conversations' },
                            { icon: '🛡️', title: 'Entity Extraction', desc: 'UPI, phone, bank, link detection' },
                        ].map((feature, idx) => (
                            <div key={idx} className="bg-slate-700/30 rounded-lg p-4">
                                <div className="text-3xl mb-2">{feature.icon}</div>
                                <h3 className="text-white font-semibold mb-1">{feature.title}</h3>
                                <p className="text-sm text-slate-400">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Impact */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="card mb-8"
                >
                    <h2 className="text-2xl font-bold text-white mb-6">Impact</h2>
                    <div className="grid grid-cols-3 gap-6 text-center">
                        <div>
                            <div className="text-4xl font-bold text-gradient mb-2">45+</div>
                            <div className="text-slate-400">Features Implemented</div>
                        </div>
                        <div>
                            <div className="text-4xl font-bold text-gradient mb-2">15+</div>
                            <div className="text-slate-400">Scam Types Detected</div>
                        </div>
                        <div>
                            <div className="text-4xl font-bold text-gradient mb-2">100%</div>
                            <div className="text-slate-400">Ethical & Safe</div>
                        </div>
                    </div>
                </motion.div>

                {/* Tech Stack */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="card mb-8"
                >
                    <h2 className="text-2xl font-bold text-white mb-6">Technology Stack</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {[
                            'React', 'FastAPI', 'OpenAI GPT', 'Google Gemini',
                            'Framer Motion', 'Recharts', 'D3.js', 'Zustand',
                            'TailwindCSS', 'Python', 'NLP', 'Machine Learning'
                        ].map((tech, idx) => (
                            <div key={idx} className="bg-slate-700/30 rounded-lg p-3 text-center">
                                <span className="text-white font-medium">{tech}</span>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Footer */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="text-center text-slate-500 text-sm"
                >
                    <p>🛡️ Built for India AI Impact Buildathon 2026</p>
                    <p className="mt-2">Making India safer, one scam at a time 🇮🇳</p>
                    <p className="mt-4">Version 2.0 - Premium Edition</p>
                </motion.div>
            </div>
        </div>
    );
};

export default About;
