// set up the peer connection, local video, and remote video elements
var peerConnection = null;
var localVideo = document.querySelector("video#localVideo");
var remoteVideo = document.querySelector("video#remoteVideo");

function negotiate() {
    peerConnection.createOffer().then(function (offer) {
        return peerConnection.setLocalDescription(offer);
    })
        .then(function () {
            // waits for the ICE (Interactive Connectivity Establishment) gathering to complete
            return new Promise(function (resolve) {
                if (peerConnection.iceGatheringState === "complete") {
                    resolve();
                } else {
                    function checkState() {
                        if (peerConnection.iceGatheringState === "complete") {
                            peerConnection.removeEventListener("icegatheringstatechange", checkState);
                            resolve();
                        }
                    }
                    peerConnection.addEventListener("icegatheringstatechange", checkState);
                }
            }
            );
        }).then(function () {
            var offer = peerConnection.localDescription;
            // fetch the json-encoded offer from the server
            return fetch("/offer", {
                body: JSON.stringify({
                    sdp: offer.sdp,
                    type: offer.type,
                }),
                headers: {
                    "Content-Type": "application/json"
                },
                method: "POST"
            });
        }).then(function (response) {
            // wait for the response
            return response.json();
        }
        ).then(function (answer) {
            // set the remote description
            return peerConnection.setRemoteDescription(answer);
        }
        ).catch(e => console.log(e));
}

function start() {
    var config = {
        iceServers: [
            {
                urls: "stun:stun.l.google.com:19302"
            }
        ],
        sdpSemantics: "unified-plan"
    };
    peerConnection = new RTCPeerConnection(config);
    // local video requires some track management
    peerConnection.srcObject.getVideoTracks().forEach(function (track) {
        peerConnection.addTrack(track, peerConnection.srcObject);
    });
    // when the remote stream arrives, show it in the remote video element
    peerConnection.addEventListener("track", function (event) {
        if (event.track.kind == "video") {
            remoteVideo.srcObject = event.streams[0];
        }
    }
    );
    // start the negotiation immediately on page load
    negotiate();
}

function gotStream(stream) {
    localVideo.srcObject = stream;
    peerConnection.srcObject = stream;
    start();
}

function init() {
    navigator.mediaDevices.getUserMedia({
        audio: true,
        video: true
    }).then(gotStream).catch(e => console.log(e));
}

function stop() {
    peerConnection.close();
    peerConnection = null;
    localVideo.srcObject = null;
    remoteVideo.srcObject = null;
}

init();

