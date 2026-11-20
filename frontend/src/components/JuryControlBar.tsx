import React from 'react';
import { 
  ShieldCheck, 
  Flame, 
  AlertTriangle, 
  Scissors, 
  Bug, 
  RotateCcw, 
  Activity, 
  Wifi, 
  WifiOff 
} from 'lucide-react';

interface JuryControlBarProps {
  activeScenario: number;
  onSelectScenario: (scenarioId: number) => void;
  onReset: () => void;
  isConnected: boolean;
  seqNo: number;
}

export const JuryControlBar: React.FC<JuryControlBarProps> = ({
  activeScenario,
  onSelectScenario,
  onReset,
  isConnected,
  seqNo,
}) => {
  const scenarios = [
    {
      id: 1,
      title: '1. Normal (12 bar)',
      desc: 'Baseline steady-state, clean tubes, valid signatures',
      icon: ShieldCheck,
      color: 'emerald',
      activeClass: 'bg-emerald-950/80 border-emerald-500 text-emerald-300 shadow-[0_0_15px_rgba(16,185,129,0.3)]',
      btnClass: 'hover:border-emerald-600/60 hover:bg-emerald-950/30 text-gray-300',
    },
    {
      id: 2,
      title: '2. Scale Buildup (100x)',
      desc: 'Ramp scale 0.1->1.8mm, stack temp climb, ₹/hr waste',
      icon: Flame,
      color: 'amber',
      activeClass: 'bg-amber-950/80 border-amber-500 text-amber-300 shadow-[0_0_15px_rgba(245,158,11,0.3)]',
      btnClass: 'hover:border-amber-600/60 hover:bg-amber-950/30 text-gray-300',
    },
    {
      id: 3,
      title: '3. MAWP Overpressure',
      desc: '16.8 bar spike & 18% low water emergency alarm',
      icon: AlertTriangle,
      color: 'crimson',
      activeClass: 'bg-red-950/80 border-red-500 text-red-300 shadow-[0_0_15px_rgba(239,68,68,0.3)]',
      btnClass: 'hover:border-red-600/60 hover:bg-red-950/30 text-gray-300',
    },
    {
      id: 4,
      title: '4. Sensor Wire Cut',
      desc: '0.00 mA loop break -> CRITICAL_LOOP_OPEN_CIRCUIT',
      icon: Scissors,
      color: 'orange',
      activeClass: 'bg-orange-950/80 border-orange-500 text-orange-300 shadow-[0_0_15px_rgba(249,115,22,0.3)]',
      btnClass: 'hover:border-orange-600/60 hover:bg-orange-950/30 text-gray-300',
    },
    {
      id: 5,
      title: '5. Spoof & DB Tamper',
      desc: 'Synthetic 10 bar clamp vs 212°C & broken ledger hash',
      icon: Bug,
      color: 'purple',
      activeClass: 'bg-purple-950/80 border-purple-500 text-purple-300 shadow-[0_0_15px_rgba(168,85,247,0.3)]',
      btnClass: 'hover:border-purple-600/60 hover:bg-purple-950/30 text-gray-300',
    },
  ];

  return (
    <div className="bg-[#0D1322] border-b border-gray-800 sticky top-0 z-50 backdrop-blur-md px-4 py-2.5 shadow-xl">
      <div className="max-w-[1920px] mx-auto flex flex-wrap items-center justify-between gap-3">
        {/* Left: Branding & Status */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-gray-900 border border-gray-800 rounded-lg px-3 py-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
            <span className="font-bold text-xs uppercase tracking-wider text-emerald-400">NSA 6.0 JURY CONTROL</span>
          </div>

          <div className="flex items-center gap-2 text-xs font-mono text-gray-400">
            {isConnected ? (
              <span className="flex items-center gap-1.5 text-emerald-400 bg-emerald-950/50 border border-emerald-800/50 rounded px-2 py-0.5">
                <Wifi className="w-3.5 h-3.5" /> LIVE WS (1 Hz)
              </span>
            ) : (
              <span className="flex items-center gap-1.5 text-amber-400 bg-amber-950/50 border border-amber-800/50 rounded px-2 py-0.5">
                <WifiOff className="w-3.5 h-3.5" /> RECONNECTING...
              </span>
            )}
            <span className="text-gray-500 hidden sm:inline">|</span>
            <span className="hidden sm:inline text-gray-400">
              SEQ <span className="text-gray-200 font-semibold">#{seqNo}</span>
            </span>
          </div>
        </div>

        {/* Center: 5 Interactive Scenario Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          {scenarios.map((s) => {
            const Icon = s.icon;
            const isActive = activeScenario === s.id;
            return (
              <button
                key={s.id}
                onClick={() => onSelectScenario(s.id)}
                title={s.desc}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium transition-all duration-200 ${
                  isActive ? s.activeClass : `bg-[#131B2E] border-gray-700/80 ${s.btnClass}`
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-inherit animate-pulse' : 'text-gray-400'}`} />
                <span>{s.title}</span>
              </button>
            );
          })}
        </div>

        {/* Right: Quick Reset Button */}
        <div className="flex items-center gap-2">
          <button
            onClick={onReset}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-gray-700 bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white text-xs font-medium transition-colors"
            title="Reset simulation, edge node, and ledger to pristine 12.0 bar state"
          >
            <RotateCcw className="w-3.5 h-3.5 text-gray-400 group-hover:rotate-180 transition-transform" />
            <span>Reset System</span>
          </button>
        </div>
      </div>
    </div>
  );
};

