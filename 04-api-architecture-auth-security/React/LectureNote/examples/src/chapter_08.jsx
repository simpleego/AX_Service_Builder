import React, { useState } from 'react';

export default function ConfirmPractice() {
  const [confirmed, setConfirmed] = useState(false);
  return <section>
    <p role="status">{confirmed ? '확인이 완료되었습니다.' : '확인이 필요합니다.'}</p>
    <button type="button" disabled={confirmed} onClick={() => setConfirmed(true)}>확인하기</button>
    <button type="button" disabled={!confirmed} onClick={() => setConfirmed(false)}>다시 확인</button>
  </section>;
}
