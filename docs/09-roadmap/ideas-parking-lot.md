# Ideas parking lot

Good ideas that are **not in pilot scope**. Kept so they aren't lost, and so we can talk about them in the demo ("what I'd do next").

| # | Date | Idea | Source | Status |
|---|---|---|---|---|
| I1 | 2026-10-13 | Health-specific "OS" (Epic-like): multi-vendor, fast, lightweight, very efficient. Proposed: a fine-tuned Linux distro | Boss meeting | Parked |

## I1 — Health "OS": first notes
**What was said:** the boss described an Epic-like, health-specific operating environment that supports many vendors and is fast, lightweight and very efficient. You proposed a fine-tuned Linux distro.

**🏗️ Architect view (to think about, not to act on):**
- Two layers are hiding in the word "OS":
  1. **Runtime layer** (the machine): a slim, hardened Linux distro tuned for speed and security. Your proposal fits here.
  2. **Platform layer** (how vendors plug in): shared data model and APIs. In healthcare that means standards like **FHIR** (the modern health-data exchange format), **SMART on FHIR** (plug-in apps) and **CDS Hooks** (alerts inside clinician workflows).
- "Multi-vendor" is mostly a platform-layer problem. A tuned distro makes it fast. Shared standards make vendors work together.
- **Link to this project:** our signal monitor could be one "app" on such a platform. Example: a CDS Hook that warns a prescriber about an active opioid recall.

**Open questions for a future conversation:** Who are the users: hospitals, vendors, or devices? Is the goal edge devices (lightweight) or the data-center core? What does "crazy efficient" mean here: latency, cost, or ease of integration?
