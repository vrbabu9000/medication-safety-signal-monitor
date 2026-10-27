"""Pull samples for every pilot ingredient (8 opioids + 5 GLP-1 RAs, decision D014).

Usage: python3 -I prototypes/explore/pull_all.py
Calls pull_samples.py once per drug. Output: prototypes/data/<drug>/ (git-ignored).
"""
import subprocess
import sys
from pathlib import Path

OPIOIDS = ["fentanyl", "morphine", "hydromorphone", "oxycodone", "hydrocodone", "methadone", "buprenorphine", "tramadol"]
GLP1 = ["semaglutide", "tirzepatide", "liraglutide", "dulaglutide", "exenatide"]
PULL = Path(__file__).with_name("pull_samples.py")  # keep the lists in sync with volume_check.py

failed = []
for drug in OPIOIDS + GLP1:
    print(f"\n===== {drug} =====", flush=True)
    r = subprocess.run([sys.executable, "-I", str(PULL), drug], capture_output=True, text=True)
    print(r.stdout, end="")
    if r.returncode or "FAIL" in r.stdout:
        failed.append(drug)
print("\nFailures:", failed or "none")
