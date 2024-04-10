// window.addEventListener('beforeunload', () => {
//     const data = 'page-closed'
//     url = '/user-exits'
//     console.log('post to /user-exits')
//     navigator.sendBeacon(url, data)
//     if (!navigator.sendBeacon) {
//         navigator.sendBeacon = (url, data) =>
//             window.fetch(url, {method: 'POST', body: data, credentials: 'include'})
//       }
// })

const username_form = document.querySelector('.user-form')
username_form.addEventListener('submit', (e) =>{
    console.log('Submited username and session')
    e.preventDefault();
    let username_input = document.querySelector('.username-input');
    let session_name_input = document.querySelector('.session-name-input');
    if (username_input.value == "" || username_input.value == "ERROR1234567891011" || session_name_input.value == "ERROR1234567891011"){
        alert("Please Desired Session Name and username!");
    } else {
        let data = new FormData();
        data.username_input = username_input.value;
        data.session_name_input = session_name_input.value;
        fetch("/connect-user-to-session", {
            method: "POST",
            headers: new Headers({
                "Content-Type": "application/json"
            }), 
            body: JSON.stringify(data)

        })
        .then(Response => Response.json()).then(data =>{
            console.log("got server response for user connection " + data);
            if (data == 'ERROR1234567891011'){
                alert('Incorrect Session name. Try again');
            } else{
                if (data != username_input.value){
                    alert('Username is currently in use. Your assigned username is ' + data);
                } else{
                    console.log("connected to session as " + data);
                }
                window.location.pathname = './greeting-user'
            }

        })
    }

})