# `::S` — Summarize plan or implementation

> **Use this prompt:** copy the body below and paste it into any AI chat.
> Synced from a personal espanso text-expansion config on 2026-05-09.

---

Summarize the current work in simple language with ASCII diagrams.

CONTEXT CHECK: Detect from the conversation whether this is a PLAN (design/approach, not yet built) or an IMPLEMENTATION (code written, changes made). State clearly at the top which you're summarizing. If both exist, summarize what was built and note where it diverged from the plan.

1. STEPS: Walk through it as numbered steps in plain English. No jargon, no code, no syntax. Each step is a sentence or two—what will happen (plan) or what was done (implementation), in human terms.

2. ASCII DIAGRAMS: Draw whatever diagrams help a reader understand. One concept per diagram—if you have orthogonal axes (flow vs structure vs time), draw separate diagrams rather than cramming them together. Use only ASCII characters (+, -, |, ->, v). No Unicode box-drawing, no code blocks inside diagrams.

RULES:
- Simple language beats precise jargon
- Multiple focused diagrams beat one dense diagram
- Skip diagrams that don't add understanding—don't force-fit
