const session_name_form = document.querySelector('.session-name-form');
const audio = document.createElement("audio");

session_name_form.addEventListener('submit', (e) =>{
    e.preventDefault();
    let session_name_input = document.querySelector('.session-name-input');
    if (session_name_input.value == ""){
        alert("Please Desired Session Name!")
    } else{
        let data = new FormData();
        console.log("Posted to server " + session_name_input.value);
        data.session_name_input = session_name_input.value;
        if (audio.canPlayType("audio/mpeg")){
            data.audio_type = "mp3";
        } else if (audio.canPlayType("audio/ogg")){
            data.audio_type = "ogg";
        } else {
            console.log("Music isn't supported on this browser");
            data.audio_type = "mp3";
        }
        fetch("/create-session", {
            method: "POST",
            headers: new Headers({
                "Content-Type": "application/json"
            }), 
            body: JSON.stringify(data)
        }).then(Response => Response.json()).then(data =>{ 
            console.log("will do alert")
            if (data != session_name_input.value){
                alert("Your Session Name " + session_name_input.value +  " is already taken. Your Session is " + data);
            } else{
                console.log("Your session Name is " + data);
            }
            window.location.pathname = '/home';
        })
    }
});