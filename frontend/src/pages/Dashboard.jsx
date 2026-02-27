import React, { useState, useEffect, useRef } from 'react';
import {
    Shield, MessageSquare, Send, Plus, Play, Pause,
    Download, Mail, TrendingUp, AlertTriangle, CheckCircle,
    Bot, User as UserIcon, Sparkles, Zap
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import { conversationAPI, mockScammerAPI, exportAPI, emailAPI } from '../utils/api';
import useStore from '../store/useStore';

const Dashboard = () => {
    const { settings, activeConversation, setActiveConversation } = useStore();

    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [testDemoMode, setTestDemoMode] = useState(false);
    const [showTemplateSelector, setShowTemplateSelector] = useState(false);
    const [selectedTemplate, setSelectedTemplate] = useState(null);
    const [currentTemplateIndex, setCurrentTemplateIndex] = useState(0);
    const [turnCount, setTurnCount] = useState(0);
    const [conversationData, setConversationData] = useState(null);
    const [scamTemplates, setScamTemplates] = useState([]);

    const chatContainerRef = useRef(null);
    const [userScrolled, setUserScrolled] = useState(false);
    const lastMessageCountRef = useRef(0);

    // Load scam templates on mount
    useEffect(() => {
        loadScamTemplates();
    }, []);

    const loadScamTemplates = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/scam-templates');
            const data = await response.json();
            setScamTemplates(data.templates || []);
        } catch (error) {
            console.error('Failed to load scam templates:', error);
        }
    };

    // Handle scroll detection - FIX FOR AUTO-SCROLL BUG
    const handleScroll = () => {
        if (!chatContainerRef.current) return;

        const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current;
        const isAtBottom = scrollHeight - scrollTop - clientHeight < 50;

        // User has scrolled up
        if (!isAtBottom) {
            setUserScrolled(true);
        } else {
            setUserScrolled(false);
        }
    };

    // Auto-scroll only when new messages arrive and user hasn't scrolled up
    useEffect(() => {
        if (messages.length > lastMessageCountRef.current && !userScrolled && settings.autoScroll) {
            scrollToBottom();
        }
        lastMessageCountRef.current = messages.length;
    }, [messages, userScrolled, settings.autoScroll]);

    const scrollToBottom = () => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTo({
                top: chatContainerRef.current.scrollHeight,
                behavior: 'smooth'
            });
        }
    };

    // Send message to agent
    const handleSendMessage = async () => {
        if (!inputMessage.trim() || loading) return;

        const userMessage = {
            id: Date.now(),
            role: 'scammer',
            content: inputMessage,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setLoading(true);
        setUserScrolled(false); // Reset scroll state when user sends message

        try {
            const response = await conversationAPI.engage(
                inputMessage,
                conversationData?.conversation_id || null
            );

            // Map entities to extracted_entities for display
            const mappedResponse = {
                ...response,
                extracted_entities: response.entities,
                scam_type: response.scam_type
            };

            setConversationData(mappedResponse);
            setTurnCount(response.turn_number || 1);

            const agentMessage = {
                id: Date.now() + 1,
                role: 'agent',
                content: response.agent_response,
                reasoning: response.internal_reasoning,
                persona: response.persona_used,
                timestamp: new Date().toISOString(),
                entities: response.entities,
                riskScore: response.risk_score
            };

            setMessages(prev => [...prev, agentMessage]);
            toast.success('Agent responded!');

        } catch (error) {
            console.error('Error:', error);
            toast.error('Failed to get agent response');
        } finally {
            setLoading(false);
        }
    };

    const handleNewConversation = () => {
        setMessages([]);
        setConversationData(null);
        setTurnCount(0);
        setTestDemoMode(false);
        setSelectedTemplate(null);
        setCurrentTemplateIndex(0);
        setUserScrolled(false);
        toast.success('New conversation started');
    };

    const startTestDemoMode = async (template) => {
        setShowTemplateSelector(false);
        setSelectedTemplate(template);
        setCurrentTemplateIndex(0);
        setTestDemoMode(true);
        setMessages([]);
        setConversationData(null);
        setTurnCount(0);

        toast.success(`🎬 Test Demo Mode: ${template.name}`);

        // Load full template
        try {
            const response = await fetch(`http://localhost:8000/api/scam-template/${template.id}`);
            const fullTemplate = await response.json();

            // Send first message after a short delay
            setTimeout(() => {
                sendTemplateMessage(fullTemplate, 0, []);
            }, 1000);
        } catch (error) {
            console.error('Failed to load template:', error);
            toast.error('Failed to load template');
            setTestDemoMode(false);
        }
    };

    const sendTemplateMessage = async (template, index, currentMessages = []) => {
        if (!template || !template.messages || index >= template.messages.length) {
            // End of template
            setTestDemoMode(false);
            toast.success('🎯 Test Demo completed!');
            return;
        }

        const scammerMessage = template.messages[index];

        // Add scammer message to chat
        const scammerMsg = {
            id: Date.now(),
            role: 'scammer',
            content: scammerMessage,
            timestamp: new Date().toISOString()
        };

        const updatedMessages = [...currentMessages, scammerMsg];
        setMessages(updatedMessages);
        setLoading(true);
        setUserScrolled(false);

        try {
            // Build conversation history for API
            const conversationHistory = updatedMessages.map(m => ({
                role: m.role,
                content: m.content
            }));

            // Get agent response
            const response = await conversationAPI.chat(
                scammerMessage,
                conversationHistory
            );

            setConversationData(response);
            setTurnCount(index + 1);

            const agentMessage = {
                id: Date.now() + 1,
                role: 'agent',
                content: response.agent_response,
                timestamp: new Date().toISOString(),
                entities: response.entities,
                riskScore: response.risk_score
            };

            const finalMessages = [...updatedMessages, agentMessage];
            setMessages(finalMessages);
            setCurrentTemplateIndex(index + 1);

            // Update conversationData with proper field names for display
            setConversationData({
                ...response,
                extracted_entities: response.entities,
                scam_type: response.scam_type
            });

            // Continue with next message after delay (REMOVED testDemoMode check)
            if (index + 1 < template.messages.length) {
                setTimeout(() => {
                    sendTemplateMessage(template, index + 1, finalMessages);
                }, 7000); // 7 second delay between messages
            } else {
                setTestDemoMode(false);
                toast.success('🎯 Test Demo completed!');
            }

        } catch (error) {
            console.error('Error:', error);
            toast.error('Test demo stopped due to error');
            setTestDemoMode(false);
        } finally {
            setLoading(false);
        }
    };

    const stopTestDemo = () => {
        setTestDemoMode(false);
        toast('Test demo stopped');
    };

    const handleExportJSON = async () => {
        if (!conversationData?.conversation_id) {
            toast.error('No conversation to export');
            return;
        }

        try {
            toast.loading('Exporting conversation...');

            // Try API export first
            try {
                const blob = await exportAPI.exportJSON(conversationData.conversation_id);
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `scamshield_${conversationData.conversation_id}.json`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
                toast.dismiss();
                toast.success('Exported as JSON!');
            } catch (apiError) {
                // Fallback: Export local data
                console.warn('API export failed, using local data:', apiError);
                const exportData = {
                    conversation_id: conversationData.conversation_id,
                    scam_type: conversationData.scam_type,
                    persona_used: conversationData.persona_used,
                    risk_score: conversationData.risk_score,
                    conversation_phase: conversationData.conversation_phase,
                    extracted_entities: conversationData.extracted_entities,
                    messages: messages,
                    turn_count: turnCount,
                    exported_at: new Date().toISOString()
                };

                const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `scamshield_local_${Date.now()}.json`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
                toast.dismiss();
                toast.success('Exported locally as JSON!');
            }
        } catch (error) {
            console.error('Export error:', error);
            toast.dismiss();
            toast.error('Export failed: ' + error.message);
        }
    };

    const handleSendEmail = async () => {
        if (!conversationData?.conversation_id) {
            toast.error('No conversation to send');
            return;
        }

        try {
            toast.loading('Sending email report...');
            await emailAPI.sendReport(conversationData.conversation_id, ['analyst@scamshield.ai']);
            toast.dismiss();
            toast.success('Report sent via email!');
        } catch (error) {
            toast.dismiss();
            if (error.response?.status === 503 || error.message.includes('Email service')) {
                toast.error('Email service not configured. Set SENDGRID_API_KEY in backend/.env');
            } else {
                toast.error('Email sending failed: ' + error.message);
            }
        }
    };

    return (
        <div className="min-h-screen p-6">
            {/* Header */}
            <div className="mb-6 flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gradient">Live Conversation Dashboard</h1>
                    <p className="text-slate-400 mt-1">Engage with scammers and extract intelligence in real-time</p>
                </div>

                <div className="flex items-center space-x-3">
                    <button onClick={handleNewConversation} className="btn btn-secondary">
                        <Plus className="w-4 h-4" />
                        New Conversation
                    </button>

                    {!testDemoMode && (
                        <>
                            <button onClick={() => setShowTemplateSelector(true)} className="btn btn-success">
                                <Play className="w-4 h-4" />
                                Test Demo Mode
                            </button>

                            {conversationData && (
                                <>
                                    <button onClick={handleExportJSON} className="btn btn-ghost">
                                        <Download className="w-4 h-4" />
                                    </button>

                                    <button onClick={handleSendEmail} className="btn btn-ghost">
                                        <Mail className="w-4 h-4" />
                                    </button>
                                </>
                            )}
                        </>
                    )}

                    {testDemoMode && (
                        <button onClick={stopTestDemo} className="btn btn-danger">
                            <Pause className="w-4 h-4" />
                            Stop Demo
                        </button>
                    )}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main Chat Area */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Chat Container */}
                    <div className="card h-[600px] flex flex-col">
                        <div className="flex items-center justify-between pb-4 border-b border-slate-700">
                            <h2 className="text-xl font-semibold flex items-center space-x-2">
                                <MessageSquare className="w-5 h-5 text-primary-400" />
                                <span>Live Chat</span>
                                {testDemoMode && (
                                    <span className="badge badge-success animate-pulse">TEST DEMO MODE</span>
                                )}
                            </h2>

                            {conversationData && (
                                <div className="flex items-center space-x-4 text-sm">
                                    <span className="text-slate-400">Turn: <span className="text-white font-semibold">{turnCount}</span></span>
                                    <div className={`px-3 py-1 rounded-lg font-semibold ${conversationData.risk_score > 70 ? 'bg-danger-500/20 text-danger-400' : 'bg-success-500/20 text-success-400'}`}>
                                        Risk: {conversationData.risk_score}/100
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Messages */}
                        <div
                            ref={chatContainerRef}
                            onScroll={handleScroll}
                            className="flex-1 overflow-y-auto space-y-4 py-4 pr-2"
                        >
                            {messages.length === 0 ? (
                                <div className="flex flex-col items-center justify-center h-full text-slate-400">
                                    <Bot className="w-16 h-16 mb-4 opacity-50" />
                                    <p className="text-lg">Start a conversation to engage with scammer</p>
                                    <p className="text-sm mt-2">Use quick scenarios below or type your own message</p>
                                </div>
                            ) : (
                                <AnimatePresence>
                                    {messages.map((msg, idx) => (
                                        <motion.div
                                            key={msg.id}
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ duration: 0.3 }}
                                            className={`flex ${msg.role === 'scammer' ? 'justify-end' : 'justify-start'}`}
                                        >
                                            <div className={`message-bubble ${msg.role === 'scammer' ? 'message-scammer' : 'message-agent'}`}>
                                                <div className="flex items-center space-x-2 mb-2">
                                                    {msg.role === 'scammer' ? (
                                                        <>
                                                            <AlertTriangle className="w-4 h-4 text-danger-400" />
                                                            <span className="text-xs font-semibold text-danger-300">Scammer</span>
                                                        </>
                                                    ) : (
                                                        <>
                                                            <Shield className="w-4 h-4 text-primary-400" />
                                                            <span className="text-xs font-semibold text-primary-300">
                                                                Agent {msg.persona && `(${msg.persona})`}
                                                            </span>
                                                        </>
                                                    )}
                                                    <span className="text-xs text-slate-500">
                                                        {new Date(msg.timestamp).toLocaleTimeString()}
                                                    </span>
                                                </div>

                                                <p className="text-white">{msg.content}</p>

                                                {msg.reasoning && (
                                                    <div className="mt-2 text-xs text-slate-400 italic border-t border-slate-700 pt-2">
                                                        💭 {msg.reasoning}
                                                    </div>
                                                )}

                                                {msg.role === 'agent' && conversationData && (
                                                    <div className="flex items-center gap-2 mt-2 pt-2 border-t border-slate-700">
                                                        <div className="px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs border border-purple-500/30 flex items-center gap-2">
                                                            <span>🎭 Persona:</span>
                                                            <span className="font-bold text-white">
                                                                {conversationData.persona_used || "Default Agent"}
                                                            </span>
                                                        </div>
                                                        <div className={`px-3 py-1 rounded-full text-xs font-bold border ${conversationData.risk_score > 70
                                                            ? 'bg-red-500/20 text-red-400 border-red-500/30'
                                                            : 'bg-green-500/20 text-green-400 border-green-500/30'
                                                            }`}>
                                                            Risk Score: {conversationData.risk_score || 0}%
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        </motion.div>
                                    ))}
                                </AnimatePresence>
                            )}

                            {loading && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="flex justify-start"
                                >
                                    <div className="message-bubble message-agent">
                                        <div className="flex items-center space-x-2">
                                            <div className="spinner w-4 h-4 border-2"></div>
                                            <span className="text-slate-400">Agent is thinking...</span>
                                        </div>
                                    </div>
                                </motion.div>
                            )}
                        </div>

                        {/* Scroll to Bottom Button */}
                        {userScrolled && (
                            <motion.button
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                onClick={() => {
                                    setUserScrolled(false);
                                    scrollToBottom();
                                }}
                                className="absolute bottom-24 right-8 btn btn-primary rounded-full w-12 h-12 flex items-center justify-center shadow-xl"
                            >
                                ↓
                            </motion.button>
                        )}

                        {/* Input Area */}
                        <div className="border-t border-slate-700 pt-4">
                            <div className="flex space-x-3">
                                <input
                                    type="text"
                                    value={inputMessage}
                                    onChange={(e) => setInputMessage(e.target.value)}
                                    onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                                    placeholder="Enter scammer's message..."
                                    className="input-field flex-1"
                                    disabled={loading || testDemoMode}
                                />
                                <button
                                    onClick={handleSendMessage}
                                    disabled={loading || !inputMessage.trim() || testDemoMode}
                                    className="btn btn-primary"
                                >
                                    <Send className="w-4 h-4" />
                                    Send
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Sidebar - Intelligence */}
                <div className="space-y-6">
                    {/* Stats Card */}
                    {conversationData && (
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="card"
                        >
                            <h3 className="text-lg font-semibold mb-4 flex items-center space-x-2">
                                <TrendingUp className="w-5 h-5 text-primary-400" />
                                <span>Intelligence</span>
                            </h3>

                            <div className="space-y-4">
                                <div className="bg-slate-700/30 rounded-lg p-3">
                                    <div className="text-xs text-slate-400">Scam Type</div>
                                    <div className="text-sm font-semibold text-white mt-1 capitalize">{conversationData.scam_type?.replace(/_/g, ' ')}</div>
                                </div>

                                <div className="bg-slate-700/30 rounded-lg p-3">
                                    <div className="text-xs text-slate-400">Persona Used</div>
                                    <div className="text-sm font-semibold text-white mt-1 capitalize">{conversationData.persona_used?.replace(/_/g, ' ')}</div>
                                </div>

                                <div className="bg-slate-700/30 rounded-lg p-3">
                                    <div className="text-xs text-slate-400">Confidence</div>
                                    <div className="text-sm font-semibold text-white mt-1 capitalize">{conversationData.confidence_level}</div>
                                </div>

                                {/* Extracted Entities */}
                                {conversationData.extracted_entities && (
                                    <div className="space-y-2">
                                        <div className="text-sm font-semibold text-slate-300">Extracted Entities:</div>

                                        {conversationData.extracted_entities.names?.length > 0 && (
                                            <div className="bg-slate-800/50 rounded p-2">
                                                <div className="text-xs text-slate-400 mb-1">👤 Names</div>
                                                {conversationData.extracted_entities.names.map((name, i) => (
                                                    <div key={i} className="text-xs font-mono text-primary-300">{name}</div>
                                                ))}
                                            </div>
                                        )}

                                        {conversationData.extracted_entities.phone_numbers?.length > 0 && (
                                            <div className="bg-slate-800/50 rounded p-2">
                                                <div className="text-xs text-slate-400 mb-1">📞 Phone Numbers</div>
                                                {conversationData.extracted_entities.phone_numbers.map((phone, i) => (
                                                    <div key={i} className="text-xs font-mono text-primary-300">{phone}</div>
                                                ))}
                                            </div>
                                        )}

                                        {conversationData.extracted_entities.upi_ids?.length > 0 && (
                                            <div className="bg-slate-800/50 rounded p-2">
                                                <div className="text-xs text-slate-400 mb-1">💳 UPI IDs</div>
                                                {conversationData.extracted_entities.upi_ids.map((upi, i) => (
                                                    <div key={i} className="text-xs font-mono text-primary-300">{upi}</div>
                                                ))}
                                            </div>
                                        )}

                                        {conversationData.scam_type && (
                                            <div className="bg-slate-800/50 rounded p-2">
                                                <div className="text-xs text-slate-400 mb-1">🎯 Scam Type</div>
                                                <div className="text-xs font-mono text-warning-300 capitalize">{conversationData.scam_type.replace(/_/g, ' ')}</div>
                                            </div>
                                        )}

                                        {conversationData.extracted_entities.bank_accounts?.length > 0 && (
                                            <div className="bg-slate-800/50 rounded p-2">
                                                <div className="text-xs text-slate-400 mb-1">🏦 Account Numbers</div>
                                                {conversationData.extracted_entities.bank_accounts.map((acc, i) => (
                                                    <div key={i} className="text-xs font-mono text-primary-300">{acc}</div>
                                                ))}
                                            </div>
                                        )}

                                        {conversationData.extracted_entities.phishing_links?.length > 0 && (
                                            <div className="bg-slate-800/50 rounded p-2">
                                                <div className="text-xs text-slate-400 mb-1">🔗 Phishing Links</div>
                                                {conversationData.extracted_entities.phishing_links.map((link, i) => (
                                                    <div key={i} className="text-xs font-mono text-danger-300 truncate">{link}</div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    )}

                    {/* System Status */}
                    <div className="card">
                        <h3 className="text-lg font-semibold mb-4">System Status</h3>
                        <div className="space-y-3">
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-slate-400">AI Engine</span>
                                <span className="flex items-center text-sm text-success-400">
                                    <span className="status-indicator status-online"></span>
                                    Online
                                </span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-slate-400">Mock Scammer API</span>
                                <span className="flex items-center text-sm text-success-400">
                                    <span className="status-indicator status-online"></span>
                                    Active
                                </span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-slate-400">Test Demo Mode</span>
                                <span className={`flex items-center text-sm ${testDemoMode ? 'text-success-400' : 'text-slate-500'}`}>
                                    <span className={`status-indicator ${testDemoMode ? 'status-online' : 'status-offline'}`}></span>
                                    {testDemoMode ? 'Active' : 'Inactive'}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Template Selector Modal */}
            {showTemplateSelector && (
                <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-6">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-slate-800 rounded-xl p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto border border-slate-700"
                    >
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-2xl font-bold text-gradient">Choose Your Scam Template</h2>
                            <button
                                onClick={() => setShowTemplateSelector(false)}
                                className="text-slate-400 hover:text-white"
                            >
                                ✕
                            </button>
                        </div>

                        <p className="text-slate-400 mb-6">
                            Select a pre-built scammer conversation to test the honeypot agent. The scammer messages will be sent automatically one by one, and the agent will respond to each.
                        </p>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {scamTemplates.map((template) => (
                                <button
                                    key={template.id}
                                    onClick={() => startTestDemoMode(template)}
                                    className="text-left bg-slate-700/30 hover:bg-slate-700/60 rounded-lg p-4 transition-all border border-slate-700 hover:border-primary-500 group"
                                >
                                    <div className="flex items-start justify-between mb-2">
                                        <div className="text-lg font-semibold text-white group-hover:text-primary-400 transition-colors">
                                            {template.name}
                                        </div>
                                        <div className="text-xs bg-primary-500/20 text-primary-300 px-2 py-1 rounded">
                                            {template.message_count} messages
                                        </div>
                                    </div>
                                    <div className="text-sm text-slate-400 mb-3">
                                        {template.description}
                                    </div>
                                    <div className="text-xs text-slate-500 capitalize">
                                        Type: {template.scam_type.replace(/_/g, ' ')}
                                    </div>
                                </button>
                            ))}
                        </div>

                        <div className="mt-6 text-center">
                            <button
                                onClick={() => setShowTemplateSelector(false)}
                                className="btn btn-secondary"
                            >
                                Cancel
                            </button>
                        </div>
                    </motion.div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
