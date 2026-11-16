import re
import subprocess
import os
import markdown

with open('PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Clean up math notation into clear typographic HTML
text = text.replace(r'\mathbf{x}_i', 'x<sub>i</sub>')
text = text.replace(r'\mathbf{w}^T', 'w<sup>T</sup>')
text = text.replace(r'\mathbf{w}', 'w')
text = text.replace(r'\|\mathbf{w}\|_2^2', '||w||₂²')
text = text.replace(r'\alpha', '&alpha;')
text = text.replace(r'\sum_{i=1}^{n}', '&Sigma;<sub>i=1..n</sub>')
text = text.replace(r'\sum_{j}', '&Sigma;<sub>j</sub>')
text = text.replace(r'\min_{\mathbf{w}}', 'min<sub>w</sub>')
text = text.replace(r'\hat{y}', 'y&#770;')
text = text.replace(r'\beta_0', '&beta;<sub>0</sub>')
text = text.replace(r'\beta_j', '&beta;<sub>j</sub>')
text = text.replace(r'x_j', 'x<sub>j</sub>')
text = text.replace(r'\mathbf{X}_{t} \in \mathbb{R}^{d}', 'X<sub>t</sub> &isin; &#8477;<sup>d</sup>')
text = text.replace(r'X_t in R^d', 'X<sub>t</sub> &isin; &#8477;<sup>d</sup>')
text = text.replace(r'y_t = \text{Close}_{t+1}', 'y<sub>t</sub> = Close<sub>t+1</sub>')
text = text.replace(r'y_{t+1}', 'y<sub>t+1</sub>')
text = text.replace(r'y_{t+k}', 'y<sub>t+k</sub>')
text = text.replace(r'y_t', 'y<sub>t</sub>')
text = text.replace(r'y_i', 'y<sub>i</sub>')
text = text.replace(r'R^2', 'R&sup2;')
text = text.replace(r'R²', 'R&sup2;')
text = text.replace(r'L_2', 'L<sub>2</sub>')

# Custom alerts replacement
def alert_sub(m):
    full = m.group(0)
    lines = full.split('\n')
    header = lines[0]
    kind_match = re.search(r'\[!(.*?)\]', header)
    kind = kind_match.group(1).upper() if kind_match else 'NOTE'
    body_lines = [l.lstrip('>').strip() for l in lines[1:] if l.strip()]
    body = ' '.join(body_lines)
    return f'<div class="alert alert-{kind.lower()}"><div class="alert-title">{kind}</div><div class="alert-body">{body}</div></div>'

text = re.sub(r'>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](?:\n>[^\n]*)+', alert_sub, text)

# Convert Markdown to HTML
html_body = markdown.markdown(text, extensions=['tables', 'fenced_code', 'toc', 'sane_lists'])

full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Atul Quant Studio — Technical & Presentation Report</title>
<style>
  @page {{
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
    @bottom-right {{
      content: counter(page);
      font-size: 8.5pt;
      color: #64748b;
    }}
    @bottom-left {{
      content: "Atul Quant Studio · Summer Analytics 2026 · IIT Guwahati";
      font-size: 8pt;
      color: #64748b;
    }}
  }}
  *, *::before, *::after {{
    box-sizing: border-box;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 9.5pt;
    background: #ffffff;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .cover {{
    background: linear-gradient(135deg, #0b1329 0%, #111e38 50%, #1e293b 100%);
    color: #f8fafc;
    padding: 28px 26px 24px 26px;
    border-radius: 10px;
    margin-bottom: 20px;
    border-left: 6px solid #22c55e;
    page-break-after: avoid;
  }}
  .cover-badge {{
    display: inline-block;
    background: rgba(34, 197, 94, 0.18);
    color: #4ade80;
    font-weight: 700;
    font-size: 8pt;
    letter-spacing: 0.08em;
    padding: 3px 9px;
    border-radius: 9999px;
    text-transform: uppercase;
    margin-bottom: 10px;
    border: 1px solid rgba(34, 197, 94, 0.35);
  }}
  .cover h1 {{
    font-size: 19pt;
    margin: 0 0 6px 0;
    color: #ffffff;
    font-weight: 800;
    letter-spacing: -0.02em;
    border: none;
    padding: 0;
  }}
  .cover-sub {{
    font-size: 10.5pt;
    color: #94a3b8;
    margin-bottom: 14px;
    font-weight: 500;
  }}
  .cover-meta {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.14);
    font-size: 8.5pt;
  }}
  .cover-meta strong {{
    display: block;
    color: #94a3b8;
    font-size: 7.2pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 2px;
  }}
  .cover-meta span {{
    color: #ffffff;
    font-weight: 600;
  }}
  h1, h2, h3, h4 {{
    color: #0f172a;
    font-weight: 700;
    letter-spacing: -0.015em;
  }}
  h1 {{
    font-size: 15pt;
    margin-top: 22px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 2px solid #e2e8f0;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h2 {{
    font-size: 12pt;
    margin-top: 18px;
    margin-bottom: 6px;
    padding-bottom: 3px;
    border-bottom: 1px solid #cbd5e1;
    color: #1e3a8a;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h3 {{
    font-size: 10.5pt;
    margin-top: 12px;
    margin-bottom: 5px;
    color: #334155;
    page-break-after: avoid;
    break-after: avoid;
  }}
  p {{
    margin: 0 0 8px 0;
    text-align: justify;
  }}
  ul, ol {{
    margin: 0 0 10px 0;
    padding-left: 18px;
  }}
  li {{
    margin-bottom: 3px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
    break-inside: avoid;
    background: #ffffff;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 5px 8px;
    text-align: left;
  }}
  th {{
    background: #f1f5f9;
    font-weight: 700;
    color: #0f172a;
  }}
  tr:nth-child(even) td {{
    background: #f8fafc;
  }}
  pre, code {{
    font-family: 'Consolas', 'Courier New', monospace;
  }}
  code {{
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 4px;
    font-size: 8pt;
    border: 1px solid #e2e8f0;
  }}
  pre {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 9px 12px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 7.5pt;
    line-height: 1.4;
    page-break-inside: avoid;
    break-inside: avoid;
    margin: 8px 0 12px 0;
    border: 1px solid #334155;
  }}
  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    border: none;
    font-size: inherit;
  }}
  .alert {{
    border-left: 4px solid #3b82f6;
    background: #eff6ff;
    padding: 8px 12px;
    border-radius: 0 6px 6px 0;
    margin: 10px 0 14px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .alert-title {{
    font-weight: 700;
    font-size: 8pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #1d4ed8;
    margin-bottom: 2px;
  }}
  .alert-body {{
    font-size: 8.5pt;
    color: #1e3a8a;
  }}
  blockquote {{
    border-left: 3px solid #94a3b8;
    margin: 8px 0 10px 0;
    padding: 4px 10px;
    color: #475569;
    background: #f8fafc;
    font-style: italic;
    page-break-inside: avoid;
  }}
  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 16px 0;
  }}
  .footer-note {{
    margin-top: 24px;
    padding-top: 10px;
    border-top: 1px solid #cbd5e1;
    font-size: 7.5pt;
    color: #64748b;
    text-align: center;
  }}
