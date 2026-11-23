import os
import subprocess

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_file = os.path.abspath("Infografia_Arquitectura_Empresarial.html")
png_file = os.path.abspath("Infografia_Arquitectura_Empresarial.png")
pdf_file = os.path.abspath("Infografia_Arquitectura_Empresarial.pdf")

url_path = "file:///" + html_file.replace("\\", "/")

# 1. High-Resolution PNG (Retina-like scale with 1440px width)
cmd_png = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1440,1720",
    f"--screenshot={png_file}",
    url_path
]

print("Rendering high-resolution PNG...")
subprocess.run(cmd_png, check=True)
if os.path.exists(png_file):
    print(f"PNG rendered: {png_file} ({os.path.getsize(png_file):,} bytes)")

# 2. Vector PDF export
cmd_pdf = [
    edge_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_file}",
    "--no-pdf-header-footer",
    url_path
]

print("Rendering vector PDF...")
subprocess.run(cmd_pdf, check=True)
if os.path.exists(pdf_file):
    print(f"PDF rendered: {pdf_file} ({os.path.getsize(pdf_file):,} bytes)")

# Also copy both files to 06_ARQUITECTURA_EMPRESARIAL_TO-BE\Infografia_Tecnologias_Emergentes
dest_folder = os.path.join(r"06_ARQUITECTURA_EMPRESARIAL_TO-BE", "Infografia_Tecnologias_Emergentes")
os.makedirs(dest_folder, exist_ok=True)

import shutil
shutil.copy(png_file, os.path.join(dest_folder, "Infografia_Arquitectura_Empresarial.png"))
shutil.copy(pdf_file, os.path.join(dest_folder, "Infografia_Arquitectura_Empresarial.pdf"))
print(f"Copies also saved to {dest_folder}")
