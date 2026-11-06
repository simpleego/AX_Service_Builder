import React, { useState, useEffect } from "react";
import useCounter from "./useCounter";

const MAX_CAPCITY = 10;

function Accommodate(props) {
    const [isFull, setIsFull] = useState(false);
    const [count, increseCount, decreaseCount] = useCounter(0);

    useEffect(() => {
        console.log("====================");
        console.log("useEffect() is called");
        console.log(`isFull: ${isFull}`);
    });

    useEffect(() => {
        setIsFull(count >= MAX_CAPCITY);
        console.log(`Current count value: ${count}`);
    },[count]);

    return (
        <div style={{padding:100}}>
            <p>{`총 ${count} 명 수용했습니다.`}</p>
            
            <button onClick={increseCount} disabled={isFull}>
                입장
            </button>
            <button onClick = {decreaseCount}>퇴장</button>

            {isFull && <p style={{color:"red"}}>정원이 가득찼습니다.</p>}
        </div>
    );
}

export default Accommodate;