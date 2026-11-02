"""외부 패키지 없이 최종 Python 소스와 JSON/버전 완결성을 검사한다."""
import ast, json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
count = 0
for folder in ['versions', 'scripts', 'tests', 'postman', 'specs']:
    for path in (root/folder).rglob('*'):
        if not path.is_file() or '.venv' in path.parts or '__pycache__' in path.parts:
            continue
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            count += 1
        elif path.suffix == '.json':
            json.loads(path.read_text(encoding='utf-8'))
            count += 1
for version in (root/'versions').iterdir():
    for file in ['app/main.py', 'app/database.py', '.env.example', 'requirements.txt', 'README.md']:
        assert (version/file).is_file(), f'{version.name}: {file} 누락'
assert len(list((root/'versions').iterdir())) == 7
print(f'PASS: {count} Python/JSON files and seven standalone versions')
