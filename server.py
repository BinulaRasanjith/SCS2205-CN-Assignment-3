from socket import socket, AddressFamily, SocketKind
from os import path, getcwd

LOCALHOST = '127.0.0.1'
PORT = 2728


# AF_INET -> ipv4, SOCK_STREAM -> TCP/IP protocol
server_socket = socket(AddressFamily.AF_INET, SocketKind.SOCK_STREAM)
print('Serever socket created successfully')

# bind ip & port into the socket
server_socket.bind((LOCALHOST, PORT))
print(f'Socket is binded to Port: {PORT}')

# start listning in the socket
server_socket.listen()
print('Socket is listning...')

# starting a infinite loop for server to keep responding to the client
while True:
    # accepting the connection with the client
    client_socket, client_address = server_socket.accept()
    print("Got connected from ", client_address)

    # getting the request from the client
    client_request = client_socket.recv(1024).decode(errors='ignore')

    # splitting http headers from the request and store it in a array
    http_headers = client_request.split('\r\n')

    # getting 1st header of the client request and split it from spaces
    http_header_0 = http_headers[0].split(' ')

    try:  # using try-except to catch the errors
        # getting the http url from the 1st header
        http_url = http_header_0[1]

        # removing any queries from the url
        http_path = http_url.split('?')[0]

        # if http_path endswith '/' remove it
        if http_path.endswith('/'):
            http_path = http_path[:-1]
        print(http_path)

        # spliting http_path from '.'
        path_seg = http_path.split('.')

        if http_path != '':  # if http_path is not a empty string
            if len(path_seg) > 1:  # if there are '.' there could be an extension in the path
                # therefore resource path is relevent resource from the htdocs folder
                resource_path = path.join(getcwd(), 'htdocs', http_path[1:])

            else:  # if there is no '.' in the path add '.html' to the http path
                resource_path = path.join(
                    getcwd(), 'htdocs', f'{http_path[1:]}.html')

        else:  # if the http_path is a empty string give the index.html as the resource path
            resource_path = path.join(getcwd(), 'htdocs', 'index.html')
        print(resource_path, '\n-----------------------------')

        try:  # using try-except to catch the errors
            # opening the relevent resource
            resource = open(resource_path, 'r')
            # reading the resource content and store it ina variable
            resource_content = resource.read()
            resource.close()
            # storing the response from the resource content
            http_response = f'HTTP/1.1 200 OK\r\n\n{resource_content}'
            # sending the response encoded to the client
            client_socket.sendall(http_response.encode())
        except FileNotFoundError:  # if the resource not found, show file not found
            client_socket.sendall('HTTP/1.1 404 Not Found'.encode())
    except IndexError:  # ifthere is an index error, show bad request
        client_socket.sendall("HTTP/1.1 400 Bad Request".encode())
    client_socket.close()
