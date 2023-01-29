// chat/static/chat/js/webrtc.js
var socket = new WebSocket('ws://' + window.location.host + '/ws/stream/');

socket.onmessage = function(event) {
  var data = JSON.parse(event.data);

  switch (data.type) {
    case 'offer':
      receiveOffer(data.offer);
      break;
    case 'answer':
      receiveAnswer(data.answer);
      break;
  }
};

function sendMessage(type, payload) {
  socket.send(JSON.stringify({
    type: type,
    payload: payload
  }));
}

// chat/templates/chat/room.html
<script src="{% static 'chat/js/webrtc.js' %}"></script>

<script>
  // Create a media stream
  navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(function(stream) {
      // Display the local video stream
      document.querySelector('#local-video').srcObject = stream;

      // Create a RTCPeerConnection
      var pc = new RTCPeerConnection();

      // Share the media stream
      pc.addStream(stream);
      pc.createOffer().then(function(offer) {
        pc.setLocalDescription(offer);
        sendMessage('offer', offer);
      });

      // Receive the offer
      pc.ontrack = function(event) {
        document.querySelector('#remote-video').srcObject = event.streams[0];
      };
      receiveOffer(function(offer) {
        pc.setRemoteDescription(offer);
        pc.createAnswer().then(function(answer) {
          pc.setLocalDescription(answer);
          sendMessage('answer', answer);
        });
      });
    });
</script>
