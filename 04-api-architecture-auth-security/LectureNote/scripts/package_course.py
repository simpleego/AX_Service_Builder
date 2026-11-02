"""비밀값/가상환경/보관 초안을 제외한 수업 배포 ZIP을 생성한다."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).resolve().parents[1]
out = root/'output'/'todo-api-course.zip'
out.parent.mkdir(exist_ok=True)
files = [root/name for name in ['README.md','requirements-dev.txt','requirements-lock.txt','.gitignore']]
for folder in ['versions','database','docs','postman','scripts','specs','tests']:
    files.extend(path for path in (root/folder).rglob('*') if path.is_file()
        and not any(part in {'.venv','__pycache__','.pytest_cache','node_modules'} for part in path.parts)
        and path.name != '.env' and path.suffix != '.pyc')
with ZipFile(out, 'w', ZIP_DEFLATED) as archive:
    for path in sorted(files):
        archive.write(path, path.relative_to(root))
with ZipFile(out) as archive:
    assert archive.testzip() is None
    assert not any(name.endswith('/.env') for name in archive.namelist())
print(f'{out}: {len(files)} files, {out.stat().st_size:,} bytes')
