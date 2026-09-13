# 04. 고차함수와 동기/비동기 - 수업용 실습

## 고차함수 5대장
```js
const names = users.map(u => u.name);
const highScore = users.filter(u => u.score >= 85);
const total = users.reduce((acc, cur) => acc + cur.score, 0);
const sorted = [...users].sort((a,b) => b.score - a.score);
users.forEach(u => console.log(u.name));
```

## 고차함수 만들기
```js
function createLogger(prefix){
  return function(message){ console.log(`[${prefix}] ${message}`); }
}
function withAuth(fn){
  return async function(...args){
    const token = localStorage.getItem('token');
    if(!token) throw new Error('로그인 필요');
    return await fn(...args);
  }
}
```

## 동기 vs 비동기
```js
console.log('1 주문');
setTimeout(()=> console.log('2 커피 완성'), 3000);
console.log('3 서빙'); // 순서 1->3->2

function getUserPromise(id){
  return new Promise((resolve, reject)=>{
    setTimeout(()=> id>0 ? resolve({id, name:'철수'}) : reject('ID 오류'), 1000);
  });
}

async function example(){
  try{
    const user = await getUserPromise(1);
  } catch(err){ console.error(err); }
}
```

## 통합 실습: AI 로그 분석기
practice/lab-higher-order-async.js 참고
