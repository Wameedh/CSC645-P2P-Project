import pickle
from pwp import PWP
from file_manager import FileManager
from config import Config

class Uploader:

    def __init__(self, peer_id, server, peer_uploader, address, torrent):
        self.peer_id = peer_id
        self.config = Config()
        self.torrent = torrent
        self.file_manager = FileManager(peer_id=peer_id, torrent=torrent)
        self.peer_uploader = peer_uploader
        self.server = server
        self.address = address
        self.pwp = PWP()
        self.peer_id = -1
        self.uploaded = 0  # bytes
        self.downloaded = 0  # bytes

        #### implement this ####
        self.uploader_bitfield = None
        self.downloader_bitfield = None

    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.peer_uploader.send(serialized_data)

    def receive(self, max_alloc_mem=4096):
        serialized_data = self.peer_uploader.recv(max_alloc_mem)
        data = pickle.loads(serialized_data)
        return data

# When the client from P2 connects to P1, the server will create and thread the
# uploader class (like the clienthandler class)

# Uploader will communicate with the client of P2 directly, send request/response to
# each other (like the Menu in Client/Server)

# P2 will send a message saying it is interested in downloading the file

# P1 has two options to respond to the message from P2,
# self.choke(0) or self.un-choke (1)

# uploader needs to call the file manager

# self.uploader_bitfield is sending your bitfield to all the other peers in the network
# self.downloader_bitfield used to download the file for P2 and putting it into persistent storage

# Implementation:
# 1. Upload bitfield and send it to all the other peers in the network.
#          - The uploader needs access to the bitfield of other peers because it needs
#           to make sure that the block P2 is requesting is not being requested twice.
#
# 2. Listen for requests  <from Peer 2 (peer trying to download file)>
#       a) interested (1)
#       b) not interested (0)
#
# 3. If interested -> send response with
#       a) un-choke (1) <permission to download>
#       b) choke (0) <download not permitted>
#    else -> continue listening
#
# 4. Now listen for next request from Peer 2
#
# 5. Forward request to download from Peer 2 to File Manager
#       -> Request will contain a piece and a block
#       -> send downloader_bitfield
#
# 6. After the last block of the piece is sent to P2, others peers needs
#    to know that P2 completed the piece.

# Notes: Need to add code into the client.py so that uploader and client
# of P2 can have this communication?
