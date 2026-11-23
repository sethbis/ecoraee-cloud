import os
import urllib.request
import subprocess
import json
import re

# Setup output directories
base_dir = r"c:\Users\nicol\OneDrive\Documentos\integrador 5to semestre"
output_dir = os.path.join(base_dir, "06_ARQUITECTURA_EMPRESARIAL_TO-BE", "Infografia_Tecnologias_Emergentes")
os.makedirs(output_dir, exist_ok=True)

# 1. Download and format official brand SVGs with bright, vibrant contrast
svg_configs = {
    'kafka': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/apachekafka.svg', '#FFFFFF'),
    'rabbitmq': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/rabbitmq.svg', '#FF6600'),
    'tensorflow': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/tensorflow.svg', '#FF6F00'),
    'aws': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/amazonaws.svg', '#FF9900'),
    'lambda': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/awslambda.svg', '#FF9900'),
    'azure': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/azurefunctions.svg', '#007FFF'),
    'hyperledger': ('https://cdnjs.cloudflare.com/ajax/libs/simple-icons/6.19.0/hyperledger.svg', '#38BDF8'),
    'googlecloud': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/googlecloud.svg', '#4285F4'),
    'mulesoft': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/mulesoft.svg', '#00A1E0'),
    'prometheus': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/prometheus.svg', '#E6522C'),
    'grafana': ('https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/grafana.svg', '#F46800')
}

req_headers = {'User-Agent': 'Mozilla/5.0'}
svg_cache = {}

def apply_color_to_svg(raw_svg, color):
    # Remove existing fill attributes inside tags
    cleaned = re.sub(r'\sfill="[^"]*"', '', raw_svg)
    # Add fill attribute to svg tag
    if '<svg' in cleaned:
        cleaned = re.sub(r'<svg\s+', f'<svg fill="{color}" ', cleaned, count=1)
    return cleaned

for name, (url, brand_color) in svg_configs.items():
    try:
        r = urllib.request.Request(url, headers=req_headers)
        raw = urllib.request.urlopen(r, timeout=10).read().decode('utf-8')
        if '<svg' in raw:
            svg_body = raw[raw.find('<svg'):]
            svg_cache[name] = apply_color_to_svg(svg_body, brand_color)
        print(f"Processed {name} with color {brand_color}")
    except Exception as e:
        print(f"Error fetching {name}: {e}")

