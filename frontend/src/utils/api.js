import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000,
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        // Add auth token if available
        const token = localStorage.getItem('auth_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Handle unauthorized
            localStorage.removeItem('auth_token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// ============================================================================
// API Methods
// ============================================================================

export const conversationAPI = {
    // Send chat message (new simple endpoint)
    chat: async (message, conversationHistory = []) => {
        const response = await api.post('/api/chat', {
            message,
            conversation_history: conversationHistory
        });
        return response.data;
    },

    // Legacy engage method (for backwards compatibility)
    engage: async (message, conversationId = null) => {
        const response = await api.post('/api/chat', {
            message,
            conversation_history: []
        });
        return response.data;
    },

    // Get conversation by ID (will implement in backend)
    getConversation: async (conversationId) => {
        const response = await api.get(`/api/conversation/${conversationId}`);
        return response.data;
    },

    // Get conversation stats (will implement in backend)
    getStats: async (conversationId) => {
        const response = await api.get(`/api/conversation/${conversationId}/stats`);
        return response.data;
    },

    // List all conversations (will implement in backend)
    listAll: async () => {
        const response = await api.get('/api/conversations');
        return response.data;
    },

    // Continue conversation (multi-turn)
    continueConversation: async (conversationId, scammerMessage) => {
        const response = await api.post('/api/chat', {
            message: scammerMessage,
            conversation_history: []
        });
        return response.data;
    }
};

export const mockScammerAPI = {
    // List available scam scenarios
    listScenarios: async () => {
        const response = await api.get('/api/mock-scammer/scenarios');
        return response.data;
    },

    // Generate scammer response
    generateResponse: async (victimMessage, scamType, turnNumber, history = []) => {
        const response = await api.post('/api/mock-scammer/generate', {
            victim_message: victimMessage,
            scam_type: scamType,
            turn_number: turnNumber,
            conversation_history: history
        });
        return response.data;
    }
};

export const analyticsAPI = {
    // Get overall metrics
    getMetrics: async () => {
        const response = await api.get('/api/analytics/metrics');
        return response.data;
    },

    // Get trend data
    getTrends: async (period = '7d') => {
        const response = await api.get(`/api/analytics/trends?period=${period}`);
        return response.data;
    },

    // Get network graph data
    getNetworkGraph: async () => {
        const response = await api.get('/api/analytics/network-graph');
        return response.data;
    },

    // Get scam type distribution
    getScamDistribution: async () => {
        const response = await api.get('/api/analytics/scam-distribution');
        return response.data;
    }
};

export const exportAPI = {
    // Export as JSON
    exportJSON: async (conversationId) => {
        const response = await api.get(`/api/export/json/${conversationId}`, {
            responseType: 'blob'
        });
        return response.data;
    },

    // Export as PDF
    exportPDF: async (conversationId) => {
        const response = await api.get(`/api/export/pdf/${conversationId}`, {
            responseType: 'blob'
        });
        return response.data;
    },

    // Export all as CSV
    exportCSV: async () => {
        const response = await api.get('/api/export/csv', {
            responseType: 'blob'
        });
        return response.data;
    },

    // Export all as Excel
    exportExcel: async () => {
        const response = await api.get('/api/export/excel', {
            responseType: 'blob'
        });
        return response.data;
    }
};

export const emailAPI = {
    // Send report via email
    sendReport: async (conversationId, recipients) => {
        const response = await api.post(`/api/email/send-report/${conversationId}`, {
            recipients
        });
        return response.data;
    }
};

export const healthAPI = {
    // Health check
    check: async () => {
        const response = await api.get('/api/health');
        return response.data;
    }
};

// Helper function to download blob
export const downloadBlob = (blob, filename) => {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
};

export default api;
