---
title: Prime Broker Onboarding and SSI Setup
doc_type: playbooks
domain: prime-brokerage
updated: 2025-02
version: 1.8
---

# Prime Broker Onboarding and SSI Setup

## Purpose

This playbook covers the end-to-end process for onboarding a new prime broker relationship: legal documentation, account setup, SSI (Standard Settlement Instructions) configuration, and operational readiness testing. It also covers ongoing SSI maintenance for existing prime broker relationships.

Incomplete onboarding is one of the most common causes of first-trade settlement failures. This checklist ensures every dependency is in place before live trading begins.

---

## Phase 1: Legal and Compliance (Weeks 1–4)

### 1.1 Required Agreements

The following agreements must be fully executed before any trading activity:

| Document | Owner | Notes |
|---|---|---|
| Prime Brokerage Agreement (PBA) | Legal + CFO | Master agreement governing the relationship |
| Securities Lending Agreement | Legal | Required for short selling and stock borrow |
| Futures Give-Up Agreement | Legal + Ops | Required if clearing futures through the prime |
| ISDA Master Agreement | Legal | Required for OTC derivatives (if applicable) |
| Credit Support Annex (CSA) | Legal | Collateral terms for OTC margining |
| Electronic Trading Agreement | Legal + Technology | Required for DMA or algo access |
| Anti-Money Laundering (AML) Documents | Compliance | KYC package — entity docs, beneficial ownership |

**Compliance checklist before agreement execution:**
- [ ] Prime broker passed internal counterparty credit review
- [ ] Prime broker is an FINRA member and SIPC participant (U.S.)
- [ ] Prime broker's clearing entity confirmed (some prime services are provided by the broker but cleared by an affiliated bank)

### 1.2 Account Documentation

While legal negotiates agreements, compliance and operations prepare:

- **Entity documentation:** Certificate of formation/incorporation, operating agreement, authorized signatories list
- **Beneficial ownership:** FINCEN form or equivalent per prime broker's KYC requirements
- **Tax documentation:** W-9 (U.S. entities) or W-8BEN-E (non-U.S. entities)
- **Investment management agreement:** Prime broker may require a copy of the IMA between the fund and its manager

Target: submit all documentation within 5 business days of receiving the prime broker's onboarding package.

---

## Phase 2: Account Setup (Weeks 3–6, overlapping with Phase 1)

### 2.1 Account Structure

Define the account structure before setup begins:

- **Account types needed:** Cash, margin, short, futures (separate DTC participant account vs. sub-account)
- **Fund entities:** Each legal entity (master fund, feeder, separately managed account) typically requires its own prime broker account
- **Currency accounts:** Identify which currencies require dedicated cash accounts (USD, EUR, GBP, JPY minimum for most multi-strat funds)
- **Rehypothecation limits:** Negotiate and confirm what percentage of long assets the prime broker can rehypothecate. Standard U.S. cap is 140% of the debit balance under Regulation T.

### 2.2 DTC/NSCC Setup

For U.S. equity settlement:

1. Obtain the prime broker's DTC Participant Number (confirm it's the clearing entity's DTC number, not the executing broker's).
2. Confirm the fund's DTC account number (sub-account or omnibus) with the prime broker operations team.
3. Test DTC connectivity: the prime broker operations team should send a test DTC message to your operations system before go-live.

### 2.3 SWIFT Setup (for international custodians and cross-border)

1. Confirm prime broker's SWIFT BIC code for settlement messages.
2. Confirm MT540/541/542/543 message formats (receive/deliver free vs. versus payment).
3. If using a third-party custodian alongside the prime, the custodian and prime broker must exchange SWIFT connectivity details.

---

## Phase 3: SSI Configuration (Weeks 4–6)

Standard Settlement Instructions are the routing information that directs where securities and cash are delivered. Incorrect SSIs cause settlement failures on the first day of trading.

### 3.1 Collecting SSIs from the Prime Broker

Request the following from the prime broker's SSI/settlement team:

**For U.S. equities (DTC):**
```
DTC Participant Number: [####]
Account Number: [fund account at DTC]
Account Name: [legal entity name exactly as registered]
```

**For U.S. Treasuries and fixed income (Fedwire):**
```
ABA/Routing Number: [prime bank ABA]
Account Number: [prime's Fed account]
Account Name: [prime entity name]
Further Credit: [fund account number]
```

**For cash wires (USD):**
```
Bank Name: [prime's bank]
ABA/Routing Number: [9-digit ABA]
Account Number: [prime's account]
Account Name: [prime entity]
Reference / FFC: [fund account number + fund name]
```

