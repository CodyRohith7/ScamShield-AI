import React from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import {
    Shield, LayoutDashboard, BarChart3, Download, Settings,
    HelpCircle, Info, LogOut, Menu, X, History as HistoryIcon, Target, Share2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import useStore from '../store/useStore';

const Sidebar = ({ isOpen, onClose }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const { user, logout } = useStore();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const navItems = [
        { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
        { path: '/analytics', icon: BarChart3, label: 'Analytics' },
        { path: '/history', icon: HistoryIcon, label: 'History' },
        { path: '/history', icon: HistoryIcon, label: 'History' },
        { path: '/campaigns', icon: Target, label: 'Campaigns' },
        { path: '/syndicate', icon: Share2, label: 'Syndicate Brain' },
        { path: '/export', icon: Download, label: 'Data Export' },
        { path: '/settings', icon: Settings, label: 'Settings' },
        { path: '/help', icon: HelpCircle, label: 'Help' },
        { path: '/about', icon: Info, label: 'About' },
    ];

    return (
        <>
            {/* Mobile Overlay */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                    />
                )}
            </AnimatePresence>

            {/* Sidebar */}
            <motion.aside
                initial={{ x: -280 }}
                animate={{ x: isOpen ? 0 : -280 }}
                transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                className="fixed left-0 top-0 h-screen w-70 bg-slate-900 border-r border-slate-800 z-50 lg:translate-x-0 lg:static"
            >
                <div className="flex flex-col h-full">
                    {/* Header */}
                    <div className="p-6 border-b border-slate-800">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                                <div className="bg-gradient-to-br from-primary-500 to-purple-600 p-2 rounded-lg">
                                    <Shield className="w-6 h-6 text-white" />
                                </div>
                                <div>
                                    <h1 className="text-lg font-bold text-white">ScamShield AI</h1>
                                    <p className="text-xs text-slate-400">v2.0 Premium</p>
                                </div>
                            </div>
                            <button onClick={onClose} className="lg:hidden text-slate-400 hover:text-white">
                                <X className="w-5 h-5" />
                            </button>
                        </div>
                    </div>

                    {/* User Info */}
                    {user && (
                        <div className="p-4 border-b border-slate-800">
                            <div className="flex items-center space-x-3">
                                <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                                    {user.name?.charAt(0) || 'U'}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <div className="text-sm font-semibold text-white truncate">{user.name}</div>
                                    <div className="text-xs text-slate-400 capitalize">{user.role}</div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Navigation */}
                    <nav className="flex-1 overflow-y-auto p-4">
                        <div className="space-y-1">
                            {navItems.map((item) => {
                                const Icon = item.icon;
                                const isActive = location.pathname === item.path;

                                return (
                                    <NavLink
                                        key={item.path}
                                        to={item.path}
                                        onClick={() => window.innerWidth < 1024 && onClose()}
                                        className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${isActive
                                            ? 'bg-primary-500/20 text-primary-400 border border-primary-500/30'
                                            : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                            }`}
                                    >
                                        <Icon className="w-5 h-5" />
                                        <span className="font-medium">{item.label}</span>
                                        {isActive && (
                                            <motion.div
                                                layoutId="activeTab"
                                                className="ml-auto w-1.5 h-1.5 bg-primary-400 rounded-full"
                                            />
                                        )}
                                    </NavLink>
                                );
                            })}
                        </div>
                    </nav>

                    {/* Footer */}
                    <div className="p-4 border-t border-slate-800">
                        <button
                            onClick={handleLogout}
                            className="flex items-center space-x-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white transition-all w-full"
                        >
                            <LogOut className="w-5 h-5" />
                            <span className="font-medium">Logout</span>
                        </button>

                        <div className="mt-4 text-center text-xs text-slate-500">
                            <p>🛡️ ScamShield AI</p>
                            <p className="mt-1">India AI Buildathon 2026</p>
                        </div>
                    </div>
                </div>
            </motion.aside>
        </>
    );
};

export default Sidebar;
