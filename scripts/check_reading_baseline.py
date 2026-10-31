"""Offline baseline check. Does not import Flask/boto3 or contact AWS."""
import ast
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
source=root/'app/reading_tracker.py'
tree=ast.parse(source.read_text(encoding='utf-8'),filename=str(source))
function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='compute_stats')
namespace={}
exec(compile(ast.Module(body=[function],type_ignores=[]),'<isolated original statistics>','exec'),namespace)
records=[{'status':'reading','pages_read':30,'rating':'4'},
    {'status':'finished','pages_read':120,'rating':'2'},
    {'status':'want','pages_read':0,'rating':None}]
actual=namespace['compute_stats'](records)
assert actual=={'total':3,'reading':1,'finished':1,'want':1,'total_pages':150,'avg_rating':3.0},actual
empty=namespace['compute_stats']([])
assert empty['total']==0 and empty['avg_rating'] is None and empty['total_pages']==0
print(json.dumps({'source':'app/reading_tracker.py','syntax':'passed','original_statistics':'passed',
    'empty_library_statistics':'passed','full_web_runtime_tested':False,'AWS_accessed':False,
    'next_check':'Install the listed dependencies, verify the web form locally, then replace/configure the data layer.'},ensure_ascii=False,indent=2))
