# Capability 010 Demo - Hero Visual System

## Problem

Capability 009 produced an approved Hero Visual prompt but had no safe,
provider-independent way to create or validate the required 720 × 425 visual.

## What Changed

The Hero Visual System now validates the request, applies brand-neutral policy
constraints, invokes a provider behind a stable interface, validates the
artifact and provenance, and returns an explicit outcome. The Publication
Package may attach the result without regenerating approved text.

## Example

```text
Approved Capability 009 Hero Visual prompt
                    |
                    v
       request and policy validation
                    |
        +-----------+-----------+
        |                       |
      blocked             selected provider
                                |
                                v
                    untrusted visual artifact
                                |
                                v
                format + dimensions + provenance
                                |
                    +-----------+-----------+
                    |                       |
             validation failed       ready 720 x 425 PNG
                                            |
                                            v
                              attach to Publication Package
```

## Author Benefit

The Author receives a clear ready, failed, or blocked visual state without the
Studio altering the approved article, changing the prompt, fabricating success,
or requiring one external provider.

## Acceptance Evidence

Behavioral tests cover dimensions, prompt preservation, provider independence,
deterministic repeatability, malformed and unsupported requests, generation and
validation failure, policy blocking, package pending/ready/failed/blocked
states, approved-content preservation, and no silent regeneration.

## Learning

Generation and validation are separate trust decisions. Treating provider
output as untrusted makes external-provider evolution possible without
weakening the stable publication contract.

## Next

Capability 011 remains responsible for Portable Editorial Project resume and
export. End-to-end RC1 release readiness remains separate.
