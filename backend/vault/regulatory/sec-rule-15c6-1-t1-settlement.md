---
title: SEC Rule 15c6-1 — T+2 Standard Settlement Cycle
doc_type: regulatory
domain: settlement
updated: 2024-05
version: 2.0
---

# SEC Rule 15c6-1 — Standard Settlement Cycle for Securities Transactions

## Rule Summary

SEC Rule 15c6-1 under the Securities Exchange Act of 1934 establishes the standard settlement cycle for most broker-dealer securities transactions in the United States.

**Current requirement (effective May 28, 2024):** Most securities transactions must settle no later than **T+1** (one business day after the trade date).

> **Important:** The U.S. moved from T+2 to T+1 settlement effective May 28, 2024. Any internal SOPs or counterparty agreements referencing T+2 as the standard must be updated to reflect T+1.

---

## Scope: What Transactions Are Covered

**Covered under Rule 15c6-1 (must settle T+1):**
- U.S. equity securities (NYSE, NASDAQ, OTC)
- Corporate bonds
- Municipal securities
- Unit investment trusts (UITs)
- ETFs
- ADRs (American Depositary Receipts)

**Exempt from T+1 (different settlement cycles apply):**
- U.S. Treasury securities (T+1 already, now effectively same-day for some)
- Government agency securities
- Options contracts (T+1 for premium, T+0 for exercise)
- Futures contracts (governed by CFTC, not SEC)
- Repos and reverse repos (contractual settlement)
- Foreign sovereign debt (varies by jurisdiction)
- Transactions where both parties expressly agree to a different settlement date at the time of the transaction

---

## Operational Impact of T+1

The move from T+2 to T+1 compressed the time available for post-trade processing. Key operational changes required:

### Same-day affirmation (SDA)

Institutional investors must affirm trades with their custodian or prime broker by **9:00 PM ET on trade date** (T+0) for T+1 settlement to be achievable. This replaced the prior T+1 affirmation window.

- **Action required:** Ensure your OMS submits allocation and affirmation messages to the prime broker no later than 7:00 PM ET on trade date.
- **Monitoring:** Track SDA rate daily. An SDA rate below 90% will result in elevated settlement fails. Industry target is 98%+.

### Allocation turnaround

For block trades requiring allocation across multiple funds:
- Allocations must be submitted to the executing broker and prime broker by **6:00 PM ET on trade date** (was end of T+0 under T+2, now the window is tighter).
- Executing brokers will not hold allocations overnight — if not received by their cutoff, the block may be returned unallocated.

### FX settlement for foreign securities

For non-USD securities: the FX leg must be booked and confirmed by **10:00 AM ET on trade date** to ensure FX settles in time for T+1 securities delivery. This is the most operationally challenging aspect of T+1 for international portfolios.

### Stock loan / short selling

Locates must be confirmed before order entry (no change), but borrow must be **confirmed and allocated** by the prime broker by end of trade date. Primes may pull locates if not converted to borrows same day, potentially causing a short sale violation.

---

## Rule 15c6-2: Institutional Trade Processing Requirements

Alongside T+1, the SEC adopted Rule 15c6-2, which requires broker-dealers to establish, maintain, and enforce written policies and procedures reasonably designed to ensure same-day affirmation.

**What this means operationally:**
- Your prime broker is required to have SDA procedures in place and will hold you accountable for affirming on time.
- Primes may impose fees or penalties for chronic late affirmation (industry practice is still developing).
- Compliance should document your firm's SDA procedures and monitor the daily affirmation rate.

---

## Fails Management Under T+1

Settlement fails are more visible and more consequential under T+1:

- **Buy-in risk accelerates:** Under T+2, a fail on T+1 had until T+2 to resolve before buy-in risk began. Under T+1, buy-in risk begins at T+1 — effectively the same day as the expected settlement date.
- **DTCC CNS:** The DTCC's Continuous Net Settlement (CNS) system nets fails across the market, which provides some buffer, but individual fails against specific counterparties (non-CNS) remain at risk.
- **Locate documentation for shorts:** Maintain records of all short sale locates for six years per Rule 17a-4. T+1 does not change this requirement but increases scrutiny on same-day borrow confirmation.

---

## Exceptions and Extended Settlement

Parties may contractually agree to settlement beyond T+1 **at the time of the transaction** (not retroactively). Extended settlement agreements must be:
- Documented in writing (email confirmation is acceptable)
- Mutual (both parties must agree)
- Specified before or at the time of trade execution

Common use cases for extended settlement:
- When-issued trading (securities not yet issued)
- Cross-border transactions where foreign settlement cycles exceed T+1
- Certain private placement transactions

---

## Compliance and Reporting Implications

- **FINRA Rule 11860:** Addresses COD (Cash on Delivery) transactions and extended settlement — ensure any COD arrangements comply.
- **Regulation SHO:** T+1 does not modify short sale locate or close-out requirements. Failure to deliver (FTD) thresholds under Reg SHO remain unchanged.
- **Form N-CEN / Form ADV:** Investment advisers should confirm their compliance policies reference the T+1 standard in disclosures.

---

## Key Dates Reference

| Date | Event |
|---|---|
| March 15, 2017 | SEC adopted T+2 rule (moved from T+3) |
| May 28, 2024 | SEC T+1 rule effective; U.S. equities move to T+1 standard |
| June 2024 | Canada and Mexico simultaneously moved to T+1 |
| TBD | EU, UK, and Asia-Pacific evaluating T+1 transition (ongoing regulatory discussions) |

---

## Related Documents

- Equity Trade Settlement and DK Resolution SOP
- Recon Break Triage Workflow
- SEC Rule 17a-3 and 17a-5 Summary (books and records)
- DTCC Settlement Guide (external reference)