# Build the complete HTML Infographic
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enterprise Architecture: Next-Gen Technology Pillars</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #070B14;
      --bg-surface: #0D1424;
      --bg-card: rgba(15, 23, 42, 0.78);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-hover: rgba(255, 255, 255, 0.22);
      
      --text-primary: #F8FAFC;
      --text-secondary: #94A3B8;
      --text-muted: #64748B;
      
      --cyan: #06B6D4;
      --cyan-glow: rgba(6, 182, 212, 0.25);
      
      --purple: #8B5CF6;
      --purple-glow: rgba(139, 92, 246, 0.25);
      
      --amber: #F59E0B;
      --amber-glow: rgba(245, 158, 11, 0.25);
      
      --emerald: #10B981;
      --emerald-glow: rgba(16, 185, 129, 0.25);
      
      --blue: #3B82F6;
      --blue-glow: rgba(59, 130, 246, 0.25);
      
      --rose: #F43F5E;
      --rose-glow: rgba(244, 63, 94, 0.25);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-primary);
      line-height: 1.5;
      padding: 40px 24px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      background-image: 
        radial-gradient(circle at 15% 10%, rgba(6, 182, 212, 0.09) 0%, transparent 40%),
        radial-gradient(circle at 85% 20%, rgba(139, 92, 246, 0.09) 0%, transparent 40%),
        radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.07) 0%, transparent 50%),
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 100% 100%, 36px 36px, 36px 36px;
    }}

    /* Container */
    .infographic-wrapper {{
      max-width: 1280px;
      width: 100%;
      margin: 0 auto;
    }}

    /* Floating Action Bar (Controls) */
    .action-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(13, 20, 36, 0.9);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 9999px;
      padding: 10px 24px;
      margin-bottom: 32px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }}

    .badge-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--cyan);
      background: rgba(6, 182, 212, 0.1);
      padding: 4px 12px;
      border-radius: 9999px;
      border: 1px solid rgba(6, 182, 212, 0.2);
    }}

    .badge-pill .pulse-dot {{
      width: 7px;
      height: 7px;
      background: var(--cyan);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--cyan);
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}

    .controls-group {{
      display: flex;
      gap: 12px;
    }}

    .btn {{
      font-family: inherit;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      border: 1px solid var(--border-subtle);
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-primary);
    }}

    .btn:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: var(--border-hover);
      transform: translateY(-1px);
    }}

    .btn-primary {{
      background: linear-gradient(135deg, #06B6D4, #3B82F6);
      border: none;
      color: #FFFFFF;
      box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3);
    }}

    .btn-primary:hover {{
      box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
    }}

    /* Executive Header */
    .header {{
      text-align: center;
      margin-bottom: 40px;
      position: relative;
    }}

    .header-tag {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--cyan);
      margin-bottom: 12px;
      display: block;
    }}

    .header-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 42px;
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.15;
      margin-bottom: 14px;
      background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .header-subtitle {{
      font-size: 16.5px;
      color: var(--text-secondary);
      max-width: 780px;
      margin: 0 auto;
      font-weight: 400;
    }}

    /* Metrics Strip (Rule of 20% Text: high visual anchoring) */
    .metrics-bar {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 38px;
    }}

    .metric-chip {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .metric-value {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 28px;
      font-weight: 700;
      color: #FFFFFF;
      line-height: 1;
    }}

    .metric-label {{
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
    }}

    /* Main Grid: Exactly 6 Technology Cards (Rule of 6) */
    .grid-technologies {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 40px;
    }}

    @media (max-width: 1080px) {{
      .grid-technologies {{
        grid-template-columns: repeat(2, 1fr);
      }}
      .metrics-bar {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    @media (max-width: 720px) {{
      .grid-technologies {{
        grid-template-columns: 1fr;
      }}
      .header-title {{
        font-size: 30px;
      }}
      .metrics-bar {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Modern Glassmorphic Tech Card */
    .tech-card {{
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .tech-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: transparent;
      transition: background 0.3s ease;
    }}

    .tech-card:hover {{
      transform: translateY(-4px);
      border-color: var(--border-hover);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
    }}

    /* Color Themes per Card */
    .card-eda:hover::before {{ background: linear-gradient(90deg, var(--cyan), transparent); }}
    .card-eda:hover {{ box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--cyan-glow); }}
    .card-eda .tech-accent {{ color: var(--cyan); }}
    .card-eda .icon-wrapper {{ background: rgba(6, 182, 212, 0.12); color: var(--cyan); border-color: rgba(6, 182, 212, 0.3); }}

    .card-ai:hover::before {{ background: linear-gradient(90deg, var(--purple), transparent); }}
    .card-ai:hover {{ box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--purple-glow); }}
    .card-ai .tech-accent {{ color: var(--purple); }}
    .card-ai .icon-wrapper {{ background: rgba(139, 92, 246, 0.12); color: var(--purple); border-color: rgba(139, 92, 246, 0.3); }}

    .card-serverless:hover::before {{ background: linear-gradient(90deg, var(--amber), transparent); }}
    .card-serverless:hover {{ box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--amber-glow); }}
    .card-serverless .tech-accent {{ color: var(--amber); }}
    .card-serverless .icon-wrapper {{ background: rgba(245, 158, 11, 0.12); color: var(--amber); border-color: rgba(245, 158, 11, 0.3); }}

    .card-blockchain:hover::before {{ background: linear-gradient(90deg, var(--emerald), transparent); }}
    .card-blockchain:hover {{ box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--emerald-glow); }}
    .card-blockchain .tech-accent {{ color: var(--emerald); }}
    .card-blockchain .icon-wrapper {{ background: rgba(16, 185, 129, 0.12); color: var(--emerald); border-color: rgba(16, 185, 129, 0.3); }}

    .card-api:hover::before {{ background: linear-gradient(90deg, var(--blue), transparent); }}
    .card-api:hover {{ box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--blue-glow); }}
    .card-api .tech-accent {{ color: var(--blue); }}
    .card-api .icon-wrapper {{ background: rgba(59, 130, 246, 0.12); color: var(--blue); border-color: rgba(59, 130, 246, 0.3); }}

    .card-obs:hover::before {{ background: linear-gradient(90deg, var(--rose), transparent); }}
    .card-obs:hover {{ box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--rose-glow); }}
    .card-obs .tech-accent {{ color: var(--rose); }}
    .card-obs .icon-wrapper {{ background: rgba(244, 63, 94, 0.12); color: var(--rose); border-color: rgba(244, 63, 94, 0.3); }}

    /* Card Top */
    .card-header {{
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 18px;
    }}

    .icon-wrapper {{
      width: 48px;
      height: 48px;
      border-radius: 14px;
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}

    .icon-wrapper svg {{
      width: 24px;
      height: 24px;
      stroke-width: 2;
    }}

    .card-title-group {{
      flex: 1;
    }}

    .card-tag {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      display: block;
      margin-bottom: 2px;
    }}

    .card-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 19.5px;
      font-weight: 700;
      color: #FFFFFF;
      letter-spacing: -0.01em;
    }}

    /* Card Blocks (Definition, Tools, Operational Impact) */
    .section-block {{
      margin-bottom: 16px;
    }}

    .section-block:last-child {{
      margin-bottom: 0;
    }}

    .block-label {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .block-label svg {{
      width: 13px;
      height: 13px;
      opacity: 0.8;
    }}

    .block-text {{
      font-size: 13.5px;
      color: var(--text-secondary);
      line-height: 1.55;
    }}

    .block-text strong {{
      color: #FFFFFF;
      font-weight: 600;
    }}

    /* Tools Pill Container */
    .tools-container {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 4px;
    }}

    .tool-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 600;
      color: #F1F5F9;
      transition: all 0.2s ease;
    }}

    .tool-badge:hover {{
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.25);
      transform: translateY(-1px);
    }}

    .tool-badge svg {{
      width: 17px;
      height: 17px;
      flex-shrink: 0;
    }}

    /* Operational Impact Box */
    .impact-box {{
      background: rgba(0, 0, 0, 0.3);
      border-left: 3px solid;
      border-radius: 0 10px 10px 0;
      padding: 12px 14px;
      margin-top: auto;
    }}

    .card-eda .impact-box {{ border-left-color: var(--cyan); }}
    .card-ai .impact-box {{ border-left-color: var(--purple); }}
    .card-serverless .impact-box {{ border-left-color: var(--amber); }}
    .card-blockchain .impact-box {{ border-left-color: var(--emerald); }}
    .card-api .impact-box {{ border-left-color: var(--blue); }}
    .card-obs .impact-box {{ border-left-color: var(--rose); }}

    /* Executive Synthesis Footer */
    .conclusion-banner {{
      background: linear-gradient(135deg, rgba(13, 20, 36, 0.95), rgba(7, 11, 20, 0.95));
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 30px 34px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }}

    .conclusion-banner::after {{
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      width: 320px;
      background: radial-gradient(circle at 100% 50%, rgba(6, 182, 212, 0.15), transparent 70%);
      pointer-events: none;
    }}

    .conclusion-grid {{
      display: grid;
      grid-template-columns: 1fr 280px;
      gap: 32px;
      align-items: center;
    }}

    @media (max-width: 900px) {{
      .conclusion-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .conclusion-tag {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--cyan);
      margin-bottom: 8px;
      display: block;
    }}

    .conclusion-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 23px;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 12px;
      line-height: 1.3;
    }}

    .conclusion-statement {{
      font-size: 14.5px;
      color: var(--text-secondary);
      line-height: 1.6;
    }}

    .conclusion-statement strong {{
      color: #38BDF8;
      font-weight: 600;
    }}

    .pillars-pills {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .pillar-pill {{
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 10px 14px;
      font-size: 13px;
      font-weight: 600;
      color: #FFFFFF;
    }}

    .pillar-indicator {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }}

    .pi-agile {{ background: var(--cyan); box-shadow: 0 0 8px var(--cyan); }}
    .pi-scalable {{ background: var(--purple); box-shadow: 0 0 8px var(--purple); }}
    .pi-resilient {{ background: var(--emerald); box-shadow: 0 0 8px var(--emerald); }}

    /* Footer Metadata */
    .infographic-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 30px;
      padding-top: 18px;
      border-top: 1px solid var(--border-subtle);
      font-size: 12px;
      color: var(--text-muted);
    }}

    .team-badge {{
      font-weight: 600;
      color: var(--text-secondary);
    }}

    /* Print styles */
    @media print {{
      body {{
        background: #070B14 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        padding: 0 !important;
      }}
      .action-bar {{
        display: none !important;
      }}
      .tech-card {{
        break-inside: avoid;
        page-break-inside: avoid;
      }}
    }}
  </style>
