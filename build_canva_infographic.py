import os
import urllib.request
import subprocess
import re
import shutil

base_dir = r"c:\Users\nicol\OneDrive\Documentos\integrador 5to semestre"
output_dir = os.path.join(base_dir, "06_ARQUITECTURA_EMPRESARIAL_TO-BE", "Infografia_Tecnologias_Emergentes")
os.makedirs(output_dir, exist_ok=True)
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 1. Download official brand SVGs
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
    cleaned = re.sub(r'\sfill="[^"]*"', '', raw_svg)
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
    except Exception as e:
        print(f"Error fetching {name}: {e}")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enterprise Architecture - Emerging Technologies</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090D16;
      --card-bg: rgba(15, 23, 42, 0.88);
      --border-color: rgba(255, 255, 255, 0.09);
      --text-main: #FFFFFF;
      --text-muted: #94A3B8;
      
      /* Vibrant Canva-inspired section palettes */
      --c1: #00F5A0; /* Mint neon */
      --c1-sub: #00D9F5;
      
      --c2: #C084FC; /* Electric Purple */
      --c2-sub: #F472B6;
      
      --c3: #FB923C; /* Solar Amber */
      --c3-sub: #FBBF24;
      
      --c4: #10B981; /* Emerald Neon */
      --c4-sub: #38BDF8;
      
      --c5: #38BDF8; /* Cyber Azure */
      --c5-sub: #818CF8;
      
      --c6: #F87171; /* Radiant Coral */
      --c6-sub: #FB923C;
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      display: flex;
      justify-content: center;
      padding: 0;
      margin: 0;
      background-image: 
        radial-gradient(circle at 10% 8%, rgba(0, 245, 160, 0.07) 0%, transparent 35%),
        radial-gradient(circle at 90% 25%, rgba(192, 132, 252, 0.07) 0%, transparent 35%),
        radial-gradient(circle at 15% 55%, rgba(251, 146, 60, 0.07) 0%, transparent 35%),
        radial-gradient(circle at 85% 75%, rgba(56, 189, 248, 0.07) 0%, transparent 35%),
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%, 32px 32px, 32px 32px;
    }}

    /* Main Poster Canvas (Canva vertical format 900px width) */
    .infographic-canvas {{
      width: 900px;
      background-color: #080C14;
      padding: 50px 46px 40px 46px;
      box-shadow: 0 0 70px rgba(0, 0, 0, 0.85);
      position: relative;
      overflow: hidden;
    }}

    /* Poster Header */
    .poster-header {{
      text-align: center;
      margin-bottom: 46px;
      position: relative;
    }}

    .category-chip {{
      display: inline-block;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--c1);
      background: rgba(0, 245, 160, 0.1);
      border: 1px solid rgba(0, 245, 160, 0.3);
      padding: 6px 20px;
      border-radius: 9999px;
      margin-bottom: 16px;
    }}

    .poster-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 42px;
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -0.02em;
      text-transform: uppercase;
      margin-bottom: 14px;
      background: linear-gradient(135deg, #FFFFFF 40%, #94A3B8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .poster-subtitle {{
      font-size: 15.5px;
      color: var(--text-muted);
      max-width: 640px;
      margin: 0 auto;
      line-height: 1.5;
      font-weight: 500;
    }}

    .header-divider {{
      width: 80px;
      height: 4px;
      background: linear-gradient(90deg, var(--c1), var(--c1-sub));
      border-radius: 2px;
      margin: 20px auto 0 auto;
    }}

    /* Section Flow (Alternating Zig-Zag like both Canva templates) */
    .sections-container {{
      display: flex;
      flex-direction: column;
      gap: 34px;
      margin-bottom: 44px;
    }}

    .section-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 34px;
      align-items: center;
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 26px;
      padding: 32px 30px;
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(14px);
    }}

    .section-row::before {{
      content: '';
      position: absolute;
      top: 0;
      bottom: 0;
      width: 4px;
    }}

    .row-1::before {{ left: 0; background: linear-gradient(180deg, var(--c1), var(--c1-sub)); }}
    .row-2::before {{ right: 0; background: linear-gradient(180deg, var(--c2), var(--c2-sub)); }}
    .row-3::before {{ left: 0; background: linear-gradient(180deg, var(--c3), var(--c3-sub)); }}
    .row-4::before {{ right: 0; background: linear-gradient(180deg, var(--c4), var(--c4-sub)); }}
    .row-5::before {{ left: 0; background: linear-gradient(180deg, var(--c5), var(--c5-sub)); }}
    .row-6::before {{ right: 0; background: linear-gradient(180deg, var(--c6), var(--c6-sub)); }}

    /* Number Badge */
    .num-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border-radius: 12px;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 17px;
      font-weight: 800;
      color: #000000;
      margin-bottom: 12px;
    }}

    .row-1 .num-badge {{ background: var(--c1); box-shadow: 0 0 16px rgba(0, 245, 160, 0.45); }}
    .row-2 .num-badge {{ background: var(--c2); box-shadow: 0 0 16px rgba(192, 132, 252, 0.45); }}
    .row-3 .num-badge {{ background: var(--c3); box-shadow: 0 0 16px rgba(251, 146, 60, 0.45); }}
    .row-4 .num-badge {{ background: var(--c4); box-shadow: 0 0 16px rgba(16, 185, 129, 0.45); }}
    .row-5 .num-badge {{ background: var(--c5); box-shadow: 0 0 16px rgba(56, 189, 248, 0.45); }}
    .row-6 .num-badge {{ background: var(--c6); box-shadow: 0 0 16px rgba(248, 113, 113, 0.45); }}

    /* Content Block (20% text rule applied cleanly) */
    .content-block {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .topic-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.01em;
      line-height: 1.2;
      color: #FFFFFF;
    }}

    .def-text {{
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    .def-text strong {{
      color: #FFFFFF;
      font-weight: 600;
    }}

    .impact-callout {{
      background: rgba(0, 0, 0, 0.38);
      border-radius: 12px;
      padding: 12px 14px;
      font-size: 12.5px;
      line-height: 1.45;
      color: #E2E8F0;
      border-left: 3px solid;
    }}

    .row-1 .impact-callout {{ border-left-color: var(--c1); }}
    .row-2 .impact-callout {{ border-left-color: var(--c2); }}
    .row-3 .impact-callout {{ border-left-color: var(--c3); }}
    .row-4 .impact-callout {{ border-left-color: var(--c4); }}
    .row-5 .impact-callout {{ border-left-color: var(--c5); }}
    .row-6 .impact-callout {{ border-left-color: var(--c6); }}

    .impact-callout .impact-tag {{
      display: block;
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 3px;
    }}

    .row-1 .impact-tag {{ color: var(--c1); }}
    .row-2 .impact-tag {{ color: var(--c2); }}
    .row-3 .impact-tag {{ color: var(--c3); }}
    .row-4 .impact-tag {{ color: var(--c4); }}
    .row-5 .impact-tag {{ color: var(--c5); }}
    .row-6 .impact-tag {{ color: var(--c6); }}

    /* =========================================================
       GRAPHIC HERO HUB: PROMINENT, LARGE VISUAL ANCHORS
       (Inspired by the large illustrations in Canva references)
       ========================================================= */
    .graphic-hub {{
      background: radial-gradient(circle at 50% 40%, rgba(255, 255, 255, 0.04) 0%, rgba(0, 0, 0, 0.25) 100%);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 22px;
      padding: 28px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      min-height: 230px;
    }}

    /* MASSIVE Central Hero Emblem (116px x 116px with 62px SVG!) */
    .main-emblem {{
      width: 116px;
      height: 116px;
      border-radius: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 18px;
      position: relative;
      transition: transform 0.3s ease;
    }}

    .main-emblem svg {{
      width: 62px;
      height: 62px;
      filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.5));
    }}

    .row-1 .main-emblem {{
      background: linear-gradient(135deg, rgba(0, 245, 160, 0.18), rgba(0, 217, 245, 0.1));
      border: 1.5px solid rgba(0, 245, 160, 0.45);
      color: var(--c1);
      box-shadow: 0 0 35px rgba(0, 245, 160, 0.3);
    }}

    .row-2 .main-emblem {{
      background: linear-gradient(135deg, rgba(192, 132, 252, 0.18), rgba(244, 114, 182, 0.1));
      border: 1.5px solid rgba(192, 132, 252, 0.45);
      color: var(--c2);
      box-shadow: 0 0 35px rgba(192, 132, 252, 0.3);
    }}

    .row-3 .main-emblem {{
      background: linear-gradient(135deg, rgba(251, 146, 60, 0.18), rgba(251, 191, 36, 0.1));
      border: 1.5px solid rgba(251, 146, 60, 0.45);
      color: var(--c3);
      box-shadow: 0 0 35px rgba(251, 146, 60, 0.3);
    }}

    .row-4 .main-emblem {{
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(56, 189, 248, 0.1));
      border: 1.5px solid rgba(16, 185, 129, 0.45);
      color: var(--c4);
      box-shadow: 0 0 35px rgba(16, 185, 129, 0.3);
    }}

    .row-5 .main-emblem {{
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.18), rgba(129, 140, 248, 0.1));
      border: 1.5px solid rgba(56, 189, 248, 0.45);
      color: var(--c5);
      box-shadow: 0 0 35px rgba(56, 189, 248, 0.3);
    }}

    .row-6 .main-emblem {{
      background: linear-gradient(135deg, rgba(248, 113, 113, 0.18), rgba(251, 146, 60, 0.1));
      border: 1.5px solid rgba(248, 113, 113, 0.45);
      color: var(--c6);
      box-shadow: 0 0 35px rgba(248, 113, 113, 0.3);
    }}

    /* Real Brand Tool Badges: Well-sized, vibrant */
    .tools-label {{
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}

    .tools-row {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: center;
    }}

    .tool-chip {{
      display: inline-flex;
      align-items: center;
      gap: 9px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 7px 14px;
      border-radius: 9999px;
      font-size: 12.5px;
      font-weight: 700;
      color: #FFFFFF;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }}

    .tool-chip svg {{
      width: 20px;
      height: 20px;
    }}

    /* Strategic Conclusion Banner */
    .conclusion-section {{
      background: linear-gradient(135deg, rgba(15, 23, 42, 0.98), rgba(8, 12, 20, 0.98));
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 26px;
      padding: 34px 38px;
      text-align: center;
      position: relative;
      overflow: hidden;
      margin-bottom: 28px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }}

    .conclusion-tag {{
      display: inline-block;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--c1);
      margin-bottom: 8px;
    }}

    .conclusion-heading {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 24px;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 12px;
      line-height: 1.25;
    }}

    .conclusion-body {{
      font-size: 14.5px;
      color: var(--text-muted);
      line-height: 1.6;
      max-width: 700px;
      margin: 0 auto 20px auto;
    }}

    .conclusion-body strong {{
      color: #38BDF8;
      font-weight: 700;
    }}

    .conclusion-triad {{
      display: flex;
      justify-content: center;
      gap: 16px;
    }}

    .triad-pill {{
      display: flex;
      align-items: center;
      gap: 9px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 9px 18px;
      border-radius: 9999px;
      font-size: 12.5px;
      font-weight: 700;
      color: #FFFFFF;
    }}

    .triad-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }}

    .dot-1 {{ background: var(--c1); box-shadow: 0 0 10px var(--c1); }}
    .dot-2 {{ background: var(--c3); box-shadow: 0 0 10px var(--c3); }}
    .dot-3 {{ background: var(--c5); box-shadow: 0 0 10px var(--c5); }}

    /* Academic Footer */
    .academic-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 18px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 12px;
      color: #64748B;
      font-weight: 500;
    }}

    .footer-highlight {{
      color: var(--text-muted);
      font-weight: 600;
    }}
  </style>
