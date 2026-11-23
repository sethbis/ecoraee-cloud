import os
import subprocess
import shutil

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
base_dir = r"c:\Users\nicol\OneDrive\Documentos\integrador 5to semestre"

html_file = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial.html")
with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

# Make Spanish default in this variant
content_es = content.replace("let currentLang = 'en';", "let currentLang = 'es';")
content_es = content_es.replace("<body", "<body onload=\"toggleLanguage()\" ")

html_es = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial_ES.html")
with open(html_es, "w", encoding="utf-8") as f:
    f.write(content_es)

png_es = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial_ES.png")
pdf_es = os.path.join(base_dir, "Infografia_Arquitectura_Empresarial_ES.pdf")

url_path = "file:///" + html_es.replace("\\", "/")

subprocess.run([
    edge_path,
    "--headless",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1440,1720",
    f"--screenshot={png_es}",
    url_path
], check=True)

subprocess.run([
    edge_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_es}",
    "--no-pdf-header-footer",
    url_path
], check=True)

dest_folder = os.path.join(base_dir, "06_ARQUITECTURA_EMPRESARIAL_TO-BE", "Infografia_Tecnologias_Emergentes")
shutil.copy(html_es, os.path.join(dest_folder, "Infografia_Arquitectura_Empresarial_ES.html"))
shutil.copy(png_es, os.path.join(dest_folder, "Infografia_Arquitectura_Empresarial_ES.png"))
shutil.copy(pdf_es, os.path.join(dest_folder, "Infografia_Arquitectura_Empresarial_ES.pdf"))

print(f"Generated Spanish versions: {png_es} and {pdf_es}")
