import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Global state management for ScamShield AI
const useStore = create(
    persist(
        (set, get) => ({
            // User & Authentication
            user: null,
            isAuthenticated: false,
            userRole: 'analyst', // analyst, manager, admin

            setUser: (user) => set({ user, isAuthenticated: true }),
            logout: () => set({ user: null, isAuthenticated: false }),
            setUserRole: (role) => set({ userRole: role }),

            // Active Conversations
            conversations: [],
            activeConversation: null,

            setConversations: (conversations) => set({ conversations }),
            setActiveConversation: (conversation) => set({ activeConversation: conversation }),
            addConversation: (conversation) => set((state) => ({
                conversations: [conversation, ...state.conversations]
            })),
            updateConversation: (id, updates) => set((state) => ({
                conversations: state.conversations.map(conv =>
                    conv.conversation_id === id ? { ...conv, ...updates } : conv
                ),
                activeConversation: state.activeConversation?.conversation_id === id
                    ? { ...state.activeConversation, ...updates }
                    : state.activeConversation
            })),

            // Analytics & Metrics
            metrics: {
                totalScamsHandled: 0,
                entitiesExtracted: 0,
                fraudPrevented: 0,
                activeConversations: 0,
                avgRiskScore: 0
            },

            setMetrics: (metrics) => set({ metrics }),

            // Threat Feed
            threatFeed: [],
            addThreatFeedItem: (item) => set((state) => ({
                threatFeed: [item, ...state.threatFeed].slice(0, 50) // Keep last 50
            })),

            // Settings
            settings: {
                autoScroll: true,
                soundEnabled: true,
                notificationsEnabled: true,
                theme: 'dark',
                maxConversationTurns: 15,
                autoExitThreshold: 0.9,
                language: 'en'
            },

            updateSettings: (newSettings) => set((state) => ({
                settings: { ...state.settings, ...newSettings }
            })),

            // UI State
            sidebarOpen: true,
            toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),

            // Network Graph Data
            networkData: { nodes: [], edges: [] },
            setNetworkData: (data) => set({ networkData: data }),
        }),
        {
            name: 'scamshield-storage',
            partialize: (state) => ({
                user: state.user,
                isAuthenticated: state.isAuthenticated,
                userRole: state.userRole,
                settings: state.settings
            })
        }
    )
);

export default useStore;
