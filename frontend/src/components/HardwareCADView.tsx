import React, { useState } from 'react';
import { 
  Cpu, 
  Layers, 
  Download, 
  Box, 
  FileCode, 
  Search, 
  Maximize2, 
  RotateCw, 
  CheckCircle2, 
  Eye, 
  Zap, 
  ShieldCheck,
  ZoomIn,
  ZoomOut,
  RotateCcw
} from 'lucide-react';

interface HardwareCADViewProps {
  telemetry?: any;
}

export const HardwareCADView: React.FC<HardwareCADViewProps> = ({ telemetry }) => {
  const [activeMode, setActiveMode] = useState<'pcb' | 'schematic' | 'bom'>('pcb');
  const [pcbDisplayType, setPcbDisplayType] = useState<'kicad_3d_iso' | 'kicad_3d_top' | 'interactive'>('kicad_3d_iso');
  const [is3DView, setIs3DView] = useState<boolean>(true);
  const [showTopCopper, setShowTopCopper] = useState<boolean>(true);
  const [showBottomCopper, setShowBottomCopper] = useState<boolean>(true);
  const [showSilkscreen, setShowSilkscreen] = useState<boolean>(true);
  const [selectedComponent, setSelectedComponent] = useState<string | null>('U1');
  const [schematicZoom, setSchematicZoom] = useState<number>(1);
  const [activeZone, setActiveZone] = useState<string | null>(null);
  const [bomSearch, setBomSearch] = useState<string>('');

  // 42 Components matching KICAD_BOM_AND_NETLIST.md
  const bomComponents = [
    { ref: 'U1', qty: 1, val: 'ESP32-S3-WROOM-1', pkg: 'SMD Module 41-SMD', desc: 'Xtensa Dual-Core @ 240MHz, 16MB Flash, 8MB PSRAM', mfr: 'Espressif Systems', zone: 'Zone 5' },
    { ref: 'U2', qty: 1, val: 'ATECC608B-TNGISVA', pkg: 'SOIC-8 (150 mil)', desc: 'Hardware Root-of-Trust, Slot 0 ECDSA P-256 Signer', mfr: 'Microchip Tech', zone: 'Zone 4' },
    { ref: 'U3', qty: 1, val: 'ADS1115IDGSR', pkg: 'MSOP-10 (3x3mm)', desc: '16-Bit 860SPS 4-Channel Delta-Sigma ADC (PGA ±4.096V)', mfr: 'Texas Instruments', zone: 'Zone 3' },
    { ref: 'U4', qty: 1, val: 'TPS54302DDCR', pkg: 'SOT-23-6', desc: '28V 3A Synchronous Step-Down DC-DC Converter (24V -> 5V)', mfr: 'Texas Instruments', zone: 'Zone 1' },
    { ref: 'U5', qty: 1, val: 'AP2112K-3.3TRG1', pkg: 'SOT-23-5', desc: 'Ultra-low noise 3.3V 600mA LDO Linear Regulator', mfr: 'Diodes Inc.', zone: 'Zone 1' },
    { ref: 'J1', qty: 1, val: '24V_PWR', pkg: 'TerminalBlock 5.08mm', desc: '24V DC Auxiliary Industrial Power Input Block', mfr: 'Phoenix Contact', zone: 'Zone 1' },
    { ref: 'J2', qty: 1, val: 'PT-101', pkg: 'TerminalBlock 5.08mm', desc: 'Channel 1: Drum Steam Pressure Loop (0-25 bar)', mfr: 'Phoenix Contact', zone: 'Zone 2' },
    { ref: 'J3', qty: 1, val: 'TT-101', pkg: 'TerminalBlock 5.08mm', desc: 'Channel 2: Steam Header Temp Loop (0-350 °C)', mfr: 'Phoenix Contact', zone: 'Zone 2' },
    { ref: 'J4', qty: 1, val: 'TT-102', pkg: 'TerminalBlock 5.08mm', desc: 'Channel 3: Flue Stack Temp Loop (0-500 °C)', mfr: 'Phoenix Contact', zone: 'Zone 2' },
    { ref: 'J5', qty: 1, val: 'FT-101', pkg: 'TerminalBlock 5.08mm', desc: 'Channel 4: Feedwater & Steam Mass Flow (0-5000 kg/hr)', mfr: 'Phoenix Contact', zone: 'Zone 2' },
    { ref: 'J6', qty: 1, val: 'AT-101', pkg: 'TerminalBlock 5.08mm', desc: 'Channel 5: Blowdown TDS & Water Quality Loop', mfr: 'Phoenix Contact', zone: 'Zone 2' },
    { ref: 'D1', qty: 1, val: 'SMAJ28CA', pkg: 'DO-214AC (SMA)', desc: '28V Bi-Directional TVS Surge Diode (PT-101 Loop)', mfr: 'Littelfuse', zone: 'Zone 2' },
    { ref: 'D2', qty: 1, val: 'SMAJ28CA', pkg: 'DO-214AC (SMA)', desc: '28V Bi-Directional TVS Surge Diode (TT-101 Loop)', mfr: 'Littelfuse', zone: 'Zone 2' },
    { ref: 'D3', qty: 1, val: 'SMAJ28CA', pkg: 'DO-214AC (SMA)', desc: '28V Bi-Directional TVS Surge Diode (TT-102 Loop)', mfr: 'Littelfuse', zone: 'Zone 2' },
    { ref: 'D4', qty: 1, val: 'SMAJ28CA', pkg: 'DO-214AC (SMA)', desc: '28V Bi-Directional TVS Surge Diode (FT-101 Loop)', mfr: 'Littelfuse', zone: 'Zone 2' },
    { ref: 'D5', qty: 1, val: 'SMAJ28CA', pkg: 'DO-214AC (SMA)', desc: '28V Bi-Directional TVS Surge Diode (AT-101 Loop)', mfr: 'Littelfuse', zone: 'Zone 2' },
    { ref: 'D6', qty: 1, val: 'B540C-13-F', pkg: 'SMC (DO-214AB)', desc: '40V 5A Schottky Barrier Rectifier (Reverse Input Protection)', mfr: 'Diodes Inc.', zone: 'Zone 1' },
    { ref: 'D7', qty: 1, val: 'B540C-13-F', pkg: 'SMC (DO-214AB)', desc: '40V 5A Schottky Catch Diode for TPS54302 Buck', mfr: 'Diodes Inc.', zone: 'Zone 1' },
    { ref: 'R1', qty: 1, val: '150.0 Ω ±0.05%', pkg: '0805 SMD', desc: 'Precision Current Shunt (PT-101, 25 ppm/°C Susumu RR)', mfr: 'Susumu', zone: 'Zone 2' },
    { ref: 'R2', qty: 1, val: '150.0 Ω ±0.05%', pkg: '0805 SMD', desc: 'Precision Current Shunt (TT-101, 25 ppm/°C Susumu RR)', mfr: 'Susumu', zone: 'Zone 2' },
    { ref: 'R3', qty: 1, val: '150.0 Ω ±0.05%', pkg: '0805 SMD', desc: 'Precision Current Shunt (TT-102, 25 ppm/°C Susumu RR)', mfr: 'Susumu', zone: 'Zone 2' },
    { ref: 'R4', qty: 1, val: '150.0 Ω ±0.05%', pkg: '0805 SMD', desc: 'Precision Current Shunt (FT-101, 25 ppm/°C Susumu RR)', mfr: 'Susumu', zone: 'Zone 2' },
    { ref: 'R5', qty: 1, val: '150.0 Ω ±0.05%', pkg: '0805 SMD', desc: 'Precision Current Shunt (AT-101, 25 ppm/°C Susumu RR)', mfr: 'Susumu', zone: 'Zone 2' },
    { ref: 'R6', qty: 1, val: '100 Ω ±1%', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Resistor (PT-101)', mfr: 'Yageo', zone: 'Zone 2' },
    { ref: 'R7', qty: 1, val: '100 Ω ±1%', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Resistor (TT-101)', mfr: 'Yageo', zone: 'Zone 2' },
    { ref: 'R8', qty: 1, val: '100 Ω ±1%', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Resistor (TT-102)', mfr: 'Yageo', zone: 'Zone 2' },
    { ref: 'R9', qty: 1, val: '100 Ω ±1%', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Resistor (FT-101)', mfr: 'Yageo', zone: 'Zone 2' },
    { ref: 'R10', qty: 1, val: '100 Ω ±1%', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Resistor (AT-101)', mfr: 'Yageo', zone: 'Zone 2' },
    { ref: 'C1', qty: 1, val: '100 nF 50V X7R', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Capacitor (PT-101)', mfr: 'Murata', zone: 'Zone 2' },
    { ref: 'C2', qty: 1, val: '100 nF 50V X7R', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Capacitor (TT-101)', mfr: 'Murata', zone: 'Zone 2' },
    { ref: 'C3', qty: 1, val: '100 nF 50V X7R', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Capacitor (TT-102)', mfr: 'Murata', zone: 'Zone 2' },
    { ref: 'C4', qty: 1, val: '100 nF 50V X7R', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Capacitor (FT-101)', mfr: 'Murata', zone: 'Zone 2' },
    { ref: 'C5', qty: 1, val: '100 nF 50V X7R', pkg: '0603 SMD', desc: 'AFE Anti-Aliasing Low-Pass Filter Capacitor (AT-101)', mfr: 'Murata', zone: 'Zone 2' },
    { ref: 'R11', qty: 1, val: '4.7 kΩ ±1%', pkg: '0603 SMD', desc: 'I2C Serial Data Bus Pull-Up (SDA, GPIO8)', mfr: 'Panasonic', zone: 'Zone 3/4' },
    { ref: 'R12', qty: 1, val: '4.7 kΩ ±1%', pkg: '0603 SMD', desc: 'I2C Serial Clock Bus Pull-Up (SCL, GPIO9)', mfr: 'Panasonic', zone: 'Zone 3/4' },
    { ref: 'R13', qty: 1, val: '220 Ω ±1%', pkg: '0603 SMD', desc: 'LED Current Limiting Resistor for Emerald Verified LED', mfr: 'Panasonic', zone: 'Zone 6' },
    { ref: 'R14', qty: 1, val: '220 Ω ±1%', pkg: '0603 SMD', desc: 'LED Current Limiting Resistor for Crimson Tamper LED', mfr: 'Panasonic', zone: 'Zone 6' },
    { ref: 'LED1', qty: 1, val: 'Emerald Green 525nm', pkg: '0805 SMD', desc: 'Verified Cryptographic State & Valid Signature Indicator', mfr: 'Kingbright', zone: 'Zone 6' },
    { ref: 'LED2', qty: 1, val: 'Crimson Red 625nm', pkg: '0805 SMD', desc: 'Tamper / IBR Overpressure / Wire-Cut Alarm Indicator', mfr: 'Kingbright', zone: 'Zone 6' },
    { ref: 'SW1', qty: 1, val: 'PTS645SM43SMTR', pkg: 'SMD Tactile 6x6mm', desc: 'SIL Tamper / Wire Break Emulation Pushbutton (GPIO5)', mfr: 'C&K Components', zone: 'Zone 6' },
    { ref: 'L1', qty: 1, val: '10 µH ±20% 3.5A', pkg: 'SMD 7.3x7.3mm', desc: 'Synchronous Buck Output Power Inductor (SRN6045)', mfr: 'Bourns', zone: 'Zone 1' },
    { ref: 'H1-H4', qty: 4, val: 'M3_Mounting_Hole', pkg: 'MountingHole 3.2mm', desc: 'Corner Mechanical Mounting Holes with 6mm Ground Pads', mfr: 'Hardware Standard', zone: 'Chassis' },
  ];

  const netlistRows = [
    { net: '+3V3_CLEAN', from: 'U5 Pin 5 (VOUT)', to: 'U1 Pin 2, U2 Pin 8, U3 Pin 8', desc: 'Low-Noise 3.3V Analog & Core Logic Supply' },
    { net: 'GND', from: 'U5 Pin 2, Ground Plane', to: 'U1, U2, U3, Shunts R1-R5, TVS D1-D5', desc: 'Common 2-Layer Reference Ground Plane' },
    { net: 'I2C_SDA', from: 'U1 Pin 13 (GPIO8)', to: 'U2 Pin 5, U3 Pin 9, R11 (4.7k Pullup)', desc: 'Hardware I2C Data (Shared with Crypto & ADC)' },
    { net: 'I2C_SCL', from: 'U1 Pin 14 (GPIO9)', to: 'U2 Pin 6, U3 Pin 10, R12 (4.7k Pullup)', desc: 'Hardware I2C Clock (Shared with Crypto & ADC)' },
    { net: 'AIN0_PT101', from: 'J2 -> D1 -> R1 -> R6', to: 'U3 Pin 4 (AIN0)', desc: 'Pressure Loop 1: 0-25 bar (16-bit ADS1115)' },
    { net: 'AIN1_TT101', from: 'J3 -> D2 -> R2 -> R7', to: 'U3 Pin 5 (AIN1)', desc: 'Steam Temp Loop 2: 0-350 °C (16-bit ADS1115)' },
    { net: 'AIN2_TT102', from: 'J4 -> D3 -> R3 -> R8', to: 'U3 Pin 6 (AIN2)', desc: 'Stack Temp Loop 3: 0-500 °C (16-bit ADS1115)' },
    { net: 'AIN3_FT101', from: 'J5 -> D4 -> R4 -> R9', to: 'U3 Pin 7 (AIN3)', desc: 'Flow Loop 4: 0-5000 kg/hr (16-bit ADS1115)' },
    { net: 'AIN4_AT101', from: 'J6 -> D5 -> R5 -> R10/C5', to: 'U1 Pin 4 (GPIO4 / ADC1_CH3)', desc: 'TDS & Level Loop 5 (Direct ESP32 12-bit SAR ADC)' },
    { net: 'TAMPER_IN', from: 'SW1 Pin 2', to: 'U1 Pin 10 (GPIO5)', desc: 'Active-Low SIL Tamper Emulation Line' },
    { net: 'LED_GREEN', from: 'U1 Pin 11 (GPIO6)', to: 'R13 (220Ω) -> LED1 Anode', desc: 'Verified Telemetry Status Indication' },
    { net: 'LED_RED', from: 'U1 Pin 12 (GPIO7)', to: 'R14 (220Ω) -> LED2 Anode', desc: 'Tamper / Statutory IBR Alarm Indication' },
  ];

  const filteredBOM = bomComponents.filter(c => 
    c.ref.toLowerCase().includes(bomSearch.toLowerCase()) ||
    c.val.toLowerCase().includes(bomSearch.toLowerCase()) ||
    c.desc.toLowerCase().includes(bomSearch.toLowerCase()) ||
    c.pkg.toLowerCase().includes(bomSearch.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-800/80 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-700 flex items-center justify-center shadow-lg">
              <Cpu className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold text-gray-100 tracking-wide uppercase">
                  Hardware CAD, KiCad 8 PCB &amp; ISO Schematic Blueprint
                </h2>
                <span className="bg-cyan-950/80 border border-cyan-600/60 text-cyan-400 font-mono text-[10px] px-2 py-0.5 rounded font-bold">
                  IEC 61508 SIL-2 HARDWARE
                </span>
              </div>
              <p className="text-xs font-mono text-gray-400">
                120mm × 90mm Industrial 2-Layer Board • 42 Components • 5x 4-20mA Channels (ADS1115 + ESP32 SAR)
              </p>
            </div>
          </div>

          {/* Mode Switcher */}
          <div className="flex items-center gap-2">
            <div className="flex items-center bg-[#1E293B] p-1 rounded-xl border border-gray-700">
              <button
                onClick={() => setActiveMode('pcb')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeMode === 'pcb'
                    ? 'bg-cyan-600 text-black shadow-md'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                <Box className="w-3.5 h-3.5" />
                <span>3D/2D PCB Visualizer</span>
              </button>

              <button
                onClick={() => setActiveMode('schematic')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeMode === 'schematic'
                    ? 'bg-cyan-600 text-black shadow-md'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                <FileCode className="w-3.5 h-3.5" />
                <span>ISO Schematic Blueprint</span>
              </button>

              <button
                onClick={() => setActiveMode('bom')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeMode === 'bom'
                    ? 'bg-cyan-600 text-black shadow-md'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                <span>BOM &amp; Netlist (42 Components)</span>
              </button>
            </div>

            {/* Quick Download Buttons */}
            <a
              href="/tapasshield_edge.kicad_pcb"
              download="tapasshield_edge.kicad_pcb"
              className="flex items-center gap-1.5 px-3 py-2 bg-emerald-600 hover:bg-emerald-500 text-black font-mono font-bold text-xs rounded-lg transition-colors shadow-lg"
              title="Download full KiCad 8 PCB S-expression layout"
            >
              <Download className="w-3.5 h-3.5" />
              <span>.kicad_pcb</span>
            </a>

            <a
              href="/tapasshield_schematic_blueprint.svg"
              download="tapasshield_schematic_blueprint.svg"
              className="flex items-center gap-1.5 px-3 py-2 bg-gray-800 hover:bg-gray-700 text-gray-200 font-mono text-xs rounded-lg border border-gray-700 transition-colors"
              title="Download publication-grade ISO 5457 blueprint SVG"
            >
              <Download className="w-3.5 h-3.5" />
              <span>SVG Blueprint</span>
            </a>
          </div>
        </div>

        {/* MODE 1: INTERACTIVE PCB LAYOUT */}
        {activeMode === 'pcb' && (
          <div className="mt-5 space-y-4">
            {/* PCB Controls Bar */}
            <div className="flex flex-wrap items-center justify-between gap-3 bg-gray-900/90 p-3 rounded-xl border border-gray-800 text-xs font-mono">
              <div className="flex items-center gap-2">
                <span className="text-gray-400 font-semibold">VIEW MODE:</span>
                <button
                  onClick={() => setPcbDisplayType('kicad_3d_iso')}
                  className={`px-3 py-1 rounded border font-semibold transition-all ${pcbDisplayType === 'kicad_3d_iso' ? 'bg-cyan-950 border-cyan-500 text-cyan-300 shadow-md' : 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white'}`}
                >
                  KiCad 3D Raytraced (ISO)
                </button>
                <button
                  onClick={() => setPcbDisplayType('kicad_3d_top')}
                  className={`px-3 py-1 rounded border font-semibold transition-all ${pcbDisplayType === 'kicad_3d_top' ? 'bg-cyan-950 border-cyan-500 text-cyan-300 shadow-md' : 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white'}`}
                >
                  KiCad 3D Top View
                </button>
                <button
                  onClick={() => setPcbDisplayType('interactive')}
                  className={`px-3 py-1 rounded border font-semibold transition-all ${pcbDisplayType === 'interactive' ? 'bg-cyan-950 border-cyan-500 text-cyan-300 shadow-md' : 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white'}`}
                >
                  Interactive Vector CAD
                </button>
              </div>

              {pcbDisplayType === 'interactive' && (
                <div className="flex items-center gap-3">
                  <span className="text-gray-400 font-semibold">LAYERS:</span>
                  <label className="flex items-center gap-1.5 text-emerald-400 cursor-pointer">
                    <input type="checkbox" checked={showTopCopper} onChange={e => setShowTopCopper(e.target.checked)} className="rounded bg-gray-800 border-gray-700 text-emerald-500" />
                    <span>F.Cu (Top Traces)</span>
                  </label>
                  <label className="flex items-center gap-1.5 text-blue-400 cursor-pointer">
                    <input type="checkbox" checked={showBottomCopper} onChange={e => setShowBottomCopper(e.target.checked)} className="rounded bg-gray-800 border-gray-700 text-blue-500" />
                    <span>B.Cu (Ground Pour)</span>
                  </label>
                  <label className="flex items-center gap-1.5 text-gray-200 cursor-pointer">
                    <input type="checkbox" checked={showSilkscreen} onChange={e => setShowSilkscreen(e.target.checked)} className="rounded bg-gray-800 border-gray-700 text-white" />
                    <span>F.SilkS (Legend)</span>
                  </label>
                </div>
              )}
            </div>

            {/* PCB Canvas Container */}
            <div className="w-full bg-[#080C14] border border-gray-800 rounded-xl p-6 flex flex-col items-center justify-center min-h-[560px] overflow-hidden relative">
              {pcbDisplayType === 'kicad_3d_iso' && (
                <div className="flex flex-col items-center gap-3 w-full">
                  <div className="relative max-w-4xl rounded-xl overflow-hidden border border-cyan-600/30 shadow-2xl bg-black/60">
                    <img 
                      src="/pcb_3d_iso.png" 
                      alt="KiCad 3D Raytraced Isometric View" 
                      className="w-full h-auto object-contain max-h-[620px]"
                    />
                    <div className="absolute top-3 right-3 bg-black/80 border border-cyan-500/50 rounded-lg px-2.5 py-1 text-[11px] font-mono text-cyan-300">
                      KiCad 8+ Raytraced 3D Engine • 120x90mm
                    </div>
                  </div>
                  <p className="text-xs font-mono text-gray-400">
                    High-quality raytraced 3D render generated directly via <code className="text-cyan-400">kicad-cli pcb render</code> with custom VRML models.
                  </p>
                </div>
              )}

              {pcbDisplayType === 'kicad_3d_top' && (
                <div className="flex flex-col items-center gap-3 w-full">
                  <div className="relative max-w-4xl rounded-xl overflow-hidden border border-cyan-600/30 shadow-2xl bg-black/60">
                    <img 
                      src="/pcb_3d_top.png" 
                      alt="KiCad 3D Top Orthographic View" 
                      className="w-full h-auto object-contain max-h-[620px]"
                    />
                    <div className="absolute top-3 right-3 bg-black/80 border border-cyan-500/50 rounded-lg px-2.5 py-1 text-[11px] font-mono text-cyan-300">
                      KiCad 8+ Top 3D View • 120x90mm
                    </div>
                  </div>
                  <p className="text-xs font-mono text-gray-400">
                    Orthographic top-down physical component layout and connector alignment render.
                  </p>
                </div>
              )}

              {pcbDisplayType === 'interactive' && (
                <div 
                  className="transition-transform duration-500 ease-out origin-center"
                  style={{
                    transform: is3DView ? 'perspective(1200px) rotateX(25deg) rotateZ(-12deg) scale(0.92)' : 'none',
                    boxShadow: is3DView ? '0 30px 60px rgba(0,0,0,0.8), 0 0 40px rgba(6,182,212,0.1)' : 'none',
                  }}
                >
                {/* 100mm x 80mm Board SVG (Scale: 10px = 1mm -> 1000 x 800) */}
                <svg
                  viewBox="0 0 1000 800"
                  width="850"
                  height="680"
                  className="select-none rounded-lg"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <defs>
                    <linearGradient id="pcbSubstrate" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#064E3B" />
                      <stop offset="50%" stopColor="#043C2E" />
                      <stop offset="100%" stopColor="#064E3B" />
                    </linearGradient>

                    <linearGradient id="goldPad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#F59E0B" />
                      <stop offset="100%" stopColor="#D97706" />
                    </linearGradient>

                    <linearGradient id="rfShield" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#94A3B8" />
                      <stop offset="50%" stopColor="#CBD5E1" />
                      <stop offset="100%" stopColor="#64748B" />
                    </linearGradient>
                  </defs>

                  {/* 1. PCB Edge.Cuts (100mm x 80mm with 3mm rounded corners) */}
                  <rect
                    x="20"
                    y="20"
                    width="960"
                    height="760"
                    rx="25"
                    fill="url(#pcbSubstrate)"
                    stroke="#F59E0B"
                    strokeWidth="3"
                  />

                  {/* 2. Bottom Ground Plane Cross-Hatch (B.Cu) */}
                  {showBottomCopper && (
                    <g opacity="0.15">
                      <pattern id="gndHatch" width="10" height="10" patternUnits="userSpaceOnUse">
                        <line x1="0" y1="0" x2="10" y2="10" stroke="#38BDF8" strokeWidth="1" />
                      </pattern>
                      <rect x="25" y="25" width="950" height="750" rx="20" fill="url(#gndHatch)" />
                    </g>
                  )}

                  {/* 3. Four M3 Mounting Holes (Corners) */}
                  {[
                    { cx: 70, cy: 70, id: 'H1' },
                    { cx: 930, cy: 70, id: 'H2' },
                    { cx: 70, cy: 730, id: 'H3' },
                    { cx: 930, cy: 730, id: 'H4' },
                  ].map(h => (
                    <g key={h.id} className="cursor-pointer" onClick={() => setSelectedComponent(h.id)}>
                      <circle cx={h.cx} cy={h.cy} r="30" fill="none" stroke="#F59E0B" strokeWidth="6" />
                      <circle cx={h.cx} cy={h.cy} r="16" fill="#080C14" />
                      <text x={h.cx} y={h.cy + 42} fill="#CBD5E1" fontSize="12" fontFamily="monospace" textAnchor="middle">{h.id} (M3)</text>
                    </g>
                  ))}

                  {/* 4. Top Copper Routing Tracks (F.Cu) */}
                  {showTopCopper && (
                    <g stroke="#10B981" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" opacity="0.9">
                      {/* Loop 1: J2 -> D1 -> R1 -> R6 -> U3 AIN0 */}
                      <path d="M 110 220 L 200 220 L 270 220 L 330 220 L 400 220 L 480 380" />
                      {/* Loop 2: J3 -> D2 -> R2 -> R7 -> U3 AIN1 */}
                      <path d="M 110 340 L 200 340 L 270 340 L 330 340 L 400 340 L 480 395" />
                      {/* Loop 3: J4 -> D3 -> R3 -> R8 -> U3 AIN2 */}
                      <path d="M 110 460 L 200 460 L 270 460 L 330 460 L 400 460 L 520 395" />
                      {/* Loop 4: J5 -> D4 -> R4 -> R9 -> U3 AIN3 */}
                      <path d="M 110 580 L 200 580 L 270 580 L 330 580 L 400 580 L 520 380" />
                      {/* Loop 5: J6 -> D5 -> R5 -> R10 -> U1 Pin 4 (GPIO4 / ADC1_CH3) */}
                      <path d="M 110 700 L 200 700 L 270 700 L 330 700 L 400 700 L 720 700 L 750 450" stroke="#EC4899" strokeWidth="6" />

                      {/* Power Rails (+24V, +5V, +3V3) */}
                      <path d="M 110 100 L 220 100 L 340 120" stroke="#F59E0B" strokeWidth="6" />
                      <path d="M 340 120 L 430 120 L 530 120" stroke="#10B981" strokeWidth="6" />
                      <path d="M 530 120 L 600 120 L 780 240" stroke="#38BDF8" strokeWidth="6" />

                      {/* I2C SDA & SCL Lines */}
                      <path d="M 520 370 L 620 370 L 620 580 L 520 580" stroke="#A855F7" strokeWidth="4" />
                      <path d="M 620 370 L 780 320" stroke="#A855F7" strokeWidth="4" />
                    </g>
                  )}

                  {/* 5. Terminal Blocks J1 - J6 (Along Left Board Edge) */}
                  {[
                    { ref: 'J1', label: '24V IN', y: 100, col: '#F59E0B' },
                    { ref: 'J2', label: 'PT-101 (PRESS)', y: 220, col: '#10B981' },
                    { ref: 'J3', label: 'TT-101 (STEAM)', y: 340, col: '#06B6D4' },
                    { ref: 'J4', label: 'TT-102 (STACK)', y: 460, col: '#F59E0B' },
                    { ref: 'J5', label: 'FT-101 (FLOW)', y: 580, col: '#38BDF8' },
                    { ref: 'J6', label: 'AT-101 (TDS)', y: 700, col: '#EC4899' },
                  ].map(j => (
                    <g 
                      key={j.ref} 
                      className="cursor-pointer transition-transform hover:opacity-90"
                      onClick={() => setSelectedComponent(j.ref)}
                    >
                      <rect x="50" y={j.y - 45} width="65" height="90" rx="6" fill="#15803D" stroke="#22C55E" strokeWidth="2" />
                      <circle cx="82" cy={j.y - 22} r="12" fill="#1E293B" stroke="#94A3B8" strokeWidth="3" />
                      <circle cx="82" cy={j.y + 22} r="12" fill="#1E293B" stroke="#94A3B8" strokeWidth="3" />
                      <text x="82" y={j.y - 18} fill="#CBD5E1" fontSize="12" fontFamily="monospace" textAnchor="middle">+</text>
                      <text x="82" y={j.y + 26} fill="#CBD5E1" fontSize="12" fontFamily="monospace" textAnchor="middle">-</text>
                      <text x="125" y={j.y + 4} fill={j.col} fontSize="11" fontFamily="monospace" fontWeight="bold">{j.ref}: {j.label}</text>
                    </g>
                  ))}

                  {/* 6. TVS Diodes D1-D5, Shunts R1-R5, Filters R6-R10 & C1-C5 */}
                  {[220, 340, 460, 580, 700].map((y, idx) => {
                    const chNum = idx + 1;
                    return (
                      <g key={`afe_row_${chNum}`}>
                        {/* TVS Diode */}
                        <g className="cursor-pointer" onClick={() => setSelectedComponent(`D${chNum}`)}>
                          <rect x="200" y={y - 15} width="35" height="30" rx="3" fill="#1E293B" stroke="#EF4444" strokeWidth="1.5" />
                          <line x1="208" y1={y - 15} x2="208" y2={y + 15} stroke="#FFFFFF" strokeWidth="2" />
                          <text x="217" y={y - 20} fill="#EF4444" fontSize="9" fontFamily="monospace">D{chNum}</text>
                        </g>

                        {/* 150R Precision Shunt 0805 */}
                        <g className="cursor-pointer" onClick={() => setSelectedComponent(`R${chNum}`)}>
                          <rect x="270" y={y - 15} width="40" height="30" rx="3" fill="#1E293B" stroke="#F59E0B" strokeWidth="1.5" />
                          <text x="290" y={y + 5} fill="#F59E0B" fontSize="9" fontFamily="monospace" textAnchor="middle">150Ω</text>
                          <text x="290" y={y - 20} fill="#CBD5E1" fontSize="9" fontFamily="monospace" textAnchor="middle">R{chNum}</text>
                        </g>

                        {/* 100R Filter Resistor 0603 */}
                        <g className="cursor-pointer" onClick={() => setSelectedComponent(`R${chNum+5}`)}>
                          <rect x="340" y={y - 12} width="35" height="24" rx="2" fill="#1E293B" stroke="#38BDF8" strokeWidth="1.5" />
                          <text x="357" y={y + 4} fill="#38BDF8" fontSize="8" fontFamily="monospace" textAnchor="middle">100Ω</text>
                          <text x="357" y={y - 16} fill="#CBD5E1" fontSize="9" fontFamily="monospace" textAnchor="middle">R{chNum+5}</text>
                        </g>

                        {/* 100nF Filter Cap 0603 */}
                        <g className="cursor-pointer" onClick={() => setSelectedComponent(`C${chNum}`)}>
                          <rect x="400" y={y - 12} width="35" height="24" rx="2" fill="#1E293B" stroke="#A855F7" strokeWidth="1.5" />
                          <text x="417" y={y + 4} fill="#A855F7" fontSize="8" fontFamily="monospace" textAnchor="middle">100n</text>
                          <text x="417" y={y - 16} fill="#CBD5E1" fontSize="9" fontFamily="monospace" textAnchor="middle">C{chNum}</text>
                        </g>
                      </g>
                    );
                  })}

                  {/* 7. Power Stage: D6/D7, U4 (TPS54302), L1 (10µH), U5 (AP2112K) */}
                  <g className="cursor-pointer" onClick={() => setSelectedComponent('U4')}>
                    <rect x="320" y="100" width="45" height="40" rx="3" fill="#0F172A" stroke="#10B981" strokeWidth="2" />
                    <text x="342" y="125" fill="#10B981" fontSize="10" fontFamily="monospace" fontWeight="bold" textAnchor="middle">U4</text>
                    <text x="342" y="90" fill="#94A3B8" fontSize="9" fontFamily="monospace" textAnchor="middle">TPS54302</text>
                  </g>

                  <g className="cursor-pointer" onClick={() => setSelectedComponent('L1')}>
                    <rect x="400" y="90" width="60" height="60" rx="4" fill="#1E293B" stroke="#F59E0B" strokeWidth="2" />
                    <circle cx="430" cy="120" r="18" fill="none" stroke="#F59E0B" strokeWidth="3" />
                    <text x="430" y="125" fill="#F59E0B" fontSize="10" fontFamily="monospace" fontWeight="bold" textAnchor="middle">10µH</text>
                    <text x="430" y="80" fill="#CBD5E1" fontSize="9" fontFamily="monospace" textAnchor="middle">L1</text>
                  </g>

                  <g className="cursor-pointer" onClick={() => setSelectedComponent('U5')}>
                    <rect x="500" y="100" width="45" height="40" rx="3" fill="#0F172A" stroke="#06B6D4" strokeWidth="2" />
                    <text x="522" y="125" fill="#06B6D4" fontSize="10" fontFamily="monospace" fontWeight="bold" textAnchor="middle">U5</text>
                    <text x="522" y="90" fill="#94A3B8" fontSize="9" fontFamily="monospace" textAnchor="middle">AP2112K</text>
                  </g>

                  {/* 8. U3: ADS1115 MSOP-10 (16-Bit ADC) */}
                  <g className="cursor-pointer" onClick={() => setSelectedComponent('U3')}>
                    <rect x="475" y="360" width="55" height="70" rx="4" fill="#0F172A" stroke="#06B6D4" strokeWidth="2" />
                    <circle cx="485" cy="372" r="3" fill="#06B6D4" />
                    <text x="502" y="400" fill="#F8FAFC" fontSize="11" fontFamily="monospace" fontWeight="bold" textAnchor="middle">U3</text>
                    <text x="502" y="416" fill="#06B6D4" fontSize="9" fontFamily="monospace" textAnchor="middle">ADS1115</text>
                  </g>

                  {/* 9. U2: ATECC608B SOIC-8 (Hardware Crypto Element) */}
                  <g className="cursor-pointer" onClick={() => setSelectedComponent('U2')}>
                    <rect x="475" y="550" width="55" height="65" rx="4" fill="#0F172A" stroke="#A855F7" strokeWidth="2" />
                    <circle cx="485" cy="562" r="3" fill="#A855F7" />
                    <text x="502" y="585" fill="#F8FAFC" fontSize="11" fontFamily="monospace" fontWeight="bold" textAnchor="middle">U2</text>
                    <text x="502" y="601" fill="#A855F7" fontSize="8" fontFamily="monospace" textAnchor="middle">ATECC608</text>
                  </g>

                  {/* 10. U1: ESP32-S3-WROOM-1 (Xtensa Dual-Core) */}
                  <g className="cursor-pointer" onClick={() => setSelectedComponent('U1')}>
                    {/* Metal RF Shield */}
                    <rect x="740" y="200" width="200" height="280" rx="6" fill="url(#rfShield)" stroke="#475569" strokeWidth="2" />
                    {/* PCB Antenna Area (Top) */}
                    <rect x="740" y="140" width="200" height="60" fill="#032D22" stroke="#F59E0B" strokeWidth="1.5" />
                    <path d="M 760 160 H 920 V 175 H 770 V 185 H 910" fill="none" stroke="#F59E0B" strokeWidth="3" />
                    <text x="840" y="195" fill="#F59E0B" fontSize="9" fontFamily="monospace" textAnchor="middle">2.4GHz PCB ANTENNA</text>
                    {/* Espressif Logo / Text */}
                    <text x="840" y="270" fill="#0F172A" fontSize="15" fontFamily="sans-serif" fontWeight="bold" textAnchor="middle">ESPRESSIF</text>
                    <text x="840" y="295" fill="#1E293B" fontSize="13" fontFamily="monospace" fontWeight="bold" textAnchor="middle">ESP32-S3</text>
                    <text x="840" y="320" fill="#334155" fontSize="10" fontFamily="monospace" textAnchor="middle">WROOM-1-N16R8</text>
                    {/* Perimeter Pads */}
                    {[...Array(14)].map((_, i) => (
                      <rect key={`esp_pad_${i}`} x="732" y={220 + i * 18} width="12" height="8" rx="1" fill="#F59E0B" />
                    ))}
                    {[...Array(14)].map((_, i) => (
                      <rect key={`esp_pad_r_${i}`} x="936" y={220 + i * 18} width="12" height="8" rx="1" fill="#F59E0B" />
                    ))}
                  </g>

                  {/* 11. SW1 Tactile Tamper Switch */}
                  <g className="cursor-pointer" onClick={() => setSelectedComponent('SW1')}>
                    <rect x="630" y="670" width="60" height="60" rx="4" fill="#334155" stroke="#94A3B8" strokeWidth="2" />
                    <circle cx="660" cy="700" r="16" fill="#EF4444" stroke="#DC2626" strokeWidth="2" />
                    <text x="660" y="660" fill="#EF4444" fontSize="10" fontFamily="monospace" fontWeight="bold" textAnchor="middle">SW1 (TAMPER)</text>
                  </g>

                  {/* 12. LEDs (LED1 Emerald, LED2 Crimson) */}
                  <g className="cursor-pointer" onClick={() => setSelectedComponent('LED1')}>
                    <rect x="760" y="660" width="30" height="20" rx="2" fill="#1E293B" stroke="#10B981" strokeWidth="1.5" />
                    <circle cx="775" cy="670" r="5" fill="#10B981" className="animate-pulse" />
                    <text x="775" y="650" fill="#10B981" fontSize="9" fontFamily="monospace" textAnchor="middle">LED1</text>
                  </g>

                  <g className="cursor-pointer" onClick={() => setSelectedComponent('LED2')}>
                    <rect x="760" y="700" width="30" height="20" rx="2" fill="#1E293B" stroke="#EF4444" strokeWidth="1.5" />
                    <circle cx="775" cy="710" r="5" fill="#EF4444" />
                    <text x="775" y="735" fill="#EF4444" fontSize="9" fontFamily="monospace" textAnchor="middle">LED2</text>
                  </g>

                  {/* 13. Silkscreen Text & Markings (F.SilkS) */}
                  {showSilkscreen && (
                    <g fill="#F8FAFC" opacity="0.85">
                      <text x="500" y="55" fontSize="18" fontFamily="monospace" fontWeight="bold" textAnchor="middle">
                        TAPASSHIELD INDUSTRIAL SIL-2 EDGE NODE
                      </text>
                      <text x="500" y="75" fontSize="11" fontFamily="monospace" textAnchor="middle" fill="#94A3B8">
                        IBR-TN-VEL-2026-0891 • 120mm × 90mm • REV 6.0
                      </text>
                    </g>
                  )}
                </svg>
              </div>
              )}

              {/* Bottom Component Quick Inspector Pill */}
              {selectedComponent && (
                <div className="mt-4 p-3.5 bg-gray-900 border border-cyan-500/60 rounded-xl max-w-2xl w-full flex items-center justify-between shadow-xl">
                  <div className="flex items-center gap-3">
                    <span className="px-2.5 py-1 bg-cyan-950 border border-cyan-600 text-cyan-300 font-mono text-xs font-bold rounded">
                      {selectedComponent}
                    </span>
                    <div>
                      <div className="text-xs font-bold text-gray-100 font-mono">
                        {bomComponents.find(c => c.ref === selectedComponent || selectedComponent.startsWith(c.ref))?.desc ?? 'Industrial Subsystem'}
                      </div>
                      <div className="text-[10px] text-gray-400 font-mono">
                        Package: {bomComponents.find(c => c.ref === selectedComponent || selectedComponent.startsWith(c.ref))?.pkg ?? 'SMD/THT'} • 
                        Part: {bomComponents.find(c => c.ref === selectedComponent || selectedComponent.startsWith(c.ref))?.val ?? 'Standard'}
                      </div>
                    </div>
                  </div>
                  <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-2 py-0.5 rounded">
                    3D Model Loaded
                  </span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* MODE 2: PUBLICATION-GRADE SCHEMATIC BLUEPRINT */}
        {activeMode === 'schematic' && (
          <div className="mt-5 space-y-4">
            {/* Schematic Controls */}
            <div className="flex flex-wrap items-center justify-between gap-3 bg-gray-900/90 p-3 rounded-xl border border-gray-800 text-xs font-mono">
              <div className="flex items-center gap-2">
                <span className="text-gray-400 font-semibold">ZONE HIGHLIGHT:</span>
                {[
                  { id: 'all', label: 'All Zones' },
                  { id: 'z1', label: '1: Power' },
                  { id: 'z2', label: '2: 4-20mA AFE' },
                  { id: 'z3', label: '3: ADS1115' },
                  { id: 'z4', label: '4: ATECC608B' },
                  { id: 'z5', label: '5: ESP32-S3' },
                ].map(z => (
                  <button
                    key={z.id}
                    onClick={() => setActiveZone(z.id === 'all' ? null : z.id)}
                    className={`px-2.5 py-1 rounded border transition-colors ${
                      (activeZone === z.id || (!activeZone && z.id === 'all'))
                        ? 'bg-cyan-950 border-cyan-500 text-cyan-300'
                        : 'bg-gray-800 border-gray-700 text-gray-400'
                    }`}
                  >
                    {z.label}
                  </button>
                ))}
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setSchematicZoom(prev => Math.max(0.6, prev - 0.15))}
                  className="p-1.5 bg-gray-800 hover:bg-gray-700 rounded border border-gray-700 text-gray-300"
                  title="Zoom Out"
                >
                  <ZoomOut className="w-4 h-4" />
                </button>
                <span className="w-12 text-center text-gray-300">{Math.round(schematicZoom * 100)}%</span>
                <button
                  onClick={() => setSchematicZoom(prev => Math.min(2.0, prev + 0.15))}
                  className="p-1.5 bg-gray-800 hover:bg-gray-700 rounded border border-gray-700 text-gray-300"
                  title="Zoom In"
                >
                  <ZoomIn className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setSchematicZoom(1)}
                  className="p-1.5 bg-gray-800 hover:bg-gray-700 rounded border border-gray-700 text-gray-300"
                  title="Reset Zoom"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Blueprint Frame */}
            <div className="w-full bg-[#080C14] border border-gray-800 rounded-xl p-4 overflow-auto max-h-[700px] flex items-center justify-center">
              <div 
                className="transition-transform duration-200 origin-top"
                style={{ transform: `scale(${schematicZoom})` }}
              >
                <img
                  src="/tapasshield_schematic_blueprint.svg"
                  alt="TapasShield ISO 5457 Schematic Blueprint"
                  className="w-[1400px] h-auto border border-gray-700/80 rounded shadow-2xl"
                />
              </div>
            </div>
          </div>
        )}

        {/* MODE 3: FULL BILL OF MATERIALS & NETLIST TABLE */}
        {activeMode === 'bom' && (
          <div className="mt-5 space-y-6">
            {/* Search Bar */}
            <div className="flex items-center justify-between gap-4 bg-gray-900/80 p-3.5 rounded-xl border border-gray-800">
              <div className="relative flex-1 max-w-md">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
                <input
                  type="text"
                  value={bomSearch}
                  onChange={e => setBomSearch(e.target.value)}
                  placeholder="Filter by RefDes (U1, D1...), Component, or Package..."
                  className="w-full pl-9 pr-4 py-1.5 bg-gray-950 border border-gray-800 rounded-lg text-xs font-mono text-gray-200 focus:outline-none focus:border-cyan-500"
                />
              </div>
              <span className="text-xs font-mono text-gray-400">
                Displaying <span className="text-cyan-400 font-bold">{filteredBOM.length}</span> of 42 Items
              </span>
            </div>

            {/* BOM Table */}
            <div className="overflow-x-auto rounded-xl border border-gray-800 bg-[#0F172A]">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-[#1E293B] text-gray-300 border-b border-gray-700 uppercase">
                  <tr>
                    <th className="py-2.5 px-3">RefDes</th>
                    <th className="py-2.5 px-3">Qty</th>
                    <th className="py-2.5 px-3">Value / Part</th>
                    <th className="py-2.5 px-3">Package / Footprint</th>
                    <th className="py-2.5 px-3">Manufacturer</th>
                    <th className="py-2.5 px-3">Function / Circuit Zone</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800 text-gray-300">
                  {filteredBOM.map(c => (
                    <tr key={c.ref} className="hover:bg-gray-800/60 transition-colors">
                      <td className="py-2.5 px-3 font-bold text-cyan-400">{c.ref}</td>
                      <td className="py-2.5 px-3">{c.qty}</td>
                      <td className="py-2.5 px-3 font-semibold text-gray-100">{c.val}</td>
                      <td className="py-2.5 px-3 text-gray-400">{c.pkg}</td>
                      <td className="py-2.5 px-3 text-gray-400">{c.mfr}</td>
                      <td className="py-2.5 px-3 text-emerald-400">{c.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pin-to-Pin Netlist Table */}
            <div className="bg-[#0F172A] border border-gray-800 rounded-xl p-4">
              <h3 className="text-sm font-bold text-gray-100 uppercase tracking-wide mb-3 flex items-center gap-2">
                <Zap className="w-4 h-4 text-emerald-400" />
                Physical Pin-to-Pin Netlist (Schematic Routing Interconnects)
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-[#1E293B] text-gray-300 border-b border-gray-700 uppercase">
                    <tr>
                      <th className="py-2 px-3">Net Name</th>
                      <th className="py-2 px-3">Origin Node</th>
                      <th className="py-2 px-3">Destination Node</th>
                      <th className="py-2 px-3">Signal Function</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-800 text-gray-300">
                    {netlistRows.map(n => (
                      <tr key={n.net} className="hover:bg-gray-800/60">
                        <td className="py-2 px-3 font-bold text-cyan-400">{n.net}</td>
                        <td className="py-2 px-3 text-gray-300">{n.from}</td>
                        <td className="py-2 px-3 text-emerald-400">{n.to}</td>
                        <td className="py-2 px-3 text-gray-400">{n.desc}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

