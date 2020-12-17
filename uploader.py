import pickle

from message import Message
from file_manager import FileManager
from config import Config


class Uploader:
    # peer_id, server, peer_uploader, address, torrent
    def __init__(self, server):
        # self.peer_id = peer_id
        self.config = Config()
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

        #### implement this ####
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

    def get_response(self, res):
        values = {
            0: self.choke,
            1: self.unchoke,
            2: self.interested,
            3: self.not_interested,
            4: self.piece_downloaded,
            # 5: self.bitfield,
            # 6: self.request,
            7: self.piece,
            8: self.cancel
        }
        return values.get(res, "Invalid ID")

    # def listen(self):
    #     while True:
    #         try:
    #             request = self.receive()
    #             filter_key = ['id']
    #             res = [request[key] for key in filter_key]
    #             self.get_response(res)
    #         except:
    #             print("Error")

    def choke(self):
        print("\nDownload not permitted")
        self.permitted = 0
        return 0

    def unchoke(self):
        print("\nDownload Permitted")
        if self.interest == 1:  # interested in downloading file
            self.permitted = 1


    def interested(self):
        print("\nPeer interested in download file")
        self.interest = 1

    def not_interested(self):
        print("\nPeer interested in downloading file")
        self.interest = 0

    def piece_downloaded(self):
        print("\npayload is a bitfield representing the pieces that have been successfully downloaded")
        ismissing = self.message.is_piece_missing()


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

    #    After the last block of the piece is sent to P2, others peers needs
    #    to know that P2 completed the piece.
    def is_completed(self):
        if self.message.is_piece_missing():
            not_completed = 0
        # send to the downloader

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
#
# 5. Now listen for next request from Peer 2
#
# 6. Forward request to download from Peer 2 to downloader
#       -> Request will contain a piece and a block
#       -> send blocks
#
# 7. After the last block of the piece is sent to P2, others peers needs
#    to know that P2 completed the piece.
#     def is_piece_missing(self, piece_index):
#         determines if a piece is missing (missing pieces has at least one block set to bit 0)
#         :param piece_index:
#         :return: True if the piece is missing. Otherwise, returns False
