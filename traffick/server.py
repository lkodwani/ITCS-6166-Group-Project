"""A simple server for packet flood testing."""
import os
import random as rand
import socket
import time
from typing import List, Tuple, Callable, Dict, Any
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
from aiohttp import web
import asyncio
import cv2 as cv
import json
import logging
import numpy as np
import socket


class Server:
    """A class to represent a server for packet flood testing."""

    def __init__(self, port: int) -> None:
        """Initialize a server."""
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', port))

    def run(self) -> None:
        """Run the server."""
        while True:
            data, addr = self.sock.recvfrom(1024)
            print('Received from {}: {}'.format(addr, data))
            self.sock.sendto(data, addr)


def main() -> None:
    """Run the server."""
    server = Server(8080)
    server.run()


if __name__ == '__main__':
    main()
