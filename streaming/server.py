from aiohttp import web
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRecorder
from aiortc.rtcrtpsender import RTCRtpSender
import asyncio
import cv2 as cv
import json
import os

peer_connection_set = set()


async def index(request: web.Request) -> web.Response:
    """
    Handle requests to the server root.

    args:
        - request: the request object
    """
    print(os.path.dirname(__file__))

    content = open(os.path.join(os.path.dirname(
        __file__), "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def js(request: web.Request) -> web.Response:
    """
    Handle requests to the server root.

    args:
        - request: the request object
    """

    content = open(os.path.join(os.path.dirname(
        __file__), "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def offer(request: web.Request) -> web.Response:
    """
    Handle requests to the /offer handler.

    args:
        - request: the request object
    """

    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    peer_connection_set.add(pc)

    @pc.on("datachannel")
    def on_datachannel(channel):
        """
        Called when a data channel is received from the remote peer.
        """
        @channel.on("message")
        def on_message(message):
            print("message from data channel:", message)

    @pc.on("track")
    def on_track(track):
        """
        Called when a track is received either from the remote peer or from the local peer.
        """
        print("Track %s received" % track.kind)

        if track.kind == "video":
            pc.addTrack(MediaStreamTrack())
        elif track.kind == "audio":
            player = MediaPlayer("default", format="pulse")
            pc.addTrack(player.audio)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


async def on_shutdown(app):
    """
    Closes all peer connections.
    """

    coroutines = [pc.close() for pc in peer_connection_set]
    await asyncio.gather(*coroutines)
    peer_connection_set.clear()


if __name__ == "__main__":
    camera = cv.VideoCapture(0)
    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_get("/client.js", js)
    app.router.add_post("/offer", offer)
    web.run_app(app)
