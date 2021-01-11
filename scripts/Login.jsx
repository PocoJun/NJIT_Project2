import * as React from 'react';

import { GoogleButton } from './GoogleButton';
import { Socket } from './Socket';

export function Login() {
    
    return (
    <div>
        <img className="img" src= "static/mail.jpg"/>
        
        <div className="OuterContainer">
            <div className="InnerContainer">
            <h3>Sign in with Google Please login your GOOGLE ID!</h3>
                <GoogleButton/>
            </div>
        </div>
    </div>
    );
}