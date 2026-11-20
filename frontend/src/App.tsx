import React, { useState, useEffect, useRef } from 'react';
import { 
  ShieldCheck, 
  Activity, 
  SlidersHorizontal, 
  FileCheck, 
  Cpu, 
  ExternalLink,
  Layers,
  Terminal,
  Presentation,
  Columns
} from 'lucide-react';

import { JuryControlBar } from './components/JuryControlBar';
import { BoilerPIDSchematic } from './components/BoilerPIDSchematic';
import { PlantScadaView } from './components/PlantScadaView';
import { GovtInspectorView } from './components/GovtInspectorView';
import { LoopCurrentMonitor } from './components/LoopCurrentMonitor';
import { HardwareCADView } from './components/HardwareCADView';
import { PitchDeckView } from './components/PitchDeckView';

export default function App() {
  const [activeTab, setActiveTab] = useState<'split' | 'scada' | 'inspector' | 'cad' | 'deck'>(() => {
    if (typeof window !== 'undefined') {
      if (window.location.pathname.includes('deck') || window.location.hash.includes('deck')) {
        return 'deck';
      }
      if (window.location.pathname.includes('hardware-cad') || window.location.hash.includes('hardware-cad')) {
        return 'cad';
      }
    }
    return 'split';
  });
  const [activeScenario, setActiveScenario] = useState<number>(1);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [snapshot, setSnapshot] = useState<any>({
    telemetry: {},
    raw_physics: {},
    cryptography: {},
    diagnostics: {},
    ledger_status: {},
  });
  const [ledgerBlocks, setLedgerBlocks] = useState<any[]>([]);

  const wsRef = useRef<WebSocket | null>(null);

  // Initialize WebSocket connection & fetch ledger blocks
  useEffect(() => {
    let reconnectTimeout: any = null;

    const connectWebSocket = () => {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      // In dev mode with Vite proxy, connect to current host ws endpoint
      const wsUrl = `${protocol}//${host}/ws/telemetry`;

      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setSnapshot(data);
        } catch (e) {
          console.error('Failed to parse telemetry message', e);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        reconnectTimeout = setTimeout(connectWebSocket, 2000);
      };

      ws.onerror = () => {
        ws.close();
      };
    };

    connectWebSocket();

    // Fallback polling for initial state and periodic ledger refresh
    const fetchStatusAndLedger = async () => {
      try {
        const resStatus = await fetch('/api/status');
        if (resStatus.ok) {
          const data = await resStatus.json();
          if (data && data.telemetry) {
            setSnapshot(data);
          }
        }
        const resLedger = await fetch('/api/ledger?count=30');
        if (resLedger.ok) {
          const ledgerData = await resLedger.json();
          if (ledgerData && ledgerData.records) {
            setLedgerBlocks(ledgerData.records);
          }
        }
      } catch (e) {
        // API server might be starting up
      }
    };

    fetchStatusAndLedger();
    const interval = setInterval(fetchStatusAndLedger, 2500);

    return () => {
      if (wsRef.current) wsRef.current.close();
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
      clearInterval(interval);
    };
  }, []);

  // Update ledger blocks when snapshot seq changes
  useEffect(() => {
    const fetchLedger = async () => {
      try {
        const res = await fetch('/api/ledger?count=30');
        if (res.ok) {
          const data = await res.json();
          setLedgerBlocks(data.records || []);
        }
      } catch (e) {}
    };
    if (snapshot?.telemetry?.seq_no) {
      fetchLedger();
    }
  }, [snapshot?.telemetry?.seq_no]);

  // Scenario Trigger
  const handleSelectScenario = async (scenarioId: number) => {
    setActiveScenario(scenarioId);
    try {
      const res = await fetch(`/api/scenario/${scenarioId}`, { method: 'POST' });
      if (res.ok) {
        // Refresh status immediately
        const statusRes = await fetch('/api/status');
        if (statusRes.ok) {
          setSnapshot(await statusRes.json());
        }
        const ledgerRes = await fetch('/api/ledger?count=30');
        if (ledgerRes.ok) {
          const lData = await ledgerRes.json();
          setLedgerBlocks(lData.records || []);
        }
      }
    } catch (e) {
      console.error('Failed to trigger scenario', e);
    }
  };

  // Reset System
  const handleReset = async () => {
    setActiveScenario(1);
    try {
      await fetch('/api/reset', { method: 'POST' });
      const statusRes = await fetch('/api/status');
      if (statusRes.ok) setSnapshot(await statusRes.json());
      const ledgerRes = await fetch('/api/ledger?count=30');
      if (ledgerRes.ok) setLedgerBlocks((await ledgerRes.json()).records || []);
    } catch (e) {
      console.error('Failed to reset system', e);
    }
  };

  // Run Forensic Audit
  const handleRunAudit = async () => {
    const res = await fetch('/api/ledger/audit');
    return await res.json();
  };

  // Simulate DB Tamper
  const handleSimulateDbTamper = async () => {
    const res = await fetch('/api/simulate/db-tamper', { method: 'POST' });
    const data = await res.json();
    const ledgerRes = await fetch('/api/ledger?count=30');
    if (ledgerRes.ok) setLedgerBlocks((await ledgerRes.json()).records || []);
    return data;
  };

  const seqNo = snapshot?.telemetry?.seq_no ?? 0;

  return (
    <div className="min-h-screen bg-[#090D16] text-gray-100 flex flex-col font-sans">
      {/* 1. Persistent NSA 6.0 Jury Control Bar */}
      <JuryControlBar
        activeScenario={activeScenario}
        onSelectScenario={handleSelectScenario}
        onReset={handleReset}
        isConnected={isConnected}
        seqNo={seqNo}
      />

      {/* 2. Primary Navigation Header */}
      <header className="bg-[#0F172A] border-b border-gray-800/80 px-6 py-3.5">
        <div className="max-w-[1920px] mx-auto flex flex-wrap items-center justify-between gap-4">
          {/* Logo & Platform Info */}
          <div className="flex items-center gap-3.5">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-emerald-600 via-teal-600 to-cyan-600 flex items-center justify-center shadow-lg shadow-emerald-950/50">
              <ShieldCheck className="w-7 h-7 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-extrabold tracking-tight text-white">
                  TapasShield <span className="text-xs px-2 py-0.5 rounded bg-emerald-950 border border-emerald-600/70 text-emerald-400 font-mono font-bold">NSA 6.0</span>
                </h1>
                <span className="text-xs font-mono text-gray-400 hidden md:inline">
                  | Shared Online Register Portal (Business + State + Central Govt)
                </span>
              </div>
              <p className="text-xs text-gray-400 font-mono">
                Govt. of India (DPIIT / Central Boilers Board) • IBR 1950 Compliance • SIL-2 Hardware Root-of-Trust
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-mono px-3 py-1 rounded bg-gray-900 border border-gray-800 text-gray-300">
              Node: <strong className="text-emerald-400">{snapshot?.telemetry?.boiler_id ?? 'IBR-TN-VEL-2026-0891'}</strong>
            </span>
          </div>
        </div>
      </header>

      {/* Stakeholder Role Switcher Bar */}
      <div className="bg-[#0B101D] border-b border-gray-800 px-6 py-2.5 shadow-inner">
        <div className="max-w-[1920px] mx-auto flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-mono font-extrabold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <Layers className="w-4 h-4 text-emerald-400" />
              INDIA EODB SHARED ONLINE REGISTER — STAKEHOLDER ROLE SWITCHER:
            </span>
          </div>

          <div className="flex flex-wrap items-center bg-[#151D30] p-1 rounded-xl border border-gray-700/80 gap-1">
            <button
              onClick={() => setActiveTab('split')}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === 'split'
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-black shadow-md shadow-emerald-900/40'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
              }`}
            >
              <Columns className="w-4 h-4" />
              <span>Dual Split-Screen (HERO VIEW)</span>
            </button>

            <button
              onClick={() => setActiveTab('scada')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'scada'
                  ? 'bg-emerald-600 text-black shadow-md shadow-emerald-900/40'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
              }`}
            >
              <Activity className="w-3.5 h-3.5" />
              <span>1. Business Portal (MSME Operator)</span>
            </button>

            <button
              onClick={() => setActiveTab('inspector')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'inspector'
                  ? 'bg-cyan-600 text-black shadow-md shadow-cyan-900/40'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
              }`}
            >
              <FileCheck className="w-3.5 h-3.5" />
              <span>2. State &amp; Central Govt Inspector Portal</span>
            </button>

            <button
              onClick={() => setActiveTab('cad')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'cad'
                  ? 'bg-emerald-600 text-black shadow-md shadow-emerald-900/40'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              <span>3. SIL-2 Hardware CAD</span>
            </button>

            <button
              onClick={() => setActiveTab('deck')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'deck'
                  ? 'bg-amber-500 text-black shadow-md shadow-amber-900/40 font-bold'
                  : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
              }`}
            >
              <Presentation className="w-3.5 h-3.5" />
              <span>4. NSA 6.0 Pitch Deck</span>
            </button>
          </div>
        </div>
      </div>

      {/* 3. Main Workspace Cockpit */}
      <main className="flex-1 max-w-[1920px] w-full mx-auto p-4 sm:p-6 space-y-6">
        {/* Animated SVG P&ID Digital Twin (Shared Across Operator & Inspector Views) */}
        {activeTab !== 'deck' && (
          <BoilerPIDSchematic
            telemetry={snapshot.telemetry}
            rawPhysics={snapshot.raw_physics}
            diagnostics={snapshot.diagnostics}
          />
        )}

        {/* Tab 0: Dual Split-Screen Live Sync (HERO VIEW) */}
        {activeTab === 'split' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
              {/* Left Column: Business SCADA & Predictive Maintenance */}
              <div className="space-y-6 bg-[#0c1222]/90 p-5 rounded-2xl border border-emerald-500/40 shadow-2xl">
                <div className="flex flex-wrap items-center justify-between pb-3 border-b border-gray-800 gap-2">
                  <div className="flex items-center gap-2.5">
                    <div className="p-2 rounded-lg bg-emerald-500/20 text-emerald-400">
                      <Activity className="w-5 h-5" />
                    </div>
                    <div>
                      <span className="text-[10px] font-mono text-emerald-400 uppercase font-bold tracking-wider">
                        Stakeholder 1: Private MSME Plant Operator
                      </span>
                      <h3 className="text-base font-bold text-white">
                        Plant SCADA, Predictive Maintenance &amp; ROI Cockpit
                      </h3>
                    </div>
                  </div>
                  <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-950 border border-emerald-700 text-emerald-300">
                    Real-Time Telemetry Feed
                  </span>
                </div>

                <PlantScadaView
                  telemetry={snapshot.telemetry}
                  diagnostics={snapshot.diagnostics}
                  rawPhysics={snapshot.raw_physics}
                />

                <LoopCurrentMonitor
                  telemetry={snapshot.telemetry}
                  rawPhysics={snapshot.raw_physics}
                />
              </div>

              {/* Right Column: State & Central Govt Inspector Online Register */}
              <div className="space-y-6 bg-[#0c1222]/90 p-5 rounded-2xl border border-cyan-500/40 shadow-2xl">
                <div className="flex flex-wrap items-center justify-between pb-3 border-b border-gray-800 gap-2">
                  <div className="flex items-center gap-2.5">
                    <div className="p-2 rounded-lg bg-cyan-500/20 text-cyan-400">
                      <FileCheck className="w-5 h-5" />
                    </div>
                    <div>
                      <span className="text-[10px] font-mono text-cyan-400 uppercase font-bold tracking-wider">
                        Stakeholders 2 &amp; 3: State Inspectorate &amp; Central Govt (DPIIT)
                      </span>
                      <h3 className="text-base font-bold text-white">
                        Statutory Online Register &amp; EODB Auto-Certification
                      </h3>
                    </div>
                  </div>
                  <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-cyan-950 border border-cyan-700 text-cyan-300">
                    Continuous Zero-Trust Audit
                  </span>
                </div>

                <GovtInspectorView
                  telemetry={snapshot.telemetry}
                  cryptoState={snapshot.cryptography}
                  ledgerStatus={snapshot.ledger_status}
                  onRunAudit={handleRunAudit}
                  onSimulateDbTamper={handleSimulateDbTamper}
                  ledgerBlocks={ledgerBlocks}
                />
              </div>
            </div>
          </div>
        )}

        {/* Tab 1: MSME Plant SCADA & Predictive View */}
        {activeTab === 'scada' && (
          <div className="space-y-6">
            <PlantScadaView
              telemetry={snapshot.telemetry}
              diagnostics={snapshot.diagnostics}
              rawPhysics={snapshot.raw_physics}
            />

            {/* Live 4-20mA & ADS1115 Loop Inspector */}
            <LoopCurrentMonitor
              telemetry={snapshot.telemetry}
              rawPhysics={snapshot.raw_physics}
            />
          </div>
        )}

        {/* Tab 2: Government Statutory Inspector Portal */}
        {activeTab === 'inspector' && (
          <div className="space-y-6">
            <GovtInspectorView
              telemetry={snapshot.telemetry}
              cryptoState={snapshot.cryptography}
              ledgerStatus={snapshot.ledger_status}
              onRunAudit={handleRunAudit}
              onSimulateDbTamper={handleSimulateDbTamper}
              ledgerBlocks={ledgerBlocks}
            />

            {/* Loop Electrical Integrity Check for Inspectors */}
            <LoopCurrentMonitor
              telemetry={snapshot.telemetry}
              rawPhysics={snapshot.raw_physics}
            />
          </div>
        )}

        {/* Tab 3: Hardware CAD, KiCad 8 PCB & Schematic Blueprint */}
        {activeTab === 'cad' && (
          <div className="space-y-6">
            <HardwareCADView telemetry={snapshot.telemetry} />
          </div>
        )}

        {/* Tab 4: NSA 6.0 Official 10-Slide Pitch Deck */}
        {activeTab === 'deck' && (
          <div className="space-y-6">
            <PitchDeckView />
          </div>
        )}
      </main>

      {/* 4. Industrial SCADA Footer */}
      <footer className="bg-[#090D16] border-t border-gray-800/80 px-6 py-4 mt-auto text-xs font-mono text-gray-500">
        <div className="max-w-[1920px] mx-auto flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span>SECURE SIL-2 DAEMON ACTIVE</span>
            <span>•</span>
            <span>CURVE: NIST P-256 (secp256r1)</span>
            <span>•</span>
            <span>AFE: ADS1115 (16-Bit @ 150.0 Ω Shunt)</span>
          </div>

          <div className="text-gray-400">
            TapasShield NSA 6.0 Platform © 2026 Central Boilers Board & DPIIT, Govt. of India.
          </div>
        </div>
      </footer>
    </div>
  );
}