</style>
</head>
<body>

<div class="cover">
  <div class="cover-badge">Summer Analytics 2026 · Capstone Project Report</div>
  <h1>ATUL QUANT STUDIO</h1>
  <div class="cover-sub">An End-to-End Machine Learning System for Quantitative Finance &amp; NSE Market Analysis</div>
  <div class="cover-meta">
    <div>
      <strong>Author &amp; Presenter</strong>
      <span>Atul Prakash</span>
    </div>
    <div>
      <strong>Organized By</strong>
      <span>C&amp;A Club, IIT Guwahati</span>
    </div>
    <div>
      <strong>Framework &amp; ML Stack</strong>
      <span>Django 5 · Scikit-Learn · XGBoost · Plotly</span>
    </div>
    <div>
      <strong>Source Repository</strong>
      <span>github.com/atulyd77/atul-quant-studio</span>
    </div>
  </div>
</div>

{html_body}

<div class="footer-note">
  Atul Quant Studio &copy; 2026 Atul Prakash. All rights reserved. &bull; Summer Analytics 2026, Consulting &amp; Analytics Club, IIT Guwahati.
</div>

</body>
</html>'''

html_path = os.path.abspath('PROJECT_REPORT.html')
pdf_path = os.path.abspath('PROJECT_REPORT.pdf')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(full_html)
print(f'Wrote HTML to {html_path}')

# Find Chrome or Edge to render to PDF
browsers = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

browser_exe = None
for b in browsers:
    if os.path.exists(b):
        browser_exe = b
        break

if not browser_exe:
    raise RuntimeError("No headless browser found to generate PDF.")

print(f"Using browser: {browser_exe}")

cmd = [
    browser_exe,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path}"
]

print("Running command:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)

if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
    print(f"SUCCESS: Generated PDF at {pdf_path} (size: {os.path.getsize(pdf_path)} bytes)")
else:
    print("FAILED to generate PDF:", res.stdout, res.stderr)
