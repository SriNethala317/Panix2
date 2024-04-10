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

let user_leave_btn = document.querySelector('.user-leave-btn')
user_leave_btn.addEventListener('click', () => {
    data = 'user-exit'
    fetch('/user-exits', {
        method: "POST",
        headers: new headers({
            "Content-Type": "application/json"
        }),
        body: JSON.stringify(data)
    }).then(Response => Response.json()).then(data => {
        window.location.pathname='/'
    })
})

let spotify_btn = document.querySelector('.spotify-btn')
spotify_btn.addEventListener('click', () =>{
    fetch('/get-spotify-auth-url', {
        method:"GET"
    }).then(Response => Response.json()).then(data => {
        window.open(data, "_self")

    })
})