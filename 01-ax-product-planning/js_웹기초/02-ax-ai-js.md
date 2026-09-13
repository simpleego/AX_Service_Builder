# 02. AX AI 전환 관점의 JS

## 1. AI API 표준 패턴
```js
const aiApi = axios.create({
  baseURL: 'https://api.openai.com/v1',
  headers: { 'Authorization': `Bearer ${process.env.OPENAI_API_KEY}` },
  timeout: 60000
});
```

## 2. 스트리밍 핵심
Node:
```js
const res = await axios.post('/chat/completions', { model: 'gpt-4o-mini', stream: true, messages }, { responseType: 'stream' });
res.data.on('data', chunk => {
  const lines = chunk.toString().split('\n').filter(l=>l.trim()!=='');
  for(const line of lines){
    if(line.includes('[DONE]')) return;
    if(line.startsWith('data: ')){
      const json = JSON.parse(line.replace('data: ', ''));
      const text = json.choices[0]?.delta?.content;
      if(text) process.stdout.write(text);
    }
  }
});
```

Frontend:
```js
const res = await fetch('/api/chat', { method: 'POST', body: JSON.stringify({prompt}) });
const reader = res.body.getReader();
const decoder = new TextDecoder();
while(true){
  const { done, value } = await reader.read();
  if(done) break;
  console.log(decoder.decode(value));
}
```

## 3. 필수 문법 5개
- 구조분해 + 옵셔널체이닝
- Promise.all 병렬 처리
- 템플릿 리터럴로 프롬프트 생성
- Array 고차함수 map/filter/slice
- 환경변수
