import socket
import pickle

def synchronize_chain(host, port):
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
    
    chain = pickle.loads(data)
    sock.close()
    
    return chain

def listen_for_requests(port, blockchain):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', port))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()

        # Recebimento da solicitação
        data = conn.recv(1024).decode()

        if data == 'GET_CHAIN':
            # Envio da cadeia de blocos em resposta à solicitação
            conn.sendall(pickle.dumps(blockchain.chain))

        conn.close()