# Webscanning tool for vulnerabilities and misconfigurations
# Automatically create PDF report with all issues on the website
# By: Adi Mahluf - Tenroot Cyber Security
# Version 1.4 - Final fix for FPDFException and Deprecation Warnings
import json
import datetime
import os
import sys
from fpdf import FPDF, XPos, YPos

# Configuration
COMPANY_NAME = "Tenroot Cyber Security"
AUTHOR = "Adi Mahluf"
LOGO_PATH = "logo.png" 

def clean_text(text):
    """Sanitize text for Latin-1 PDF encoding."""
    if not text: return "N/A"
    text = text.replace('\u2013', '-').replace('\u2014', '-').replace('\u2019', "'").replace('\u201d', '"').replace('\u201c', '"')
    return text.encode('latin-1', 'replace').decode('latin-1')

class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, 10, 8, 30)
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(150)
        # Explicitly move to next line after header
        self.cell(0, 10, clean_text(f'{COMPANY_NAME} Audit - Confidential'), 
                  align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_pdf(domain, json_file, output_pdf):
    findings = []
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    
    # Parse Nuclei results
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    sev = data.get('info', {}).get('severity', 'info').lower()
                    counts[sev] = counts.get(sev, 0) + 1
                    findings.append(data)
                except: continue

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Define safe effective width to prevent horizontal space errors
    eff_width = pdf.w - 2 * pdf.l_margin 

    # --- Title Page ---
    pdf.ln(60)
    pdf.set_font('helvetica', 'B', 26)
    pdf.cell(0, 20, "Security Assessment Report", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', '', 14)
    pdf.cell(0, 10, clean_text(f"Target: {domain}"), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.add_page()

    # --- Summary Table ---
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, "Risk Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    pdf.set_font('helvetica', '', 11)
    for sev in ["critical", "high", "medium", "low", "info"]:
        pdf.cell(40, 8, f"{sev.upper()}:", border=1)
        pdf.cell(20, 8, f"{counts.get(sev, 0)}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    # --- Detailed Findings ---
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, "Detailed Findings", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    colors = {"CRITICAL": (150,0,0), "HIGH": (200,0,0), "MEDIUM": (255,140,0), "LOW": (0,100,0), "INFO": (0,0,200)}

    for data in findings:
        info = data.get('info', {})
        severity = info.get('severity', 'info').upper()
        
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_text_color(*colors.get(severity, (0,0,0)))
        pdf.cell(0, 8, clean_text(f"[{severity}] {info.get('name')}"), 
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_text_color(0)
        pdf.set_font('helvetica', '', 10)
        desc = clean_text(info.get('description'))
        url = clean_text(data.get('matched-at'))
        
        # Use explicit eff_width to ensure proper wrapping
        pdf.multi_cell(eff_width, 5, f"Description: {desc}\nURL: {url}")
        
        remedy = clean_text(info.get('remediation'))
        if remedy and remedy != "N/A":
            pdf.ln(2)
            pdf.set_font('helvetica', 'I', 10)
            pdf.multi_cell(eff_width, 5, f"Suggested Fix: {remedy}")
        
        pdf.ln(4)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

    pdf.output(output_pdf)

if __name__ == "__main__":
    generate_pdf(sys.argv[1], sys.argv[2], sys.argv[3])