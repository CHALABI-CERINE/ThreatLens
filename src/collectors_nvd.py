"""A simple NVD collector that fetches recent CVE JSON feed and stores new alerts in the DB.
This is a pragmatic, robust starter implementation. For production you should use the official NVD APIs
with an API key, rate limiting, error handling, and tests.
"""
from datetime import datetime
import requests
from .db import SessionLocal
from .models import Alert
import time

NVD_RECENT_URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0'  # NVD v2 search


def fetch_nvd(query_params=None, max_results=50):
    """Fetch recent CVE items from NVD. query_params can be dict for search filters.
    Returns list of dicts with keys: cve_id, severity, summary, published_date, raw
    """
    params = query_params.copy() if query_params else {}
    params.setdefault('resultsPerPage', str(max_results))

    try:
        resp = requests.get(NVD_RECENT_URL, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print('NVD fetch error:', e)
        return []

    items = []
    for it in data.get('vulnerabilities', []):
        cve = it.get('cve') or {}
        cve_id = cve.get('id') or cve.get('CVE_data_meta', {}).get('ID')
        # summary extraction (best-effort)
        summary = ''
        descriptions = cve.get('descriptions') or []
        if descriptions:
            summary = descriptions[0].get('value','')

        # severity extraction: NVD v2 has metrics
        severity = 'Unknown'
        metrics = it.get('cveMetrics') or it.get('metrics') or {}
        # crude attempts to fetch severity
        if isinstance(metrics, dict):
            # try common CVSS v3 or v2
            cvss = metrics.get('cvssMetricV31') or metrics.get('cvssMetricV30') or metrics.get('cvssMetricV2')
            if cvss:
                try:
                    score = float(cvss[0].get('cvssData', {}).get('baseScore') or 0)
                    if score >= 9:
                        severity = 'Critical'
                    elif score >= 7:
                        severity = 'High'
                    elif score >= 4:
                        severity = 'Medium'
                    else:
                        severity = 'Low'
                except:
                    pass

        published = None
        p = cve.get('published') or cve.get('publishedDate') or None
        if p:
            try:
                published = datetime.fromisoformat(p.replace('Z','+00:00'))
            except Exception:
                published = None

        items.append({
            'cve_id': cve_id,
            'severity': severity,
            'summary': summary,
            'published_date': published,
            'raw': str(it)
        })

    return items


def store_alerts(alert_items):
    """Insert new alerts into DB, deduplicating by cve_id and summary."""
    db = SessionLocal()
    added = 0
    try:
        for a in alert_items:
            q = db.query(Alert)
            if a.get('cve_id'):
                exists = q.filter(Alert.cve_id == a['cve_id']).first()
            else:
                exists = q.filter(Alert.summary == a['summary']).first()
            if exists:
                continue
            alert = Alert(
                cve_id=a.get('cve_id'),
                source='NVD',
                severity=a.get('severity') or 'Unknown',
                summary=a.get('summary') or '',
                published_date=a.get('published_date'),
                raw=a.get('raw')
            )
            db.add(alert)
            added += 1
        db.commit()
    except Exception as e:
        db.rollback()
        print('store_alerts error:', e)
    finally:
        db.close()
    return added


if __name__ == '__main__':
    items = fetch_nvd({'pubStartDate':''}, max_results=20)
    print('fetched', len(items))
    print('storing', store_alerts(items))
"""