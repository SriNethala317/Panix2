let add_songs_queue_form = document.querySelector('.add-songs-popup-form');
add_songs_queue_form.addEventListener('submit', function (event){
    event.preventDefault();
    addSongsToQueue();
});

let cancel_popup_btn = document.querySelector('.cancel-popup-btn');
cancel_popup_btn.addEventListener('click', closePopup)

let go_to_spotify_btn = document.querySelector('.go-to-spotify-btn');
go_to_spotify_btn.addEventListener('click', goToSpotify);

let popup_btn = document.querySelector('.popup-btn');
popup_btn.addEventListener('click', openPopup);



function addSongsToQueue(){
    let data = document.querySelector('.number-of-songs').value;
    let error_display = document.querySelector('.popup-error-msg');
    error_display.style.display = 'none';
    console.log('data is: ' + data);
    if(data == null || data <= 0){
        error_display.style.display = 'block';
        error_display.textContent = "Error: you haven't entered a valid number"
    } else{
        fetch('/add-spotify-songs-to-Queue', {
            method:"POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        }).then(Response => Response.json()).then(data =>{
            if(data === 'Error: no songs selected') {
                error_display.style.display = 'block';
                error_display.textContent = data;
            } else {
                console.log(data)
                closePopup();

                const songsList = document.querySelector('.songs-list');
                //makes string into list of dictionaries
                const listOfSongs = JSON.parse(data);
                listOfSongs.forEach(song => {
                    //creates container for image and the artist
                    const songContainer = document.createElement('div');
                    songContainer.className = 'song-container';

                    //creates image element
                    const songImage = document.createElement('img');
                    songImage.className = 'song-image';
                    songImage.src = song.image_url;
                    songImage.alt = song.song_name;
                    songContainer.appendChild(songImage);

                    const songText = document.createElement('div');
                    songText.className = 'song-text'
                    const songName = document.createElement('h3');
                    songName.className = 'song-name';
                    songName.textContent = song.song_name;
                    const artistName = document.createElement('h4');
                    songName.className = 'artist-name';
                    artistName.textContent = song.artist_name;

                    songText.appendChild(songName);
                    songText.appendChild(artistName);
                    songContainer.appendChild(songText);

                    songsList.appendChild(songContainer);

                });

            }
    
        })
    }
}

function closePopup(){
    document.querySelector('.popup-error-msg').style.display = 'none';
    document.querySelector('.add-songs-popup').style.display = 'none';
    document.querySelector('.overlay').style.display = 'none';
}

function goToSpotify(){
    window.open("https://open.spotify.com/", "_blank")
}

function openPopup(){
    document.querySelector('.add-songs-popup').style.display = 'flex';
    document.querySelector('.overlay').style.display = 'block';
}