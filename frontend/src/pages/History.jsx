import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function History() {
    const [conversations, setConversations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedConversation, setSelectedConversation] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [filterScamType, setFilterScamType] = useState('all');
    const [stats, setStats] = useState(null);
    const [page, setPage] = useState(0);
    const [totalConversations, setTotalConversations] = useState(0);

    const ITEMS_PER_PAGE = 20;

    useEffect(() => {
        loadConversations();
        loadStatistics();
    }, [page, filterScamType]);

    const loadConversations = async () => {
        try {
            setLoading(true);
            const response = await axios.get(`${API_BASE_URL}/api/conversations`);

            // Backend returns { conversations: [...] }
            setConversations(response.data.conversations || []);
            setTotalConversations(response.data.conversations?.length || 0);
        } catch (error) {
            console.error('Error loading conversations:', error);
            toast.error('Failed to load conversation history');
        } finally {
            setLoading(false);
        }
    };

    const loadStatistics = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/analytics`);
            const data = response.data;
            // Map analytics data to stats state structure
            setStats({
                total_conversations: data.total_conversations,
                active_conversations: data.recent_activity?.length || 0, // Placeholder
                completed_conversations: data.total_conversations, // Placeholder since we don't distinguish yet
                total_entities_extracted: data.total_entities
            });
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    };

    const handleSearch = async () => {
        // Client-side search since backend doesn't support it yet
        if (!searchQuery.trim()) {
            loadConversations();
            return;
        }

        const lowerQuery = searchQuery.toLowerCase();
        const filtered = conversations.filter(c =>
            c.id?.toString().includes(lowerQuery) ||
            c.scam_type?.toLowerCase().includes(lowerQuery) ||
            c.status?.toLowerCase().includes(lowerQuery)
        );

        setConversations(filtered);
        toast.success(`Found ${filtered.length} conversations`);
    };

    const viewConversation = async (conversationId) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/conversation/${conversationId}`);
            setSelectedConversation(response.data);
        } catch (error) {
            console.error('Error loading conversation:', error);
            toast.error('Failed to load conversation details');
        }
    };

    const deleteConversation = async (conversationId) => {
        toast.error('Delete not supported in this version');
    };

    const exportConversation = (conversation) => {
        // Use backend export endpoint
        window.open(`${API_BASE_URL}/api/export/json/${conversation.id || conversation.conversation_id}`, '_blank');
        toast.success('Export started');
    };

    const formatDate = (dateString) => {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getRiskColor = (score) => {
        if (score >= 0.7) return 'text-red-400';
        if (score >= 0.4) return 'text-yellow-400';
        return 'text-green-400';
    };

    const getScamTypeColor = (type) => {
        const colors = {
            'loan_approval': 'bg-blue-500/20 text-blue-300',
            'prize_lottery': 'bg-purple-500/20 text-purple-300',
            'investment': 'bg-green-500/20 text-green-300',
            'digital_arrest': 'bg-red-500/20 text-red-300',
            'other': 'bg-gray-500/20 text-gray-300'
        };
        return colors[type] || colors.other;
    };
    const [relatedCases, setRelatedCases] = useState(null);
    const [searchingRelated, setSearchingRelated] = useState(false);

    const checkRelatedCases = async (type, value) => {
        if (!value) return;

        try {
            setSearchingRelated(true);
            const response = await axios.get(`${API_BASE_URL}/api/intelligence/related`, {
                params: {
                    entity_type: type,
                    entity_value: value,
                    exclude_id: selectedConversation?.id
                }
            });

            if (response.data.count > 0) {
                setRelatedCases({
                    type,
                    value,
                    cases: response.data.related_conversations
                });
                toast.success(`Found ${response.data.count} linked cases!`);
            } else {
                toast.dismiss();
                toast('No other cases linked to this entity.', { icon: '🔍' });
            }
        } catch (error) {
            console.error('Error finding related cases:', error);
            toast.error('Failed to check for links');
        } finally {
            setSearchingRelated(false);
        }
    };

    const totalPages = Math.ceil(totalConversations / ITEMS_PER_PAGE);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
            {/* Related Cases Drawer/Modal */}
            <AnimatePresence>
                {relatedCases && (
                    <motion.div
                        initial={{ opacity: 0, x: 300 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 300 }}
                        className="fixed right-0 top-0 h-full w-80 bg-slate-900 border-l border-purple-500/30 p-6 shadow-2xl z-50 overflow-y-auto"
                    >
                        <div className="flex justify-between items-center mb-6">
                            <h3 className="text-xl font-bold text-white flex items-center gap-2">
                                <span className="text-2xl">🕸️</span> Network
                            </h3>
                            <button
                                onClick={() => setRelatedCases(null)}
                                className="text-gray-400 hover:text-white"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="mb-6">
                            <div className="text-xs text-purple-400 font-bold uppercase tracking-wider mb-1">
                                Linked Entity
                            </div>
                            <div className="bg-purple-500/10 border border-purple-500/30 p-3 rounded-lg text-white font-mono text-sm break-all">
                                {relatedCases.value}
                            </div>
                            <div className="text-xs text-gray-500 mt-1 capitalize">
                                {relatedCases.type.replace('_', ' ')}
                            </div>
                        </div>

                        <div>
                            <div className="text-xs text-gray-400 font-bold uppercase tracking-wider mb-3">
                                Linked Cases ({relatedCases.cases.length})
                            </div>
                            <div className="space-y-3">
                                {relatedCases.cases.map(cse => (
                                    <div
                                        key={cse.id}
                                        onClick={() => {
                                            viewConversation(cse.id);
                                            // Optional: close panel or keep it?
                                        }}
                                        className="bg-slate-800 p-3 rounded-lg border border-slate-700 hover:border-purple-500 cursor-pointer transition-colors"
                                    >
                                        <div className="flex justify-between items-start mb-1">
                                            <span className="text-white font-medium">#{cse.id}</span>
                                            <span className={`text-xs font-bold ${getRiskColor(cse.risk_score)}`}>
                                                {((cse.risk_score || 0) * 100).toFixed(0)}%
                                            </span>
                                        </div>
                                        <div className="text-xs text-gray-400 mb-1">
                                            {formatDate(cse.created_at)}
                                        </div>
                                        <div className="text-xs text-purple-300 bg-purple-500/10 px-2 py-0.5 rounded inline-block">
                                            {cse.scam_type?.replace('_', ' ')}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-8"
                >
                    <h1 className="text-4xl font-bold text-white mb-2">
                        📚 Conversation History
                    </h1>
                    <p className="text-gray-300">
                        View, search, and manage all past conversations
                    </p>
                </motion.div>

                {/* Statistics Cards */}
                {stats && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6"
                    >
                        <div className="glass-card p-4">
                            <div className="text-gray-400 text-sm mb-1">Total Conversations</div>
                            <div className="text-3xl font-bold text-white">{stats.total_conversations || 0}</div>
                        </div>
                        <div className="glass-card p-4">
                            <div className="text-gray-400 text-sm mb-1">Active</div>
                            <div className="text-3xl font-bold text-green-400">{stats.active_conversations || 0}</div>
                        </div>
                        <div className="glass-card p-4">
                            <div className="text-gray-400 text-sm mb-1">Completed</div>
                            <div className="text-3xl font-bold text-blue-400">{stats.completed_conversations || 0}</div>
                        </div>
                        <div className="glass-card p-4">
                            <div className="text-gray-400 text-sm mb-1">Entities Extracted</div>
                            <div className="text-3xl font-bold text-purple-400">{stats.total_entities_extracted || 0}</div>
                        </div>
                    </motion.div>
                )}

                {/* Search and Filters */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="glass-card p-4 mb-6"
                >
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="flex-1">
                            <input
                                type="text"
                                placeholder="Search conversations..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                                className="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-purple-500"
                            />
                        </div>
                        <button
                            onClick={handleSearch}
                            className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
                        >
                            🔍 Search
                        </button>
                        <select
                            value={filterScamType}
                            onChange={(e) => setFilterScamType(e.target.value)}
                            className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:border-purple-500"
                        >
                            <option value="all">All Types</option>
                            <option value="loan_approval">Loan Approval</option>
                            <option value="prize_lottery">Prize/Lottery</option>
                            <option value="investment">Investment</option>
                            <option value="digital_arrest">Digital Arrest</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                </motion.div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Conversation List */}
                    <div className="lg:col-span-2">
                        <div className="glass-card p-6">
                            <h2 className="text-xl font-bold text-white mb-4">
                                Conversations ({totalConversations})
                            </h2>

                            {loading ? (
                                <div className="text-center py-12">
                                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto"></div>
                                    <p className="text-gray-400 mt-4">Loading conversations...</p>
                                </div>
                            ) : conversations.length === 0 ? (
                                <div className="text-center py-12">
                                    <p className="text-gray-400 text-lg">No conversations found</p>
                                    <p className="text-gray-500 text-sm mt-2">Start a new conversation to see it here</p>
                                </div>
                            ) : (
                                <div className="space-y-3">
                                    <AnimatePresence>
                                        {conversations.map((conv, index) => (
                                            <motion.div
                                                key={conv.id}
                                                initial={{ opacity: 0, x: -20 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                exit={{ opacity: 0, x: 20 }}
                                                transition={{ delay: index * 0.05 }}
                                                className={`p-4 rounded-lg border cursor-pointer transition-all ${selectedConversation?.id === conv.id
                                                    ? 'bg-purple-500/20 border-purple-500'
                                                    : 'bg-white/5 border-white/10 hover:bg-white/10'
                                                    }`}
                                                onClick={() => viewConversation(conv.id)}
                                            >
                                                <div className="flex justify-between items-start mb-2">
                                                    <div className="flex-1">
                                                        <div className="flex items-center gap-2 mb-1">
                                                            <span className={`px-2 py-1 rounded text-xs font-medium ${getScamTypeColor(conv.scam_type)}`}>
                                                                {conv.scam_type?.replace('_', ' ').toUpperCase() || 'UNKNOWN'}
                                                            </span>
                                                            <span className="text-gray-400 text-xs">
                                                                {conv.turn_count || 0} turns
                                                            </span>
                                                        </div>
                                                        <div className="text-white font-medium">
                                                            #{conv.id}
                                                        </div>
                                                        <div className="text-gray-400 text-sm">
                                                            {formatDate(conv.created_at)}
                                                        </div>
                                                    </div>
                                                    <div className="text-right">
                                                        <div className={`text-2xl font-bold ${getRiskColor(conv.risk_score || 0)}`}>
                                                            {((conv.risk_score || 0) * 100).toFixed(0)}%
                                                        </div>
                                                        <div className="text-gray-400 text-xs">Risk</div>
                                                    </div>
                                                </div>

                                                <div className="flex gap-2 mt-3">
                                                    <button
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            exportConversation(conv);
                                                        }}
                                                        className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition-colors"
                                                    >
                                                        📥 Export
                                                    </button>
                                                    <button
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            deleteConversation(conv.id);
                                                        }}
                                                        className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-xs rounded transition-colors"
                                                    >
                                                        🗑️ Delete
                                                    </button>
                                                </div>
                                            </motion.div>
                                        ))}
                                    </AnimatePresence>
                                </div>
                            )}

                            {/* Pagination */}
                            {totalPages > 1 && (
                                <div className="flex justify-center items-center gap-2 mt-6">
                                    <button
                                        onClick={() => setPage(Math.max(0, page - 1))}
                                        disabled={page === 0}
                                        className="px-4 py-2 bg-white/10 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded transition-colors"
                                    >
                                        ← Previous
                                    </button>
                                    <span className="text-white">
                                        Page {page + 1} of {totalPages}
                                    </span>
                                    <button
                                        onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
                                        disabled={page >= totalPages - 1}
                                        className="px-4 py-2 bg-white/10 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded transition-colors"
                                    >
                                        Next →
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Conversation Details */}
                    <div className="lg:col-span-1">
                        <div className="glass-card p-6 sticky top-6">
                            <h2 className="text-xl font-bold text-white mb-4">Details</h2>

                            {!selectedConversation ? (
                                <div className="text-center py-12">
                                    <p className="text-gray-400">Select a conversation to view details</p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {/* Metadata */}
                                    <div>
                                        <div className="text-gray-400 text-sm mb-1">Conversation ID</div>
                                        <div className="text-white text-sm font-mono break-all">
                                            {selectedConversation.id}
                                        </div>
                                    </div>

                                    <div>
                                        <div className="text-gray-400 text-sm mb-1">Scam Type</div>
                                        <div className="text-white">
                                            {selectedConversation.scam_type?.replace('_', ' ').toUpperCase() || 'Unknown'}
                                        </div>
                                    </div>

                                    <div>
                                        <div className="text-gray-400 text-sm mb-1">Persona Used</div>
                                        <div className="text-white">
                                            {selectedConversation.persona_used || 'N/A'}
                                        </div>
                                    </div>

                                    <div>
                                        <div className="text-gray-400 text-sm mb-1">Risk Score</div>
                                        <div className={`text-2xl font-bold ${getRiskColor(selectedConversation.risk_score || 0)}`}>
                                            {((selectedConversation.risk_score || 0) * 100).toFixed(0)}%
                                        </div>
                                    </div>

                                    <div>
                                        <div className="text-gray-400 text-sm mb-1">Phase</div>
                                        <div className="text-white capitalize">
                                            {selectedConversation.conversation_phase || 'N/A'}
                                        </div>
                                    </div>

                                    {/* Entities */}
                                    <div>
                                        <div className="text-gray-400 text-sm mb-2">Extracted Entities</div>
                                        <div className="space-y-2">
                                            {Object.entries(selectedConversation.entities || {}).map(([key, values]) => {
                                                if (!Array.isArray(values) || values.length === 0) return null;
                                                return (
                                                    <div key={key} className="bg-white/5 p-2 rounded">
                                                        <div className="text-purple-400 text-xs font-medium mb-1 flex items-center justify-between">
                                                            <span>{key.replace('_', ' ').toUpperCase()}</span>
                                                            <span className="text-[10px] text-gray-500 bg-white/5 px-1 rounded">Click to check link</span>
                                                        </div>
                                                        {values.map((value, idx) => (
                                                            <button
                                                                key={idx}
                                                                onClick={() => checkRelatedCases(key, value)}
                                                                disabled={searchingRelated}
                                                                className="w-full text-left text-white text-sm font-mono break-all hover:bg-purple-500/20 p-1 rounded transition-colors flex items-center gap-2 group"
                                                            >
                                                                <span className="opacity-0 group-hover:opacity-100 text-xs">🔍</span>
                                                                {value}
                                                            </button>
                                                        ))}
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    {/* Messages */}
                                    <div>
                                        <div className="text-gray-400 text-sm mb-2">Messages ({selectedConversation.messages?.length || 0})</div>
                                        <div className="max-h-64 overflow-y-auto space-y-2">
                                            {selectedConversation.messages?.map((msg, idx) => (
                                                <div
                                                    key={idx}
                                                    className={`p-2 rounded text-sm ${msg.role === 'scammer'
                                                        ? 'bg-red-500/20 text-red-100'
                                                        : 'bg-green-500/20 text-green-100'
                                                        }`}
                                                >
                                                    <div className="font-medium text-xs mb-1">
                                                        {msg.role === 'scammer' ? '🚨 Scammer' : '🛡️ Agent'}
                                                    </div>
                                                    <div>{msg.content}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
