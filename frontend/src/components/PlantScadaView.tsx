import React, { useState, useEffect } from 'react';
import { 
  TrendingDown, 
  IndianRupee, 
  Hourglass, 
  Gauge, 
  Droplets, 
  Flame, 
  AlertTriangle, 
  CheckCircle2 
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Legend 
} from 'recharts';

interface PlantScadaViewProps {
  telemetry: any;
  diagnostics: any;
  rawPhysics: any;
}

export const PlantScadaView: React.FC<PlantScadaViewProps> = ({
  telemetry,
  diagnostics,
  rawPhysics,
}) => {
  const [history, setHistory] = useState<any[]>([]);

  const pressure = telemetry?.pressure_bar ?? 12.0;
  const steamTemp = telemetry?.steam_temp_c ?? 188.0;
  const stackTemp = telemetry?.stack_temp_c ?? 220.0;
  const scaleMm = telemetry?.scale_thickness_mm ?? 0.0;
  const waterLevel = telemetry?.drum_water_level_pct ?? 65.0;

  const eff = diagnostics?.efficiency ?? {};
  const fin = diagnostics?.financial ?? {};
  const scaleRul = diagnostics?.scale_rul ?? {};
  const chem = diagnostics?.chemistry ?? {};

  const currentEff = eff.efficiency_pct ?? 85.5;
  const lossInrHr = fin.financial_loss_inr_hr ?? 0.0;
  const lossInrYear = fin.projected_loss_inr_year ?? 0.0;
  const rulDays = scaleRul.rul_days ?? 180.0;
  const descalingRequired = scaleRul.descaling_required ?? false;

  // Append history sliding window for charts
  useEffect(() => {
    if (!telemetry?.timestamp) return;
    const timeLabel = new Date().toLocaleTimeString();
    setHistory((prev) => {
      const updated = [
        ...prev,
        {
          time: timeLabel,
          pressure: Number(pressure.toFixed(2)),
          stackTemp: Number(stackTemp.toFixed(1)),
          efficiency: Number(currentEff.toFixed(1)),
          lossHr: Number(lossInrHr.toFixed(0)),
        },
      ];
      return updated.slice(-25); // Keep last 25 ticks
    });
  }, [telemetry?.seq_no]);

  return (
    <div className="space-y-6">
      {/* Top 4 KPI Metrics Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* KPI 1: IS 8753 Efficiency */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 shadow-xl">
          <div className="flex items-center justify-between text-gray-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">IS 8753 Efficiency</span>
            <Gauge className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="flex items-baseline gap-2 mb-1">
            <span className={`text-3xl font-extrabold font-mono ${currentEff < 82.0 ? 'text-amber-400' : 'text-emerald-400'}`}>
              {currentEff.toFixed(1)}%
            </span>
            <span className="text-xs text-gray-500 font-mono">Baseline: 86.5%</span>
          </div>
          <div className="text-xs text-gray-400 flex items-center justify-between">
            <span>Dry Flue Loss: {eff.loss_dry_flue_pct ?? 8.8}%</span>
            <span className={currentEff < 86.5 ? 'text-amber-400' : 'text-emerald-400'}>
              {(currentEff - 86.5).toFixed(1)}%
            </span>
          </div>
        </div>

        {/* KPI 2: Live Fuel Penalty ₹/hr */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 shadow-xl">
          <div className="flex items-center justify-between text-gray-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Fuel Waste Rate</span>
            <IndianRupee className="w-4 h-4 text-amber-400" />
          </div>
          <div className="flex items-baseline gap-2 mb-1">
            <span className={`text-3xl font-extrabold font-mono ${lossInrHr > 100 ? 'text-red-400 animate-pulse' : 'text-amber-400'}`}>
              ₹{lossInrHr.toFixed(0)}
            </span>
            <span className="text-xs text-gray-400 font-mono">/ hour</span>
          </div>
          <div className="text-xs text-gray-400">
            Excess Fuel: <span className="font-mono text-gray-200">{(fin.fuel_penalty_kg_h ?? 0).toFixed(1)} kg/hr</span> (@ ₹18/kg)
          </div>
        </div>

        {/* KPI 3: Projected Annual Loss */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 shadow-xl">
          <div className="flex items-center justify-between text-gray-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Projected Annual Penalty</span>
            <TrendingDown className="w-4 h-4 text-red-400" />
          </div>
          <div className="flex items-baseline gap-2 mb-1">
            <span className="text-3xl font-extrabold font-mono text-red-400">
              ₹{(lossInrYear / 100000).toFixed(2)}
            </span>
            <span className="text-xs text-gray-400 font-mono">Lakhs/yr</span>
          </div>
          <div className="text-xs text-gray-400">
            Based on <span className="font-mono text-gray-200">8,000</span> operating hours/year
          </div>
        </div>

        {/* KPI 4: Predictive Descaling RUL */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-4 shadow-xl">
          <div className="flex items-center justify-between text-gray-400 mb-2">
            <span className="text-xs font-mono uppercase tracking-wider">Descaling RUL</span>
            <Hourglass className={`w-4 h-4 ${descalingRequired ? 'text-red-400 animate-spin' : 'text-blue-400'}`} />
          </div>
          <div className="flex items-baseline gap-2 mb-1">
            <span className={`text-3xl font-extrabold font-mono ${descalingRequired ? 'text-red-400 animate-pulse' : 'text-blue-400'}`}>
              {descalingRequired ? '0' : rulDays.toFixed(0)}
            </span>
            <span className="text-xs text-gray-400 font-mono">Days</span>
          </div>
          <div className="text-xs">
            {descalingRequired ? (
              <span className="text-red-400 font-bold flex items-center gap-1">
                <AlertTriangle className="w-3.5 h-3.5" /> SHUTDOWN FOR DESCALING!
              </span>
            ) : (
              <span className="text-gray-400">
                CaCO₃ Scale: <span className="font-mono text-amber-400">{scaleMm.toFixed(2)} mm</span>
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Real-time Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Thermodynamic Pressures & Temperatures */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-gray-100 uppercase tracking-wide">
                Steam Pressure & Flue Stack Temperature Drift
              </h3>
              <p className="text-xs font-mono text-gray-400">
                P_steam (bar) vs T_stack (°C) | Threshold ΔT &gt; 85°C
              </p>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block" /> Pressure
              <span className="w-2.5 h-2.5 rounded-full bg-amber-400 inline-block ml-2" /> Stack Temp
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10, fill: '#6B7280' }} />
                <YAxis yAxisId="left" stroke="#10B981" domain={[0, 20]} tick={{ fontSize: 10, fill: '#10B981' }} />
                <YAxis yAxisId="right" orientation="right" stroke="#F59E0B" domain={[150, 350]} tick={{ fontSize: 10, fill: '#F59E0B' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }}
                  labelStyle={{ color: '#94A3B8', fontFamily: 'monospace' }}
                />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="pressure"
                  stroke="#10B981"
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="stackTemp"
                  stroke="#F59E0B"
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Boiler Efficiency & Financial Loss */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-gray-100 uppercase tracking-wide">
                Thermal Efficiency & Financial Loss Correlation
              </h3>
              <p className="text-xs font-mono text-gray-400">
                IS 8753 Indirect η (%) vs Hourly Fuel Loss (₹/hr)
              </p>
            </div>
            <div className="flex items-center gap-2 text-xs font-mono">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 inline-block" /> Efficiency
              <span className="w-2.5 h-2.5 rounded-full bg-red-400 inline-block ml-2" /> Loss ₹/hr
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
                <XAxis dataKey="time" stroke="#4B5563" tick={{ fontSize: 10, fill: '#6B7280' }} />
                <YAxis yAxisId="left" stroke="#06B6D4" domain={[70, 95]} tick={{ fontSize: 10, fill: '#06B6D4' }} />
                <YAxis yAxisId="right" orientation="right" stroke="#EF4444" domain={[0, 1000]} tick={{ fontSize: 10, fill: '#EF4444' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }}
                  labelStyle={{ color: '#94A3B8', fontFamily: 'monospace' }}
                />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="efficiency"
                  stroke="#06B6D4"
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="lossHr"
                  stroke="#EF4444"
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Predictive Diagnostics & Chemistry Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Scale & Thermal Resistance Card */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-xl">
          <h3 className="text-sm font-bold text-gray-100 uppercase tracking-wide mb-3 flex items-center gap-2">
            <Flame className="w-4 h-4 text-amber-400" />
            Waterside CaCO₃ Scaling & Thermal Resistance Diagnostic
          </h3>

          <div className="space-y-3 text-xs font-mono">
            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Estimated Scale Layer (d_scale):</span>
              <span className="font-bold text-amber-400">{scaleMm.toFixed(3)} mm</span>
            </div>

            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Current Flue Superheat (ΔT = T_stack - T_sat):</span>
              <span className="font-bold text-gray-200">
                +{(stackTemp - (rawPhysics?.t_sat_c ?? 187.96)).toFixed(1)} °C
              </span>
            </div>

            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Clean Tube Nominal ΔT_clean:</span>
              <span className="text-gray-300">32.0 °C</span>
            </div>

            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Mandatory Descaling Threshold:</span>
              <span className="text-red-400 font-bold">ΔT ≥ 85.0 °C (d_scale ≥ 1.38 mm)</span>
            </div>

            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Remaining Temperature Headroom:</span>
              <span className="text-emerald-400 font-bold">
                {(scaleRul.remaining_temp_headroom_c ?? 53.0).toFixed(1)} °C
              </span>
            </div>
          </div>
        </div>

        {/* Boiler Water Chemistry & CoC */}
        <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-xl">
          <h3 className="text-sm font-bold text-gray-100 uppercase tracking-wide mb-3 flex items-center gap-2">
            <Droplets className="w-4 h-4 text-blue-400" />
            Water Quality, pH & Cycles of Concentration (CoC)
          </h3>

          <div className="space-y-3 text-xs font-mono">
            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Boiler Drum TDS (AT-101):</span>
              <span className="font-bold text-gray-200">{(chem.boiler_tds_ppm ?? 2100).toFixed(0)} ppm</span>
            </div>

            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Softened Feedwater TDS:</span>
              <span className="text-gray-300">{(chem.feedwater_tds_ppm ?? 350).toFixed(0)} ppm</span>
            </div>

            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Cycles of Concentration (CoC):</span>
              <span className="font-bold text-cyan-400">{(chem.cycles_of_concentration ?? 6.0).toFixed(2)}x</span>
            </div>

            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Boiler Water pH:</span>
              <span className="font-bold text-emerald-400">{(chem.ph_level ?? 9.8).toFixed(1)} (Optimal 9.5-10.5)</span>
            </div>

            <div className="flex justify-between p-2.5 rounded bg-gray-900 border border-gray-800">
              <span className="text-gray-400">Blowdown Status:</span>
              <span className="text-emerald-400 flex items-center gap-1 font-semibold">
                <CheckCircle2 className="w-3.5 h-3.5" /> {chem.tds_status ?? 'OPTIMAL'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
