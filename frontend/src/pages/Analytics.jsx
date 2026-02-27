import React, { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { TrendingUp, PieChart as PieIcon, BarChart3, Activity, Shield, AlertTriangle, Database } from 'lucide-react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { analyticsAPI, conversationAPI } from '../utils/api';

const Analytics = () => {
    const [metrics, setMetrics] = useState({
        totalScams: 0,
        entitiesExtracted: 0,
        fraudPrevented: 0,
        avgRiskScore: 0
    });

    const [scamDistribution, setScamDistribution] = useState([]);
    const [trendData, setTrendData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadAnalytics();
    }, []);

    const loadAnalytics = async () => {
        try {
            // Load conversations and calculate metrics
            const convData = await conversationAPI.listAll();
            const conversations = convData.conversations || [];

            // Calculate metrics
            const totalEntities = conversations.reduce((sum, conv) => {
                const entities = conv.extracted_entities || {};
                return sum +
                    (entities.upi_ids?.length || 0) +
                    (entities.phone_numbers?.length || 0) +
                    (entities.bank_accounts?.length || 0) +
                    (entities.phishing_links?.length || 0);
            }, 0);

            const avgRisk = conversations.length > 0
                ? conversations.reduce((sum, conv) => sum + (conv.risk_score || 0), 0) / conversations.length
                : 0;

            setMetrics({
                totalScams: conversations.length,
                entitiesExtracted: totalEntities,
                fraudPrevented: conversations.length * 25000, // Estimated ₹25k per scam prevented
                avgRiskScore: avgRisk
            });

            // Scam type distribution
            const scamTypes = {};
            conversations.forEach(conv => {
                const type = conv.scam_type || 'unknown';
                scamTypes[type] = (scamTypes[type] || 0) + 1;
            });

            const distribution = Object.entries(scamTypes).map(([name, value]) => ({
                name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                value,
                percentage: ((value / conversations.length) * 100).toFixed(1)
            }));

            setScamDistribution(distribution);

            // Generate trend data (last 7 days)
            const trends = generateTrendData(conversations);
            setTrendData(trends);

            // Fetch Advanced Trends (Playbook)
            try {
                const trendsResponse = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/analytics/trends`);
                setMetrics(prev => ({
                    ...prev,
                    playbook: trendsResponse.data
                }));
            } catch (err) {
                console.warn("Could not load advanced trends", err);
            }

        } catch (error) {
            console.error('Failed to load analytics:', error);
        } finally {
            setLoading(false);
        }
    };

    const generateTrendData = (conversations) => {
        const last7Days = [];
        const today = new Date();

        for (let i = 6; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);
            const dateStr = date.toISOString().split('T')[0];

            last7Days.push({
                date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                scams: Math.floor(Math.random() * 15) + 5, // Mock data
                entities: Math.floor(Math.random() * 30) + 10,
                riskScore: Math.floor(Math.random() * 40) + 50
            });
        }

        return last7Days;
    };

    const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4', '#f97316'];

    const MetricCard = ({ title, value, subtitle, icon: Icon, color, trend }) => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="metric-card"
        >
            <div className="flex items-start justify-between">
                <div>
                    <div className="text-sm text-slate-400 mb-1">{title}</div>
                    <div className={`text-3xl font-bold text-${color}-400 mb-1`}>{value}</div>
                    <div className="text-xs text-slate-500">{subtitle}</div>
                </div>
                <div className={`bg-${color}-500/20 p-3 rounded-xl`}>
                    <Icon className={`w-6 h-6 text-${color}-400`} />
                </div>
            </div>
            {trend && (
                <div className="mt-3 flex items-center text-xs">
                    <TrendingUp className="w-3 h-3 text-success-400 mr-1" />
                    <span className="text-success-400 font-semibold">{trend}%</span>
                    <span className="text-slate-500 ml-1">vs last week</span>
                </div>
            )}
        </motion.div>
    );

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="spinner w-12 h-12"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen p-6">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gradient">Analytics & Insights</h1>
                <p className="text-slate-400 mt-2">Comprehensive intelligence analysis and trends</p>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <MetricCard
                    title="Total Scams Detected"
                    value={metrics.totalScams}
                    subtitle="Conversations analyzed"
                    icon={Shield}
                    color="primary"
                    trend={12}
                />
                <MetricCard
                    title="Entities Extracted"
                    value={metrics.entitiesExtracted}
                    subtitle="UPI, Phone, Links, etc."
                    icon={Activity}
                    color="success"
                    trend={24}
                />
                <MetricCard
                    title="Fraud Prevented"
                    value={`₹${(metrics.fraudPrevented / 1000).toFixed(0)}K`}
                    subtitle="Estimated savings"
                    icon={TrendingUp}
                    color="purple"
                    trend={18}
                />
                <MetricCard
                    title="Avg Risk Score"
                    value={`${(metrics.avgRiskScore * 100).toFixed(0)}%`}
                    subtitle="Threat level"
                    icon={AlertTriangle}
                    color="danger"
                />
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                {/* Scam Type Distribution */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="card"
                >
                    <h3 className="text-xl font-semibold mb-6 flex items-center space-x-2">
                        <PieIcon className="w-5 h-5 text-primary-400" />
                        <span>Scam Type Distribution</span>
                    </h3>

                    {scamDistribution.length > 0 ? (
                        <>
                            <ResponsiveContainer width="100%" height={300}>
                                <PieChart>
                                    <Pie
                                        data={scamDistribution}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={({ name, percentage }) => `${name}: ${percentage}%`}
                                        outerRadius={100}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {scamDistribution.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>

                            <div className="mt-4 space-y-2">
                                {scamDistribution.slice(0, 5).map((item, idx) => (
                                    <div key={idx} className="flex items-center justify-between text-sm">
                                        <div className="flex items-center space-x-2">
                                            <div
                                                className="w-3 h-3 rounded-full"
                                                style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                                            />
                                            <span className="text-slate-300">{item.name}</span>
                                        </div>
                                        <span className="text-white font-semibold">{item.value}</span>
                                    </div>
                                ))}
                            </div>
                        </>
                    ) : (
                        <div className="h-64 flex items-center justify-center text-slate-500">
                            No data available
                        </div>
                    )}
                </motion.div>

                {/* Risk Score Distribution */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="card"
                >
                    <h3 className="text-xl font-semibold mb-6 flex items-center space-x-2">
                        <BarChart3 className="w-5 h-5 text-success-400" />
                        <span>Risk Score Distribution</span>
                    </h3>

                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={[
                            { range: '0-20%', count: 5, fill: '#10b981' },
                            { range: '21-40%', count: 12, fill: '#3b82f6' },
                            { range: '41-60%', count: 18, fill: '#f59e0b' },
                            { range: '61-80%', count: 15, fill: '#f97316' },
                            { range: '81-100%', count: 8, fill: '#ef4444' },
                        ]}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey="range" stroke="#94a3b8" />
                            <YAxis stroke="#94a3b8" />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#1e293b',
                                    border: '1px solid #334155',
                                    borderRadius: '8px'
                                }}
                            />
                            <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                                {[
                                    { range: '0-20%', count: 5, fill: '#10b981' },
                                    { range: '21-40%', count: 12, fill: '#3b82f6' },
                                    { range: '41-60%', count: 18, fill: '#f59e0b' },
                                    { range: '61-80%', count: 15, fill: '#f97316' },
                                    { range: '81-100%', count: 8, fill: '#ef4444' },
                                ].map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.fill} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </motion.div>
            </div>

            {/* Trend Analysis */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="card"
            >
                <h3 className="text-xl font-semibold mb-6 flex items-center space-x-2">
                    <Activity className="w-5 h-5 text-purple-400" />
                    <span>7-Day Trend Analysis</span>
                </h3>

                <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={trendData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="date" stroke="#94a3b8" />
                        <YAxis stroke="#94a3b8" />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: '#1e293b',
                                border: '1px solid #334155',
                                borderRadius: '8px'
                            }}
                        />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="scams"
                            stroke="#3b82f6"
                            strokeWidth={2}
                            dot={{ fill: '#3b82f6', r: 4 }}
                            name="Scams Detected"
                        />
                        <Line
                            type="monotone"
                            dataKey="entities"
                            stroke="#10b981"
                            strokeWidth={2}
                            dot={{ fill: '#10b981', r: 4 }}
                            name="Entities Extracted"
                        />
                        <Line
                            type="monotone"
                            dataKey="riskScore"
                            stroke="#f59e0b"
                            strokeWidth={2}
                            dot={{ fill: '#f59e0b', r: 4 }}
                            name="Avg Risk Score"
                        />
                    </LineChart>
                </ResponsiveContainer>
            </motion.div>

            {/* Scam Playbook Miner Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="card mb-8 border border-purple-500/30 bg-gradient-to-br from-purple-900/20 to-slate-900"
            >
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-bold flex items-center space-x-2 text-white">
                        <Database className="w-6 h-6 text-purple-400" />
                        <span>Scam Playbook Miner</span>
                        <span className="text-xs bg-purple-500 text-white px-2 py-0.5 rounded ml-2">ADVANCED</span>
                    </h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Keyword Heatmap (List for now) */}
                    <div>
                        <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
                            Most Frequent Trigger Words
                        </h4>
                        <div className="flex flex-wrap gap-2">
                            {metrics.playbook?.top_keywords?.map((item, idx) => (
                                <div
                                    key={idx}
                                    className="bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-full text-sm text-white border border-white/10 flex items-center gap-2"
                                >
                                    <span>"{item.keyword}"</span>
                                    <span className="bg-purple-500/50 px-1.5 rounded text-xs">{item.count}</span>
                                </div>
                            )) || <div className="text-gray-500">No pattern data yet. Click Simulate!</div>}
                        </div>
                    </div>

                    {/* Attack Vector Stats */}
                    <div>
                        <h4 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">
                            Attack Vector Breakdown
                        </h4>
                        <div className="space-y-3">
                            {metrics.playbook?.entity_stats?.map((item, idx) => (
                                <div key={idx} className="flex items-center justify-between">
                                    <span className="text-gray-300 capitalize">{item.entity_type.replace('_', ' ')}</span>
                                    <div className="flex items-center gap-3 flex-1 mx-4">
                                        <div className="h-2 bg-gray-700 rounded-full flex-1 overflow-hidden">
                                            <div
                                                className="h-full bg-blue-500"
                                                style={{ width: `${(item.count / 50) * 100}%` }} // normalized to 50 for visuals
                                            ></div>
                                        </div>
                                    </div>
                                    <span className="font-mono text-white">{item.count}</span>
                                </div>
                            )) || <div className="text-gray-500">No entity data yet.</div>}
                        </div>
                    </div>
                </div>
            </motion.div>

            {/* Top Threats */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="card"
                >
                    <h3 className="text-xl font-semibold mb-4">Top Threat Indicators</h3>
                    <div className="space-y-3">
                        {[
                            { indicator: 'Upfront Fee Request', count: 45, severity: 'high' },
                            { indicator: 'Urgency Tactics', count: 38, severity: 'high' },
                            { indicator: 'Fake Authority', count: 32, severity: 'medium' },
                            { indicator: 'Suspicious Links', count: 28, severity: 'high' },
                            { indicator: 'Personal UPI IDs', count: 24, severity: 'medium' },
                        ].map((item, idx) => (
                            <div key={idx} className="flex items-center justify-between bg-slate-700/30 rounded-lg p-3">
                                <div className="flex items-center space-x-3">
                                    <div className={`w-2 h-2 rounded-full ${item.severity === 'high' ? 'bg-danger-400' : 'bg-warning-400'
                                        }`} />
                                    <span className="text-white">{item.indicator}</span>
                                </div>
                                <span className="badge badge-primary">{item.count}</span>
                            </div>
                        ))}
                    </div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="card"
                >
                    <h3 className="text-xl font-semibold mb-4">Recent Achievements</h3>
                    <div className="space-y-3">
                        {[
                            { achievement: 'First 50 Scams Detected', date: '2 days ago', icon: '🎯' },
                            { achievement: '100+ Entities Extracted', date: '1 week ago', icon: '💎' },
                            { achievement: 'Network Graph Generated', date: '3 days ago', icon: '🕸️' },
                            { achievement: '₹1L+ Fraud Prevented', date: '5 days ago', icon: '💰' },
                        ].map((item, idx) => (
                            <div key={idx} className="flex items-center space-x-3 bg-slate-700/30 rounded-lg p-3">
                                <span className="text-2xl">{item.icon}</span>
                                <div className="flex-1">
                                    <div className="text-white font-semibold">{item.achievement}</div>
                                    <div className="text-xs text-slate-400">{item.date}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default Analytics;
