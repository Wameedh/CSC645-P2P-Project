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

    #TODO -
    # Downloader requests a block
    def send_request(self):





    # Call the file manager to save blocks
    def get_blocks(self):



    # Hash the peice


    # compare the hash with the one on the torrent file


    # send acknowledge


    # FILE_MANAGER:
        # 1- put them into a piece (8 blocks for ech piece)
        # 2- put pieces into a file


#     Ok let me explain:
# 1.	Once you receive a block (assuming it does not complete the piece) , create a pointer Hash_of(hash_info + piece_index + block_index)
# 2.	Put the block in the blocks file using this order: hash + delimiter + block_data
# 3.	repeat steps 1 && 2 until you receive a block that complete one piece (see bitfield)
# 4.	Call pointers = get_pointers(hash_info, piece_index) to get the pointers (hashes) of all the blocks for that piece.
# 5.	go to the blocks file and extract all the blocks that match with those hashes
