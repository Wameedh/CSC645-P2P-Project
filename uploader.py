# file:           uploader.py
# Author:         Nathalia Sainez

import pickle

from message import Message
from file_manager import FileManager
from config import Config

class Uploader:
    # peer_id, server, peer_uploader, address, torrent
    def __init__(self, server):
        # self.peer_id = peer_id
        self.config = Config()

        #forward requests to downloader
        self.downloader = Downloader()
        # self.torrent = torrent
        # self.file_manager = FileManager(peer_id=peer_id, torrent=torrent)
        # self.peer_uploader = peer_uploader
        self.server = server
        # self.address = address
        self.peer_id = -1
        self.uploaded = 0  # bytes
        self.downloaded = 0  # bytes
        self.message = Message()
        self.permitted = 0
        self.interest = 0

        self.uploader_bitfield = None
        self.downloader_bitfield = None

    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.server.send(serialized_data)

    def receive(self, max_alloc_mem=4096):
        serialized_data = self.server.recv(max_alloc_mem)
        data = pickle.loads(serialized_data)
        return data

    # sends initial uploader bitfield to all peers in network
    def setUp(self):
        self.uploader_bitfield = self.message.init_bitfield(200)  # this will create a bitfield of size 25.
        self.send(self.uploader_bitfield)

    def get_response(self, request, res):
        values = {
            0: self.choke(request),
            1: self.unchoke(request),
            2: self.interested(request),
            3: self.not_interested(request),
            4: self.piece_downloaded(request),
            # 5: self.bitfield,
            # 6: self.request,
            7: self.piece,
            8: self.cancel
        }
        return values.get(res, "Invalid ID")

    # Moved to the server class so we can forward the
    # requests here instead.
    #
    # def listen(self):
    #     while True:
    #         try:
    #             request = self.receive()
    #             filter_key = ['id']
    #             res = [request[key] for key in filter_key]
    #             self.get_response(res)
    #         except:
    #             print("Error")

    def choke(self, request):
        print("\nDownload not permitted")
        self.permitted = 0
        return 0

    def unchoke(self, request):
        print("\nDownload Permitted")
        if self.interest == 1:  # interested in downloading file
            self.permitted = 1
            filter_key = ['bitfield']
            res = [request[key] for key in filter_key]
            all_zero = res.all((arr == 0))
            if all_zero:
                print("Bitfield is empty. None of the file has been shared.")
            else:
                print("Bitfield contains at least one non-zero number: ")
                print(res)
                self.send(res)

    def interested(self, request):
        print("\nPeer interested in download file")
        self.interest = 1

    def not_interested(self, request):
        print("\nPeer not interested in downloading file")
        self.interest = 0

    def piece_downloaded(self, request):
        print("\npayload is a bitfield representing the pieces that have been successfully downloaded")
        if self.is_completed(request):
            self.downloader_bitfield = request
            self.send(self.downloader_bitfield)
        else:
            print("...")
    # ismissing = self.message.is_piece_missing()

    # def bitfield(self):
    #     print("\nBitfield")
    #
    # def request(self):
    #     print("request")
    # send to downloader

    def piece(self):
        print("piece")
        self.send(self.downloader_bitfield)

    def cancel(self):
        print("cancel")
        self.permitted = 0

    # After the last block of the piece is sent to P2, others peers needs
    # to know that P2 completed the piece.
    def is_completed(self, request):
        if self.message.is_piece_missing():
            not_completed = 0
        # send to the downloader
        all_zero = res.all((arr == 1))

        if all_zero:
            print("Bitfield contains all ones.")
            return true
        else:
            print("Bitfield contains at least one zero. ")
            print(res)
            return false

# When the client from P2 connects to P1, the server will create and thread the
# uploader class (like the clienthandler class)

# Uploader will communicate with the client of P2 directly, send request/response to
# each other (like the Menu in Client/Server)

# P2 will send a message saying it is interested in downloading the file

# P1 has two options to respond to the message from P2,
# self.choke(0) or self.un-choke (1)

# self.uploader_bitfield is sending your bitfield to all the other peers in the network
# self.downloader_bitfield used to download the file for P2 and putting it into persistent storage

# The uploader needs access to the bitfield of other peers because it needs
# to make sure that the block P2 is requesting is not being requested twice.

# TODO
# 1. Init bitfield
#    -> init_bitfield will initialize the bitfield with all the pieces set to missing: b'00000000'
# 2. Send bitfield to all the other peers in the network.

# 3. Listen for requests:  <from Peer 2 (peer trying to download file)>
#       a) interested
#       b) not interested
# 4. If interested -> send response w/
#       a) un-choke <permission to download>
#       b) choke <download not permitted>
#   else -> not interested

# self.choke = {'len': b'0001', 'id': 0}
# self.unchoke = {'len': b'0001', 'id': 1}
# self.interested = {'len': b'0001', 'id': 2}
# self.not_interested = {'len': b'0001', 'id': 3}

# 5. Now listen for next request from Peer 2

# 6. Forward request to download from Peer 2 to downloader
#       -> Request will contain a piece and a block
#       -> send blocks

# 7. After the last block of the piece is sent to P2, others peers needs
#    to know that P2 completed the piece.
#     def is_piece_missing(self, piece_index):
#         determines if a piece is missing (missing pieces has at least one block set to bit 0)
#         :param piece_index:
#         :return: True if the piece is missing. Otherwise, returns False
