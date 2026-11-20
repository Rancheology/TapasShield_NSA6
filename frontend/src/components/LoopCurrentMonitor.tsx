import React from 'react';
import { Cpu, AlertCircle, CheckCircle2, Sliders, Zap } from 'lucide-react';

interface LoopCurrentMonitorProps {
  telemetry: any;
  rawPhysics: any;
}

export const LoopCurrentMonitor: React.FC<LoopCurrentMonitorProps> = ({
  telemetry,
  rawPhysics,
}) => {
  const loopCurrents = telemetry?.loop_currents_ma ?? {};
  const adcCounts = rawPhysics?.adc_counts ?? {};

  const channels = [
    {
      tag: 'PT-101',
      name: 'Drum Steam Pressure',
      key: 'PT_101',
      afe: 'U3 ADS1115 (AIN0)',
      adcType: '16-bit ΔΣ',
      unit: 'bar',
      min: 0.0,
      max: 25.0,
      val: telemetry?.pressure_bar ?? 12.0,
    },
    {
      tag: 'TT-101',
      name: 'Steam Header Temp (PT100)',
      key: 'TT_101',
      afe: 'U3 ADS1115 (AIN1)',
      adcType: '16-bit ΔΣ',
      unit: '°C',
      min: 0.0,
      max: 350.0,
      val: telemetry?.steam_temp_c ?? 188.0,
    },
    {
      tag: 'TT-102',
      name: 'Flue Stack Temp (K-Type)',
      key: 'TT_102',
      afe: 'U3 ADS1115 (AIN2)',
      adcType: '16-bit ΔΣ',
      unit: '°C',
      min: 0.0,
      max: 500.0,
      val: telemetry?.stack_temp_c ?? 220.0,
    },
    {
      tag: 'FT-101',
      name: 'Steam Mass Flow',
      key: 'FT_101',
      afe: 'U3 ADS1115 (AIN3)',
      adcType: '16-bit ΔΣ',
      unit: 'kg/hr',
      min: 0.0,
      max: 5000.0,
      val: telemetry?.mass_flow_kgh ?? 3500.0,
    },
    {
      tag: 'AT-101',
      name: 'Blowdown TDS & Quality',
      key: 'AT_101',
      afe: 'U1 ESP32-S3 (GPIO4 / ADC1_CH3)',
      adcType: '12-bit SAR',
      unit: 'ppm',
      min: 0.0,
      max: 5000.0,
      val: telemetry?.tds_ppm ?? 2100.0,
    },
    {
      tag: 'LT-101',
      name: 'Drum Water Level',
      key: 'LT_101',
      afe: 'Derived Level Transducer',
      adcType: '16-bit / SIL-2',
      unit: '%',
      min: 0.0,
      max: 100.0,
      val: telemetry?.drum_water_level_pct ?? 65.0,
    },
  ];

  return (
    <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-2xl">
      {/* Title */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4 border-b border-gray-800/80 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-emerald-950/60 border border-emerald-800/60 rounded-lg text-emerald-400">
            <Cpu className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-gray-100 uppercase tracking-wide">
              Industrial 4–20 mA Current Loop & ADS1115 AFE Inspector
            </h3>
            <p className="text-xs font-mono text-gray-400">
              150.0 Ω ±0.05% Precision Shunt Resistors | PGA Gain = ±4.096V (125 µV/LSB) | IEC 60381-1
            </p>
          </div>
        </div>

        <div className="text-xs font-mono text-gray-400 bg-gray-900 px-3 py-1.5 rounded-lg border border-gray-800">
          V_shunt = I_mA × 0.150V | ADC = (V_shunt / 4.096) × 32767
        </div>
      </div>

      {/* Grid of channels */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {channels.map((ch) => {
          const ma = loopCurrents[ch.key] ?? 12.0;
          const counts = adcCounts[ch.key] ?? Math.round((ma * 0.150 / 4.096) * 32767);
          const vShunt = (ma * 0.150).toFixed(4);

          // Status determination
          let statusText = 'NORMAL LOOP';
          let statusColor = 'text-emerald-400 border-emerald-800/60 bg-emerald-950/40';
          let isFault = false;

          if (ma < 3.6) {
            statusText = 'LOOP CUT / OPEN CKT';
            statusColor = 'text-red-400 border-red-800/80 bg-red-950/80 animate-pulse';
            isFault = true;
          } else if (ma > 20.5) {
            statusText = 'OVER-RANGE';
            statusColor = 'text-amber-400 border-amber-800/60 bg-amber-950/40';
          }

          // Percentage for visual bar (0 - 24 mA range)
          const pct = Math.max(0, Math.min(100, (ma / 24.0) * 100));

          return (
            <div
              key={ch.key}
              className={`p-3.5 rounded-xl border bg-gray-900/80 transition-all ${
                isFault ? 'border-red-500/80 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : 'border-gray-800 hover:border-gray-700'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-1.5">
                  <span className="font-mono text-xs font-bold text-gray-300">{ch.tag}</span>
                  <span className="text-xs text-gray-400 truncate max-w-[120px]">{ch.name}</span>
                </div>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded border font-semibold ${statusColor}`}>
                  {statusText}
                </span>
              </div>

              {/* Hardware AFE Netlist Tap */}
              <div className="mb-2">
                <span className="inline-block text-[10px] font-mono text-cyan-400 bg-cyan-950/70 border border-cyan-800/60 px-1.5 py-0.5 rounded font-medium">
                  {ch.afe}
                </span>
              </div>

              {/* Loop Current readout */}
              <div className="flex items-baseline justify-between mb-2">
                <div className="flex items-baseline gap-1.5">
                  <span className={`text-2xl font-bold font-mono ${isFault ? 'text-red-400' : 'text-gray-100'}`}>
                    {ma.toFixed(2)}
                  </span>
                  <span className="text-xs font-mono text-gray-400">mA</span>
                </div>

                <div className="text-right">
                  <div className="text-sm font-semibold font-mono text-emerald-400">
                    {ch.val.toFixed(1)} <span className="text-xs text-gray-400">{ch.unit}</span>
                  </div>
                  <div className="text-[10px] text-gray-500 font-mono">
                    Span: {ch.min}-{ch.max}
                  </div>
                </div>
              </div>

              {/* Visual 4-20mA Bar */}
              <div className="relative w-full h-2.5 bg-gray-800 rounded-full overflow-hidden mb-2">
                {/* 4mA marker line (16.6% of 24mA) */}
                <div className="absolute top-0 bottom-0 left-[16.6%] w-0.5 bg-gray-600 z-10" />
                {/* 20mA marker line (83.3% of 24mA) */}
                <div className="absolute top-0 bottom-0 left-[83.3%] w-0.5 bg-gray-600 z-10" />
                {/* Live Fill */}
                <div
                  className={`h-full transition-all duration-300 rounded-full ${
                    isFault ? 'bg-red-500' : ma > 20.0 ? 'bg-amber-400' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${pct}%` }}
                />
              </div>

              {/* Bottom electrical details */}
              <div className="grid grid-cols-2 gap-2 text-[10px] font-mono text-gray-400 pt-1 border-t border-gray-800">
                <div>
                  <span className="text-gray-500">V_shunt: </span>
                  <span className="text-gray-200">{vShunt} V</span>
                </div>
                <div className="text-right">
                  {ch.key === 'AT_101' ? (
                    <>
                      <span className="text-gray-500">ADC12: </span>
                      <span className="text-cyan-300 font-semibold">
                        {Math.min(4095, Math.round((ma * 0.150 / 3.3) * 4095))} cnt
                      </span>
                    </>
                  ) : (
                    <>
                      <span className="text-gray-500">ADC16: </span>
                      <span className="text-gray-200">{counts} cnt</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

