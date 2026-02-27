import React from 'react';
import { Book, MessageSquare, Shield, BarChart3, Download, Settings as SettingsIcon } from 'lucide-react';
import { motion } from 'framer-motion';

const Help = () => {
    const Section = ({ title, icon: Icon, children }) => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card mb-6"
        >
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center space-x-2">
                <Icon className="w-6 h-6 text-primary-400" />
                <span>{title}</span>
            </h2>
            {children}
        </motion.div>
    );

    return (
        <div className="min-h-screen p-6">
            <div className="max-w-4xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gradient">Help & Documentation</h1>
                    <p className="text-slate-400 mt-2">Learn how to use ScamShield AI effectively</p>
                </div>

                <Section title="Getting Started" icon={Book}>
                    <div className="space-y-4 text-slate-300">
                        <div>
                            <h3 className="text-white font-semibold mb-2">1. Login</h3>
                            <p>Sign in with your credentials or use Quick Demo Mode for instant access.</p>
                        </div>
                        <div>
                            <h3 className="text-white font-semibold mb-2">2. Start a Conversation</h3>
                            <p>Navigate to the Dashboard and either type a scammer message or use a quick scenario.</p>
                        </div>
                        <div>
                            <h3 className="text-white font-semibold mb-2">3. Enable Auto-Mode</h3>
                            <p>Click "Auto Mode" to let the agent automatically continue the conversation with the scammer.</p>
                        </div>
                        <div>
                            <h3 className="text-white font-semibold mb-2">4. Review Intelligence</h3>
                            <p>Check the sidebar for extracted entities, risk scores, and conversation insights.</p>
                        </div>
                    </div>
                </Section>

                <Section title="Dashboard Features" icon={MessageSquare}>
                    <div className="space-y-3">
                        <div className="bg-slate-700/30 rounded-lg p-4">
                            <h3 className="text-white font-semibold mb-2">💬 Live Chat</h3>
                            <p className="text-slate-300 text-sm">Real-time conversation with scammers using AI-powered personas.</p>
                        </div>
                        <div className="bg-slate-700/30 rounded-lg p-4">
                            <h3 className="text-white font-semibold mb-2">🤖 Auto-Mode</h3>
                            <p className="text-slate-300 text-sm">Automated multi-turn conversations that continue until intelligence is extracted.</p>
                        </div>
                        <div className="bg-slate-700/30 rounded-lg p-4">
                            <h3 className="text-white font-semibold mb-2">📊 Intelligence Panel</h3>
                            <p className="text-slate-300 text-sm">View extracted entities (UPI, phone, links) and risk scores in real-time.</p>
                        </div>
                        <div className="bg-slate-700/30 rounded-lg p-4">
                            <h3 className="text-white font-semibold mb-2">⚡ Quick Scenarios</h3>
                            <p className="text-slate-300 text-sm">Pre-configured scam messages for quick testing.</p>
                        </div>
                    </div>
                </Section>

                <Section title="Analytics" icon={BarChart3}>
                    <div className="text-slate-300 space-y-3">
                        <p>The Analytics page provides comprehensive insights:</p>
                        <ul className="list-disc list-inside space-y-2 ml-4">
                            <li>Total scams detected and entities extracted</li>
                            <li>Estimated fraud prevented (₹)</li>
                            <li>Scam type distribution (pie chart)</li>
                            <li>Risk score distribution (bar chart)</li>
                            <li>7-day trend analysis (line chart)</li>
                            <li>Top threat indicators</li>
                        </ul>
                    </div>
                </Section>

                <Section title="Data Export" icon={Download}>
                    <div className="text-slate-300 space-y-3">
                        <p>Export intelligence data in multiple formats:</p>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
                            <div className="bg-primary-500/20 border border-primary-500/30 rounded-lg p-3">
                                <h4 className="text-white font-semibold mb-1">JSON</h4>
                                <p className="text-xs text-slate-400">Complete data with metadata</p>
                            </div>
                            <div className="bg-success-500/20 border border-success-500/30 rounded-lg p-3">
                                <h4 className="text-white font-semibold mb-1">CSV</h4>
                                <p className="text-xs text-slate-400">Spreadsheet format</p>
                            </div>
                            <div className="bg-purple-500/20 border border-purple-500/30 rounded-lg p-3">
                                <h4 className="text-white font-semibold mb-1">Excel</h4>
                                <p className="text-xs text-slate-400">Formatted workbook</p>
                            </div>
                        </div>
                    </div>
                </Section>

                <Section title="Settings" icon={SettingsIcon}>
                    <div className="text-slate-300 space-y-3">
                        <p>Customize your experience:</p>
                        <ul className="list-disc list-inside space-y-2 ml-4">
                            <li><strong>Auto Scroll:</strong> Automatically scroll to latest messages</li>
                            <li><strong>Max Conversation Turns:</strong> Set limit for auto-mode (5-50)</li>
                            <li><strong>Auto-Exit Threshold:</strong> Risk score threshold for auto-exit (50-100%)</li>
                            <li><strong>Sound Effects:</strong> Enable/disable notification sounds</li>
                            <li><strong>Language:</strong> Choose interface language (English, Hindi, Hinglish)</li>
                        </ul>
                    </div>
                </Section>

                <div className="card bg-primary-500/10 border-primary-500/30">
                    <h3 className="text-white font-semibold mb-2">💡 Pro Tips</h3>
                    <ul className="text-slate-300 space-y-2 text-sm">
                        <li>• Use Auto-Mode for hands-free intelligence extraction</li>
                        <li>• Monitor the risk score to gauge conversation progress</li>
                        <li>• Export data regularly for backup and analysis</li>
                        <li>• Check Analytics for trends and patterns</li>
                        <li>• Adjust settings based on your workflow preferences</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default Help;
