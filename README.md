# AI in Security Experiments Lab

Hands-on experiments exploring how AI agents can support real SOC workflows.

This repository focuses on **automation that behaves like a SOC team**, not chatbots:
parse → analyze → report → evaluate.

## What This Repo Covers

- Multi-agent SOC pipelines (Parser → Analyst → Reporter)
- Log analysis for common attack patterns (RDP, SSH, SMB, RPC, outbound traffic)
- Structured incident reporting with strict output contracts
- Evaluation harnesses using gold-standard answers
- Measuring correctness, not just confidence

## Key Experiments

### Agent-Based SOC Workflow
AI agents with defined roles collaborate to:
- Parse raw telemetry (syslog, Zeek, Suricata, Windows Events)
- Identify suspicious behavior
- Produce management-ready incident summaries

### Evaluation Harness
- Gold Q&A datasets for security questions
- Automated comparison between model output and expected answers
- Similarity scoring to track accuracy and drift

### Structured Output Contracts
- Enforced JSON schemas for incident tickets
- Validation failures surface model errors early
- Reduces hallucination and formatting issues

## Why This Exists

AI in security fails when it isn’t tested, validated, or constrained.

This lab explores **where AI helps**, **where it breaks**, and **how to keep humans in control**.

## Status

Active experimentation.  
Expect frequent changes, new agents, and improved evaluation methods.

---

Built for SOC analysts, DFIR practitioners, and security engineers experimenting with AI responsibly.
