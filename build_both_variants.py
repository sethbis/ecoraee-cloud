import os
import urllib.request
import subprocess
import json
import re
import shutil

base_dir = r"c:\Users\nicol\OneDrive\Documentos\integrador 5to semestre"
output_dir = os.path.join(base_dir, "06_ARQUITECTURA_EMPRESARIAL_TO-BE", "Infografia_Tecnologias_Emergentes")
os.makedirs(output_dir, exist_ok=True)
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 1. Official brand SVGs
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

# Data structure for both languages
data = {
    'en': {
        'page_title': 'Enterprise Architecture: Next-Gen Technology Pillars',
        'badge_header': 'Enterprise & Industrial Architecture',
        'header_tag': 'Next-Generation Enterprise Stack',
        'header_title': 'Emerging Technologies in Enterprise Architecture',
        'header_subtitle': 'Modernizing IT ecosystems through decoupled, intelligent, and scalable distributed paradigms designed for business agility.',
        'metrics': [
            ('6', 'Strategic Pillars', 'Enterprise Ready', 'var(--cyan)'),
            ('<20%', 'Cognitive Density', 'High-Retention Focus', 'var(--purple)'),
            ('0%', 'AI Clichés / Fluff', 'Pure Vector Assets', 'var(--emerald)'),
            ('3x', 'Operational Agility', 'Decoupled Speed', 'var(--amber)')
        ],
        'pillars': [
            {
                'id': '01',
                'title': 'Event-Driven Architecture',
                'class': 'card-eda',
                'icon': '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
                'def_title': 'Definition',
                'def_text': 'A software architecture pattern where decoupled components communicate through the production, detection, and consumption of <strong>asynchronous real-time events</strong>.',
                'tools_title': 'Real-World Tools',
                'tools': [('kafka', 'Apache Kafka'), ('rabbitmq', 'RabbitMQ')],
                'impact_title': 'Operational Impact',
                'impact_text': 'Eliminates blocking bottlenecks, drastically improving <strong>high-availability resilience</strong> and linear <strong>horizontal scalability</strong> under spiky workloads.'
            },
            {
                'id': '02',
                'title': 'AI & Machine Learning',
                'class': 'card-ai',
                'icon': '<path d="M12 2a4 4 0 0 1 4 4v1a4 4 0 0 1-4 4 4 4 0 0 1-4-4V6a4 4 0 0 1 4-4z"/><path d="M16 11.37A4 4 0 1 1 12.63 8"/><path d="M12 18v4"/><path d="M8 22h8"/>',
                'def_title': 'Definition',
                'def_text': 'Mathematical models and algorithms that learn from data patterns to <strong>automate complex cognitive tasks</strong> and continuously optimize business workflows.',
                'tools_title': 'Real-World Tools',
                'tools': [('tensorflow', 'TensorFlow'), ('aws', 'AWS SageMaker')],
                'impact_title': 'Operational Impact',
                'impact_text': 'Empowers <strong>predictive decision-making</strong> with sub-second insights while bolstering <strong>proactive cybersecurity</strong> via automated anomaly detection.'
            },
            {
                'id': '03',
                'title': 'Serverless Computing',
                'class': 'card-serverless',
                'icon': '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>',
                'def_title': 'Definition',
                'def_text': 'Cloud execution model that runs application logic on-demand <strong>without managing or provisioning servers</strong>, abstracting infrastructure maintenance entirely.',
                'tools_title': 'Real-World Tools',
                'tools': [('lambda', 'AWS Lambda'), ('azure', 'Azure Functions')],
                'impact_title': 'Operational Impact',
                'impact_text': 'Shifts engineering priority from <strong>infrastructure patching to code delivery</strong>, enabling zero-idle costs and automatic scale-to-zero agility.'
            },
            {
                'id': '04',
                'title': 'Enterprise Blockchain',
                'class': 'card-blockchain',
                'icon': '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><line x1="10" y1="6.5" x2="14" y2="6.5"/><line x1="17.5" y1="10" x2="17.5" y2="14"/><line x1="14" y1="17.5" x2="10" y2="17.5"/><line x1="6.5" y1="14" x2="6.5" y2="10"/>',
                'def_title': 'Definition',
                'def_text': 'A decentralized, cryptographically shared ledger characterized by triple pillars: <strong>ironclad security, radical transparency, and immutability</strong>.',
                'tools_title': 'Real-World Tools',
                'tools': [('hyperledger', 'Hyperledger Fabric'), ('custom_dlt', 'Enterprise DLT')],
                'impact_title': 'Operational Impact',
                'impact_text': 'Revolutionizes multi-party <strong>supply chain asset tracking</strong> while providing cryptographically verifiable, <strong>tamper-proof data integrity</strong>.'
            },
            {
                'id': '05',
                'title': 'API Management',
                'class': 'card-api',
                'icon': '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><line x1="6" y1="9" x2="6" y2="21"/>',
                'def_title': 'Definition',
                'def_text': 'Comprehensive architectural gateway for publishing, securing, and governing interfaces <strong>crucial for microservices integration</strong> across hybrid clouds.',
                'tools_title': 'Real-World Tools',
                'tools': [('googlecloud', 'Google Apigee'), ('mulesoft', 'MuleSoft Anypoint')],
                'impact_title': 'Operational Impact',
                'impact_text': 'Enforces <strong>Zero-Trust security</strong>, guarantees high-throughput scalability via rate-limiting, and accelerates enterprise <strong>service reusability</strong>.'
            },
            {
                'id': '06',
                'title': 'Observability Platforms',
                'class': 'card-obs',
                'icon': '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
                'def_title': 'Definition',
                'def_text': 'Full-spectrum telemetric telemetry (metrics, distributed traces, and logs) that provides a <strong>complete real-time view of distributed systems</strong>.',
                'tools_title': 'Real-World Tools',
                'tools': [('prometheus', 'Prometheus'), ('grafana', 'Grafana')],
                'impact_title': 'Operational Impact',
                'impact_text': 'Drives <strong>proactive issue detection and automated triage</strong>, slashing Mean Time to Resolution (MTTR) before business degradation occurs.'
            }
        ],
        'conclusion_tag': 'Architectural Synthesis & Strategic Value',
        'conclusion_title': 'The Foundation of the Modern Enterprise Ecosystem',
        'conclusion_statement': 'In modern Enterprise Architecture, adopting these six emerging technologies transcends individual technical upgrades: <strong>orchestrated together, they forge radically more agile, scalable, and resilient enterprise architectures</strong> capable of thriving amidst continuous business disruption.',
        'pills': [
            ('pi-agile', 'Agility: Decoupled & Event-Driven'),
            ('pi-scalable', 'Scalability: Serverless & Auto-Elastic'),
            ('pi-resilient', 'Resilience: Observable & Immutable')
        ],
        'lang_toggle_label': 'Español',
        'lang_toggle_target': 'Infografia_Arquitectura_Empresarial_ES.html',
        'print_label': 'Export PDF / Print'
    },
    'es': {
        'page_title': 'Arquitectura Empresarial: Pilares Tecnológicos de Próxima Generación',
        'badge_header': 'Arquitectura Empresarial e Industrial',
        'header_tag': 'Stack Tecnológico de Próxima Generación',
        'header_title': 'Tecnologías Emergentes en Arquitectura Empresarial',
        'header_subtitle': 'Modernización de ecosistemas de TI mediante paradigmas distribuidos, desacoplados e inteligentes diseñados para la agilidad del negocio.',
        'metrics': [
            ('6', 'Pilares Estratégicos', 'Listos para Producción', 'var(--cyan)'),
            ('<20%', 'Densidad de Texto', 'Máxima Retención Visual', 'var(--purple)'),
            ('0%', 'Clichés de IA', 'Activos Vectoriales Puros', 'var(--emerald)'),
            ('3x', 'Agilidad Operativa', 'Velocidad Desacoplada', 'var(--amber)')
        ],
        'pillars': [
            {
                'id': '01',
                'title': 'Arquitectura Orientada a Eventos',
                'class': 'card-eda',
                'icon': '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
                'def_title': 'Definición',
                'def_text': 'Patrón arquitectónico donde componentes desacoplados se comunican mediante la producción, detección y consumo de <strong>eventos asíncronos en tiempo real</strong>.',
                'tools_title': 'Herramientas Reales',
                'tools': [('kafka', 'Apache Kafka'), ('rabbitmq', 'RabbitMQ')],
                'impact_title': 'Impacto Operativo',
                'impact_text': 'Elimina cuellos de botella bloqueantes, elevando drásticamente la <strong>resiliencia y alta disponibilidad</strong> junto con una <strong>escalabilidad horizontal lineal</strong> ante picos de demanda.'
            },
            {
                'id': '02',
                'title': 'Inteligencia Artificial y Machine Learning',
                'class': 'card-ai',
                'icon': '<path d="M12 2a4 4 0 0 1 4 4v1a4 4 0 0 1-4 4 4 4 0 0 1-4-4V6a4 4 0 0 1 4-4z"/><path d="M16 11.37A4 4 0 1 1 12.63 8"/><path d="M12 18v4"/><path d="M8 22h8"/>',
                'def_title': 'Definición',
                'def_text': 'Modelos matemáticos y algoritmos que aprenden patrones de datos para <strong>automatizar tareas cognitivas complejas</strong> y optimizar flujos empresariales.',
                'tools_title': 'Herramientas Reales',
                'tools': [('tensorflow', 'TensorFlow'), ('aws', 'AWS SageMaker')],
                'impact_title': 'Impacto Operativo',
                'impact_text': 'Potencia la <strong>toma de decisiones predictiva</strong> en tiempo real y fortalece la <strong>ciberseguridad proactiva</strong> mediante detección automatizada de anomalías.'
            },
            {
                'id': '03',
                'title': 'Computación Serverless',
                'class': 'card-serverless',
                'icon': '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>',
                'def_title': 'Definición',
                'def_text': 'Modelo de ejecución en la nube que ejecuta lógica bajo demanda <strong>sin administrar servidores</strong>, abstrayendo por completo el mantenimiento de infraestructura.',
                'tools_title': 'Herramientas Reales',
                'tools': [('lambda', 'AWS Lambda'), ('azure', 'Azure Functions')],
                'impact_title': 'Impacto Operativo',
                'impact_text': 'Traslada el enfoque de <strong>mantener infraestructura a generar código de negocio</strong>, logrando costos cero en reposo y autoescalado instantáneo.'
            },
            {
                'id': '04',
                'title': 'Blockchain Empresarial',
                'class': 'card-blockchain',
                'icon': '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><line x1="10" y1="6.5" x2="14" y2="6.5"/><line x1="17.5" y1="10" x2="17.5" y2="14"/><line x1="14" y1="17.5" x2="10" y2="17.5"/><line x1="6.5" y1="14" x2="6.5" y2="10"/>',
                'def_title': 'Definición',
                'def_text': 'Libro mayor descentralizado y compartido criptográficamente caracterizado por tres pilares: <strong>seguridad blindada, transparencia total e inmutabilidad</strong>.',
                'tools_title': 'Herramientas Reales',
                'tools': [('hyperledger', 'Hyperledger Fabric'), ('custom_dlt', 'Enterprise DLT')],
                'impact_title': 'Impacto Operativo',
                'impact_text': 'Revoluciona el <strong>rastreo de activos multiparte</strong> en cadenas de suministro y garantiza una <strong>integridad de datos a prueba de manipulación</strong>.'
            },
            {
                'id': '05',
                'title': 'Gestión de APIs (API Management)',
                'class': 'card-api',
                'icon': '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><line x1="6" y1="9" x2="6" y2="21"/>',
                'def_title': 'Definición',
                'def_text': 'Pasarela arquitectónica integral para publicar, proteger y gobernar interfaces <strong>cruciales para la integración de microservicios</strong> híbridos.',
                'tools_title': 'Herramientas Reales',
                'tools': [('googlecloud', 'Google Apigee'), ('mulesoft', 'MuleSoft Anypoint')],
                'impact_title': 'Impacto Operativo',
                'impact_text': 'Garantiza <strong>seguridad Zero-Trust</strong>, asegura alta escalabilidad mediante control de tráfico y maximiza la <strong>reutilización de servicios</strong>.'
            },
            {
                'id': '06',
                'title': 'Plataformas de Observabilidad',
                'class': 'card-obs',
                'icon': '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
                'def_title': 'Definición',
                'def_text': 'Telemetría de espectro completo (métricas, trazas distribuidas y logs) que brinda una <strong>visión integral en tiempo real de sistemas distribuidos</strong>.',
                'tools_title': 'Herramientas Reales',
                'tools': [('prometheus', 'Prometheus'), ('grafana', 'Grafana')],
                'impact_title': 'Impacto Operativo',
                'impact_text': 'Habilita la <strong>detección proactiva de incidentes y resolución rápida (MTTR)</strong> mucho antes de que impacten a los usuarios de negocio.'
            }
        ],
        'conclusion_tag': 'Síntesis Arquitectónica y Valor Estratégico',
        'conclusion_title': 'Los Cimientos del Ecosistema Empresarial Moderno',
        'conclusion_statement': 'En la Arquitectura Empresarial moderna, adoptar estas seis tecnologías emergentes trasciende mejoras técnicas aisladas: <strong>orquestadas en conjunto, forjan arquitecturas radicalmente más ágiles, escalables y resilientes</strong> capaces de prosperar ante la disrupción continua del mercado.',
        'pills': [
            ('pi-agile', 'Agilidad: Desacople Orientado a Eventos'),
            ('pi-scalable', 'Escalabilidad: Serverless y Auto-Elástica'),
            ('pi-resilient', 'Resilience: Observable e Inmutable')
        ],
        'lang_toggle_label': 'English',
        'lang_toggle_target': 'Infografia_Arquitectura_Empresarial.html',
        'print_label': 'Exportar PDF / Imprimir'
    }
}

