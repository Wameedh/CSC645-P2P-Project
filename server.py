########################################################################################################################
# Class: Computer Networks
# Date: 09/23/2020
# Lab6: TCP Server Socket
# Student Name: Wameedh Mohammed Ali
# Student ID: 920678405
# Student Github Username: wameedh
# Program Running instructions: python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import socket
import pickle
import sys
from threading import Thread

from uploader import Uploader


class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10 # keeps 10 clients in queue

    def __init__(self, host='0.0.0.0', port=5000):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TODO: create the server socket
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_handlers = [] # initializes client_handlers list



    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if successful, print the message "Server listening at ip/port"
        :return: VOID
        """
        #self.uploader = Uploader()
        try:
            self._bind()
            # your code here
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Listening at " + self.host + "/" + str(self.port))
            # self._bind()
            # self.serversocket.listen(self.MAX_NUM_CONN)
            # print("Listening at " + self.host + "/" + str(self.port))
            #
            # #thread uploader class
            # Thread(target=self.uploader.setUp, args=" ").start()
            # #request = self.receive()
            #
            # # Extract id from the request from the Peer
            # filter_key = ['id']
            # res = [request[key] for key in filter_key]
            # # Send request to Uploader
            # self.uploader.get_response(self)

        except socket.error as e:
            print("Error while listening for client %s" % e)
            self.serversocket.close()
            sys.exit(1)

    def _handler(self, tracker):
        """
        #TODO: receive, process, send response to the client using this handler.
        :param clienthandler:
        :return:
        """
        while True:
             # TODO: receive data from client
             # TODO: if no data, break the loop
             # TODO: Otherwise, send acknowledge to client. (i.e a message saying 'server got the data
             deserialized_data = self.receive(tracker)
             if not deserialized_data:
                 break
             # message = "Server got the data!"
             # self.send(tracker, message)
             ip = deserialized_data['ip']
             port = deserialized_data['port']
             log = "Connected: IP: " + str(ip) + ", Port: " + str(port)
             print(log)


    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
               tracker, addr = self.serversocket.accept()

               # TODO: from the addr variable, extract the client id assigned to the client
               # TODO: send assigned id to the new client. hint: call the send_clientid(..) method
              # client_id = addr[1]
              # self._send_clientid(clienthandler, client_id)
               self._handler(tracker) # receive, process, send response to client.
            except socket.error as e:
               # handle exceptions here
               print("Error accepting client %s" % e)
               self.serversocket.close()
               sys.exit(1)

    def _send_clientid(self, clienthandler, clientid):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        client_id = {'clientid': clientid}
        self.send(clienthandler, client_id)


    def send(self, clienthandler, data):
        """
        # TODO: Serialize the data with pickle.
        # TODO: call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        serialized_data = pickle.dumps(data)
        try:
            clienthandler.send(serialized_data)
        except socket.error as e:
            print("Error sending data %s" % e)
            self.serversocket.close()
            sys.exit(1)

    def receive(self,tracker, MAX_ALLOC_MEM=4096):
        """
        # TODO: Deserialized the data from client
        :param MAX_ALLOC_MEM: default set to 4096
        :return: the deserialized data.
        """
        try:
            data_from_client = tracker.recv(MAX_ALLOC_MEM)
        except socket.error as e:
            print("Error receiving data %s" % e)
            self.serversocket.close()
            sys.exit(1)
        if len(data_from_client) == 0:
            return None
        return pickle.loads(data_from_client)


    def getID(self):
        return {'ip_address': self.host, 'port': self.port}

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()

# main execution
# if __name__ == '__main__':
#     server = Server()
#     server.run()











