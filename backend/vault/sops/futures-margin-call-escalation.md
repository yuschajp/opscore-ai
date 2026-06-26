---
title: Futures Margin Call Escalation Playbook
doc_type: sops
domain: margin
updated: 2025-01
version: 2.1
---

# Futures Margin Call Escalation Playbook

## Purpose

This playbook covers the identification, triage, approval, and payment of variation margin (VM) and initial margin (IM) calls from FCMs and clearing brokers for exchange-traded futures and cleared swaps. Applies to all listed futures (CME, ICE, LME) and cleared OTC derivatives.

**Regulatory basis:** CFTC Regulations 1.22 and 1.23 govern futures customer funds segregation. FCMs are required to issue VM calls by 10:00 AM ET for the prior day's settlement. Late payment may result in position liquidation.

---

## Types of Margin Calls

| Type | Description | Typical Timing | Payment Deadline |
|---|---|---|---|
| Variation Margin (VM) | Daily mark-to-market gain/loss vs. prior settlement | Issued by 10:00 AM ET | 2:00 PM ET same day |
| Initial Margin (IM) | Collateral to open new or increase positions | Issued intraday on trade date | By FCM close (varies) |
| Intraday IM | Excess volatility buffer requested mid-session | Issued anytime | Within 1 hour of notice |
| Maintenance Margin Call | Account equity fell below maintenance threshold | Issued by 10:00 AM ET | 2:00 PM ET same day |

---

## Daily Margin Workflow

### Morning Routine (9:00–10:30 AM ET)

1. **Retrieve settlement prices:** Download prior day CME/ICE settlement prices from FCM portal or direct feed. Verify against internal pricing system.
2. **Calculate expected VM:** Run the daily P&L script (`scripts/margin_calc.py`) or pull from risk system. Compare expected VM against FCM-issued call amount.
   - Tolerance: ≤$5,000 or 0.1% of call amount (whichever is greater). Discrepancies outside tolerance require immediate investigation.
3. **Confirm FCM call receipt:** By 10:00 AM ET, the FCM should have issued VM calls via portal, email, or SWIFT MT564. Log each call in the margin call tracker with: FCM name, amount, currency, deadline.
4. **Treasury notification:** Forward confirmed calls to Treasury by 10:30 AM ET with wire instructions.

### Approval and Payment (10:30 AM–2:00 PM ET)

**Approval thresholds:**

| Call Amount | Required Approval |
|---|---|
| Up to $500K | Operations Manager |
| $500K–$2M | CFO or designated deputy |
| Above $2M | CFO + Managing Partner |
| Any intraday IM call | CFO notification required regardless of amount |

**Payment process:**
1. Submit wire approval in banking system (Signature, JPMorgan, or Citi portal) per treasury instructions.
2. Record payment confirmation number in margin tracker.
3. Send payment confirmation to FCM via email and portal upload (attach SWIFT MT103 or wire receipt).
4. Confirm receipt acknowledgment from FCM by 3:30 PM ET.

---

## Escalation Path for Failed or Disputed Calls

### Scenario 1: Call Amount Discrepancy

If the FCM-issued call differs from your internal calculation by more than the tolerance:

1. Call the FCM margin desk immediately. Do not delay payment pending resolution — pay the FCM amount to avoid position risk, then dispute.
2. Request FCM's settlement price file and margin parameters for the disputed contracts.
3. Reconcile line by line. Common causes:
   - End-of-day price disputes (especially on thinly traded LME broken dates)
   - New position not yet reflected in internal system
   - FCM applying incorrect multiplier for non-standard contract sizes
4. Document the reconciliation and, if FCM calculation is wrong, request a credit on the next business day.

### Scenario 2: Wire Transfer Delayed

If the outgoing wire is delayed (banking system outage, approval bottleneck):

1. Notify FCM margin desk immediately by phone. Do not wait for email.
2. Escalate to CFO for emergency wire authorization.
3. If delay will cause the 2:00 PM deadline to be missed, FCM may issue a formal cure notice. Obtain the cure period extension in writing.
4. Log all communications with timestamps in the margin tracker.

### Scenario 3: FCM Issues Intraday Margin Call

Intraday calls are uncommon but occur during high-volatility sessions (e.g., macro events, limit-move days):

1. **Immediately** notify the CFO and portfolio manager. Do not wait for scheduled check-in.
2. Assess whether the call is driven by a position increase or market move:
   - If position increase: confirm PM is aware and intended.
   - If market move: confirm current exposure is within risk limits before paying.
3. Payment must be made within 1 hour of receipt per standard FCM agreements.
4. If the firm cannot meet the intraday call within the hour, the FCM has the right to liquidate positions at market. Escalate to the Managing Partner immediately if this risk exists.

### Scenario 4: Missed Margin Call (Position Liquidation Risk)

If a margin call is missed and FCM threatens liquidation:

1. **Immediate escalation:** Operations → CFO → Managing Partner within 5 minutes.
2. Call the FCM relationship manager (not just the margin desk) and request a short extension.
3. Prepare a statement of ability to pay (verbal authorization from CFO is sufficient for FCM to grant extension; follow up in writing).
4. Document the full incident timeline for compliance reporting.

---

## LME Broken Date Margin — Special Procedures

London Metal Exchange (LME) futures trade on daily prompt dates (broken dates), not standardized monthly contracts. This creates non-standard margin calculations:

1. **Broken date identification:** Pull open position report from FCM and identify any trades with settlement dates outside standard forward dates.
2. **Tenor matching:** LME broken dates require tenor-matched margin calculation. Confirm the FCM is using the correct carry-adjusted rate for each broken date.
3. **LME fee structure:** LME charges a premium margin rate for broken dates vs. standard prompts. Ensure this is reflected in your IM calculation.
4. **Dispute resolution:** LME broken date disputes must be escalated to LME Clearing directly (in addition to FCM) for margin methodology questions.

---

## Margin Tracker Template Fields

Each call logged in the tracker must include:

- Date, FCM name, asset class (futures / cleared swap)
- Contract and exchange (CME / ICE / LME / Eurex)
- Call type (VM / IM / intraday)
- FCM call amount and currency
- Internal calculated amount
- Variance and variance %
- Approval obtained from (name and time)
- Wire reference number
- FCM receipt confirmation (Y/N, timestamp)
- Notes (disputes, delays, extensions)

---

## Related Documents

- Recon Break Triage Workflow
- CME Clearing Member Agreement (see Legal folder)
- CFTC Regulations 1.22 and 1.23 Summary (see Regulatory folder)
- Equity Trade Settlement and DK Resolution SOP