css_common = """
    :root {
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
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
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
    }

    .infographic-wrapper {
      max-width: 1280px;
      width: 100%;
      margin: 0 auto;
    }

    .action-bar {
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
    }

    .badge-pill {
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
    }

    .badge-pill .pulse-dot {
      width: 7px;
      height: 7px;
      background: var(--cyan);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--cyan);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    .controls-group {
      display: flex;
      gap: 12px;
    }

    .btn {
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
      text-decoration: none;
    }

    .btn:hover {
      background: rgba(255, 255, 255, 0.12);
      border-color: var(--border-hover);
      transform: translateY(-1px);
    }

    .btn-primary {
      background: linear-gradient(135deg, #06B6D4, #3B82F6);
      border: none;
      color: #FFFFFF;
      box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3);
    }

    .btn-primary:hover {
      box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5);
    }

    .header {
      text-align: center;
      margin-bottom: 40px;
      position: relative;
    }

    .header-tag {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--cyan);
      margin-bottom: 12px;
      display: block;
    }

    .header-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 42px;
      font-weight: 700;
      letter-spacing: -0.02em;
      line-height: 1.15;
      margin-bottom: 14px;
      background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .header-subtitle {
      font-size: 16.5px;
      color: var(--text-secondary);
      max-width: 780px;
      margin: 0 auto;
      font-weight: 400;
    }

    .metrics-bar {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 38px;
    }

    .metric-chip {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .metric-value {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 28px;
      font-weight: 700;
      line-height: 1;
    }

    .metric-label {
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
    }

    .grid-technologies {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 40px;
    }

    @media (max-width: 1080px) {
      .grid-technologies { grid-template-columns: repeat(2, 1fr); }
      .metrics-bar { grid-template-columns: repeat(2, 1fr); }
    }

    @media (max-width: 720px) {
      .grid-technologies { grid-template-columns: 1fr; }
      .header-title { font-size: 30px; }
      .metrics-bar { grid-template-columns: 1fr; }
    }

    .tech-card {
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
    }

    .tech-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: transparent;
      transition: background 0.3s ease;
    }

    .tech-card:hover {
      transform: translateY(-4px);
      border-color: var(--border-hover);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
    }

    .card-eda:hover::before { background: linear-gradient(90deg, var(--cyan), transparent); }
    .card-eda:hover { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--cyan-glow); }
    .card-eda .tech-accent { color: var(--cyan); }
    .card-eda .icon-wrapper { background: rgba(6, 182, 212, 0.12); color: var(--cyan); border-color: rgba(6, 182, 212, 0.3); }

    .card-ai:hover::before { background: linear-gradient(90deg, var(--purple), transparent); }
    .card-ai:hover { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--purple-glow); }
    .card-ai .tech-accent { color: var(--purple); }
    .card-ai .icon-wrapper { background: rgba(139, 92, 246, 0.12); color: var(--purple); border-color: rgba(139, 92, 246, 0.3); }

    .card-serverless:hover::before { background: linear-gradient(90deg, var(--amber), transparent); }
    .card-serverless:hover { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--amber-glow); }
    .card-serverless .tech-accent { color: var(--amber); }
    .card-serverless .icon-wrapper { background: rgba(245, 158, 11, 0.12); color: var(--amber); border-color: rgba(245, 158, 11, 0.3); }

    .card-blockchain:hover::before { background: linear-gradient(90deg, var(--emerald), transparent); }
    .card-blockchain:hover { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--emerald-glow); }
    .card-blockchain .tech-accent { color: var(--emerald); }
    .card-blockchain .icon-wrapper { background: rgba(16, 185, 129, 0.12); color: var(--emerald); border-color: rgba(16, 185, 129, 0.3); }

    .card-api:hover::before { background: linear-gradient(90deg, var(--blue), transparent); }
    .card-api:hover { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--blue-glow); }
    .card-api .tech-accent { color: var(--blue); }
    .card-api .icon-wrapper { background: rgba(59, 130, 246, 0.12); color: var(--blue); border-color: rgba(59, 130, 246, 0.3); }

    .card-obs:hover::before { background: linear-gradient(90deg, var(--rose), transparent); }
    .card-obs:hover { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px var(--rose-glow); }
    .card-obs .tech-accent { color: var(--rose); }
    .card-obs .icon-wrapper { background: rgba(244, 63, 94, 0.12); color: var(--rose); border-color: rgba(244, 63, 94, 0.3); }

    .card-header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 18px;
    }

    .icon-wrapper {
      width: 48px;
      height: 48px;
      border-radius: 14px;
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .icon-wrapper svg {
      width: 24px;
      height: 24px;
      stroke-width: 2;
    }

    .card-title-group {
      flex: 1;
    }

    .card-tag {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      display: block;
      margin-bottom: 2px;
    }

    .card-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 19.5px;
      font-weight: 700;
      color: #FFFFFF;
      letter-spacing: -0.01em;
    }

    .section-block {
      margin-bottom: 16px;
    }

    .section-block:last-child {
      margin-bottom: 0;
    }

    .block-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .block-label svg {
      width: 13px;
      height: 13px;
      opacity: 0.8;
    }

    .block-text {
      font-size: 13.5px;
      color: var(--text-secondary);
      line-height: 1.55;
    }

    .block-text strong {
      color: #FFFFFF;
      font-weight: 600;
    }

    .tools-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 4px;
    }

    .tool-badge {
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
    }

    .tool-badge:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.25);
      transform: translateY(-1px);
    }

    .tool-badge svg {
      width: 17px;
      height: 17px;
      flex-shrink: 0;
    }

    .impact-box {
      background: rgba(0, 0, 0, 0.3);
      border-left: 3px solid;
      border-radius: 0 10px 10px 0;
      padding: 12px 14px;
      margin-top: auto;
    }

    .card-eda .impact-box { border-left-color: var(--cyan); }
    .card-ai .impact-box { border-left-color: var(--purple); }
    .card-serverless .impact-box { border-left-color: var(--amber); }
    .card-blockchain .impact-box { border-left-color: var(--emerald); }
    .card-api .impact-box { border-left-color: var(--blue); }
    .card-obs .impact-box { border-left-color: var(--rose); }

    .conclusion-banner {
      background: linear-gradient(135deg, rgba(13, 20, 36, 0.95), rgba(7, 11, 20, 0.95));
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      padding: 30px 34px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }

    .conclusion-banner::after {
      content: '';
      position: absolute;
      top: 0; right: 0; bottom: 0;
      width: 320px;
      background: radial-gradient(circle at 100% 50%, rgba(6, 182, 212, 0.15), transparent 70%);
      pointer-events: none;
    }

    .conclusion-grid {
      display: grid;
      grid-template-columns: 1fr 280px;
      gap: 32px;
      align-items: center;
    }

    @media (max-width: 900px) {
      .conclusion-grid { grid-template-columns: 1fr; }
    }

    .conclusion-tag {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--cyan);
      margin-bottom: 8px;
      display: block;
    }

    .conclusion-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 23px;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 12px;
      line-height: 1.3;
    }

    .conclusion-statement {
      font-size: 14.5px;
      color: var(--text-secondary);
      line-height: 1.6;
    }

    .conclusion-statement strong {
      color: #38BDF8;
      font-weight: 600;
    }

    .pillars-pills {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .pillar-pill {
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
    }

    .pillar-indicator {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .pi-agile { background: var(--cyan); box-shadow: 0 0 8px var(--cyan); }
    .pi-scalable { background: var(--purple); box-shadow: 0 0 8px var(--purple); }
    .pi-resilient { background: var(--emerald); box-shadow: 0 0 8px var(--emerald); }

    .infographic-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 30px;
      padding-top: 18px;
      border-top: 1px solid var(--border-subtle);
      font-size: 12px;
      color: var(--text-muted);
    }

    .team-badge {
      font-weight: 600;
      color: var(--text-secondary);
    }

    @media print {
      body {
        background: #070B14 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        padding: 0 !important;
      }
      .action-bar { display: none !important; }
      .tech-card { break-inside: avoid; page-break-inside: avoid; }
    }
"""

