"""Read-only source/config review. Does not execute deployment code or contact AWS."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / 'deployment/configure-monitoring-baseline.py'
    tree = ast.parse(source.read_text(encoding='utf-8'))
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                constants[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass

    def literal(node):
        if isinstance(node, ast.Name):
            return constants[node.id]
        if isinstance(node, ast.List):
            return [literal(item) for item in node.elts]
        if isinstance(node, ast.Dict):
            return {literal(k): literal(v) for k, v in zip(node.keys, node.values)}
        return ast.literal_eval(node)

    call = next(node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'put_metric_alarm')
    actual = {kw.arg: literal(kw.value) for kw in call.keywords}
    expected = json.loads((ROOT / 'deployment/c-t08-alarm-review.json').read_text(encoding='utf-8'))['expected_readback']
    for name, value in expected.items():
        assert actual[name] == value, (name, actual[name], value)
    resources = json.loads((ROOT / 'project/aws-resources.json').read_text(encoding='utf-8'))
    assert resources['load_balancer']['arn'].split('loadbalancer/')[1] == constants['lb']
    assert resources['load_balancer']['target_group'].split(':targetgroup/')[1] == constants['tg'].split('targetgroup/')[1]
    print(json.dumps({'scope': 'OFFLINE repository-source comparison; no AWS accessed', 'alarm_expected_fields_matched': len(expected), 'resource_dimension_match': True, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'historical_notifications': resources['monitoring']['notifications'], 'live_readback': False}, indent=2))
    files = ['sources/text/S12-INFS3701_Group_Assignment.md', 'sources/text/S13-INFS3701_Group_Assignment_Marking_Scheme.md', 'docs/interfaces.md', 'project/handoffs.json', 'docs/2026-11-01-foundation-verification.md']
    for name in files:
        data = (ROOT / name).read_bytes()
        print(json.dumps({'reviewed_reference': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}))


if __name__ == '__main__':
    main()
