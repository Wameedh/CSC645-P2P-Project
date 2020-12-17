# File: tracker.py
# Author: Raymond Au
# SID: 916672216
# Date: 11/2/2020
# Description: this file contains the implementation of the tracker class.

import bencodepy
import socket
import threading
import time

class Tracker:
    """
    This class contains methods that provide implementations to support trackerless peers
    supporting the DHT and KRPC protocols
    """

    def __init__(self, server, torrent, announce=True):
        """
        TODO: Add more work here as needed.
        :param server:
        :param torrent:
        :param announce:
        """
        self._server = server
        self._torrent = torrent
        self._is_announce = announce
        self.DHT_PORT = server.getID()['port']
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(('', self.DHT_PORT))
        # self._clienthandler = server.clienthandlers[0]
        # will story a list of dictionaries representing entries in the routing table
        # dictionaries stored here are in the following form
        # {'nodeID': '<the node id is a SHA1 hash of the ip_address and port of the server node and a random uuid>',
        #  'ip_address': '<the ip address of the node>', 'port': '<the port number of the node',
        #  'info_hash': '<the info hash from the torrent file>', last_changed': 'timestamp'}
        id = self._server.getID()
        nodeID = bencodepy.encode(id)
        self.nodeID = self._torrent._hash_torrent_info(nodeID)
        self._routing_table = [[self._server.host, self.DHT_PORT]]
        self.tokens = ["token"]

    def broadcast(self, message, self_broadcast_enabled=False):

        if (self.DHT_PORT == 5000):
            port = 5001
        if (self.DHT_PORT == 4999):
            port = 5000

        try:
            encoded_message = self.encode(message)
            self.udp_socket.sendto(encoded_message, ('<broadcast>', self.DHT_PORT))
            print("\nMessage broadcast.....")
        except socket.error as error:
            print(error)

    def send_udp_message(self, message, ip, port):
        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            message = self.encode(message)
            new_socket.sendto(message, (ip, port))
        except:
            print("error")

    def broadcast_listener(self):
        try:
            print("\nListening at DHT port: ", self.DHT_PORT)
            while True:
                raw_data, sender_ip_and_port = self.udp_socket.recvfrom(4096)
                print("STEP-1")
                if raw_data:
                    data = self.decode(raw_data)
                    ip_sender = sender_ip_and_port[0]
                    port_sender = sender_ip_and_port[1]
                    print("STEP-2")
                    self._routing_table.append([ip_sender, port_sender])
                    print("STEP-3")
                    print("\ndata received by sender {}:{}".format(ip_sender, port_sender))
                    #self.process_query(data)

        except:
            print("\nError listening at DHT port")

    def encode(self, message):
        """
        bencodes a message
        :param message: a dictionary representing the message
        :return: the bencoded message
        """
        return bencodepy.encode(message)


    def decode(self, bencoded_message):
        """
        Decodes a bencoded message
        :param bencoded_message: the bencoded message
        :return: the original message
        """
        return bencodepy.decode(bencoded_message)

    def ping(self, t, y, a=None, r=None):
        """
        TODO: implement the ping method
        :param t:
        :param y:
        :param a:
        :return:
        """
        """
        TODO: implement the ping method. 
        :return:
        """
        if (y == 'q'):
            query = {'t': t, 'y': y, 'q': 'ping',
                 'a': {'id': self._server.getIP()}}
            print("\nping Query = {}".format(query))
            print("bencoded = {}".format(self.encode(query)))
            return query

        if (y == 'r'):
            query = {'t': t, 'y': y,
                     'r': {'id': self._server.getIP()}}
            print("Response = {}".format(query))
            print("bencoded = {}".format(self.encode(query)))
            return query

    def find_node(self, t, y, a=None, r=None):
        """
        TODO: implement the find_node method
        :return:
        """
        if (y == 'q'):
            query = {'t': t, 'y': y, 'q': 'find_node',
                 'a': {'id': self._server.getIP(), 'target': ["127.0.0.1", 12001]}}
            print("find_node Query = {}".format(query))
            print("bencoded = {}".format(self.encode(query)))
            return query

        if (y == 'r'):
            query = {'t': t, 'y': y,
                     'r': {'id': self._server.getIP(), 'nodes': {'ip': self._server.getIP()['ip_address'], 'port': self._server.getIP()['port']}}}
            print("Response = {}".format(query))
            print("bencoded = {}".format(self.encode(query)))
            return query

    def get_peers(self, t, y, a=None, r=None):
        """
        TODO: implement the get_peers method
        :return:
        """
        if (y == 'q'):
            query = {'t': t, 'y': y, 'q': 'get_peers',
                'a': {'id': self._server.getIP(), 'info_hash': self._server.get_hash_info()}}
            print("get_peers Query = {}".format(query))
            print("bencoded = {}".format(self.encode(query)))
            return query

        if (y == 'r'):
            query = {'t': t, 'y': y,
                'r': {'id': self._server.getIP(), 'token': 'token', 'values': self._routing_table}}
            print("Response with closest nodes = {}".format(query))
            print("bencoded = {}".format(self.encode(query)))
            return query

    def announce_peer(self, t, y, a=None, r=None):
        """
        TODO: implement the announce_peers method
        :return:
        """
        if (y == 'q'):
            print(self.tokens[-1])
            query = {'t': t, 'y': y, 'q': 'announce_peer',
                'a': {'id': self._server.getIP(), 'info_hash': self._server.get_hash_info(), 'implied_port': 1,
                      'port': self._server.getIP()['port'], 'token': self.tokens[-1]}}
            if (query['a']['token'] in self.tokens):
                return query

        if (y == 'r'):
            query = {'t': t, 'y': y,
                'r': {'id': self._server.getIP()}}
            print("Response = {}".format(query))
            print("bencoded = {}".format(self.encode(query)))
            return query

    def process_query(self, data):
        """
        TODO: process an incoming query from a node
        :return: the response
        """
        if (data[b'y'] == b'q'):
            print("Query: ", data)
            if data[b'q'] == b'ping':
                message = self.ping('aa', 'r',)
                self.broadcast(message)
            if data[b'q'] == b'find_node':
                message = self.find_node('aa', 'r',)
                self.broadcast(message)
            if data[b'q'] == b'get_peers':
                message = self.get_peers('aa', 'r',)
                self.broadcast(message)
            if data[b'q'] == b'announce_peer':
                message = self.announce_peer('aa', 'r',)
                self.broadcast(message)
        if (data[b'y'] == b'r'):
            print("Response: ", data)
            try:
                if (data[b'r'][b'token']):
                    self.tokens.append(data[b'r'][b'token'])
            except:
                pass
        pass

    def run(self, start_with_broadcast=True):
        """
        TODO: This function is called from the peer.py to start this tracker
        :return: VOID
        """
        if (self.DHT_PORT == 12001):
            start_with_broadcast = False

        if self._is_announce:
            threading.Thread(target=self.broadcast_listener).start()
            if start_with_broadcast:
                message = self.ping('aa', 'q')
                self.broadcast(message, self_broadcast_enabled=True)
                time.sleep(1)
                message = self.find_node('aa', 'q')
                self.broadcast(message, self_broadcast_enabled=True)
                time.sleep(1)
                message = self.get_peers('aa', 'q')
                self.broadcast(message, self_broadcast_enabled=True)
                time.sleep(1)
                message = self.announce_peer('aa', 'q')
                self.broadcast(message, self_broadcast_enabled=True)
        else:
            print("This tracker does not support DHT protocol")



