"""固定样例函数的可信验证器；不由执行者修改。"""
import json
import sys
from pathlib import Path


SCRIPT = '''
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("sample_feature", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
function = module.due_for_review
assert function(100, 30, 129) is False
assert function(100, 30, 130) is True
assert function(100, 30, 131) is True
assert function(100, 0, 100) is True
assert function(100, 0, 101, hold=True) is False
for hold in (False, True):
    try:
        function(100, -1, 100, hold=hold)
    except ValueError:
        pass
    else:
        raise AssertionError("negative retention must raise ValueError")
print(json.dumps({"passed": True, "cases": 7}))
'''


def verifier_digest():
    from .paths import digest
    return digest(Path(__file__))


def validate_feature(root):
    from .paths import checked, digest
    from .runtime import run_bounded
    source = checked(root, 'workspace/feature.py')
    before = digest(source)
    receipt = run_bounded(
        [sys.executable, '-I', '-c', SCRIPT, str(source)], root,
        checked(root, '.runtime/verification'), 10, 65536,
    )
    report = json.loads(receipt['stdout'])
    if before != digest(source) or report != {'passed': True, 'cases': 7}:
        raise ValueError('source changed or invalid verifier result')
    return report | {'source_digest': before, 'verifier_digest': verifier_digest()}
