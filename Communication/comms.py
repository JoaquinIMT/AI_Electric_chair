from socket import socket


class HttpServer():
    def __init__(self):
        self.host_ip = "127.0.0.1"
        self.port = 65432

    def open_comm(self):        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.bind((self.host_ip,self.port))
        self.s.listen()


class HttpSender():
    def __init__(self):
        pass