#simple python-based proxy server using socketserver
import random
import socket
import socketserver
import ipaddress
import re
Addresses = ["1.2.3.4", "5.6.7.8", "9.10.11.12"]

class ProxyHandler(socketserver.BaseRequestHandler):
    data = None
    def handle(self):
        print("choosing ip")
        ip_address = random.choice(Addresses)
        # with open("ranges.txt",'r') as ranges:
        #     #rstrip removes any extra spaces or newline characters from the file contents
        #     #maxsplit splits the file contents into a list with a maximum of two elements
        #     contents = ranges.read().rstrip()
        #     first_ip, last_ip = contents.split(" ", maxsplit=1)
        # print('try')
        try:
            # generate a random ip address within the range
            ip_str = "192.168.0.1"
            # ip_range = ipaddress.summarize_address_range(ipaddress.IPv4Address(first_ip),
            #                                              ipaddress.IPv4Address(last_ip))
            # if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_range):
            #     raise ValueError("Invalid IP address format: %s" % ip_range)
            # print('ip_range ok')
            # ip_network = list(ip_range)[ 0 ]
            # ip_addresses = list(ip_network.hosts())
            # ip_address = random.choice(ip_addresses)
            # print("Selected IP: %s" % ip_address)

            self.data = self.request.recv(1024).strip()
            print("Received data from the client %s" % self.data)
            # self.request is the TCP socket connected to the client
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip_address, 0))
            print("Local address: %s:%d" % server_socket.getsockname())
            print("Client allocated the ip: %s", ip_address)
            server_socket.connect(("server.com", 80))
            server_socket.sendall(self.data)
            print("Sending data to the sever: %ds" % self.data)
            # send the data to the server

            server_response = server_socket.recv(1024)
            server_socket.close()
            # recieve data from the server

            self.request.sendall(server_response)
            # send the data back to the client
        except Exception as e:
            print("Error: ", e)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    try:
        server = socketserver.TCPServer((HOST, PORT), ProxyHandler)
        print("Server Running on Port: ", PORT)
        # create the server, binding to the localhost on port 8080
        server.serve_forever()
        # acticate the server deamon
    except Exception as e:
        print("Error Connecting to the server:", e)

# with open("ip", 'r') as infile:
#     with open("ranges.txt",'w')as outfile:
#         for line in infile:
#             columns = line.split()
#             first_ip = columns[1]
#             last_ip = columns[2]
#             outfile.write(first_ip + ' ' + last_ip + '\n')

