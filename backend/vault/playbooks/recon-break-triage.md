---
title: Reconciliation Break Triage Workflow
doc_type: playbooks
domain: reconciliation
updated: 2025-04
version: 4.0
---

# Reconciliation Break Triage Workflow

## Purpose

This playbook governs the daily identification, classification, prioritization, and resolution of reconciliation breaks across all asset classes. A "break" is any discrepancy between the firm's internal books and records and an external source: prime broker statements, custodian reports, counterparty confirms, or exchange records.

Unresolved breaks are a regulatory and financial risk. SEC Rule 17a-3 and 17a-5 require broker-dealers to maintain accurate books and records. CFTC Regulation 1.32 imposes similar requirements for futures customer funds.

---

## Break Classification

Every break must be classified before triage. Classification determines urgency and resolution path.

| Class | Description | Examples | Max Age |
|---|---|---|---|
| **P0 — Cash** | Cash or collateral discrepancy affecting margin or settlement | Wire amount mismatch, missing VM payment, custodian cash break | Same day |
| **P1 — Position** | Position quantity or price discrepancy vs. prime or custodian | Share count mismatch, wrong lot, incorrect price | T+1 |
| **P2 — Trade** | Trade-level mismatch between OMS and prime broker blotter | Missing trade, duplicate booking, wrong account | T+2 |
| **P3 — Accrual** | Income, dividend, or fee accrual discrepancy | Dividend not posted, management fee timing | T+5 |
| **P4 — Corporate Action** | Mismatch stemming from a CA event | Stock split not applied, merger consideration wrong | T+3 from CA effective date |

---

## Daily Recon Cycle

### Morning Run (7:30–9:30 AM ET)

1. **Download statements:** Pull prior-day statements from all prime broker portals (Goldman, Morgan Stanley, JPMorgan, etc.) and custodians. File in the dated folder: `recon/YYYY-MM-DD/`.
2. **Load to recon system:** Import into the reconciliation platform (Tradar, Advent Geneva, or internal script). If using the Python recon script: `python scripts/run_recon.py --date YYYY-MM-DD --tenant {tenant_id}`.
3. **Generate break report:** System produces a break report sorted by classification (P0 → P4). Export to the shared breaks log.
4. **Morning standup (9:00 AM):** Ops team reviews P0 and P1 breaks together. Assign owners to each open item.

### Break Ownership Rules

- **P0:** Senior Operations Manager owns until resolved. CFO notified for any P0 > $100K.
- **P1:** Assigned operations associate owns. Senior manager reviews at noon if unresolved.
- **P2–P4:** Assigned by asset class to the relevant ops associate.

---

## Break Investigation Protocol

For each open break, the investigator must answer three questions in order:

### 1. Is the break a timing difference or a true break?

**Timing differences** resolve automatically and should not consume investigation time:
- Trades booked today but settling tomorrow (T+1 or T+2 lag)
- Dividends with ex-date / pay-date timing differences
- Wire transfers in transit (initiated but not yet settled)

Flag these as "timing — monitor" and move on. If they persist past the expected settlement date, reclassify as a true break.

**True breaks** require active investigation. Proceed to step 2.

### 2. What is the source of the discrepancy?

Work through the hierarchy of causes from most common to least:

**Booking error (most common):**
- Pull the original trade ticket or execution report from the OMS.
- Compare: quantity, price, account, trade date, settlement date, currency.
- Check for duplicates: search the OMS for the same CUSIP/ISIN on the same trade date.
- Check for misallocation: was this supposed to be split across multiple funds?

**Data feed issue:**
- Check whether the prime broker's file loaded cleanly (no parsing errors in the ingest log).
- Verify the statement date matches what you expect (primes sometimes send T-1 files late).
- Pull a fresh statement from the prime broker portal and recompare manually.

**Corporate action not applied:**
- Check the CA calendar for any events on the security: splits, mergers, spin-offs, rights offerings.
- Confirm the CA effective date against the position discrepancy date — they should match.
- If CA was applied to prime but not internal books: run the CA adjustment script or post a manual journal.

**Settlement fail carrying forward:**
- A prior-day fail will create a position break the next morning. Check the fails log.
- Resolve the underlying fail first (see Equity Settlement SOP), then the position break should clear.

**Prime broker error:**
- Less common but real. If internal records are confirmed correct (OMS matches execution reports), escalate to the prime broker operations contact with documentation.
- Request a corrected statement if the prime confirms the error.

### 3. What is the financial impact?

Before escalating any break, quantify the P&L impact:
- **Mark-to-market:** `(quantity discrepancy) × (current price)`
- **Cash:** state the exact dollar amount
- **Report format:** "P1 break — AAPL, 500 share short vs. GS Prime. MTM impact: $94,500 at $189.00. Under investigation."

---

## Escalation Thresholds

| MTM or Cash Impact | Action Required |
|---|---|
| < $10K | Ops associate resolves, log update only |
| $10K–$100K | Notify Senior Ops Manager; daily update required |
| $100K–$500K | CFO notified; resolution plan due within 4 hours |
| > $500K | CFO + Managing Partner + Compliance; immediate call |
| Any aged > T+5 regardless of size | CFO notification required |

---

## Aged Break Management

Any break open longer than its maximum age (see classification table above) is an **aged break** and requires:

1. A written root cause summary in the breaks log (not just "investigating").
2. A resolution target date with rationale.
3. Escalation to CFO if MTM > $50K.
4. Weekly review by the Senior Ops Manager until resolved.

Aged breaks are the primary focus of month-end recon review. The breaks log must be clean (no aged items or all aged items documented and escalated) before the month-end NAV sign-off.

---

## Month-End Close Procedures

1. **T-1 before month-end:** Run a full recon against all prime broker month-end preliminary statements. Identify and resolve all P0/P1 breaks.
2. **Month-end day:** Obtain final statements from all primes and custodians. Run final recon. All breaks must be classified and documented.
3. **Sign-off checklist before NAV release:**
   - [ ] Zero P0 (cash) breaks
   - [ ] All P1 breaks resolved or documented with CFO sign-off
   - [ ] All aged breaks have written root cause and resolution plan
   - [ ] Corporate action calendar reconciled for the month
   - [ ] Breaks log exported and filed in the month-end folder
4. **NAV package:** Include a recon summary page: total breaks opened, closed, and outstanding by class.

---

## Common Breaks and Fast Resolutions

**"Prime shows 0 shares, we show 10,000"**
Check for a settlement fail from prior day. If a purchase failed to settle, the prime won't show the position yet. Confirm with the fails log — if there's a fail, resolve the settlement issue and the position break will clear.

**"Price break — same quantity, different value"**
Usually a corporate action (stock split, rights offering) or a pricing source mismatch. Pull Bloomberg end-of-day price for trade date and compare against both internal and prime pricing.

**"Duplicate position on prime statement"**
Occasionally primes show both a long and a short in the same security due to a transfer between accounts. Confirm net position is correct; request consolidated view from prime.

**"Cash break matches an unsettled trade exactly"**
Almost certainly a timing difference from a T+2 settlement. Set a monitor and confirm it clears in two business days.

---

## Related Documents

- Equity Trade Settlement and DK Resolution SOP
- Futures Margin Call Escalation Playbook
- Prime Broker Onboarding and SSI Setup
- SEC Rule 17a-3 and 17a-5 Summary (see Regulatory folder)
