"""버전마다 새 Python 프로세스를 사용하여 app 패키지 import 캐시를 격리한다."""
import os, sys, subprocess
from pathlib import Path
root = Path(__file__).resolve().parents[1]
for version in sorted((root/'versions').iterdir()):
    print(f'\n=== {version.name} ===', flush=True)
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', 'tests'], cwd=root,
        env={**os.environ, 'TEST_VERSION':version.name, 'PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1'}, timeout=180)
    if result.returncode:
        raise SystemExit(result.returncode)
