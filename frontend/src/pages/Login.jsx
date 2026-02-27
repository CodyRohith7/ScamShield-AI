import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Lock, User, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import useStore from '../store/useStore';
import toast from 'react-hot-toast';

const Login = () => {
    const navigate = useNavigate();
    const { setUser, setUserRole } = useStore();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [selectedRole, setSelectedRole] = useState('analyst');
    const [loading, setLoading] = useState(false);

    const roles = [
        {
            id: 'analyst',
            name: 'Analyst',
            description: 'Full access to conversations and intelligence',
            icon: '🔍'
        },
        {
            id: 'manager',
            name: 'Manager',
            description: 'Overview dashboards and reports',
            icon: '📊'
        },
        {
            id: 'admin',
            name: 'Administrator',
            description: 'System configuration and management',
            icon: '⚙️'
        }
    ];

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);

        // Simulate authentication (replace with real auth in production)
        setTimeout(() => {
            const user = {
                id: '1',
                username: username || 'demo_user',
                role: selectedRole,
                name: username || 'Demo User',
                email: `${username || 'demo'}@scamshield.ai`
            };

            setUser(user);
            setUserRole(selectedRole);
            toast.success(`Welcome back, ${user.name}!`);
            navigate('/dashboard');
            setLoading(false);
        }, 1000);
    };

    const handleDemoMode = () => {
        const demoUser = {
            id: 'demo',
            username: 'demo_analyst',
            role: 'analyst',
            name: 'Demo Analyst',
            email: 'demo@scamshield.ai'
        };

        setUser(demoUser);
        setUserRole('analyst');
        toast.success('Entered Demo Mode!');
        navigate('/dashboard');
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden">
            {/* Animated Background */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute w-96 h-96 bg-primary-500/10 rounded-full blur-3xl -top-48 -left-48 animate-pulse"></div>
                <div className="absolute w-96 h-96 bg-purple-500/10 rounded-full blur-3xl -bottom-48 -right-48 animate-pulse" style={{ animationDelay: '1s' }}></div>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-5xl relative z-10"
            >
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Left Side - Branding */}
                    <div className="flex flex-col justify-center space-y-6">
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.2 }}
                            className="flex items-center space-x-4"
                        >
                            <div className="bg-gradient-to-br from-primary-500 to-purple-600 p-4 rounded-2xl glow">
                                <Shield className="w-12 h-12 text-white" />
                            </div>
                            <div>
                                <h1 className="text-5xl font-bold text-gradient">ScamShield AI</h1>
                                <p className="text-slate-400 mt-2">Agentic Honey-Pot Intelligence Platform</p>
                            </div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.3 }}
                            className="space-y-4"
                        >
                            <div className="flex items-start space-x-3">
                                <div className="bg-success-500/20 p-2 rounded-lg mt-1">
                                    <span className="text-2xl">🤖</span>
                                </div>
                                <div>
                                    <h3 className="text-lg font-semibold text-white">AI-Powered Detection</h3>
                                    <p className="text-slate-400 text-sm">Advanced NLP & ML for scam classification</p>
                                </div>
                            </div>

                            <div className="flex items-start space-x-3">
                                <div className="bg-primary-500/20 p-2 rounded-lg mt-1">
                                    <span className="text-2xl">🕵️</span>
                                </div>
                                <div>
                                    <h3 className="text-lg font-semibold text-white">Intelligence Extraction</h3>
                                    <p className="text-slate-400 text-sm">Automated entity extraction & validation</p>
                                </div>
                            </div>

                            <div className="flex items-start space-x-3">
                                <div className="bg-purple-500/20 p-2 rounded-lg mt-1">
                                    <span className="text-2xl">📊</span>
                                </div>
                                <div>
                                    <h3 className="text-lg font-semibold text-white">Real-Time Analytics</h3>
                                    <p className="text-slate-400 text-sm">Network graphs & trend analysis</p>
                                </div>
                            </div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.4 }}
                            className="glass-card p-4"
                        >
                            <p className="text-sm text-slate-300">
                                <span className="font-semibold text-primary-400">🇮🇳 India AI Impact Buildathon 2026</span>
                                <br />
                                Making India safer, one scam at a time
                            </p>
                        </motion.div>
                    </div>

                    {/* Right Side - Login Form */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3 }}
                        className="glass-card p-8"
                    >
                        <div className="mb-6">
                            <h2 className="text-2xl font-bold text-white mb-2">Welcome Back</h2>
                            <p className="text-slate-400">Sign in to access the intelligence platform</p>
                        </div>

                        <form onSubmit={handleLogin} className="space-y-6">
                            {/* Username */}
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    <User className="w-4 h-4 inline mr-2" />
                                    Username
                                </label>
                                <input
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    placeholder="Enter your username"
                                    className="input-field"
                                />
                            </div>

                            {/* Password */}
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    <Lock className="w-4 h-4 inline mr-2" />
                                    Password
                                </label>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="Enter your password"
                                    className="input-field"
                                />
                            </div>

                            {/* Role Selection */}
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-3">
                                    Select Role
                                </label>
                                <div className="grid grid-cols-1 gap-3">
                                    {roles.map((role) => (
                                        <div
                                            key={role.id}
                                            onClick={() => setSelectedRole(role.id)}
                                            className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${selectedRole === role.id
                                                    ? 'border-primary-500 bg-primary-500/10'
                                                    : 'border-slate-700 bg-slate-800/30 hover:border-slate-600'
                                                }`}
                                        >
                                            <div className="flex items-center space-x-3">
                                                <span className="text-2xl">{role.icon}</span>
                                                <div className="flex-1">
                                                    <div className="font-semibold text-white">{role.name}</div>
                                                    <div className="text-xs text-slate-400">{role.description}</div>
                                                </div>
                                                {selectedRole === role.id && (
                                                    <div className="w-5 h-5 bg-primary-500 rounded-full flex items-center justify-center">
                                                        <div className="w-2 h-2 bg-white rounded-full"></div>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Login Button */}
                            <button
                                type="submit"
                                disabled={loading}
                                className="btn btn-primary w-full"
                            >
                                {loading ? (
                                    <>
                                        <div className="spinner w-5 h-5 border-2"></div>
                                        Signing in...
                                    </>
                                ) : (
                                    <>
                                        Sign In
                                        <ArrowRight className="w-5 h-5" />
                                    </>
                                )}
                            </button>

                            {/* Demo Mode */}
                            <div className="relative">
                                <div className="absolute inset-0 flex items-center">
                                    <div className="w-full border-t border-slate-700"></div>
                                </div>
                                <div className="relative flex justify-center text-sm">
                                    <span className="px-2 bg-slate-900 text-slate-400">or</span>
                                </div>
                            </div>

                            <button
                                type="button"
                                onClick={handleDemoMode}
                                className="btn btn-secondary w-full"
                            >
                                🚀 Quick Demo Mode
                            </button>
                        </form>

                        <div className="mt-6 text-center text-xs text-slate-500">
                            <p>Demo credentials: Any username/password will work</p>
                            <p className="mt-1">Or use Quick Demo Mode for instant access</p>
                        </div>
                    </motion.div>
                </div>

                {/* Footer */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6 }}
                    className="mt-8 text-center text-sm text-slate-500"
                >
                    <p>🛡️ ScamShield AI v2.0 - Premium Intelligence Platform</p>
                    <p className="mt-1">Built for India AI Impact Buildathon 2026</p>
                </motion.div>
            </motion.div>
        </div>
    );
};

export default Login;
