#######################################################################
# File:             client.py
# Author:           Wameedh Mohammed Ali
# Description:      Client class. A client socket that connects to a server socket who is already listening for request.
# Running:          Python 2: python client.py
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle
from client_helper import ClientHelper


class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constractpr
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = 0
        self.userInfo = {}

    def bind(self, client_ip, client_port):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.clientSocket.bind((client_ip, client_port))

    def set_info(self):
        host = input("Enter the server IP Address: ")
        port = input("Enter the server port: ")
        name = input("Your id key (i.e. your name): ")
        self.userInfo = {'host': host, 'port': int(port), 'name': name}

    def set_client_id(self):
        """
        Sets the client id assigned by the server to this client after a succesfull connection
        :return:
        """
        data = self.receive()  # deserialized data
        client_id = data['clientid']  # extracts client id from data
        self.client_id = client_id  # sets the client id to this client
        print("Successfully connected to server: " + self.userInfo['host'] + " / " + str(self.userInfo['port']))
        print("Your client info is:\n" + "Client Name: " + self.userInfo['name'] + "\nClient ID: " + str(client_id))

    def send_user_Name(self):
        name = self.userInfo['name']
        self.send(name)

    def connect(self, host, port):
        """
        TODO: Connects to a server. Implements exception handler if connection is resetted.
	    Then retrieves the cliend id assigned from server, and sets
        :param host:
        :param port:
        :return: VOID
        """
        try:
            print("Connecting...")
            self.clientSocket.connect((host, port))
        except socket.error as exc:
            print("Caught exception socket.error : %s" % exc)
            self.close()

        # Once the client creates a successful connection, the server will send the client id to this client.
        #self.set_client_id()
        #self.send_user_Name()
        # clientHelper = ClientHelper(self.clientSocket, self.client_id, "Wameedh")
        # while True:  # client is put in listening mode to retrieve data from server.
        #     data = self.receive()
        #     if not data:
        #         break
        #     # do something with the data
        #     clientHelper.process(data)
        # self.close()

    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data)  # serialized data
        self.clientSocket.send(data)

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        TODO: Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = self.clientSocket.recv(MAX_BUFFER_SIZE)  # deserializes the data from server
        return pickle.loads(raw_data)

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        # self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()


# if __name__ == '__main__':
#     # server_ip_address = "127.0.0.1"  # don't modify for this lab only
#     # server_port = 12000  # don't modify for this lab only
#     client = Client()
#     client.set_info()
#     server_ip_address = client.userInfo['host']
#     server_port = client.userInfo['port']
#     client.connect(server_ip_address, server_port)
