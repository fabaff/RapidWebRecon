#!/bin/bash

# Check if domain is provided
if [ -z "$1" ]; then
    echo "Usage: ./scan.sh <domain> [--aggressive]"
    echo "Default mode is STEALTH (Rate-limited to 10 req/s)"
    exit 1
fi

DOMAIN=$1
MODE=$2
TIMESTAMP=$(date +"%Y%m%d-%H%M")
JSON_TMP="tmp_${TIMESTAMP}.json"
PDF_NAME="Report_${DOMAIN}_${TIMESTAMP}.pdf"

# Check for Virtual Environment
if [ ! -d "venv" ]; then
    echo "[-] Error: Virtual environment 'venv' not found."
    exit 1
fi

# Determine Scan Intensity
if [ "$MODE" == "--aggressive" ]; then
    echo "[!] CAUTION: Starting AGGRESSIVE Scan for: $DOMAIN"
    # No rate limit, higher concurrency
    NUCLEI_FLAGS="-as -c 50"
else
    echo "[*] Starting STEALTH Scan for: $DOMAIN (WAF-friendly)"
    # Rate limit 10/sec, low concurrency
    NUCLEI_FLAGS="-as -rl 10 -c 5"
fi

# RUN NUCLEI
nuclei -u "$DOMAIN" \
    $NUCLEI_FLAGS \
    -tags wordpress,ssl,headers,cve,vulnerability,misconfig,tech \
    -severity critical,high,medium,low,info \
    -o "$JSON_TMP" \
    -jsonl \
    -vv

echo "[*] Scan complete. Generating Professional PDF..."

# RUN PYTHON GENERATOR
./venv/bin/python3 generate_report.py "$DOMAIN" "$JSON_TMP" "$PDF_NAME"

# Check Success
if [ -f "$PDF_NAME" ]; then
    echo "[+] Success! Report generated: $PDF_NAME"
else
    echo "[-] Error: PDF generation failed."
fi

# CLEANUP
rm "$JSON_TMP"