import React from 'react';
import { Download, FileJson, FileText, Table, Mail } from 'lucide-react';
import { motion } from 'framer-motion';
import { exportAPI } from '../utils/api';
import toast from 'react-hot-toast';

const DataExport = () => {
    const handleExport = async (format) => {
        try {
            let blob;
            let filename;

            switch (format) {
                case 'json':
                    blob = await exportAPI.exportJSON('all');
                    filename = 'scamshield_data.json';
                    break;
                case 'csv':
                    blob = await exportAPI.exportCSV();
                    filename = 'scamshield_data.csv';
                    break;
                case 'excel':
                    blob = await exportAPI.exportExcel();
                    filename = 'scamshield_data.xlsx';
                    break;
                default:
                    return;
            }

            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.click();
            toast.success(`Exported as ${format.toUpperCase()}!`);
        } catch (error) {
            toast.error('Export failed');
        }
    };

    const ExportCard = ({ title, description, icon: Icon, format, color }) => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card card-interactive"
            onClick={() => handleExport(format)}
        >
            <div className={`bg-${color}-500/20 p-4 rounded-xl mb-4 inline-block`}>
                <Icon className={`w-8 h-8 text-${color}-400`} />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
            <p className="text-slate-400 text-sm mb-4">{description}</p>
            <button className={`btn btn-${color === 'primary' ? 'primary' : 'secondary'} w-full`}>
                <Download className="w-4 h-4" />
                Export as {format.toUpperCase()}
            </button>
        </motion.div>
    );

    return (
        <div className="min-h-screen p-6">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gradient">Data Export</h1>
                <p className="text-slate-400 mt-2">Export intelligence data in various formats</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                <ExportCard
                    title="JSON Export"
                    description="Complete data with all fields and metadata"
                    icon={FileJson}
                    format="json"
                    color="primary"
                />
                <ExportCard
                    title="CSV Export"
                    description="Spreadsheet-compatible format for analysis"
                    icon={Table}
                    format="csv"
                    color="success"
                />
                <ExportCard
                    title="Excel Export"
                    description="Formatted workbook with multiple sheets"
                    icon={FileText}
                    format="excel"
                    color="purple"
                />
            </div>

            <div className="card">
                <h3 className="text-xl font-semibold mb-4">Export Options</h3>
                <div className="space-y-4">
                    <div className="flex items-center justify-between py-3 border-b border-slate-700">
                        <div>
                            <div className="text-white font-medium">Include Conversation History</div>
                            <div className="text-sm text-slate-400">Full chat logs for each conversation</div>
                        </div>
                        <input type="checkbox" defaultChecked className="w-5 h-5" />
                    </div>
                    <div className="flex items-center justify-between py-3 border-b border-slate-700">
                        <div>
                            <div className="text-white font-medium">Include Entity Metadata</div>
                            <div className="text-sm text-slate-400">Confidence scores and validation status</div>
                        </div>
                        <input type="checkbox" defaultChecked className="w-5 h-5" />
                    </div>
                    <div className="flex items-center justify-between py-3">
                        <div>
                            <div className="text-white font-medium">Anonymize Sensitive Data</div>
                            <div className="text-sm text-slate-400">Remove personally identifiable information</div>
                        </div>
                        <input type="checkbox" className="w-5 h-5" />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DataExport;