def generate_html_string(lang_code):
    c = data[lang_code]
    
    metrics_html = ""
    for val, lbl, sub, color in c['metrics']:
        metrics_html += f"""
        <div class="metric-chip">
          <div class="metric-value" style="color: {color};">{val}</div>
          <div>
            <div class="metric-label">{lbl}</div>
            <div style="font-size: 11px; color: var(--text-secondary);">{sub}</div>
          </div>
        </div>"""

    cards_html = ""
    for p in c['pillars']:
        tools_html = ""
        for tool_key, tool_name in p['tools']:
            if tool_key == 'custom_dlt':
                tool_svg = '<svg viewBox="0 0 24 24" fill="#10B981"><path d="M12 1.75l-6.5 10.75L12 16.5l6.5-4L12 1.75zM5.5 13.5L12 22.25l6.5-8.75L12 17.5 5.5 13.5z"/></svg>'
            else:
                tool_svg = svg_cache.get(tool_key, '')
            tools_html += f"""
            <div class="tool-badge">
              {tool_svg}
              <span>{tool_name}</span>
            </div>"""

        cards_html += f"""
        <article class="tech-card {p['class']}">
          <div class="card-header">
            <div class="icon-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">{p['icon']}</svg>
            </div>
            <div class="card-title-group">
              <span class="card-tag tech-accent">Pillar {p['id']}</span>
              <h2 class="card-title">{p['title']}</h2>
            </div>
          </div>

          <div class="section-block">
            <div class="block-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
              <span>{p['def_title']}</span>
            </div>
            <p class="block-text">{p['def_text']}</p>
          </div>

          <div class="section-block">
            <div class="block-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              <span>{p['tools_title']}</span>
            </div>
            <div class="tools-container">
              {tools_html}
            </div>
          </div>

          <div class="section-block impact-box">
            <div class="block-label" style="color: var(--cyan);">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>
              <span>{p['impact_title']}</span>
            </div>
            <p class="block-text">{p['impact_text']}</p>
          </div>
        </article>"""

    pills_html = ""
    for pi_cls, pi_txt in c['pills']:
        pills_html += f"""
        <div class="pillar-pill">
          <span class="pillar-indicator {pi_cls}"></span>
          <span>{pi_txt}</span>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c['page_title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <style>{css_common}</style>
</head>
<body>
  <div class="infographic-wrapper">
    <div class="action-bar">
      <div class="badge-pill">
        <span class="pulse-dot"></span>
        <span>{c['badge_header']}</span>
      </div>
      <div class="controls-group">
        <a class="btn" href="{c['lang_toggle_target']}">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span>{c['lang_toggle_label']}</span>
        </a>
        <button class="btn btn-primary" onclick="window.print()">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
          <span>{c['print_label']}</span>
        </button>
      </div>
    </div>

    <header class="header">
      <span class="header-tag">{c['header_tag']}</span>
      <h1 class="header-title">{c['header_title']}</h1>
      <p class="header-subtitle">{c['header_subtitle']}</p>
    </header>

    <div class="metrics-bar">
      {metrics_html}
    </div>

    <main class="grid-technologies">
      {cards_html}
    </main>

    <section class="conclusion-banner">
      <div class="conclusion-grid">
        <div>
          <span class="conclusion-tag">{c['conclusion_tag']}</span>
          <h3 class="conclusion-title">{c['conclusion_title']}</h3>
          <p class="conclusion-statement">{c['conclusion_statement']}</p>
        </div>
        <div class="pillars-pills">
          {pills_html}
        </div>
      </div>
    </section>

    <footer class="infographic-footer">
      <div>
        <span>UIDE — Faculty of Technical Sciences | School of Computer Science & IT</span>
      </div>
      <div class="team-badge">
        <span>Arquitectura Empresarial (05-SIN-A) • Ing. Iván Reyes Chacón</span>
      </div>
    </footer>
  </div>
</body>
</html>"""

