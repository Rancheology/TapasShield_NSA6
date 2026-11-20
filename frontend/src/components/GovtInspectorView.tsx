import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  Key, 
  Search, 
  Database, 
  Lock, 
  FileText, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle,
  RefreshCw,
  Eye,
  ExternalLink,
  Award,
  Globe,
  Building2,
  Clock,
  Check,
  AlertOctagon
} from 'lucide-react';

interface GovtInspectorViewProps {
  telemetry: any;
  cryptoState: any;
  ledgerStatus: any;
  onRunAudit: () => Promise<any>;
  onSimulateDbTamper: () => Promise<any>;
  ledgerBlocks: any[];
}

export const GovtInspectorView: React.FC<GovtInspectorViewProps> = ({
  telemetry,
  cryptoState,
  ledgerStatus,
  onRunAudit,
  onSimulateDbTamper,
  ledgerBlocks,
}) => {
  const [auditReport, setAuditReport] = useState<any | null>(null);
  const [isAuditing, setIsAuditing] = useState(false);
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [showCertModal, setShowCertModal] = useState(false);
  const [tamperFeedback, setTamperFeedback] = useState<string | null>(null);
  const [nationalRegistry, setNationalRegistry] = useState<any | null>(null);
  const [certificateData, setCertificateData] = useState<any | null>(null);

  // Fetch National Registry & Certificate Data
  const fetchEodbData = async () => {
    try {
      const [regRes, certRes] = await Promise.all([
        fetch('/api/eodb/national-registry'),
        fetch('/api/eodb/certificate'),
      ]);
      if (regRes.ok) {
        setNationalRegistry(await regRes.json());
      }
      if (certRes.ok) {
        setCertificateData(await certRes.json());
      }
    } catch (e) {
      console.error('Failed to fetch EODB data', e);
    }
  };

  useEffect(() => {
    fetchEodbData();
  }, [telemetry?.seq_no, ledgerBlocks.length]);

  const handleAuditClick = async () => {
    setIsAuditing(true);
    try {
      const res = await onRunAudit();
      setAuditReport(res);
      await fetchEodbData();
    } catch (e) {
      console.error(e);
    } finally {
      setIsAuditing(false);
    }
  };

  const handleTamperClick = async () => {
    try {
      const res = await onSimulateDbTamper();
      setTamperFeedback(`Historical Block #${res.tampered_seq_no} pressure altered from ${res.original_pressure_bar} to ${res.falsified_pressure_bar} bar directly in DB.`);
      // Automatically re-run audit and refresh certificate to demonstrate instant revocation
      const audit = await onRunAudit();
      setAuditReport(audit);
      await fetchEodbData();
    } catch (e) {
      console.error(e);
    }
  };

  const isVerified = cryptoState?.signature_valid && cryptoState?.hash_chain_valid;
  const isTampered = ledgerStatus?.tamper_detected || (auditReport && !auditReport.chain_valid);
  const isRevoked = certificateData?.eodb_green_channel_status === 'REVOKED_STATUTORY_BREACH' || isTampered || (telemetry?.pressure_bar > 15.0);

  return (
    <div className="space-y-6">
      {/* Top Banner: Central Boilers Board & Regulatory Portal */}
      <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-2xl relative overflow-hidden">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-800/80 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-800 flex items-center justify-center shadow-lg">
              <ShieldCheck className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-bold text-gray-100 tracking-wide uppercase">
                  Central Boilers Board (DPIIT) & State Boiler Inspectorate e-Register
                </h2>
                <span className="bg-emerald-950/80 border border-emerald-600/60 text-emerald-400 font-mono text-[10px] px-2 py-0.5 rounded font-bold">
                  IBR SEC. 2(c) CERTIFIED
                </span>
              </div>
              <p className="text-xs font-mono text-gray-400">
                Official Statutory Registry | Monitored Boiler ID: <span className="text-gray-200 font-semibold">{telemetry?.boiler_id ?? 'IBR-TN-VEL-2026-0891'}</span>
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setShowCertModal(true)}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg border text-xs font-mono font-bold transition-all shadow-md ${
                isRevoked
                  ? 'border-red-600 bg-red-950/80 text-red-200 animate-pulse'
                  : 'border-emerald-600 bg-emerald-950/60 text-emerald-300 hover:bg-emerald-900/60'
              }`}
            >
              <Award className="w-3.5 h-3.5" />
              <span>{isRevoked ? 'View Revoked Certificate' : 'View Digital IBR Form-VI'}</span>
            </button>

            <button
              onClick={() => setShowKeyModal(true)}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-700 bg-gray-800 hover:bg-gray-700 text-xs font-mono text-gray-300 hover:text-white transition-colors"
            >
              <Key className="w-3.5 h-3.5 text-emerald-400" />
              <span>Inspect Public Key</span>
            </button>

            <button
              onClick={handleTamperClick}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-red-700/60 bg-red-950/40 hover:bg-red-900/60 text-xs font-mono text-red-300 hover:text-red-100 transition-colors"
              title="Tamper with a historical log in server memory without hardware private key"
            >
              <Database className="w-3.5 h-3.5 text-red-400" />
              <span>Simulate DB Tamper Attack</span>
            </button>

            <button
              onClick={handleAuditClick}
              disabled={isAuditing}
              className="flex items-center gap-1.5 px-4 py-2 rounded-lg border border-emerald-600 bg-emerald-600 hover:bg-emerald-500 text-xs font-mono font-bold text-black transition-all shadow-[0_0_15px_rgba(16,185,129,0.3)] disabled:opacity-50"
            >
              <Search className={`w-3.5 h-3.5 ${isAuditing ? 'animate-spin' : ''}`} />
              <span>{isAuditing ? 'Auditing Ledger...' : 'Run Forensic Audit'}</span>
            </button>
          </div>
        </div>

        {/* Audit Report Banner (if generated) */}
        {auditReport && (
          <div className={`mt-4 p-4 rounded-xl border text-xs font-mono transition-all ${
            auditReport.chain_valid
              ? 'bg-emerald-950/60 border-emerald-500 text-emerald-300'
              : 'bg-red-950/80 border-red-500 text-red-300 shadow-[0_0_20px_rgba(239,68,68,0.3)] animate-pulse'
          }`}>
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-center gap-2 font-bold text-sm">
                {auditReport.chain_valid ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <XCircle className="w-4 h-4 text-red-400" />
                )}
                <span>{auditReport.message}</span>
              </div>
              <span className="text-[10px] text-gray-400">Total Blocks: {auditReport.total_blocks}</span>
            </div>

            {!auditReport.chain_valid && auditReport.tampered_details && (
              <div className="mt-2 pt-2 border-t border-red-800/80 space-y-1 text-red-200">
                <div><span className="text-gray-400">Tampered Block:</span> Sequence #{auditReport.tampered_block_seq}</div>
                <div><span className="text-gray-400">Forensic Reason:</span> {auditReport.tampered_details.reason}</div>
                {auditReport.tampered_details.stored_hash && (
                  <div className="break-all"><span className="text-gray-400">Stored Hash:</span> {auditReport.tampered_details.stored_hash}</div>
                )}
                {auditReport.tampered_details.recomputed_hash && (
                  <div className="break-all"><span className="text-gray-400">Recomputed:</span> {auditReport.tampered_details.recomputed_hash}</div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Tamper Feedback Notification */}
        {tamperFeedback && !auditReport && (
          <div className="mt-3 p-3 bg-red-950/60 border border-red-700/60 rounded-lg text-xs font-mono text-red-300 flex items-center justify-between">
            <span>{tamperFeedback}</span>
            <button onClick={() => setTamperFeedback(null)} className="text-gray-400 hover:text-white">✕</button>
          </div>
        )}

        {/* Regulatory Metadata Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-xs font-mono">
          <div className="p-3 bg-gray-900/80 rounded-lg border border-gray-800">
            <span className="text-gray-400 block text-[10px]">REGISTERED MAWP</span>
            <span className="text-gray-100 font-bold text-sm">15.00 bar</span>
            <span className="text-gray-400 block text-[10px]">Test Press: 22.50 bar</span>
          </div>

          <div className="p-3 bg-gray-900/80 rounded-lg border border-gray-800">
            <span className="text-gray-400 block text-[10px]">HARDWARE SIL CHIP</span>
            <span className="text-emerald-400 font-bold text-sm">ATECC608B</span>
            <span className="text-gray-400 block text-[10px]">Slot 0 Locked (ECDSA P-256)</span>
          </div>

          <div className="p-3 bg-gray-900/80 rounded-lg border border-gray-800">
            <span className="text-gray-400 block text-[10px]">HASH CHAIN INTEGRITY</span>
            <span className={`font-bold text-sm ${isTampered ? 'text-red-400' : 'text-emerald-400'}`}>
              {isTampered ? 'BROKEN / CORRUPTED' : '100% UNBROKEN'}
            </span>
            <span className="text-gray-400 block text-[10px]">Genesis: 00000000...</span>
          </div>

          <div className="p-3 bg-gray-900/80 rounded-lg border border-gray-800">
            <span className="text-gray-400 block text-[10px]">EODB CERTIFICATE SEAL</span>
            <span className={`font-bold text-sm ${!isRevoked ? 'text-emerald-400' : 'text-red-400'}`}>
              {!isRevoked ? 'GREEN-CHANNEL AUTO' : 'STATUTORY HOLD / REVOKED'}
            </span>
            <span className="text-gray-400 block text-[10px]">IBR Form-VI Digital</span>
          </div>
        </div>
      </div>

      {/* Central Govt (DPIIT / Central Boilers Board) National Cluster Grid */}
      <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-2xl">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-4 border-b border-gray-800/80 pb-3">
          <div className="flex items-center gap-2.5">
            <Globe className="w-5 h-5 text-cyan-400" />
            <div>
              <h3 className="text-sm font-bold text-gray-100 uppercase tracking-wide">
                Central Govt (DPIIT) National Industrial Cluster Grid
              </h3>
              <p className="text-xs font-mono text-gray-400">
                Multi-State Real-Time Telemetry &amp; Statutory Compliance Oversight
              </p>
            </div>
          </div>

          {/* EODB Delay Reduction Badge */}
          <div className="flex items-center gap-3">
            <div className="px-3 py-1 rounded-lg bg-emerald-950/70 border border-emerald-600/70 text-emerald-300 font-mono text-xs flex items-center gap-1.5 shadow-sm">
              <Clock className="w-3.5 h-3.5 text-emerald-400" />
              <span>Inspection Queue: <strong className="text-emerald-200">14 Days Manual Visit → 0 Sec Continuous Audit</strong></span>
            </div>
            <div className="px-2.5 py-1 rounded bg-gray-900 border border-gray-800 text-xs font-mono text-gray-300">
              Active States: <span className="text-cyan-400 font-bold">4 (TN, GJ, MH, PB)</span>
            </div>
          </div>
        </div>

        {/* National Boiler Grid Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-gray-800 text-gray-400 bg-gray-950/60">
                <th className="py-2.5 px-3">Registration ID</th>
                <th className="py-2.5 px-3">Cluster / State</th>
                <th className="py-2.5 px-3">Owner MSME</th>
                <th className="py-2.5 px-3 text-right">Pressure / MAWP</th>
                <th className="py-2.5 px-3 text-right">Stack Temp</th>
                <th className="py-2.5 px-3 text-right">Efficiency</th>
                <th className="py-2.5 px-3 text-center">Crypto Chain</th>
                <th className="py-2.5 px-3 text-center">EODB Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60">
              {(nationalRegistry?.boilers || []).map((boiler: any) => {
                const isLive = boiler.is_live_sil_stream;
                const isCompliant = boiler.eodb_inspection_status === 'AUTO-COMPLIANT';

                return (
                  <tr 
                    key={boiler.registration_id}
                    className={`transition-colors ${
                      isLive 
                        ? 'bg-emerald-950/20 hover:bg-emerald-950/30 font-medium' 
                        : 'hover:bg-gray-900/60 text-gray-300'
                    }`}
                  >
                    <td className="py-2.5 px-3 flex items-center gap-2">
                      {isLive && (
                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" title="Live SIL Hardware Stream" />
                      )}
                      <span className={isLive ? 'text-emerald-300 font-bold' : 'text-gray-200'}>
                        {boiler.registration_id}
                      </span>
                      {isLive && (
                        <span className="text-[9px] px-1.5 py-0.2 rounded bg-emerald-900/80 text-emerald-300 border border-emerald-700">
                          LIVE SIL
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 px-3">
                      <div className="text-gray-200">{boiler.cluster_name}</div>
                      <div className="text-[10px] text-gray-500">{boiler.state} ({boiler.state_code})</div>
                    </td>
                    <td className="py-2.5 px-3 text-gray-300 max-w-[200px] truncate" title={boiler.owner_msme}>
                      {boiler.owner_msme}
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <span className={boiler.current_pressure_bar > boiler.mawp_bar ? 'text-red-400 font-bold' : 'text-gray-200'}>
                        {boiler.current_pressure_bar.toFixed(2)}
                      </span>
                      <span className="text-gray-500 text-[10px]"> / {boiler.mawp_bar.toFixed(1)} bar</span>
                    </td>
                    <td className="py-2.5 px-3 text-right text-gray-200">
                      {boiler.stack_temp_c.toFixed(1)} °C
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <span className="text-emerald-400 font-semibold">{boiler.efficiency_pct.toFixed(1)}%</span>
                    </td>
                    <td className="py-2.5 px-3 text-center">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] border ${
                        boiler.crypto_chain_status === 'VERIFIED'
                          ? 'bg-emerald-950/60 border-emerald-800 text-emerald-400'
                          : 'bg-red-950/70 border-red-700 text-red-300 font-bold animate-pulse'
                      }`}>
                        {boiler.crypto_chain_status === 'VERIFIED' ? <Check className="w-3 h-3" /> : <AlertOctagon className="w-3 h-3" />}
                        {boiler.crypto_chain_status}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-center">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded text-[10px] font-bold border ${
                        isCompliant
                          ? 'bg-teal-950/70 border-teal-600 text-teal-300'
                          : 'bg-red-950/80 border-red-500 text-red-200 shadow-[0_0_10px_rgba(239,68,68,0.3)] animate-pulse'
                      }`}>
                        {isCompliant ? 'AUTO-COMPLIANT' : 'INSPECTOR HOLD'}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Live Hash-Chained Blockchain Stream */}
      <div className="bg-[#111827] border border-gray-800 rounded-xl p-5 shadow-2xl">
        <div className="flex items-center justify-between mb-4 border-b border-gray-800/80 pb-3">
          <div>
            <h3 className="text-sm font-bold text-gray-100 uppercase tracking-wide flex items-center gap-2">
              <Lock className="w-4 h-4 text-emerald-400" />
              Cryptographic Telemetry Chain (Zero-Trust Verified Ledger)
            </h3>
            <p className="text-xs font-mono text-gray-400">
              Each block contains SHA-256 hash pointer to predecessor and NIST P-256 DER signature from hardware root-of-trust
            </p>
          </div>

          <span className="text-xs font-mono text-gray-400 bg-gray-900 px-3 py-1 rounded border border-gray-800">
            Blocks: {ledgerBlocks.length}
          </span>
        </div>

        {/* Scrollable Blockchain Cards */}
        <div className="space-y-3 max-h-[460px] overflow-y-auto pr-1">
          {ledgerBlocks.length === 0 ? (
            <div className="text-center py-12 text-gray-500 font-mono text-xs">
              No ledger blocks ingested yet. Waiting for telemetry packets...
            </div>
          ) : (
            ledgerBlocks.slice().reverse().map((block, idx) => {
              const isBlockTampered = !block.signature_valid || !block.hash_chain_valid || block.tamper_detected;
              const p = block.payload ?? {};

              return (
                <div
                  key={block.seq_no}
                  className={`p-3.5 rounded-xl border font-mono text-xs transition-all ${
                    isBlockTampered
                      ? 'bg-red-950/40 border-red-500 shadow-[0_0_15px_rgba(239,68,68,0.2)]'
                      : 'bg-gray-900/90 border-gray-800 hover:border-gray-700'
                  }`}
                >
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded bg-gray-800 text-gray-200 font-bold border border-gray-700">
                        BLOCK #{block.seq_no}
                      </span>
                      <span className="text-gray-400 text-[10px]">
                        {block.timestamp}
                      </span>
                    </div>

                    <div className="flex items-center gap-2">
                      {block.signature_valid ? (
                        <span className="flex items-center gap-1 text-[10px] text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-2 py-0.5 rounded">
                          <CheckCircle2 className="w-3 h-3" /> ECDSA P-256 VALID
                        </span>
                      ) : (
                        <span className="flex items-center gap-1 text-[10px] text-red-400 bg-red-950/60 border border-red-800 px-2 py-0.5 rounded font-bold animate-pulse">
                          <XCircle className="w-3 h-3" /> SIGNATURE INVALID
                        </span>
                      )}

                      {block.hash_chain_valid ? (
                        <span className="flex items-center gap-1 text-[10px] text-blue-400 bg-blue-950/60 border border-blue-800 px-2 py-0.5 rounded">
                          CHAIN LINKED
                        </span>
                      ) : (
                        <span className="flex items-center gap-1 text-[10px] text-red-400 bg-red-950/60 border border-red-800 px-2 py-0.5 rounded font-bold animate-pulse">
                          CHAIN BROKEN
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Telemetry Payload Snapshot */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 my-2 text-[11px] p-2 bg-gray-950/70 rounded border border-gray-800/80">
                    <div>
                      <span className="text-gray-500">Pressure: </span>
                      <span className={p.pressure_bar > 15.0 ? 'text-red-400 font-bold' : 'text-gray-200'}>
                        {p.pressure_bar?.toFixed(2)} bar
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Steam Temp: </span>
                      <span className="text-gray-200">{p.steam_temp_c?.toFixed(1)} °C</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Stack Temp: </span>
                      <span className="text-gray-200">{p.stack_temp_c?.toFixed(1)} °C</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Water Level: </span>
                      <span className={p.drum_water_level_pct < 25.0 ? 'text-red-400 font-bold' : 'text-gray-200'}>
                        {p.drum_water_level_pct?.toFixed(1)} %
                      </span>
                    </div>
                  </div>

                  {/* Hash Linkage Chain */}
                  <div className="space-y-1 text-[10px] text-gray-400 pt-1">
                    <div className="flex items-center gap-1.5 truncate">
                      <span className="text-gray-500 w-16 shrink-0">PREV_HASH:</span>
                      <span className="text-gray-400 font-mono">{block.prev_hash?.slice(0, 24)}...{block.prev_hash?.slice(-8)}</span>
                    </div>
                    <div className="flex items-center gap-1.5 truncate">
                      <span className="text-gray-500 w-16 shrink-0">CURR_HASH:</span>
                      <span className="text-emerald-400 font-mono">{block.current_hash?.slice(0, 24)}...{block.current_hash?.slice(-8)}</span>
                    </div>
                    <div className="flex items-center gap-1.5 truncate">
                      <span className="text-gray-500 w-16 shrink-0">SIGNATURE:</span>
                      <span className="text-cyan-400 font-mono">{block.signature_hex?.slice(0, 32)}...{block.signature_hex?.slice(-10)}</span>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Public Key Modal */}
      {showKeyModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#111827] border border-gray-800 rounded-xl max-w-2xl w-full p-6 shadow-2xl relative">
            <div className="flex items-center justify-between pb-3 border-b border-gray-800 mb-4">
              <div className="flex items-center gap-2">
                <Key className="w-5 h-5 text-emerald-400" />
                <h3 className="font-bold text-gray-100 text-sm">
                  ATECC608B Provisioned ECDSA P-256 Public Key (PEM)
                </h3>
              </div>
              <button
                onClick={() => setShowKeyModal(false)}
                className="text-gray-400 hover:text-white font-mono text-sm"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-gray-400 mb-3">
              This public key is permanently registered with the State Boiler Inspectorate. Telemetry signed by the on-chip private key in Slot 0 is verified against this certificate.
            </p>

            <pre className="bg-[#090D16] p-4 rounded-lg border border-gray-800 text-[11px] font-mono text-emerald-400 overflow-x-auto select-all">
              {cryptoState?.public_key_pem || 'No public key registered yet.'}
            </pre>

            <div className="mt-4 flex justify-end">
              <button
                onClick={() => setShowKeyModal(false)}
                className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-200 rounded-lg text-xs font-mono font-medium"
              >
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Digital IBR Form-VI EODB Certificate Modal */}
      {showCertModal && certificateData && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-[#0B1120] border-2 border-emerald-600/80 rounded-2xl max-w-3xl w-full p-8 shadow-[0_0_50px_rgba(16,185,129,0.25)] relative my-8">
            {/* Header: Ashoka Lion & Govt Identity */}
            <div className="text-center pb-5 border-b border-gray-700/80 relative">
              <button
                onClick={() => setShowCertModal(false)}
                className="absolute right-0 top-0 text-gray-400 hover:text-white font-mono text-lg p-2"
              >
                ✕
              </button>

              <div className="inline-block px-3 py-1 bg-emerald-950/80 border border-emerald-500/70 rounded-full text-emerald-300 font-mono text-[11px] font-bold tracking-wider uppercase mb-2">
                GOVERNMENT OF INDIA • STATUTORY EODB REGISTRY
              </div>
              <h2 className="text-lg font-black text-white tracking-wide uppercase font-serif">
                Directorate of Boilers • Government of Tamil Nadu
              </h2>
              <p className="text-xs text-gray-300 font-mono mt-0.5">
                In Concurrence with the Central Boilers Board (CBB) &amp; DPIIT (Ministry of Commerce &amp; Industry)
              </p>
              <h3 className="text-base font-extrabold text-emerald-400 uppercase tracking-widest mt-2 border-t border-b border-gray-800 py-1 font-mono">
                FORM-VI: CERTIFICATE FOR THE USE OF A BOILER
              </h3>
              <p className="text-[11px] text-gray-400 font-mono mt-1">
                Indian Boiler Regulations 1950 (Rule 392 &amp; Continuous Digital Telemetry Revision 2026)
              </p>
            </div>

            {/* Dynamic Status Seal Banner */}
            <div className="my-5">
              {certificateData.eodb_green_channel_status === 'APPROVED_REMOTE' && !isRevoked ? (
                <div className="p-4 rounded-xl bg-gradient-to-r from-emerald-950/80 via-teal-950/80 to-emerald-950/80 border-2 border-emerald-500 shadow-[0_0_25px_rgba(16,185,129,0.3)] flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-400 flex items-center justify-center shrink-0">
                      <Award className="w-7 h-7 text-emerald-400" />
                    </div>
                    <div>
                      <div className="text-xs font-mono font-bold text-emerald-400 tracking-wider">
                        IBR GREEN-CHANNEL AUTO-RENEWAL SEAL
                      </div>
                      <div className="text-base font-extrabold text-white">
                        DIGITAL USE CERTIFICATE: APPROVED &amp; VALID
                      </div>
                      <div className="text-[11px] font-mono text-emerald-300/80">
                        Zero In-Person Inspection Queue • Zero Manual Bribery Touchpoint
                      </div>
                    </div>
                  </div>
                  <div className="text-right hidden sm:block font-mono text-xs text-emerald-300">
                    <div>CERT #{certificateData.certificate_id}</div>
                    <div className="text-[10px] text-gray-400">VALID UNTIL: {certificateData.valid_until?.slice(0, 10)}</div>
                  </div>
                </div>
              ) : (
                <div className="p-4 rounded-xl bg-gradient-to-r from-red-950 via-rose-950 to-red-950 border-2 border-red-500 shadow-[0_0_30px_rgba(239,68,68,0.4)] animate-pulse flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-red-500/20 border border-red-400 flex items-center justify-center shrink-0">
                      <AlertOctagon className="w-7 h-7 text-red-400" />
                    </div>
                    <div>
                      <div className="text-xs font-mono font-bold text-red-400 tracking-wider">
                        STATUTORY ENFORCEMENT NOTICE — IBR SECTION 14
                      </div>
                      <div className="text-base font-extrabold text-white">
                        CERTIFICATE OF USE IMMEDIATELY REVOKED
                      </div>
                      <div className="text-[11px] font-mono text-red-300">
                        Immediate Steam Cessation Order • Inspector Hold Placed on Cluster Node
                      </div>
                    </div>
                  </div>
                  <div className="text-right hidden sm:block font-mono text-xs text-red-300">
                    <div>STATUS: REVOKED</div>
                    <div className="text-[10px] text-red-400">NON-COMPLIANT</div>
                  </div>
                </div>
              )}
            </div>

            {/* Revocation Reasons (if revoked) */}
            {(isRevoked || certificateData.eodb_green_channel_status !== 'APPROVED_REMOTE') && (
              <div className="mb-5 p-3.5 bg-red-950/60 border border-red-800 rounded-xl font-mono text-xs text-red-200">
                <div className="font-bold text-red-300 mb-1 flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4 text-red-400" />
                  Forensic Grounds for Certificate Revocation:
                </div>
                <ul className="list-disc list-inside space-y-0.5 text-[11px] text-red-200">
                  {certificateData.revocation_reasons?.map((reason: string, i: number) => (
                    <li key={i}>{reason}</li>
                  ))}
                  {isTampered && <li>Cryptographic Hash Chain Tamper Fraud Detected via Server Memory Inspection</li>}
                  {telemetry?.pressure_bar > 15.0 && <li>Exceeded Statutory MAWP 15.0 bar (Current: {telemetry.pressure_bar.toFixed(2)} bar)</li>}
                </ul>
              </div>
            )}

            {/* Registered Details Two-Column Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono mb-5">
              <div className="p-3.5 rounded-xl bg-gray-900/80 border border-gray-800 space-y-2">
                <div className="text-gray-400 text-[10px] uppercase font-bold tracking-wider text-emerald-400">
                  Boiler Installation &amp; Ownership
                </div>
                <div><span className="text-gray-400">Registration ID:</span> <strong className="text-white">{certificateData.boiler_registration_id}</strong></div>
                <div><span className="text-gray-400">Owner MSME:</span> <span className="text-gray-200">{certificateData.owner_msme_name}</span></div>
                <div><span className="text-gray-400">Location:</span> <span className="text-gray-300 text-[11px]">{certificateData.location}</span></div>
                <div><span className="text-gray-400">Boiler Type:</span> <span className="text-gray-200">{certificateData.boiler_rating?.type}</span></div>
                <div><span className="text-gray-400">Max Allowable Working Pressure (MAWP):</span> <strong className="text-emerald-400">{certificateData.boiler_rating?.mawp_bar} bar</strong></div>
              </div>

              <div className="p-3.5 rounded-xl bg-gray-900/80 border border-gray-800 space-y-2">
                <div className="text-gray-400 text-[10px] uppercase font-bold tracking-wider text-cyan-400">
                  Zero-Trust Telemetry Verification Summary
                </div>
                <div><span className="text-gray-400">Total Verified Packets:</span> <span className="text-white font-bold">{certificateData.telemetry_verification_summary?.total_verified_blocks}</span></div>
                <div><span className="text-gray-400">Zero MAWP Violations:</span> <span className={certificateData.telemetry_verification_summary?.zero_mawp_violations_verified ? 'text-emerald-400' : 'text-red-400 font-bold'}>{certificateData.telemetry_verification_summary?.zero_mawp_violations_verified ? 'VERIFIED (0 Overpressure Events)' : 'FAILED (>15.0 bar recorded)'}</span></div>
                <div><span className="text-gray-400">ECDSA P-256 Public Key:</span> <span className="text-emerald-400 font-mono text-[10px] break-all">{certificateData.telemetry_verification_summary?.ecdsa_public_key_fingerprint}</span></div>
                <div><span className="text-gray-400">Chain Tip Hash:</span> <span className="text-cyan-300 font-mono text-[10px] break-all">{certificateData.telemetry_verification_summary?.sha256_chain_tip_hash}</span></div>
                <div><span className="text-gray-400">EODB Queue Reduction:</span> <span className="text-gray-200 font-bold text-[10px]">{certificateData.telemetry_verification_summary?.inspection_delay_reduction}</span></div>
              </div>
            </div>

            {/* Cryptographic Hardware Seal Footer */}
            <div className="pt-4 border-t border-gray-800 text-xs font-mono flex flex-wrap items-center justify-between gap-3">
              <div>
                <span className="text-gray-500 block text-[10px]">DIGITAL IBR SIGNATURE (SECP256R1 / HARDWARE ROOTED)</span>
                <span className="text-cyan-400 text-[10px] break-all">
                  {certificateData.ecdsa_digital_signature_hex || 'ECDSA_P256_VERIFIED'}
                </span>
              </div>
              <button
                onClick={() => setShowCertModal(false)}
                className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-black font-bold rounded-lg text-xs font-mono transition-all"
              >
                Close Certificate
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};


