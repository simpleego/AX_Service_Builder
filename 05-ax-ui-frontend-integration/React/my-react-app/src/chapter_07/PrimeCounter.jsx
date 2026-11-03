import { useState, useMemo } from 'react';

// 1부터 n까지의 소수를 구하는 무거운 계산
function getPrimes(n) {
  console.log('소수 계산 실행');
  const primes = [];
  for (let i = 2; i <= n; i++) {
    let isPrime = true;
    for (let j = 2; j * j <= i; j++) {
      if (i % j === 0) { isPrime = false; break; }
    }
    if (isPrime) primes.push(i);
  }
  return primes;
}

function PrimeCounter() {
  const [limit, setLimit] = useState(100000);
  const [dark, setDark] = useState(false);

  // limit이 바뀔 때만 다시 계산합니다 (테마를 바꿀 때는 계산하지 않음)
  const primes = useMemo(() => getPrimes(limit), [limit]);

  return (
    <div style={{ background: dark ? '#222' : '#fff', color: dark ? '#fff' : '#000' }}>
      <input type="number" value={limit} onChange={e => setLimit(Number(e.target.value))} />
      <p>소수 개수: {primes.length}</p>
      <button onClick={() => setDark(d => !d)}>테마 전환</button>
    </div>
  );
}

export default PrimeCounter;