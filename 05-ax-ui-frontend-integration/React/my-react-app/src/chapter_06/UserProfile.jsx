import { useState, useEffect } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let ignore = false; // 이전 요청 응답이 늦게 도착해 덮어쓰는 것을 막습니다

    fetch(`https://jsonplaceholder.typicode.com/users/${userId}`)
      .then(res => res.json())
      .then(data => { if (!ignore) setUser(data); });

    return () => { ignore = true; };
  }, [userId]); // userId가 바뀔 때마다 다시 요청합니다

  if (!user) return <p>로딩 중...</p>;
  return (
        <>
            <h2>{user.name}</h2>
            <h2>{user.email}</h2>
        </>
    );
}

export default UserProfile;