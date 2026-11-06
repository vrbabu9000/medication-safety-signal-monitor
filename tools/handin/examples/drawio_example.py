"""Worked example for tools/handin/drawio.py: raw sources -> pipeline -> ontology -> screen.

Run:  .venv/bin/python tools/handin/examples/drawio_example.py [output folder]
Default output is a temp folder, so the example never adds files to docs/diagrams.
For a real diagram, call d.save() with no folder: it writes docs/diagrams/{drawio,png,pdf}/<name>.*
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from drawio import Diagram  # noqa: E402

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.gettempdir()) / "handin-drawio-example"

d = Diagram("90-handin-drawio-example-v1", 1120, 400, title="Hand-in draw.io example")
d.group("g_src", 20, 20, 240, 360, "Public sources")
d.group("g_fdy", 290, 20, 540, 360, "Foundry: raw → clean → ontology")
d.box("faers", 40, 60, 200, 70, "FAERS", ["quarterly files"], kind="source")
d.box("dm", 40, 165, 200, 70, "DailyMed", ["label SPL XML"], kind="source")
d.box("enf", 40, 270, 200, 70, "openFDA enforcement", ["recalls, weekly"], kind="source")
d.box("clean", 310, 60, 200, 70, "faers_clean", ["one row per case version"], kind="pipeline")
d.box("llm", 310, 165, 200, 70, "Label extraction", ["LLM + grounding check"], kind="ai")
d.box("rec", 310, 270, 200, 70, "recalls_clean", ["status = Ongoing"], kind="pipeline")
d.box("sig", 610, 112, 200, 70, "Signal", ["ontology object"], kind="ontology")
d.box("recall", 610, 270, 200, 70, "Recall", ["ontology object"], kind="ontology")
d.box("app", 880, 165, 210, 80, "Workshop screen", ["three morning questions", "triage writes back"], kind="app")
d.arrow("faers", "clean")
d.arrow("dm", "llm")
d.arrow("enf", "rec")
d.arrow("clean", "sig", label="PRR")
d.arrow("llm", "sig")
d.arrow("rec", "recall")
d.arrow("sig", "app", via=[(845, 147), (845, 190)])
d.arrow("recall", "app", via=[(845, 305), (845, 220)])
d.save(out)
print("open", out)
