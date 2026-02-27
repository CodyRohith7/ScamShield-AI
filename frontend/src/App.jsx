import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { Menu } from 'lucide-react';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import History from './pages/History';
import Campaigns from './pages/Campaigns';
import Syndicate from './pages/Syndicate';
import DataExport from './pages/DataExport';
import Settings from './pages/Settings';
import Help from './pages/Help';
import About from './pages/About';

// Components
import Sidebar from './components/Sidebar';

// Store
import useStore from './store/useStore';

// Styles
import './index.css';

function App() {
    const { isAuthenticated } = useStore();
    const [sidebarOpen, setSidebarOpen] = useState(false);

    // Protected Route Component
    const ProtectedRoute = ({ children }) => {
        if (!isAuthenticated) {
            return <Navigate to="/login" replace />;
        }
        return children;
    };

    // Layout Component
    const Layout = ({ children }) => (
        <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800">
            <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            <div className="flex-1 flex flex-col min-w-0">
                {/* Mobile Header */}
                <header className="lg:hidden bg-slate-900 border-b border-slate-800 p-4">
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="text-slate-400 hover:text-white"
                    >
                        <Menu className="w-6 h-6" />
                    </button>
                </header>

                {/* Main Content */}
                <main className="flex-1 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );

    return (
        <Router>
            <Toaster
                position="top-right"
                toastOptions={{
                    duration: 3000,
                    style: {
                        background: '#1e293b',
                        color: '#fff',
                        border: '1px solid #334155',
                        borderRadius: '12px',
                        padding: '16px',
                    },
                    success: {
                        iconTheme: {
                            primary: '#10b981',
                            secondary: '#fff',
                        },
                    },
                    error: {
                        iconTheme: {
                            primary: '#ef4444',
                            secondary: '#fff',
                        },
                    },
                }}
            />

            <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<Login />} />

                {/* Protected Routes */}
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Dashboard />
                            </Layout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/analytics"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Analytics />
                            </Layout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/history"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <History />
                            </Layout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/campaigns"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Campaigns />
                            </Layout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/export"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <DataExport />
                            </Layout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/syndicate"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Syndicate />
                            </Layout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/settings"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Settings />
                            </Layout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/help"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Help />
                            </Layout>
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/about"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <About />
                            </Layout>
                        </ProtectedRoute>
                    }
                />

                {/* Redirects */}
                <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} />
                <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} />
            </Routes>
        </Router>
    );
}

export default App;
