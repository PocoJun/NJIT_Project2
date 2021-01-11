import React from 'react';
import * as ReactDOM from 'react-dom';

import { Socket } from './Socket';
import { GoogleLogin } from 'react-google-login';
import { Content } from './Content';

const responseGoogle = (response) => {
    console.log(response);
}

function handleSubmit(response) {
    console.log(response.profileObj)
    console.log(response.profileObj.name);
    console.log(response.profileObj.email);
    
    let user = response.profileObj.name;
    let email = response.profileObj.email;
    let picture = response.profileObj.imageUrl;
    
    Socket.emit('new google user', {
        'user': user,
        'email': email,
        'picture': picture
    });
    
    console.log('Sent the name ' + user + ' to server!');
    console.log('Sent the email ' + email + ' to server!');
    console.log('Sent the picture ' + picture + ' to server!');
    ReactDOM.render(<Content/>, document.getElementById('content'));
}


export function GoogleButton() {
    return (
                <GoogleLogin
                className="gbutton"
                clientId="1095618364070-gn12nanh49q9maoagge55j1ijuh369uu.apps.googleusercontent.com"
                buttonText="Login with GOOGLE"
                onSuccess={handleSubmit}
                onFailure={responseGoogle}
                cookiePolicy={'single_host_origin'}/>
            );
}

 
