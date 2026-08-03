# Capability 009 Demo - Article Engine and Publication Package

## Problem

The Studio could validate evidence and editorial risk but could not
construct an evidence-aligned article or assemble its textual package.

## What Changed

A provider-independent Article Engine now preserves approved Editorial
Intent, uses attributable evidence, blocks High and Severe risk, and
constructs a structured professional article. The Publication Package
builder validates every Capability 009 textual component.

## Example

```text
Approved Author inputs + Evidence Validation report
                      |
                      v
            High or Severe risk? -- yes --> stop
                      |
                     no
                      v
         provider-independent Article Engine
                      |
                      v
           validated textual package
                      |
            +---------+---------+
            |                   |
     Capability 010       Capability 011
     rendered visual      portable project
```

## Author Benefit

The Author receives a coherent article grounded in approved intent and
evidence without the Studio inventing sources, silently changing
approved insights, or pretending later deliverables exist.

## Acceptance Evidence

Tests cover input validity, intent preservation, source attribution,
provider independence, Low/Moderate readiness, High/Severe blocking,
complete textual components, and explicit Capability 010/011 deferral.

## Learning

Publication readiness and Version 1.0 package completeness are different
facts. Modeling deferred deliverables explicitly prevents partial product
state from being presented as finished.

## Next

Capability 010 may consume the approved Hero Visual prompt to create the
rendered 720 × 425 Hero Visual. Capability 011 remains separate.
