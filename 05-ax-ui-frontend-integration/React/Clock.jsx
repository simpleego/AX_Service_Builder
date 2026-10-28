
import React, { useState, useEffect } from "react";

function Clock() {
    // 현재 시간을 상태로 관리
    const [time, setTime] = useState(new Date());

    // 컴포넌트가 마운트되면 타이머 시작
    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date()); // 1초마다 상태 변경
        }, 1000);

        // 컴포넌트가 언마운트되면 타이머 제거
        return () => clearInterval(timer);
    }, []);

    return (
        <div>
            <h1>안녕, 리액트!</h1>
            <h2>현재 시간: {time.toLocaleTimeString()}</h2>
        </div>
    );
}

export default Clock;
