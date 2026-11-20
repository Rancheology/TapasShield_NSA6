import React, { useState, useEffect, useRef } from 'react';
import { 
  Presentation, 
  ChevronLeft, 
  ChevronRight, 
  Download, 
  Printer, 
  Maximize2, 
  Minimize2, 
  Play, 
  Pause, 
  ShieldCheck, 
  Cpu, 
  Activity, 
  Zap, 
  FileCheck, 
  CheckCircle2, 
  Flame, 
  TrendingUp, 
  Users, 
  Scale, 
  HelpCircle 
} from 'lucide-react';

interface SlideData {
  id: number;
  kicker: string;
  title: string;
  rubric: string;
  rubricColor: string;
  category: string;
}

const SLIDES: SlideData[] = [
  {
    id: 1,
    kicker: "NATIONAL STARTUP AWARDS 6.0 | STUDENT INNOVATOR (IV: 18+ YRS)",
    title: "TapasShield: SIL-2 Edge Hardware Node & Dual-Access Statutory e-Register",
    rubric: "EODB GRAND CHALLENGE",
    rubricColor: "text-amber-400 border-amber-500/40 bg-amber-500/10",
    category: "Executive Cockpit"
  },
  {
    id: 2,
    kicker: "PROBLEM DEFINITION & NATIONAL SIGNIFICANCE",
    title: "India's Industrial Boiler Crisis: Explosions, Paper Fraud & Fuel Bleed",
    rubric: "1,00,000+ BOILERS AT RISK",
    rubricColor: "text-rose-400 border-rose-500/40 bg-rose-500/10",
    category: "Problem Definition"
  },
  {
    id: 3,
    kicker: "STATE-OF-THE-ART BENCHMARKING",
    title: "The Innovation Gap: Why Traditional Boiler Loggers Fail Industrial Needs",
    rubric: "COMPETITIVE ADVANTAGE",
    rubricColor: "text-sky-400 border-sky-500/40 bg-sky-500/10",
    category: "Competitive Matrix"
  },
  {
    id: 4,
    kicker: "EODB MANDATE: SHARED STATUTORY REGISTER",
    title: "Dual-Access Online Register: MSME Factory Cockpit & Inspector Portal",
    rubric: "EODB DUAL COCKPIT",
    rubricColor: "text-emerald-400 border-emerald-500/40 bg-emerald-500/10",
    category: "Shared Online Register"
  },
  {
    id: 5,
    kicker: "HARDWARE-ROOTED CRYPTOGRAPHY & TRUST LEDGER",
    title: "Silicon-Rooted Anti-Falsification: From Sensor Shunt to Inspector Register",
    rubric: "HARDWARE SECURITY",
    rubricColor: "text-amber-400 border-amber-500/40 bg-amber-500/10",
    category: "Hardware Security"
  },
  {
    id: 6,
    kicker: "PREDICTIVE MAINTENANCE & THERMODYNAMICS",
    title: "Physics-Informed Scale Prediction & IS 8753 Real-Time Fuel Optimization",
    rubric: "PREDICTIVE ROI",
    rubricColor: "text-emerald-400 border-emerald-500/40 bg-emerald-500/10",
    category: "Predictive ROI"
  },
  {
    id: 7,
    kicker: "ANALOG FRONT-END & SIL-2 HARDWARE ARCHITECTURE",
    title: "Non-Intrusive 4–20 mA Precision Analog Front-End & Sensor Interception",
    rubric: "SIL-2 HARDWARE",
    rubricColor: "text-sky-400 border-sky-500/40 bg-sky-500/10",
    category: "SIL-2 Hardware"
  },
  {
    id: 8,
    kicker: "VERIFIED SIL-2 PROTOTYPE & JURY AUDIT GUIDE",
    title: "Verified KiCad 8 Hardware, SIL Test Suite & Live Jury Walkthrough",
    rubric: "100% GREEN VERIFIED",
    rubricColor: "text-emerald-400 border-emerald-500/40 bg-emerald-500/10",
    category: "Engineering Verification"
  },
  {
    id: 9,
    kicker: "COMMERCIALIZATION & UNIT ECONOMICS",
    title: "₹5,420 BOM Unit Economics & Phased National Scale Strategy",
    rubric: "SCALE & ECONOMICS",
    rubricColor: "text-amber-400 border-amber-500/40 bg-amber-500/10",
    category: "Scale & Economics"
  },
  {
    id: 10,
    kicker: "INCLUSIVITY, WORKER SAFETY & ENVIRONMENTAL IMPACT",
    title: "Empowering Blue-Collar Boiler Operators & Driving Industrial Decarbonization",
    rubric: "VIKSIT BHARAT @ 2047",
    rubricColor: "text-sky-400 border-sky-500/40 bg-sky-500/10",
    category: "Viksit Bharat @ 2047"
  },
  {
    id: 11,
    kicker: "VISUAL GUIDE 01 • HARDWARE INSPECTION",
    title: "All-Around Look: TapasShield SIL-2 Edge Node PCB",
    rubric: "360° TEARDOWN",
    rubricColor: "text-sky-400 border-sky-500/40 bg-sky-500/10",
    category: "Hardware Teardown"
  },
  {
    id: 12,
    kicker: "VISUAL GUIDE 02 • VISUAL WIRING MAP",
    title: "Visual Connectivity Guide: Direct Boiler-to-PCB Hookup",
    rubric: "PLUG & PLAY",
    rubricColor: "text-emerald-400 border-emerald-500/40 bg-emerald-500/10",
    category: "Wiring Map"
  },
  {
    id: 13,
    kicker: "VISUAL GUIDE 03 • MSME FACTORY INTERFACE",
    title: "Full-Screen Tour: Business Plant SCADA & Predictive ROI Portal",
    rubric: "BUSINESS VIEW",
    rubricColor: "text-sky-400 border-sky-500/40 bg-sky-500/10",
    category: "Business Portal"
  },
  {
    id: 14,
    kicker: "VISUAL GUIDE 04 • GOVERNMENT E-REGISTER INTERFACE",
    title: "Full-Screen Tour: State Inspectorate & Central Govt (DPIIT) e-Register",
    rubric: "INSPECTOR VIEW",
    rubricColor: "text-emerald-400 border-emerald-500/40 bg-emerald-500/10",
    category: "Govt e-Register"
  },
  {
    id: 15,
    kicker: "VISUAL GUIDE 05 • QUICK-START & OPEN VERIFICATION PACKAGE",
    title: "4-Step Visual Quick-Start + Full Code & KiCad 3D Hardware Files",
    rubric: "QUICK-START",
    rubricColor: "text-purple-400 border-purple-500/40 bg-purple-500/10",
    category: "Quick-Start & GitHub"
  }
];

