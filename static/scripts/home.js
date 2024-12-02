const socket = io(); // sends socket "connect" msg to server
let sessionName;
let songList = []
let currSong = null; // songList index
let audio_type = ""
let audio = document.createElement("audio")

if (audio.canPlayType("audio/mpeg")){
    audio_type = "mp3";
} else if (audio.canPlayType("audio/ogg")){
    audio_type = "ogg";
} else {
    console.log("Music isn't supported on this browser");
}

fetch('/get-session-name', {
    method:"GET"
}).then(Response => Response.json()).then(data => {
    sessionName = data;
    data = {"session_name": sessionName, "username": "HOST"};
    console.log("Session name: ", sessionName);
    socket.emit('join', data);

    socket.on('logs', (data)=>{
        console.log('socketio logs data: ', data);
        let hostSongsText = document.querySelector('.host-songs-text');
        hostSongsText.textContent = data; 

    })

    socket.on('update', (data)=>{
        // console.log('socketio update data: ' + data);
        // console.log('type: ', typeof(data))
        // console.log(JSON.parse(data))
        let updatedSongList = JSON.parse(data)
        updatedSongList.forEach(song => {
            console.log('song: ', song)
        });
        handleSongUpdate(updatedSongList)
    })

}).catch(error =>{
    console.log("Error fetching session Name: ", error);
})

async function handleSongUpdate(updatedSongList){
    if (songList.length === 0){
        songList = updatedSongList;
        console.log('songList: ', songList);
    } else {
        let currDBSongPos = songList[songList.length-1]['songNo'];
        let updatedDBSongPos = updatedSongList[0]['songNo'];
        console.log('curr db song pos: ', currDBSongPos);
        console.log('updated db pos: ', updatedDBSongPos);
        updatedDBSongPos += currDBSongPos - updatedDBSongPos;
        console.log('update updatedDBSongPos: ', updatedDBSongPos);
        console.log(updatedSongList[updatedDBSongPos]);
        // check if songNo is the same
        if (songList[currDBSongPos]['songNo'] === updatedSongList[updatedDBSongPos]['songNo']){
            songList.concat(updatedSongList.slice(updatedDBSongPos+1));
        }
        console.log('updated songlist: ', songList);
    }

}







