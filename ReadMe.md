# Nuclei to PDF Report Generator

A professional-grade automation tool designed to bridge the gap between technical vulnerability scanning and executive reporting. Developed by **Adi Mahluf (Tenroot Cyber Security)**.

---

## 🚀 Overview

This project provides a seamless "one-command" workflow to audit web assets. It leverages the high-performance **Nuclei** engine to identify vulnerabilities and misconfigurations, then automatically compiles the raw results into a formatted, client-ready PDF report. It is specifically tailored for Security Architects and Incident Response teams who need to deliver clear, actionable data to stakeholders.

---

## 🛠️ Prerequisites

To ensure the tool runs correctly across different environments, the following components must be installed on your workstation.

### 1. Nuclei Engine (v3.x+)

The core scanning engine. Ensure you are using version 3.0 or higher to support modern templates and flags.

```bash
go install -v [github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest](https://github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest)
```

### 2. Python 3 & Virtual Environment
The reporting script requires Python 3.10+ and the fpdf2 library for modern PDF features and Unicode support.
Setup Instructions:
```Bash
# Install venv tools if missing (Ubuntu/WSL)
sudo apt update && sudo apt install python3-venv python3-full -y
# Create and configure the environment
python3 -m venv venv
./venv/bin/pip install fpdf2
```

### 3. Utility Tools
Required to handle script permissions and cross-platform encoding.
```Bash
sudo apt install dos2unix -y
```
## 📥 Installation

### 1. Clone the Repository:
```Bash
git clone https://github.com/YourUsername/Nuclei-PDF-Generator.git
cd Nuclei-PDF-Generator
```
### 2. Fix Encoding & Permissions: Ensure the scripts have execution rights and use Unix line endings.

```bash
chmod +x scan.sh
dos2unix scan.sh generate_report.py
```
### 3. Add Your Branding: Place your company logo in the root project folder and name it exactly logo.png.

##📑 Usage
Run the audit script by providing the target domain. The script defaults to Stealth Mode (rate-limited) to avoid being blocked by Web Application Firewalls (WAF).
```Bash
./scan.sh <domain_name> [--aggressive]
```
- Example (Stealth): ./scan.sh tenroot.io
- Example (Aggressive): ./scan.sh internal-site.local --aggressive

The tool will generate a file named: Report_domain.com_YYYYMMDD-HHMM.pdf.

## 📋 Report Features

- Executive Risk Summary: A high-level count of findings categorized from Critical to Informational.
- Detailed Findings: Technical descriptions of every identified vulnerability or technology, including the affected URL.
- Remediation Advice: Actionable, step-by-step mitigation steps pulled directly from the Nuclei templates.

## 📷 Images
<img width="1959" height="1606" alt="image" src="https://github.com/user-attachments/assets/1f5698b0-8b8d-4b80-a5c8-f47a439f75cb" />
<img width="1307" height="272" alt="image" src="https://github.com/user-attachments/assets/afa7280d-9951-4585-928a-e6bbed62b898" />
<img width="1150" height="401" alt="image" src="https://github.com/user-attachments/assets/b19a6767-9a05-4d14-b8d9-d06b800bc0a0" />


## ⚠️ Troubleshooting

|Error|Root Cause|Resolution|
|---|---|---|
|FPDFException|Cursor reached right margin.|Use version 1.4+ of the Python script.|
|UnicodeEncodeError|Special characters in results.|Use the clean_text() function in the script|
|ModuleNotFoundError|Missing Python libraries|Ensure the venv is active or use ./venv/bin/python3.|
|Permission denied|Script is not marked executable|Run chmod +x scan.sh in your terminal.|
|WAF Blocking|IP blacklisted by request rate|Use default scan mode without the --aggressive flag.|

---
**Disclaimer**: This tool is intended for authorized security testing only. The developer assumes no liability for misuse or damage caused by this application
