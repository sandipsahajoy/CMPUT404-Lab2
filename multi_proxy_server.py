import socket
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def handle_multi(addr, conn, proxy_end):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending recieved data {send_full_data} to google")
    proxy_end.sendall(send_full_data)
    data = proxy_end.recv(BUFFER_SIZE)
    conn.sendall(data)
    proxy_end.shutdown(socket.SHUT_WR)

def main():
    host = "www.google.com"
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Start Server")
        #QUESTION 3
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)
        
        #continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                #recieve data, wait a bit, then send it back
                print("Connnecting to Google")
                remote_ip = socket.gethostbyname(host)
                proxy_end.connect((remote_ip, port))
                p = Process(target=handle_multi, args=(addr, conn, proxy_end))
                p.start()

            conn.close()

if __name__ == "__main__":
    main()