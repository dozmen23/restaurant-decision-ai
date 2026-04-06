# Project Context — Restaurant Decision AI

## Project Goal

This project aims to build an explainable restaurant decision system using:

- Google Maps data
- Review-based property extraction
- Aggregated scoring
- Future MCDA ranking

The system is NOT just sentiment analysis.
It is a structured decision intelligence system.

---

## Current Stage

We are in:

> Baseline keyword-based extraction phase

No LLM is used yet.

---

## Current Architecture

Pipeline:

1. Load raw reviews
2. Apply review quality filtering
3. Extract property signals (keyword-based)
4. Aggregate into restaurant-level scores
5. Generate explainability (evidence, snippets)
6. Output structured JSON

---

## Active Properties (CURRENT IMPLEMENTATION)

These properties MUST be supported:

- serviceQuality
- staffFriendliness
- foodQuality
- valueForMoney
- portionSatisfaction
- cleanliness
- speed
- ambience
- groupSuitability
- dateSuitability
- repeatVisitIntent
- consistency
- viewQuality
- luxuryPerception
- reservationEase

All properties should exist in:
- config/properties.py
- extractor
- output

---

## Important Design Rules

- Do NOT remove existing properties
- Do NOT change JSON output structure
- Do NOT introduce LLM yet
- Keep everything keyword-based for now
- Maintain backward compatibility

---

## Explainability Requirement

Each property must include:

- score
- confidence
- supportCount
- evidence:
  - keywords
  - review snippets
  - review ids

---

## Review Filtering

Only usable reviews should be processed.

Rejected reviews must still be stored with reason.

---

## Consistency Metric (IMPORTANT)

Consistency is NOT a normal property.

It is a META METRIC.

It compares:

- Google rating
vs
- review-based scores

It will be implemented separately.

DO NOT treat it like a standard keyword-based property.

---

## Future Phases (NOT NOW)

- LLM-based extraction
- strength / weight modeling
- advanced scoring
- MCDA ranking system

---

## Coding Rules

- Prefer minimal changes
- Do not refactor entire files unnecessarily
- Keep functions small and clear
- Preserve existing logic unless explicitly instructed

---

## When in doubt

Do NOT assume new architecture.
Follow existing patterns.