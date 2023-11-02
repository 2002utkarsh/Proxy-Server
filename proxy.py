#Type this url to use the proxy server:    http://192.168.56.1:8888/www.google.com      
# 
# Type this in the terminal:               python proxyServerss.py 8888


from socket import *
import sys
import os


if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip port"')
    print('[server_ip: IP Address Of Proxy Server]')
    print('[port: Port of Proxy Server]')
    sys.exit(2)

server_port = int(sys.argv[1])

tcp_sock = socket(AF_INET, SOCK_STREAM)
tcp_sock.bind(('192.168.56.1', server_port))
tcp_sock.listen(1)

def change_file_name(filename):
    new_filename = "".join([c if c.isalnum() or c in "-_." else "_" for c in filename])
    return new_filename


url = ""

while 1:
    try: 
        print("#Server is waiting for connection...")
        
        tcp_cli_sock, addr = tcp_sock.accept()

        #Receiving data from the client
        print(f'\nReceived a connection from:  ({addr})')
        message = tcp_cli_sock.recv(1024).decode()
        print(message)

        if len(message) > 1:
            
            filename = message.split()[1].partition("/")[2]
            print(f"Filename = {filename}")
           

        chk_file_exist = False
        chk_domain = False
        search_file = ""

        if filename.startswith("www."):
            url = filename
            chk_domain = True
            print(f"domainName = {url}")

        else:
            search_file = filename.strip("/")
            print(f"searchFile = {search_file}")

        try:
            if chk_domain:
                file_path = os.path.join("./cache/",url, url)
            else:
                sanitized_filename = change_file_name(filename.strip("/"))
                file_path = os.path.join("./cache/", url,  sanitized_filename)

            print(f"file_path = {file_path}")
        
            with open(file_path, "rb") as f:
                outputdata = f.readlines()
                chk_file_exist = True
                print("Hit in cache")

            tcp_cli_sock.send("HTTP/1.0 200 OK\r\n".encode())
            tcp_cli_sock.send("Content-Type:text/html\r\n".encode())
            tcp_cli_sock.send("Connection: close\r\n".encode()) 

            for line in outputdata:
                tcp_cli_sock.send(line)
            tcp_cli_sock.send("\r\n".encode())
            tcp_cli_sock.close()

        except IOError:
            if chk_file_exist == False:
                c = socket(AF_INET, SOCK_STREAM)

                try:
                    c.connect((url, 80))

                    file_obj = c.makefile('rwb', 0)
                    file_obj.write(b"GET /" + search_file.encode() + b" HTTP/1.0\r\n\r\n")
                    
                    new_url_content = file_obj.readlines()
                    

                    if chk_domain:
                        file_path = os.path.join("./cache/", url, url)
                    else:
                        sanitized_filename = change_file_name(filename.strip("/"))
                        file_path = os.path.join("./cache/", url,  sanitized_filename)

                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(f"{file_path}", "wb") as f:
                        for line in new_url_content:
                            f.write(line)
                            tcp_cli_sock.send(line)

                except Exception as e:
                    print("...Illegal request...", e)

                c.close()

            else:
                    tcp_cli_sock.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode())

    except ConnectionAbortedError as e:
            print(e, "Retrying...")
            continue
    print()
    tcp_cli_sock.close()

tcp_sock.close()