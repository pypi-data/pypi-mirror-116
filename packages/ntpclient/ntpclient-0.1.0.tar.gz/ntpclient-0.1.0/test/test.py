import unittest
import socket
from NTP.ntpclient import Client

class TestServerConnection(unittest.TestCase):

    def setUp(self):
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.client = Client('127.0.0.1', '1234')
        
    def test_connection(self):
        connection = self.udp_socket.connect_ex(("127.0.0.1", 1234))
        self.assertEqual(connection, 0)

    def test_failed_message_to_server(self):
        self.udp_socket.sendto(str.encode("test"), ('127.0.0.1', 1234))
        server_message = self.udp_socket.recvfrom(1024)
        self.assertEqual(server_message[0].decode(), "Failed, Try again.")

    def test_exit_command_to_server(self):
        self.udp_socket.sendto(str.encode("exit"), ('127.0.0.1', 1234))
        server_message = self.udp_socket.recvfrom(1024)
        self.assertEqual(server_message[0].decode(), "Client Closed.")
    
    def test_get_time_message_to_server(self):
        self.udp_socket.sendto(str.encode("time"), ('127.0.0.1', 1234))
        server_message = self.udp_socket.recvfrom(1024)
        self.assertIsNotNone(server_message[0].decode)

    def test_host_port_control(self):
        self.client.host_port_control()
        self.assertIsNotNone(self.client.server_address)
