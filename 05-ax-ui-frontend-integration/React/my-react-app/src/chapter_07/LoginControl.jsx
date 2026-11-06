import LoginButton from "./LoginButton";
import LogoutButton from "./LogoutButton";
import Greeting from "./Greeting";

import {useState} from "react";

function LoginControl(props) {
    const [isLoggedIn, setIsLoggedIn] = useState(true);

    const handleLoginClick = ()=> {
        setIsLoggedIn(true);
    }

    const handleLogoutClick = () => {
        setIsLoggedIn(false);
    }

    let button;

    if(!isLoggedIn) {
        button = <LogoutButton onClick={handleLogoutClick}/>;
        
    }else {
        button = <LoginButton onClick={handleLoginClick}/>;
    }

    return (
        <div>
            <Greeting isLogggedIn={isLoggedIn}/>
            {button}
        </div>
    )
}

export default LoginControl;