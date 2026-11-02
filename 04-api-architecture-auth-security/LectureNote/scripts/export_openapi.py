"""선택 버전의 실제 FastAPI 앱에서 OpenAPI를 내보낸다. DB 접속 없이 스키마만 생성한다."""
import os, sys, json, importlib
from pathlib import Path
root = Path(__file__).resolve().parents[1]
version = sys.argv[1] if len(sys.argv) > 1 else 'v06-postman'
target = root/'versions'/version
if target.parent != root/'versions' or not (target/'app/main.py').is_file():
    raise SystemExit('유효한 버전 이름을 지정하세요.')
# 문서 출력 전용 임시 키. 실제 서버에서는 .env의 무작위 키가 필요하다.
os.environ.setdefault('JWT_SECRET', 'documentation-only-key-0123456789abcdef')
sys.path.insert(0, str(target))
app = importlib.import_module('app.main').app
out = root/'specs'/f'{version}.openapi.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(app.openapi(), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(out)
