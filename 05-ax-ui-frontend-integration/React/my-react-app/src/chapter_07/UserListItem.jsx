import React from "react";

function UserListItem(props) {
    const isOnline = useUserStatus(props.user.id);

    return (
        <li style={{color:isOnline ? 'green' : 'black'}}>
            {props.user.name}
        </li>
    );
}

export default UserListItem;
