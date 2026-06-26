---
title: Equity Trade Settlement and DK Resolution
doc_type: sops
domain: settlement
updated: 2025-06
version: 3.2
---

# Equity Trade Settlement and DK Resolution

## Purpose

This SOP governs the end-to-end settlement process for U.S. equity trades and the escalation path for Don't Know (DK) disputes. It applies to all long/short equity positions cleared through DTC and prime broker networks.

**Regulatory basis:** SEC Rule 15c6-1 requires standard settlement of most broker-dealer equity transactions by T+2. Failure to settle by T+2 may trigger buy-in procedures and DTCC reporting obligations.

---

## Scope

- U.S. equity trades (listed and OTC) settled via DTC
- Applicable to all accounts: long, short, margin, and cash
- Covers prime-to-prime fails, counterparty DKs, and internal mismatches

---

## T+0: Trade Date

1. **Trade capture:** Confirm all executions are booked in the OMS by 5:00 PM ET on trade date. Any unbooked trades must be escalated to the trading desk before EOD.
2. **Allocation confirmation:** If the trade requires allocation across multiple funds or sleeves, allocations must be submitted to the prime broker by 6:00 PM ET.
3. **SSI validation:** Confirm counterparty settlement instructions (SSIs) are on file for the executing broker. Missing SSIs must be resolved same-day.

---

## T+1: Affirmation and Early Warning

1. **Morning match review (9:00 AM ET):** Run the T+0 trade date reconciliation. All matched trades should show a DTC Deliver Order (DO) or Receive Order (RO).
2. **Unmatched trade identification:** Any trade not yet matched by 12:00 PM T+1 is flagged as a potential DK. The operations associate must:
   - Contact the counterparty operations desk via DTC messaging (DTC OASYS/CTM) or direct phone call.
   - Log the break in the breaks management system with: trade reference, counterparty, quantity, price, and CUSIP.
3. **DK notification:** If the counterparty formally DKs the trade, send a DTC DK Notice. Escalate to the senior operations manager and notify prime broker.
4. **Quantity or price discrepancy:** If the DK stems from a quantity or price mismatch, pull the original trade confirmation and compare against the counterparty's confirm. Common causes:
   - Fat finger on quantity (check OMS vs. execution report)
   - Partial fill misallocation
   - Corporate action price adjustment not reflected

---

## T+2: Settlement Date

1. **Pre-settlement check (8:00 AM ET):** Confirm sufficient shares are available in the DTC account for all scheduled deliveries.
2. **Fails management:** Any trade not settled by 3:00 PM ET on T+2 is a confirmed fail.
   - Open a fail case in the breaks log immediately.
   - Notify the prime broker fails desk.
   - For short positions: confirm borrow is still in place; do not release locate.
3. **T+2 noon escalation:** Any DK unresolved by 12:00 PM T+2 must be escalated to:
   - Senior Operations Manager
   - Prime Broker Relationship contact
   - Portfolio Manager (for awareness only — do not await PM approval to escalate)

---

## T+3 and Beyond: Buy-In Risk

1. **DTCC buy-in eligibility:** DTCC may initiate a mandatory buy-in on any fail aged T+3 or later per NSCC Rule 11.
2. **Buy-in notification:** DTCC issues a buy-in notice with a 24-hour cure period. Operations must:
   - Attempt to source shares in the market or via stock loan within the cure period.
   - Notify the portfolio manager and CFO immediately upon receipt of buy-in notice.
   - Document all cure attempts with timestamps.
3. **If buy-in executes:** Record the buy-in price and calculate P&L impact. Report to CFO and compliance same day.

---

## Escalation Matrix

| Situation | Escalation Level | Timeline |
|---|---|---|
| Unmatched trade | Operations Associate → Counterparty Ops | T+1 by 12:00 PM |
| Formal DK received | Senior Ops Manager + Prime Broker | T+1 same day |
| Unresolved DK at noon | Senior Ops Manager + Portfolio Manager | T+2 by 12:00 PM |
| Confirmed fail | CFO notification | T+2 by 3:30 PM |
| DTCC buy-in notice | CFO + Compliance + PM | Immediately |

---

## Common Root Causes and Quick Fixes

**Quantity mismatch (most common):**
Pull the OASYS confirm and compare against the OMS booking. Check for partial fills that may have been booked as a single lot. Correct in OMS and resend DTC affirmation.

**Price mismatch:**
Most often caused by accrued interest on bond-like instruments or corporate action adjustments. Verify against Bloomberg settlement price for the trade date.

**Wrong CUSIP:**
Check for recent ticker changes, mergers, or symbol reuses (common with SPACs). Cross-reference CUSIP with Bloomberg or DTCC's security master.

**SSI mismatch:**
Confirm DTC Participant number with counterparty. If counterparty clears through a different prime or custodian than expected, update SSI on file immediately.

---

## Related Documents

- Futures Margin Call Escalation Playbook
- Prime Broker Onboarding and SSI Setup
- SEC Rule 15c6-1 Summary (see Regulatory folder)
- Recon Break Triage Workflow