</head>
<body>

  <div class="infographic-wrapper">
    
    <!-- Top Action & Meta Bar -->
    <div class="action-bar">
      <div class="badge-pill">
        <span class="pulse-dot"></span>
        <span>Enterprise & Industrial Architecture</span>
      </div>

      <div class="controls-group">
        <button class="btn" onclick="toggleLanguage()" id="btn-lang">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span id="lang-label">Español</span>
        </button>
        <button class="btn btn-primary" onclick="window.print()">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
          <span>Exportar PDF / Imprimir</span>
        </button>
      </div>
    </div>

    <!-- Executive Header -->
    <header class="header">
      <span class="header-tag" data-en="Next-Generation Enterprise Stack" data-es="Stack Tecnológico de Próxima Generación">Next-Generation Enterprise Stack</span>
      <h1 class="header-title" data-en="Emerging Technologies in Enterprise Architecture" data-es="Tecnologías Emergentes en Arquitectura Empresarial">Emerging Technologies in Enterprise Architecture</h1>
      <p class="header-subtitle" data-en="Modernizing IT ecosystems through decoupled, intelligent, and scalable distributed paradigms designed for business agility." data-es="Modernización de ecosistemas de TI mediante paradigmas distribuidos, desacoplados e inteligentes diseñados para la agilidad del negocio.">
        Modernizing IT ecosystems through decoupled, intelligent, and scalable distributed paradigms designed for business agility.
      </p>
    </header>

    <!-- Metrics Bar (Visual Anchors - Rule of 20% Text) -->
    <div class="metrics-bar">
      <div class="metric-chip">
        <div class="metric-value" style="color: var(--cyan);">6</div>
        <div>
          <div class="metric-label" data-en="Strategic Pillars" data-es="Pilares Estratégicos">Strategic Pillars</div>
          <div style="font-size: 11px; color: var(--text-secondary);">Enterprise Ready</div>
        </div>
      </div>
      <div class="metric-chip">
        <div class="metric-value" style="color: var(--purple);">&lt;20%</div>
        <div>
          <div class="metric-label" data-en="Cognitive Density" data-es="Densidad Cognitiva">Cognitive Density</div>
          <div style="font-size: 11px; color: var(--text-secondary);">High-Retention Focus</div>
        </div>
      </div>
      <div class="metric-chip">
        <div class="metric-value" style="color: var(--emerald);">0%</div>
        <div>
          <div class="metric-label" data-en="AI Clichés / Fluff" data-es="Clichés de IA">AI Clichés / Fluff</div>
          <div style="font-size: 11px; color: var(--text-secondary);">Pure Vector Assets</div>
        </div>
      </div>
      <div class="metric-chip">
        <div class="metric-value" style="color: var(--amber);">3x</div>
        <div>
          <div class="metric-label" data-en="Operational Agility" data-es="Agilidad Operativa">Operational Agility</div>
          <div style="font-size: 11px; color: var(--text-secondary);">Decoupled Speed</div>
        </div>
      </div>
    </div>

    <!-- Main Grid: 6 Pillars (Miller's Law - 6 Objects Rule) -->
    <main class="grid-technologies">

      <!-- 1. Event-Driven Architecture (EDA) -->
      <article class="tech-card card-eda">
        <div class="card-header">
          <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <div class="card-title-group">
            <span class="card-tag tech-accent">Pillar 01</span>
            <h2 class="card-title">Event-Driven Architecture</h2>
          </div>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            <span data-en="Definition" data-es="Definición">Definition</span>
          </div>
          <p class="block-text" data-en="A software architecture pattern where decoupled components communicate through the production, detection, and consumption of <strong>asynchronous real-time events</strong>." data-es="Patrón arquitectónico donde componentes desacoplados se comunican mediante la producción, detección y consumo de <strong>eventos asíncronos en tiempo real</strong>.">
            A software architecture pattern where decoupled components communicate through the production, detection, and consumption of <strong>asynchronous real-time events</strong>.
          </p>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            <span data-en="Real-World Tools" data-es="Herramientas Reales">Real-World Tools</span>
          </div>
          <div class="tools-container">
            <div class="tool-badge">
              {svg_cache.get('kafka', '')}
              <span>Apache Kafka</span>
            </div>
            <div class="tool-badge">
              {svg_cache.get('rabbitmq', '')}
              <span>RabbitMQ</span>
            </div>
          </div>
        </div>

        <div class="section-block impact-box">
          <div class="block-label" style="color: var(--cyan);">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            <span data-en="Operational Impact" data-es="Impacto Operativo">Operational Impact</span>
          </div>
          <p class="block-text" data-en="Eliminates blocking bottlenecks, drastically improving <strong>high-availability resilience</strong> and linear <strong>horizontal scalability</strong> under spiky workloads." data-es="Elimina cuellos de botella bloqueantes, elevando la <strong>resiliencia y alta disponibilidad</strong> junto con una <strong>escalabilidad horizontal lineal</strong> ante picos de demanda.">
            Eliminates blocking bottlenecks, drastically improving <strong>high-availability resilience</strong> and linear <strong>horizontal scalability</strong> under spiky workloads.
          </p>
        </div>
      </article>

      <!-- 2. Artificial Intelligence & Machine Learning -->
      <article class="tech-card card-ai">
        <div class="card-header">
          <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 2a4 4 0 0 1 4 4v1a4 4 0 0 1-4 4 4 4 0 0 1-4-4V6a4 4 0 0 1 4-4z"/><path d="M16 11.37A4 4 0 1 1 12.63 8"/><path d="M12 18v4"/><path d="M8 22h8"/></svg>
          </div>
          <div class="card-title-group">
            <span class="card-tag tech-accent">Pillar 02</span>
            <h2 class="card-title">AI & Machine Learning</h2>
          </div>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            <span data-en="Definition" data-es="Definición">Definition</span>
          </div>
          <p class="block-text" data-en="Mathematical models and algorithms that learn from data patterns to <strong>automate complex cognitive tasks</strong> and continuously optimize business workflows." data-es="Modelos matemáticos y algoritmos que aprenden patrones de datos para <strong>automatizar tareas cognitivas complejas</strong> y optimizar flujos empresariales.">
            Mathematical models and algorithms that learn from data patterns to <strong>automate complex cognitive tasks</strong> and continuously optimize business workflows.
          </p>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            <span data-en="Real-World Tools" data-es="Herramientas Reales">Real-World Tools</span>
          </div>
          <div class="tools-container">
            <div class="tool-badge">
              {svg_cache.get('tensorflow', '')}
              <span>TensorFlow</span>
            </div>
            <div class="tool-badge">
              {svg_cache.get('aws', '')}
              <span>AWS SageMaker</span>
            </div>
          </div>
        </div>

        <div class="section-block impact-box">
          <div class="block-label" style="color: var(--purple);">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            <span data-en="Operational Impact" data-es="Impacto Operativo">Operational Impact</span>
          </div>
          <p class="block-text" data-en="Empowers <strong>predictive decision-making</strong> with sub-second insights while bolstering <strong>proactive cybersecurity</strong> via automated anomaly detection." data-es="Potencia la <strong>toma de decisiones predictiva</strong> en tiempo real y fortalece la <strong>ciberseguridad proactiva</strong> mediante detección automatizada de anomalías.">
            Empowers <strong>predictive decision-making</strong> with sub-second insights while bolstering <strong>proactive cybersecurity</strong> via automated anomaly detection.
          </p>
        </div>
      </article>

      <!-- 3. Serverless Computing -->
      <article class="tech-card card-serverless">
        <div class="card-header">
          <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>
          </div>
          <div class="card-title-group">
            <span class="card-tag tech-accent">Pillar 03</span>
            <h2 class="card-title">Serverless Computing</h2>
          </div>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            <span data-en="Definition" data-es="Definición">Definition</span>
          </div>
          <p class="block-text" data-en="Cloud execution model that runs application logic on-demand <strong>without managing or provisioning servers</strong>, abstracting infrastructure maintenance entirely." data-es="Modelo de ejecución en la nube que ejecuta lógica bajo demanda <strong>sin administrar servidores</strong>, abstrayendo por completo el mantenimiento de infraestructura.">
            Cloud execution model that runs application logic on-demand <strong>without managing or provisioning servers</strong>, abstracting infrastructure maintenance entirely.
          </p>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            <span data-en="Real-World Tools" data-es="Herramientas Reales">Real-World Tools</span>
          </div>
          <div class="tools-container">
            <div class="tool-badge">
              {svg_cache.get('lambda', '')}
              <span>AWS Lambda</span>
            </div>
            <div class="tool-badge">
              {svg_cache.get('azure', '')}
              <span>Azure Functions</span>
            </div>
          </div>
        </div>

        <div class="section-block impact-box">
          <div class="block-label" style="color: var(--amber);">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            <span data-en="Operational Impact" data-es="Impacto Operativo">Operational Impact</span>
          </div>
          <p class="block-text" data-en="Shifts engineering priority from <strong>infrastructure patching to code delivery</strong>, enabling zero-idle costs and automatic scale-to-zero agility." data-es="Traslada el enfoque de <strong>mantener infraestructura a generar código de negocio</strong>, logrando costos cero en reposo y autoescalado instantáneo.">
            Shifts engineering priority from <strong>infrastructure patching to code delivery</strong>, enabling zero-idle costs and automatic scale-to-zero agility.
          </p>
        </div>
      </article>

      <!-- 4. Blockchain & Distributed Ledgers -->
      <article class="tech-card card-blockchain">
        <div class="card-header">
          <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><line x1="10" y1="6.5" x2="14" y2="6.5"/><line x1="17.5" y1="10" x2="17.5" y2="14"/><line x1="14" y1="17.5" x2="10" y2="17.5"/><line x1="6.5" y1="14" x2="6.5" y2="10"/></svg>
          </div>
          <div class="card-title-group">
            <span class="card-tag tech-accent">Pillar 04</span>
            <h2 class="card-title">Enterprise Blockchain</h2>
          </div>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            <span data-en="Definition" data-es="Definición">Definition</span>
          </div>
          <p class="block-text" data-en="A decentralized, cryptographically shared ledger characterized by triple pillars: <strong>ironclad security, radical transparency, and immutability</strong>." data-es="Libro mayor descentralizado y compartido criptográficamente caracterizado por tres pilares: <strong>seguridad blindada, transparencia total e inmutabilidad</strong>.">
            A decentralized, cryptographically shared ledger characterized by triple pillars: <strong>ironclad security, radical transparency, and immutability</strong>.
          </p>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            <span data-en="Real-World Tools" data-es="Herramientas Reales">Real-World Tools</span>
          </div>
          <div class="tools-container">
            <div class="tool-badge">
              {svg_cache.get('hyperledger', '')}
              <span>Hyperledger Fabric</span>
            </div>
            <div class="tool-badge">
              <svg viewBox="0 0 24 24" fill="#10B981"><path d="M12 1.75l-6.5 10.75L12 16.5l6.5-4L12 1.75zM5.5 13.5L12 22.25l6.5-8.75L12 17.5 5.5 13.5z"/></svg>
              <span>Enterprise DLT</span>
            </div>
          </div>
        </div>

        <div class="section-block impact-box">
          <div class="block-label" style="color: var(--emerald);">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            <span data-en="Operational Impact" data-es="Impacto Operativo">Operational Impact</span>
          </div>
          <p class="block-text" data-en="Revolutionizes multi-party <strong>supply chain asset tracking</strong> while providing cryptographically verifiable, <strong>tamper-proof data integrity</strong>." data-es="Revoluciona el <strong>rastreo de activos multiparte</strong> en cadenas de suministro y garantiza una <strong>integridad de datos a prueba de manipulación</strong>.">
            Revolutionizes multi-party <strong>supply chain asset tracking</strong> while providing cryptographically verifiable, <strong>tamper-proof data integrity</strong>.
          </p>
        </div>
      </article>

      <!-- 5. API Management -->
      <article class="tech-card card-api">
        <div class="card-header">
          <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><line x1="6" y1="9" x2="6" y2="21"/></svg>
          </div>
          <div class="card-title-group">
            <span class="card-tag tech-accent">Pillar 05</span>
            <h2 class="card-title">API Management</h2>
          </div>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            <span data-en="Definition" data-es="Definición">Definition</span>
          </div>
          <p class="block-text" data-en="Comprehensive architectural gateway for publishing, securing, and governing interfaces <strong>crucial for microservices integration</strong> across hybrid clouds." data-es="Pasarela arquitectónica integral para publicar, proteger y gobernar interfaces <strong>cruciales para la integración de microservicios</strong> híbridos.">
            Comprehensive architectural gateway for publishing, securing, and governing interfaces <strong>crucial for microservices integration</strong> across hybrid clouds.
          </p>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            <span data-en="Real-World Tools" data-es="Herramientas Reales">Real-World Tools</span>
          </div>
          <div class="tools-container">
            <div class="tool-badge">
              {svg_cache.get('googlecloud', '')}
              <span>Google Apigee</span>
            </div>
            <div class="tool-badge">
              {svg_cache.get('mulesoft', '')}
              <span>MuleSoft Anypoint</span>
            </div>
          </div>
        </div>

        <div class="section-block impact-box">
          <div class="block-label" style="color: var(--blue);">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            <span data-en="Operational Impact" data-es="Impacto Operativo">Operational Impact</span>
          </div>
          <p class="block-text" data-en="Enforces <strong>Zero-Trust security</strong>, guarantees high-throughput scalability via rate-limiting, and accelerates enterprise <strong>service reusability</strong>." data-es="Garantiza <strong>seguridad Zero-Trust</strong>, asegura alta escalabilidad mediante control de tráfico y maximiza la <strong>reutilización de servicios</strong>.">
            Enforces <strong>Zero-Trust security</strong>, guarantees high-throughput scalability via rate-limiting, and accelerates enterprise <strong>service reusability</strong>.
          </p>
        </div>
      </article>

      <!-- 6. Observability Platforms -->
      <article class="tech-card card-obs">
        <div class="card-header">
          <div class="icon-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          </div>
          <div class="card-title-group">
            <span class="card-tag tech-accent">Pillar 06</span>
            <h2 class="card-title">Observability Platforms</h2>
          </div>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            <span data-en="Definition" data-es="Definición">Definition</span>
          </div>
          <p class="block-text" data-en="Full-spectrum telemetric telemetry (metrics, distributed traces, and logs) that provides a <strong>complete real-time view of distributed systems</strong>." data-es="Telemetría de espectro completo (métricas, trazas distribuidas y logs) que brinda una <strong>visión integral en tiempo real de sistemas distribuidos</strong>.">
            Full-spectrum telemetric telemetry (metrics, distributed traces, and logs) that provides a <strong>complete real-time view of distributed systems</strong>.
          </p>
        </div>

        <div class="section-block">
          <div class="block-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            <span data-en="Real-World Tools" data-es="Herramientas Reales">Real-World Tools</span>
          </div>
          <div class="tools-container">
            <div class="tool-badge">
              {svg_cache.get('prometheus', '')}
              <span>Prometheus</span>
            </div>
            <div class="tool-badge">
              {svg_cache.get('grafana', '')}
              <span>Grafana</span>
            </div>
          </div>
        </div>

        <div class="section-block impact-box">
          <div class="block-label" style="color: var(--rose);">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
            <span data-en="Operational Impact" data-es="Impacto Operativo">Operational Impact</span>
          </div>
          <p class="block-text" data-en="Drives <strong>proactive issue detection and automated triage</strong>, slashing Mean Time to Resolution (MTTR) before business degradation occurs." data-es="Habilita la <strong>detección proactiva de incidentes y resolución rápida (MTTR)</strong> mucho antes de que impacten a los usuarios de negocio.">
            Drives <strong>proactive issue detection and automated triage</strong>, slashing Mean Time to Resolution (MTTR) before business degradation occurs.
          </p>
        </div>
      </article>

    </main>

    <!-- Executive Synthesis Conclusion Banner -->
    <section class="conclusion-banner">
      <div class="conclusion-grid">
        <div>
          <span class="conclusion-tag" data-en="Architectural Synthesis & Strategic Value" data-es="Síntesis Arquitectónica y Valor Estratégico">Architectural Synthesis & Strategic Value</span>
          <h3 class="conclusion-title" data-en="The Foundation of the Modern Enterprise Ecosystem" data-es="Los Cimientos del Ecosistema Empresarial Moderno">The Foundation of the Modern Enterprise Ecosystem</h3>
          <p class="conclusion-statement" data-en="In modern Enterprise Architecture, adopting these six emerging technologies transcends individual technical upgrades: <strong>orchestrated together, they forge radically more agile, scalable, and resilient enterprise architectures</strong> capable of thriving amidst continuous business disruption." data-es="En la Arquitectura Empresarial moderna, adoptar estas seis tecnologías emergentes trasciende mejoras técnicas aisladas: <strong>orquestadas en conjunto, forjan arquitecturas radicalmente más ágiles, escalables y resilientes</strong> capaces de prosperar ante la disrupción continua del mercado.">
            In modern Enterprise Architecture, adopting these six emerging technologies transcends individual technical upgrades: <strong>orchestrated together, they forge radically more agile, scalable, and resilient enterprise architectures</strong> capable of thriving amidst continuous business disruption.
          </p>
        </div>

        <div class="pillars-pills">
          <div class="pillar-pill">
            <span class="pillar-indicator pi-agile"></span>
            <span data-en="Agility: Decoupled & Event-Driven" data-es="Agilidad: Desacople Orientado a Eventos">Agility: Decoupled &amp; Event-Driven</span>
          </div>
          <div class="pillar-pill">
            <span class="pillar-indicator pi-scalable"></span>
            <span data-en="Scalability: Serverless & Auto-Elastic" data-es="Escalabilidad: Serverless y Auto-Elástica">Scalability: Serverless &amp; Auto-Elastic</span>
          </div>
          <div class="pillar-pill">
            <span class="pillar-indicator pi-resilient"></span>
            <span data-en="Resilience: Observable & Immutable" data-es="Resiliencia: Observable e Inmutable">Resilience: Observable &amp; Immutable</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Metadata Footer -->
    <footer class="infographic-footer">
      <div>
        <span>UIDE — Faculty of Technical Sciences | School of Computer Science & IT</span>
      </div>
      <div class="team-badge">
        <span>Arquitectura Empresarial (05-SIN-A) • Ing. Iván Reyes Chacón</span>
      </div>
    </footer>

  </div>

  <script>
    let currentLang = 'en';
    function toggleLanguage() {{
      currentLang = currentLang === 'en' ? 'es' : 'en';
      document.querySelectorAll('[data-en]').forEach(el => {{
        const text = el.getAttribute(`data-${{currentLang}}`);
        if (text) {{
          el.innerHTML = text;
        }}
      }});
      document.getElementById('lang-label').innerText = currentLang === 'en' ? 'Español' : 'English';
      document.documentElement.lang = currentLang;
    }}
  </script>
</body>
</html>
"""

html_path = os.path.join(output_dir, "Infografia_Arquitectura_Empresarial.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

root_html = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial.html")
with open(root_html, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated new vibrant HTML at {html_path} and {root_html}")
