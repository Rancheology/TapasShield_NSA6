import React from 'react';
import { Flame, AlertTriangle, ShieldCheck, Zap } from 'lucide-react';

interface BoilerPIDSchematicProps {
  telemetry: any;
  rawPhysics: any;
  diagnostics: any;
}

export const BoilerPIDSchematic: React.FC<BoilerPIDSchematicProps> = ({
  telemetry,
  rawPhysics,
  diagnostics,
}) => {
  const pressure = telemetry?.pressure_bar ?? 12.0;
  const steamTemp = telemetry?.steam_temp_c ?? 188.0;
  const stackTemp = telemetry?.stack_temp_c ?? 220.0;
  const flow = telemetry?.mass_flow_kgh ?? 3500.0;
  const waterLevel = telemetry?.drum_water_level_pct ?? 65.0;
  const tds = telemetry?.tds_ppm ?? 2100.0;
  const ph = telemetry?.ph_level ?? 9.8;
  const scaleMm = telemetry?.scale_thickness_mm ?? 0.0;
  const tamperStatus = telemetry?.tamper_status ?? 'SECURE_VERIFIED';
  const safetyViolation = telemetry?.safety_violation ?? 'NORMAL';

  const loopCurrents = telemetry?.loop_currents_ma ?? {};
  const adcCounts = rawPhysics?.adc_counts ?? {};

  // Visual cues
  const isOverpressure = pressure > 15.0;
  const isLowWater = waterLevel < 25.0;
  const isWireCut = tamperStatus === 'CRITICAL_LOOP_OPEN_CIRCUIT';
  const isSpoofed = tamperStatus === 'SYNTHETIC_RESISTOR_SPOOF_DETECTED';

  // Flame color calculation based on stack temp / efficiency
  // Clean: intense blue flame (#3B82F6). Scaled/High flue loss: orange-red (#F97316 / #EF4444)
  const flameHue = Math.max(15, Math.min(220, 210 - (scaleMm * 95)));
  const flameColor = `hsl(${flameHue}, 90%, 55%)`;

  // Scale stroke thickness visual (0mm = 0px, 2.0mm = 12px)
  const scaleStrokeWidth = Math.min(14, scaleMm * 7);

  // Water level Y position in drum (drum height = 140px, top=120, bottom=260)
  // 100% water -> y=130, 0% water -> y=250
  const waterY = 250 - (waterLevel / 100.0) * 115;

  return (
    <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-2xl relative overflow-hidden">
      {/* Header bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4 border-b border-gray-800/80 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-blue-950/60 border border-blue-800/60 rounded-lg text-blue-400">
            <Zap className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-gray-100 uppercase tracking-wide">
              P&ID Digital Twin: Industrial Fire-Tube Boiler (MAWP 15.0 bar)
            </h2>
            <p className="text-xs font-mono text-gray-400">
              TAG: B-101 | 3500 kg/hr Saturated Steam | Twin Clock: Tick #{rawPhysics?.tick ?? 0}
            </p>
          </div>
        </div>

        {/* Global Security / Compliance Tag */}
        <div className="flex items-center gap-2">
          {isOverpressure || isLowWater ? (
            <span className="flex items-center gap-1.5 px-3 py-1 bg-red-950 border border-red-500 rounded-lg text-xs font-mono font-bold text-red-400 animate-pulse">
              <AlertTriangle className="w-3.5 h-3.5" /> IBR EMERGENCY ALARM
            </span>
          ) : isWireCut ? (
            <span className="flex items-center gap-1.5 px-3 py-1 bg-orange-950 border border-orange-500 rounded-lg text-xs font-mono font-bold text-orange-400 animate-pulse">
              <AlertTriangle className="w-3.5 h-3.5" /> 4-20mA LOOP SEVERED
            </span>
          ) : isSpoofed ? (
            <span className="flex items-center gap-1.5 px-3 py-1 bg-purple-950 border border-purple-500 rounded-lg text-xs font-mono font-bold text-purple-400 animate-pulse">
              <AlertTriangle className="w-3.5 h-3.5" /> THERMODYNAMIC SPOOF DETECTED
            </span>
          ) : (
            <span className="flex items-center gap-1.5 px-3 py-1 bg-emerald-950/70 border border-emerald-600 rounded-lg text-xs font-mono font-semibold text-emerald-400">
              <ShieldCheck className="w-3.5 h-3.5" /> STATUTORY COMPLIANT (SIL-2)
            </span>
          )}
        </div>
      </div>

      {/* SVG Canvas */}
      <div className="w-full aspect-[16/9] max-h-[520px] bg-[#090D16] border border-gray-800/70 rounded-xl relative flex items-center justify-center p-2">
        <svg
          viewBox="0 0 1000 560"
          className="w-full h-full select-none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            {/* Gradients */}
            <linearGradient id="drumGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#1E293B" />
              <stop offset="50%" stopColor="#0F172A" />
              <stop offset="100%" stopColor="#1E293B" />
            </linearGradient>

            <linearGradient id="waterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#0284C7" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#0369A1" stopOpacity="0.95" />
            </linearGradient>

            <linearGradient id="steamGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#E2E8F0" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#94A3B8" stopOpacity="0.05" />
            </linearGradient>

            <linearGradient id="stackGrad" x1="0%" y1="100%" x2="0%" y2="0%">
              <stop offset="0%" stopColor="#475569" />
              <stop offset="100%" stopColor="#334155" />
            </linearGradient>

            <filter id="glowFilter" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="5" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            <filter id="scaleGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* BACKGROUND GRID */}
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1E293B" strokeWidth="0.5" strokeOpacity="0.4" />
          </pattern>
          <rect width="1000" height="560" fill="url(#grid)" />

          {/* ================= PIPING INFRASTRUCTURE ================= */}

          {/* Steam Header Pipe (Top Exit) */}
          <path d="M 500 130 L 500 60 L 880 60" fill="none" stroke="#64748B" strokeWidth="14" strokeLinecap="round" />
          <path d="M 500 130 L 500 60 L 880 60" fill="none" stroke="#CBD5E1" strokeWidth="2" strokeDasharray="6 6" />

          {/* Feedwater Inlet Pipe (Left) */}
          <path d="M 80 220 L 220 220" fill="none" stroke="#0284C7" strokeWidth="10" strokeLinecap="round" />
          <path d="M 80 220 L 220 220" fill="none" stroke="#38BDF8" strokeWidth="2" strokeDasharray="5 5" />

          {/* Continuous Blowdown Pipe (Bottom Drain) */}
          <path d="M 500 370 L 500 480 L 760 480" fill="none" stroke="#D97706" strokeWidth="8" strokeLinecap="round" />

          {/* Chimney Flue Gas Stack (Right Exit) */}
          <path d="M 780 270 L 850 270 L 850 140" fill="none" stroke="#475569" strokeWidth="24" strokeLinecap="round" />

          {/* ================= BOILER SHELL & DRUM ================= */}
          {/* Main Cylindrical Shell */}
          <rect
            x="220"
            y="130"
            width="560"
            height="240"
            rx="45"
            fill="url(#drumGrad)"
            stroke="#475569"
            strokeWidth="5"
          />

          {/* Drum Water Space (Dynamic Level) */}
          <clipPath id="drumClip">
            <rect x="222" y="132" width="556" height="236" rx="43" />
          </clipPath>

          <g clipPath="url(#drumClip)">
            {/* Water Fill */}
            <rect
              x="220"
              y={waterY}
              width="560"
              height={370 - waterY}
              fill="url(#waterGrad)"
              className="transition-all duration-700 ease-out"
            />

            {/* Animated Water Surface Waves */}
            <path
              d={`M 220 ${waterY} Q 360 ${waterY - 5} 500 ${waterY} T 780 ${waterY} L 780 370 L 220 370 Z`}
              fill="#0369A1"
              opacity="0.4"
            />

            {/* Steam Bubbles Rising in Water */}
            <circle cx="340" cy={waterY + 35} r="3" fill="#E0F2FE" opacity="0.6" className="steam-bubble" />
            <circle cx="480" cy={waterY + 50} r="4" fill="#E0F2FE" opacity="0.7" className="steam-bubble" />
            <circle cx="620" cy={waterY + 25} r="3.5" fill="#E0F2FE" opacity="0.5" className="steam-bubble" />
            <circle cx="400" cy={waterY + 65} r="2.5" fill="#E0F2FE" opacity="0.6" className="steam-bubble" />

            {/* Steam Space at top */}
            <rect x="220" y="130" width="560" height={waterY - 130} fill="url(#steamGrad)" />
          </g>

          {/* Low Water Cut-off Threshold Line (25% = Y=222) */}
          <line x1="220" y1="222" x2="780" y2="222" stroke="#EF4444" strokeWidth="1.5" strokeDasharray="4 4" opacity="0.6" />
          <text x="230" y="217" fill="#EF4444" fontSize="10" fontFamily="monospace" opacity="0.8">
            LOW-WATER CUTOFF LEVEL (25%)
          </text>

          {/* ================= INTERNAL FIRE-TUBES & SCALE LAYER ================= */}
          {/* Main Furnace Flue (Bottom Center) */}
          <rect x="250" y="280" width="500" height="60" rx="12" fill="#1E293B" stroke="#334155" strokeWidth="3" />

          {/* Upper Return Fire-Tubes (Pass 2 & 3) */}
          <rect x="260" y="240" width="480" height="18" rx="5" fill="#1E293B" stroke="#334155" strokeWidth="2" />
          <rect x="260" y="195" width="480" height="18" rx="5" fill="#1E293B" stroke="#334155" strokeWidth="2" />

          {/* Dynamic Waterside CaCO3 Scale Coating on Tubes */}
          {scaleMm > 0.05 && (
            <g filter="url(#scaleGlow)">
              {/* Scale Layer on Main Flue */}
              <rect
                x="248"
                y="278"
                width="504"
                height="64"
                rx="14"
                fill="none"
                stroke="#F59E0B"
                strokeWidth={scaleStrokeWidth}
                strokeOpacity={Math.min(0.9, 0.3 + scaleMm * 0.4)}
                className="transition-all duration-500"
              />
              {/* Scale Layer on Upper Tubes */}
              <rect
                x="258"
                y="238"
                width="484"
                height="22"
                rx="7"
                fill="none"
                stroke="#F59E0B"
                strokeWidth={Math.max(1, scaleStrokeWidth * 0.7)}
                strokeOpacity={Math.min(0.85, 0.3 + scaleMm * 0.35)}
              />
              <rect
                x="258"
                y="193"
                width="484"
                height="22"
                rx="7"
                fill="none"
                stroke="#F59E0B"
                strokeWidth={Math.max(1, scaleStrokeWidth * 0.7)}
                strokeOpacity={Math.min(0.85, 0.3 + scaleMm * 0.35)}
              />
            </g>
          )}

          {/* ================= BURNER & FLAME ASSEMBLY ================= */}
          {/* Burner Housing (Left Flange) */}
          <path d="M 190 270 L 250 285 L 250 335 L 190 350 Z" fill="#334155" stroke="#475569" strokeWidth="3" />
          <circle cx="190" cy="310" r="14" fill="#0F172A" stroke="#64748B" strokeWidth="2" />

          {/* Animated Burner Flame inside Main Flue */}
          <g className="flame-anim" style={{ transformOrigin: '255px 310px' }}>
            {/* Outer Flame Cone */}
            <path
              d="M 250 288 Q 360 295 440 310 Q 360 325 250 332 Z"
              fill={flameColor}
              opacity="0.85"
              filter="url(#glowFilter)"
            />
            {/* Core Intense Flame */}
            <path
              d="M 250 295 Q 320 300 370 310 Q 320 320 250 325 Z"
              fill="#FFFFFF"
              opacity="0.9"
            />
          </g>

          {/* Flue Gas Path Arrows */}
          <path d="M 680 310 L 740 310 L 740 249 L 680 249" fill="none" stroke="#F59E0B" strokeWidth="2" strokeDasharray="4 3" opacity="0.6" />
          <path d="M 300 249 L 270 249 L 270 204 L 300 204" fill="none" stroke="#F59E0B" strokeWidth="2" strokeDasharray="4 3" opacity="0.6" />
          <path d="M 720 204 L 790 204 L 790 270 L 850 270" fill="none" stroke="#EF4444" strokeWidth="2" strokeDasharray="4 3" opacity="0.6" />

          {/* Chimney Exhaust Smoke Particles */}
          <g opacity="0.7">
            <circle cx="850" cy="110" r="16" fill="#475569" opacity="0.5" className="steam-bubble" />
            <circle cx="855" cy="80" r="22" fill="#475569" opacity="0.3" className="steam-bubble" />
          </g>

          {/* ================= SENSOR CALLOUT BADGES (P&ID) ================= */}

          {/* PT-101 (Drum Steam Pressure) */}
          <g transform="translate(430, 10)">
            <rect
              width="145"
              height="50"
              rx="6"
              fill="#0F172A"
              stroke={isOverpressure || isWireCut || isSpoofed ? '#EF4444' : '#10B981'}
              strokeWidth={isOverpressure ? '2.5' : '1.5'}
              className={isOverpressure ? 'animate-pulse' : ''}
            />
            <text x="8" y="16" fill="#94A3B8" fontSize="10" fontFamily="monospace" fontWeight="bold">PT-101 DRUM PRESS</text>
            <text x="8" y="34" fill="#F8FAFC" fontSize="15" fontFamily="monospace" fontWeight="bold">
              {isWireCut ? '0.00' : pressure.toFixed(2)} <tspan fontSize="10" fill="#94A3B8">bar</tspan>
            </text>
            <text x="8" y="45" fill={isWireCut ? '#EF4444' : '#10B981'} fontSize="9" fontFamily="monospace">
              {(loopCurrents['PT_101'] ?? 11.68).toFixed(2)} mA | {adcCounts['PT_101'] ?? 14015} cnt
            </text>
            {/* Lead line */}
            <line x1="72" y1="50" x2="72" y2="120" stroke="#64748B" strokeWidth="1.5" strokeDasharray="2 2" />
            <circle cx="72" cy="120" r="4" fill="#10B981" />
          </g>

          {/* TT-101 (Steam Header Temp) */}
          <g transform="translate(680, 10)">
            <rect width="140" height="50" rx="6" fill="#0F172A" stroke="#06B6D4" strokeWidth="1.5" />
            <text x="8" y="16" fill="#94A3B8" fontSize="10" fontFamily="monospace" fontWeight="bold">TT-101 STEAM TEMP</text>
            <text x="8" y="34" fill="#F8FAFC" fontSize="15" fontFamily="monospace" fontWeight="bold">
              {steamTemp.toFixed(1)} <tspan fontSize="10" fill="#94A3B8">°C</tspan>
            </text>
            <text x="8" y="45" fill="#06B6D4" fontSize="9" fontFamily="monospace">
              {(loopCurrents['TT_101'] ?? 12.59).toFixed(2)} mA | T_sat: {(rawPhysics?.t_sat_c ?? 187.96).toFixed(1)}°C
            </text>
            {/* Lead line */}
            <line x1="70" y1="50" x2="70" y2="60" stroke="#06B6D4" strokeWidth="1.5" />
            <circle cx="70" cy="60" r="4" fill="#06B6D4" />
          </g>

          {/* TT-102 (Flue Stack Temp) */}
          <g transform="translate(820, 160)">
            <rect
              width="145"
              height="50"
              rx="6"
              fill="#0F172A"
              stroke={scaleMm > 1.0 ? '#EF4444' : scaleMm > 0.4 ? '#F59E0B' : '#64748B'}
              strokeWidth="1.5"
            />
            <text x="8" y="16" fill="#94A3B8" fontSize="10" fontFamily="monospace" fontWeight="bold">TT-102 STACK TEMP</text>
            <text x="8" y="34" fill="#F8FAFC" fontSize="15" fontFamily="monospace" fontWeight="bold">
              {stackTemp.toFixed(1)} <tspan fontSize="10" fill="#94A3B8">°C</tspan>
            </text>
            <text x="8" y="45" fill={scaleMm > 0.4 ? '#F59E0B' : '#94A3B8'} fontSize="9" fontFamily="monospace">
              {(loopCurrents['TT_102'] ?? 11.04).toFixed(2)} mA | ΔT: +{(stackTemp - (rawPhysics?.t_sat_c ?? 187.96)).toFixed(1)}°C
            </text>
            {/* Lead line */}
            <line x1="0" y1="25" x2="-20" y2="25" stroke="#F59E0B" strokeWidth="1.5" />
            <circle cx="-20" cy="25" r="4" fill="#F59E0B" />
          </g>

          {/* FT-101 (Feedwater & Steam Flow) */}
          <g transform="translate(20, 160)">
            <rect width="140" height="50" rx="6" fill="#0F172A" stroke="#38BDF8" strokeWidth="1.5" />
            <text x="8" y="16" fill="#94A3B8" fontSize="10" fontFamily="monospace" fontWeight="bold">FT-101 STEAM FLOW</text>
            <text x="8" y="34" fill="#F8FAFC" fontSize="15" fontFamily="monospace" fontWeight="bold">
              {flow.toFixed(0)} <tspan fontSize="10" fill="#94A3B8">kg/hr</tspan>
            </text>
            <text x="8" y="45" fill="#38BDF8" fontSize="9" fontFamily="monospace">
              {(loopCurrents['FT_101'] ?? 15.20).toFixed(2)} mA | 100% Load
            </text>
            {/* Lead line */}
            <line x1="140" y1="25" x2="160" y2="25" stroke="#38BDF8" strokeWidth="1.5" />
            <circle cx="160" cy="25" r="4" fill="#38BDF8" />
          </g>

          {/* LT-101 (Drum Water Level) */}
          <g transform="translate(20, 390)">
            <rect
              width="140"
              height="50"
              rx="6"
              fill="#0F172A"
              stroke={isLowWater ? '#EF4444' : '#0284C7'}
              strokeWidth={isLowWater ? '2' : '1.5'}
              className={isLowWater ? 'animate-pulse' : ''}
            />
            <text x="8" y="16" fill="#94A3B8" fontSize="10" fontFamily="monospace" fontWeight="bold">LT-101 DRUM LEVEL</text>
            <text x="8" y="34" fill={isLowWater ? '#EF4444' : '#38BDF8'} fontSize="15" fontFamily="monospace" fontWeight="bold">
              {waterLevel.toFixed(1)} <tspan fontSize="10" fill="#94A3B8">%</tspan>
            </text>
            <text x="8" y="45" fill={isLowWater ? '#EF4444' : '#0284C7'} fontSize="9" fontFamily="monospace">
              {isLowWater ? 'CRITICAL LOW WATER' : 'NORMAL WATER LEVEL'}
            </text>
          </g>

          {/* AT-101 (Blowdown TDS / pH) */}
          <g transform="translate(680, 450)">
            <rect width="150" height="50" rx="6" fill="#0F172A" stroke="#D97706" strokeWidth="1.5" />
            <text x="8" y="16" fill="#94A3B8" fontSize="10" fontFamily="monospace" fontWeight="bold">AT-101 WATER QUALITY</text>
            <text x="8" y="34" fill="#F8FAFC" fontSize="15" fontFamily="monospace" fontWeight="bold">
              {tds.toFixed(0)} <tspan fontSize="10" fill="#94A3B8">ppm</tspan> | pH {ph.toFixed(1)}
            </text>
            <text x="8" y="45" fill="#D97706" fontSize="9" fontFamily="monospace">
              CoC: {((diagnostics?.chemistry?.cycles_of_concentration) ?? 6.0).toFixed(1)}x | Soft Feed
            </text>
          </g>

          {/* Scale Thickness Floating Annotation */}
          <g transform="translate(380, 400)">
            <rect
              width="240"
              height="36"
              rx="6"
              fill="#18181B"
              stroke={scaleMm > 1.0 ? '#EF4444' : scaleMm > 0.3 ? '#F59E0B' : '#27272A'}
              strokeWidth="1.5"
            />
            <text x="12" y="22" fill="#E4E4E7" fontSize="11" fontFamily="monospace">
              CaCO₃ SCALE: <tspan fontWeight="bold" fill={scaleMm > 1.0 ? '#EF4444' : scaleMm > 0.3 ? '#F59E0B' : '#10B981'}>{scaleMm.toFixed(2)} mm</tspan>
              <tspan fill="#71717A"> (ΔT: +{(stackTemp - (rawPhysics?.t_sat_c ?? 187.96)).toFixed(1)}°C)</tspan>
            </text>
          </g>
        </svg>
      </div>
    </div>
  );
};

