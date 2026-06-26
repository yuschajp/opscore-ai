---
title: CME Give-Up Agreement and FCM Dispute Resolution
doc_type: sops
domain: clearing
updated: 2025-03
version: 2.3
---

# CME Give-Up Agreement and FCM Dispute Resolution

## Purpose

This SOP governs the give-up process for exchange-traded futures and options executed through an executing broker and cleared through a designated clearing FCM. It covers trade matching, give-up acceptance, rejection handling, and escalation paths for FCM disputes at CME Group, ICE, and LME.

**Background:** A "give-up" occurs when a buy-side firm executes a futures trade through one broker (the executing broker) but clears it through a different firm (the clearing FCM). The executing broker "gives up" the trade to the clearing FCM. The clearing FCM must accept the give-up for the trade to be booked into the clearing account.

---

## Parties in a Give-Up Transaction

| Party | Role |
|---|---|
| Buy-side firm (us) | Instructs executing broker; designated clearing FCM on file |
| Executing broker | Takes the order and executes on exchange; gives up trade to clearing FCM |
| Clearing FCM | Accepts give-up; books trade to customer account; handles margin |
| Exchange (CME/ICE/LME) | Matches and confirms the original execution |

The authority for give-ups is governed by the **CME Give-Up Agreement** (formerly the FIA Give-Up Agreement), which must be in place between the buy-side firm, executing broker, and clearing FCM before any give-up trades can be processed.

---

## Pre-Trade Setup: Give-Up Agreement Requirements

Before the first give-up trade with any executing broker:

1. **Confirm give-up agreement is signed:** Three-way agreement between fund, executing broker, and clearing FCM. File in Legal/Agreements.
2. **Confirm executing broker is on clearing FCM's approved list:** Clearing FCMs maintain a list of executing brokers they will accept give-ups from. Call the FCM give-up desk to confirm.
3. **Set up standing instructions:** The clearing FCM needs the fund's account number and the list of authorized executing brokers in their system before trading begins.
4. **Test trade:** For a new executing broker relationship, run one small test give-up and confirm it clears end-to-end before going live with real size.

---

## Daily Give-Up Workflow

### Trade Date (T+0)

**Step 1: Execution**
The portfolio manager or trader places an order with the executing broker. The executing broker must have the clearing FCM's account designation on record. The trader should confirm: "Please give up to [Clearing FCM], account [account number]" at the time of the order.

**Step 2: Give-up submission**
The executing broker submits the give-up to the exchange matching system (CME's EGUS — Electronic Give-Up System, or ICE's equivalent) by the exchange's give-up submission deadline, typically within 30 minutes of execution for CME.

**Step 3: FCM acceptance window**
The clearing FCM has until the exchange's acceptance deadline (CME: 6:00 PM CT on trade date for most products) to accept or reject the give-up in EGUS.

**Step 4: Operations monitoring**
The operations associate must monitor the give-up status in the FCM portal or EGUS access by 4:00 PM CT. Any give-up not showing "Accepted" by then requires immediate follow-up.

```
Give-up status codes:
  PENDING    — submitted by executing broker, awaiting FCM action
  ACCEPTED   — FCM accepted; trade booked to clearing account
  REJECTED   — FCM rejected; requires immediate resolution (see below)
  EXPIRED    — deadline passed without FCM action; treat as rejected
```

**Step 5: Trade confirmation**
Once accepted, confirm the trade appears on the FCM's trade register with correct: contract, expiry, quantity, price, buy/sell, and account number. Compare against the OMS booking.

---

## Give-Up Rejection Handling

A rejection is a time-sensitive event. An unresolved rejection means the executing broker holds a position they weren't meant to hold, and the fund has no cleared position.

### Immediate actions (within 15 minutes of identifying a rejection):

1. **Call the clearing FCM give-up desk** — do not rely on email. Get the rejection reason code:

| Rejection Code | Meaning | Resolution |
|---|---|---|
| R01 | Account not found | Confirm account number with FCM; resubmit |
| R02 | Executing broker not authorized | FCM doesn't have the executing broker on approved list; ops escalates to FCM relationship manager to add |
| R03 | Contract/expiry mismatch | Price or contract details differ; executing broker must resubmit with corrected details |
| R04 | Quantity over limit | Position would breach FCM-set concentration limit; FCM risk desk must approve override |
| R05 | Past deadline | Deadline missed; requires exchange and FCM manual processing (see below) |
| R99 | Other / manual review | FCM risk team reviewing; stay on the phone with FCM until resolved |

