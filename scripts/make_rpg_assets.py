import os
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
ASSETS = os.path.join(ROOT, "assets")

BASE_URL = "https://raw.githubusercontent.com/AgriciDaniel/AgriciDaniel/main/assets"

def get_base(filename):
    local_path = os.path.join(ASSETS, f"agrici-{filename}")
    if not os.path.exists(local_path):
        url = f"{BASE_URL}/{filename}"
        print(f"Fetching {url}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(content)
    with open(local_path, "r", encoding="utf-8") as f:
        return f.read()

def patch_hero():
    svg = get_base("hero.svg")

    with open(os.path.join(HERE, "press_start.woff2"), "rb") as f:
        press_b64 = urllib.request.base64.b64encode(f.read()).decode("ascii") if hasattr(urllib.request, "base64") else __import__("base64").b64encode(f.read()).decode("ascii")
    with open(os.path.join(HERE, "silkscreen_bold.woff2"), "rb") as f:
        silk_b64 = __import__("base64").b64encode(f.read()).decode("ascii")

    # Meta
    svg = svg.replace(
        'aria-label="Agrici Daniel. Open-source Claude Code skills for SEO, paid ads, blog content and second brains. Click to light the bonfire."',
        'aria-label="Andi Sakta Rifki. Fullstack Developer &amp; Automation Specialist. Click to light the bonfire."'
    )
    svg = svg.replace(
        '<title>Agrici Daniel. Open-source Claude Code skills for SEO, paid ads, blog content and second brains. Click to light the bonfire.</title>',
        '<title>Andi Sakta Rifki. Fullstack Developer &amp; Automation Specialist. Click to light the bonfire.</title>'
    )
    
    # Tagline
    svg = svg.replace("LV 99  AI MARKETING SYSTEMS ARCHITECT",
                      "LV 77  FULLSTACK DEVELOPER")
    
    font_css = f"""@font-face {{
  font-family: 'PressStart';
  src: url(data:font/woff2;base64,{press_b64}) format('woff2');
  font-weight: 700;
  font-style: normal;
}}
@font-face {{
  font-family: 'SilkTag';
  src: url(data:font/woff2;base64,{silk_b64}) format('woff2');
  font-weight: 700;
  font-style: normal;
}}"""
    svg = re.sub(r"@font-face\{font-family:'N'[^}]+format\('woff2'\);\}", font_css, svg)

    # Styles - genuine arcade pixel font without blurry double shadow
    svg = re.sub(r"\.tg\{[^}]+\}", ".tg{font:700 18px 'SilkTag', monospace;fill:#ffcd75;letter-spacing:4px}", svg)
    svg = re.sub(r"\.nm\{[^}]+\}", ".nm{font:700 32px 'PressStart', monospace;fill:#f4f4f4;letter-spacing:1px}", svg)
    svg = re.sub(r"\.nms\{[^}]+\}", ".nms{display:none}", svg)
    
    # Replace name and remove duplicate shadow text
    svg = svg.replace(
        '<text x="294" y="180" class="nms">Agrici Daniel</text><text x="290" y="174" class="nm">Agrici Daniel</text>',
        '<text x="270" y="168" class="nm">Andi Sakta Rifki</text>'
    )

    # Shift 3 figures closer to name (26px gap)
    figures_pattern = re.compile(
        r'(<g><path d="M846 144.+?<g class="bk2"><rect x="902" y="136" width="4" height="4" fill="#7ED957"/><rect x="910" y="136" width="4" height="4" fill="#7ED957"/></g>)',
        re.DOTALL
    )
    m = figures_pattern.search(svg)
    if m:
        figures_html = m.group(1)
        wrapped = f'<g id="figures" transform="translate(-18, 0)">{figures_html}</g>'
        svg = svg.replace(figures_html, wrapped)

    dst = os.path.join(ASSETS, "hero.svg")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Created hero.svg")

def patch_boss():
    svg = get_base("boss.svg")

    # Aria label & title - escape ampersands!
    svg = svg.replace(
        "Boss fight: the $10K/month agency retainer throws hidden fees, a Monthly Report PDF, a Strategy Call and Scope Creep; claude-seo, claude-ads and claude-blog beat each one, and their open-source combo fells it for an MIT license",
        "Boss fight: The Legacy Monolith &amp; Chaotic Spreadsheets throws manual tasks, broken formulas and spaghetti code; Fullstack, Automation and Agentic AI beat each one, and modern velocity fells it forever"
    )
    
    # Boss name on screen
    svg = svg.replace("THE $10K/MO AGENCY RETAINER", "THE LEGACY MONOLITH &amp; SPREADSHEETS")
    svg = svg.replace("The Retainer", "The Monolith")
    
    # Dialogues
    svg = svg.replace("MONTHLY REPORT PDF!", "CHAOTIC SPREADSHEET!")
    svg = svg.replace("claude-seo used TECHNICAL AUDIT!", "Fullstack Knight used REFACTOR!")
    svg = svg.replace("claude-ads used SCORED REPORT!", "Automation Alchemist used PYTHON!")
    svg = svg.replace("The PDF had no real numbers.", "Manual task automated in 0.2s.")
    svg = svg.replace("STRATEGY CALL!", "SPAGHETTI CODE!")
    svg = svg.replace("claude-blog used PUBLISH!", "Metrics Oracle used DASHBOARD!")
    svg = svg.replace("That call could have been a post.", "Real-time metrics visualised.")
    svg = svg.replace("PHASE 2: 12-MONTH LOCK-IN", "PHASE 2: LEGACY MELTDOWN")
    svg = svg.replace("The Retainer renewed itself!", "The Monolith destabilized!")
    svg = svg.replace("SCOPE CREEP!", "DATA CORRUPTION!")
    svg = svg.replace("claude-seo parries. Riposte!", "AI Artificer parries with Agentic AI!")
    svg = svg.replace("COMBO: OPEN SOURCE!", "COMBO: FULL AUTOMATION!")
    svg = svg.replace("MIT licensed. Free forever.", "Zero-click workflows active.")
    svg = svg.replace("Received: MIT License (x99)", "Received: 100+ Hours Saved/Mo")
    svg = svg.replace("+$10K/mo back in your pocket.", "System running at 10x velocity.")

    # Actions list on right
    svg = svg.replace(">claude-seo<", ">Fullstack<")
    svg = svg.replace(">claude-ads<", ">Automation<")
    svg = svg.replace(">claude-blog<", ">Metrics<")
    svg = svg.replace(">Audit<", ">Laravel<")
    svg = svg.replace(">Report<", ">Python<")
    svg = svg.replace(">Publish<", ">Oracle<")
    svg = svg.replace(">Open Source<", ">Agentic<")

    # Font fallbacks
    svg = svg.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    svg = svg.replace("font:700 18px S;", "font:700 16px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    svg = svg.replace("font:500 15px S;", "font:600 14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")

    dst = os.path.join(ASSETS, "boss.svg")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Created boss.svg")

def make_cards():
    tmpl = get_base("card-claude-seo.svg")

    # Card 1: Fullstack Knight
    c1 = tmpl
    c1 = c1.replace(
        "claude-seo, the Knight class: you run an seo agency. 23K GitHub stars.",
        "Fullstack Knight: Modern Web Applications. Laravel, React, Express, PHP &amp; SQL."
    )
    c1 = c1.replace(">KNIGHT<", ">FULLSTACK KNIGHT<")
    c1 = c1.replace(">claude-seo<", ">Web Developer<")
    c1 = c1.replace(">You run an SEO agency<", ">Laravel · React · Express · SQL<")
    c1 = c1.replace(">23K<", ">LV 99<")
    c1 = c1.replace(">STARS<", ">CLASS<")
    c1 = c1.replace("font:700 40px N;", "font:900 32px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c1 = c1.replace("font:500 20px D;", "font:600 16px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c1 = c1.replace("font:13px S;", "font:700 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c1 = c1.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    with open(os.path.join(ASSETS, "card-fullstack.svg"), "w", encoding="utf-8") as f:
        f.write(c1)

    # Card 2: Automation Alchemist
    c2 = tmpl
    c2 = c2.replace(
        "claude-seo, the Knight class: you run an seo agency. 23K GitHub stars.",
        "Automation Alchemist: Zero-Click Workflows. Python &amp; Google Apps Script."
    )
    c2 = c2.replace(">KNIGHT<", ">AUTOMATION ALCHEMIST<")
    c2 = c2.replace(">claude-seo<", ">Process Automator<")
    c2 = c2.replace(">You run an SEO agency<", ">Python · Google Apps Script · Bots<")
    c2 = c2.replace(">23K<", ">100%<")
    c2 = c2.replace(">STARS<", ">AUTO<")
    c2 = c2.replace('fill="#F44336"', 'fill="#10b981"')
    c2 = c2.replace('fill="#22306a"', 'fill="#065f46"')
    c2 = c2.replace('fill="#3b5dc9"', 'fill="#059669"')
    c2 = c2.replace("font:700 40px N;", "font:900 32px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c2 = c2.replace("font:500 20px D;", "font:600 16px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c2 = c2.replace("font:13px S;", "font:700 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c2 = c2.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    with open(os.path.join(ASSETS, "card-automation.svg"), "w", encoding="utf-8") as f:
        f.write(c2)

    # Card 3: Metrics Oracle
    c3 = tmpl
    c3 = c3.replace(
        "claude-seo, the Knight class: you run an seo agency. 23K GitHub stars.",
        "Metrics Oracle: Interactive Dashboards &amp; Analytics. BNSP Data Science."
    )
    c3 = c3.replace(">KNIGHT<", ">METRICS ORACLE<")
    c3 = c3.replace(">claude-seo<", ">Data &amp; Dashboard<")
    c3 = c3.replace(">You run an SEO agency<", ">Interactive BI · Analytics · BNSP<")
    c3 = c3.replace(">23K<", ">BNSP<")
    c3 = c3.replace(">STARS<", ">DATA<")
    c3 = c3.replace('fill="#F44336"', 'fill="#8b5cf6"')
    c3 = c3.replace('fill="#22306a"', 'fill="#4c1d95"')
    c3 = c3.replace('fill="#3b5dc9"', 'fill="#6d28d9"')
    c3 = c3.replace("font:700 40px N;", "font:900 32px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c3 = c3.replace("font:500 20px D;", "font:600 16px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c3 = c3.replace("font:13px S;", "font:700 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c3 = c3.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    with open(os.path.join(ASSETS, "card-metrics.svg"), "w", encoding="utf-8") as f:
        f.write(c3)

    # Card 4: AI Artificer
    c4 = tmpl
    c4 = c4.replace(
        "claude-seo, the Knight class: you run an seo agency. 23K GitHub stars.",
        "AI Artificer: Agentic AI Engineering. Claude Code, Codex, Antigravity."
    )
    c4 = c4.replace(">KNIGHT<", ">AI ARTIFICER<")
    c4 = c4.replace(">claude-seo<", ">Agentic AI<")
    c4 = c4.replace(">You run an SEO agency<", ">Claude Code · Codex · Antigravity<")
    c4 = c4.replace(">23K<", ">10X<")
    c4 = c4.replace(">STARS<", ">SPEED<")
    c4 = c4.replace('fill="#F44336"', 'fill="#f59e0b"')
    c4 = c4.replace('fill="#22306a"', 'fill="#78350f"')
    c4 = c4.replace('fill="#3b5dc9"', 'fill="#d97706"')
    c4 = c4.replace("font:700 40px N;", "font:900 32px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c4 = c4.replace("font:500 20px D;", "font:600 16px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c4 = c4.replace("font:13px S;", "font:700 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    c4 = c4.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    with open(os.path.join(ASSETS, "card-agentic.svg"), "w", encoding="utf-8") as f:
        f.write(c4)
    print("Created 4 Class cards")

def patch_stack():
    svg = get_base("stack.svg")

    replacements = [
        ("Claude Code", "Laravel"),
        ("Codex", "React"),
        ("Gemini", "Express.js"),
        ("MCP", "JavaScript"),
        ("Python", "Python"),
        ("Obsidian", "Google Apps Script"),
        ("Google Ads", "MySQL"),
        ("Meta Ads", "PostgreSQL"),
        ("WordPress", "Claude Code"),
        ("n8n", "Codex"),
        ("FFmpeg", "Antigravity"),
        ("TypeScript", "PHP"),
        ("React", "Figma"),
        ("PHP", "WordPress"),
        ("Bash", "Git &amp; Bash"),  # MUST BE ESCAPED!
        ("YouTube", "sktafolio.my.id"),
    ]
    for old, new in replacements:
        svg = svg.replace(f">{old}<", f">{new}<")

    svg = svg.replace(
        'Tech stack: Claude Code, Codex, Gemini, MCP, Python, Obsidian, Google Ads, Meta Ads, WordPress, n8n, FFmpeg, TypeScript, React, PHP, Bash, YouTube',
        'Tech stack: Laravel, React, Express.js, JavaScript, Python, Google Apps Script, MySQL, PostgreSQL, Claude Code, Codex, Antigravity, PHP, Figma, WordPress, Git, sktafolio'
    )

    svg = svg.replace("font:700 24px S;", "font:800 22px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    svg = svg.replace("font:500 18px D;", "font:700 18px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")

    dst = os.path.join(ASSETS, "stack.svg")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Created stack.svg")

def make_buttons():
    btn_w = get_base("btn-website.svg")
    
    # Portfolio
    bp = btn_w.replace("Website", "Portfolio")
    bp = bp.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    with open(os.path.join(ASSETS, "btn-portfolio.svg"), "w", encoding="utf-8") as f:
        f.write(bp)

    # LinkedIn
    btn_l = get_base("btn-linkedin.svg")
    bl = btn_l.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    with open(os.path.join(ASSETS, "btn-linkedin.svg"), "w", encoding="utf-8") as f:
        f.write(bl)

    # Instagram
    bi = btn_l.replace("LinkedIn", "Instagram")
    bi = bi.replace('fill="#41a6f6"', 'fill="#e1306c"')
    bi = bi.replace('viewBox="0 0 201 64" width="201"', 'viewBox="0 0 216 64" width="216"')
    bi = bi.replace('width="193"', 'width="208"')
    bi = bi.replace('width="185"', 'width="200"')
    bi = bi.replace('x="197"', 'x="212"')
    bi = bi.replace('x="193"', 'x="208"')
    bi = bi.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    with open(os.path.join(ASSETS, "btn-instagram.svg"), "w", encoding="utf-8") as f:
        f.write(bi)

    # GitHub
    bg = btn_w.replace("Website", "GitHub")
    bg = bg.replace('fill="#73eff7"', 'fill="#a78bfa"')
    bg = bg.replace('viewBox="0 0 197 64" width="197"', 'viewBox="0 0 185 64" width="185"')
    bg = bg.replace('width="189"', 'width="177"')
    bg = bg.replace('width="181"', 'width="169"')
    bg = bg.replace('x="193"', 'x="181"')
    bg = bg.replace('x="189"', 'x="177"')
    bg = bg.replace("font:700 24px N;", "font:800 20px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;")
    with open(os.path.join(ASSETS, "btn-github.svg"), "w", encoding="utf-8") as f:
        f.write(bg)

    print("Created buttons")

def validate_all_svgs():
    print("\n--- Validating XML of all SVGs ---")
    all_ok = True
    for item in sorted(os.listdir(ASSETS)):
        if not item.endswith(".svg") or item.startswith("agrici-"):
            continue
        path = os.path.join(ASSETS, item)
        try:
            ET.parse(path)
            print(f"[OK] Valid XML: {item}")
        except Exception as e:
            print(f"[ERR] INVALID XML: {item} -> {e}")
            all_ok = False
    return all_ok

if __name__ == "__main__":
    patch_hero()
    patch_boss()
    make_cards()
    patch_stack()
    make_buttons()
    
    # Cleanup downloaded base templates
    for item in os.listdir(ASSETS):
        if item.startswith("agrici-"):
            os.remove(os.path.join(ASSETS, item))
            
    success = validate_all_svgs()
    if success:
        print("\nAll SVG assets are 100% valid XML!")
    else:
        raise SystemExit(1)
