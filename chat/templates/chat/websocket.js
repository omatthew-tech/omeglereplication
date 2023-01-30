// Send a message to the other client
function sendMessage(type, message) {
    // Open a WebSocket connection to the server
    var socket = new WebSocket('ws://${window.location.host}/ws/chat/${room_name}/');
  
    // Send the message when the WebSocket connection is open
    socket.addEventListener('open', function(event) {
      socket.send(JSON.stringify({
        type: type,
        message: message.toString()
      }));
    });
  }
  
  // Receive an offer from the other client
  function receiveOffer(callback) {
    // Open a WebSocket connection to the server
    var socket = new WebSocket('ws://${window.location.host}/ws/chat/${room_name}/');
  
    // Call the callback with the offer when a message is received
    socket.addEventListener('message', function(event) {
      var data = JSON.parse(event.data);
      if (data.type === 'offer') {
        callback(data.message);
      }
    });
  }
  