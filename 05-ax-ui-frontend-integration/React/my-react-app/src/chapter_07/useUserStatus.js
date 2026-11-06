import React, { useState, useEffect } from "react";

function useUserStatus (props) {
    const [isOnline, setIsOnline ] = useState(null);

    function handleStatusChange(status) {
        setIsOnline(status.inOnline);
    }

    useEffect(()=>{
        ServerAPI.subscribeUserStatus(props.user.id, handleStatusChange);
        return () => {
            ServerAPI.unsubscribeUserStatus(props.user.id, handleStatusChange);
        };
    });

    return isOnline;

}

export default useUserStatus