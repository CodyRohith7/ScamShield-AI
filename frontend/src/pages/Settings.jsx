import React from 'react';
import { Settings as SettingsIcon, Bell, Volume2, Palette, Globe, Shield, Save } from 'lucide-react';
import { motion } from 'framer-motion';
import useStore from '../store/useStore';
import toast from 'react-hot-toast';

const Settings = () => {
    const { settings, updateSettings } = useStore();

    const handleSave = () => {
        toast.success('Settings saved successfully!');
    };

    const SettingSection = ({ title, icon: Icon, children }) => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
        >
            <h3 className="text-xl font-semibold mb-6 flex items-center space-x-2">
                <Icon className="w-5 h-5 text-primary-400" />
                <span>{title}</span>
            </h3>
            <div className="space-y-4">
                {children}
            </div>
        </motion.div>
    );

    const Toggle = ({ label, description, checked, onChange }) => (
        <div className="flex items-center justify-between py-3 border-b border-slate-700 last:border-0">
            <div>
                <div className="text-white font-medium">{label}</div>
                <div className="text-sm text-slate-400">{description}</div>
            </div>
            <button
                onClick={() => onChange(!checked)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${checked ? 'bg-primary-500' : 'bg-slate-700'
                    }`}
            >
                <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${checked ? 'translate-x-6' : 'translate-x-1'
                        }`}
                />
            </button>
        </div>
    );

    return (
        <div className="min-h-screen p-6">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gradient">Settings</h1>
                <p className="text-slate-400 mt-2">Configure your ScamShield AI preferences</p>
            </div>

            <div className="max-w-4xl space-y-6">
                {/* Developer Zone */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="card border border-purple-500/30"
                >
                    <h3 className="text-xl font-semibold mb-6 flex items-center space-x-2">
                        <Database className="w-5 h-5 text-purple-400" />
                        <span>Developer & Demo Tools</span>
                    </h3>
                    <div className="bg-white/5 p-4 rounded-lg flex justify-between items-center">
                        <div>
                            <div className="text-white font-medium">Synthetic Traffic Generator</div>
                            <div className="text-sm text-gray-400">
                                Simulates background activity using AI bots. Useful for populating graphs.
                            </div>
                        </div>
                        <button
                            onClick={runSimulation}
                            disabled={simulating}
                            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded flex items-center gap-2 disabled:opacity-50"
                        >
                            <Play className="w-4 h-4" />
                            {simulating ? 'Simulating...' : 'Run Simulation'}
                        </button>
                    </div>
                </motion.div>

                {/* General Settings */}
                <SettingSection title="General" icon={SettingsIcon}>
                    <Toggle
                        label="Auto Scroll"
                        description="Automatically scroll to latest message in conversations"
                        checked={settings.autoScroll}
                        onChange={(val) => updateSettings({ autoScroll: val })}
                    />
                    <Toggle
                        label="Sound Effects"
                        description="Play sounds for notifications and events"
                        checked={settings.soundEnabled}
                        onChange={(val) => updateSettings({ soundEnabled: val })}
                    />
                    <Toggle
                        label="Notifications"
                        description="Show desktop notifications for important events"
                        checked={settings.notificationsEnabled}
                        onChange={(val) => updateSettings({ notificationsEnabled: val })}
                    />
                </SettingSection>

                {/* Conversation Settings */}
                <SettingSection title="Conversation" icon={Shield}>
                    <div className="py-3 border-b border-slate-700">
                        <label className="text-white font-medium block mb-2">Max Conversation Turns</label>
                        <input
                            type="number"
                            value={settings.maxConversationTurns}
                            onChange={(e) => updateSettings({ maxConversationTurns: parseInt(e.target.value) })}
                            className="input-field w-32"
                            min="5"
                            max="50"
                        />
                        <p className="text-sm text-slate-400 mt-1">Maximum number of turns before auto-exit</p>
                    </div>

                    <div className="py-3">
                        <label className="text-white font-medium block mb-2">Auto-Exit Risk Threshold</label>
                        <input
                            type="range"
                            value={settings.autoExitThreshold * 100}
                            onChange={(e) => updateSettings({ autoExitThreshold: e.target.value / 100 })}
                            className="w-full"
                            min="50"
                            max="100"
                        />
                        <div className="flex justify-between text-sm text-slate-400 mt-1">
                            <span>50%</span>
                            <span className="text-primary-400 font-semibold">{(settings.autoExitThreshold * 100).toFixed(0)}%</span>
                            <span>100%</span>
                        </div>
                        <p className="text-sm text-slate-400 mt-1">Exit conversation when risk score exceeds this threshold</p>
                    </div>
                </SettingSection>

                {/* Appearance */}
                <SettingSection title="Appearance" icon={Palette}>
                    <div className="py-3">
                        <label className="text-white font-medium block mb-3">Theme</label>
                        <div className="grid grid-cols-2 gap-3">
                            {['dark', 'light'].map((theme) => (
                                <button
                                    key={theme}
                                    onClick={() => updateSettings({ theme })}
                                    className={`p-4 rounded-lg border-2 transition-all ${settings.theme === theme
                                        ? 'border-primary-500 bg-primary-500/10'
                                        : 'border-slate-700 bg-slate-800/30 hover:border-slate-600'
                                        }`}
                                >
                                    <div className="text-white font-semibold capitalize">{theme}</div>
                                    <div className="text-xs text-slate-400 mt-1">
                                        {theme === 'dark' ? 'Dark mode (current)' : 'Light mode (coming soon)'}
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>
                </SettingSection>

                {/* Language */}
                <SettingSection title="Language & Region" icon={Globe}>
                    <div className="py-3">
                        <label className="text-white font-medium block mb-2">Interface Language</label>
                        <select
                            value={settings.language}
                            onChange={(e) => updateSettings({ language: e.target.value })}
                            className="input-field w-full"
                        >
                            <option value="en">English</option>
                            <option value="hi">हिन्दी (Hindi)</option>
                            <option value="hinglish">Hinglish</option>
                        </select>
                    </div>
                </SettingSection>

                {/* Save Button */}
                <div className="flex justify-end space-x-3">
                    <button className="btn btn-secondary">
                        Reset to Defaults
                    </button>
                    <button onClick={handleSave} className="btn btn-primary">
                        <Save className="w-4 h-4" />
                        Save Changes
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Settings;
