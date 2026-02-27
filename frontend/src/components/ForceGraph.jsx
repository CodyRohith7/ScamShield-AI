import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

const ForceGraph = ({ data, onNodeClick }) => {
    const canvasRef = useRef(null);
    const [tooltip, setTooltip] = useState(null);

    // Physics simulation state
    const simulationRef = useRef({
        nodes: [],
        links: [],
        animationId: null,
        draggingNode: null,
        transform: { x: 0, y: 0, k: 1 }
    });

    useEffect(() => {
        if (!data || !data.nodes || !data.links) return;

        // Initialize simulation data
        const width = canvasRef.current.width;
        const height = canvasRef.current.height;

        simulationRef.current.nodes = data.nodes.map(n => ({
            ...n,
            x: Math.random() * width,
            y: Math.random() * height,
            vx: 0,
            vy: 0
        }));

        simulationRef.current.links = data.links.map(l => ({
            source: l.source,
            target: l.target
        }));

        startSimulation();

        return () => stopSimulation();
    }, [data]);

    const startSimulation = () => {
        if (simulationRef.current.animationId) return;
        animate();
    };

    const stopSimulation = () => {
        if (simulationRef.current.animationId) {
            cancelAnimationFrame(simulationRef.current.animationId);
            simulationRef.current.animationId = null;
        }
    };

    const animate = () => {
        updatePhysics();
        draw();
        simulationRef.current.animationId = requestAnimationFrame(animate);
    };

    const updatePhysics = () => {
        const { nodes, links } = simulationRef.current;
        const width = canvasRef.current.width;
        const height = canvasRef.current.height;
        const k = 100; // Exploring constant (repulsion)

        // 1. Repulsion (Nodes push apart)
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const a = nodes[i];
                const b = nodes[j];
                const dx = a.x - b.x;
                const dy = a.y - b.y;
                let dist = Math.sqrt(dx * dx + dy * dy) || 1;

                if (dist < 300) {
                    const force = (k * k) / dist;
                    const fx = (dx / dist) * force * 0.05;
                    const fy = (dy / dist) * force * 0.05;

                    a.vx += fx;
                    a.vy += fy;
                    b.vx -= fx;
                    b.vy -= fy;
                }
            }
        }

        // 2. Attraction (Springs along links)
        links.forEach(link => {
            const source = nodes.find(n => n.id === link.source);
            const target = nodes.find(n => n.id === link.target);
            if (!source || !target) return;

            const dx = target.x - source.x;
            const dy = target.y - source.y;
            const dist = Math.sqrt(dx * dx + dy * dy) || 1;
            const force = (dist - 100) * 0.05; // Spring length 100

            const fx = (dx / dist) * force;
            const fy = (dy / dist) * force;

            source.vx += fx;
            source.vy += fy;
            target.vx -= fx;
            target.vy -= fy;
        });

        // 3. Center Gravity & Velocity Update
        nodes.forEach(node => {
            // Push to center
            const dx = (width / 2) - node.x;
            const dy = (height / 2) - node.y;
            node.vx += dx * 0.01;
            node.vy += dy * 0.01;

            if (node !== simulationRef.current.draggingNode) {
                node.vx *= 0.9; // Friction
                node.vy *= 0.9;
                node.x += node.vx;
                node.y += node.vy;
            }
        });
    };

    const draw = () => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const { nodes, links } = simulationRef.current;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw Links
        ctx.strokeStyle = '#4b5563'; // Gray-600
        ctx.lineWidth = 1;
        links.forEach(link => {
            const source = nodes.find(n => n.id === link.source);
            const target = nodes.find(n => n.id === link.target);
            if (!source || !target) return;

            ctx.beginPath();
            ctx.moveTo(source.x, source.y);
            ctx.lineTo(target.x, target.y);
            ctx.stroke();
        });

        // Draw Nodes
        nodes.forEach(node => {
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.val + 5, 0, Math.PI * 2);
            ctx.fillStyle = node.color;
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // Label (conditional)
            if (node.val > 7 || node.type === 'entity') {
                ctx.fillStyle = '#e5e7eb';
                ctx.font = '10px sans-serif';
                ctx.fillText(node.label, node.x + 12, node.y + 4);
            }
        });
    };

    // Interaction Handlers
    const handleMouseDown = (e) => {
        const rect = canvasRef.current.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Find clicked node
        const node = simulationRef.current.nodes.find(n => {
            const dx = n.x - x;
            const dy = n.y - y;
            return dx * dx + dy * dy < 400; // 20px radius hit testing
        });

        if (node) {
            simulationRef.current.draggingNode = node;
            if (onNodeClick) onNodeClick(node);
        }
    };

    const handleMouseMove = (e) => {
        if (simulationRef.current.draggingNode) {
            const rect = canvasRef.current.getBoundingClientRect();
            simulationRef.current.draggingNode.x = e.clientX - rect.left;
            simulationRef.current.draggingNode.y = e.clientY - rect.top;

            // Reset velocity so it stops quickly on release
            simulationRef.current.draggingNode.vx = 0;
            simulationRef.current.draggingNode.vy = 0;
        }

        // Tooltip logic could go here
    };

    const handleMouseUp = () => {
        simulationRef.current.draggingNode = null;
    };

    return (
        <div className="relative w-full h-[600px] bg-slate-950 rounded-xl border border-slate-800 overflow-hidden shadow-inner cursor-move">
            <canvas
                ref={canvasRef}
                width={1200}
                height={600}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                className="w-full h-full"
            />

            <div className="absolute bottom-4 right-4 bg-black/50 p-2 rounded text-xs text-gray-400">
                ● Conversation | ● Phone | ● UPI | ● Bank
            </div>
        </div>
    );
};

export default ForceGraph;