</head>
<body>

  <div class="infographic-canvas">

    <!-- Poster Header -->
    <header class="poster-header">
      <span class="category-chip">Enterprise Architecture Framework</span>
      <h1 class="poster-title">Emerging Technologies</h1>
      <p class="poster-subtitle">
        Foundational architectural paradigms modernizing enterprise systems toward high agility, auto-scalability, and non-blocking resilience.
      </p>
      <div class="header-divider"></div>
    </header>

    <!-- 6 Alternating Sections (Zig-Zag format like Canva) -->
    <div class="sections-container">

      <!-- 1. Event-Driven Architecture (Graphic Left, Content Right) -->
      <section class="section-row row-1">
        <div class="graphic-hub">
          <div class="main-emblem">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <span class="tools-label">Real-World Platforms</span>
          <div class="tools-row">
            <span class="tool-chip">
              {svg_cache.get('kafka', '')}
              Apache Kafka
            </span>
            <span class="tool-chip">
              {svg_cache.get('rabbitmq', '')}
              RabbitMQ
            </span>
          </div>
        </div>

        <div class="content-block">
          <span class="num-badge">01</span>
          <h2 class="topic-title">Event-Driven Architecture</h2>
          <p class="def-text">
            A software pattern where decoupled services interact by generating, detecting, and consuming <strong>asynchronous real-time events</strong> without direct synchronous coupling.
          </p>
          <div class="impact-callout">
            <span class="impact-tag">Operational Impact</span>
            Eliminates blocking dependencies, drastically boosting <strong>fault-tolerant resilience</strong> and linear <strong>horizontal scalability</strong> under heavy workloads.
          </div>
        </div>
      </section>

      <!-- 2. AI & Machine Learning (Content Left, Graphic Right) -->
      <section class="section-row row-2">
        <div class="content-block">
          <span class="num-badge">02</span>
          <h2 class="topic-title">AI &amp; Machine Learning</h2>
          <p class="def-text">
            Mathematical models and continuous learning algorithms engineered to <strong>automate complex cognitive tasks</strong> and optimize enterprise business processes at scale.
          </p>
          <div class="impact-callout">
            <span class="impact-tag">Operational Impact</span>
            Empowers real-time <strong>predictive decision-making</strong> while fortifying <strong>proactive cybersecurity</strong> through automated anomaly and threat detection.
          </div>
        </div>

        <div class="graphic-hub">
          <div class="main-emblem">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 2a4 4 0 0 1 4 4v1a4 4 0 0 1-4 4 4 4 0 0 1-4-4V6a4 4 0 0 1 4-4z"/><path d="M16 11.37A4 4 0 1 1 12.63 8"/><path d="M12 18v4"/><path d="M8 22h8"/></svg>
          </div>
          <span class="tools-label">Real-World Platforms</span>
          <div class="tools-row">
            <span class="tool-chip">
              {svg_cache.get('tensorflow', '')}
              TensorFlow
            </span>
            <span class="tool-chip">
              {svg_cache.get('aws', '')}
              AWS SageMaker
            </span>
          </div>
        </div>
      </section>

      <!-- 3. Serverless Computing (Graphic Left, Content Right) -->
      <section class="section-row row-3">
        <div class="graphic-hub">
          <div class="main-emblem">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>
          </div>
          <span class="tools-label">Real-World Platforms</span>
          <div class="tools-row">
            <span class="tool-chip">
              {svg_cache.get('lambda', '')}
              AWS Lambda
            </span>
            <span class="tool-chip">
              {svg_cache.get('azure', '')}
              Azure Functions
            </span>
          </div>
        </div>

        <div class="content-block">
          <span class="num-badge">03</span>
          <h2 class="topic-title">Serverless Computing</h2>
          <p class="def-text">
            On-demand cloud execution model where application logic executes <strong>without managing or provisioning servers</strong>, abstracting infrastructure entirely.
          </p>
          <div class="impact-callout">
            <span class="impact-tag">Operational Impact</span>
            Shifts corporate engineering priority from <strong>infrastructure maintenance to rapid code delivery</strong>, enabling zero-idle costs and automatic scaling.
          </div>
        </div>
      </section>

      <!-- 4. Blockchain (Content Left, Graphic Right) -->
      <section class="section-row row-4">
        <div class="content-block">
          <span class="num-badge">04</span>
          <h2 class="topic-title">Enterprise Blockchain</h2>
          <p class="def-text">
            A cryptographically distributed shared ledger delivering three core capabilities: <strong>ironclad security, radical transparency, and immutability</strong>.
          </p>
          <div class="impact-callout">
            <span class="impact-tag">Operational Impact</span>
            Revolutionizes multi-party <strong>supply chain asset tracking</strong> while ensuring verifiable, <strong>tamper-proof data integrity</strong> across ecosystems.
          </div>
        </div>

        <div class="graphic-hub">
          <div class="main-emblem">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><line x1="10" y1="6.5" x2="14" y2="6.5"/><line x1="17.5" y1="10" x2="17.5" y2="14"/><line x1="14" y1="17.5" x2="10" y2="17.5"/><line x1="6.5" y1="14" x2="6.5" y2="10"/></svg>
          </div>
          <span class="tools-label">Real-World Platforms</span>
          <div class="tools-row">
            <span class="tool-chip">
              {svg_cache.get('hyperledger', '')}
              Hyperledger Fabric
            </span>
            <span class="tool-chip">
              <svg viewBox="0 0 24 24" fill="#10B981"><path d="M12 1.75l-6.5 10.75L12 16.5l6.5-4L12 1.75zM5.5 13.5L12 22.25l6.5-8.75L12 17.5 5.5 13.5z"/></svg>
              Enterprise DLT
            </span>
          </div>
        </div>
      </section>

      <!-- 5. API Management (Graphic Left, Content Right) -->
      <section class="section-row row-5">
        <div class="graphic-hub">
          <div class="main-emblem">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><line x1="6" y1="9" x2="6" y2="21"/></svg>
          </div>
          <span class="tools-label">Real-World Platforms</span>
          <div class="tools-row">
            <span class="tool-chip">
              {svg_cache.get('googlecloud', '')}
              Google Apigee
            </span>
            <span class="tool-chip">
              {svg_cache.get('mulesoft', '')}
              MuleSoft Anypoint
            </span>
          </div>
        </div>

        <div class="content-block">
          <span class="num-badge">05</span>
          <h2 class="topic-title">API Management</h2>
          <p class="def-text">
            Comprehensive lifecycle governance and architectural gateway <strong>crucial for seamless microservices integration</strong> across hybrid cloud landscapes.
          </p>
          <div class="impact-callout">
            <span class="impact-tag">Operational Impact</span>
            Assures <strong>Zero-Trust security</strong>, guarantees throughput scalability via traffic throttling, and maximizes modular <strong>service reusability</strong>.
          </div>
        </div>
      </section>

      <!-- 6. Observability Platforms (Content Left, Graphic Right) -->
      <section class="section-row row-6">
        <div class="content-block">
          <span class="num-badge">06</span>
          <h2 class="topic-title">Observability Platforms</h2>
          <p class="def-text">
            Full-spectrum telemetry systems providing a <strong>complete, real-time view of distributed application performance</strong> through unified metrics, logs, and traces.
          </p>
          <div class="impact-callout">
            <span class="impact-tag">Operational Impact</span>
            Drives <strong>proactive issue detection and automated triage</strong>, drastically minimizing Mean Time to Resolution (MTTR) before outages occur.
          </div>
        </div>

        <div class="graphic-hub">
          <div class="main-emblem">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          </div>
          <span class="tools-label">Real-World Platforms</span>
          <div class="tools-row">
            <span class="tool-chip">
              {svg_cache.get('prometheus', '')}
              Prometheus
            </span>
            <span class="tool-chip">
              {svg_cache.get('grafana', '')}
              Grafana
            </span>
          </div>
        </div>
      </section>

    </div>

    <!-- Strategic Synthesis Conclusion -->
    <section class="conclusion-section">
      <span class="conclusion-tag">Strategic Architectural Synthesis</span>
      <h3 class="conclusion-heading">The Modern Enterprise Architecture</h3>
      <p class="conclusion-body">
        Adopting and integrating these emerging technologies transcends isolated IT upgrades: <strong>orchestrated together, they directly forge more agile, scalable, and resilient architectures</strong> capable of accelerating business innovation.
      </p>
      <div class="conclusion-triad">
        <div class="triad-pill">
          <span class="triad-dot dot-1"></span>
          Agile Architecture
        </div>
        <div class="triad-pill">
          <span class="triad-dot dot-2"></span>
          Scalable Infrastructure
        </div>
        <div class="triad-pill">
          <span class="triad-dot dot-3"></span>
          Resilient Operations
        </div>
      </div>
    </section>

    <!-- Academic Metadata Footer -->
    <footer class="academic-footer">
      <div>UIDE • Faculty of Technical Sciences</div>
      <div class="footer-highlight">Enterprise &amp; Industrial Architecture (05-SIN-A) • Eng. Iván Reyes Chacón</div>
    </footer>

  </div>

</body>
</html>
"""

# Write HTML file
main_html = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial.html")
with open(main_html, "w", encoding="utf-8") as f:
    f.write(html_content)

shutil.copy(main_html, os.path.join(output_dir, "Infografia_Arquitectura_Empresarial.html"))

print("HTML written. Rendering PNG and PDF...")

png_out = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial.png")
pdf_out = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial.pdf")
url_path = "file:///" + main_html.replace("\\", "/")

# Render high-res PNG (window size 940px wide, 2900px high)
subprocess.run([
    edge_path,
    "--headless",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=940,2920",
    f"--screenshot={png_out}",
    url_path
], check=True)

# Render vector PDF
subprocess.run([
    edge_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_out}",
    "--no-pdf-header-footer",
    url_path
], check=True)

shutil.copy(png_out, os.path.join(output_dir, "Infografia_Arquitectura_Empresarial.png"))
shutil.copy(pdf_out, os.path.join(output_dir, "Infografia_Arquitectura_Empresarial.pdf"))

print(f"PNG rendered: {png_out} ({os.path.getsize(png_out):,} bytes)")
print(f"PDF rendered: {pdf_out} ({os.path.getsize(pdf_out):,} bytes)")
