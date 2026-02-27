import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';
import axios from 'axios';
import { Share2, RefreshCw } from 'lucide-react';
import ForceGraph from '../components/ForceGraph';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function Syndicate() {
    const [graphData, setGraphData] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const [selectedNode, setSelectedNode] = useState(null);

    useEffect(() => {
        loadGraph();
    }, []);

    const loadGraph = async () => {
        try {
            setLoading(true);
            const response = await axios.get(`${API_BASE_URL}/api/intelligence/graph`);
            setGraphData(response.data || { nodes: [], links: [] });
            toast.success(`Loaded ${response.data.nodes.length} network nodes`);
        } catch (error) {
            console.error('Error loading graph:', error);
            toast.error('Failed to load network intelligence');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-900 p-6">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Share2 className="text-purple-500" />
                        Syndicate Brain
                    </h1>
                    <p className="text-gray-400">Visual Fraud Network Analysis</p>
                </div>
                <button
                    onClick={loadGraph}
                    className="p-2 bg-white/10 hover:bg-white/20 rounded-full text-white transition-colors"
                    title="Refresh Graph"
                >
                    <RefreshCw className="w-5 h-5" />
                </button>
            </div>

            <div className="flex gap-6 h-[calc(100vh-140px)]">
                {/* Main Graph Area */}
                <div className="flex-1 glass-card p-1 rounded-2xl overflow-hidden relative">
                    {loading ? (
                        <div className="absolute inset-0 flex items-center justify-center">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
                        </div>
                    ) : (
                        <ForceGraph
                            data={graphData}
                            onNodeClick={setSelectedNode}
                        />
                    )}
                </div>

                {/* Details Sidebar */}
                <AnimatePresence>
                    {selectedNode && (
                        <motion.div
                            initial={{ width: 0, opacity: 0 }}
                            animate={{ width: 350, opacity: 1 }}
                            exit={{ width: 0, opacity: 0 }}
                            className="bg-slate-800 border-l border-slate-700 overflow-hidden flex flex-col"
                        >
                            <div className="p-6 min-w-[350px]">
                                <h2 className="text-xl font-bold text-white mb-2">
                                    Node Intelligence
                                </h2>
                                <div className="p-3 bg-white/5 rounded-lg mb-4 text-center">
                                    <div
                                        className="w-12 h-12 rounded-full mx-auto mb-2 flex items-center justify-center text-xl font-bold border-2 border-white/20"
                                        style={{ backgroundColor: selectedNode.color }}
                                    >
                                        {selectedNode.type === 'conversation' ? '💬' : '🔍'}
                                    </div>
                                    <div className="text-white font-mono break-all font-bold">
                                        {selectedNode.label}
                                    </div>
                                    <div className="text-sm text-gray-400 capitalize mt-1">
                                        {selectedNode.subtype || selectedNode.type}
                                    </div>
                                </div>

                                {selectedNode.type === 'conversation' && (
                                    <div className="space-y-3">
                                        <div className="bg-black/30 p-3 rounded">
                                            <div className="text-xs text-gray-500 uppercase">Scam Type</div>
                                            <div className="text-purple-300 font-medium capitalize">
                                                {selectedNode.data.scam_type?.replace('_', ' ')}
                                            </div>
                                        </div>
                                        <div className="bg-black/30 p-3 rounded">
                                            <div className="text-xs text-gray-500 uppercase">Risk Score</div>
                                            <div className={`font-bold ${selectedNode.data.risk_score > 0.7 ? 'text-red-400' : 'text-green-400'
                                                }`}>
                                                {(selectedNode.data.risk_score * 100).toFixed(0)}%
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {selectedNode.type === 'entity' && (
                                    <div className="space-y-3">
                                        <div className="bg-black/30 p-3 rounded">
                                            <div className="text-xs text-gray-500 uppercase">Connections</div>
                                            {/* We could count links if we computed them client side fully, 
                                                for now this is just a placeholder or needs 'links' access */}
                                            <div className="text-white">Active in multiple cases</div>
                                        </div>
                                        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded text-red-300 text-sm">
                                            ⚠️ This entity is part of a fraud network.
                                        </div>
                                    </div>
                                )}

                                <button
                                    className="mt-6 w-full py-2 bg-white/10 hover:bg-white/20 text-white rounded transition-colors"
                                    onClick={() => setSelectedNode(null)}
                                >
                                    Close Details
                                </button>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
