// import { io } from "../../socket.io/socket.io.js";

const socket = io(); // sends socket "connect" msg to server
let sessionName;
console.log('io protocol: ', io.protocol);
localStorage.debug = 'socket.io-client:socket';

fetch('/get-session-name', {
    method:"GET"
}).then(Response => Response.json()).then(data => {
    sessionName = data;
    data = {"session_name": sessionName, "username": "HOST"};
    console.log("Session name: ", sessionName);
    socket.emit('join', data);
    // socket.on("connect", () =>{
    //     socket.emit('join', data);
    // })

    socket.on('logs', (data)=>{
        console.log('socketio logs data: ', data);
        let hostSongsText = document.querySelector('.host-songs-text');
        hostSongsText.textContent = data; 

    })

    socket.on('update', (data)=>{
        console.log('socketio update data: ', data);
    })

}).catch(error =>{
    console.log("Error fetching session Name: ", error);
})







