"""Offline document checks; not AWS service or effective IAM validation."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def main():
    pdf=ROOT/'output/pdf/reading-tracker-architecture.pdf'
    reader=PdfReader(pdf)
    assert len(reader.pages)==1
    page=reader.pages[0]
    text=page.extract_text()
    inventory=json.loads((ROOT/'project/aws-resources.json').read_text(encoding='utf-8'))
    required=['HTTP :80','HTTP :8000','HTTPS :443','Amazon DynamoDB','Amazon S3','Amazon CloudWatch',
              'EBS root: 8 GiB gp3, encrypted','Automatic scaling deferred','whole AZ not tested','certificate unresolved']
    required += [s['cidr'] for s in inventory['vpc']['subnets']]
    required += [h[k] for h in inventory['compute'] for k in ['id','az','private_ip']]
    for value in required:assert value in text, f'Missing architecture element: {value}'
    assert float(page.mediabox.width)>float(page.mediabox.height)
    config=json.loads((ROOT/'project/config.json').read_text(encoding='utf-8'))
    assert config['enhancements_enabled'] is False
    assert config['enhancement_decision']['prepared_surge_is_authorized_to_deploy'] is False
    policy=json.loads((ROOT/'deployment/policies/proposed-app-permissions-not-attached.json').read_text())
    assert policy['Version']=='2012-10-17' and len(policy['Statement'])==2
    for statement in policy['Statement']:
        assert '*' not in statement['Resource']
        assert statement['Condition']['Bool']['aws:SecureTransport']=='true'
    # Integrity/provenance check, not semantic AWS policy validation.
    icons=json.loads((ROOT/'assets/aws/manifest.json').read_text())
    for meta in icons['files'].values():
        assert hashlib.sha256((ROOT/'assets/aws'/meta['png']).read_bytes()).hexdigest()==meta['sha256']
    files=['output/pdf/reading-tracker-architecture.pdf','output/pdf/reading-tracker-architecture.png',
           'scripts/build_architecture_pdf.py','docs/architecture-review-2026-11-11.md',
           'docs/network-security-chapter-2026-11-11.md','docs/tutor-questions-ready-en.md',
           'deployment/policies/proposed-app-permissions-not-attached.json','docs/design-report-working.md']
    report=(ROOT/'docs/design-report-working.md').read_text(encoding='utf-8')
    body=report.split('## 1. Objective and scope',1)[1].split('## References and internal evidence',1)[0]
    print(json.dumps({'at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'pdf_pages':len(reader.pages),'page_points':[float(page.mediabox.width),float(page.mediabox.height)],
        'required_text_checks':len(required),'icon_hashes_checked':len(icons['files']),
        'policy_check':'JSON/scoping/TLS fields only; no IAM simulation or attachment',
        'report_body_whitespace_words_including_headings':len(body.split()),
        'report_pages':'not rendered; full design report PDF remains outstanding',
        'aws_calls':0,'hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}},indent=2))


if __name__=='__main__':main()
