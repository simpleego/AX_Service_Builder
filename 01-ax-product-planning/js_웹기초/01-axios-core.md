# 01. Ax(Axios) 사용을 위한 핵심 자바스크립트

## 핵심 1: Promise / async-await
```js
// then 방식
axios.get('/api/user').then(res => console.log(res.data))

// async/await 방식 (실무 표준)
async function getUser() {
  try {
    const res = await axios.get('/api/user');
    console.log(res.data);
  } catch (error) {
    console.error(error.response?.data);
  }
}
```

## 핵심 2: Axios 5대 문법
```js
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
});

const { data } = await api.get('/users', { params: { page: 1 } });
const { data: newUser } = await api.post('/users', { name: 'hyun', age: 29 });
await api.put('/users/1', { name: 'newName' });
await api.delete('/users/1');

const [users, posts] = await Promise.all([
  api.get('/users'),
  api.get('/posts')
]);
```

## 핵심 3: 구조 분해, 스프레드, 옵셔널 체이닝
```js
const { data } = await axios.get('/api/user');
const token = localStorage.getItem('token') ?? 'no-token';
```
