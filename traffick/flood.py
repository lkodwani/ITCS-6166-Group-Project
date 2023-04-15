"""Generates synthetic traffic for testing."""
import os
import random as rand
import socket
import sys
import time

# run hostname to get the IP address of the server
DEFAULT_HOST = os.environ.get('HOSTNAME', 'localhost')
print('Using host: {}'.format(DEFAULT_HOST))
DEFAULT_PORT = 8080


def create_packet(type: str) -> bytes:
    """Create a packet of the given type (a, c, d, or v)."""
    type_bytes = type.encode('utf-8')
    return type_bytes + os.urandom(1024)


def send_packet(sock: socket.socket, packet: bytes) -> None:
    """Send a packet to the server."""
    sock.sendall(packet)


def setup_socket(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> socket.socket:
    """Create a socket and connect to the server."""
    print('Connecting to {}:{}...'.format(host, port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def verify_packet_type(packet: bytes, expected_type: str) -> None:
    """Verify that the packet is of the expected type."""
    if packet[0] != expected_type.encode('utf-8')[0]:
        raise Exception('Expected packet type {}, got {}'.format(
            expected_type, packet[0]))


def test_packet_types() -> None:
    """Test that the server responds with the correct packet type."""
    sock = setup_socket()
    for type in ['a', 'c', 'd', 'v']:
        packet = create_packet(type)
        send_packet(sock, packet)
        response = sock.recv(1024)
        verify_packet_type(response, type)
    sock.close()


def test_flood() -> None:
    """Test that the server can handle a flood of packets."""
    sock = setup_socket()
    for type in ['a', 'c', 'd', 'v']:
        packet = create_packet(type)
        for i in range(100):
            send_packet(sock, packet)
            response = sock.recv(1024)
            verify_packet_type(response, type)
    sock.close()


def test_flood_with_delay(random: bool) -> None:
    """
    Test that the server can handle a flood of packets with a delay.

    args:
        - random: boolean indicating whether to use a random delay
    """
    sock = setup_socket()
    for type in ['a', 'c', 'd', 'v']:
        packet = create_packet(type)
        for i in range(100):
            send_packet(sock, packet)
            response = sock.recv(1024)
            verify_packet_type(response, type)
            time.sleep(0.1 if not random else rand.randrange(0, 10) / 10)
    sock.close()


def connect_to_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> socket.socket:
    """Create a socket and connect to the server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def all_tests() -> None:
    """Run all tests."""
    test_packet_types()
    test_flood()
    test_flood_with_delay(False)
    test_flood_with_delay(True)


def main() -> None:
    """Run all tests and exit."""
    try:
        all_tests()
    except Exception as e:
        print('Test failed: {}'.format(e))
        sys.exit(1)
    else:
        print('All tests passed.')
        sys.exit(0)


if __name__ == '__main__':
    main()
