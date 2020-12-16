import hashlib
import threading
from file_manager import FileManager


class Downloader:

    def __init__(self, peer_downloader, peer_id, torrent, pwp, interested, keep_alive):
        self.peer_downloader = peer_downloader
        self.peer_id = peer_id
        self.torrent = torrent
        self.uploader_id = -1  # not know until the downloader runs.
        self.info_hash = self.torrent.info_hash()
        self.pwp = pwp
        self.alive = keep_alive
        self.interested = interested
        self.file_manager = FileManager(self.torrent, self.peer_id)
        self.bitfield_lock = threading.Lock()
        self.file_lock = threading.Lock()

   #TODO - STEPS
    # 1- find the uploader
    # 2- request pieces from the uploader
    # 3- receive blocks

    # #TODO -
    # # Downloader requests a block
    # def send_request(self):
    #     return self.interested
    #
    #
    #
    #
    #
    # #Call the file manager to save blocks
    # def get_blocks(self):
    #
    #    #calls the  FileManager
    #
    #
    #
    # # Hash the piece
    # def hash(self, piece):
    #     sha1 = hashlib.sha1()
    #     sha1.update(piece)
    #     hashed_piece = sha1.hexdigest()
    #     return hashed_piece
    #
    #
    # # compare the hash with the one on the torrent file
    # def validate_hashed_piece(self, hash):
    #     return self.torrent.info_hash() == hash
    #
    #

    # send acknowledge




    # FILE_MANAGER:
        # 1- put them into a piece (8 blocks for ech piece)
        # 2- put pieces into a file

