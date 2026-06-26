"""
Regulatory alert engine.
Run via cron: python -m app.core.reg_alerts
Or hit the POST /api/alerts/refresh endpoint manually.

Fetches SEC and CFTC RSS feeds → filters for ops-relevant releases →
summarizes with Claude → stores in Postgres alerts table.
"""
import os
import json
import hashlib
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
import anthropic

ANTHROPIC_CLIENT = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

RSS_FEEDS = [
    {
        "name": "SEC Press Releases",
        "url": "https://www.sec.gov/rss/news/pressreleases.xml",
        "regulator": "SEC",
    },
    {
        "name": "CFTC Press Releases",
        "url": "https://www.cftc.gov/rss/pressreleases",
        "regulator": "CFTC",
    },
]

# Keywords that indicate ops-relevant releases
OPS_KEYWORDS = [
    "settlement", "clearing", "margin", "repo", "swap", "reporting",
    "trading", "prime broker", "custody", "reconciliation", "futures",
    "derivatives", "short sale", "fail", "rule 15c", "rule 17a",
    "cat ", "consolidated audit", "CAT", "DTCC", "DTC", "CME", "ICE",
]

SUMMARY_SYSTEM = """You are a capital markets regulatory analyst.
Given a regulatory press release or rule announcement, extract:
1. A concise title (max 10 words)
2. Severity: high | medium | low (based on operational impact)
3. Impacted workflows (comma-separated from: settlement, clearing, margin, reporting, trading, custody, recon)
4. A 2-3 sentence plain-English summary of what changed and what ops teams need to do.

Respond ONLY as JSON with keys: title, severity, workflows, summary.
"""


def is_ops_relevant(text: str) -> bool:
    lower = text.lower()
    return any(kw.lower() in lower for kw in OPS_KEYWORDS)


def parse_feed(feed_url: str) -> list[dict]:
    """Fetch and parse RSS feed items."""
    try:
        resp = httpx.get(feed_url, timeout=15, follow_redirects=True)
        resp.raise_for_status()
    except Exception as e:
        print(f"Feed fetch failed: {feed_url} — {e}")
        return []

    root = ET.fromstring(resp.text)
    items = []
    for item in root.iter("item"):
        title = item.findtext("title", "")
        desc  = item.findtext("description", "")
        link  = item.findtext("link", "")
        pub   = item.findtext("pubDate", "")
        items.append({"title": title, "description": desc, "link": link, "pub": pub})
    return items


def summarize_release(title: str, description: str) -> dict:
    """Use Claude to extract structured summary from a regulatory release."""
    prompt = f"Title: {title}\n\nContent: {description[:2000]}"
    resp = ANTHROPIC_CLIENT.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=SUMMARY_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    # Strip markdown fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "title": title[:80],
            "severity": "medium",
            "workflows": "general",
            "summary": description[:300],
        }


def run_alert_refresh() -> list[dict]:
    """
    Main entry: fetch all feeds, filter, summarize, return structured alerts.
    In production, persist to Postgres and deduplicate by content hash.
    """
    alerts = []

    for feed in RSS_FEEDS:
        print(f"Fetching {feed['name']}...")
        items = parse_feed(feed["url"])

        for item in items[:20]:  # process latest 20 per feed
            combined = f"{item['title']} {item['description']}"
            if not is_ops_relevant(combined):
                continue

            content_hash = hashlib.md5(combined.encode()).hexdigest()
            print(f"  Summarizing: {item['title'][:60]}...")
            summary = summarize_release(item["title"], item["description"])

            alerts.append({
                "hash":       content_hash,
                "regulator":  feed["regulator"],
                "link":       item["link"],
                "published":  item["pub"],
                "fetched_at": datetime.utcnow().isoformat(),
                **summary,
            })

    print(f"\nProcessed {len(alerts)} ops-relevant alerts.")
    return alerts


if __name__ == "__main__":
    results = run_alert_refresh()
    print(json.dumps(results, indent=2))
