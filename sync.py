import socket
import pickle

def synchronize_chain(self, host, port):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
       
        request = 'GET_CHAIN'
        sock.sendall(request.encode())
       
        data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        
        self.chain = pickle.loads(data)

        sock.close()