# Generate EN
html_en_content = generate_html_string('en')
html_en_path = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial.html")
with open(html_en_path, "w", encoding="utf-8") as f:
    f.write(html_en_content)

# Generate ES
html_es_content = generate_html_string('es')
html_es_path = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial_ES.html")
with open(html_es_path, "w", encoding="utf-8") as f:
    f.write(html_es_content)

# Render screenshots & PDFs for both
for lang, h_path in [('EN', html_en_path), ('ES', html_es_path)]:
    suffix = "" if lang == 'EN' else "_ES"
    png_out = os.path.join(base_dir, f"Infografia_Arquitectura_Empresarial{suffix}.png")
    pdf_out = os.path.join(base_dir, f"Infografia_Arquitectura_Empresarial{suffix}.pdf")
    url_p = "file:///" + h_path.replace("\\", "/")
    
    print(f"Rendering {lang} PNG...")
    subprocess.run([
        edge_path, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--window-size=1440,1720", f"--screenshot={png_out}", url_p
    ], check=True)

    print(f"Rendering {lang} PDF...")
    subprocess.run([
        edge_path, "--headless", "--disable-gpu",
        f"--print-to-pdf={pdf_out}", "--no-pdf-header-footer", url_p
    ], check=True)

    # Copy to destination folder
    shutil.copy(h_path, os.path.join(output_dir, os.path.basename(h_path)))
    shutil.copy(png_out, os.path.join(output_dir, os.path.basename(png_out)))
    shutil.copy(pdf_out, os.path.join(output_dir, os.path.basename(pdf_out)))

print("ALL BUILDS AND RENDERS COMPLETE IN BOTH ENGLISH AND SPANISH!")