export const PitchDeckView: React.FC = () => {
  const [currentSlide, setCurrentSlide] = useState<number>(1);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [viewMode, setViewMode] = useState<'rendered' | 'interactive'>('rendered');
  const playerRef = useRef<HTMLDivElement>(null);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
        e.preventDefault();
        setCurrentSlide(prev => (prev < 15 ? prev + 1 : 1));
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        setCurrentSlide(prev => (prev > 1 ? prev - 1 : 15));
      } else if (e.key === 'Home') {
        e.preventDefault();
        setCurrentSlide(1);
      } else if (e.key === 'End') {
        e.preventDefault();
        setCurrentSlide(14);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Slideshow auto-advance
  useEffect(() => {
    let timer: any;
    if (isPlaying) {
      timer = setInterval(() => {
        setCurrentSlide(prev => (prev < 15 ? prev + 1 : 1));
      }, 8000);
    }
    return () => clearInterval(timer);
  }, [isPlaying]);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      playerRef.current?.requestFullscreen?.();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen?.();
      setIsFullscreen(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  const slide = SLIDES[currentSlide - 1];

  return (
    <div className="space-y-6">
      {/* 1. Header Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 bg-[#1E293B]/80 rounded-2xl border border-gray-700/80 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
            <Presentation className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              National Startup Awards 6.0 Official Pitch Deck
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                14-SLIDE EXPANDED JURY EDITION
              </span>
            </h2>
            <p className="text-xs text-gray-400">
              Interactive 16:9 Widescreen Presentation &bull; Slide {currentSlide} of 14 &bull; {slide.category}
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Mode Switcher */}
          <div className="flex items-center bg-gray-900 border border-gray-700 rounded-lg p-0.5">
            <button
              onClick={() => setViewMode('rendered')}
              className={`px-2.5 py-1 rounded text-xs font-semibold transition-all ${
                viewMode === 'rendered'
                  ? 'bg-sky-500 text-black font-bold shadow'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              16:9 Retina Slides
            </button>
            <button
              onClick={() => setViewMode('interactive')}
              className={`px-2.5 py-1 rounded text-xs font-semibold transition-all ${
                viewMode === 'interactive'
                  ? 'bg-sky-500 text-black font-bold shadow'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Interactive Mode
            </button>
          </div>

          {/* Slideshow Play/Pause */}
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all border ${
              isPlaying
                ? 'bg-amber-600 text-black border-amber-500 shadow-md shadow-amber-900/30'
                : 'bg-gray-800 text-gray-300 border-gray-700 hover:text-white hover:bg-gray-750'
            }`}
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            <span>{isPlaying ? 'Pause' : 'Auto Play'}</span>
          </button>

          {/* Download Final .PPTX */}
          <a
            href="/deck/TapasShield_NSA6_Final_Deck.pptx"
            download="TapasShield_NSA6_Final_Deck.pptx"
            className="px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 bg-emerald-600 text-black border border-emerald-500 hover:bg-emerald-500 transition-all shadow-md shadow-emerald-900/30"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Deck .PPTX (4.3 MB)</span>
          </a>

          {/* Download Vector Master PDF */}
          <a
            href="/deck/TapasShield_NSA6_Final_Deck.pdf"
            download="TapasShield_NSA6_Final_Deck.pdf"
            className="px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 bg-sky-600 text-black border border-sky-500 hover:bg-sky-500 transition-all shadow-md shadow-sky-900/30"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Master .PDF (4.3 MB)</span>
          </a>

          {/* Download Standalone Visual User Guide PDF */}
          <a
            href="/deck/TapasShield_Visual_User_Guide.pdf"
            download="TapasShield_Visual_User_Guide.pdf"
            className="px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 bg-purple-600 text-white border border-purple-500 hover:bg-purple-500 transition-all shadow-md shadow-purple-900/30"
          >
            <Download className="w-3.5 h-3.5" />
            <span>User Guide .PDF (1.6 MB)</span>
          </a>

          {/* Fullscreen Toggle */}
          <button
            onClick={toggleFullscreen}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-all border border-gray-700"
            title="Toggle Fullscreen"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* 2. Main 16:9 Presentation Frame */}
      <div 
        ref={playerRef}
        className="relative w-full aspect-[16/9] max-h-[860px] bg-[#090D16] rounded-2xl border border-gray-800 shadow-2xl overflow-hidden flex flex-col justify-between"
      >
        {viewMode === 'rendered' ? (
          <div className="relative w-full h-full flex flex-col justify-between p-2 sm:p-4 bg-black">
            <div className="relative w-full h-full flex items-center justify-center overflow-hidden rounded-xl">
              <img
                src={`/deck/slide_${String(currentSlide).padStart(2, '0')}.png`}
                alt={`TapasShield NSA 6.0 Slide ${currentSlide}`}
                className="w-full h-full object-contain"
              />
            </div>
            
            {/* Quick Floating Navigation Bar */}
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-4 px-4 py-2 bg-[#090E17]/90 backdrop-blur-md border border-gray-700/80 rounded-full shadow-2xl z-20">
              <button
                onClick={() => setCurrentSlide(prev => (prev > 1 ? prev - 1 : 15))}
                className="p-1.5 rounded-full hover:bg-gray-800 text-gray-300 hover:text-white transition-all"
                title="Previous Slide"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="font-mono text-xs font-bold text-emerald-400">
                SLIDE {String(currentSlide).padStart(2, '0')} / 15
              </span>
              <button
                onClick={() => setCurrentSlide(prev => (prev < 15 ? prev + 1 : 1))}
                className="p-1.5 rounded-full hover:bg-gray-800 text-gray-300 hover:text-white transition-all"
                title="Next Slide"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        ) : (
          <div className="flex flex-col justify-between h-full p-6 sm:p-8">
            {/* Top Header Section */}
            <div className="flex items-start justify-between gap-4 border-b border-gray-800/80 pb-3">
              <div className="space-y-1 max-w-[80%]">
                <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-md bg-[#1E293B] border border-emerald-500/40 text-[10px] font-bold text-emerald-400">
                  <ShieldCheck className="w-3 h-3" />
                  <span>{slide.kicker}</span>
                </div>
                <h1 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                  {slide.title}
                </h1>
              </div>
              <div className={`px-3 py-1.5 rounded-xl border text-xs font-black tracking-wide ${slide.rubricColor}`}>
                {slide.rubric}
              </div>
            </div>

            {/* Dynamic Slide Body (Slides 1 to 14) */}
            <div className="flex-1 my-3 overflow-hidden">
              {currentSlide === 1 && <Slide1View />}
              {currentSlide === 2 && <Slide2View />}
              {currentSlide === 3 && <Slide3View />}
              {currentSlide === 4 && <Slide4View />}
              {currentSlide === 5 && <Slide5View />}
              {currentSlide === 6 && <Slide6View />}
              {currentSlide === 7 && <Slide7View />}
              {currentSlide === 8 && <Slide8View />}
              {currentSlide === 9 && <Slide9View />}
              {currentSlide === 10 && <Slide10View />}
              {currentSlide === 11 && <Slide11View />}
              {currentSlide === 12 && <Slide12View />}
              {currentSlide === 13 && <Slide13View />}
              {currentSlide === 14 && <Slide14View />}
              {currentSlide === 15 && <Slide15View />}
            </div>

            {/* Bottom Footer Section */}
            <div className="flex items-center justify-between border-t border-gray-800/80 pt-2.5 text-[10px] text-gray-500">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-gray-400">TapasShield IIoT</span>
                <span>&bull;</span>
                <span>India EODB Grand Challenge &amp; National Startup Awards 6.0</span>
                <span>&bull;</span>
                <span>Compliance: IBR 1950 (2026 Rev) &amp; IEC 61508 SIL-2</span>
              </div>

              <div className="flex items-center gap-3">
                <span className="font-mono text-emerald-400 font-bold">
                  SLIDE {String(currentSlide).padStart(2, '0')} / 15
                </span>
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => setCurrentSlide(prev => (prev > 1 ? prev - 1 : 15))}
                    className="p-1 rounded hover:bg-gray-800 text-gray-400 hover:text-white transition-all"
                    title="Previous Slide"
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setCurrentSlide(prev => (prev < 15 ? prev + 1 : 1))}
                    className="p-1 rounded hover:bg-gray-800 text-gray-400 hover:text-white transition-all"
                    title="Next Slide"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 3. Thumbnail Navigator Strip (14 Slides) */}
      <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 xl:grid-cols-15 gap-2">
        {SLIDES.map(s => {
          const isActive = s.id === currentSlide;
          return (
            <button
              key={s.id}
              onClick={() => setCurrentSlide(s.id)}
              className={`text-left p-2 rounded-xl border transition-all flex flex-col justify-between h-20 ${
                isActive
                  ? 'bg-emerald-950/40 border-emerald-500 ring-2 ring-emerald-500/30'
                  : 'bg-[#131D31]/80 border-gray-800 hover:border-gray-700 hover:bg-[#1E293B]/60'
              }`}
            >
              <div className="flex items-center justify-between w-full">
                <span className={`text-[10px] font-mono font-bold ${isActive ? 'text-emerald-400' : 'text-gray-400'}`}>
                  #{String(s.id).padStart(2, '0')}
                </span>
                <span className={`w-1.5 h-1.5 rounded-full ${isActive ? 'bg-emerald-400' : 'bg-gray-700'}`} />
              </div>
              <p className={`text-[10.5px] font-semibold line-clamp-2 leading-tight ${isActive ? 'text-white' : 'text-gray-300'}`}>
                {s.category}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
};

/* =========================================================================
   INDIVIDUAL SLIDE RENDERERS
   ========================================================================= */

// Slide 1: Executive Title & Mission Cockpit
const Slide1View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-5 h-full items-center">
    <div className="md:col-span-6 flex flex-col justify-between h-full space-y-4">
      <div className="p-4 rounded-xl bg-[#131D31] border border-sky-500/40 space-y-2.5">
        <h3 className="text-sm font-bold text-sky-400 uppercase tracking-wide">
          Solving India's Industrial Boiler Safety &amp; Compliance Crisis
        </h3>
        <p className="text-xs text-gray-200 leading-relaxed">
          TapasShield unites non-intrusive 4–20 mA loop sniffing, silicon cryptography, and thermodynamic predictive digital twins into a Shared Secure Online Register accessible by MSME plant operators and State/Central Government inspecting authorities.
        </p>
        <div className="space-y-1.5 pt-1 text-[11px]">
          <div className="flex items-start gap-1.5">
            <span className="text-emerald-400 font-bold">&bull; Non-Intrusive Edge Node:</span>
            <span className="text-gray-300">Installs in &lt;45 minutes across 5 loops without cutting, welding, or IBR shutdown.</span>
          </div>
          <div className="flex items-start gap-1.5">
            <span className="text-emerald-400 font-bold">&bull; Dual-Access e-Register:</span>
            <span className="text-gray-300">Simultaneously powers MSME fuel ROI and State/Central Govt (DPIIT) continuous audit.</span>
          </div>
          <div className="flex items-start gap-1.5">
            <span className="text-emerald-400 font-bold">&bull; Hardware-Rooted Trust:</span>
            <span className="text-gray-300">ATECC608B ECDSA NIST P-256 signatures &amp; SHA-256 hash chains guarantee non-repudiation.</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2.5">
        <div className="p-3 rounded-xl bg-[#131D31] border border-emerald-500/40 text-center">
          <div className="text-lg font-black text-emerald-400">&lt; 45 Mins</div>
          <div className="text-[10px] font-bold text-white uppercase">Fast Retrofit</div>
          <div className="text-[9px] text-gray-400">5x 4-20mA Loops</div>
        </div>
        <div className="p-3 rounded-xl bg-[#131D31] border border-sky-500/40 text-center">
          <div className="text-lg font-black text-sky-400">0-Sec EODB</div>
          <div className="text-[10px] font-bold text-white uppercase">Dual e-Register</div>
          <div className="text-[9px] text-gray-400">State + Central DPIIT</div>
        </div>
        <div className="p-3 rounded-xl bg-[#131D31] border border-amber-500/40 text-center">
          <div className="text-lg font-black text-amber-400">₹4.65L/yr</div>
          <div className="text-[10px] font-bold text-white uppercase">Net Fuel Saved</div>
          <div className="text-[9px] text-gray-400">IS 8753 Digital Twin</div>
        </div>
      </div>
    </div>

    <div className="md:col-span-6 h-full p-2.5 rounded-xl bg-[#131D31] border border-emerald-500/40 flex flex-col justify-between">
      <div className="text-xs font-bold text-emerald-400 flex items-center justify-between pb-1.5 px-1">
        <span>Live Platform Hero View (Business SCADA + Govt Register Sync)</span>
        <span className="text-[10px] text-gray-400">http://localhost:8000</span>
      </div>
      <div className="flex-1 flex items-center justify-center overflow-hidden rounded-lg bg-black/40">
        <img 
          src="/deck/screenshot_hero_split.png" 
          alt="TapasShield Live Hero Split Screen View" 
          className="w-full h-full object-contain drop-shadow-xl"
        />
      </div>
      <p className="text-[9.5px] text-gray-400 pt-1 text-center">
        Verified 1 Hz Telemetry &bull; IAPWS-IF97 Physics Engine &bull; ATECC608B Hardware Cryptographic Ledger
      </p>
    </div>
  </div>
);

// Slide 2: The Core Problem
const Slide2View = () => (
  <div className="flex flex-col justify-between h-full space-y-3">
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
      <div className="p-3.5 rounded-xl bg-[#131D31] border border-rose-500/40 space-y-2">
        <div className="text-[10px] font-bold text-rose-400 uppercase">[CATASTROPHIC RISK]</div>
        <h4 className="text-xs font-bold text-white">Boiler Explosions</h4>
        <ul className="text-[10px] text-gray-300 space-y-1.5">
          <li>&bull; Overpressure (&gt;MAWP) and low-water starvation (&lt;25%) cause fatal industrial boiler explosions annually.</li>
          <li>&bull; Mechanical gauges and sight glasses fail silently from sediment buildup without remote regulatory alerting.</li>
          <li>&bull; Calcified safety valves stick, leaving operators blind during runaway thermal excursions.</li>
        </ul>
        <div className="text-[9.5px] font-bold text-rose-400 pt-1">★ 100% PREVENTABLE DISASTERS</div>
      </div>

      <div className="p-3.5 rounded-xl bg-[#131D31] border border-amber-500/40 space-y-2">
        <div className="text-[10px] font-bold text-amber-400 uppercase">[EODB BOTTLENECK]</div>
        <h4 className="text-xs font-bold text-white">Manual Paperwork &amp; Fraud</h4>
        <ul className="text-[10px] text-gray-300 space-y-1.5">
          <li>&bull; 1,00,000+ registered boilers rely on paper logbooks or isolated USB loggers without audit trails.</li>
          <li>&bull; Mandatory annual IBR inspections require physical inspector visits, delaying factory clearances by weeks.</li>
          <li>&bull; Operators clamp fixed resistors to transmitters or overwrite logs to mask statutory violations.</li>
        </ul>
        <div className="text-[9.5px] font-bold text-amber-400 pt-1">★ 14-DAY QUEUES &amp; BRIBERY TOUCHPOINTS</div>
      </div>

      <div className="p-3.5 rounded-xl bg-[#131D31] border border-sky-500/40 space-y-2">
        <div className="text-[10px] font-bold text-sky-400 uppercase">[MSME PROFIT BLEED]</div>
        <h4 className="text-xs font-bold text-white">Hidden Fuel Waste from Scale</h4>
        <ul className="text-[10px] text-gray-300 space-y-1.5">
          <li>&bull; Untreated feedwater chemistry deposits calcium carbonate (CaCO3) scale on firetubes.</li>
          <li>&bull; Just 1.5 mm of scale raises flue gas exit temp by +58°C, bleeding 8% to 15% of coal/gas fuel.</li>
          <li>&bull; Average MSME loses ₹3.5 to ₹6.0 Lakh/yr in preventable fuel waste due to delayed descaling.</li>
        </ul>
        <div className="text-[9.5px] font-bold text-sky-400 pt-1">★ ₹4.65 LAKH/YR FUEL WASTED / BOILER</div>
      </div>
    </div>

    <div className="p-3 rounded-xl bg-[#1E293B] border border-emerald-500/40">
      <div className="text-xs font-bold text-emerald-400 mb-1.5">
        STATUTORY GRAND CHALLENGE MANDATE: 5-CHANNEL REGULATORY COMPLIANCE MATRIX
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-[10px]">
        <div className="p-2 rounded bg-black/30 border border-gray-700">
          <span className="font-bold text-sky-400">1. PT-101 Drum Press</span>
          <p className="text-gray-300 text-[9px]">0–25 bar MAWP Overpressure Guard</p>
        </div>
        <div className="p-2 rounded bg-black/30 border border-gray-700">
          <span className="font-bold text-sky-400">2. TT-101 Steam Temp</span>
          <p className="text-gray-300 text-[9px]">0–350°C Saturation Reference</p>
        </div>
        <div className="p-2 rounded bg-black/30 border border-gray-700">
          <span className="font-bold text-sky-400">3. TT-102 Stack Temp</span>
          <p className="text-gray-300 text-[9px]">0–500°C Scale &amp; Efficiency Drift</p>
        </div>
        <div className="p-2 rounded bg-black/30 border border-gray-700">
          <span className="font-bold text-sky-400">4. FT-101 Steam Flow</span>
          <p className="text-gray-300 text-[9px]">0–5000 kg/hr Mass Balance</p>
        </div>
        <div className="p-2 rounded bg-black/30 border border-gray-700">
          <span className="font-bold text-sky-400">5. AT-101 Water TDS</span>
          <p className="text-gray-300 text-[9px]">0–5000 ppm Chemistry &amp; Level</p>
        </div>
      </div>
    </div>
  </div>
);


// Slide 3: Industrial Retrofit Deployment Diagram
const Slide3View = () => (
  <div className="flex flex-col justify-between h-full space-y-3">
    <div className="flex-1 flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-emerald-500/40 overflow-hidden">
      <img 
        src="/deck/diagram_industrial_deployment.png" 
        alt="Industrial Boiler Physical Deployment Topology" 
        className="w-full h-full max-h-[340px] object-contain drop-shadow-xl"
      />
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-[10.5px]">
      <div className="p-2.5 rounded-xl bg-[#1E293B] border border-emerald-500/40">
        <div className="text-[10px] font-bold text-emerald-400 uppercase">WHERE INSTALLED</div>
        <h4 className="font-bold text-white text-xs">Inside Boiler Room Electrical BMS</h4>
        <p className="text-gray-300 text-[9.5px]">Clips onto standard 35mm DIN-rail in IP66 enclosure adjacent to burner controller.</p>
      </div>
      <div className="p-2.5 rounded-xl bg-[#1E293B] border border-sky-500/40">
        <div className="text-[10px] font-bold text-sky-400 uppercase">HOW CONNECTED</div>
        <h4 className="font-bold text-white text-xs">Non-Intrusive Series Pass-Through</h4>
        <p className="text-gray-300 text-[9.5px]">Passes 4–20 mA signals over 150Ω precision shunts (3.0V drop). Zero piping cuts or welding!</p>
      </div>
      <div className="p-2.5 rounded-xl bg-[#1E293B] border border-amber-500/40">
        <div className="text-[10px] font-bold text-amber-400 uppercase">ZERO PLANT DOWNTIME</div>
        <h4 className="font-bold text-white text-xs">Installed in &lt;45 Minutes</h4>
        <p className="text-gray-300 text-[9.5px]">Requires zero boiler shutdown, zero hydro-tests, and zero IBR de-rating.</p>
      </div>
    </div>
  </div>
);


// Slide 4: 4-20mA AFE Architecture & Annotated 3D PCB
const Slide4View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-7 h-full flex flex-col justify-between p-2 rounded-xl bg-[#131D31] border border-emerald-500/40">
      <div className="text-xs font-bold text-emerald-400 pb-1 px-1">
        KiCad 8 Verified 120×90mm SIL-2 Hardware Engine (Annotated 3D View)
      </div>
      <div className="flex-1 flex items-center justify-center overflow-hidden rounded-lg bg-black/40">
        <img 
          src="/deck/diagram_pcb_3d_annotated.png" 
          alt="Annotated 3D PCB Diagram" 
          className="w-full h-full max-h-[320px] object-contain drop-shadow-xl"
        />
      </div>
    </div>

    <div className="md:col-span-5 h-full flex flex-col justify-between space-y-2">
      <div className="flex-1 flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-sky-500/40 overflow-hidden">
        <img 
          src="/deck/chart_afe_loop_calibration.png" 
          alt="AFE Loop Calibration Curve" 
          className="w-full h-full max-h-[160px] object-contain drop-shadow-md"
        />
      </div>
      <div className="flex-1 flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-amber-500/40 overflow-hidden">
        <img 
          src="/deck/crop_loop_current_monitor.png" 
          alt="Industrial 4-20mA Loop Inspector" 
          className="w-full h-full max-h-[160px] object-contain drop-shadow-md"
        />
      </div>
    </div>
  </div>
);


// Slide 5: Silicon-Rooted Anti-Falsification & Tamper Detection
const Slide5View = () => (
  <div className="flex flex-col justify-between h-full space-y-2.5">
    <div className="flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-sky-500/40">
      <img 
        src="/deck/diagram_crypto_pipeline.png" 
        alt="Cryptographic Trust Pipeline" 
        className="w-full max-h-[130px] object-contain drop-shadow-lg"
      />
    </div>

    <div className="grid grid-cols-1 md:grid-cols-12 gap-3 flex-1 overflow-hidden">
      <div className="md:col-span-7 flex flex-col justify-between p-2 rounded-xl bg-[#131D31] border border-rose-500/40">
        <div className="text-[10px] font-bold text-rose-400 pb-1">
          Forensic Tamper Detection: Real-time Database Modification Trap
        </div>
        <div className="flex-1 flex items-center justify-center overflow-hidden rounded-lg bg-black/40">
          <img 
            src="/deck/screenshot_forensic_tamper_alert.png" 
            alt="Forensic Audit Tamper Alert" 
            className="w-full h-full max-h-[160px] object-contain drop-shadow-md"
          />
        </div>
      </div>

      <div className="md:col-span-5 flex flex-col justify-between p-2 rounded-xl bg-[#131D31] border border-emerald-500/40">
        <div className="text-[10px] font-bold text-emerald-400 pb-1">
          Hardware-Rooted SHA-256 Hash Chain &amp; ECDSA Signatures
        </div>
        <div className="flex-1 flex items-center justify-center overflow-hidden rounded-lg bg-black/40">
          <img 
            src="/deck/crop_crypto_hash_chain.png" 
            alt="Cryptographic Ledger Hash Chain" 
            className="w-full h-full max-h-[160px] object-contain drop-shadow-md"
          />
        </div>
      </div>
    </div>
  </div>
);


// Slide 6: Predictive Maintenance & Thermodynamics
const Slide6View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-6 flex flex-col justify-between h-full space-y-2.5">
      <div className="flex-1 flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-sky-500/40 overflow-hidden">
        <img 
          src="/deck/crop_pid_schematic_twin.png" 
          alt="P&amp;ID Digital Twin" 
          className="w-full h-full max-h-[180px] object-contain drop-shadow-md"
        />
      </div>
      <div className="p-3 rounded-xl bg-[#1E293B] border border-emerald-500/40 text-[10px] space-y-1">
        <div className="font-bold text-emerald-400 text-xs">THERMODYNAMIC PHYSICS &amp; PREDICTIVE ROI</div>
        <p className="text-gray-300">
          <strong className="text-white">&bull; IAPWS-IF97 Physics Anchor:</strong> Cross-checks |T_steam - T_sat(P)| &le; 5°C to defeat synthetic resistor clamping.
        </p>
        <p className="text-gray-300">
          <strong className="text-white">&bull; Descaling Countdown:</strong> Predicts waterside scale thickness; alerts 14 days before fuel waste spikes.
        </p>
        <p className="text-gray-300">
          <strong className="text-white">&bull; Cycles of Concentration (CoC):</strong> Automates blowdown TDS schedule, preventing tube rupture.
        </p>
      </div>
    </div>

    <div className="md:col-span-6 h-full flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-amber-500/40 overflow-hidden">
      <img 
        src="/deck/chart_thermodynamic_drift.png" 
        alt="Scale Thickness vs Flue Drift &amp; IS 8753 Efficiency" 
        className="w-full h-full max-h-[320px] object-contain drop-shadow-md"
      />
    </div>
  </div>
);

// Slide 7: Shared Online Register (MSME Cockpit & State/Central Govt e-Register)
const Slide7View = () => (
  <div className="flex flex-col justify-between h-full space-y-2.5">
    <div className="flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-emerald-500/40 overflow-hidden">
      <img 
        src="/deck/screenshot_hero_split.png" 
        alt="Dual Split-Screen Hero View" 
        className="w-full max-h-[170px] object-contain drop-shadow-xl"
      />
    </div>

    <div className="grid grid-cols-1 md:grid-cols-12 gap-3 flex-1 overflow-hidden">
      <div className="md:col-span-7 flex flex-col justify-between p-2 rounded-xl bg-[#131D31] border border-sky-500/40">
        <div className="text-[10px] font-bold text-sky-400 pb-1">
          DPIIT Central Boilers Board National Industrial Cluster Grid
        </div>
        <div className="flex-1 flex items-center justify-center overflow-hidden rounded-lg bg-black/40">
          <img 
            src="/deck/crop_national_cluster_grid.png" 
            alt="National Cluster Grid" 
            className="w-full h-full max-h-[130px] object-contain drop-shadow-md"
          />
        </div>
      </div>

      <div className="md:col-span-5 p-3 rounded-xl bg-[#1E293B] border border-indigo-500/40 flex flex-col justify-between text-[10px]">
        <div className="font-bold text-indigo-400 text-xs">SHARED ONLINE REGISTER: 3 TIERS</div>
        <div className="space-y-1">
          <p className="text-gray-300">
            <strong className="text-emerald-400">Tier 1: MSME Operator:</strong> Real-time SCADA, fuel loss ticker (₹/hr), descaling RUL.
          </p>
          <p className="text-gray-300">
            <strong className="text-sky-400">Tier 2: State Directorate:</strong> Continuous remote IBR Rule 392 audit, 0-sec auto-renewal.
          </p>
          <p className="text-gray-300">
            <strong className="text-amber-400">Tier 3: Central Boilers Board:</strong> Multi-state national safety grid with tamper detection.
          </p>
        </div>
        <div className="p-1 rounded bg-black/30 border border-gray-700 text-center text-[9px] text-gray-400">
          14-Day Queue &rarr; 0 Sec Real-Time Continuous Audit
        </div>
      </div>
    </div>
  </div>
);


// Slide 8: Statutory Green-Channel Auto-Renewal (IBR Form-VI)
const Slide8View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-6 h-full flex flex-col justify-between p-2 rounded-xl bg-[#131D31] border border-emerald-500/40">
      <div className="text-xs font-bold text-emerald-400 pb-1 px-1">
        Official Digital IBR Form-VI Certificate (State Directorate of Boilers)
      </div>
      <div className="flex-1 flex items-center justify-center overflow-hidden rounded-lg bg-black/40">
        <img 
          src="/deck/crop_form_vi_modal.png" 
          alt="IBR Form-VI Certificate Modal" 
          className="w-full h-full max-h-[320px] object-contain drop-shadow-xl"
        />
      </div>
    </div>

    <div className="md:col-span-6 h-full flex flex-col justify-between space-y-2.5 text-[10.5px]">
      <div className="p-3 rounded-xl bg-[#131D31] border border-emerald-500/40 space-y-1">
        <div className="text-[10px] font-bold text-emerald-400 uppercase">14-DAY QUEUE &rarr; 0 SECONDS</div>
        <h4 className="font-bold text-white text-xs">Automated Green-Channel Certificate Renewal</h4>
        <p className="text-gray-300 text-[9.5px]">
          Boilers maintaining 365 days of continuous verified telemetry with 0 MAWP violations qualify for instant Form-VI renewal.
        </p>
      </div>

      <div className="p-3 rounded-xl bg-[#131D31] border border-sky-500/40 space-y-1">
        <div className="text-[10px] font-bold text-sky-400 uppercase">ELIMINATING RENT-SEEKING</div>
        <h4 className="font-bold text-white text-xs">Zero Manual Bribery Touchpoints</h4>
        <p className="text-gray-300 text-[9.5px]">
          Replaces subjective physical inspector visits with mathematically verifiable cryptographic proofs.
        </p>
      </div>

      <div className="p-3 rounded-xl bg-[#131D31] border border-rose-500/40 space-y-1">
        <div className="text-[10px] font-bold text-rose-400 uppercase">INSTANT STATUTORY REVOCATION</div>
        <h4 className="font-bold text-white text-xs">Zero-Tolerance Safety Enforcement</h4>
        <p className="text-gray-300 text-[9.5px]">
          Any MAWP pressure excursion (&gt;15 bar) or database tamper instantly revokes the Form-VI certificate and alerts authorities.
        </p>
      </div>
    </div>
  </div>
);


// Slide 9: Unit Economics & Scalability
const Slide9View = () => (
  <div className="flex flex-col justify-between h-full space-y-2.5">
    <div className="flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-sky-500/40 overflow-hidden">
      <img 
        src="/deck/chart_bom_and_roi.png" 
        alt="BOM Cost and 12-Month Net Cashflow" 
        className="w-full max-h-[170px] object-contain drop-shadow-lg"
      />
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-[10.5px]">
      <div className="p-3 rounded-xl bg-[#131D31] border border-emerald-500/40 space-y-1">
        <div className="text-[10px] font-bold text-emerald-400 uppercase">[BILL OF MATERIALS]</div>
        <h4 className="font-bold text-white text-xs">42-Component BOM: ₹5,420</h4>
        <ul className="text-gray-300 text-[9px] space-y-0.5">
          <li>&bull; ESP32-S3-WROOM-1: ₹420</li>
          <li>&bull; ATECC608B Crypto Element: ₹95</li>
          <li>&bull; ADS1115 16-bit ADC: ₹180</li>
          <li>&bull; 5x Shunts &amp; TVS Diodes: ₹340</li>
          <li>&bull; IP66 Enclosure, Power &amp; 4G: ₹4,385</li>
          <li className="font-bold text-emerald-400 pt-0.5">Total Edge Kit BOM: ₹5,420 ($65)</li>
        </ul>
      </div>

      <div className="p-3 rounded-xl bg-[#131D31] border border-amber-500/40 space-y-1">
        <div className="text-[10px] font-bold text-amber-400 uppercase">[BUSINESS MODEL]</div>
        <h4 className="font-bold text-white text-xs">Hardware + High-Margin SaaS</h4>
        <ul className="text-gray-300 text-[9px] space-y-0.5">
          <li>&bull; Upfront Kit: ₹9,999 (45% gross margin)</li>
          <li>&bull; Recurring SaaS: ₹999/month per boiler</li>
          <li>&bull; Customer Payback: 4.2 Weeks</li>
          <li className="font-bold text-amber-400 pt-0.5">MSME Year-1 Net ROI: 44x capital outlay</li>
        </ul>
      </div>

      <div className="p-3 rounded-xl bg-[#131D31] border border-sky-500/40 space-y-1">
        <div className="text-[10px] font-bold text-sky-400 uppercase">[SCALE ROADMAP]</div>
        <h4 className="font-bold text-white text-xs">Phased 1,00,000+ Expansion</h4>
        <ul className="text-gray-300 text-[9px] space-y-0.5">
          <li>&bull; Phase 1 (M1–6): 50-boiler pilot in Vellore/Ranipet.</li>
          <li>&bull; Phase 2 (M6–18): Gujarat &amp; Maharashtra belts.</li>
          <li className="font-bold text-sky-400 pt-0.5">Phase 3 (M18–36): 10,000+ units across India.</li>
        </ul>
      </div>
    </div>
  </div>
);


// Slide 10: Live Jury Verification Roadmap
const Slide10View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-6 flex flex-col justify-between h-full space-y-2.5">
      <div className="flex-1 flex items-center justify-center p-2 rounded-xl bg-[#131D31] border border-emerald-500/40 overflow-hidden">
        <img 
          src="/deck/screenshot_hardware_cad_3d.png" 
          alt="KiCad 8 PCB 3D Viewer" 
          className="w-full h-full max-h-[190px] object-contain drop-shadow-xl"
        />
      </div>
      <div className="p-3 rounded-xl bg-[#1E293B] border border-emerald-500/40 space-y-1 text-[10px]">
        <div className="text-xs font-bold text-emerald-400">
          100% Green Verification &amp; Industrial Readiness
        </div>
        <ul className="text-gray-300 text-[9.5px] space-y-0.5">
          <li>&bull; <strong className="text-white">KiCad 8 Formal DRC:</strong> 0 Errors across 42 BOM components (120×90mm 2-layer).</li>
          <li>&bull; <strong className="text-white">Automated Pytest Suite:</strong> 17/17 Passed (100% Green) — Physics, Crypto, EODB Grid.</li>
          <li>&bull; <strong className="text-white">PlatformIO ESP32-S3 Firmware:</strong> 0 Errors — Hardware mbedTLS ECDSA/SHA-256.</li>
        </ul>
      </div>
    </div>

    <div className="md:col-span-6 h-full p-4 rounded-xl bg-[#131D31] border border-sky-500/40 flex flex-col justify-between text-[10.5px]">
      <h3 className="text-xs font-bold text-sky-400 uppercase tracking-wide border-b border-gray-700 pb-1">
        Try These 5 Scenarios Live in the Web Prototype:
      </h3>
      <div className="space-y-1.5 text-gray-200">
        <div className="p-1.5 rounded bg-black/30 border border-gray-800">
          <span className="font-bold text-emerald-400">&bull; Scenario 1: Normal Operation (12.0 bar)</span>
          <p className="text-gray-400 text-[9px]">187.96°C IAPWS saturation match, zero scale, green hash chaining.</p>
        </div>
        <div className="p-1.5 rounded bg-black/30 border border-gray-800">
          <span className="font-bold text-emerald-400">&bull; Scenario 2: Scale Drift (100x Accelerated)</span>
          <p className="text-gray-400 text-[9px]">Stack temp climbs to 285°C, efficiency drops, ₹/hr waste ticks up.</p>
        </div>
        <div className="p-1.5 rounded bg-black/30 border border-gray-800">
          <span className="font-bold text-emerald-400">&bull; Scenario 3: MAWP Overpressure (16.8 bar)</span>
          <p className="text-gray-400 text-[9px]">Trigger 16.8 bar spike; instant emergency alarm &amp; Form-VI revoked.</p>
        </div>
        <div className="p-1.5 rounded bg-black/30 border border-gray-800">
          <span className="font-bold text-emerald-400">&bull; Scenario 4: 0 mA Wire-Cut Attack</span>
          <p className="text-gray-400 text-[9px]">Disconnect sensor loop; verify immediate hardware trap (&lt;3.6 mA).</p>
        </div>
        <div className="p-1.5 rounded bg-black/30 border border-gray-800">
          <span className="font-bold text-emerald-400">&bull; Scenario 5: Resistor Spoof &amp; DB Tamper</span>
          <p className="text-gray-400 text-[9px]">Trigger synthetic spoof &amp; DB tamper; run forensic audit to catch broken hash link.</p>
        </div>
      </div>
    </div>
  </div>
);


// Slide 11: 360° Hardware Teardown
const Slide11View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-7 flex flex-col justify-between h-full space-y-2">
      <div className="flex-1 flex items-center justify-center p-2 rounded-xl bg-[#FAF9F6] border border-gray-300 overflow-hidden relative">
        <img 
          src="/deck/guide_01_pcb_360.png" 
          alt="360° Hardware Teardown" 
          className="w-full h-full object-contain"
        />
      </div>
    </div>
    <div className="md:col-span-5 h-full p-4 rounded-xl bg-[#131D31] border border-sky-500/40 flex flex-col justify-between text-[11px]">
      <div>
        <h3 className="text-xs font-bold text-sky-400 uppercase tracking-wide border-b border-gray-700 pb-1 mb-2">
          SIL-2 Hardware Architecture Highlights:
        </h3>
        <ul className="text-gray-200 space-y-1.5">
          <li>&bull; <strong className="text-white">Pin 01:</strong> 24V DC Plant Bus In with B540C reverse-polarity Schottky guard.</li>
          <li>&bull; <strong className="text-white">Pin 02:</strong> TPS54302 buck converter + AP2112K LDO (24V➔5V➔3.3V).</li>
          <li>&bull; <strong className="text-white">Pin 03:</strong> 5× Phoenix Contact 5.08mm screw blocks + 400W SMAJ28CA TVS.</li>
          <li>&bull; <strong className="text-white">Pin 04:</strong> Texas Instruments ADS1115 16-bit precision delta-sigma ADC.</li>
          <li>&bull; <strong className="text-white">Pin 05:</strong> Microchip ATECC608B hardware crypto root (ECDSA NIST P-256).</li>
          <li>&bull; <strong className="text-white">Pin 06:</strong> ESP32-S3 dual-core 240MHz SoC + physical SW1 enclosure tamper.</li>
        </ul>
      </div>
      <div className="p-2.5 rounded bg-emerald-950/40 border border-emerald-500/40 text-[10px] text-emerald-300">
        ✓ 120×90mm 2-layer FR4 • KiCad 8 DRC: 0 Errors, 0 Unconnected Tracks.
      </div>
    </div>
  </div>
);

// Slide 12: Visual Wiring Map
const Slide12View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-7 flex flex-col justify-between h-full space-y-2">
      <div className="flex-1 flex items-center justify-center p-2 rounded-xl bg-[#FAF9F6] border border-gray-300 overflow-hidden relative">
        <img 
          src="/deck/guide_02_wiring_map.png" 
          alt="Direct Boiler-to-PCB Wiring Map & Industrial 4G Uplink" 
          className="w-full h-full object-contain"
        />
      </div>
    </div>
    <div className="md:col-span-5 h-full p-4 rounded-xl bg-[#131D31] border border-emerald-500/40 flex flex-col justify-between text-[11px]">
      <div>
        <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wide border-b border-gray-700 pb-1 mb-2">
          Full Physical Connectivity &amp; Router Architecture:
        </h3>
        <ul className="text-gray-200 space-y-1.5">
          <li>&bull; <strong className="text-red-400">Power (J1):</strong> 24V DC DIN-Rail SMPS ➔ J1 (<code className="text-red-300">Pin 1: +24V Red</code>, <code className="text-gray-300">Pin 2: GND Black</code>) inside IP65 box.</li>
          <li>&bull; <strong className="text-sky-400">Boiler Loops (J2–J6):</strong> 5 shielded 2-core 4–20 mA cables via PG7 waterproof glands from PT-101, TT-101, TT-102, FT-101 &amp; AT-101 ➔ J2–J6 (<code className="text-sky-300">Pin 1: +Loop</code>, <code className="text-gray-300">Pin 2: GND</code>).</li>
          <li>&bull; <strong className="text-emerald-400">Uplink Hop:</strong> ESP32-S3 Wi-Fi ➔ Mini Industrial 4G Router (mounted beside box) ➔ encrypted mTLS + ECDSA P-256 stream ➔ MSME Portal &amp; Govt e-Register.</li>
        </ul>
      </div>
      <div className="space-y-1 text-[10px]">
        <div className="p-1.5 rounded bg-black/40 border border-gray-800 flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
          <span className="text-gray-300"><strong>LED1 Green Solid:</strong> Signed telemetry active (1 Hz mTLS sync).</span>
        </div>
        <div className="p-1.5 rounded bg-black/40 border border-gray-800 flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-red-400" />
          <span className="text-gray-300"><strong>LED2 Red Blink:</strong> Wire-cut (&lt;3.6 mA) or MAWP &gt;15 bar trip.</span>
        </div>
        <div className="p-1.5 rounded bg-black/40 border border-gray-800 flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-indigo-400" />
          <span className="text-gray-300"><strong>SW1 Lid Switch:</strong> Physical enclosure breach triggers security lockout.</span>
        </div>
      </div>
    </div>
  </div>
);

// Slide 13: Dedicated Full-Screen Business MSME Plant SCADA
const Slide13View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-8 flex flex-col justify-between h-full space-y-2">
      <div className="flex-1 flex items-center justify-center p-1 rounded-xl bg-[#070D1A] border border-gray-700 overflow-hidden relative">
        <img 
          src="/deck/slide_13.png" 
          alt="Business Plant SCADA Portal" 
          className="w-full h-full object-contain"
        />
      </div>
    </div>
    <div className="md:col-span-4 h-full p-4 rounded-xl bg-[#131D31] border border-sky-500/40 flex flex-col justify-between text-[11px]">
      <div>
        <h3 className="text-xs font-bold text-sky-400 uppercase tracking-wide border-b border-gray-700 pb-1 mb-2">
          Business Plant Cockpit:
        </h3>
        <div className="space-y-2">
          <div className="p-2 rounded bg-black/30 border border-gray-800">
            <span className="font-bold text-sky-400">1. Fault Simulator Bar:</span>
            <p className="text-gray-300 text-[10px] mt-0.5">Inject 5 real-world plant faults (Scale drift, Low Water, Tamper) directly for live jury audit.</p>
          </div>
          <div className="p-2 rounded bg-black/30 border border-gray-800">
            <span className="font-bold text-sky-400">2. Physics Digital Twin:</span>
            <p className="text-gray-300 text-[10px] mt-0.5">Animated SVG P&ID displaying live IAPWS-IF97 steam saturation physics & growing CaCO3 scale.</p>
          </div>
          <div className="p-2 rounded bg-black/30 border border-gray-800">
            <span className="font-bold text-amber-400">3. ₹/hr Fuel Waste Loss:</span>
            <p className="text-gray-300 text-[10px] mt-0.5">Real-time coal cost penalty & 14-day advance predictive descaling countdown.</p>
          </div>
          <div className="p-2 rounded bg-black/30 border border-gray-800">
            <span className="font-bold text-emerald-400">4. 4–20 mA Loop Monitor:</span>
            <p className="text-gray-300 text-[10px] mt-0.5">Continuous current & 16-bit ADC count tracking catches sensor drift before failure.</p>
          </div>
        </div>
      </div>
      <div className="p-2 rounded bg-sky-950/40 border border-sky-500/40 text-[10px] text-sky-300">
        Empowers MSME factory attendants with actionable financial & safety insights.
      </div>
    </div>
  </div>
);

// Slide 14: Dedicated Full-Screen State & Central Govt Inspector Portal
const Slide14View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-8 flex flex-col justify-between h-full space-y-2">
      <div className="flex-1 flex items-center justify-center p-1 rounded-xl bg-[#070D1A] border border-gray-700 overflow-hidden relative">
        <img 
          src="/deck/slide_14.png" 
          alt="Govt Inspector Portal" 
          className="w-full h-full object-contain"
        />
      </div>
    </div>
    <div className="md:col-span-4 h-full p-4 rounded-xl bg-[#131D31] border border-emerald-500/40 flex flex-col justify-between text-[11px]">
      <div>
        <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wide border-b border-gray-700 pb-1 mb-2">
          State & Central Govt e-Register:
        </h3>
        <div className="space-y-2">
          <div className="p-2 rounded bg-black/30 border border-gray-800">
            <span className="font-bold text-emerald-400">5. Forensic Audit Toolbar:</span>
            <p className="text-gray-300 text-[10px] mt-0.5">One-click SHA-256 ledger integrity audit & instant digital IBR Form-VI certificate verification.</p>
          </div>
          <div className="p-2 rounded bg-black/30 border border-gray-800">
            <span className="font-bold text-rose-400">6. Broken Hash Alert:</span>
            <p className="text-gray-300 text-[10px] mt-0.5">Instant tamper alert flags modified historical records with crimson Stored vs Recomputed hash breakdown.</p>
          </div>
          <div className="p-2 rounded bg-black/30 border border-gray-800">
            <span className="font-bold text-emerald-400">7. ATECC608B Hardware Trust:</span>
            <p className="text-gray-300 text-[10px] mt-0.5">Silicon private key signs telemetry; tamper triggers instant regulatory hold.</p>
          </div>
          <div className="p-2 rounded bg-black/30 border border-gray-800">
            <span className="font-bold text-cyan-400">8. National Cluster Grid:</span>
            <p className="text-gray-300 text-[10px] mt-0.5">DPIIT national grid tracks live compliance across Tamil Nadu, Gujarat, Maharashtra, Punjab clusters.</p>
          </div>
        </div>
      </div>
      <div className="p-2 rounded bg-emerald-950/40 border border-emerald-500/40 text-[10px] text-emerald-300">
        Fulfills India EODB Grand Challenge: Shared online register eliminating manual inspection queues.
      </div>
    </div>
  </div>
);

// Slide 15: 4-Step Quick-Start + GitHub Repo & QR Code
const Slide15View = () => (
  <div className="grid grid-cols-1 md:grid-cols-12 gap-4 h-full items-center">
    <div className="md:col-span-7 flex flex-col justify-between h-full space-y-2">
      <div className="flex-1 flex items-center justify-center p-1 rounded-xl bg-[#FAF9F6] border border-gray-300 overflow-hidden relative">
        <img 
          src="/deck/slide_15.png" 
          alt="4-Step Quick-Start + GitHub Repo" 
          className="w-full h-full object-contain"
        />
      </div>
    </div>
    <div className="md:col-span-5 h-full p-4 rounded-xl bg-[#131D31] border border-purple-500/40 flex flex-col justify-between text-[11px]">
      <div>
        <h3 className="text-xs font-bold text-purple-400 uppercase tracking-wide border-b border-gray-700 pb-1 mb-2">
          4-Step Quick-Start & Open Repository:
        </h3>
        <div className="grid grid-cols-1 gap-1.5 text-gray-200 text-[10.5px]">
          <div className="flex items-center gap-2 p-1.5 rounded bg-black/30 border border-gray-800">
            <span className="font-mono px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-400 font-bold text-[9px]">STEP 01</span>
            <span><strong>Power & Loops:</strong> Wire 24V DC to J1; tap 5 loops via PG7 glands.</span>
          </div>
          <div className="flex items-center gap-2 p-1.5 rounded bg-black/30 border border-gray-800">
            <span className="font-mono px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold text-[9px]">STEP 02</span>
            <span><strong>Pair 4G:</strong> Connect industrial 4G SIM router; LED1 green confirms mTLS.</span>
          </div>
          <div className="flex items-center gap-2 p-1.5 rounded bg-black/30 border border-gray-800">
            <span className="font-mono px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-400 font-bold text-[9px]">STEP 03</span>
            <span><strong>Test Scenarios:</strong> Switch Business/Govt views or click buttons 1–5.</span>
          </div>
          <div className="flex items-center gap-2 p-1.5 rounded bg-black/30 border border-gray-800">
            <span className="font-mono px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-400 font-bold text-[9px]">STEP 04</span>
            <span><strong>Audit & Cert:</strong> Run SHA-256 forensic audit & issue Form-VI certs.</span>
          </div>
        </div>
      </div>

      {/* GitHub Repo Card */}
      <div className="p-2.5 rounded-xl bg-[#090E17] border border-emerald-500/50 space-y-1.5">
        <div className="text-[10px] font-mono font-bold text-emerald-400 uppercase">
          100% REPRODUCIBLE OPEN SOURCE CODE
        </div>
        <p className="text-[10px] text-gray-300">
          FastAPI + React portal, PlatformIO ESP32-S3 firmware, KiCad 8 PCB & 3D models.
        </p>
        <a 
          href="https://github.com/Rancheology/TapasShield_NSA6" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="font-mono text-[10.5px] font-bold text-sky-400 hover:text-sky-300 flex items-center gap-1.5"
        >
          <span>https://github.com/Rancheology/TapasShield_NSA6</span>
          <span>➔</span>
        </a>
      </div>
    </div>
  </div>
);