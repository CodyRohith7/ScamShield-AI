import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { toast } from 'react-hot-toast';
import axios from 'axios';
import { TrendingUp, Users, Clock, AlertTriangle, Target, Activity } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function Campaigns() {
    const [campaigns, setCampaigns] = useState([]);
    const [activeCampaigns, setActiveCampaigns] = useState([]);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(false);
    const [selectedCampaign, setSelectedCampaign] = useState(null);
    const [detecting, setDetecting] = useState(false);

    useEffect(() => {
        loadActiveCampaigns();
        loadStatistics();
    }, []);

    const loadActiveCampaigns = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/campaigns/active`);
            setActiveCampaigns(response.data.active_campaigns || []);
        } catch (error) {
            console.error('Error loading campaigns:', error);
        }
    };

    const loadStatistics = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/campaigns/statistics`);
            setStats(response.data);
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    };

    const detectCampaigns = async () => {
        try {
            setDetecting(true);
            toast.loading('Analyzing conversations for campaigns...');

            const response = await axios.post(`${API_BASE_URL}/api/campaigns/detect`, {
                similarity_threshold: 0.7,
                min_conversations: 2
            });

            toast.dismiss();

            if (response.data.campaigns.length > 0) {
                setCampaigns(response.data.campaigns);
                toast.success(`Detected ${response.data.campaigns.length} campaigns!`);
                loadActiveCampaigns();
                loadStatistics();
            } else {
                toast.info('No campaigns detected. Need more conversations.');
            }
        } catch (error) {
            toast.dismiss();
            console.error('Error detecting campaigns:', error);
            toast.error('Campaign detection failed');
        } finally {
            setDetecting(false);
        }
    };

    const viewCampaignDetails = async (campaignId) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/campaigns/report/${campaignId}`);
            setSelectedCampaign(response.data);
        } catch (error) {
            console.error('Error loading campaign details:', error);
            toast.error('Failed to load campaign details');
        }
    };

    const getThreatColor = (level) => {
        const colors = {
            'critical': 'text-red-400 bg-red-500/20',
            'high': 'text-orange-400 bg-orange-500/20',
            'medium': 'text-yellow-400 bg-yellow-500/20',
            'low': 'text-green-400 bg-green-500/20'
        };
        return colors[level] || colors.low;
    };

    const getStatusColor = (status) => {
        return status === 'active'
            ? 'text-green-400 bg-green-500/20'
            : 'text-gray-400 bg-gray-500/20';
    };

    const formatDate = (dateString) => {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-8"
                >
                    <div className="flex justify-between items-start">
                        <div>
                            <h1 className="text-4xl font-bold text-white mb-2">
                                🎯 Campaign Intelligence
                            </h1>
                            <p className="text-gray-300">
                                Detect and track fraud campaigns across conversations
                            </p>
                        </div>
                        <button
                            onClick={detectCampaigns}
                            disabled={detecting}
                            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-all shadow-lg hover:shadow-xl"
                        >
                            {detecting ? '🔄 Analyzing...' : '🔍 Detect Campaigns'}
                        </button>
                    </div>
                </motion.div>

                {/* Statistics */}
                {stats && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6"
                    >
                        <div className="glass-card p-6">
                            <div className="flex items-center justify-between mb-2">
                                <Target className="w-8 h-8 text-purple-400" />
                                <div className="text-3xl font-bold text-white">
                                    {stats.total_campaigns || 0}
                                </div>
                            </div>
                            <div className="text-gray-400 text-sm">Total Campaigns</div>
                        </div>

                        <div className="glass-card p-6">
                            <div className="flex items-center justify-between mb-2">
                                <Activity className="w-8 h-8 text-green-400" />
                                <div className="text-3xl font-bold text-green-400">
                                    {stats.active_campaigns || 0}
                                </div>
                            </div>
                            <div className="text-gray-400 text-sm">Active Campaigns</div>
                        </div>

                        <div className="glass-card p-6">
                            <div className="flex items-center justify-between mb-2">
                                <Users className="w-8 h-8 text-blue-400" />
                                <div className="text-3xl font-bold text-blue-400">
                                    {stats.total_conversations_tracked || 0}
                                </div>
                            </div>
                            <div className="text-gray-400 text-sm">Conversations Tracked</div>
                        </div>

                        <div className="glass-card p-6">
                            <div className="flex items-center justify-between mb-2">
                                <TrendingUp className="w-8 h-8 text-yellow-400" />
                                <div className="text-3xl font-bold text-yellow-400">
                                    {stats.avg_conversations_per_campaign?.toFixed(1) || 0}
                                </div>
                            </div>
                            <div className="text-gray-400 text-sm">Avg Conv/Campaign</div>
                        </div>
                    </motion.div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Campaigns List */}
                    <div className="lg:col-span-2">
                        <div className="glass-card p-6">
                            <h2 className="text-xl font-bold text-white mb-4">
                                {campaigns.length > 0 ? 'Detected Campaigns' : 'Active Campaigns'}
                            </h2>

                            {(campaigns.length > 0 ? campaigns : activeCampaigns).length === 0 ? (
                                <div className="text-center py-12">
                                    <Target className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                                    <p className="text-gray-400 text-lg mb-2">No campaigns detected yet</p>
                                    <p className="text-gray-500 text-sm mb-4">
                                        Click "Detect Campaigns" to analyze conversations
                                    </p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {(campaigns.length > 0 ? campaigns : activeCampaigns).map((campaign, index) => (
                                        <motion.div
                                            key={campaign.campaign_id}
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: index * 0.1 }}
                                            className={`p-6 rounded-lg border cursor-pointer transition-all ${selectedCampaign?.campaign?.campaign_id === campaign.campaign_id
                                                    ? 'bg-purple-500/20 border-purple-500'
                                                    : 'bg-white/5 border-white/10 hover:bg-white/10'
                                                }`}
                                            onClick={() => viewCampaignDetails(campaign.campaign_id)}
                                        >
                                            {/* Header */}
                                            <div className="flex justify-between items-start mb-4">
                                                <div className="flex-1">
                                                    <div className="flex items-center gap-2 mb-2">
                                                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${getStatusColor(campaign.status)}`}>
                                                            {campaign.status?.toUpperCase()}
                                                        </span>
                                                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${getThreatColor(campaign.threat_level)}`}>
                                                            {campaign.threat_level?.toUpperCase()} THREAT
                                                        </span>
                                                    </div>
                                                    <h3 className="text-white font-bold text-lg mb-1">
                                                        {campaign.scam_type?.replace('_', ' ').toUpperCase()} Campaign
                                                    </h3>
                                                    <p className="text-gray-400 text-sm font-mono">
                                                        {campaign.campaign_id}
                                                    </p>
                                                </div>
                                                <div className="text-right">
                                                    <div className="text-3xl font-bold text-purple-400">
                                                        {campaign.conversation_count}
                                                    </div>
                                                    <div className="text-gray-400 text-xs">Conversations</div>
                                                </div>
                                            </div>

                                            {/* Stats Grid */}
                                            <div className="grid grid-cols-3 gap-4 mb-4">
                                                <div className="bg-white/5 p-3 rounded">
                                                    <div className="text-blue-400 text-xl font-bold">
                                                        {campaign.unique_numbers || 0}
                                                    </div>
                                                    <div className="text-gray-400 text-xs">Phone Numbers</div>
                                                </div>
                                                <div className="bg-white/5 p-3 rounded">
                                                    <div className="text-green-400 text-xl font-bold">
                                                        {campaign.unique_upi_ids || 0}
                                                    </div>
                                                    <div className="text-gray-400 text-xs">UPI IDs</div>
                                                </div>
                                                <div className="bg-white/5 p-3 rounded">
                                                    <div className="text-red-400 text-xl font-bold">
                                                        {campaign.unique_links || 0}
                                                    </div>
                                                    <div className="text-gray-400 text-xs">Phishing Links</div>
                                                </div>
                                            </div>

                                            {/* Timeline */}
                                            <div className="flex items-center gap-2 text-sm text-gray-400">
                                                <Clock className="w-4 h-4" />
                                                <span>{formatDate(campaign.start_date)}</span>
                                                <span>→</span>
                                                <span>{formatDate(campaign.end_date)}</span>
                                                <span className="ml-auto">
                                                    ({campaign.duration_days} days)
                                                </span>
                                            </div>

                                            {/* Script Preview */}
                                            {campaign.script_template && (
                                                <div className="mt-4 p-3 bg-black/30 rounded border border-white/10">
                                                    <div className="text-gray-400 text-xs mb-1">Script Template:</div>
                                                    <div className="text-white text-sm line-clamp-2">
                                                        "{campaign.script_template}"
                                                    </div>
                                                </div>
                                            )}
                                        </motion.div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Campaign Details */}
                    <div className="lg:col-span-1">
                        <div className="glass-card p-6 sticky top-6">
                            <h2 className="text-xl font-bold text-white mb-4">Campaign Details</h2>

                            {!selectedCampaign ? (
                                <div className="text-center py-12">
                                    <AlertTriangle className="w-12 h-12 text-gray-600 mx-auto mb-3" />
                                    <p className="text-gray-400">Select a campaign to view details</p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {/* Threat Assessment */}
                                    <div className="p-4 bg-gradient-to-br from-red-500/20 to-orange-500/20 rounded-lg border border-red-500/30">
                                        <div className="text-red-400 text-sm font-medium mb-1">Threat Level</div>
                                        <div className="text-2xl font-bold text-white">
                                            {selectedCampaign.campaign?.threat_level?.toUpperCase()}
                                        </div>
                                        <div className="text-red-300 text-sm mt-2">
                                            Risk Score: {(selectedCampaign.campaign?.avg_risk_score * 100).toFixed(0)}%
                                        </div>
                                    </div>

                                    {/* Evolution Timeline */}
                                    {selectedCampaign.campaign?.evolution && (
                                        <div>
                                            <div className="text-gray-400 text-sm mb-2">Campaign Evolution</div>
                                            <div className="space-y-2 max-h-48 overflow-y-auto">
                                                {selectedCampaign.campaign.evolution.map((stage, idx) => (
                                                    <div key={idx} className="p-2 bg-white/5 rounded text-sm">
                                                        <div className="flex justify-between items-center">
                                                            <span className="text-purple-400 font-medium">Stage {stage.stage}</span>
                                                            <span className="text-gray-400 text-xs">
                                                                Risk: {(stage.risk_score * 100).toFixed(0)}%
                                                            </span>
                                                        </div>
                                                        <div className="text-gray-400 text-xs mt-1">
                                                            {stage.entities_extracted} entities • {stage.conversation_phase}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Full Report */}
                                    {selectedCampaign.report && (
                                        <div>
                                            <div className="text-gray-400 text-sm mb-2">Full Report</div>
                                            <div className="p-4 bg-black/30 rounded border border-white/10 max-h-96 overflow-y-auto">
                                                <pre className="text-white text-xs whitespace-pre-wrap font-mono">
                                                    {selectedCampaign.report}
                                                </pre>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
