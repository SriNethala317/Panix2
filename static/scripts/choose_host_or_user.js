const host_button = document.querySelector('.host-button');
host_button.addEventListener('click', session_name);

const user_button = document.querySelector('.user-button');
user_button.addEventListener('click', user_connect_page);



// const user_button = document.querySelector('user-button');
// user_button.addEventListener('click', user_page);

function session_name(){
    window.location.pathname = "/html/session-name.html"
}

function user_connect_page(){
    window.location.pathname = "/html/user-connect-to-host.html"
}

// function user_page(){
    

// }