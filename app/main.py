import socket  # noqa: F401

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Create a socket that will listen on localhost, port 4221
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to localhost and port 4221
    server_socket.bind(("localhost", 4221))
    
    # Listen for incoming connections (max 1 connection at a time)
    server_socket.listen(1)
    print("Server is listening on port 4221...")
    
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    
    # Send the HTTP response
    response = b"HTTP/1.1 200 OK\r\n\r\n"
    client_socket.sendall(response)
    
    # Close the client connection
    client_socket.close()
    
    # Close the server socket
    server_socket.close()

if __name__ == "__main__":
    main()