2. **Call the executing broker** — notify them of the rejection and the reason. For R01/R02/R03, the executing broker must resubmit a corrected give-up.

3. **Log the rejection** in the breaks management system with timestamps, rejection code, and who was contacted.

### If rejection cannot be resolved same day:

- The executing broker retains the position overnight in their own account.
- The fund has an uncleared economic exposure with no margin posted.
- Escalate to CFO and Senior Ops Manager immediately.
- Work with the executing broker and FCM to arrange a manual transfer the next morning.
- Compliance must be notified if the position remains uncleared at T+1 open.

---

## FCM Dispute Resolution

### Types of FCM disputes

**Trade price dispute:** FCM books the give-up at a different price than the fund's OMS.
- Pull the original execution confirmation from the executing broker.
- Compare against CME/ICE time and sales for the exact execution timestamp.
- If executing broker confirm matches time and sales, request FCM correction.
- FCM must correct within T+1. If they refuse, escalate to FCM relationship manager with documentation.

**Quantity dispute:** FCM books a different quantity than what was executed.
- Same process as price dispute. The executing broker's confirm and the exchange fill report are the authoritative sources.
- Partial fill disputes: confirm how many lots actually crossed on the exchange. The executing broker may have submitted a block for a partial fill.

**Account allocation dispute:** Trade booked to wrong account (e.g., Fund A vs. Fund B).
- Correctable by the FCM via internal transfer on T+0 or T+1 if caught quickly.
- Call FCM operations immediately; have both account numbers ready.
- After T+1, account transfers may require exchange approval — FCM relationship manager must be involved.

**Margin dispute (give-up related):** Margin charged on a give-up trade differs from expectation.
- Confirm the clearing FCM is using the correct margin rate for the contract and account type (hedge vs. speculative).
- LME give-ups: confirm the tenor is correctly identified — broken date vs. standard prompt affects margin materially.
- If FCM confirms their margin is correct but it differs from your calculation, pull the exchange's published SPAN margin parameters and reconcile line by line.

---

## LME Give-Up Specifics

LME give-ups have additional complexity vs. CME/ICE:

1. **Prompt date confirmation:** Every LME give-up must specify the exact prompt date (settlement date), not a contract month. Confirm the prompt date with the executing broker before submitting.
2. **Ring trading:** LME Ring trades may have different give-up deadlines than electronic trades. Confirm with the FCM give-up desk for any Ring-executed trades.
3. **Carry trades:** LME spreads (carries) between two prompt dates must be given up as two separate legs. Ensure both legs clear to the same account or the hedge is broken.
4. **Approval chain:** LME give-ups involving broken dates > 3 months forward may require FCM credit approval in addition to standard give-up acceptance.

---

## Give-Up Fee Tracking

Executing brokers charge a give-up fee (typically $0.50–$2.00 per lot, paid by the clearing FCM who charges it back to the fund). Track monthly:

1. Download the give-up fee invoice from each executing broker at month-end.
2. Reconcile against FCM's monthly give-up fee statement.
3. Discrepancies > $500 or 5%: dispute with FCM. They will request a corrected invoice from the executing broker.
4. File invoices in `billing/give-up-fees/YYYY-MM/`.

---

## Escalation Matrix

| Situation | Contact | Timeline |
|---|---|---|
| Give-up PENDING past 4:00 PM CT | FCM give-up desk | Same day |
| Give-up REJECTED | FCM give-up desk + Executing broker | Within 15 min |
| Rejection unresolved at EOD | Senior Ops Manager + CFO | EOD T+0 |
| Uncleared position overnight | Compliance + CFO + PM | Immediately |
| FCM trade dispute | FCM operations → FCM relationship manager | T+1 resolution target |

---

## Related Documents

- Futures Margin Call Escalation Playbook
- Prime Broker Onboarding and SSI Setup
- Recon Break Triage Workflow
- CME Give-Up Agreement template (see Legal folder)