**For international equities (Euroclear/Clearstream):**
```
Euroclear/Clearstream Account: [####]
BIC/SWIFT: [prime entity BIC]
Account Name: [fund name]
```

### 3.2 Loading SSIs into the OMS/EMS

1. Enter all SSIs in the OMS counterparty database under the prime broker's counterparty record.
2. Tag each SSI with: asset class, currency, settlement method (DTC, Fedwire, SWIFT, etc.).
3. Have a second operations associate verify all SSIs independently against the prime broker's official SSI document (four-eyes check). Do not skip this step — SSI errors are a leading cause of first-trade fails.
4. Date-stamp the SSI entry and file the source document in `onboarding/[prime-broker-name]/SSIs/`.

### 3.3 Providing Our SSIs to the Prime Broker

The prime broker also needs the fund's settlement instructions for delivering securities and cash to the fund (for sells and income payments). Provide:

- The fund's custodian DTC Participant Number (if assets are held at a third-party custodian)
- Cash wire instructions for each currency
- Contact list: operations primary, secondary, and after-hours contacts

Confirm the prime broker has loaded the fund's SSIs in their system before go-live.

---

## Phase 4: Operational Readiness Testing (Week 5–6)

### 4.1 Systems Access

Before go-live, confirm the following access is provisioned and tested:

- [ ] Prime broker client portal (position reports, trade blotter, margin reports)
- [ ] Statement download access (daily position and transaction files)
- [ ] Margin call notification setup (email + portal alerts)
- [ ] Give-up submission access (EGUS for CME, equivalent for ICE) — if applicable
- [ ] Fail/DK notification setup

### 4.2 Connectivity Test

1. Request a test file from the prime broker's file delivery team (test position file in the format they'll deliver daily — CSV, XML, or SWIFT).
2. Load the test file into the reconciliation system and confirm it parses cleanly.
3. Identify any field mapping issues (different column headers, date formats, CUSIP vs. ISIN, etc.) and resolve before go-live.

### 4.3 Operational Contacts

Collect and file the following contacts from the prime broker:

| Function | Contact Type |
|---|---|
| Daily operations (breaks, fails, DKs) | Direct phone + email |
| Give-up desk (futures) | Direct phone (time-sensitive) |
| Margin desk | Direct phone + email |
| Client relationship manager | Primary escalation |
| After-hours emergency line | Phone only |
| Technology/file delivery | Email |

Store in `onboarding/[prime-broker-name]/contacts.md`. Keep this current — turnover at prime broker desks is high.

### 4.4 Go-Live Checklist

Complete all items before authorizing the first live trade:

- [ ] All agreements fully executed and countersigned copies received
- [ ] Account numbers confirmed with prime broker operations
- [ ] SSIs loaded in OMS and independently verified
- [ ] Fund's SSIs confirmed loaded at prime broker
- [ ] DTC/SWIFT connectivity tested
- [ ] Statement file delivery tested and reconciliation system parsing confirmed
- [ ] All portal access provisioned and tested
- [ ] Contact list complete and filed
- [ ] First-trade notification sent to prime broker ops (date, expected asset class, approximate size)

**Do not trade until all items are checked.** A missed item on this list has caused a first-trade settlement failure on every occasion it has occurred.

---

## SSI Maintenance (Ongoing)

### When SSIs change

Prime brokers change settlement instructions when they: switch clearing banks, merge entities, change DTC numbers after an acquisition, or restructure sub-accounts.

The prime broker is required to give advance notice (typically 30 days), but operational teams often receive the notice late. Establish a standing process:

1. **Monthly check:** On the first business day of each month, confirm SSIs on file match the prime broker's current published SSI sheet (most post to their client portal).
2. **Change notification:** If a change is received, update the OMS immediately and send confirmation to the prime broker that you've updated your records.
3. **Change log:** Maintain an SSI change log: `onboarding/[prime-broker-name]/ssi-changelog.md` with date, old SSI, new SSI, and who made the change.

### When a counterparty SSI causes a fail

If a settlement fails because the prime broker's SSI has changed without notification:

1. Contact the prime broker operations desk immediately. They can redirect the failed delivery same-day in most cases.
2. Request written confirmation of the correct SSI and update the OMS.
3. File a complaint with the prime broker relationship manager if the change was not communicated with adequate notice.

---

## Related Documents

- Equity Trade Settlement and DK Resolution SOP
- CME Give-Up Agreement and FCM Dispute Resolution SOP
- Recon Break Triage Workflow
- Counterparty Credit Review Policy (see Compliance folder)
