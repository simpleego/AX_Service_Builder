from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import text
from .database import engine
from .todos import router as todo_router
@asynccontextmanager
async def lifespan(_app):
    with engine.connect() as connection:
        connection.execute(text('SELECT 1'))
    yield
    engine.dispose()
app = FastAPI(title='Todo API - API 아키텍처 & 인증 보안', version='2.0.0',
    description='48시간 단계별 실습. 인증과 Todo 소유권을 Postman으로 검증합니다.',
    docs_url=None, redoc_url=None, openapi_url='/openapi.json', lifespan=lifespan)
@app.exception_handler(StarletteHTTPException)
async def http_error(_request: Request, exc):
    return JSONResponse({'error': {'code': str(exc.detail)}}, status_code=exc.status_code, headers=exc.headers)
@app.exception_handler(RequestValidationError)
async def validation_error(_request: Request, exc):
    # 검증 오류에 비밀번호 등 입력 원문을 포함하지 않는다.
    fields = [{'loc': list(e['loc']), 'type': e['type'], 'message': e['msg']} for e in exc.errors()]
    return JSONResponse({'error': {'code': 'VALIDATION_ERROR', 'fields': fields}}, status_code=422)
@app.exception_handler(Exception)
async def internal_error(_request: Request, _exc):
    return JSONResponse({'error': {'code': 'INTERNAL_ERROR'}}, status_code=500)
@app.middleware('http')
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    if request.url.path.startswith('/api/auth'):
        response.headers['Cache-Control'] = 'no-store'
    return response
@app.get('/health', tags=['Health'], summary='DB 연결 확인')
def health():
    with engine.connect() as connection:
        connection.execute(text('SELECT 1'))
    return {'status': 'ok'}
app.include_router(todo_router)
