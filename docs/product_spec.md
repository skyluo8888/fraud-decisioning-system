# Fraud Decisioning System — Product Specification

## Overview
One paragraph: what this system does and for whom.

## Input
Transaction request fields:

| Field | Type | Description |
|-------|------|-------------|
| customer_id | string | ... |
| amount | float | Transaction amount in USD |

## Output
| Field | Type | Description |
|-------|------|-------------|
| fraud_score | float | Probability of fraud, 0-1 |
| decision | enum | APPROVE / REVIEW / DECLINE |

## Decision Policy
How score maps to decision (thresholds to be tuned in Phase 1).

## Non-Functional Requirements
- Callable through an API
- Reproducible across environments
- Resilient to bad inputs
- ...(其余照大纲填)

## Out of Scope (v1)
What we deliberately do NOT build yet.