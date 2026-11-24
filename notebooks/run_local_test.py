#!/usr/bin/env python3
"""Execute the notebook from top to bottom in its quick mode and print what each cell wrote.

    MDC_QUICK=1 PYTHONPATH=<packages> python3 notebooks/run_local_test.py <work dir>

The executed copy is saved as <work dir>/executed.ipynb.
"""
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

here = Path(__file__).resolve().parent
work = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
work.mkdir(parents=True, exist_ok=True)
nb = nbformat.read(here / "md_lysozyme_openmm.ipynb", as_version=4)
client = NotebookClient(nb, timeout=3600, kernel_name="python3", resources={"metadata": {"path": str(work)}})
t0 = time.time()
ok = True
try:
    client.execute()
except CellExecutionError as err:
    ok = False
    print("EXECUTION STOPPED:", str(err)[-1500:])
nbformat.write(nb, work / "executed.ipynb")
print(f"\n=== finished in {time.time() - t0:.0f} s, {'no error' if ok else 'WITH AN ERROR'}\n")
n = 0
for cell in nb.cells:
    if cell.cell_type != "code":
        continue
    n += 1
    texts, kinds = [], []
    for out in cell.get("outputs", []):
        if out.output_type == "stream":
            texts.append(out.text)
        elif out.output_type == "error":
            texts.append("ERROR " + out.ename + ": " + out.evalue)
        else:
            kinds.append("+".join(sorted(out.get("data", {}).keys())))
    first = cell.source.strip().splitlines()[0][:70]
    print(f"--- code cell {n}: {first}")
    body = "".join(texts).strip()
    if body:
        print("\n".join("    " + line[:170] for line in body.splitlines()[:40]))
    if kinds:
        print("    [rich outputs: " + "; ".join(kinds) + "]")
