document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        //  emit a "add channel" event
        document.querySelector('#addChannel').onclick = () => {
            var channel_name = document.querySelector('#channel_name').value;
            if (channel_name) {
              document.querySelector('#channel_name').value = "";
                socket.emit('add-channel', {'channel_name': channel_name});
            } else {
                alert("Please Insert a Name");
            }
        };

        // When a new Channel is added
        socket.on('added-new-channel', data => {
            console.log(data);
            const li = document.createElement('li');
            const items = data.channel_list;
            items.forEach(function (channel) {
                li.innerHTML = "<a href='/chat-details/"+ channel + "'>"+channel+"</a>";
                document.querySelector('#channel_list').append(li);
            });
            $('#modalNewChannel').modal('hide')
        });
    });

    if (localStorage.getItem('current_channel') != "" && !sessionStorage.getItem('redirected')){
        sessionStorage.setItem('redirected', 1);
        window.location.href = "http://127.0.0.1:5000/chat-details/" + localStorage.getItem('current_channel');
    }
});
