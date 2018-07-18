document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        //  emit a "add channel" event
        /*document.querySelector('#addChannel').onclick = () => {
            var channel_name = document.querySelector('#channel_name').value;
            if (channel_name) {
                socket.emit('add a channel', {'channel_name': [channel_name]});
            } else {
                alert("Please Insert a Name");
            }
        };*/


        // When a new vote is announced, add to the unordered list
        socket.on('added new channel', data => {
            const li = document.createElement('li');
            data.channel_list.forEach(function (channel) {
                li.innerHTML = "<a href='/chat-details/"+ channel + "'>"+channel+"</a>";
                document.querySelector('#channel_list').append(li);
            });

            $('#modalNewChannel').modal('toggle')
        });
    });








});
