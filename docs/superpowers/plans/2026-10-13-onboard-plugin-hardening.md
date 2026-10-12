# Onboard Plugin Hardening and Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Harden the plugin's validation and redaction boundaries, make the installer portable and safer, and rename the plugin identity and package directory to `onboard`.

**Architecture:** Keep the existing Python scripts and single-file HTML engine. Strengthen the existing checker at its input boundary, scan every value that can reach the rendered page, and make the installer update files safely without adding dependencies. Rename the package directory and manifests to `onboard`.

**Tech Stack:** Python 3.8+, standard library `unittest`, Claude Code plugin JSON manifests, inline HTML/JavaScript.

**Spec:** User request to fix the audit findings, rename the plugin to `onboard`, and publish the result.

## Global Constraints

- No new runtime dependencies.
- Preserve the existing story format and sample behavior where possible.
- Reject malformed or unsafe input with structured checker errors.
- Never claim tests or publishing succeeded without fresh command output.
- Push only to an explicitly configured GitHub remote; the current workspace has no remote yet.

## Review Focus

- External stories containing secrets in stats, heatmaps, custom HTML, or non-selected locales must fail validation.
- Redaction must cover `brief`, authorization bearer tokens, and paths containing spaces.
- Malformed story structures must produce errors instead of tracebacks.
- Calculator expressions and input IDs must be validated against the runtime grammar and HTML boundary.
- Installer commands must work in a Windows non-UTF-8 console and must not silently destroy or skip project guidance.
- Plugin identity, paths, manifests, and documentation must consistently use `onboard`.

## Tasks

- [ ] Add standard-library regression tests for the review focus and confirm the vulnerable behavior fails before edits.
- [ ] Harden `check.py`, `redact.py`, `reader_view.py`, and the HTML calculator boundary.
- [ ] Make installer output UTF-8 safe, update AGENTS.md paths idempotently, create parents, and avoid unsafe replacement behavior.
- [ ] Rename the plugin directory and manifests/documentation to `onboard`; migrate sample theme names.
- [ ] Run compile, focused tests, sample regressions, manifest validation, and packaging smoke checks.
- [ ] Initialize/inspect Git metadata, commit the verified result, and push only after a GitHub remote is available.
